"""Reproduction table (DEVIATIONS D-08): retro mean MAPE (mean over days 1-4) of our SARIMA
and GBM arms per zone against the published Khepri v1.5 tables. Descriptive only.

Published values: khepri-v1.5 docs/forecast-results.md:50-54 (NO) and
docs/se-forecast-results.md:45-48 (SE), columns SARIMA and GBM (corrected).

Usage: python repro_v15.py <pred_dir> <out.md>
"""

import glob
import os
import sys

import pandas as pd

from khepri_v15 import forecast as fc

PUBLISHED = {  # zone: (SARIMA, GBM corrected)
    "NO1": (2.47, 2.31), "NO2": (3.96, 3.42), "NO3": (6.87, 6.58), "NO4": (7.24, 10.16),
    "NO5": (0.72, 1.26), "SE1": (11.64, 10.76), "SE2": (10.42, 9.57), "SE3": (4.54, 4.53),
    "SE4": (20.19, 17.54),
}


def day_mean(df):
    vals = []
    for _, g in df.groupby(["zone", "origin"]):
        g = g.sort_values("h")
        vals += [fc.mape(g.actual.values[d * 24:(d + 1) * 24], g.point.values[d * 24:(d + 1) * 24])
                 for d in range(4)]
    return sum(vals) / len(vals)


def main(pred_dir, out):
    md = [f"Arkivnøkkel: {os.path.splitext(os.path.basename(out))[0]}", "",
          "Reproduksjon av publiserte Khepri v1.5-tall (retro 2025, snitt MAPE dag 1–4, %). "
          "Beskrivende (DEVIATIONS D-02, D-08).", "",
          "| sone | SARIMA publisert | SARIMA her | Δ | GBM publisert | GBM her | Δ |",
          "|---|---|---|---|---|---|---|"]
    preds = {}
    for arm in ("SARIMA", "GBM"):
        fp, = glob.glob(os.path.join(pred_dir, f"PRED-{arm}_KHEPRI-TSFM_v1_*.parquet"))
        df = pd.read_parquet(fp)
        preds[arm] = df[df.split == "retro"]
    for zone, (ps, pg) in PUBLISHED.items():
        s = day_mean(preds["SARIMA"][preds["SARIMA"].zone == zone])
        g = day_mean(preds["GBM"][preds["GBM"].zone == zone])
        md.append(f"| {zone} | {ps:.2f} | {s:.4f} | {s - ps:+.4f} | {pg:.2f} | {g:.4f} | {g - pg:+.4f} |")
    open(out, "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:3])
