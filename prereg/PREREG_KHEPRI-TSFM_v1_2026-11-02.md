Arkivnøkkel: PREREG_KHEPRI-TSFM_v1_2026-11-02

# Khepri-TSFM v1: zero-shot time-series foundation models against the Khepri v1.5 baselines for day-ahead-to-4-day carbon-intensity forecasting in nine Nordic bidding zones

Preregistration following the OSF template "Secondary Data Preregistration". Data exist; no
TSFM forecast has been produced on real carbon-intensity (CI) data at the time of
registration. Language: English. Design source: `truth/DECISIONS_KHEPRI-TSFM_v1_2026-11-02.md`
(DESIGN v1, verbatim, with filled fields); deviations from DESIGN v1 made before registration
are listed in `truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md` (D-01 to D-08) and summarised in §6.

Author: Eirik Botten Nicolaysen (EcoDeco AS). Code: github.com/avalyset/khepri-tsfm, tag
`prereg-v1` (this registration's tarball contains the repository at that tag).

## 1. Study information

### 1.1 Research questions
- **RQ1 (holdout, post-release).** On origins from 2026-10-16 (after the release of
  Timestral on 2026-10-15), do zero-shot TSFMs (Timestral-5M, Timestral-209M, Chronos-2)
  have lower 96-h MAPE than the Khepri v1.5 SARIMA and GBM baselines?
- **RQ2 (retro).** On the Khepri v1.5 2025 test (361 origins per zone), do the TSFMs have
  lower 96-h MAPE than SARIMA and GBM? Labelled "contamination not ruled out": the 2025 data
  predate the TSFMs' training cut-offs, which are undisclosed for Timestral.
- **RQ3 (NO4/NO5).** How do the TSFMs fare in NO4 and NO5, the two zones where GBM lost to
  SARIMA in Khepri v1.5 (+2.92 pp and +0.53 pp)? Descriptive.
- **RQ4 (calibration, holdout only).** Are TSFM predictive quantiles better than SARIMA's
  (CRPS from the common quantile set; empirical coverage of the 80 % and 90 % central
  intervals)?
- **RQ5 (contamination indicator).** Is the TSFM advantage larger on the retro test than on
  the post-release holdout?

### 1.2 Hypotheses
- **H1.** On the retro test, a TSFM beats SARIMA (lower mean 96-h MAPE) in the majority of
  zones (at least 5 of 9). Evaluated separately for each TSFM arm.
- **H2.** On the retro test, the TSFM advantage over SARIMA is smallest in NO5. Primary
  measure: advantage in percentage points (pp) of MAPE, as Khepri v1.5 reports differences.
  Because NO5 has by far the lowest MAPE level (SARIMA 0.72 % in v1.5), the pp measure makes
  H2 likely by scale alone; the relative advantage (pp / SARIMA MAPE) is therefore also
  reported, as a secondary measure.
- **H0** (no difference) is reported as a genuine result. A holdout difference within ±MDE
  is reported as "not determined" ("ikke avgjort"), never as equivalence.

## 2. Data description

### 2.1 Datasets
- ENTSO-E Transparency Platform, Actual Generation per Production Type (A75), bidding zones
  NO1–NO5 and SE1–SE4, 15/60-min resolution.
  - 2019–2025: the existing Khepri raw files (`{zone}_generation_{year}.csv`), unchanged,
    as used for Khepri v1.5.
  - 2026-01-01 – 2026-11-02 06:00/07:00 UTC: fetched for this study on 2026-11-02
    07:12–07:28 UTC (`fetch_a75.py`, entsoe-py 0.8.0, `query_generation`, `psr_type=None`,
    "Actual Aggregated" kept, as in the Khepri v1 fetch pattern). The NO data end at 05:45 UTC
    and the SE data at 06:30 UTC; the last complete hour for all zones is 2026-11-02 05:00 UTC.
- CI is computed with Khepri v1.5 (DOI 10.5281/zenodo.23101127, git tag v1.5) and no study
  code of its own: `khepri.forecast.hourly_ci` → `khepri.ci.load_zone`/`ci_series`
  (AR5 lifecycle factors, materiality threshold ADR-0002, pumped-storage hours → NaN,
  Waste/Other excluded), hourly mean, `interpolate(limit=6).ffill().bfill()`.

### 2.2 Availability, access, identifiers
- Raw A75 data are public (ENTSO-E, token required) and are not redistributed. Their sha256
  sums are stamped with OpenTimestamps (`SHA256SUMS_raw2026.txt.ots`, on the author's
  volume; hashes listed in the repository's STATE file).
- The derived hourly CI series used by every arm is in the repository:
  `data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet`
  (sha256 ab308ae9f49fb9a4229d3ef089bb8b005fd149101a1e9596c9295c3e5cfa95f0, OTS stamp
  `.ots`), with per-zone/per-split metadata in `data/CI_KHEPRI-TSFM_v1_2026-11-02.meta.json`
  (sha256 97f1cf6d7c640968ec800ebefb578680bdcdf44a8269dea6bdb6f0638a5f7929).
- Access date: 2026-11-02.

### 2.3 Data collection and codebook
- CI parquet columns: `zone`, `split` (retro/holdout), `time` (UTC, hour start),
  `ci_g_per_kwh` (gCO2-eq/kWh, the v1.5 hourly series after v1.5's gap filling).
- Prediction parquet `PRED-<arm>_KHEPRI-TSFM_v1_<date>.parquet` columns: `zone`, `split`,
  `origin`, `h` (1..96), `target_time`, `actual`, `point`, `fallback` (SARIMA diurnal
  substitution, v1.5 rule), `q0.01`…`q0.99` (21 quantile columns; NaN for GBM and the
  seasonal-naive arm), `revision`.

## 3. Variables

### 3.1 Forecast arms (all univariate, no covariates)
| Arm | Specification |
|---|---|
| snaive_week | f(o+h) = y(o+h−168 h) |
| SARIMA | Khepri v1.5, unchanged: SARIMAX (2,0,1)(1,1,0,24), `enforce_stationarity=False`, `enforce_invertibility=False`, `fit(disp=False, maxiter=50)` once on `hist.loc[:train_end]`; per origin `apply()` on a 45-day window ending at the origin, `forecast(96)`; diurnal substitution on failure, flagged. Quantiles from `get_forecast(96)` (Gaussian), D-03. |
| GBM | Khepri v1.5, unchanged: LightGBM `n_estimators=200, num_leaves=31, learning_rate=0.05`, seeds 0/1/2 averaged; features day-of-week, month, CI at origin, 24 lags, horizon h; trained once on the last 365 daily origins whose 96-h targets lie at or before `train_end`. |
| Timestral-5M | `mistralai/Timestral-5M` @ `bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f`, package `timestral` 1.0.0 (github.com/mistralai/timestral @ a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff), `TimestralForecaster.from_pretrained(..., max_context=8192)`, `forecast(context, prediction_length=96)` with library defaults (`symmetric_averaging=True`, `clip_nonnegative=True`). |
| Timestral-209M | `mistralai/Timestral-209M` @ `9874d252ab0aae16f7f7c999f98f98d6ad7d8365`, as above. |
| Chronos-2 | `amazon/chronos-2` @ `29ec3766d36d6f73f0696f85560a422f50e8498c`, `chronos-forecasting` 2.3.2, `Chronos2Pipeline.predict_quantiles(..., prediction_length=96, context_length=8192)` with its 21 native levels. |

- TSFM context: the last 8192 hourly values of the same CI series the baselines use, ending
  at the origin hour inclusive (common context end for all arms, as v1.5's SARIMA window and
  GBM lags end at the origin). TSFM point forecast = the 0.5 quantile.
- Common quantile set (DESIGN [steg 2]): the 21 levels 0.01, 0.05, 0.10, …, 0.90, 0.95, 0.99,
  native in all three TSFMs.
- Inference on CPU (Apple M1, 16 GB), `torch.set_num_threads(8)`, `HF_HUB_OFFLINE=1` after
  download. Environment pinned by `uv.lock` (python 3.12.13).

### 3.2 Splits and origins
- Origins: daily 00:00 UTC with the full 96-h truth available (v1.5 rule,
  `o + 96 h <= last hour of the series`). Truth = hours o+1 … o+96.
- **Retro** = the Khepri v1.5 2025 test, exactly as published: NO train years
  2021–2024 (history from 2021), SE 2022–2024, `train_end` 2023-12-31 23:00, test
  2025-01-01 – 2025-12-31 → 361 origins per zone (2025-01-01 – 2025-12-27).
- **Holdout** = origins from 2026-10-16 with o+96 h ≤ 2026-11-02 05:00 UTC → 14 origins per
  zone (2026-10-16 – 2026-10-29). SARIMA/GBM training rule = v1.5's rule applied with test
  start 2026-10-16, parameters only (D-06): `train_end` 2025-10-15 23:00, NO train years
  2023–2025, SE 2024–2025; GBM training origins 2024-10-12 – 2025-10-11.

### 3.3 Outcome
- Loss per arm, split, zone and origin = the Khepri v1.5 MAPE (forecast.py:132-135: hours with
  |actual| ≤ 1e-6 are excluded) over the 96 target hours of the point forecast.
- Test series = the zone-averaged loss per origin (mean over the nine zones).
- CRPS (RQ4) = quantile-score approximation over the 21 levels,
  CRPS ≈ (2/21) Σ_k pinball_{τ_k}(y, q_k), averaged over the 96 hours, in gCO2-eq/kWh.
  Coverage = share of hours inside [q0.10, q0.90] and [q0.05, q0.95].

### 3.4 Inclusion and exclusion
- All nine zones, all origins satisfying the v1.5 origin rule. Lost origins (any arm missing
  any zone) are never back-filled; each comparison uses the origins where all compared arms
  have all zones. Numbers of origins per arm are reported.

## 4. Knowledge of data

- The author built Khepri and has analysed the 2025 data with SARIMA, GBM, flat and diurnal
  baselines (published in Khepri v1.5). Published v1.5 result: GBM beats SARIMA in 7 of 9
  zones (by 0.02–2.64 pp) and loses in NO4 (+2.92 pp) and NO5 (+0.53 pp).
- Before registration the author has seen: the holdout CI series and its share of filled
  pumped-storage hours (D-07); the retro SARIMA/GBM per-origin losses of NO1 and SE1 from the
  driver validation (D-01, D-02); synthetic (random-walk) TSFM latencies. No TSFM forecast on
  real CI and no SARIMA/GBM/naive forecast on the holdout has been produced.
- The H1 2026 window (2026-01-01 – 2026-06-29) was already used as a final holdout by Khepri
  v1.4 and is not used here.

## 5. Analyses

### 5.1 Statistical models
- Diebold–Mariano test with the Harvey–Leybourne–Newbold (1997) small-sample correction on
  d_t = loss(TSFM)_t − loss(baseline)_t (zone-averaged, per origin), h = 4 (overlapping 96-h
  horizons at daily origins). Long-run variance: rectangular kernel, lags 0..3 (Diebold &
  Mariano 1995); if not positive, Bartlett weights over the same lags. Statistic referred
  to t(n−1), two-sided. Comparisons: each of the 3 TSFMs against SARIMA and against GBM
  (6 tests per split). Holm-adjusted p-values across the 6 tests per split are reported
  as a secondary safeguard.
- RQ1 = holdout DM tests. RQ2 = retro DM tests.
- H1: per TSFM, count of zones where the retro mean loss of the TSFM < that of SARIMA;
  supported if ≥ 5 of 9.
- H2: per TSFM, the zone with the smallest retro advantage SARIMA − TSFM in pp; supported if
  NO5. Secondary: same with the relative advantage.
- RQ3: per-zone mean losses for NO4 and NO5, both splits, all arms; descriptive.
- RQ4: holdout CRPS and coverage per arm; DM-HLN on the zone-averaged per-origin CRPS
  difference TSFM − SARIMA.
- RQ5: advantage A = loss(baseline) − loss(TSFM) per origin (zone-averaged).
  Indicator = mean(A_retro) − mean(A_holdout), standard error = √(SE_retro² + SE_holdout²)
  with HAC (rectangular, lags 0..3) standard errors of each mean; descriptive. "Clearly
  larger advantage on retro" is operationalised as z = indicator/SE > 1.96 and reported as
  "possible contamination". The indicator also reflects any genuine change between the
  2025 and October 2026 periods; it is not a test of contamination.
- Per-zone results: descriptive tables of mean loss per arm, zone and split.
- Seasonal-naive (week) is a reference arm; it enters no test.

### 5.2 Inference criteria
- α = 0.05 two-sided for each DM test (unadjusted, as designed); Holm-adjusted p reported
  alongside.
- Holdout decision rule: if |mean d| < MDE the result is "not determined" regardless of p;
  if |mean d| ≥ MDE and p < 0.05, "TSFM better" (d < 0) or "TSFM worse" (d > 0); otherwise
  "not significant".

### 5.3 Statistical power (MDE, computed before any TSFM run)
- From the stored v1.5 per-origin metric rows of the 2025 test (SARIMA − GBM zone-averaged
  loss difference, 361 origins): σ²_LR = 7.6455 pp² (rectangular kernel, h = 4).
- MDE = (t_{0.975, n−1} + t_{0.80, n−1}) / HLN(n, h) · √(σ²_LR / n) with n = 14 holdout
  origins: **MDE = 2.989 pp**. For n = 361 (retro): 0.413 pp.
- The holdout is therefore a contamination control with low power; the retro test carries
  the power. See `results/MDE_KHEPRI-TSFM_v1_2026-11-02.md`.

### 5.4 Data traps, assumption violations, non-convergence
- Data traps are handled exactly as in Khepri v1.5, without new methods: pumped-storage hours
  give NaN (NO2/NO3/NO5), the ADR-0002 materiality threshold applies, Waste is excluded;
  gaps are filled by v1.5's `interpolate(limit=6).ffill().bfill()`, also in the truth.
- SARIMA fit failure → no SARIMA rows for that zone/split; apply/forecast failure at an origin →
  diurnal persistence substituted and flagged (v1.5 rule); the number of substitutions is
  reported. TSFM failure at an origin → origin lost for that arm, not back-filled.

### 5.5 Robustness and sensitivity
- **S1** (D-07): the DM-HLN tests repeated on the zone average over the six zones with no
  filled hours in either test window (NO1, NO4, SE1, SE2, SE3, SE4), descriptive. In the
  holdout window the share of filled hours is 54.5 % (NO2), 41.6 % (NO3) and 16.7 % (NO5);
  in 2025 it is 9.5 %, 4.7 % and 4.8 %.
- **Reproduction table** (D-08): retro mean MAPE (days 1–4) of our SARIMA and GBM against
  the published v1.5 tables, per zone. Known before registration: NO1 SARIMA converges after
  1 L-BFGS iteration in the current environment versus 22 in the 2026-10-01 v1.5 run; mean
  MAPE 2.4596 vs 2.4656 (D-02). SE1 SARIMA and NO1/SE1 GBM reproduce to ≤ 0.0004 pp.

### 5.6 Exploratory analyses
- Anything not listed above is labelled exploratory.

### 5.7 Prospective log
- From the registration onward a daily job issues all arms for origin 00:00 UTC with the
  holdout training rule (`issue.py`, launchd `no.ecodeco.khepri-tsfm.v1`), writes
  `PROSP_KHEPRI-TSFM_v1_<issue date>.parquet`, its sha256 and an OpenTimestamps stamp. Lost
  days are logged and never back-filled. The log will be analysed later, with no fixed
  date, with the same locked `analysis.py` (split `prosp`), after joining the truth from a
  later A75 pull through the same Khepri v1.5 CI code.

### 5.8 Deferred to v2 (not part of this study)
- 32768-step context, Timestral-28M and -123M, covariates.

## 6. Deviations from DESIGN v1 made before registration
D-01 prediction-keeping driver (forecast.py unchanged, validated); D-02 NO1 SARIMA fit not
bit-reproducible (cause not found; reported); D-03 SARIMA quantiles from `get_forecast`;
D-04 seasonal-naive (week) arm added; D-05 MDE from stored per-origin metric rows (no stored
2025 predictions exist); RQ2 includes SARIMA (rerun fits the 6-h budget: est. < 1 h for all
arms); D-06 holdout training rule mapped by parameters only; D-07 sensitivity S1; D-08
reproduction table. Full text in `truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md`.

## 7. Licences and responsibility
- Code Apache-2.0; derived data CC-BY-4.0. Timestral weights are under Mistral AI's
  "Modified MIT License" (revenue restriction); Chronos-2 Apache-2.0.
- AI use: implementation assisted by Claude Code (Anthropic) as a tool under the author's
  direction; the author is responsible for all choices and numbers.

## 8. Statement of integrity
The author confirms that no TSFM forecast on real CI data has been produced or seen before
this registration was submitted, and that the analysis code (`analysis.py`,
`khepri_tsfm/stats.py`) is final and committed at tag `prereg-v1`.
