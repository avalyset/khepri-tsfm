"""Builds BREVETPAKKE_KHEPRI-TSFM_v1_<date>.md: full text of the manuscript, README, the Zenodo
description and an anchor list (DOIs, arXiv IDs, OSF, model revisions, shas, every number with its
source) generated from truth/NUMBERS and truth/SOURCES. Written to the repository and to $V.

Usage: python build_brevetpakke.py
"""

import os
import re
import subprocess

R = os.path.dirname(os.path.abspath(__file__))
V = os.environ.get("V", "/Volumes/Vault/khepri-tsfm")
NAME = "BREVETPAKKE_KHEPRI-TSFM_v1_2026-11-02.md"
OSF = "submitted to OSF Registries 2026-11-02 07:49 UTC (osf.io/hncz5, under embargo)"

ZENODO = f"""Khepri-TSFM v1 — preregistered comparison of zero-shot time-series foundation models (Timestral-5M,
Timestral-209M, Chronos-2; pinned Hugging Face revisions, 8192-hour context, no covariates) with the Khepri v1.5
SARIMA and GBM baselines (code and hyperparameters unchanged) and a weekly seasonal-naive reference, for 96-hour
forecasts of hourly carbon intensity in the nine Nordic bidding zones NO1–NO5 and SE1–SE4.

Design, analysis code and minimum detectable effect were timestamped before any foundation-model forecast by an
OpenTimestamps proof (Bitcoin-confirmed) and the GPG-signed tag prereg-v1. The proofs are archived in this deposit
(prereg-bevis/: the PREREG tarball, sha256 6fb2c76cfdcf7235a8284d9631a64714b3aeaf3efddb997f0b173ebcbf7ab5a0, its .ots
proof and the signed tag objects). The preregistration was also {OSF}.

Contents: code (Apache-2.0), the hourly CI series every arm saw and all forecasts with 21 quantiles (CC-BY-4.0),
the output of the locked analysis (results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.md), reproduction reports, tests,
and the ledgers that tie every number in the manuscript to a file and line (truth/). Khepri v1.5 is included
byte-identically as khepri_v15/ (DOI 10.5281/zenodo.23101127). Raw ENTSO-E data are not redistributed.
Reproduce: `uv sync --frozen`, then `uv run pytest -q` and `uv run python analysis.py predictions
results/MDE_KHEPRI-TSFM_v1_2026-11-02.json <out>` (expected sha256 of the .md output:
2883d030b1832fa05e815b262490148d91296be652a48a6e7700535470c7a76a).
AI use: implementation assisted by Claude Code (Anthropic) as a tool; the author is responsible for all choices and
numbers (AIUSE_KHEPRI-TSFM_v1_2026-11-02.md)."""

MANUS = [
    ("1.1 MANUS-01 Introduction", "manus/MANUS-01-INNLEDNING_KHEPRI-TSFM_v1_2026-11-02.md", None),
    ("1.2 MANUS-02 Related work", "manus/MANUS-02-RELATEDWORK_KHEPRI-TSFM_v1_2026-11-02.md", None),
    ("1.3 MANUS-03 Methods", "manus/MANUS-03-METODE_KHEPRI-TSFM_v1_2026-11-02.md", None),
    ("1.4 MANUS-04 Results and Software and availability", "manus/MANUS-04-RESULTATER_KHEPRI-TSFM_v1_2026-11-02.tex", "latex"),
    ("1.5 References (arxiv/references.tex)", "arxiv/references.tex", "latex"),
]
MODELS = """- mistralai/Timestral-5M @ bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f
- mistralai/Timestral-209M @ 9874d252ab0aae16f7f7c999f98f98d6ad7d8365
- amazon/chronos-2 @ 29ec3766d36d6f73f0696f85560a422f50e8498c
- timestral package: github.com/mistralai/timestral @ a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff; chronos-forecasting 2.3.2
- Khepri v1.5: tag v1.5 = 9e2214f8bf9410f6fcf45d4d5b287bac6441bb47 (DOI 10.5281/zenodo.23101127; concept DOI 10.5281/zenodo.21042581)"""


