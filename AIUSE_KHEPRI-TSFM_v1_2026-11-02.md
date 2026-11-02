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
| Claude Code (Anthropic), local session A | CLI 2.1.303, model Opus 5.5 (`claude-opus-5-5`) | Wrote the code in this repository, fetched data, ran the arms and the locked analysis, filled the OSF form from the PREREG file, drafted the results section and this file. |
| Claude Code subagent | model Sonnet (Anthropic) | Step 1: read the Khepri v1.5 sources and model cards; reported file:line references, which session A checked against the code. |
| Claude Code, cloud session B | as reported in `truth/STATE-B_…` | Literature, the manuscript sections without results, and independent reproduction (see `truth/STATE-B_…` and the REPRO file). |

No model was fine-tuned or trained on project data. The forecasting models studied
(Timestral, Chronos-2) are objects of study, not tools; they are listed in the PREREG with
pinned revisions.

## Checks

- Every number in the manuscript is listed in `truth/NUMBERS_…` with file:line.
- Every external claim is listed in `truth/SOURCES_…` with URL, date read and locator.
- Results come only from `analysis.py` as locked at tag `prereg-v1`. The preregistration is anchored by the
  Zenodo deposit (DOI: {{ZENODO_DOI}}, set at publication), which holds the PREREG tarball, the OpenTimestamps
  proofs and the signed tag; additional reference: OSF https://osf.io/hncz5, registered 2026-11-02 07:49 UTC.
