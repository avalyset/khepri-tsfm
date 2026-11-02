Arkivnøkkel: DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02

Alle avvik fra DECISIONS (DESIGN v1) og fra PREREG. Hvert avvik: ID, UTC-tid,
før/etter PREREG, hva, hvorfor, konsekvens, sha256 + OTS-stempel av fila etter føring.

## Før PREREG (ført 2026-11-02, før noen TSFM-prediksjon på ekte CI-data)

### D-01 Prediksjonsfangende driver (ingen endring i forecast.py)
- Hva: `khepri.forecast.eval_split` returnerer bare metrikkrader (forecast.py:227-232), ikke
  timesprediksjoner. `khepri_tsfm/baselines.py` og `run_arms.py` gjentar løkka i
  forecast.py:178-222 linje for linje og kaller de samme v1.5-funksjonene (`hourly_ci`,
  `gbm_train_origins`, `build_gbm`, `fc_gbm`, `actual_window`, `fc_diurnal`, SARIMAX med samme
  orden og argumenter), men tar vare på prediksjonene. forecast.py er uendret.
- Validering før PREREG (publiserte baselines, ingen TSFM), `validate_baselines.py`:
  SE1 retro: SARIMA maks |Δ| 0,00036 pp per (origin, dag) mot v1.5-kjøringen
  `eds-revisjon/_data/s3-v15` (snitt 11,6383 mot 11,6384), GBM maks |Δ| 3,6e-15.
  NO1 retro: GBM maks |Δ| 4,4e-16 mot `s2-ren/..._std_ren365` (snitt 2,3070 begge).

### D-02 NO1-SARIMA-tilpasningen reproduseres ikke bit for bit
- Hva: i dag konvergerer NO1-tilpasningen (train 2021-01-01–2023-12-31 23:00) etter 1 L-BFGS-
  iterasjon (ar.L1 1,4090, ar.L2 −0,4556, ma.L1 −0,1349, ar.S.L24 −0,3856, sigma2 0,02053);
  v1.5-kjøringen 2026-10-01 (`s2-j2b/NO1_primaer_2025_meta.json`) brukte 22 iterasjoner
  (1,4244 / −0,4639 / −0,1550 / −0,4941 / 0,01553).
- Utelukket: rådata (mtime 2026-06-29, før kjøringen), kode (ci.py og factors.py identiske
  v1.4/v1.5; serien har samme lengde 43 824 og sum 616 414,178 med v1.4- og v1.5-koden),
  bibliotek (numpy 2.4.2, scipy 1.17.1, statsmodels 0.14.6; systemets python 3.14, som
  reproduserte v1.5, gir også 1 iterasjon), BLAS-trådantall (1 og 4 gir samme). Årsak ikke funnet.
- Konsekvens: NO1 retro SARIMA snitt-MAPE 2,4596 mot publisert 2,4656 (−0,006 pp); maks
  |Δ| 0,58 pp per (origin, dag). SE1 reproduseres (D-01).
- Håndtering: SARIMA-armen kjøres i det pinnede miljøet (uv.lock) med v1.5-koden uendret.
  RESULTATER får en reproduksjonstabell per sone (vår SARIMA/GBM mot lagrede v1.5-rader).
  MDE beregnes fra de lagrede publiserte radene (D-05).
- Miljø: scipy pinnet til 1.17.1 og scikit-learn til 1.9.0 (versjonene i miljøet som
  reproduserte v1.5; lightgbm.sklearn krever scikit-learn); python 3.12 (v1.5-CI: 3.11/3.12).

### D-03 SARIMA-kvantiler
- v1.5 lagrer ingen kvantiler (forecast.py:214 bruker `.forecast(H)`). For RQ4 hentes de 21
  felles kvantilene fra samme tilpassede modell: `apply(w).get_forecast(H)`, gaussisk
  predicted_mean + z_q · se_mean. Punktprognosen er uendret (assert mot `.forecast(H)`).

### D-04 Sesongnaiv (uke) er en ny arm
- v1.5 har bare flat og diurnal (24 t) persistens (forecast.py:77-87). Sesongnaiv uke:
  f(o+h) = y(o+h−168 t), h = 1..96, implementert i `khepri_tsfm/baselines.py`.

### D-05 MDE fra lagrede per-origin-metrikker, ikke prediksjoner
- Per-origin-prediksjoner for 2025 finnes ikke på disk (steg 1). Lagrede per-(origin, dag)-
  MAPE-rader som reproduserer de publiserte tabellene (±0,005) finnes for alle ni soner:
  SARIMA `eds-revisjon/_data/s2-j2b/{sone}_{primaer_2025|se_2025}_rows.csv`, GBM
  `eds-revisjon/_data/s2-ren/{sone}_..._std_ren365_rows.csv`. Tap per origin = snitt av de
  fire dags-MAPE = MAPE over 96 t (ingen maskerte timer). Dette er nøyaktig tapsdifferansen
  SARIMA–GBM som DESIGN ber om; rekjøring av GBM og naiv (promptens reserve) trengs ikke.
