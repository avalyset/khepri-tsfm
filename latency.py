"""Step 2: latency and peak RSS per arm on synthetic data (no real CI touched).

TSFM: synthetic random walk of length 8192, 10 timed calls after one warm-up call,
single series and a batch of 9. SARIMA: one fit + one origin apply/forecast with the
Khepri v1.5 code path on NO1 2025 (published baseline, no TSFM). Each measurement runs
in its own subprocess so peak RSS (ru_maxrss) is per arm.
"""

import json
import resource
import subprocess
import sys
import time

import numpy as np

SEED = 20261102


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20  # macOS: bytes


def tsfm(name):
    from khepri_tsfm.models import Arm, CONTEXT, offline
    offline()
    rng = np.random.default_rng(SEED)
    walk = 300 + np.cumsum(rng.normal(0, 1, size=(9, CONTEXT)), axis=1)
    t0 = time.perf_counter(); arm = Arm(name); load_s = time.perf_counter() - t0
    out = {"arm": name, "load_s": load_s}
    for label, x in (("single", walk[:1]), ("batch9", walk)):
        arm.forecast(x)  # warm-up
        ts = []
        for _ in range(10):
            t0 = time.perf_counter(); q = arm.forecast(x); ts.append(time.perf_counter() - t0)
        assert q.shape == (len(x), 96, 21) and np.isfinite(q).all()
        out[label] = {"median_s": float(np.median(ts)), "max_s": float(np.max(ts))}
    out["peak_rss_mb"] = rss_mb()
    return out


def sarima():
    import pandas as pd
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from khepri import forecast as fc
    from khepri_tsfm.data import set_raw_dir
    set_raw_dir()
    T = lambda s: pd.Timestamp(s, tz="UTC")
    train_end = T("2023-12-31 23:00")
    hist, _ = fc.hourly_ci("NO1", fc.history_years([2021, 2022, 2023, 2024], T("2025-12-31")))
    t0 = time.perf_counter()
    fitted = SARIMAX(hist.loc[:train_end], order=(2, 0, 1), seasonal_order=(1, 1, 0, 24),
                     enforce_stationarity=False, enforce_invertibility=False
                     ).fit(disp=False, maxiter=50)
    fit_s = time.perf_counter() - t0
    o = T("2025-03-01")
    ts = []
    for _ in range(5):
        t0 = time.perf_counter()
        w = hist.loc[o - pd.Timedelta(days=45): o]
        fitted.apply(w).get_forecast(96).summary_frame(alpha=0.1)
        ts.append(time.perf_counter() - t0)
    return {"arm": "SARIMA", "fit_s": fit_s, "n_train_hours": int(len(hist.loc[:train_end])),
            "origin_apply_forecast_median_s": float(np.median(ts)),
            "origin_apply_forecast_max_s": float(np.max(ts)), "peak_rss_mb": rss_mb()}


if __name__ == "__main__":
    if len(sys.argv) == 2:
        arm = sys.argv[1]
        print(json.dumps(sarima() if arm == "SARIMA" else tsfm(arm)))
        sys.exit(0)
    results = []
    for arm in ("Timestral-5M", "Timestral-209M", "Chronos-2", "SARIMA"):
        r = subprocess.run([sys.executable, __file__, arm], capture_output=True, text=True)
        if r.returncode != 0:
            results.append({"arm": arm, "error": r.stderr.strip().splitlines()[-1]})
        else:
            results.append(json.loads(r.stdout.strip().splitlines()[-1]))
        print(json.dumps(results[-1]), flush=True)
