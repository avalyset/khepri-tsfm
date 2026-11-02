Arkivnøkkel: STATE_KHEPRI-TSFM_v1_2026-11-02

Eier: økt A (lokal Mac). Tilstand påstås kun herfra.

## Oppsett
- Start 2026-11-02T06:56:29Z. `df -h /` ved start: 460Gi, 13Gi brukt, 31Gi ledig (30 %).
- Vault-vakt: OK. V=/Volumes/Vault/khepri-tsfm, env.sh opprettet.
- Khepri v1.5: tagg v1.5 = commit 9e2214f8bf9410f6fcf45d4d5b287bac6441bb47;
  origin/main 70571f2067a4013537ad472e59922475958a47f5 er merge-commit med identisk tre
  (`git diff --stat v1.5 origin/main` tom). Pakket ut til $V/khepri-v1.5.
- GPG-signering C96D4E5C5636088C: test OK.
- Repo: github.com/avalyset/khepri-tsfm, PRIVAT. Arbeidstre $V/repo.
- Kreditt (formåling): se $V/CREDITCHECK_KHEPRI-TSFM_v1_2026-11-02.md (bare på Vault).
  204 av 250 USD sky-kreditt igjen; uke 47 % brukt (2026-11-02 ~07:0x UTC).

## Milepæler
| M | Steg | Status | UTC |
|---|---|---|---|
| M0 | 0 repo, truth/ | FERDIG, commit 6d89c93 | 2026-11-02 |
| M1 | 1 kilder, 2 latens, 3 data | FERDIG, commit 38b8441 | 2026-11-02 |
| M2 | 4 MDE, PREREG, OSF | FERDIG: OSF SENDT https://osf.io/hncz5 (07:49 UTC), embargo til 2027-12-31, venter admin-godkjenning | 2026-11-02 |
| M3 | 6 logg, 7 kjøring, 8 analyse | steg 7 startet etter OSF-innsending | 2026-11-02 |
| M4 | 9 frys | ikke startet | |

## Steg 1 (kilder, Sonnet-subagent; råsvar i $V/tmp/steg1/ med sha256 i subagentrapport)
- Origin 00:00 UTC daglig, H = 96 (forecast.py:4-5, 49, 183-184). Fasit = timene o+1..o+96 (forecast.py:153-155).
- SARIMA (2,0,1)(1,1,0,24), tilpasset én gang på `hist.loc[:train_end]`, frosne parametre,
  `apply()` på 45-døgnsvindu per origin (forecast.py:186-192, 201-214). GBM LightGBM 200/31/0,05,
  frø 0,1,2, 28 features, 365 origins med mål ≤ train_end (forecast.py:93-128, 163-168).
- MAPE forecast.py:132-135. Ingen kvantiler og ingen prediksjoner lagres i v1.5.
- 2025-prediksjoner per origin: finnes ikke. Per-(origin, dag)-metrikkrader finnes og reproduserer
  publiserte tall (±0,005) for alle ni soner (eds-revisjon/_data/s2-j2b og s2-ren std_ren365).
- HF-revisjoner: amazon/chronos-2 29ec3766d36d6f73f0696f85560a422f50e8498c;
  mistralai/Timestral-5M bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f;
  mistralai/Timestral-209M 9874d252ab0aae16f7f7c999f98f98d6ad7d8365;
  GitHub mistralai/timestral main a534bdbd244d64f3d9d743f46c7bf6fc330ed4ff (Apache-2.0).
  Timestral-vekter: «Modified MIT License» (sha256 648194727930df73…fc8c), inntektsgrense 20 M USD/mnd.
- Chronos-2-treningsdata: navnetreff (ingen ENTSO-E/Norge/Sverige/Nordic i navnene):
  chronos_datasets electricity_15min, monash_australian_electricity, monash_electricity_hourly,
  monash_electricity_weekly; GiftEvalPretrain australian_electricity_demand, covid19_energy,
  gfc12_load, gfc14_load, gfc17_load, residential_load_power. Timestral: treningsdata ikke oppgitt.