- RQ2 tar med SARIMA: rekjøring av SARIMA på 2025 er anslått til ~10 min (LATENS), godt
  innenfor 6 t-budsjettet.

### D-06 Treningsregelen på holdout (tolkning, bare parametre)
- v1.5-regelen (data.py `holdout_split`): train_end = test-start − 1 år − 1 t (som
  2023-12-31 23:00 → test 2025-01-01) = 2025-10-15 23:00; treningsårene er v1.5-årene
  forskjøvet med train_end-året (2023 → 2025): NO 2023–2025, SE 2024–2025. SARIMA tilpasses
  på `hist.loc[:train_end]` fra 1. januar første treningsår; GBM på de 365 siste daglige
  origins med mål ≤ train_end (2024-10-12 – 2025-10-11). Ingen kodeendring.
- Konsekvens: SARIMA-treningsspennet blir 2,79 år (NO) og 1,79 år (SE) mot 3,0 og 2,0 år i
  v1.5, fordi `hourly_ci` leser hele kalenderår. Å bevare spennet eksakt ville kreve
  kodeendring i forecast.py; det er valgt bort.

### D-07 Pumpetime-utfylling i holdout-vinduet; forhåndsregistrert sensitivitet S1
- Funn ved datauttaket (før TSFM): andel timer der Khepri-v1.5-CI er NaN før utfylling
  (pumpetimer, ADR-0002), med lengste sammenhengende hull:
  holdout 2026-10-16 – 2026-11-02 04:00: NO2 0,545 (111 t), NO3 0,416 (45 t), NO5 0,167 (58 t);
  retro 2025: NO2 0,095 (104 t), NO3 0,047 (107 t), NO5 0,048 (67 t);
  NO1, NO4, SE1–SE4: 0 i begge vinduer.
- Primæranalysen er uendret: datafellene håndteres nøyaktig som i v1.5
  (`interpolate(limit=6).ffill().bfill()`, forecast.py:72), også for fasiten.
- Tillegg (før PREREG): sensitivitet S1 = de samme DM-HLN-testene på sone-gjennomsnitt over
  de seks sonene uten utfylte timer (NO1, NO4, SE1–SE4), rapportert beskrivende.
  Utvalget er låst fra CI-dataene over, før noen TSFM-prediksjon.

### D-08 Reproduksjonstabell
- RESULTATER får en tabell per sone: retro-snitt-MAPE for vår SARIMA og GBM mot de
  publiserte v1.5-tallene (docs/forecast-results.md:46-54, docs/se-forecast-results.md:41-48),
  laget av `repro_v15.py`. Den er beskrivende og påvirker ingen test.

## Etter tagg prereg-v1, før OSF-innsending og før noen TSFM-prediksjon på ekte CI

### D-09 Feilretting i issue.py (prospektiv logg), ikke analyse eller armer
- 2026-11-02 ca. 07:45 UTC. Tørrtest av `issue.build_raw` (bare A75-delta og skjøting, ingen
  prognoser) viste at skjøtet 2026-fil ble sortert som tekst med blandet UTC-offset
  (+01:00/+02:00), altså ikke kronologisk. Rettet: sortering på tolket UTC-tid
  (`np.argsort`, stabil). Etter rettingen: NO2 29 308 rader, SE4 29 307, monotont stigende,
  0 duplikater. `analysis.py`, `khepri_tsfm/*`, `run_arms.py` og `prosp_arms.py` er uendret
  siden prereg-v1.

## Etter OSF-innsending (osf.io/hncz5, 07:49 UTC)

### D-10 SES-vakt i issue.py (felles maskinregel fra Eirik, 2026-11-02 ca. 07:52 UTC)
- `issue.py` leser (bare leser) /Volumes/Vault/sjel-eller-speil/kjoring/STATUS_SES.txt (siste linjer)
  og LAS før utstedelsen. Går SES-S1, eller peker LAS på en levende prosess, hoppes dagens
  utstedelse over og logges som «tapt: SES aktiv»; aldri etterfylling. Testet mot ekte status
  (ledig), tre testmapper (går / pause / levende LAS) og hele `main()` (logger tapt, rører
  ingen lås eller henting). Ingen endring i analyse eller armer. Steg 7: SES sjekkes manuelt
  før hver tung kjøring; den køsatte TSFM-jobben (pid 4343, bare ventende på run.lock) ble
  avsluttet før den startet, og startes etter ny SES-sjekk.

### D-11 Khepri v1.5 vendret som khepri_v15/ (pakking, ingen endring i analyse eller tall)
- 2026-11-02 ca. 08:45 UTC, før tagg repro-ready. Varslet av økt B (STATE-B 08:39:02Z): `analysis.py:21`
  (`from khepri import forecast as fc`) krevde Khepri v1.5, som verken lå i pyproject.toml eller uv.lock; lokalt ble den
  lagt på stien med en .pth-fil i $V/.venv. Taggen var dermed ikke selvstendig (ModuleNotFoundError etter `uv sync --frozen`).
