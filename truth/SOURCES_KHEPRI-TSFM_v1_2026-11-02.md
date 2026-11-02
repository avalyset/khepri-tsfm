Arkivnøkkel: SOURCES_KHEPRI-TSFM_v1_2026-11-02

Eier: økt B. Hver påstand i manus/MANUS-01/-02/-03 om en ekstern kilde står her med URL, dato lest
(UTC) og lokator. Står det ikke her, står det ikke i manus.

Nettverk i økt B (truth/CLOUDSMOKE_KHEPRI-TSFM_v1_2026-11-02.md): arxiv.org, doi.org, crossref,
mdpi.com, pnas.org og huggingface.co er blokkert; github.com er nåbar. Derfor er INGEN av de
oppgitte artiklene lest i fulltekst, med ett unntak: DACF, der forfatternes PDF ligger i kodelageret (S06).
De andre står i manus bare som bibliografiske oppføringer, merket [NR] (not read). For CarbonX, CarbonCast,
EnsembleCI og Impermanent er forfatternes offentlige kodelagre lest, og påstandene i manus er formulert som
påstander om lagrene. Titler/forfattere i referanselista kommer bare fra forfatternes egen bibtex i lagrene
eller fra DACF-referanselista; ellers står bare identifikatoren (merket [ID ONLY]).
WebSearch-sammendrag er ikke brukt som kilde for noen påstand.

Interne kilder (DECISIONS, DEVIATIONS, PREREG, MDE, STATE, KJENTGRUNNLAG) står som fil:linje i
kommentarer i manus og gjentas ikke her.

## Lest (kodelager på GitHub, lest via git clone; ingen kode kjørt)

### S02 CarbonX-kodelageret — github.com/codecexp/CarbonX @ 542536f43ba2ad97e2a6f779db98fdeea3ac1c69
Klonet 2026-11-02 08:29:54 UTC (grunn klon, én commit, datert 2025-10-02). Lest 2026-11-02 08:30–08:40 UTC
(Sonnet-subagent; hovedøkta kontrollerte selv linjene merket *).
sha256: README.md 1087fbe9866d5e807807e28a6fc787102fcac73ec45c2eea8ccf5c3f36e54f8d;
config/config.json 199702d28b41fa3db371c4c1696c35d2aed65d152673cb8c1ff882c11d0dd5c6;
data/forecasting-data/NO.csv 91cb5026d82881596091d15231ab1483c46db853574b01f6a277d7dd61f81570;
data/forecasting-data/SE.csv 2cc25dbc4bced67f907f0eadb3d56512cd61d65e3661be5efba7183401269835.
| Påstand i manus | Lokator |
|---|---|
| Lageret identifiserer seg ikke med arXiv:2510.01521 (ingen arXiv-id, tittel eller bibtex). Forfatterfeltet i config lister «Diptyaroop Maji, Kang Yang, Prashant Shenoy, Ramesh K Sitaraman, Mani Srivastava». | README.md:1-2*; config/config.json:3-8*; grep `arxiv\|bibtex\|cite\|citation\|paper\|2510` uten treff |
| Lageret oppgir prognoser for 214 nett, som inkluderer landkodene NO og SE. | README.md:60-73*; config/config.json:22-23* |
| Benchmarking-settet er 13 nett, med SE og uten NO; datoer 2020-01-01–2021-12-31. | README.md:50-59* |
| Imputeringssettet er 50 nett, med DK, FI og SE og uten NO. | README.md:80-87* |
| Utgitte data for NO og SE er timeserier på landnivå, 2021-01-01 00:00 – 2024-12-31 23:00, 35 064 rader hver. | data/forecasting-data/NO.csv:1-2, siste linje*; `wc -l` = 35 065 inkl. topptekst* |
| Ingen tidsserier for budområdene NO1–NO5 eller SE1–SE4 i utgitte data; navnene finnes bare som kartpolygoner. | config/supported-grids.geojson (NO-NO1 l. 30939 osv., subagent); grep `\b(NO[1-5]\|SE[1-4])\b\|NO[-_]\|SE[-_]` utenom geojson/csv: bare US-koder |
| Zero-shot TSFM-er: Chronos, MOMENT, Sundial, Time-MoE, Times-FM. | README.md:94-101* |
| Prognosehorisont maks 96 t; «Extended forecasting (up to 21 days)». | README.md:41*; README.md:121* |
| Ingen tekst om prospektiv/«live» evaluering, data etter modellenes slipp eller treningscutoff, kontaminering eller lekkasje. | grep `prospective, live, real-time, realtime, post-release, cutoff, cut-off, contaminat, leak, training data, held-out, pretrain` over tekstfiler: ingen treff (subagent) |
| Lageret sier selv at koden er ufullstendig. | README.md:92* |
Begrensning: om lageret svarer til evalueringen i artikkelen arXiv:2510.01521, kan ikke avgjøres uten å lese artikkelen.