## Steg 2 (latens) — results/LATENS_KHEPRI-TSFM_v1_2026-11-02.md
- Batch 9 median: Timestral-5M 0,14 s, Timestral-209M 1,80 s, Chronos-2 0,92 s. SARIMA-tilpasning 17,8 s,
  0,07 s per origin. Anslag steg 7 < 1 t (grense 6 t): steg 7 går.
- Felles kvantilsett: alle 21 nivåer 0,01–0,99 (native i begge TSFM-familier).
- venv $V/.venv, python 3.12.13, uv.lock i repoet; torch 2.15.0, chronos-forecasting 2.3.2,
  timestral 1.0.0 (git), transformers 5.22.1, opentimestamps-client 0.8.0, scipy 1.17.1, scikit-learn 1.9.0.
- Torch og LightGBM i samme prosess gir segfault (rc 139): kjøres i separate prosesser.

## Steg 3 (data, M1)
- A75 2026 hentet 2026-11-02 07:12–ca. 07:28 UTC (fetch_a75.py, end 07:00Z), 9 soner, $V/data/raw/entsoe-rest-2026/
  (aldri i git). NO slutter 05:45 UTC, SE 06:30 UTC. Siste komplette time for alle: 2026-11-02 05:00 UTC.
  sha256 per fil i $V/data/raw/entsoe-rest-2026/SHA256SUMS_raw2026.txt, OTS-stempel .ots (venter på Bitcoin).
- 2019–2025 leses på plass fra ~/khepri-data/raw/entsoe-rest og ~/khepri-data/se/raw/entsoe-rest (symlenker i $V/data/raw/merged).
- CI: data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet sha256 ab308ae9f49fb9a4229d3ef089bb8b005fd149101a1e9596c9295c3e5cfa95f0,
  meta sha256 97f1cf6d7c640968ec800ebefb578680bdcdf44a8269dea6bdb6f0638a5f7929, OTS-stempel .ots.
- Origins: retro 361 per sone (2025-01-01 – 2025-12-27), holdout 14 per sone (2026-10-16 – 2026-10-29).
- Pumpetime-NaN før utfylling i holdout: NO2 54,5 %, NO3 41,6 %, NO5 16,7 % (DEVIATIONS D-07).

## Steg 4 (M2)
- MDE: results/MDE_KHEPRI-TSFM_v1_2026-11-02.md — 2,989 pp (n = 14, h = 4, σ²_LR 7,6455 fra 361 retro-origins); retro n = 361: 0,413 pp.
- PREREG: prereg/PREREG_KHEPRI-TSFM_v1_2026-11-02.md (OSF-mal «Secondary Data Preregistration»), signert tagg prereg-v1
  (tag-objekt bab425f2a39ad3f6cb46cdc789828bc83e95c1db → commit 74539f2af7bb6d203d8c8452e01d96a222156078), pushet.
- Tarball: $V/PREREG_KHEPRI-TSFM_v1_2026-11-02.tar.gz (git archive prereg-v1, 5 822 754 B),
  sha256 6fb2c76cfdcf7235a8284d9631a64714b3aeaf3efddb997f0b173ebcbf7ab5a0, OTS-stempel .ots (venter på Bitcoin).
- OSF, første forsøk ca. 07:40 UTC: Eirik ikke innlogget (videresendt til accounts.osf.io/login); stoppet før steg 7.
- OSF, andre forsøk etter at Eirik logget inn: registrering SENDT 2026-11-02 07:49 UTC (OSF viser 8:49 AM lokal tid).
  **Registrering: https://osf.io/hncz5** (malen «Secondary Data Preregistration»), tilknyttet prosjekt https://osf.io/dbwvx
  (OSF-utkast 6ae83f66e155f9e3fc296ed7). Lisens CC-BY 4.0. Vedlegg: PREREG_KHEPRI-TSFM_v1_2026-11-02.tar.gz (5,8 MB).
  Embargo med sluttdato 2027-12-31. Status «Pending approval»: OSF sender godkjenningslenke på e-post til admin
  (Eirik); uten handling godkjennes den automatisk etter 48 t. Godkjenning i nettleseren var ikke mulig (ingen knapp på siden).
  D-09 er nevnt i feltet «Prior knowledge». Registrerings-DOI: ingen ennå.