def rd(p):
    return open(os.path.join(R, p), encoding="utf-8").read()


def fence(text, lang):
    return [f"```{lang}", text.rstrip(), "```"] if lang else [text.rstrip()]


def dois(text):
    out = set()
    for m in re.finditer(r'10\.\d{4,9}/[^\s,;\]}>`"]+', text):
        d = m.group(0).rstrip(".")
        while d.endswith(")") and d.count("(") < d.count(")"):
            d = d[:-1]
        out.add(d.rstrip("."))
    return sorted(out)


def main():
    head = subprocess.run(["git", "-C", R, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    pub = rd("arxiv/main.tex") + "".join(rd(p) for _, p, _ in MANUS) + rd("README.md") + ZENODO
    arx = sorted(set(re.findall(r"arXiv:\d{4}\.\d{4,5}(?:v\d)?", pub + rd("truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md"))))
    shas = sorted(set(re.findall(r"\b[0-9a-f]{64}\b|\b[0-9a-f]{40}\b", pub + rd("truth/STATE_KHEPRI-TSFM_v1_2026-11-02.md")
                                 + rd("truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md"))))
    nums = [l for l in rd("truth/NUMBERS_KHEPRI-TSFM_v1_2026-11-02.md").splitlines()
            if l.startswith("| ") and not l.startswith("| Tall")]
    out = [f"Arkivnøkkel: {NAME[:-3]}", "",
           f"Til publiseringsprompten (Brevet). Generert av build_brevetpakke.py fra main {head}.",
           "Plassholdere som settes ved publisering: \\zenodoDOI (arxiv/main.tex), [ZENODO-DOI] (MANUS-01/-03),",
           "{{ZENODO_DOI}} (README, AIUSE). Repoet er privat; repo-URL legges inn ved utgivelse.",
           "Manuskriptkilden for arXiv er arxiv/ (main.tex, references.tex) med MANUS-01–04; md-filene i manus/ er rensede",
           "arbeidsfiler (annoterte versjoner med kildekommentarer på Vault, se SOURCES).",
           f"OSF-ordlyd overalt: «{OSF}». Aldri «registered», aldri «public» eller «approved».", "",
           "# 1 Fulltekst av manus", "", "## 1.0 Tittel og abstract (arxiv/main.tex)", ""]
    out += fence(rd("arxiv/main.tex"), "latex") + [""]
    for title, p, lang in MANUS:
        out += [f"## {title}", ""] + fence(rd(p), lang) + [""]
    out += ["# 2 README", "", "````markdown", rd("README.md").rstrip(), "````", "", "# 3 Zenodo-beskrivelse", "", ZENODO, "",
            "# 4 Ankerliste (generert fra manus, README, Zenodo-beskrivelse, NUMBERS, SOURCES, STATE, DEVIATIONS)", "",
            "## 4.1 DOI-er", ""] + [f"- {d}" for d in dois(pub + rd("truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md"))]
    out += ["", "## 4.2 arXiv-ID-er", ""] + [f"- {a}" for a in arx]
    out += ["", "## 4.3 OSF", "", f"- osf.io/hncz5 — {OSF}", "- osf.io/dbwvx — tilknyttet prosjekt", "",
            "## 4.4 Modellnavn og revisjoner (PREREG §3.1)", "", MODELS, "",
            "## 4.5 sha-er (40 hex = git, 64 hex = sha256) i manus, README, Zenodo-beskrivelse, STATE og DEVIATIONS", ""]
    out += [f"- {x}" for x in shas]
    out += ["", f"## 4.6 Alle tall i manus og README med kilde ({len(nums)} rader, fra truth/NUMBERS)", "",
            "| Tall | Manus (fil:linje) | Kilde (fil:linje) |", "|---|---|---|"] + nums + [""]
    txt = "\n".join(out)
    for p in (os.path.join(R, NAME), os.path.join(V, NAME)):
        open(p, "w", encoding="utf-8").write(txt)
    print(f"{len(txt.splitlines())} linjer, {len(arx)} arXiv-ID, {len(shas)} sha, {len(nums)} tall")


if __name__ == "__main__":
    main()