### S03 Timestral-kodelageret — github.com/mistralai/timestral @ a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff
Klonet og lest 2026-11-02 ca. 08:30–08:35 UTC (subagent; alle linjer under kontrollert av hovedøkta).
sha256 README.md 1805e8a574e49880e06fb68618bd7e4bbf798e852b97ed3cfc851f5c3861d382.
| Påstand i manus | Lokator |
|---|---|
| Commit a534bdbd har meldingen «Timestral release», forfatterdato 2026-10-15 14:59:55 +0000. | `git log -1` |
| Fire størrelser: 5M, 28M, 123M, 209M (Hub-id-er mistralai/Timestral-*). | README.md:50-57 |
| Koden er Apache-2.0; vektene er utgitt separat på Hugging Face Hub under en «Modified MIT license». Lisensteksten for vektene (på Hub) er IKKE lest av B. | README.md:16, 150-162 |
| Kontekst opptil 32 768 steg. | README.md:31, 81 |
| 21 kvantiler per tidssteg. | README.md:30, 128 |
| README, LICENSE og pyproject.toml oppgir ikke treningsdata eller treningscutoff. | grep `train\|corpus\|cutoff\|pretrain` (README.md:20,22,59,67,81,87,128 er eneste treff; ingen av dem om data) |
Ikke brukt: benchmark-påstandene i README.md:20-24.

### S04 chronos-forecasting-kodelageret — github.com/amazon-science/chronos-forecasting @ 1224fafa91e1ecd6674f5204066b159e40b5e4a1
Klonet og lest 2026-11-02 ca. 08:30–08:35 UTC (subagent; linjene under kontrollert av hovedøkta).
sha256 README.md 7f9e55723daadb20f79f3d76d23370888301d917f075e9eafa3e780c78f9ff35;
notebooks/chronos-2-quickstart.ipynb c33dc42f9f131c706dee79b83c88bd983b6a1535c1d591219c8da27b6f2d6559.
| Påstand i manus | Lokator |
|---|---|
| Chronos-2 sluppet 20 Oct 2025. | README.md:20 |
| Chronos-2 gir zero-shot-støtte for univariat, multivariat og kovariat-informert prognose. | README.md:29 |
| Maks kontekstlengde 8192 for Chronos-2. | notebooks/chronos-2-quickstart.ipynb:26 |
| Bibliografisk oppføring (forfatternes bibtex): Ansari et al., «Chronos-2: From Univariate to Universal Forecasting», arXiv:2510.15821, 2025. Rapporten selv er IKKE lest [NR]. | README.md:148-154 |
| Prosjektet (koden) er Apache-2.0. Vektenes lisens og treningsdata står ikke i README; de står i KJENTGRUNNLAG:17-18 og STATE:36-41 (As lesing av modellkortet), ikke kontrollert av B. | README.md:163 |