- Etter tagg: D-09 (feilretting i issue.py, commit e4231f5). LICENSE (Apache-2.0) og LICENSE-DATA (CC-BY-4.0) lagt til.

## Steg 5 (B)
- STATE-B er tom (bare arkivnøkkel) ved M2. Ingen ettermåling av kreditt.

## Maskinregel (TILLEGG fra Eirik, 2026-11-02 ca. 07:52 UTC)
- SES-sjekk før hver tung kjøring; én tung jobb om gangen; kun lesing under sjel-eller-speil.
- Sjekk 07:52 UTC: STATUS_SES siste linje «2026-11-02T06:41:24Z STEMPEL F5-prosessen er avsluttet»
  (PAUSET 06:38:29Z), ingen LAS, pid 41217/41402 lever ikke → baseline-kjøringen (startet 07:50:33Z) fortsetter.

## OSF-sjekk og TILLEGG (2026-11-02 ca. 08:25 UTC)
- $V/OSFSJEKK_KHEPRI-TSFM_v1_2026-11-02.md: embargo_initiated på dbwvx 07:49:55Z (vxm64); embargo_approved mangler;
  admin-varsel ikke sendt av OSF (Eiriks konklusjon i TILLEGG); auto-godkjenning ventes (help.osf.io/article/330).
- TILLEGG fra Eirik: OSF gater ingenting; ingen flere OSF-sjekker, ingen ny registrering, ingen henvendelse til OSF.
- Steg 9-krav: Zenodo-deponeringen får PREREG-tarballen, alle .ots-bevis (ots upgrade der mulig) og tagg-signaturen
  for prereg-v1. Manus, README og CITATION.cff siterer Zenodo-DOI-en som preregistreringens anker og osf.io/hncz5 som
  tilleggsreferanse med «registrert 2026-11-02 07:49 UTC». Ingen tekst påstår at OSF-registreringen er offentlig eller godkjent.

## GitHub-app-tilgang for økt B (TILLEGG, ca. 08:20 UTC)
- `gh api /user/installations` → 403 («must authenticate with an access token authorized to a GitHub App»).
- Chrome: github.com/settings/installations viser appen «Claude» (installasjon 92484438). «Configure» krever
  «Confirm access» (sudo-modus: passkey/GitHub Mobile/autentiseringsapp/passord). Ikke utført; ingen endring gjort.
  Repo-id avalyset/khepri-tsfm: se svaret. Eirik må selv bekrefte tilgang og legge til repoet.

## Steg 7–8 (M3)
- SES-sjekk 07:52Z og 08:08Z: pauset, ingen LAS → kjørt. Baselines 07:50:33–08:07Z, TSFM 08:08–08:28Z (serielt, run.lock).
- predictions/PRED-{snaive_week,SARIMA,GBM,Timestral-5M,Timestral-209M,Chronos-2}_KHEPRI-TSFM_v1_2026-11-02.parquet,
  324 000 rader hver (9 soner × (361 + 14) origins × 96 t); sha256 i predictions/PRED_KHEPRI-TSFM_v1_2026-11-02.sha256;
  OTS-stempel per fil. SARIMA-fallback: 0 origins. Ingen tapte origins.
- analysis.py uendret siden prereg-v1 (`git diff --stat prereg-v1` tom for analysis.py, khepri_tsfm/, run_arms.py).
  Utdata: results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.{md,json}.
- Reproduksjon: results/REPRO-V15_KHEPRI-TSFM_v1_2026-11-02.md — alle |Δ| ≤ 0,005 mot v1.5-tabellene unntatt NO1 SARIMA −0,0104 (D-02).
- Observasjon: NO5-CI i holdout er konstant 24,0 g/kWh (1 unik verdi fra 2026-10-01; 3 291 unike i 2025), så NO5-holdout-MAPE
  er 0,000 for SARIMA, snaive og alle TSFM (GBM 0,047). NO5-holdouten er uinformativ; rapporteres slik.

