"""Step 7: run the arms on the retro (v1.5 2025 test) and holdout splits per PREREG.

  python run_arms.py baselines <holdout_test_end>   # snaive_week, SARIMA, GBM (serial)
  python run_arms.py tsfm <holdout_test_end>        # Timestral-5M, Timestral-209M, Chronos-2

Baselines and TSFM run in separate processes (torch + LightGBM share no process) and
never at the same time: both take an exclusive lock on $V/run.lock. Checkpoints are
written per origin under $V/run/ckpt and reused on restart; the final PRED-<arm>
parquet is written once and never overwritten.
"""

import fcntl
import glob
import os
import sys
import time

import numpy as np
import pandas as pd

from khepri_tsfm import data
from khepri_tsfm.common import BASELINE_ARMS, CONTEXT, H, PINS, QCOLS, TSFM_ARMS

V = os.environ["V"]
CKPT = os.path.join(V, "run", "ckpt")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "predictions")
DATE = pd.Timestamp.now("UTC").strftime("%Y-%m-%d")


def lock():
    f = open(os.path.join(V, "run.lock"), "w")
    fcntl.flock(f, fcntl.LOCK_EX)
    f.write(f"{os.getpid()} {sys.argv[1]} {pd.Timestamp.now('UTC').isoformat()}\n"); f.flush()
    return f


def splits(holdout_end):
    for zone in data.ZONES:
        g = zone[:2]
        yield zone, "retro", data.RETRO[g]
        yield zone, "holdout", data.holdout_split(g, holdout_end)


def ckpt_path(arm, split, zone, origin):
    return os.path.join(CKPT, arm, split, zone, origin.strftime("%Y%m%dT%H") + ".parquet")


def finalize(arm, revision):
    os.makedirs(OUT, exist_ok=True)
    if glob.glob(os.path.join(OUT, f"PRED-{arm}_KHEPRI-TSFM_v1_*.parquet")):
        raise SystemExit(f"PRED-{arm} exists: never overwritten")
    parts = sorted(glob.glob(os.path.join(CKPT, arm, "*", "*", "*.parquet")))
    df = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)
    df["revision"] = revision
    df = df.sort_values(["split", "zone", "origin", "h"]).reset_index(drop=True)
    fp = os.path.join(OUT, f"PRED-{arm}_KHEPRI-TSFM_v1_{DATE}.parquet")
    df.to_parquet(fp, index=False)
    print(f"wrote {fp} rows={len(df)}", flush=True)


def run_baselines(holdout_end):
    from khepri_tsfm.baselines import fit_gbm, fit_sarima, sarima_origin, snaive_week
    from khepri_v15 import forecast as fc
    for zone, split, (years, train_end, ts, te) in splits(holdout_end):
        hist, gap = data.series(zone, years, te)
        origins = data.origins(hist, ts, te)
        t0 = time.time()
        fitted = fit_sarima(hist, train_end)
        gbm = fit_gbm(hist, train_end)
        print(f"{zone} {split} gap={gap:.5f} origins={len(origins)} fit={time.time()-t0:.1f}s "
              f"sarima={'ok' if fitted is not None else 'FAILED'} gbm={'ok' if gbm else 'FAILED'}",
              flush=True)
        for o in origins:
            actual = fc.actual_window(hist, o)
            if np.isnan(actual).any():
                continue
            tt = [o + pd.Timedelta(hours=h) for h in range(1, H + 1)]
            for arm in BASELINE_ARMS:
                fp = ckpt_path(arm, split, zone, o)
                if os.path.exists(fp):
                    continue
                q, fb = None, False
                if arm == "SARIMA":
                    if fitted is None:
                        continue
                    p, q, fb = sarima_origin(fitted, hist, o)
                elif arm == "GBM":
                    if gbm is None:
                        continue
                    p = fc.fc_gbm(gbm, hist, o)
                else:
                    p = snaive_week(hist, o)
                df = pd.DataFrame({"zone": zone, "split": split, "origin": o, "h": np.arange(1, H + 1),
                                   "target_time": tt, "actual": actual, "point": np.asarray(p, float),
                                   "fallback": fb})
                for j, c in enumerate(QCOLS):
                    df[c] = q[:, j] if q is not None else np.nan
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                df.to_parquet(fp, index=False)
        print(f"{zone} {split} done {time.time()-t0:.1f}s", flush=True)
    for arm in BASELINE_ARMS:
        finalize(arm, "khepri v1.5 (tag v1.5, 9e2214f)" if arm != "snaive_week" else "n/a")


def run_tsfm(holdout_end):
    from khepri_tsfm.models import Arm, offline
    from khepri_v15 import forecast as fc
    offline()
    series = {}
    for zone, split, (years, train_end, ts, te) in splits(holdout_end):
        hist, _ = data.series(zone, years, te)
        series[(zone, split)] = (hist, data.origins(hist, ts, te))
    for arm_name in TSFM_ARMS:
        arm = Arm(arm_name)
        for split in ("retro", "holdout"):
            all_o = sorted(set().union(*[set(series[(z, split)][1]) for z in data.ZONES]))
            t0 = time.time()
            for i, o in enumerate(all_o):
                todo = [z for z in data.ZONES if o in series[(z, split)][1]
                        and not os.path.exists(ckpt_path(arm_name, split, z, o))]
                if not todo:
                    continue
                ctx, acts = [], []
                for z in todo:
                    hist = series[(z, split)][0]
                    c = hist.loc[:o].values[-CONTEXT:]
                    assert len(c) == CONTEXT and hist.index[hist.index.get_loc(o)] == o
                    ctx.append(c)
                    acts.append(fc.actual_window(hist, o))
                q = arm.forecast(np.stack(ctx))
                tt = [o + pd.Timedelta(hours=h) for h in range(1, H + 1)]
                for k, z in enumerate(todo):
                    if np.isnan(acts[k]).any():
                        continue
                    df = pd.DataFrame({"zone": z, "split": split, "origin": o, "h": np.arange(1, H + 1),
                                       "target_time": tt, "actual": acts[k],
                                       "point": q[k, :, QCOLS.index("q0.50")], "fallback": False})
                    for j, c in enumerate(QCOLS):
                        df[c] = q[k, :, j]
                    fp = ckpt_path(arm_name, split, z, o)
                    os.makedirs(os.path.dirname(fp), exist_ok=True)
                    df.to_parquet(fp, index=False)
                if i % 25 == 0:
                    print(f"{arm_name} {split} {i+1}/{len(all_o)} {time.time()-t0:.0f}s", flush=True)
        del arm
        repo, sha = PINS[arm_name]
        finalize(arm_name, f"{repo}@{sha}")


if __name__ == "__main__":
    which, end = sys.argv[1], pd.Timestamp(sys.argv[2], tz="UTC")
    lk = lock()
    print(f"lock taken {pd.Timestamp.now('UTC').isoformat()} {which} holdout_end={end}", flush=True)
    run_baselines(end) if which == "baselines" else run_tsfm(end)