### S06 DACF — artikkel (fulltekst) og kodelager github.com/carbonfirst/DACF @ bde62273135703c731090552436a36b464aa97ef
Klonet 2026-11-02 ca. 08:31 UTC (subagent; URL funnet med WebSearch avgrenset til github.com). DACF.pdf (5 s., sha256
fb8795a73a1d9c9909e22bd1df6d56e32937cd449ffdcc8b7d964e238a029f25) lest i sin helhet av hovedøkta 2026-11-02 ca. 08:36 UTC.
README.md sha256 3267862d35fd012af74c9a3f8f558532095905ee740f47fe890e3847de1b218a.
Merk: PDF-en oppgir kodeadressen github.com/UMass-LIDS/DACF (s. 2 fotnote 1, s. 3 §3.3), ikke carbonfirst/DACF; README.md:15-20
har artikkelens bibtex. Om PDF-en er identisk med ACM-versjonen er ikke kontrollert (doi.org blokkert); den bærer ACM-
referansen og DOI 10.1145/3538637.3538849 (s. 1).
| Påstand i manus | Lokator |
|---|---|
| Tittel, forfattere (Maji, Sitaraman, Shenoy), e-Energy ’22, DOI 10.1145/3538637.3538849 | DACF.pdf s. 1 (ACM Reference Format) |
| CI-prognoser beskrives som byggestein for å flytte forbruk til timer med lavere utslipp | s. 1 Abstract; §1 «The need for carbon-aware systems» |
| Prognoserer CI for de neste 24 timene | s. 2 Fig. 1-tekst; s. 2 §3 |
| Én ANN per produksjonskilde; input historisk produksjon, dato/tid-trekk, døgnforut værprognoser | s. 3 §3.1 punkt 1–3, Fig. 2 |
| Direkte (operasjonelle) utslippsrater, CI = Σ(E·CR)/ΣE | s. 2 Table 1, Eq. 1; §2 «Average carbon intensity» |
| Seks regioner: CA, PJM, TX, NE (USA), Sverige (SE) og Tyskland (DE) på landnivå | s. 2 §2.1 |
| SE og DE fra ENTSOE | s. 3 Table 3 |
| Trent på 2019–2021, ANN retrenes hver sjette måned, test siste seks måneder av 2021, MAPE | s. 3–4 §4.1 |
| Sammenligner med egen reimplementering av Leerbeck et al., fordi koden ikke var offentlig | s. 4 §4.3 |
| Bibliografiske data for Leerbeck et al. 2020 (forfattere, tittel, Applied Energy 277, 115527) | s. 5 ref. [14] |
| Grep i lageret: ingen Norway/Nordic/NO1–5/SE1–4; regionliste | README.md:23-31 (hovedøkta), grep (subagent) |

### S07 CarbonCast — kodelager github.com/carbonfirst/CarbonCast @ 12d6989beb30d2d1a48ea8ef8c0c83745d4dac9d (artikkel IKKE lest)
Klonet 2026-11-02 ca. 08:31 UTC (subagent; URL fra WebSearch avgrenset til github.com). Linjene kontrollert av hovedøkta 08:35 UTC.
README.md sha256 dcc2c0e5715ae0c784c8883adee73f1636fff439c4c197a262550e05d222c738.
| Påstand i manus | Lokator |
|---|---|
| «up to 96 hours», utvidelse av DACF | README.md:5 |
| 13 regioner; Europa DE, NL, ES, SE, PL (ENTSOE) | README.md:30-46 |
| Lagrede modeller: trent jan–des 2020, validert jan–jun 2021, test jul–des 2021 | README.md:94 |
| Bibtex: «CarbonCast: multi-day forecasting of grid carbon intensity», Maji, Shenoy, Sitaraman, BuildSys 2022, s. 198–207 | README.md:157-165 |
| Ikke lest: v3.0-grenen for sanntidsprognoser (README.md:11). | |

### S08 EnsembleCI — kodelager github.com/emmayly/EnsembleCI @ 613929b8e227105205c95e7317247bbd12dd63a3 (artikkel IKKE lest)
Klonet 2026-11-02 ca. 08:31 UTC (subagent; URL fra WebSearch avgrenset til github.com). Linjene kontrollert av hovedøkta.
README.md sha256 39282f01272ee7fd7e98d04fd413304cebada9fbc1b9519855613ef97a733dc0.
| Påstand i manus | Lokator |
|---|---|
| 11 regioner; Europa DE, SE, PL, NL, ES | README.md:17-32 |
| Modeller LightGBM, FastAI-nett, CatBoost, XGBoost, AutoGluon weighted ensemble | README.md:38-43 |
| Bibtex: Yan, Wang, Liu, Ding, «EnsembleCI: Ensemble Learning for Carbon Intensity Forecasting», e-Energy 2025, doi 10.1145/3679240.3734630 | README.md:53-59 |

