Arkivnøkkel: MANUS-02-RELATEDWORK_KHEPRI-TSFM_v1_2026-11-02

# 2 Related work

## 2.1 Carbon-intensity forecasting

DACF (Maji et al. 2022a) forecasts the hourly average CI of a grid for the next 24 hours. It
predicts the production of each generation source with a separate neural network that uses
historical production, calendar features and day-ahead weather forecasts, and combines the
source forecasts with direct (operational) emission rates.

It is evaluated on six regions, four in the US and two in Europe, Sweden (SE) and Germany (DE),
with ENTSO-E data for the European regions. It uses data from 2019–2021, retrains its models every
six months and reports predictions for the last six months of 2021 as the test, with MAPE as the
metric.

DACF is compared with the authors' own reimplementation of the method of Leerbeck et al. (2020),
since that code was not public.

According to its public repository, CarbonCast (Maji et al. 2022b) extends DACF to
forecasts of up to 96 hours. The repository covers 13 regions, among them Sweden (SE) as the only
Nordic region, and its saved models are trained on 2020 and validated on January–June 2021; the
repository states that results similar to the paper are obtained when testing on July–December
2021. It also points to a real-time v3.0 branch in testing, which we did
not read.

The repository of EnsembleCI (Yan et al. 2025) implements CI forecasting with
gradient-boosting, neural and ensemble learners (LightGBM, a FastAI network, CatBoost, XGBoost and
an AutoGluon weighted ensemble) and lists 11 regions, with Sweden (SE) as the only Nordic one.

In the region lists and released data of these three repositories, Sweden appears only at
country level and Norway does not appear; no series for the bidding zones NO1–NO5 or SE1–SE4 is
included.

Leerbeck et al. (2020) forecast average and marginal CO2 emission intensity for the Danish bidding
zone DK2 up to 24 hours ahead with 95 % prediction intervals, combining linear models with
exogenous inputs (ARIMAX) fitted to data supplied by Tmrow.

The EnsembleCI paper (Yan et al. 2025) evaluates a stacked ensemble of gradient-boosting and neural
learners on 11 grids, six in the US and five in the EU with Sweden as a country, up to four days
ahead with MAPE, testing the EU grids on the second half of 2021, and reports lower MAPE than
CarbonCast on all four days.

Clauß et al. (2019) compute hourly average CO2-equivalent intensities for Scandinavian bidding
zones with an input–output method that accounts for trade between zones, from ENTSO-E generation
data (Swedish zones from the Swedish TSO), and use them as a control signal for the demand response
of residential heating; the intensities are computed for 2015 and are not forecast.

GEFCom2014 had four probabilistic forecasting tracks, on load, price, wind and solar power (Hong
et al. 2016).

## 2.2 Foundation models for carbon intensity

The CarbonX paper (Maji et al. 2025) evaluates five TSFMs (MOMENT, Chronos, TimesFM, Sundial and
Time-MoE) zero-shot for CI forecasts up to 96 hours, extended to 21 days. Its benchmark has 13 grids;
the European ones are Sweden (SE), Germany, Poland, Spain and the Netherlands, evaluated on the last
six months of 2021, and a global evaluation uses Electricity Maps data for 214 grids (2021–2024,
70/30 split) whose names are not given in the paper. The evaluations are on historical data; we found
no discussion in the paper of overlap between the models' pretraining data and the evaluation data,
and no Norwegian grid or bidding zone is named.

The CarbonX repository provides zero-shot CI forecasts with five TSFMs (Chronos, MOMENT, Sundial,
Time-MoE and TimesFM) for 214 grids at a horizon of up to 96 hours, with an extended mode of up to
21 days.

Norway and Sweden are included as whole countries; the released data for both are hourly series
from 2021-01-01 to 2024-12-31, and no bidding-zone series is released.

We found no statement in the repository about prospective evaluation, evaluation on data after
the models' release, or overlap between the models' pretraining data and the evaluation data.

Whether the repository corresponds exactly to the evaluation reported in the CarbonX paper could
not be verified.

The three TSFMs evaluated here come from two families: Timestral (Mistral AI) and Chronos-2
(Ansari et al. 2025). The Chronos-2 technical report describes a pretrained model for univariate,
multivariate and covariate-informed forecasting in a zero-shot manner; its context length is
extended to 8192 in a second training stage, multivariate and covariate-informed training relies
entirely on synthetic data, and none of the real univariate pretraining datasets it lists (its
Table 6) is an ENTSO-E or CI series; the energy-domain datasets listed are Electricity, Solar, Wind
Farms, London Smart Meters and Buildings 900K. The report gives no training cut-off or release date.

The Timestral code is released under Apache-2.0 and the weights separately under a
"Modified MIT license"; its repository discloses neither training data nor a training cut-off.
Chronos-2 became public in October 2025: its technical report appeared on 2025-10-17, its
repository announces the release on 2025-10-20, and the Hugging Face model repository
amazon/chronos-2 dates from 2025-10-30 (D-12). The quickstart notebook in its repository gives a
maximum context of 8192 steps.

## 2.3 Contamination and live evaluation

According to its repository, Impermanent (Garza et al. 2026) is a live benchmark for
temporal generalisation in which models must forecast before the future is observed and are
scored as data arrive. The repository motivates this with the risk that, for foundation models,
"[t]raining data may overlap with evaluation data" in static benchmarks. The signals it lists are
activity series derived from GitHub Archive (stars, pushes, pull requests, issues).

Our post-release holdout is not a live evaluation: its forecasts were produced after the truth
had been observed. It guarantees only that the target hours postdate the public release of
Timestral (2026-10-15, the date of its GitHub release commit) and of Chronos-2 (October 2025). In
the prospective log (Section 3.10) a scheduled job issues the forecast for each 00:00 UTC origin
a few hours later, while most of the 96 target hours are still unobserved; the context ends at the
origin.

In the paper, every model must produce point and probabilistic forecasts for the next horizon at
each cutoff before any ground truth is available, and forecasts are scored after the outcomes
arrive; it evaluates four TSFMs, among them Chronos-2, on GitHub activity series from GH Archive and
contains no energy or CI series.

## 2.4 Forecast comparison and evaluation

Real-time probabilistic forecasting exercises outside energy evaluate forecasts submitted as
quantiles with the weighted interval score and the empirical coverage of prediction intervals, for
example the US COVID-19 Forecast Hub, whose forecasts were submitted as 23 quantiles from 0.01 to
0.99 (Cramer et al. 2022).

We compare forecast accuracy with the Diebold–Mariano test (Diebold & Mariano 1995) with the
small-sample correction of Harvey, Leybourne & Newbold (1997), and evaluate predictive
quantiles with the CRPS (Gneiting & Raftery 2007); details are in Section 3.

## References

The verified reference list (metadata checked against arXiv API and Crossref records, SOURCES) is
`arxiv/references.tex`.
