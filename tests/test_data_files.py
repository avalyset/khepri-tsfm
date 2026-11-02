"""Published data files: sha256 as recorded in truth/STATE, row counts and columns."""

import hashlib
import os

import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHA = {  # truth/STATE_KHEPRI-TSFM_v1_2026-11-02.md (steg 3 og steg 7-8)
    "data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "ab308ae9f49fb9a4229d3ef089bb8b005fd149101a1e9596c9295c3e5cfa95f0",
    "data/CI_KHEPRI-TSFM_v1_2026-11-02.meta.json":
        "97f1cf6d7c640968ec800ebefb578680bdcdf44a8269dea6bdb6f0638a5f7929",
    "predictions/PRED-Chronos-2_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "b643e82093061d324d1b1565a0154c33f9455e10f9ef1ff79b3937dd58d821d3",
    "predictions/PRED-GBM_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "176de684adda5553c049ce63b4e3c597252dc05a362d97d7f2c799964a0f7343",
    "predictions/PRED-SARIMA_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "0723656c5c4ce047612a8240becee9d59565db98bcee6763ec6871bc8a760d0e",
    "predictions/PRED-Timestral-209M_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "0f48d616284e9248b4626b19d6fa8f302169a57de193b228ec2469a2b17deb5d",
    "predictions/PRED-Timestral-5M_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "cfa2d315c7b9ca2c1df9911edd7f6a514c2f04c0be691fa8edda4c870bb89456",
    "predictions/PRED-snaive_week_KHEPRI-TSFM_v1_2026-11-02.parquet":
        "5cbfa2d01689d979fbf05c626c96bc6740b0e3e88bb8c73b4ccbae290909caf1",
}
PRED = [p for p in SHA if p.startswith("predictions/")]
COLS = ["zone", "split", "origin", "h", "target_time", "actual", "point", "fallback"] + \
       [f"q{q:.2f}" for q in (0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                               0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99)] + ["revision"]


def sha256(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


@pytest.mark.parametrize("rel", sorted(SHA))
def test_sha256(rel):
    assert sha256(os.path.join(ROOT, rel)) == SHA[rel]


@pytest.mark.parametrize("rel", sorted(PRED))
def test_pred_rows_and_columns(rel):
    df = pd.read_parquet(os.path.join(ROOT, rel))
    # 9 zones x (361 retro + 14 holdout) origins x 96 hours
    assert len(df) == 324000
    assert list(df.columns) == COLS
    assert set(df.split) == {"retro", "holdout"}
    assert df.groupby(["split"]).origin.nunique().to_dict() == {"holdout": 14, "retro": 361}
