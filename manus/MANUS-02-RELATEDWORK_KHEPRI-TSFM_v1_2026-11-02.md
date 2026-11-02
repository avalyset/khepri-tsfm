Arkivnøkkel: MANUS-02-RELATEDWORK_KHEPRI-TSFM_v1_2026-11-02

<!-- Owner: session B. Language: English (arXiv). No results in this section.
Every external claim has a source ID S.. in truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md (URL, date read, locator).
Read in full text by B: only DACF (S06, author PDF bundled in the DACF code repository).
For CarbonX, CarbonCast, EnsembleCI and Impermanent B read the authors' public code repositories only;
claims about them are phrased as claims about the repositories. [NR] = paper not read.
Not read at all (network policy): Leerbeck et al. 2020, Hong et al. 2016, Cramer et al. 2022, Clauß et al. 2019,
Diebold & Mariano 1995, Harvey et al. 1997, Gneiting & Raftery 2007. They carry no content claim here.
NO ABSENCE OR PRIORITY CLAIM is made. The absence checks the brief asks for (CarbonX papers' NO/SE coverage,
prospective evaluation in the papers, the building-physics / demand-response vocabulary of Clauß et al.)
could not be done from session B; only the repository-level checks below were done.
FULL-TEXT PASS by session A, 2026-11-02 ca. 09:10 UTC (SOURCES S20–S26): CarbonX, Impermanent, EnsembleCI,
Leerbeck et al. (arXiv preprint only), Cramer et al. and Clauß et al. read in full text; Hong et al. 2016 abstract only.
[NR] removed where the paper is now read. -->

# 2 Related work

## 2.1 Carbon-intensity forecasting

DACF (Maji et al. 2022a) forecasts the hourly average CI of a grid for the next 24 hours. It
predicts the production of each generation source with a separate neural network that uses
historical production, calendar features and day-ahead weather forecasts, and combines the
source forecasts with direct (operational) emission rates.
<!-- src: S06 DACF.pdf p.2 Fig. 1 caption ("the next 24 hours"), §3 p.2-3, §3.1 p.3 (inputs 1–3), p.2 Eq. 1 and Table 1 (direct emission rates) -->
It is evaluated on six regions, four in the US and two in Europe, Sweden (SE) and Germany (DE),
with ENTSO-E data for the European regions. It uses data from 2019–2021, retrains its models every
six months and reports predictions for the last six months of 2021 as the test, with MAPE as the
metric.
<!-- src: S06 DACF.pdf p.2 §2.1 (six regions; Europe: Sweden (SE), Germany (DE)); p.3 Table 3 (SE, DE: ENTSOE); p.3-4 §4.1 (2019–2021, re-train every six months, last six months of 2021, MAPE) -->
DACF is compared with the authors' own reimplementation of the method of Leerbeck et al. (2020),
since that code was not public.
<!-- src: S06 DACF.pdf p.4 §4.3 ("Since the code is not publicly available, we develop our own implementation"); bibliographic data for Leerbeck et al. from DACF.pdf p.5 ref. [14] -->

According to its public repository, CarbonCast (Maji et al. 2022b) [NR] extends DACF to
forecasts of up to 96 hours. The repository covers 13 regions, among them Sweden (SE) as the only
Nordic region, and its saved models are trained on 2020 and validated on January–June 2021; the
repository states that results similar to the paper are obtained when testing on July–December
2021. It also points to a real-time v3.0 branch in testing, which we did
not read.
<!-- src: S07 CarbonCast README.md:5 ("up to 96 hours ... extension of DACF"), README.md:30-46 (regions; Europe: DE, NL, ES, SE, PL), README.md:94 (train Jan–Dec 2020, validate Jan–Jun 2021, test Jul–Dec 2021); README.md:11 (v3.0 real-time branch, not read); bibtex README.md:159-165. Paper not read. -->
The repository of EnsembleCI (Yan et al. 2025) implements CI forecasting with
gradient-boosting, neural and ensemble learners (LightGBM, a FastAI network, CatBoost, XGBoost and
an AutoGluon weighted ensemble) and lists 11 regions, with Sweden (SE) as the only Nordic one.
<!-- src: S08 EnsembleCI README.md:17-32 (regions; Europe DE, SE, PL, NL, ES), README.md:38-43 (models), README.md:53-59 (bibtex). Paper not read. -->
In the region lists and released data of these three repositories, Sweden appears only at
country level and Norway does not appear; no series for the bidding zones NO1–NO5 or SE1–SE4 is
included.
<!-- src: SOURCES S06–S08: grep for Norway, Nordic, NO1..NO5, SE1..SE4, "NO-", "SE-<digit>" in the three repositories: no matches (subagent report, PRIORART_REPOS_REPORT.md); B checked the region lists (CarbonCast README.md:30-46, EnsembleCI README.md:17-32, DACF README.md:23-31). This is a statement about the repositories only, not about the papers. -->

