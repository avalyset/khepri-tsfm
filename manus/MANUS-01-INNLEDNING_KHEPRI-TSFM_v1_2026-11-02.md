Arkivnøkkel: MANUS-01-INNLEDNING_KHEPRI-TSFM_v1_2026-11-02

<!-- Owner: session B. Language: English (arXiv). No results in this section.
External claims: source IDs S.. refer to truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md (URL, date read, locator).
Internal numbers: FILE:LINE with the abbreviations of MANUS-03 (DEC, DEV, PRE, MDE, STA, KG), files at commit 315e487.
[NR] = not read in full text by session B; bibliographic attribution only. -->

# 1 Introduction

Forecasts of the carbon intensity (CI) of electricity, in grams of CO2-equivalent per kWh, are
proposed as a building block for shifting flexible electricity use to hours with lower
emissions (Maji et al. 2022, DACF).
<!-- src: S06 DACF.pdf p.1, Abstract ("An essential building block for these optimizations is future knowledge of the carbon intensity of the supplied electricity") and §1 "The need for carbon-aware systems" -->
For the nine Nordic bidding zones NO1–NO5 and SE1–SE4, Khepri v1.5 computes an hourly CI series
from ENTSO-E generation per production type and evaluates SARIMA and gradient-boosting (GBM)
baselines over a 96-hour horizon from daily origins (Khepri v1.5, DOI 10.5281/zenodo.23101127).
<!-- src: PRE:45-46, PRE:53-56 (A75 generation per production type, nine zones, Khepri v1.5 CI); DEC:35-38 (daily origins, 96 h); KG:2 (DOI) -->
On the 2025 test, GBM beat SARIMA in 7 of the 9 zones, by 0.02 to 2.64 percentage points (pp) of
mean absolute percentage error (MAPE), and lost in NO4 (+2.92 pp) and NO5 (+0.53 pp).
<!-- src: KG:5-7; PRE:124-125. Cite against the v1.5 DOI, never arXiv:2608.29717 (KG:2-9). -->

Time-series foundation models (TSFMs) are pretrained forecasters that are applied to a new
series without training on it ("zero-shot"). Chronos-2 is described by its developers as
offering zero-shot support for univariate, multivariate and covariate-informed forecasting
(Ansari et al. 2025 [NR]); Timestral, released by Mistral AI on 2026-10-15, comes in four sizes
from 5M to 209M parameters with 21 predictive quantiles per time step.
<!-- src: S04 chronos-forecasting README.md:29 (zero-shot), README.md:148-154 (bibtex); S03 timestral README.md:30 (21 quantiles), README.md:50-57 (5M, 28M, 123M, 209M), git log a534bdbd "Timestral release" 2026-10-15; KG:15 (released 2026-10-15) -->
For a CI series, a zero-shot TSFM needs only the history of the series itself. This makes it a
natural comparison for the Khepri baselines, which are also univariate and are fitted per zone.
<!-- src: DEC:9-10 (no covariates, context 8192 h); PRE:79-87 (all arms univariate; SARIMA/GBM fitted per zone) -->
TSFMs have already been applied to CI: the public CarbonX repository lists zero-shot forecasts
with five TSFMs for 214 grids, among them Norway and Sweden as whole countries (CarbonX [NR]).
<!-- src: S02 CarbonX README.md:73 (214 grids), README.md:60-72 (NO, SE in the Europe list), README.md:95-101 (Chronos, MOMENT, Sundial, Time-MoE, Times-FM); config/config.json:22-23. The paper arXiv:2510.01521 was not read; whether the repo matches the paper is unverified (SOURCES S02). -->
At bidding-zone level the baselines behave differently from zone to zone: in v1.5, NO5 had by
far the lowest MAPE level (SARIMA 0.72 %), and NO4 and NO5 were the two zones where GBM lost to
SARIMA.
<!-- src: PRE:23-24, PRE:35-36; KG:5-7 -->