- Taggen v1.5 (9e2214f) har ingen pakkedefinisjon (verken pyproject.toml eller setup.py; bare requirements.txt og src/),
  så en git-avhengighet kan ikke installeres. Derfor er `src/khepri/` vendret ordrett som `khepri_v15/` (6 filer, byte-like
  med `git show v1.5:src/khepri/<fil>`, kontrollert med cmp), med LICENSE (Apache-2.0) og VENDORED.md.
- Endret: bare importlinjene `from khepri import forecast as fc` → `from khepri_v15 import forecast as fc` i analysis.py,
  repro_v15.py, khepri_tsfm/data.py, khepri_tsfm/baselines.py, run_arms.py (2), prosp_arms.py, latency.py,
  validate_baselines.py, repro_from_ci.py. .pth-fila i $V/.venv er fjernet.
- Kontroll: ren venv fra `git archive` (uv sync --frozen) kjører analysis.py; resultatet sammenlignes byte for byte med
  results/ (se STATE).
- Kontroll 2026-11-02 ca. 09:06 UTC (A): `diff -r -x VENDORED.md -x LICENSE -x __pycache__ khepri_v15 $V/khepri-v1.5/src/khepri`
  gir ingen forskjell. Blob-sha (`git hash-object`) mot `git -C ~/khepri ls-tree -r v1.5 src/khepri/`: alle seks like —
  __init__.py c3150f10bbf080f05054646d0c169b8593f59ff1, ci.py f1ebe0500af5d0629d1f271f198721e45a509d41,
  codecarbon_map.py a90ac7557a58c7d53dd0fbf13a028b654e1381ef, drift.py 19604aa701f89ec41f552172c754ac47b021de02,
  factors.py ff2d252fe16a562e08d7cdde6516d59683c1083d, forecast.py fa8eb2aae2b948af20c9d6862840d02239bca09e.
  khepri_v15/LICENSE er byte-lik med v1.5 sin LICENSE. Ingen avvik utover importlinjene i Khepri-TSFM sine egne filer.
- Arkivnøkkel-linja i RESULTATER-md skrives av analysis.py selv (`analysis.py:200`, fra utfilnavnet). Med samme utfilnavn er
  md byte-lik (A: full `cmp` i ren venv, sha256 2883d030…a76a). B kjørte med utfilnavnet «RESULTATER_B» og fikk derfor bare
  linje 1 ulik (truth/REPRO_KHEPRI-TSFM_v1_2026-11-02.md). Ingen endring i analysis.py.

### D-12 Ordlyd i PREREG om treningsgrenser (ingen endring i analyse eller tall)
- Meldt av økt B (STATE-B 08:48:15Z). PREREG §1.1 RQ2 (prereg/PREREG_KHEPRI-TSFM_v1_2026-11-02.md:21-22) sier
  «the 2025 data predate the TSFMs' training cut-offs». Det stemmer ikke nødvendigvis for hele vinduet for Chronos-2, som ble
  offentlig i oktober–november 2025. For Timestral er treningsdata og cut-off ikke oppgitt.
- Slippdatoen for Chronos-2 fra primærkilder (lest 2026-11-02 ca. 09:05 UTC av A; råsvar i $V/tmp/chronos2-dato/ med sha256):
  - arXiv:2510.15821v1 (teknisk rapport), published 2025-10-17T17:00:53Z — http://export.arxiv.org/api/query?id_list=2510.15821
    (arxiv_2510.15821.xml, sha256 473dbd7972b0cf9d6a18ea4746944fa74c9559f6ec5f24eff363a520ae953c94).
  - github.com/amazon-science/chronos-forecasting README.md:20: «20 Oct 2025: … Chronos-2 released» (kunngjøring;
    chronos_forecasting_README.md, sha256 7f9e55723daadb20f79f3d76d23370888301d917f075e9eafa3e780c78f9ff35).
  - https://huggingface.co/api/models/amazon/chronos-2/commits/main: «initial commit» 2025-10-30T14:54:39Z (createdAt samme;
    hf_commits.json sha256 8b250d266e0ab1fa909706b1d3dfc32f9d963d810a541c2984880d7476149ec8).
  - https://huggingface.co/api/models/autogluon/chronos-2/commits/main: «initial commit» 2025-10-06T18:52:51Z, «Add model»
    2025-11-24T21:38:47Z (hf_autogluon_commits.json sha256 e532e19c8aa5cbb028b694942a1e39e8c01158ab6e92ac3e6b86b867b58704de).
  - Første føring av D-12 (ca. 09:02 UTC) brukte bare 2025-10-20; rettet her til intervallet over. Kildene binder ikke slippet
    til én dag; tidligste spor er 2025-10-06 (tomt repo), tidligste innhold 2025-10-17 (rapporten).
- Følge: retro-origins 2025-01-01 – 2025-10-05 (278 av 361) ligger før ethvert spor av Chronos-2 offentlig; senere origins kan
  ligge etter slippet. PREREG og OSF-teksten er låst og endres ikke. Manus bruker «most 2025 origins precede the public release of
  Chronos-2 in October 2025». Merkelappen «contamination not ruled out» og alle analyser er uendret.
