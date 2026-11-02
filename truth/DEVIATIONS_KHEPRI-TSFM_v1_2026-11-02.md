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
