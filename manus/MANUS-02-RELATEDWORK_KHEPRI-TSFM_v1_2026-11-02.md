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
could not be done from session B; only the repository-level checks below were done. -->

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
DACF is compared with the authors' own reimplementation of the method of Leerbeck et al. (2020) [NR],
since that code was not public.
<!-- src: S06 DACF.pdf p.4 §4.3 ("Since the code is not publicly available, we develop our own implementation"); bibliographic data for Leerbeck et al. from DACF.pdf p.5 ref. [14] -->

According to its public repository, CarbonCast (Maji et al. 2022b) [NR] extends DACF to
forecasts of up to 96 hours. The repository covers 13 regions, among them Sweden (SE) as the only
Nordic region, and its saved models are trained on 2020 and validated on January–June 2021; the
repository states that results similar to the paper are obtained when testing on July–December
2021. It also points to a real-time v3.0 branch in testing, which we did
not read.
<!-- src: S07 CarbonCast README.md:5 ("up to 96 hours ... extension of DACF"), README.md:30-46 (regions; Europe: DE, NL, ES, SE, PL), README.md:94 (train Jan–Dec 2020, validate Jan–Jun 2021, test Jul–Dec 2021); README.md:11 (v3.0 real-time branch, not read); bibtex README.md:159-165. Paper not read. -->
The repository of EnsembleCI (Yan et al. 2025) [NR] implements CI forecasting with
gradient-boosting, neural and ensemble learners (LightGBM, a FastAI network, CatBoost, XGBoost and
an AutoGluon weighted ensemble) and lists 11 regions, with Sweden (SE) as the only Nordic one.
<!-- src: S08 EnsembleCI README.md:17-32 (regions; Europe DE, SE, PL, NL, ES), README.md:38-43 (models), README.md:53-59 (bibtex). Paper not read. -->
In the region lists and released data of these three repositories, Sweden appears only at
country level and Norway does not appear; no series for the bidding zones NO1–NO5 or SE1–SE4 is
included.
<!-- src: SOURCES S06–S08: grep for Norway, Nordic, NO1..NO5, SE1..SE4, "NO-", "SE-<digit>" in the three repositories: no matches (subagent report, PRIORART_REPOS_REPORT.md); B checked the region lists (CarbonCast README.md:30-46, EnsembleCI README.md:17-32, DACF README.md:23-31). This is a statement about the repositories only, not about the papers. -->

<!-- [TO WRITE after reading — B could not read these: Leerbeck et al. 2020 (Applied Energy 277:115527);
Hong et al. 2016 (IJF 32(3):896–913); Cramer et al. 2022 (PNAS 119(15):e2113561119);
Clauß et al. 2019 (Energies 12(7):1345). Include the absence check in the building-physics and
demand-response vocabulary (Clauß et al.) before any statement about what this literature does or does not cover.] -->

## 2.2 Foundation models for carbon intensity

The CarbonX repository provides zero-shot CI forecasts with five TSFMs (Chronos, MOMENT, Sundial,
Time-MoE and TimesFM) for 214 grids at a horizon of up to 96 hours, with an extended mode of up to
21 days (CarbonX [NR]).
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

According to its repository, Impermanent (Garza et al. 2026) [NR] is a live benchmark for
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

## 2.4 Forecast comparison and evaluation

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
