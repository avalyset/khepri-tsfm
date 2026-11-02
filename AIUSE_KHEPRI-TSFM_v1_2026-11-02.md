Arkivnøkkel: AIUSE_KHEPRI-TSFM_v1_2026-11-02

# AI use in Khepri-TSFM v1

## Principle

AI tools were used as tools under the owner's direction, not as authors. The owner,
Eirik Botten Nicolaysen, is responsible for every design choice and every number in this
repository and in the manuscript. The design (DESIGN v1 in `truth/DECISIONS_…`) was written
by the owner before any computation; deviations are logged in `truth/DEVIATIONS_…`.

## Tools, versions and roles

| Tool | Version | Role |
|---|---|---|
| Claude Code (Anthropic), local session | CLI 2.1.303, model Opus 5.5 (`claude-opus-5-5`) | Wrote the code in this repository, fetched data, ran the arms and the locked analysis, filled the OSF form from the PREREG file, drafted the results section and this file. |
| Claude Code subagent | model Sonnet (Anthropic) | Step 1: read the Khepri v1.5 sources and model cards; reported file:line references, which session A checked against the code. |
| Claude Code, cloud session | as reported in `truth/STATE-B_…` | Literature, the manuscript sections without results, and independent reproduction (see `truth/STATE-B_…` and the REPRO file). |

No model was fine-tuned or trained on project data. The forecasting models studied
(Timestral, Chronos-2) are objects of study, not tools; they are listed in the PREREG with
pinned revisions.

## Checks

- Every number in the manuscript is listed in `truth/NUMBERS_…` with file:line.
- Every external claim is listed in `truth/SOURCES_…` with URL, date read and locator.
- Results come only from `analysis.py` as locked at tag `prereg-v1`. Design, analysis code and MDE were
  timestamped before any foundation-model forecast by an OpenTimestamps proof (Bitcoin-confirmed) and the
  GPG-signed tag `prereg-v1`; the proofs are archived in Zenodo (DOI: 10.5281/zenodo.23881315). The
  preregistration was also submitted to OSF Registries 2026-11-02 07:49 UTC (osf.io/hncz5; embargo requested, pending OSF approval).