## Økt B og eierskap (KORREKSJON fra Eirik, ca. 08:35 UTC)
- Eirik ga GitHub-appen tilgang manuelt. Verifisert 08:34 UTC i Chrome (github.com/settings/installations/92484438):
  «Only select repositories», 6 valgte, blant dem avalyset/khepri-tsfm. (`gh api /user/installations/92484438/repositories`
  avvises fortsatt for OAuth-token.) Økt B kjører.
- Eierskap: B eier MANUS-01/02/03 og SOURCES; A eier MANUS-04 og NUMBERS. A har ikke skrevet MANUS-01–03 i repoet;
  A sin kildeverifisering (15 referanser, råsvar i $V/tmp/sources/) ligger som reserve i $V/tmp/manus-reserve/.
- Frist: «manus ferdig» i STATE-B innen 10:30 UTC, ellers brukes reserven. REPRO: maks 1 t etter «manus ferdig», ellers fallback-subagent.

## RESULTATER byte-lik analysis.py (RETTELSE fra Eirik, ca. 08:50 UTC)
- To håndførte tillegg (SARIMA-fallbacks 0/3249 retro og 0/126 holdout; NO5-holdout uinformativ) var lagt til på slutten av
  RESULTATER-md i commit e74be60. De er flyttet uendret til results/TILLEGG_KHEPRI-TSFM_v1_2026-11-02.md, med arkivnøkkel og en
  linje om at fila ikke er utdata fra analysis.py.
- RESULTATER-md er gjenopprettet fra M3-commit 315e487 (`git checkout 315e487 -- …`; `git checkout --` alene ville gitt e74be60-versjonen).
- sha256 results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.md = 2883d030b1832fa05e815b262490148d91296be652a48a6e7700535470c7a76a,
  identisk med blob-en i 315e487. (STATE hadde ingen sha256 for RESULTATER-md fra M3; verifisert mot M3-commiten og ført her nå.)
- NUMBERS generert på nytt med TILLEGG blant kildene: 208 tall, 0 uten kilde.

## D-11-kontroll, reproduksjon fra CI og tester (ca. 08:45–09:00 UTC)
- Ren venv fra `git archive` (e74be60) under $V/tmp/cleantest: `uv sync --frozen`; `import khepri` → ModuleNotFoundError;
  analysis.py → RESULTATER md og json byte-like med repoet (md sha256 2883d030b1832fa05e815b262490148d91296be652a48a6e7700535470c7a76a).
- repro_from_ci.py (SES pauset, ingen LAS; kjørt serielt): baselines k=361 (alle holdout + 1 retro-origin per sone, 12960 rader per arm)
  maks |Δ| 0.0 for snaive_week, GBM og SARIMA (punkt og 21 kvantiler); tsfm k=361: maks |Δ| 0.0 for Timestral-5M, Timestral-209M, Chronos-2.
- pytest 9.1.1 lagt til som dev-gruppe (uv.lock oppdatert). `pytest -q` i $V/.venv: 27 passed.

## Merge av B, kreditt og arXiv (ca. 08:59–09:05 UTC)
- STATE-B: «manus ferdig 2026-11-02T08:54:21Z». Grenen origin/claude/focused-mayer-kv2xv5 inneholdt bare B-eide filer (MANUS-01–03,
  SOURCES, CLOUDSMOKE, STATE-B) pluss én merge fra main; 0 Co-Authored-By. Merget inn i main (640544d, vanlig merge), pushet.
