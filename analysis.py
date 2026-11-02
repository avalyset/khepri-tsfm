"""Locked analysis for Khepri-TSFM v1 (PREREG). Reads PRED-<arm> parquet files and the MDE
file, writes the RESULTATER markdown and a JSON with every number.

Loss per (arm, split, zone, origin) = Khepri v1.5 MAPE (forecast.py:132-135) over the 96
hourly targets of the origin, on the point forecast (TSFM: the 0.5 quantile). Origins
are never back-filled: every comparison uses the origins where all compared arms have
all nine zones. Splits: 'retro' (v1.5 2025 test), 'holdout' (from 2026-10-16) and,
for the later prospective log, 'prosp'.

Usage: python analysis.py <pred_dir> <mde.json> <out_prefix>
"""

import glob
import json
import os
import sys

import numpy as np
import pandas as pd

from khepri import forecast as fc
from khepri_tsfm.common import BASELINE_ARMS, QCOLS, QLEVELS, TSFM_ARMS
from khepri_tsfm.data import ZONES
from khepri_tsfm.stats import H_DM, dm_hln, hac_se_mean, holm

BASES = ("SARIMA", "GBM")
MAJORITY = 5  # of 9 zones (H1)
# Sensitivity S1 (DEVIATIONS D-07): the six zones with no filled (pumped-storage NaN) hours
# in either test window, fixed from the CI before any TSFM run.
S1_ZONES = ("NO1", "NO4", "SE1", "SE2", "SE3", "SE4")


def load(pred_dir):
    frames = []
    for arm in BASELINE_ARMS + TSFM_ARMS:
        hits = glob.glob(os.path.join(pred_dir, f"PRED-{arm}_KHEPRI-TSFM_v1_*.parquet"))
        if len(hits) != 1:
            raise SystemExit(f"PRED-{arm}: expected exactly one file, found {len(hits)}")
        df = pd.read_parquet(hits[0])
        df["arm"] = arm
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def losses(pred):
    """MAPE over the 96 h per (arm, split, zone, origin); only complete 96-h windows."""
    def one(g):
        if len(g) != 96 or g.point.isna().any():
            return np.nan
        return fc.mape(g.actual.values, g.point.values)
    L = pred.groupby(["arm", "split", "zone", "origin"]).apply(one, include_groups=False)
    return L.rename("loss").reset_index().dropna()


def crps_q(g):
    """Quantile-score approximation of CRPS: (2/K) * sum_k pinball_tau_k, averaged over hours."""
    y = g.actual.values[:, None]
    q = g[list(QCOLS)].values
    tau = np.asarray(QLEVELS)[None, :]
    pin = np.maximum(tau * (y - q), (tau - 1) * (y - q))
    return float((2 * pin.mean(axis=1)).mean())


def zone_avg(L, arms, split, zones=ZONES):
    """Zone-averaged loss per origin, restricted to origins where every arm has all zones."""
    sub = L[(L.split == split) & L.arm.isin(arms) & L.zone.isin(zones)]
    w = sub.pivot_table(index="origin", columns=["arm", "zone"], values="loss").dropna()
    out = {a: w[a].mean(axis=1) for a in arms
           if a in w.columns.get_level_values(0) and w[a].shape[1] == len(zones)}
    return pd.DataFrame(out), w


def compare(L, split, mde_pp=None, zones=ZONES):
    out = []
    for t in TSFM_ARMS:
        for b in BASES:
            za, _ = zone_avg(L, (t, b), split, zones)
            if t not in za or b not in za or len(za) < 2 * H_DM:
                out.append({"tsfm": t, "base": b, "n": int(len(za)), "status": "for få origins"})
                continue
            r = dm_hln((za[t] - za[b]).values)
            r.update({"tsfm": t, "base": b, "mean_loss_tsfm": float(za[t].mean()),
                      "mean_loss_base": float(za[b].mean())})
            if mde_pp is not None:
                r["mde_pp"] = mde_pp
                r["verdict"] = verdict(r, mde_pp)
            out.append(r)
    ok = [r for r in out if "p" in r]
    for r, a in zip(ok, holm([r["p"] for r in ok])):
        r["p_holm"] = float(a)
    return out


def verdict(r, mde_pp):
    if abs(r["mean_diff"]) < mde_pp:
        return "ikke avgjort (innenfor ±MDE)"
    if r["p"] >= 0.05:
        return "ikke signifikant (utenfor ±MDE)"
    return "TSFM bedre" if r["mean_diff"] < 0 else "TSFM dårligere"


def per_zone(L, split):
    t = L[L.split == split].groupby(["zone", "arm"]).loss.agg(["mean", "count"]).reset_index()
    return t