Leerbeck et al. (2020) forecast average and marginal CO2 emission intensity for the Danish bidding
zone DK2 up to 24 hours ahead with 95 % prediction intervals, combining linear models with
exogenous inputs (ARIMAX) fitted to data supplied by Tmrow.
<!-- src: S23 leerbeck_arxiv.pdf (arXiv:2003.05740v1, submitted version; publisher version not read) p.1 abstract ("Danish bidding zone DK2", "ARIMAX"), p.2 ("short-term (24h ahead) forecasts with uncertainty margins (95% prediction intervals)"), p.11 §6 ("data collected and supplied by Tmrow IVS") -->
The EnsembleCI paper (Yan et al. 2025) evaluates a stacked ensemble of gradient-boosting and neural
learners on 11 grids, six in the US and five in the EU with Sweden as a country, up to four days
ahead with MAPE, testing the EU grids on the second half of 2021, and reports lower MAPE than
CarbonCast on all four days.
<!-- src: S22 ensembleci.pdf p.1 ("across 11 grids (6 in the US and 5 in the EU)", "up to 4 days into the future"), p.2 Table 1 (State/Country: Germany Sweden Spain Netherlands Poland), p.3 (LightGBM, CatBoost, NN; multi-layer stacking), p.4 (MAPE; EU test second half of 2021; day-1..4 MAPE vs CarbonCast) -->
Clauß et al. (2019) compute hourly average CO2-equivalent intensities for Scandinavian bidding
zones with an input–output method that accounts for trade between zones, from ENTSO-E generation
data (Swedish zones from the Swedish TSO), and use them as a control signal for the demand response
of residential heating; the intensities are computed for 2015 and are not forecast.
<!-- src: S25 clauss_ntnu_nva.pdf (published CC-BY version via NTNU Brage) p.1 abstract (input–output; trading between bidding zones; "six Scandinavian bidding zones"), p.6 §3.1.1 (ENTSO-E; Swedish TSO), p.10 §3.4 (all Norwegian BZs evaluated for 2015), p.14 §4.2, p.19 (CI "can actually be predicted" — suggested, not done; "forecast" 1 hit, "predict" 0 in the forecasting sense) -->
GEFCom2014 had four probabilistic forecasting tracks, on load, price, wind and solar power (Hong
et al. 2016).
<!-- src: S26 Hong et al. 2016 abstract only (DTU Orbit record); full text not accessible; no further claim. -->

## 2.2 Foundation models for carbon intensity

