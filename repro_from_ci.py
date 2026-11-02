"""Independent reproduction from the published CI series only (no ENTSO-E raw data needed).

Recomputes the arms from data/CI_KHEPRI-TSFM_v1_<date>.parquet for every holdout origin and
for every k-th retro origin, and compares with the PRED files. Baselines and TSFM run in
separate processes (torch and LightGBM must not share one).

  python repro_from_ci.py baselines <k> <out.json>
  python repro_from_ci.py tsfm <k> <out.json>
  python repro_from_ci.py verify            # sha256 of CI and PRED files against the .sha256 lists
  python repro_from_ci.py analysis <dir>    # rerun the locked analysis into <dir> and diff with results/
"""

import glob
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CI = glob.glob(os.path.join(HERE, "data", "CI_KHEPRI-TSFM_v1_*.parquet"))[0]
PRED = os.path.join(HERE, "predictions")


def sha(fp):
    h = hashlib.sha256()
    with open(fp, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def verify():
    bad = 0
    for lst in glob.glob(os.path.join(HERE, "data", "*.sha256")) + glob.glob(os.path.join(PRED, "*.sha256")):
        for line in open(lst):
            digest, name = line.split()
            fp = os.path.join(os.path.dirname(lst), name)
            ok = os.path.exists(fp) and sha(fp) == digest
            bad += not ok
            print(("OK  " if ok else "FEIL"), name)
    sys.exit(1 if bad else 0)


def series():
    ci = pd.read_parquet(CI)
    ci["time"] = pd.to_datetime(ci.time, utc=True)
    out = {}
    for (z, s), g in ci.groupby(["zone", "split"]):
        out[(z, s)] = g.set_index("time").ci_g_per_kwh.sort_index().asfreq("1h")
    return out


def sample(pred, k):
    o = pred[["split", "zone", "origin"]].drop_duplicates()
    keep = []
    for (s, z), g in o.groupby(["split", "zone"]):
        g = g.sort_values("origin")
        keep.append(g if s == "holdout" else g.iloc[::k])
    return pd.concat(keep)


def compare(name, mine, ref):
    m = mine.merge(ref, on=["split", "zone", "origin", "h"], suffixes=("", "_ref"))
    cols = ["point"] + [c for c in mine.columns if c.startswith("q") and c in ref.columns]
    res = {"arm": name, "n_rows": int(len(m)), "n_expected": int(len(mine))}
    for c in cols:
        a, b = m[c].values, m[c + "_ref"].values
        both = ~(np.isnan(a) & np.isnan(b))
        res[f"maxabs_{c}"] = float(np.nanmax(np.abs(a[both] - b[both]))) if both.any() else 0.0
    res["max_abs_point"] = res["maxabs_point"]
    return res


def baselines(k, out):
    from khepri_v15 import forecast as fc
    from khepri_tsfm import data
    from khepri_tsfm.baselines import fit_gbm, fit_sarima, sarima_origin, snaive_week
    from khepri_tsfm.common import QCOLS
    S = series()
    results = []
    for arm in ("snaive_week", "GBM", "SARIMA"):
        ref = pd.read_parquet(glob.glob(os.path.join(PRED, f"PRED-{arm}_KHEPRI-TSFM_v1_*.parquet"))[0])
        ref["origin"] = pd.to_datetime(ref.origin, utc=True)
        todo = sample(ref, k)
        rows = []
        for (s, z), g in todo.groupby(["split", "zone"]):
            hist = S[(z, s)]
            spec = data.RETRO[z[:2]] if s == "retro" else data.holdout_split(z[:2], hist.index.max())
            train_end = spec[1]
            model = fit_sarima(hist, train_end) if arm == "SARIMA" else fit_gbm(hist, train_end) if arm == "GBM" else None
            for o in g.origin:
                actual = fc.actual_window(hist, o)
                q = None
                if arm == "SARIMA":
                    p, q, _ = sarima_origin(model, hist, o)
                elif arm == "GBM":
                    p = fc.fc_gbm(model, hist, o)
                else:
                    p = snaive_week(hist, o)
                d = pd.DataFrame({"split": s, "zone": z, "origin": o, "h": np.arange(1, 97), "point": p})
                if q is not None:
                    for j, c in enumerate(QCOLS):
                        d[c] = q[:, j]
                rows.append(d)
        r = compare(arm, pd.concat(rows), ref)
        results.append(r)
        print(json.dumps(r), flush=True)
    json.dump(results, open(out, "w"), indent=1)


def tsfm(k, out):
    from khepri_tsfm.common import CONTEXT, QCOLS, TSFM_ARMS
    from khepri_tsfm.models import Arm
    S = series()
    results = []
    for name in TSFM_ARMS:
        ref = pd.read_parquet(glob.glob(os.path.join(PRED, f"PRED-{name}_KHEPRI-TSFM_v1_*.parquet"))[0])
        ref["origin"] = pd.to_datetime(ref.origin, utc=True)
        todo = sample(ref, k)
        arm = Arm(name)
        rows = []
        for (s, o), g in todo.groupby(["split", "origin"]):
            zones = list(g.zone)
            ctx = np.stack([S[(z, s)].loc[:o].values[-CONTEXT:] for z in zones])
            q = arm.forecast(ctx)
            for i, z in enumerate(zones):
                d = pd.DataFrame({"split": s, "zone": z, "origin": o, "h": np.arange(1, 97),
                                  "point": q[i, :, QCOLS.index("q0.50")]})
                for j, c in enumerate(QCOLS):
                    d[c] = q[i, :, j]
                rows.append(d)
        r = compare(name, pd.concat(rows), ref)
        results.append(r)
        print(json.dumps(r), flush=True)
    json.dump(results, open(out, "w"), indent=1)


def analysis(outdir):
    os.makedirs(outdir, exist_ok=True)
    mde = glob.glob(os.path.join(HERE, "results", "MDE_KHEPRI-TSFM_v1_*.json"))[0]
    prefix = os.path.join(outdir, "RESULTATER_KHEPRI-TSFM_v1_2026-11-02")
    subprocess.run([sys.executable, os.path.join(HERE, "analysis.py"), PRED, mde, prefix], check=True,
                   stdout=subprocess.DEVNULL)
    a = json.load(open(prefix + ".json"))
    b = json.load(open(glob.glob(os.path.join(HERE, "results", "RESULTATER_KHEPRI-TSFM_v1_*.json"))[0]))
    a.pop("mde", None); b.pop("mde", None)
    same = json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    print("analysis.py-utdata identisk med results/ (JSON):", same)
    sys.exit(0 if same else 1)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "verify":
        verify()
    elif cmd == "analysis":
        analysis(sys.argv[2])
    elif cmd == "baselines":
        baselines(int(sys.argv[2]), sys.argv[3])
    else:
        tsfm(int(sys.argv[2]), sys.argv[3])