def h1_h2(L):
    pz = L[L.split == "retro"].pivot_table(index="zone", columns="arm", values="loss",
                                           aggfunc="mean")
    res = {}
    for t in TSFM_ARMS:
        if t not in pz or "SARIMA" not in pz:
            continue
        adv_pp = pz["SARIMA"] - pz[t]
        adv_rel = adv_pp / pz["SARIMA"] * 100
        wins = int((adv_pp > 0).sum())
        res[t] = {"zones_tsfm_beats_sarima": wins, "H1_supported": wins >= MAJORITY,
                  "adv_pp": adv_pp.round(6).to_dict(), "adv_rel_pct": adv_rel.round(6).to_dict(),
                  "min_adv_zone_pp": str(adv_pp.idxmin()),
                  "H2_supported_pp": str(adv_pp.idxmin()) == "NO5",
                  "min_adv_zone_rel": str(adv_rel.idxmin()),
                  "H2_supported_rel": str(adv_rel.idxmin()) == "NO5"}
    return res


def contamination(L):
    res = []
    for t in TSFM_ARMS:
        for b in BASES:
            parts = {}
            for split in ("retro", "holdout"):
                za, _ = zone_avg(L, (t, b), split)
                if t in za and b in za and len(za) >= 2 * H_DM:
                    adv = (za[b] - za[t]).values
                    parts[split] = (adv.mean(), hac_se_mean(adv), len(adv))
            if len(parts) < 2:
                continue
            ind = parts["retro"][0] - parts["holdout"][0]
            se = float(np.hypot(parts["retro"][1], parts["holdout"][1]))
            z = ind / se if se > 0 else np.nan
            res.append({"tsfm": t, "base": b, "adv_retro_pp": float(parts["retro"][0]),
                        "adv_holdout_pp": float(parts["holdout"][0]),
                        "indicator_pp": float(ind), "hac_se": se, "z": float(z),
                        "n_retro": parts["retro"][2], "n_holdout": parts["holdout"][2],
                        "possible_contamination": bool(z > 1.96)})
    return res


def calibration(pred, split="holdout"):
    """RQ4: CRPS (quantile score) and 80/90 % central-interval coverage, TSFM vs SARIMA."""
    sub = pred[(pred.split == split) & pred.arm.isin(("SARIMA",) + TSFM_ARMS)]
    sub = sub.dropna(subset=list(QCOLS))
    rows = []
    for (arm, zone, origin), g in sub.groupby(["arm", "zone", "origin"]):
        if len(g) != 96:
            continue
        cov80 = float(((g.actual >= g["q0.10"]) & (g.actual <= g["q0.90"])).mean())
        cov90 = float(((g.actual >= g["q0.05"]) & (g.actual <= g["q0.95"])).mean())
        rows.append({"arm": arm, "zone": zone, "origin": origin, "crps": crps_q(g),
                     "cov80": cov80, "cov90": cov90})
    C = pd.DataFrame(rows)
    if C.empty:
        return {}, []
    summ = C.groupby("arm")[["crps", "cov80", "cov90"]].mean().to_dict(orient="index")
    tests = []
    for t in TSFM_ARMS:
        w = C[C.arm.isin((t, "SARIMA"))].pivot_table(index="origin", columns=["arm", "zone"],
                                                     values="crps").dropna()
        if t not in w or "SARIMA" not in w or len(w) < 2 * H_DM:
            continue
        d = w[t].mean(axis=1) - w["SARIMA"].mean(axis=1)
        r = dm_hln(d.values)
        r.update({"tsfm": t, "base": "SARIMA", "metric": "CRPS"})
        tests.append(r)
    return summ, tests


def fmt(x, nd=3):
    return "–" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{nd}f}"