- CREDITCHECK ettermåling 08:59:26Z: 194 USD igjen (fra 204) → «bekreftet: B trekker kreditt»; uke 51 % (fra 47 %).
- REPRO-frist: 09:54 UTC (1 t etter «manus ferdig»).
- Plist lastet 2026-11-02 ca. 09:00 UTC: ~/Library/LaunchAgents/no.ecodeco.khepri-tsfm.v1.plist, `launchctl bootstrap gui/<uid>`,
  daglig 05:00 lokal tid. Første utstedelse kjørt manuelt 08:30–08:41 UTC: $V/prosp/PROSP_KHEPRI-TSFM_v1_2026-11-02.parquet,
  5184 rader (6 armer × 9 soner × 96 t), sha256 7b0f70333409f33b34043f1d7eb149bc23ad73ed84eefc1144a5a51bb0f3d535, OTS-stempel rc 0.
- arXiv: arxiv/main.tex + arxiv/references.tex + arxiv/build_arxiv.sh (pandoc for MANUS-01–03, MANUS-04 som LaTeX). Kompilert
  med pdflatex: 0 feil, 0 udefinerte referanser, 0 overfull hbox, 14 sider. Zenodo-DOI som makro \zenodoDOI (settes ved publisering).

## REPRO fra B og TILLEGG-punktene (ca. 09:04–09:07 UTC)
- truth/REPRO_KHEPRI-TSFM_v1_2026-11-02.md (B, fra repro-ready 423329f, x86_64 Linux): alle sha256 like; RESULTATER-md 467/467 celler like
  (linje 1 ulik bare fordi utfilnavnet var RESULTATER_B); JSON 67 av 921 blader ulike i siste siffer (maks |Δ| 4,3e-14); pytest 27 passed.
  TSFM-delen ikke kjørt i skyen (huggingface.co ikke nåbar). Merget inn i main (a7e6782; bare B-eide filer, 0 Co-Authored-By).
- Uavhengig TSFM-sjekk (Timestral-5M, Chronos-2, NO4-holdout) startet 09:06 UTC i fersk Opus-subagent fra taggen repro-ready alene
  (SES pauset, ingen LAS); resultat → results/TSFMREPRO_KHEPRI-TSFM_v1_2026-11-02.md.
- D-11 utvidet med diff -r og blob-sha (alle seks like) og arkivnøkkel-avklaringen. D-12 rettet med primærkilder for Chronos-2
  (arXiv 2025-10-17, README 2025-10-20, HF amazon/chronos-2 2025-10-30, autogluon/chronos-2 tom 2025-10-06/modell 2025-11-24).
- «NOTE for A» fjernet etter behandling: `grep -rn "NOTE for A" manus/` → 0. Åpent punkt for publisering: repo-URL i MANUS-01
  legges inn først når utgivelsen er besluttet (repoet er privat).
- Kreditt-ettermåling: allerede gjort 08:59:26Z (194 USD, fall 10 USD).

## Fulltekstpass, TSFM-sjekk og historikk (ca. 09:07–09:14 UTC)
- results/TSFMREPRO_KHEPRI-TSFM_v1_2026-11-02.md: uavhengig TSFM-sjekk fra taggen repro-ready alene (fersk Opus-subagent, ny venv,
  én origin om gangen): NO4-holdout maks |Δ| punkt 7.820e-4 (Timestral-5M) og 3.815e-6 (Chronos-2) g/kWh; største MAPE-endring 1.263e-4 pp.
- MANUS-02 oppgradert fra fulltekst (S20–S26 i SOURCES): CarbonX, Impermanent, EnsembleCI, Leerbeck (arXiv-preprint), Cramer, Clauß lest;
  Hong et al. 2016 bare abstrakt. [NR] fjernet der arbeidet er lest; står igjen for CarbonCast (artikkel), Chronos-2-rapporten, DM, HLN, G&R.
- `git pull --rebase` flatet ut REPRO-mergen (a7e6782 → 4fec392); historikken gjenopprettet med innholdsløs merge 7ba4835 av 2c23d31
  (ingen force). Heretter `git pull --no-rebase`.
- NUMBERS generert over MANUS-01–04, arxiv/main.tex og README: 492 tall, 0 uten kilde (SOURCES inkludert for eksterne tall).
- arXiv bygget på nytt: 0 feil, 0 overfull/udefinert, 14 sider.
