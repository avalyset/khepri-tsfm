Arkivnøkkel: MANUS-01-INNLEDNING_KHEPRI-TSFM_v1_2026-11-02

# 1 Introduction

Forecasts of the carbon intensity (CI) of electricity, in grams of CO2-equivalent per kWh, are
proposed as a building block for shifting flexible electricity use to hours with lower
emissions (Maji et al. 2022a).

For the nine Nordic bidding zones NO1–NO5 and SE1–SE4, Khepri v1.5 computes an hourly CI series
from ENTSO-E generation per production type and evaluates SARIMA and gradient-boosting (GBM)
baselines over a 96-hour horizon from daily origins (Khepri v1.5, DOI 10.5281/zenodo.23101127).

On the 2025 test, GBM beat SARIMA in 7 of the 9 zones, by 0.02 to 2.64 percentage points (pp) of
mean absolute percentage error (MAPE), and lost in NO4 (+2.92 pp) and NO5 (+0.53 pp).

Time-series foundation models (TSFMs) are pretrained forecasters that can be applied to a new
series without training on it ("zero-shot").
Chronos-2 is described by its developers as
offering zero-shot support for univariate, multivariate and covariate-informed forecasting
(Ansari et al. 2025); Timestral, released by Mistral AI on 2026-10-15, comes in four sizes
from 5M to 209M parameters with 21 predictive quantiles per time step.

For a CI series, a zero-shot TSFM needs only the history of the series itself. This makes it a
direct comparison for the Khepri baselines, which are also univariate and are fitted per zone.

TSFMs have already been applied to CI: the public CarbonX repository lists zero-shot forecasts
with five TSFMs for 214 grids, among them Norway and Sweden as whole countries (CarbonX).

At bidding-zone level the baselines behave differently from zone to zone: in v1.5, NO5 had by
far the lowest MAPE level (SARIMA 0.72 %), and NO4 and NO5 were the two zones where GBM lost to
SARIMA.

Evaluating a pretrained model on historical data raises a contamination problem. If the test
period, or the series itself, was part of the pretraining corpus, a retrospective test can
overstate the accuracy the model would have on data it has not seen. The repository of
the live benchmark Impermanent states the same concern for static benchmarks: "[t]raining data may
overlap with evaluation data" (Garza et al. 2026).

For the models used here the corpus cannot be checked directly. The Timestral repository
discloses neither training data nor a training cut-off. For Chronos-2 the pretraining datasets
are named on its model card; in our reading of the card no dataset name refers to ENTSO-E, Norway
or Sweden, but a name match cannot rule out that Nordic data entered through aggregated datasets.

We therefore pair two tests. A retrospective test on the Khepri v1.5 2025 test set (361 daily
origins per zone) has more statistical power but is labelled "contamination not ruled out". A
post-release holdout uses only origins from 2026-10-16, the day after the Timestral release, so
that every target hour lies after the release of all three TSFMs; it has 14 origins per zone.

Fourteen origins give little power: the minimum detectable effect for the zone-averaged MAPE
difference, estimated from the SARIMA − GBM loss difference on the 2025 test, is 2.989 pp, against 0.413 pp on the retro test, and a holdout difference smaller than
this is reported as "not determined", not as equivalence.

The holdout is therefore a contamination control, and the difference between the TSFM advantage
on the two tests is reported as a descriptive contamination indicator, not as a test.

The contributions are as follows. We make no claim of priority.
- A preregistered comparison of three zero-shot TSFMs (Timestral-5M, Timestral-209M,
  Chronos-2) with the Khepri v1.5 SARIMA and GBM baselines and a seasonal-naive reference, for
  96-hour CI forecasts in nine Nordic bidding zones. Design, analysis code and MDE were
  timestamped before any foundation-model forecast by an OpenTimestamps proof (Bitcoin-confirmed)
  and the GPG-signed tag `prereg-v1`; the proofs are archived in Zenodo ([ZENODO-DOI]). The
  preregistration was also submitted to OSF Registries 2026-11-02 07:49 UTC (osf.io/hncz5; embargo requested, pending OSF approval).

- A design that pairs a retrospective test with a small minimum detectable effect and a
  post-release holdout, with the minimum detectable effect and the decision rule fixed before
  any TSFM forecast was made.

- Hourly predictions of every arm, the derived CI series and the code, stored with sha256 sums
  and OpenTimestamps stamps, and a deviation log in which every deviation is dated.

- A prospective log that issues all arms daily from the registration onward, to be analysed
  later with the same locked analysis code.

The rest of the paper is organised as follows. Section 2 reviews related work, Section 3
describes the data, arms, tests and deviations, [Section 4 results, Section 5 discussion: A].