def main(pred_dir, mde_file, out_prefix):
    pred = load(pred_dir)
    pred["origin"] = pd.to_datetime(pred.origin, utc=True)
    mde = json.load(open(mde_file))
    L = losses(pred)
    splits = [s for s in ("retro", "holdout", "prosp") if s in set(L.split)]
    res = {"mde": mde, "n_origins": {}, "per_zone": {}, "dm": {}}
    for s in splits:
        res["n_origins"][s] = {a: int(L[(L.split == s) & (L.arm == a)].origin.nunique())
                               for a in sorted(set(L.arm))}
        res["per_zone"][s] = per_zone(L, s).to_dict(orient="records")
        res["dm"][s] = compare(L, s, mde["mde_pp"] if s == "holdout" else None)
    res["dm_s1"] = {s: compare(L, s, None, S1_ZONES) for s in splits}
    res["h1_h2"] = h1_h2(L)
    res["contamination"] = contamination(L)
    res["calibration_summary"], res["calibration_dm"] = calibration(pred)
    json.dump(res, open(out_prefix + ".json", "w"), indent=2, default=str)

    md = [f"Arkivnøkkel: {os.path.basename(out_prefix)}", "",
          "Generert av analysis.py (låst i PREREG). Tap = Khepri v1.5 MAPE over 96 t per origin og sone; "
          "testserie = sone-gjennomsnittlig tap per origin; DM med HLN-korreksjon, h = 4, t(n-1). "
          "Negativ differanse = TSFM har lavere tap.", "",
          f"MDE (holdout, n = {mde['n_holdout']}): {fmt(mde['mde_pp'])} pp. "
          "En holdout-forskjell innenfor ±MDE rapporteres som «ikke avgjort», aldri som likhet.", ""]
    for s in splits:
        md += [f"## DM-tester, {s}", "",
               "| TSFM | mot | n | snitt-tap TSFM | snitt-tap base | diff pp | HLN-stat | p | p (Holm) | vurdering |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for r in res["dm"][s]:
            md.append(f"| {r['tsfm']} | {r['base']} | {r['n']} | {fmt(r.get('mean_loss_tsfm'))} | "
                      f"{fmt(r.get('mean_loss_base'))} | {fmt(r.get('mean_diff'))} | {fmt(r.get('dm_hln'), 2)} | "
                      f"{fmt(r.get('p'), 4)} | {fmt(r.get('p_holm'), 4)} | {r.get('verdict', r.get('status', ''))} |")
        md += ["", f"### Per sone, {s} (beskrivende, snitt MAPE %)", ""]
        pz = pd.DataFrame(res["per_zone"][s]).pivot(index="zone", columns="arm", values="mean")
        cols = [a for a in BASELINE_ARMS + TSFM_ARMS if a in pz]
        md += ["| sone | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
        for z in pz.index:
            md.append(f"| {z} | " + " | ".join(fmt(pz.loc[z, a]) for a in cols) + " |")
        md.append("")
    md += ["## Sensitivitet S1: seks soner uten utfylte timer (" + ", ".join(S1_ZONES) + ")", "",
           "Beskrivende; MDE-regelen gjelder bare primæranalysen.", "",
           "| splitt | TSFM | mot | n | diff pp | HLN-stat | p |", "|---|---|---|---|---|---|---|"]
    for s in splits:
        for r in res["dm_s1"][s]:
            md.append(f"| {s} | {r['tsfm']} | {r['base']} | {r['n']} | {fmt(r.get('mean_diff'))} | "
                      f"{fmt(r.get('dm_hln'), 2)} | {fmt(r.get('p'), 4)} |")
    md += ["", "## H1 og H2 (retro)", ""]
    for t, r in res["h1_h2"].items():
        md.append(f"- {t}: slår SARIMA i {r['zones_tsfm_beats_sarima']} av 9 soner (H1 "
                  f"{'støttet' if r['H1_supported'] else 'ikke støttet'}); minst fordel i pp: "
                  f"{r['min_adv_zone_pp']} (H2 {'støttet' if r['H2_supported_pp'] else 'ikke støttet'}); "
                  f"minst relativ fordel: {r['min_adv_zone_rel']}.")
    md += ["", "## RQ3: NO4 og NO5 (retro og holdout, beskrivende)", ""]
    for s in splits:
        pz = pd.DataFrame(res["per_zone"][s]).pivot(index="zone", columns="arm", values="mean")
        for z in ("NO4", "NO5"):
            if z in pz.index:
                md.append(f"- {s} {z}: " + ", ".join(f"{a} {fmt(pz.loc[z, a])}" for a in
                                                    BASELINE_ARMS + TSFM_ARMS if a in pz))
    md += ["", "## RQ4: kalibrering (holdout, TSFM mot SARIMA)", "",
           "| arm | CRPS (g/kWh) | dekning 80 % | dekning 90 % |", "|---|---|---|---|"]
    for a, r in res["calibration_summary"].items():
        md.append(f"| {a} | {fmt(r['crps'], 4)} | {fmt(r['cov80'])} | {fmt(r['cov90'])} |")
    md += ["", "| TSFM | n | CRPS-diff mot SARIMA | HLN-stat | p |", "|---|---|---|---|---|"]
    for r in res["calibration_dm"]:
        md.append(f"| {r['tsfm']} | {r['n']} | {fmt(r['mean_diff'], 4)} | {fmt(r['dm_hln'], 2)} | {fmt(r['p'], 4)} |")
    md += ["", "## RQ5: kontamineringsindikator (beskrivende)", "",
           "Fordel = tap(base) − tap(TSFM). Indikator = fordel retro − fordel holdout; HAC-SE (lag 0..3) "
           "kombinert som uavhengige perioder. z > 1,96 rapporteres som «mulig kontaminering».", "",
           "| TSFM | mot | fordel retro | fordel holdout | indikator | HAC-SE | z | mulig kontaminering |",
           "|---|---|---|---|---|---|---|---|"]
    for r in res["contamination"]:
        md.append(f"| {r['tsfm']} | {r['base']} | {fmt(r['adv_retro_pp'])} | {fmt(r['adv_holdout_pp'])} | "
                  f"{fmt(r['indicator_pp'])} | {fmt(r['hac_se'])} | {fmt(r['z'], 2)} | "
                  f"{'ja' if r['possible_contamination'] else 'nei'} |")
    md += ["", "## Antall origins per arm", ""]
    for s in splits:
        md.append(f"- {s}: " + ", ".join(f"{a} {n}" for a, n in res["n_origins"][s].items()))
    open(out_prefix + ".md", "w").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main(*sys.argv[1:4])
