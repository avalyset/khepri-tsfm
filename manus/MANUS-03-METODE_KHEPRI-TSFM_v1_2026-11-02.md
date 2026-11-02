Arkivnøkkel: MANUS-03-METODE_KHEPRI-TSFM_v1_2026-11-02

<!-- Owner: session B. Language: English (arXiv). No results in this section.
Every number carries a source comment "src: FILE:LINE". Abbreviations used in the comments:
  DEC = truth/DECISIONS_KHEPRI-TSFM_v1_2026-11-02.md
  DEV = truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md
  PRE = prereg/PREREG_KHEPRI-TSFM_v1_2026-11-02.md
  MDE = results/MDE_KHEPRI-TSFM_v1_2026-11-02.md
  STA = truth/STATE_KHEPRI-TSFM_v1_2026-11-02.md
  KG  = truth/KJENTGRUNNLAG_KHEPRI-TSFM_v1_2026-11-02.md
Line numbers refer to the files at commit 315e487 (origin/main when this section was written).
Citations marked [NR] were NOT read in full text by session B (network policy, see
truth/CLOUDSMOKE_KHEPRI-TSFM_v1_2026-11-02.md and truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md);
they are bibliographic attributions only and must be checked by the author before submission. -->

# 3 Methods

## 3.1 Study design and preregistration