The CarbonX paper (Maji et al. 2025) evaluates five TSFMs (MOMENT, Chronos, TimesFM, Sundial and
Time-MoE) zero-shot for CI forecasts up to 96 hours, extended to 21 days. Its benchmark has 13 grids;
the European ones are Sweden (SE), Germany, Poland, Spain and the Netherlands, evaluated on the last
six months of 2021, and a global evaluation uses Electricity Maps data for 214 grids (2021–2024,
70/30 split) whose names are not given in the paper. The evaluations are on historical data; we found
no discussion in the paper of overlap between the models' pretraining data and the evaluation data,
and no Norwegian grid or bidding zone is named.
<!-- src: S20 carbonx.pdf (arXiv:2510.01521v2) p.2 Table 1 (five TSFMs), p.3 §3.1 ("up to 96 hours"), p.9 ("up to 3 weeks (21 days)"), p.6 §5.1 ("The European grids are Sweden (SE), Germany (DE), Poland (PL), Spain (ES), and the Netherlands (NL)"; "final six months of 2021"; 214 grids; "2021 to 2024 ... 70–30 ratio"), p.6 Table 6 (counts per continent only); searched without hits: Norway, Norwegian, NO1, SE3, bidding, Nordic, contaminat, prospective, live; "leakage" only in conformal calibration (p.6 §4.2.3) -->
The CarbonX repository provides zero-shot CI forecasts with five TSFMs (Chronos, MOMENT, Sundial,
Time-MoE and TimesFM) for 214 grids at a horizon of up to 96 hours, with an extended mode of up to
21 days.
<!-- src: S02 CarbonX README.md:95-101 (models), README.md:73 (214 grids), README.md:41 (max 96), README.md:121 (up to 21 days) -->
Norway and Sweden are included as whole countries; the released data for both are hourly series
from 2021-01-01 to 2024-12-31, and no bidding-zone series is released.
<!-- src: S02 README.md:60-72 (NO, SE in Europe list); data/forecasting-data/NO.csv and SE.csv (first and last rows 2021-01-01 00:00 and 2024-12-31 23:00); grep for NO1..NO5/SE1..SE4 outside map polygons: none -->
We found no statement in the repository about prospective evaluation, evaluation on data after
the models' release, or overlap between the models' pretraining data and the evaluation data.
<!-- src: S02 grep (prospective, live, real-time, post-release, cutoff, contaminat, leak, training data, held-out, pretrain): no hits. Scope: the repository at 542536f only; the paper arXiv:2510.01521 was not read. -->
Whether the repository corresponds exactly to the evaluation reported in the CarbonX paper could
not be verified.
<!-- src: S02 (repo does not cite the paper; README.md:1-2, README.md:93 "some code needs to be cleaned up before release") -->