### S05 Impermanent — kodelager github.com/TimeCopilot/impermanent @ 00ec1cde270f5f99b60061e61712c35a10326cbc (artikkel IKKE lest)
Klonet 2026-11-02 ca. 08:31 UTC (subagent; URL fra WebSearch avgrenset til github.com). Linjene kontrollert av hovedøkta.
README.md sha256 354e640849a466cba256d07c73c8cd5200431de87934bbdae6a490921ece9baf.
| Påstand i manus | Lokator |
|---|---|
| Undertittel «Live Benchmark for Temporal Generalization in Time Series Forecasting» | README.md:8 |
| Sitat «Training data may overlap with evaluation data» (statiske benchmarker, grunnmodeller) | README.md:39 |
| Modellene må prognosere før fremtiden er observert; måles etter hvert som data kommer | README.md:41 |
| Seriene er fra GitHub Archive (stars, pushes, prs_opened, issues_opened) | README.md:133 |
| Bibtex: Garza et al. 2026, «Impermanent: A Live Benchmark for Temporal Generalization in Time Series Forecasting», arXiv:2603.08707 | README.md:177-185 |

## Ikke lest (bare bibliografisk omtale i manus, merket [NR])
Identifikatorer fra truth/KJENTGRUNNLAG_KHEPRI-TSFM_v1_2026-11-02.md:2-3, 19-24. Forsøkt 2026-11-02 08:27–08:28 UTC.
| ID | Identifikator | Forsøk / grunn |
|---|---|---|
| S00 | Khepri v1.5.0, DOI 10.5281/zenodo.23101127 | Ikke forsøkt (zenodo.org ikke testet; doi.org blokkert). Fakta om v1.5 i manus kommer fra KJENTGRUNNLAG/PREREG/DEVIATIONS. |
| S01 | CarbonX, arXiv:2510.01521 | WebFetch: «getaddrinfo ENOTFOUND arxiv.org» |
| S05/S07/S08 | Artiklene Impermanent (arXiv:2603.08707), CarbonCast (BuildSys ’22), EnsembleCI (arXiv:2505.01959) | arxiv.org/doi.org blokkert; bare kodelagrene lest (over) |
| S09 | Leerbeck et al. 2020, Applied Energy 277:115527 | doi.org ikke nåbar; bibliografiske data i manus fra DACF.pdf ref. [14] |
| S10 | Cramer et al. 2022, PNAS 119(15) e2113561119 | WebFetch www.pnas.org: ENOTFOUND |
| S11 | Hong et al. 2016, IJF 32(3) 896–913 | doi.org ikke nåbar |
| S12 | Clauß et al. 2019, Energies 12(7):1345 | WebFetch www.mdpi.com: ENOTFOUND |
| S13 | Diebold & Mariano 1995 | DOI-oppslag ikke mulig (doi.org, crossref blokkert) |
| S14 | Harvey, Leybourne & Newbold 1997 | som S13 |
| S15 | Gneiting & Raftery 2007 | som S13 |

## Revisjon 1 (2026-11-02 ca. 08:50 UTC, uavhengig kontroll av manus mot kildene)
- Rettet: KG-linjenumre (DOI KG:4, Timestral-slipp KG:16); OTS gjelder tarballen av prereg-v1, ikke commiten (STA:65-66);
  D-02-tallet merket som valideringskjøring før registrering; «open material» erstattet med det som er belagt (sha256, OTS,
  daterte avvik; repoet er privat, STA:12); påstander om CarbonCast/EnsembleCI/Impermanent formulert som påstander om
  lagrene; Chronos-2-kontekst 8192 belagt med notatboka, ikke modellkortet; Chronos-2-treningsdata merket som «our reading
  of the card» (As lesing, STA:38-41, ikke kontrollert av B); holdouten beskrevet som ikke-live.
