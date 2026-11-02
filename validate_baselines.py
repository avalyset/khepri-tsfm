"""Pre-registration check: the prediction-keeping driver reproduces Khepri v1.5.

Runs SARIMA and GBM on one zone's v1.5 2025 test (published baselines, no TSFM) and
compares per-(origin, day) MAPE with the stored v1.5 rows that reproduce the published
tables (SARIMA: eds-revisjon/_data/s2-j2b, GBM: eds-revisjon/_data/s2-ren std_ren365).

Usage: python validate_baselines.py NO1
"""

import json
import os
import sys

import numpy as np
import pandas as pd

from khepri_v15 import forecast as fc
from khepri_tsfm import data
from khepri_tsfm.baselines import run_baselines

D = os.path.expanduser("~/khepri-data/eds-revisjon/_data")


def day_mape(df):
    rows = []
    for (o), g in df.groupby("origin"):
        g = g.sort_values("h")
        for d in range(4):
            s = g.iloc[d * 24:(d + 1) * 24]
            rows.append({"origin": o, "day": d + 1, "mape": fc.mape(s.actual, s.point)})
    return pd.DataFrame(rows)


def main(zone):
    grp = zone[:2]
    years, train_end, ts, te = data.RETRO[grp]
    hist, gap = data.series(zone, years, te)
    origins = data.origins(hist, ts, te)
    out = run_baselines(zone, "retro", hist, train_end, origins, ("SARIMA", "GBM"))
    tag = "primaer_2025" if grp == "NO" else "se_2025"
    ref_s = pd.read_csv(f"{D}/s2-j2b/{zone}_{tag}_rows.csv")
    ref_s = ref_s[ref_s.model == "SARIMA"]
    ref_g = pd.read_csv(f"{D}/s2-ren/{zone}_{tag}_std_ren365_rows.csv")
    ref_g = ref_g[ref_g.model == "GBM"]
    rep = {"zone": zone, "n_origins": len(origins), "gap_frac": float(gap)}
    for arm, ref in (("SARIMA", ref_s), ("GBM", ref_g)):
        mine = day_mape(out[arm])
        ref = ref.assign(origin=pd.to_datetime(ref.origin, utc=True))[["origin", "day", "mape"]]
        m = mine.merge(ref, on=["origin", "day"], suffixes=("", "_ref"))
        diff = (m.mape - m.mape_ref).abs()
        rep[arm] = {"n_matched": int(len(m)), "n_mine": int(len(mine)), "n_ref": int(len(ref)),
                    "mean_mine": float(mine.mape.mean()), "mean_ref": float(ref.mape.mean()),
                    "max_abs_diff": float(diff.max()), "mean_abs_diff": float(diff.mean())}
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
