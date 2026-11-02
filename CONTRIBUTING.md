<!-- Arkivnøkkel: CONTRIBUTING (fast navn) — Khepri-TSFM v1 -->
# Contributing

Khepri-TSFM v1 is a preregistered study. The analysis code and the arms are frozen at tag
`prereg-v1`; changes to them would change the study and are not accepted as contributions.
Corrections are recorded as deviations in `truth/DEVIATIONS_*`, never as silent edits.

## Issues

Open an issue at https://github.com/avalyset/khepri-tsfm/issues. The repository is maintained
by one person; there is no guarantee of a reply or of a fix within any time frame.

## Reporting a problem with the data or the numbers

Please include:

1. the file and line (for example `results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.md:13` or a
   row of a `predictions/PRED-*` file: zone, split, origin, h);
2. what you expected and what you found, with the command you ran;
3. the output of `uv run python repro_from_ci.py verify` (sha256 of the published files).

Upstream data problems (missing or revised ENTSO-E A75 values, pumped-storage hours) belong to
the ENTSO-E Transparency Platform; the carbon-intensity method belongs to Khepri v1.5
(https://github.com/avalyset/khepri). Report them there as well if they are not specific to this
study.

## Tests

```bash
uv sync --frozen
uv run pytest -q
```