The design, the analysis code and deviations D-01 to D-08 were fixed in the tagged
preregistration before any time-series foundation model (TSFM) forecast was produced on real
carbon-intensity (CI) data; D-09 and D-10 came later (Section 3.9).
<!-- src: PRE:5-9, PRE:207-213, PRE:221-224; DEV:82-101 -->
The preregistration is archived on Zenodo ([ZENODO-DOI]) and is the anchor of this study. It
contains the repository at the GPG-signed git tag `prereg-v1` (commit
74539f2af7bb6d203d8c8452e01d96a222156078) as a tarball whose sha256 is stamped with
OpenTimestamps.
<!-- src: STA:63-66 (tag prereg-v1, commit 74539f2af7bb6d203d8c8452e01d96a222156078, OTS); KG/brief: Zenodo is the anchor (STA, "OSF-sjekk og TILLEGG" section: "Manus ... siterer Zenodo-DOI-en som preregistreringens anker") -->
It was also registered on OSF 2026-11-02 07:49 UTC (osf.io/hncz5).
<!-- src: STA:68-69 (sent 2026-11-02 07:49 UTC, https://osf.io/hncz5). Wording fixed by the brief. Do NOT describe it as public or approved (STA:88-90). -->
The locked analysis is `analysis.py` with `khepri_tsfm/stats.py` at that tag.
<!-- src: PRE:222-224 -->
Deviations are listed in Section 3.9 and in full in the repository
(`truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md`).

The study has two test windows with different roles. A *retrospective* test (retro) on the
Khepri v1.5 2025 test set carries the statistical power but is labelled "contamination not
ruled out": the training cut-off of Timestral is not disclosed in its repository, and most of the 2025 test period
precedes the public release of Chronos-2 in October 2025 (D-12). A *post-release holdout* uses only forecast origins after the public
release of Timestral and serves as a contamination control with low power.
<!-- src: DEC:5-7, DEC:23-26; PRE:20-22; DEV D-12 (Chronos-2 public in October–November 2025: arXiv report 2025-10-17, README announcement 2025-10-20, HF amazon/chronos-2 2025-10-30; PRE wording handled in D-12). -->

## 3.2 Data and carbon intensity

We use ENTSO-E Transparency Platform data on actual generation per production type (A75) for
the nine Nordic bidding zones NO1–NO5 and SE1–SE4.
<!-- src: PRE:45-46 (A75, NO1–NO5, SE1–SE4) -->
For 2019–2025 we use the raw files of Khepri v1.5 unchanged. Data for 2026-01-01 to
2026-11-02 were fetched for this study on 2026-11-02 between 07:12 and 07:28 UTC with
entsoe-py 0.8.0; the last hour complete for all nine zones is 2026-11-02 05:00 UTC.
<!-- src: PRE:47-52; STA:52-53 -->
Raw ENTSO-E data are not redistributed; their sha256 sums are stamped with OpenTimestamps.
<!-- src: PRE:59-61 -->

Hourly CI (gCO2-eq/kWh) is computed with Khepri v1.5 (DOI 10.5281/zenodo.23101127, git tag
v1.5) without study-specific code: AR5 life-cycle emission factors, the ADR-0002 materiality
threshold, pumped-storage hours set to missing, Waste/Other excluded, hourly mean, and the
v1.5 gap filling `interpolate(limit=6).ffill().bfill()`.
<!-- src: PRE:53-56 (DOI 10.5281/zenodo.23101127, tag v1.5, factors and gap filling); KG:4 -->
The same filled series is used as model input and as truth, exactly as in v1.5.
<!-- src: DEV:71-72; PRE:176-178 -->
The derived CI series is in the repository (`data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet`, sha256
ab308ae9f49fb9a4229d3ef089bb8b005fd149101a1e9596c9295c3e5cfa95f0).
<!-- src: PRE:63-64; STA:56 -->

## 3.3 Forecast origins, horizon and splits

Forecast origins are daily at 00:00 UTC. Each forecast covers the 96 hours o+1 h … o+96 h, and
an origin is used only if the full 96-hour truth is available.
<!-- src: DEC:35-38 (daily 00:00 UTC, truth o+1..o+96, context ends at o inclusive); PRE:98-99 -->
All arms share the same context end: the origin hour, inclusive.
<!-- src: DEC:9-10 ("Felles kontekstslutt for alle armer"), DEC:37-38; PRE:89-91 -->

*Retro.* The Khepri v1.5 2025 test exactly as published: history from 2021 (NO) and 2022 (SE)
(v1.5 data years 2021–2024 and 2022–2024), `train_end` 2023-12-31 23:00, test period 2025-01-01 to 2025-12-31, giving
361 origins per zone (2025-01-01 to 2025-12-27).
<!-- src: PRE:100-102; DEC:48-49; STA:58 -->

*Holdout.* Origins from 2026-10-16, the day after the Timestral release on 2026-10-15, with
o+96 h ≤ 2026-11-02 05:00 UTC. This gives 14 origins per zone (2026-10-16 to 2026-10-29).
<!-- src: PRE:17-18 (release 2026-10-15), PRE:103-104 (14 origins, 2026-10-16 – 2026-10-29, ≤ 2026-11-02 05:00 UTC); STA:58 -->
For SARIMA and GBM the v1.5 training rule is applied with test start 2026-10-16, changing
parameters only (Deviation D-06): `train_end` 2025-10-15 23:00, history from 2023 (NO) and 2024
(SE) (data years 2023–2025 and 2024–2025), and GBM training origins 2024-10-12 to 2025-10-11.
<!-- src: PRE:104-106; DEV:56-60 (DEV:58-59: SARIMA fitted on hist.loc[:train_end] from 1 January of the first training year) -->
Because v1.5 reads whole calendar years, the SARIMA training span becomes 2.79 years (NO) and
1.79 years (SE), against 3.0 and 2.0 years in v1.5; preserving the span exactly would have
required a change to the v1.5 forecasting code, which we did not make.
<!-- src: DEV:61-63 -->
The window 2026-01-01 to 2026-06-29, already used as a final holdout by Khepri v1.4, is not
used.
<!-- src: PRE:130-131 -->

## 3.4 Forecasting arms

All arms are univariate; no covariates are used.
<!-- src: DEC:10; PRE:79 -->

| Arm | Specification |
|---|---|
| Seasonal naive (week) | f(o+h) = y(o+h−168 h), h = 1…96. A reference arm added for this study (D-04); it enters no test. |
| SARIMA | Khepri v1.5, unchanged: SARIMAX (2,0,1)(1,1,0,24), `enforce_stationarity=False`, `enforce_invertibility=False`, `fit(disp=False, maxiter=50)` once on the training data; per origin `apply()` on a 45-day window ending at the origin and a 96-step forecast; diurnal persistence substituted and flagged if a forecast fails. |
| GBM | Khepri v1.5, unchanged: LightGBM with 200 estimators, 31 leaves, learning rate 0.05, seeds 0, 1 and 2 averaged; features day of week, month, CI at the origin, 24 lags and horizon; trained once on the last 365 daily origins whose 96-h targets lie at or before `train_end`. |
| Timestral-5M | `mistralai/Timestral-5M` at revision bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f, package `timestral` 1.0.0 (github.com/mistralai/timestral at a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff), maximum context 8192, 96-step forecast with library defaults. |
| Timestral-209M | `mistralai/Timestral-209M` at revision 9874d252ab0aae16f7f7c999f98f98d6ad7d8365, as above. |
| Chronos-2 | `amazon/chronos-2` at revision 29ec3766d36d6f73f0696f85560a422f50e8498c, `chronos-forecasting` 2.3.2, `predict_quantiles` with prediction length 96 and context length 8192. |
<!-- src: row 1: PRE:82, DEV:42-43, PRE:158; row 2: PRE:83, DEC:41-44; row 3: PRE:84, STA:28-29; rows 4-6: PRE:85-87 -->

The TSFM context is the last 8192 hourly values of the same CI series the baselines use, and
the TSFM point forecast is the 0.5 quantile.
<!-- src: DEC:9; PRE:89-91 -->
All three TSFMs natively provide the same 21 quantile levels 0.01, 0.05, 0.10, …, 0.90, 0.95,
0.99, which form the common quantile set. SARIMA provides them from its Gaussian predictive
distribution (`get_forecast`, predicted mean + z_q · standard error), with the point forecast
unchanged (D-03). GBM and the seasonal-naive arm give no quantiles.
<!-- src: DEC:56-58; PRE:92-93; DEV:37-39; PRE:74-75 (quantile columns NaN for GBM and seasonal naive) -->

Khepri v1.5 does not store hourly predictions, so a driver repeats the v1.5 forecasting loop line
by line, calls the same v1.5 functions and keeps the predictions; the v1.5 forecasting module
itself is unchanged (D-01). Before registration this driver was validated against stored v1.5
runs: for SE1 the SARIMA per-(origin, day) MAPE differs by at most 0.00036 pp and GBM by at
most 3.6e-15; for NO1 GBM differs by at most 4.4e-16.
<!-- src: DEV:8-17 -->
The NO1 SARIMA fit is not bit-reproducible (D-02): in the pinned environment it converges after
1 L-BFGS iteration, against 22 in the 2026-10-01 v1.5 run; in the validation before registration
this gave a NO1 retro mean SARIMA MAPE of 2.4596 against 2.4656 in the stored v1.5 rows. The
reproduction table (Section 3.8) reports the final run. Data, code, library versions and BLAS thread count were
ruled out; the cause was not found. We report this rather than adjust the fit.
<!-- src: DEV:19-29; PRE:189-191 -->
The environment is pinned by `uv.lock` (Python 3.12.13). Inference ran on a CPU (Apple M1, 16 GB)
with `torch.set_num_threads(8)` and the Hugging Face hub offline after download.
<!-- src: PRE:94-95; STA:47 (python 3.12.13); khepri_tsfm/models.py:17 (set_num_threads(8)), :59 (HF_HUB_OFFLINE=1); confirmed by A 2026-11-02 for the step-7 run (run_arms.py tsfm started with HF_HUB_OFFLINE=1). -->

## 3.5 Loss

The loss per arm, split, zone and origin is the Khepri v1.5 MAPE over the 96 target hours of
the point forecast; hours with |actual| ≤ 1e-6 are excluded.
<!-- src: DEC:52-55; PRE:109-110 -->
The test series is the zone-averaged loss per origin, the mean over the nine zones.
<!-- src: PRE:111; DEC:15-16 -->
For probabilistic forecasts (RQ4) we use the quantile-score approximation of the continuous
ranked probability score (CRPS) over the 21 levels, CRPS ≈ (2/21) Σ_k pinball_{τ_k}(y, q_k),
averaged over the 96 hours, in gCO2-eq/kWh, and the empirical coverage of the central 80 %
interval [q0.10, q0.90] and 90 % interval [q0.05, q0.95] (Gneiting & Raftery 2007 [NR]).
<!-- src: PRE:112-114; DEC:56-58; KG:22-24 (Gneiting & Raftery 2007, bibliographic only) -->
Origins are never back-filled. If any compared arm misses any zone at an origin, that origin
drops out of the comparison, and the numbers of origins per arm are reported.
<!-- src: PRE:117-119; DEC:29 -->

## 3.6 Research questions, hypotheses and tests

The research questions are: RQ1, on the post-release holdout, do the TSFMs have lower 96-h MAPE
than the Khepri v1.5 SARIMA and GBM baselines; RQ2, the same question on the retro test; RQ3,
how the TSFMs fare in NO4 and NO5, the two zones where GBM lost to SARIMA in Khepri v1.5
(+2.92 pp and +0.53 pp), descriptively; RQ4, whether TSFM predictive quantiles are better than
SARIMA's on the holdout (CRPS and coverage); and RQ5, whether the TSFM advantage is larger on
the retro test than on the holdout.
<!-- src: PRE:17-29 (RQ1–RQ5; +2.92 pp and +0.53 pp at PRE:24); KG:6-7 -->

*Hypotheses.* H1: on the retro test a TSFM beats SARIMA (lower mean 96-h MAPE) in at least 5 of
the 9 zones, evaluated separately for each TSFM. H2: on the retro test the TSFM advantage over
SARIMA, in percentage points (pp) of MAPE, is smallest in NO5. Because NO5 has by far the lowest
MAPE level (SARIMA 0.72 % in v1.5), the pp measure favours H2 by scale alone, so the relative
advantage (pp divided by SARIMA MAPE) is reported as a secondary measure. The null of no
difference is reported as a result in its own right.
<!-- src: PRE:32-40; PRE:144-147 -->

*Diebold–Mariano tests.* For each TSFM against each baseline we form
d_t = loss(TSFM)_t − loss(baseline)_t on the zone-averaged per-origin losses and apply the
Diebold–Mariano test (Diebold & Mariano 1995 [NR]) with the Harvey–Leybourne–Newbold
small-sample correction (Harvey et al. 1997 [NR]), h = 4, because 96-hour horizons at daily
origins overlap. The long-run variance uses a rectangular kernel over lags 0…3, with Bartlett
weights over the same lags if it is not positive. The statistic is referred to t(n−1),
two-sided. There are 6 tests per split (3 TSFMs × SARIMA and GBM), each at α = 0.05 unadjusted,
as designed; Holm-adjusted p-values across the 6 tests per split are reported alongside as a
secondary safeguard.
<!-- src: PRE:136-142; PRE:161-162; DEC:15-17; KG:22-24 (Diebold–Mariano 1995, Harvey et al. 1997: bibliographic only) -->
RQ1 uses the holdout tests and RQ2 the retro tests. RQ4 applies the same test to the
zone-averaged per-origin CRPS difference TSFM − SARIMA on the holdout.
<!-- src: PRE:143; PRE:149-150; DEC:27-28 -->

*Holdout decision rule.* If |mean d| is smaller than the minimum detectable effect (MDE,
Section 3.7) the holdout result is "not determined", regardless of p, and never read as
equivalence. If |mean d| ≥ MDE and p < 0.05 the result is "TSFM better" (d < 0) or "TSFM worse"
(d > 0); otherwise "not significant".
<!-- src: PRE:39-40; PRE:163-165; DEC:21-22 -->

*Contamination indicator (RQ5).* With the advantage A_t = loss(baseline)_t − loss(TSFM)_t
(zone-averaged), the indicator is mean(A_retro) − mean(A_holdout), with standard error
√(SE_retro² + SE_holdout²) from HAC (rectangular, lags 0…3) standard errors of each mean. A
value with z = indicator/SE > 1.96 is reported as "possible contamination". The indicator also
reflects any genuine change between 2025 and October 2026 and is not a test of contamination.
<!-- src: PRE:151-156; DEC:24-26 -->

Per-zone results are descriptive tables of mean loss per arm, zone and split. Analyses not
listed in the preregistration are labelled exploratory.
<!-- src: PRE:157; PRE:194 -->

## 3.7 Statistical power

The MDE was computed before any TSFM run, from the stored Khepri v1.5 per-(origin, day) metric
rows of the 2025 test (D-05), because no 2025 per-origin predictions were stored. The series is
the zone-averaged SARIMA − GBM loss difference over 361 origins; its long-run variance with a
rectangular kernel and h = 4 is σ²_LR = 7.6455 pp².
<!-- src: MDE:7-12; DEV:45-51; PRE:168-169 -->
With MDE = (t_{0.975, n−1} + t_{0.80, n−1}) / HLN(n, h) · √(σ²_LR / n), where
HLN(n, h) = √((n + 1 − 2h + h(h−1)/n) / n), α = 0.05 two-sided and power 0.8, the MDE is
2.989 pp for the n = 14 holdout origins and 0.413 pp for the n = 361 retro origins.
<!-- src: MDE:13-14 (formula, α, power); MDE:15, MDE:18-19 (2.989 pp at n = 14, 0.413 pp at n = 361); PRE:170-171 -->
The holdout is therefore a contamination control with low power; the retro test carries the
power.
<!-- src: PRE:172-173; DEC:23-24 -->

## 3.8 Data traps and sensitivity analysis

Data traps are handled exactly as in Khepri v1.5, without new methods.
<!-- src: PRE:176-178; KG:13-14 -->
In the holdout window, however, the share of hours where the v1.5 CI is missing before gap
filling (pumped-storage hours) is large: 54.5 % in NO2, 41.6 % in NO3 and 16.7 % in NO5, with
longest gaps of 111, 45 and 58 hours; in 2025 the shares are 9.5 %, 4.7 % and 4.8 %. NO1, NO4
and SE1–SE4 have no filled hours in either window (D-07).
<!-- src: DEV:65-70 (0,545/111 t, 0,416/45 t, 0,167/58 t; 0,095, 0,047, 0,048; holdout window measured 2026-10-16 – 2026-11-02 04:00); PRE:186-187 -->
Since filled hours enter the truth, the preregistration adds sensitivity analysis S1: the same
Diebold–Mariano tests on the zone average over the six zones without filled hours (NO1, NO4,
SE1, SE2, SE3, SE4), reported descriptively next to the primary tests. The zone set was fixed
from the CI data before any TSFM forecast.
<!-- src: DEV:73-75; PRE:184-185 -->

A descriptive reproduction table compares our retro mean MAPE for SARIMA and GBM with the
published v1.5 tables per zone (D-08); it enters no test.
<!-- src: DEV:77-80; PRE:188-191 -->

## 3.9 Deviations

All deviations from the design and the preregistration are logged with dates in the deviation
log; the table below summarises them. D-01 to D-08 were made before registration and are part of it; D-09 and D-10 were
made after the `prereg-v1` tag and concern only the prospective log, not the arms or the
analysis.
<!-- src: PRE:207-213 (D-01–D-08 in the registration); DEV:84-90 (D-09), DEV:92-101 (D-10) -->

| ID | Deviation | Effect |
|---|---|---|
| D-01 | Prediction-keeping driver around the unchanged v1.5 forecasting code | Validated against stored v1.5 runs (Section 3.4) |
| D-02 | NO1 SARIMA fit not bit-reproducible; cause not found | Pre-registration validation: NO1 retro SARIMA mean MAPE 2.4596 vs. 2.4656 |
| D-03 | SARIMA quantiles from the Gaussian predictive distribution | Point forecast unchanged |
| D-04 | Seasonal naive (week) added as a new reference arm | Enters no test |
| D-05 | MDE from stored v1.5 per-origin metric rows | No 2025 predictions were stored |
| D-06 | Holdout training rule mapped by parameters only | SARIMA training span 2.79 y (NO), 1.79 y (SE) vs. 3.0 and 2.0 y |
| D-07 | Large share of filled pumped-storage hours in the holdout | Sensitivity S1 on six zones without filled hours |
| D-08 | Reproduction table against published v1.5 results | Descriptive |
| D-09 | Bug fix in the prospective-log issuer (chronological splicing of new A75 data) | Prospective log only; analysis and arms unchanged |
| D-10 | Guard in the prospective-log issuer that skips a day's issue while another heavy job runs; such days are logged as lost, never back-filled | Prospective log only; analysis and arms unchanged |
<!-- src: D-01 DEV:8-17; D-02 DEV:19-29; D-03 DEV:36-39; D-04 DEV:41-43; D-05 DEV:45-51; D-06 DEV:55-63; D-07 DEV:65-75; D-08 DEV:77-80; D-09 DEV:84-90; D-10 DEV:94-99 -->

## 3.10 Prospective log

From registration onward, a daily job issues all arms for the 00:00 UTC origin with the holdout
training rule and writes each issue with its sha256 and an OpenTimestamps stamp. Lost days are
logged and never back-filled. The log will be analysed later, with no fixed date, with the same
locked `analysis.py`, after joining the truth from a later A75 pull through the same Khepri v1.5
CI code. It is not part of the results of this paper.
<!-- src: PRE:197-202; DEC:29-31; DEV:94-99 -->

## 3.11 Deferred to a later version

A 32 768-step context, Timestral-28M and Timestral-123M, and covariates are deferred to a later
version and are not part of this study.
<!-- src: PRE:205; DEC:30-31 -->

## 3.12 Licences

The code is licensed under Apache-2.0 and the derived data under CC-BY-4.0. The Timestral weights
are under Mistral AI's "Modified MIT License", which includes a revenue restriction; Chronos-2
is under Apache-2.0.
<!-- src: PRE:216-217; STA:74 (LICENSE, LICENSE-DATA); STA:37 (Modified MIT, revenue limit) -->
