"""One prospective issue for one group of arms (called by issue.py in its own process).

  python prosp_arms.py baselines|tsfm <raw_dir> <origin-utc> <out.parquet>

Same arms, rules and context as the holdout (run_arms.py): SARIMA/GBM with the v1.5
procedure under the holdout training rule, seasonal-naive (week), and the pinned TSFMs
on the last 8192 hourly values ending at the origin. Actuals are left empty.
"""

import sys

import numpy as np
import pandas as pd

from khepri_v15 import forecast as fc
from khepri_tsfm import data
from khepri_tsfm.common import BASELINE_ARMS, CONTEXT, H, PINS, QCOLS, TSFM_ARMS


def main(group, raw, origin, out):
    fc.RAW_DIR = raw
    o = pd.Timestamp(origin)
    tt = [o + pd.Timedelta(hours=h) for h in range(1, H + 1)]
    hists = {}
    for zone in data.ZONES:
        years, train_end, _, _ = data.holdout_split(zone[:2], o)
        hist, gap = fc.hourly_ci(zone, fc.history_years(years, o))
        hists[zone] = (hist.loc[:o], train_end)
        assert hist.index.max() >= o, f"{zone}: data end {hist.index.max()} before origin"
    rows = []

    def emit(arm, zone, p, q=None, fb=False, rev=""):
        df = pd.DataFrame({"arm": arm, "zone": zone, "split": "prosp", "origin": o,
                           "h": np.arange(1, H + 1), "target_time": tt, "actual": np.nan,
                           "point": np.asarray(p, float), "fallback": fb, "revision": rev})
        for j, c in enumerate(QCOLS):
            df[c] = q[:, j] if q is not None else np.nan
        rows.append(df)

    if group == "baselines":
        from khepri_tsfm.baselines import fit_gbm, fit_sarima, sarima_origin, snaive_week
        for zone, (hist, train_end) in hists.items():
            emit("snaive_week", zone, snaive_week(hist, o), rev="n/a")
            fitted = fit_sarima(hist, train_end)
            if fitted is not None:
                p, q, fb = sarima_origin(fitted, hist, o)
                emit("SARIMA", zone, p, q, fb, "khepri v1.5 (tag v1.5, 9e2214f)")
            gbm = fit_gbm(hist, train_end)
            if gbm is not None:
                emit("GBM", zone, fc.fc_gbm(gbm, hist, o), rev="khepri v1.5 (tag v1.5, 9e2214f)")
    else:
        from khepri_tsfm.models import Arm, offline
        offline()
        ctx = np.stack([h.values[-CONTEXT:] for h, _ in hists.values()])
        assert ctx.shape == (len(data.ZONES), CONTEXT)
        for name in TSFM_ARMS:
            q = Arm(name).forecast(ctx)
            for k, zone in enumerate(hists):
                emit(name, zone, q[k, :, QCOLS.index("q0.50")], q[k], rev="@".join(PINS[name]))
    pd.concat(rows, ignore_index=True).to_parquet(out, index=False)


if __name__ == "__main__":
    main(*sys.argv[1:5])