Evaluating a pretrained model on historical data raises a contamination problem. If the test
period, or the series itself, was part of the pretraining corpus, a retrospective test can
overstate the accuracy the model would have on data it has not seen. Live benchmarks are
motivated by the same concern; the Impermanent benchmark, for example, states that with
static benchmarks "training data may overlap with evaluation data" (Garza et al. 2026 [NR]).
<!-- src: S05 impermanent README.md:39 (quote), README.md:41 (live evaluation). The paper arXiv:2603.08707 was not read. -->
For the models used here the corpus cannot be checked directly. The Timestral repository
discloses neither training data nor a training cut-off. For Chronos-2 the pretraining datasets
are named on its model card, and no dataset name refers to ENTSO-E, Norway or Sweden; a name
match cannot, however, rule out that Nordic data entered through aggregated datasets.
<!-- src: S03 (grep train|corpus|cutoff|pretrain in README.md, LICENSE, pyproject.toml: no disclosure); KG:17-18; STA:38-41 (A's step-1 reading of the Chronos-2 model card; NOT re-read by B, huggingface.co blocked). The last clause is B's reasoning, not a sourced fact. -->

We therefore pair two tests. A retrospective test on the Khepri v1.5 2025 test set (361 daily
origins per zone) has statistical power but is labelled "contamination not ruled out". A
post-release holdout uses only origins from 2026-10-16, the day after the Timestral release, so
that every target hour lies after the release of all three TSFMs; it has 14 origins per zone.
<!-- src: PRE:100-104; DEC:5-7; STA:58. Chronos-2 release 2025-10-20 (S04 README.md:20) precedes the holdout. -->
Fourteen origins give little power: the minimum detectable effect for the zone-averaged MAPE
difference is 2.989 pp, against 0.413 pp on the retro test, and a holdout difference smaller than
this is reported as "not determined", not as equivalence.
<!-- src: MDE:18-21; PRE:163-165, PRE:170-171 -->
The holdout is therefore a contamination control, and the difference between the TSFM advantage
on the two tests is reported as a descriptive contamination indicator, not as a test.
<!-- src: DEC:23-26; PRE:151-156, PRE:172-173 -->

The contributions are as follows. We make no claim of priority.
- A preregistered comparison of three zero-shot TSFMs (Timestral-5M, Timestral-209M,
  Chronos-2) with the Khepri v1.5 SARIMA and GBM baselines and a seasonal-naive reference, for
  96-hour CI forecasts in nine Nordic bidding zones. The preregistration is archived on Zenodo
  ([ZENODO-DOI]) and was registered on OSF 2026-11-02 07:49 UTC (osf.io/hncz5).
  <!-- src: PRE:79-87; STA:63-69; STA "OSF-sjekk og TILLEGG" (Zenodo is the anchor; OSF never described as public or approved) -->
- A design that pairs a powered retrospective test with a post-release holdout, with the
  minimum detectable effect and the decision rule fixed before any TSFM forecast was made.
  <!-- src: DEC:18-22; MDE:3-4 (computed before any TSFM prediction) -->
- Open material: all hourly predictions of every arm, the derived CI series, the code and the
  timestamped deviation log.
  <!-- src: PRE:62-75 (derived CI and prediction files); DEV:1-4 (deviation log with sha256 + OTS); STA:99-102 (prediction files written, sha256, OTS). NOTE for A: confirm that predictions/ will be in the public release. -->
- A prospective log that issues all arms daily from the registration onward, to be analysed
  later with the same locked analysis code.
  <!-- src: PRE:197-202 -->

<!-- [RESULTS SUMMARY: one paragraph, written by A after freeze. B has not read or used RESULTATER.] -->

The rest of the paper is organised as follows. Section 2 reviews related work, Section 3
describes the data, arms, tests and deviations, [Section 4 results, Section 5 discussion: A].