The three TSFMs evaluated here come from two families: Timestral (Mistral AI) and Chronos-2
(Ansari et al. 2025 [NR]). The Timestral code is released under Apache-2.0 and the weights separately under a
"Modified MIT license"; its repository discloses neither training data nor a training cut-off.
Chronos-2 became public in October 2025: its technical report appeared on 2025-10-17, its
repository announces the release on 2025-10-20, and the Hugging Face model repository
amazon/chronos-2 dates from 2025-10-30 (D-12). The quickstart notebook in its repository gives a
maximum context of 8192 steps.
<!-- src: S03 timestral README.md:16, 150-162 (licences), grep (no training-data disclosure); S04 chronos-forecasting README.md:20 (release 20 Oct 2025), notebooks/chronos-2-quickstart.ipynb:26 (max context 8192); KG:17-18 (max context 8192; A's reading of the model card). -->

## 2.3 Contamination and live evaluation

According to its repository, Impermanent (Garza et al. 2026) is a live benchmark for
temporal generalisation in which models must forecast before the future is observed and are
scored as data arrive. The repository motivates this with the risk that, for foundation models,
"[t]raining data may overlap with evaluation data" in static benchmarks. The signals it lists are
activity series derived from GitHub Archive (stars, pushes, pull requests, issues).
<!-- src: S05 impermanent README.md:8 (subtitle "Live Benchmark for Temporal Generalization in Time Series Forecasting"), README.md:39 (quote), README.md:41, README.md:133 (signals), README.md:177-185 (bibtex). Paper not read. -->
Our post-release holdout is not a live evaluation: its forecasts were produced after the truth
had been observed. It guarantees only that the target hours postdate the public release of
Timestral (2026-10-15, the date of its GitHub release commit) and of Chronos-2 (October 2025). In
the prospective log (Section 3.10) a scheduled job issues the forecast for each 00:00 UTC origin
a few hours later, while most of the 96 target hours are still unobserved; the context ends at the
origin.
<!-- src: DEC:5-7; PRE:197-202; STA:52-53, STA:99 (data fetched 07:12–07:28 UTC, arms run 07:50–08:28 UTC on 2026-11-02); S03 git log (2026-10-15), S04 README.md:20 (2025-10-20); launchd/no.ecodeco.khepri-tsfm.v1.plist:10 (05:00 local time), issue.py:9 and :84 (waits for run.lock at most 6 h). Describes our design, not Impermanent. -->

In the paper, every model must produce point and probabilistic forecasts for the next horizon at
each cutoff before any ground truth is available, and forecasts are scored after the outcomes
arrive; it evaluates four TSFMs, among them Chronos-2, on GitHub activity series from GH Archive and
contains no energy or CI series.
<!-- src: S21 impermanent.pdf (arXiv:2603.08707v2) p.3 §3 ("must produce point and probabilistic forecasts for the next h periods before any ground truth is available"), p.4 §5, p.8 (scoring once ground truth arrives), p.2 §2 (GH Archive; four event types; 400 repositories), p.4 §3 (Chronos-2, Moirai 2.0-R-Small, TimesFM 2.5, TiRex); searched without hits: energy, electric, carbon, grid -->

## 2.4 Forecast comparison and evaluation

Real-time probabilistic forecasting exercises outside energy evaluate forecasts submitted as
quantiles with the weighted interval score and the empirical coverage of prediction intervals, for
example the US COVID-19 Forecast Hub, whose forecasts were submitted as 23 quantiles from 0.01 to
0.99 (Cramer et al. 2022).
<!-- src: S24 cramer_epmc.xml (PMC9169655, CC-BY) Results > Overall Model Accuracy (WIS; empirical coverage of PIs), Methods > Forecast Format (23 quantiles 0.01 ... 0.99), Introduction ("published weekly in real time") -->
We compare forecast accuracy with the Diebold–Mariano test (Diebold & Mariano 1995 [NR]) with the
small-sample correction of Harvey, Leybourne & Newbold (1997) [NR], and evaluate predictive
quantiles with the CRPS (Gneiting & Raftery 2007 [NR]); details are in Section 3.
<!-- src: PRE:136-142, PRE:112-114; KG:22-24 (bibliographic only) -->

## References (draft, for A)
<!-- Bibliographic data below come only from the sources named in brackets. Entries marked [ID ONLY] have no
verified title/authors; A must complete them from the source. -->
- Ansari, A. F., et al. (2025). Chronos-2: From Univariate to Universal Forecasting. arXiv:2510.15821. [from authors' bibtex, S04 README.md:148-154; not read]
- CarbonX. arXiv:2510.01521. [ID ONLY; S01 not read] <!-- repo config.json:6 lists authors Maji, Yang, Shenoy, Sitaraman, Srivastava; unverified against paper -->
- Clauß et al. (2019). Energies 12(7):1345. [ID ONLY; KG:23]
- Cramer et al. (2022). PNAS 119(15):e2113561119. [ID ONLY; KG:22]
- Diebold & Mariano (1995). [ID ONLY; KG:23]
- Garza, A., Rosillo, R., Mendoza-Smith, R., Salinas, D., Williams, A. R., Ashok, A., Goswami, M., & Juárez, J. M. (2026). Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting. arXiv:2603.08707. [from authors' bibtex, S05 README.md:177-185; not read]
- Gneiting & Raftery (2007). [ID ONLY; KG:24]
- Harvey, Leybourne & Newbold (1997). [ID ONLY; KG:23-24 and the brief]
- Hong et al. (2016). IJF 32(3):896–913. [ID ONLY; KG:22]
- Khepri v1.5.0. Zenodo. doi:10.5281/zenodo.23101127. [KG:4; author and year: A]
- Leerbeck, K., Bacher, P., Junker, R. G., Goranović, G., Corradi, O., Ebrahimy, R., Tveit, A., & Madsen, H. (2020). Short-term forecasting of CO2 emission intensity in power grids by machine learning. Applied Energy 277:115527. [from DACF.pdf p.5 ref. [14]; not read]
- Maji, D., Sitaraman, R. K., & Shenoy, P. (2022a). DACF: Day-ahead Carbon Intensity Forecasting of Power Grids using Machine Learning. e-Energy ’22. doi:10.1145/3538637.3538849. [read, S06 DACF.pdf p.1]
- Maji, D., Shenoy, P., & Sitaraman, R. K. (2022b). CarbonCast: multi-day forecasting of grid carbon intensity. BuildSys ’22, pp. 198–207. [from authors' bibtex, S07 README.md:159-165; not read]
- Mistral AI (2026). Timestral. github.com/mistralai/timestral, commit a534bdbd. [S03]
- Yan, L., Wang, L., Liu, S., & Ding, Y. (2025). EnsembleCI: Ensemble Learning for Carbon Intensity Forecasting. e-Energy ’25. doi:10.1145/3679240.3734630. [from authors' bibtex, S08 README.md:53-59; not read]
- Zenodo preregistration: [ZENODO-DOI]. OSF: registered on OSF 2026-11-02 07:49 UTC (osf.io/hncz5).
