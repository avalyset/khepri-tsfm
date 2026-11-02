"""Step 3: build the hourly CI series with Khepri v1.5 (no own factor logic) for every
zone and split, exactly as the arms see them, and write the CI parquet.

Usage: python build_ci.py <holdout_test_end> <out.parquet> <meta.json>
"""

import json
import sys

import pandas as pd

from khepri_tsfm import data


def main(end, out, meta_fp):
    end = pd.Timestamp(end, tz="UTC")
    frames, meta = [], {}
    for zone in data.ZONES:
        for split, spec in (("retro", data.RETRO[zone[:2]]),
                            ("holdout", data.holdout_split(zone[:2], end))):
            years, train_end, ts, te = spec
            hist, gap = data.series(zone, years, te)
            org = data.origins(hist, ts, te)
            frames.append(pd.DataFrame({"zone": zone, "split": split, "time": hist.index,
                                        "ci_g_per_kwh": hist.values}))
            meta[f"{zone}/{split}"] = {
                "train_years": years, "train_end": str(train_end), "test_start": str(ts),
                "test_end": str(te), "series_start": str(hist.index.min()),
                "series_end": str(hist.index.max()), "n_hours": int(len(hist)),
                "gap_frac": float(gap), "n_origins": len(org),
                "first_origin": str(org[0]) if org else None,
                "last_origin": str(org[-1]) if org else None}
    pd.concat(frames, ignore_index=True).to_parquet(out, index=False)
    json.dump(meta, open(meta_fp, "w"), indent=1)
    for k, v in meta.items():
        print(k, v["series_end"], v["gap_frac"], v["n_origins"], v["first_origin"], v["last_origin"])


if __name__ == "__main__":
    main(*sys.argv[1:4])