- Ikke endret (fast ordlyd i oppdraget): «[ZENODO-DOI]» og «registered on OSF 2026-11-02 07:49 UTC (osf.io/hncz5)».

## Revisjon 2 (2026-11-02 ca. 08:58 UTC, siste runde)
- Rettet: prospektiv logg utstedes noen timer etter origin (launchd/no.ecodeco.khepri-tsfm.v1.plist:10 kl. 05:00 lokal tid;
  issue.py:9, :84 venter på run.lock i maks 6 t), ikke «før fasiten finnes»; holdoutens slippdatoer belagt (S03 git log,
  S04 README.md:20); CarbonCast-testperioden sitert som README.md:94 sier den; sitatet «[t]raining data …»; D-01–D-08 i
  taggen, D-09/D-10 etterpå; «licensed», ikke «released»; Maji et al. 2022a/b.
- [NR]-markørene står bevisst i prosaen; A fjerner dem når kildene er lest.

## Ikke gjort (krav i oppdraget som ikke kunne oppfylles fra økt B)
- «Sjekk om CarbonX dekker NO/SE»: besvart bare for kodelageret (S02), ikke for artikkelen.
- «Om noe er prospektivt eller post-release»: besvart bare for CarbonX-lageret (S02, ingen treff).
- Fraværspåstander i nabolitteraturens vokabular (bygningsfysikk, demand response, jf. Clauß):
  IKKE kontrollert. Manus inneholder derfor ingen fraværspåstand.

## Fulltekstpass (økt A, 2026-11-02 ca. 09:00–09:12 UTC; etter merge av B, på oppdrag fra Eirik)
Lest lokalt (nett åpent) av en Sonnet-subagent; hvert sitat grep-kontrollert mot pdftotext-/XML-uttrekket, og hovedøkta
kontrollerte selv sju bærende sitater (alle treff). Filer i $V/tmp/fulltekst/. Ærlig User-Agent, ingen omgåelse; 403/CAPTCHA
førte til alternativ åpen kopi eller «ikke tilgjengelig». Lesedato for alle: 2026-11-02 (UTC).

### S20 CarbonX — artikkel (fulltekst) arXiv:2510.01521v2
- URL https://arxiv.org/pdf/2510.01521v2 · carbonx.pdf sha256 65498b6ce37778ea78d708f55e37a3686281d78fea86a1378d79ab28cf910347
- s.2 Tabell 1 (fem TSFM-er: MOMENT-1-large, Chronos-t5-large, TimesFM-2.0-500M, sundial-base-128m, Time-MoE-50M); s.3 §3.1 «up to 96 hours»;
  s.9 «up to 3 weeks (21 days)»; s.6 §5.1 «The European grids are Sweden (SE), Germany (DE), Poland (PL), Spain (ES), and the Netherlands (NL).»,
  «we evaluate forecasting accuracy on the final six months of 2021», 214 nett fra Electricity Maps, «2021 to 2024 … 70–30 ratio»; s.6 Tabell 6
  (bare antall per verdensdel). Søk uten treff: Norway, Norwegian, NO1, SE3, bidding, Nordic, contaminat, prospective, live.
  «leakage» bare i konform kalibrering (s.6 §4.2.3). → MANUS-02 §2.2.
### S21 Impermanent — artikkel (fulltekst) arXiv:2603.08707v2
- URL https://arxiv.org/pdf/2603.08707v2 · impermanent.pdf sha256 12f4fabf4e3a9cc8920348174b8530b182045b45628213c9e4d1d9a6677fd5ee
- s.3 §3 «must produce point and probabilistic forecasts for the next h periods before any ground truth is available»; s.4 §5; s.8 (scoring etter
  fasit); s.2 §2 (GH Archive, fire hendelsestyper, 400 repoer); s.4 §3 (Chronos-2, Moirai 2.0-R-Small, TimesFM 2.5, TiRex). Søk uten treff:
  energy, electric, carbon, grid. → MANUS-02 §2.3.
