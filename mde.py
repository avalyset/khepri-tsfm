"""Step 4: MDE for the holdout, computed before any TSFM run.

Loss differences SARIMA - GBM per 2025 origin from the stored per-(origin, day) v1.5
metric rows that reproduce the published tables (SARIMA: s2-j2b, GBM: s2-ren
std_ren365). Per-origin loss = mean of the four day-MAPEs = MAPE over the 96 h (no
masked hours: every |actual| > 1e-6). The series is the zone-averaged loss per origin.

Usage: python mde.py <n_holdout_origins> <out.json>
"""

import json
import os
import sys

import numpy as np
import pandas as pd

from khepri_tsfm.common import H
from khepri_tsfm.data import ZONES
from khepri_tsfm.stats import H_DM, lrv, mde

D = os.path.expanduser("~/khepri-data/eds-revisjon/_data")


def per_origin(zone):
    tag = "primaer_2025" if zone.startswith("NO") else "se_2025"
    s = pd.read_csv(f"{D}/s2-j2b/{zone}_{tag}_rows.csv")
    g = pd.read_csv(f"{D}/s2-ren/{zone}_{tag}_std_ren365_rows.csv")
    s["origin"] = pd.to_datetime(s.origin, utc=True)
    g["origin"] = pd.to_datetime(g.origin, utc=True)
    s = s[s.model == "SARIMA"].groupby("origin").mape.agg(["mean", "count"])
    g = g[g.model == "GBM"].groupby("origin").mape.agg(["mean", "count"])
    assert (s["count"] == 4).all() and (g["count"] == 4).all()
    return pd.DataFrame({"SARIMA": s["mean"], "GBM": g["mean"], "zone": zone})


def main(n, out):
    frames = [per_origin(z) for z in ZONES]
    df = pd.concat(frames)
    files = {}
    for z in ZONES:
        tag = "primaer_2025" if z.startswith("NO") else "se_2025"
        files[z] = [f"s2-j2b/{z}_{tag}_rows.csv", f"s2-ren/{z}_{tag}_std_ren365_rows.csv"]
    wide = df.reset_index().pivot(index="origin", columns="zone", values=["SARIMA", "GBM"])
    wide = wide.dropna()
    d = (wide["SARIMA"].mean(axis=1) - wide["GBM"].mean(axis=1)).values
    v, kernel = lrv(d, H_DM)
    res = {
        "method": "MDE = (t_{0.975,n-1} + t_{0.80,n-1}) / HLN(n,h) * sqrt(sigma2_LR / n); "
                  "sigma2_LR = rectangular-kernel long-run variance (lags 0..h-1) of the "
                  "zone-averaged per-origin MAPE difference SARIMA - GBM on the v1.5 2025 test",
        "source_rows": files,
        "n_retro_origins": int(len(d)), "mean_diff_retro_pp": float(d.mean()),
        "sigma2_lr": float(v), "kernel": kernel, "h": H_DM, "horizon_hours": H,
        "alpha": 0.05, "power": 0.8, "n_holdout": int(n),
        "mde_pp": mde(v, int(n)),
        "mde_retro_pp_n361": mde(v, int(len(d))),
    }
    json.dump(res, open(out, "w"), indent=2)
    print(json.dumps({k: res[k] for k in ("n_retro_origins", "mean_diff_retro_pp", "sigma2_lr",
                                          "kernel", "n_holdout", "mde_pp", "mde_retro_pp_n361")}))


if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
