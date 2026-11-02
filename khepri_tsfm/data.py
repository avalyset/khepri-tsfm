"""CI series via Khepri v1.5 (no own factor logic) and the study's splits.

Raw A75 CSVs are read in place: years <= 2025 from the existing Khepri raw trees,
2026 from the fresh fetch on the Vault volume. A directory of symlinks on the Vault
volume presents them to khepri.forecast.hourly_ci under the v1 filename convention.
"""

import os

import pandas as pd

from khepri import forecast as fc

V = os.environ.get("V", "/Volumes/Vault/khepri-tsfm")
HOME = os.path.expanduser("~")
SRC = {
    "NO": os.path.join(HOME, "khepri-data", "raw", "entsoe-rest"),
    "SE": os.path.join(HOME, "khepri-data", "se", "raw", "entsoe-rest"),
}
SRC_2026 = os.path.join(V, "data", "raw", "entsoe-rest-2026")
MERGED = os.path.join(V, "data", "raw", "merged")
ZONES = ("NO1", "NO2", "NO3", "NO4", "NO5", "SE1", "SE2", "SE3", "SE4")

T = lambda s: pd.Timestamp(s, tz="UTC")

# Retro = the v1.5 2025 test, exactly as the published driver splits
# (train_years, train_end, test_start, test_end).
RETRO = {
    "NO": ([2021, 2022, 2023, 2024], T("2023-12-31 23:00"), T("2025-01-01"), T("2025-12-31")),
    "SE": ([2022, 2023, 2024], T("2023-12-31 23:00"), T("2025-01-01"), T("2025-12-31")),
}
HOLDOUT_START = T("2026-10-16")


def holdout_split(group, test_end):
    """v1.5 rule applied with test start 2026-10-16 (DECISIONS [steg 1]): train_end lies
    one year + 1 h before test start, and the training calendar years are the v1.5 ones
    shifted with train_end's year (2023 -> 2025). Parameters only; forecast.py unchanged."""
    train_end = HOLDOUT_START - pd.DateOffset(years=1) - pd.Timedelta(hours=1)
    shift = train_end.year - RETRO[group][1].year
    years = [y + shift for y in RETRO[group][0] if y + shift <= train_end.year]
    return years, train_end, HOLDOUT_START, test_end


def set_raw_dir():
    os.makedirs(MERGED, exist_ok=True)
    for zone in ZONES:
        for y in range(2019, 2027):
            name = f"{zone}_generation_{y}.csv"
            src = os.path.join(SRC_2026 if y == 2026 else SRC[zone[:2]], name)
            dst = os.path.join(MERGED, name)
            if os.path.exists(src) and not os.path.lexists(dst):
                os.symlink(src, dst)
    fc.RAW_DIR = MERGED
    return MERGED


def series(zone, train_years, test_end):
    """The hourly CI series exactly as khepri.forecast.eval_split builds it."""
    set_raw_dir()
    return fc.hourly_ci(zone, fc.history_years(train_years, test_end))


def origins(hist, test_start, test_end):
    """v1.5 origin rule (forecast.py:183-184)."""
    return [o for o in pd.date_range(test_start, test_end, freq="1D", tz="UTC")
            if o in hist.index and (o + pd.Timedelta(hours=fc.H)) <= hist.index.max()]
