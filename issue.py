"""Step 6: daily prospective issue (launchd no.ecodeco.khepri-tsfm.v1).

Origin = today 00:00 UTC. Fetches an A75 delta (first day of the previous month -> now),
splices it onto the step-3 extraction, builds the CI with Khepri v1.5, and issues all
arms (snaive_week, SARIMA, GBM with the holdout training rule; Timestral-5M/-209M,
Chronos-2) for the next 96 h. Writes PROSP_KHEPRI-TSFM_v1_<issue date>.parquet (actuals
empty; they are joined later from a fresh pull with the same CI code and analysed with
the locked analysis.py), its sha256 and an OpenTimestamps stamp, and upgrades
yesterday's stamp. Waits for $V/run.lock at most 6 h; otherwise the origin is logged as
lost and never back-filled.
"""

import fcntl
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

import numpy as np
import pandas as pd

V = os.environ["V"]
REPO = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
UTTAK = os.path.join(V, "data", "raw", "entsoe-rest-2026")
PROSP = os.path.join(V, "prosp")
LOGF = os.path.join(PROSP, "issue_log.jsonl")


def log(rec):
    os.makedirs(PROSP, exist_ok=True)
    rec["utc"] = pd.Timestamp.now("UTC").isoformat()
    with open(LOGF, "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)


def vault_ok():
    m = subprocess.run(["/sbin/mount"], capture_output=True, text=True).stdout
    return " on /Volumes/Vault " in m and os.access("/Volumes/Vault", os.W_OK)


def take_lock(max_wait_s=6 * 3600):
    f = open(os.path.join(V, "run.lock"), "a")
    t0 = time.time()
    while True:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return f
        except BlockingIOError:
            if time.time() - t0 > max_wait_s:
                return None
            time.sleep(60)


def sha256(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def build_raw(day):
    """Delta fetch, then the merged raw dir for this issue (uttak + delta, latest wins)."""
    ddir = os.path.join(PROSP, day, "delta")
    start = (pd.Timestamp(day, tz="UTC") - pd.offsets.MonthBegin(2)).strftime("%Y-%m-%d")
    end = pd.Timestamp.now("UTC").floor("h").strftime("%Y-%m-%dT%H:00Z")
    r = subprocess.run([PY, os.path.join(REPO, "fetch_a75.py"), end, "--start", start,
                        "--out", ddir], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("fetch failed: " + r.stderr.strip().splitlines()[-1][:200])
    mdir = os.path.join(PROSP, "current_raw")
    shutil.rmtree(mdir, ignore_errors=True)
    os.makedirs(mdir)
    from khepri_tsfm.data import SRC, ZONES
    for zone in ZONES:
        frames = [pd.read_csv(p, index_col=0) for p in
                  (os.path.join(UTTAK, f"{zone}_generation_2026.csv"),
                   os.path.join(ddir, f"{zone}_generation_2026.csv")) if os.path.exists(p)]
        frames += [pd.read_csv(p, index_col=0) for p in
                   sorted(glob.glob(os.path.join(ddir, f"{zone}_generation_20[3-9]*.csv")))]
        df = pd.concat(frames)
        idx = pd.to_datetime(df.index, utc=True)
        df = df[~idx.duplicated(keep="last")]
        idx = pd.to_datetime(df.index, utc=True)
        order = np.argsort(idx.values, kind="stable")
        df, idx = df.iloc[order], idx[order]
        for y in sorted(set(idx.year)):
            if y >= 2026:
                df[idx.year == y].to_csv(os.path.join(mdir, f"{zone}_generation_{y}.csv"))
        for y in range(2019, 2026):
            src = os.path.join(SRC[zone[:2]], f"{zone}_generation_{y}.csv")
            if os.path.exists(src):
                os.symlink(src, os.path.join(mdir, f"{zone}_generation_{y}.csv"))
    return mdir


def main():
    if not vault_ok():
        print("VAULT_FAIL", file=sys.stderr); sys.exit(1)
    day = pd.Timestamp.now("UTC").strftime("%Y-%m-%d")
    origin = pd.Timestamp(day, tz="UTC")
    out = os.path.join(PROSP, f"PROSP_KHEPRI-TSFM_v1_{day}.parquet")
    if os.path.exists(out):
        log({"day": day, "status": "already issued"}); return
    lk = take_lock()
    if lk is None:
        log({"day": day, "origin": str(origin), "status": "TAPT: run.lock ikke ledig innen 6 t"})
        return
    try:
        raw = build_raw(day)
        parts = []
        for group in ("baselines", "tsfm"):
            fp = os.path.join(PROSP, day, f"{group}.parquet")
            r = subprocess.run([PY, os.path.join(REPO, "prosp_arms.py"), group, raw, str(origin), fp],
                               capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"{group}: " + (r.stderr.strip().splitlines() or ["?"])[-1][:200])
            parts.append(pd.read_parquet(fp))
        df = pd.concat(parts, ignore_index=True)
        df["issued_utc"] = pd.Timestamp.now("UTC").isoformat()
        df.to_parquet(out, index=False)
        digest = sha256(out)
        with open(out + ".sha256", "w") as f:
            f.write(f"{digest}  {os.path.basename(out)}\n")
        ots = os.path.join(os.path.dirname(PY), "ots")
        st = subprocess.run([ots, "stamp", out], capture_output=True, text=True).returncode
        yday = (origin - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        prev = os.path.join(PROSP, f"PROSP_KHEPRI-TSFM_v1_{yday}.parquet.ots")
        up = subprocess.run([ots, "upgrade", prev], capture_output=True, text=True).returncode \
            if os.path.exists(prev) else None
        log({"day": day, "origin": str(origin), "status": "OK", "rows": int(len(df)),
             "arms": sorted(df.arm.unique().tolist()), "sha256": digest, "ots_stamp_rc": st,
             "ots_upgrade_yesterday_rc": up})
    except Exception as ex:
        log({"day": day, "origin": str(origin), "status": "TAPT", "exc": type(ex).__name__,
             "msg": str(ex)[:200]})
    finally:
        lk.close()


if __name__ == "__main__":
    main()
