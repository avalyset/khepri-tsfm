"""Baseline arms with the Khepri v1.5 code and hyperparameters unchanged.

khepri.forecast.eval_split returns only metric rows, so this driver repeats its loop
(forecast.py:178-222) line for line, calling the same v1.5 functions, and keeps the
hourly predictions. Two additions, both declared in DEVIATIONS before PREREG:
SARIMA quantiles come from the same fitted model's Gaussian predictive distribution
(get_forecast; its predicted_mean equals forecast(H)), and a seasonal-naive (weekly)
arm, f(o+h) = y(o+h-168h), which v1.5 does not have.
"""

import logging

import numpy as np
import pandas as pd
from scipy.stats import norm

from khepri import forecast as fc
from khepri_tsfm.common import QLEVELS

log = logging.getLogger(__name__)
H = fc.H
Z = norm.ppf(QLEVELS)


def fit_sarima(hist, train_end):
    """forecast.py:186-195."""
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX
        tr = hist.loc[:train_end]
        return SARIMAX(tr, order=(2, 0, 1), seasonal_order=(1, 1, 0, 24),
                       enforce_stationarity=False, enforce_invertibility=False
                       ).fit(disp=False, maxiter=50)
    except Exception as e:
        log.warning("SARIMA fit failed: %r", e)
        return None


def fit_gbm(hist, train_end):
    """forecast.py:197-199."""
    train_origins = fc.gbm_train_origins(hist, train_end)
    return fc.build_gbm(hist, train_origins) if train_origins else None


def sarima_origin(fitted, hist, o):
    """forecast.py:202-220, plus quantiles. Returns (point, quantiles (H,Q), fallback)."""
    WIN = pd.Timedelta(days=45)
    try:
        w = hist.loc[o - WIN: o]
        res = fitted.apply(w)
        point = np.asarray(res.forecast(H))
        gf = res.get_forecast(H)
        mean = np.asarray(gf.predicted_mean)
        se = np.asarray(gf.se_mean)
        assert np.allclose(mean, point)
        return point, mean[:, None] + se[:, None] * Z[None, :], False
    except Exception as e:
        log.warning("%s: SARIMA apply/forecast failed, diurnal substituted: %r", o, e)
        return fc.fc_diurnal(hist, o), np.full((H, len(QLEVELS)), np.nan), True


def snaive_week(hist, o):
    idx = [o + pd.Timedelta(hours=h - 168) for h in range(1, H + 1)]
    return hist.reindex(idx).values


def run_baselines(zone, split, hist, train_end, origins, arms):
    """Rows (one per origin x horizon) for the requested baseline arms."""
    fitted = fit_sarima(hist, train_end) if "SARIMA" in arms else None
    gbm = fit_gbm(hist, train_end) if "GBM" in arms else None
    out = {a: [] for a in arms}
    for o in origins:
        actual = fc.actual_window(hist, o)
        if np.isnan(actual).any():
            continue
        tt = [o + pd.Timedelta(hours=h) for h in range(1, H + 1)]
        base = {"zone": zone, "split": split, "origin": o}
        for arm in arms:
            q, fb = None, False
            if arm == "SARIMA":
                if fitted is None:
                    continue
                p, q, fb = sarima_origin(fitted, hist, o)
            elif arm == "GBM":
                if gbm is None:
                    continue
                p = fc.fc_gbm(gbm, hist, o)
            elif arm == "snaive_week":
                p = snaive_week(hist, o)
            for h in range(H):
                r = dict(base, h=h + 1, target_time=tt[h], actual=float(actual[h]),
                         point=float(p[h]), fallback=fb)
                if q is not None:
                    r.update({f"q{lv:.2f}": float(q[h, j]) for j, lv in enumerate(QLEVELS)})
                out[arm].append(r)
    return {a: pd.DataFrame(v) for a, v in out.items()}