### S22 EnsembleCI — artikkel (fulltekst) arXiv:2505.01959v2
- URL https://arxiv.org/pdf/2505.01959v2 · ensembleci.pdf sha256 cca7e386935f456777e38e6cee9266a7dd85419e884ac25f879626fbee0e606a
- s.1 «across 11 grids (6 in the US and 5 in the EU)», «up to 4 days into the future»; s.2 Tabell 1 (State/Country: Germany, Sweden, Spain,
  Netherlands, Poland); s.3 (LightGBM, CatBoost, NN; stacking); s.4 (MAPE; EU-test andre halvår 2021; dag 1–4 mot CarbonCast). → MANUS-02 §2.1.
### S23 Leerbeck et al. 2020 — innsendt versjon arXiv:2003.05740v1 (utgiverversjon IKKE lest: ScienceDirect 403, ingen åpen utgiverkopi)
- URL https://arxiv.org/pdf/2003.05740 · leerbeck_arxiv.pdf sha256 2b7a3348bd8a877cb52d1f0b488e46ef4c917d7ac64ef5cb778d111662fe98bb
- s.1 abstrakt «Danish bidding zone DK2», ARIMAX, softmax-vektet kombinasjon; s.2 «short-term (24h ahead) forecasts with uncertainty margins
  (95% prediction intervals)»; s.11 §6 «data collected and supplied by Tmrow IVS». → MANUS-02 §2.1.
### S24 Cramer et al. 2022 — fulltekst PMC9169655 (CC-BY) via Europe PMC XML
- URL https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9169655/fullTextXML · cramer_epmc.xml sha256 22f3ab5b3984b6aed283af78bce89c5b3ce5a62fbbb6071d712ef3c3e362a3df
- Results > Overall Model Accuracy (WIS; «empirical coverage rates of prediction intervals»); Methods > Forecast Format («a set of 23 quantiles at
  probability levels 0.01, 0.025, 0.05, 0.10, 0.15, …, 0.95, 0.975, 0.99»); Introduction («published weekly in real time»). Lokator er seksjon
  (XML, ingen sider). → MANUS-02 §2.4.
### S25 Clauß et al. 2019 — publisert CC-BY-versjon via NTNU Brage (hdl.handle.net/11250/2598501); mdpi.com ga 403
- clauss_ntnu_nva.pdf sha256 8de0b4098b4d492c2a3bfc44e1ff06f5a1392c63e96bde64333fe6ca44bb8084
- s.1 abstrakt (input–output; handel mellom budområder; «six Scandinavian bidding zones»; DR for boligoppvarming); s.6 §3.1.1 (ENTSO-E; svenske
  BZ fra svensk TSO); s.10 §3.4 (alle norske BZ for 2015); s.14 §4.2; s.19 (CI «can actually be predicted» — antydet, ikke gjort). → MANUS-02 §2.1.
### S26 Hong et al. 2016 — KUN abstrakt (DTU Orbit); fulltekst ikke tilgjengelig (utgiver lukket; CORE 403)
- URL https://orbit.dtu.dk/en/publications/5407773d-7770-4ae7-b5d7-fcd7df6fd9bc · orbit_hong.html sha256 d85072e18685580aa29e1ca02d173e3ec6f0a4805f0ed133561faa1325b65b3b
- Abstrakt: «four tracks on load, price, wind and solar forecasting». Ingen påstand utover dette. → MANUS-02 §2.1.
### Bibliografiske metadata (referanselista i arxiv/references.tex)
- Rå arXiv-API-/Crossref-svar for 15 referanser i $V/tmp/sources/ (lest 2026-11-02; sha256 per fil i A sin kildeverifisering, ført i
  $V/tmp/manus-reserve/KILDER-RESERVE.md). Hong et al. 2016: riktig DOI 10.1016/j.ijforecast.2016.02.001.
### Chronos-2 slippdato (D-12)
- Primærkilder og sha256 i truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md D-12 (arXiv 2025-10-17; README 2025-10-20; HF amazon/chronos-2 2025-10-30;
  autogluon/chronos-2 opprettet 2025-10-06, modell 2025-11-24). Råsvar i $V/tmp/chronos2-dato/.
