Arkivnøkkel: DECISIONS_KHEPRI-TSFM_v1_2026-11-02

DESIGN v1 (skrives ordrett i DECISIONS; felt merket [steg N] fylles inn fra
kilden før PREREG låses)
- Holdout: post-release, origins fra 2026-10-16 (origin-time som v1.5 [steg 1])
  med origin+96 t <= siste komplette time ved uttak. Retro: v1.5 sin 2025-test,
  merket «kontaminering ikke utelukket».
- Armer: sesongnaiv (uke), SARIMA og GBM med v1.5-koden og -hyperparametrene
  uendret, Timestral-5M og -209M, Chronos-2. Kontekst 8192 t for alle TSFM.
  Felles kontekstslutt for alle armer. Ingen covariates.
- SARIMA/GBM på holdout: v1.5 sin treningsvindu- og refit-regel anvendt med
  test-start 2026-10-16 [steg 1: regelen ordrett med fil:linje]. Krever det
  kodeendring: minste endring som bevarer prosedyren, ført i DEVIATIONS før PREREG.
- Tap per origin og sone = MAPE over de 96 timene (v1.5-definisjonen [steg 1]).
  Test: Diebold–Mariano med Harvey–Leybourne–Newbold-korreksjon på serien av
  sone-gjennomsnittlig tap per origin, h = 4 (overlappende 96 t-horisonter ved
  daglige origins), TSFM mot SARIMA og TSFM mot GBM. Per sone beskrivende.
- Styrke: holdouten har få origins (cirka 13–14 ved uttak tidlig i november).
  MDE beregnes FØR TSFM-kjøring fra variansen i tapsdifferansen SARIMA–GBM på
  2025-testen (publiserte baselines, ingen TSFM), med n = antall holdout-origins,
  h = 4, α = 0,05, styrke 0,8 [steg 4: verdi i MDE-fila]. En holdout-forskjell
  innenfor ±MDE rapporteres som «ikke avgjort», aldri som likhet.
- Rollene: retro-testen (cirka 365 origins) bærer styrken. Holdouten er
  kontamineringskontroll. Kontamineringsindikator = TSFM-fordel på retro minus
  TSFM-fordel på holdout, med HAC-standardfeil, rapportert beskrivende. Klart
  større fordel på retro enn holdout rapporteres som mulig kontaminering.
- RQ4 kalibrering kun på holdout: CRPS fra felles kvantilsett som alle armer
  leverer [steg 2], og dekning for 80 % og 90 %, kun TSFM mot SARIMA.
- Tapte origins etterfylles aldri. Den prospektive loggen analyseres senere med
  samme låste analysis.py, uten fast dato. Utsatt til v2 og skrevet slik i
  PREREG: 32768-kontekst, 28M/123M, covariates.

---
UTFYLTE FELT (fylt fra kilde 2026-11-02, før PREREG; endringer i selve designet går kun via DEVIATIONS)
- [steg 1] origin-time: daglig 00:00 UTC (khepri-v1.5 src/khepri/forecast.py:4-5 og :183-184:
  `pd.date_range(test_start, test_end, freq="1D", tz="UTC")` med `(o + pd.Timedelta(hours=H)) <=
  hist.index.max()`); fasit = timene o+1 t .. o+96 t (forecast.py:153-155). Konteksten for alle
  armer slutter ved timen o (inklusiv), som v1.5 (forecast.py:118-119, :213).
- [steg 1] treningsvindu- og refit-regel ordrett med fil:linje (khepri-v1.5 src/khepri/forecast.py):
  :160 `return list(range(min(train_years), test_end.year + 1))`;
  :189-192 `tr = hist.loc[:train_end]` / `fitted = SARIMAX(tr, order=(2, 0, 1), seasonal_order=(1, 1, 0, 24),
  enforce_stationarity=False, enforce_invertibility=False).fit(disp=False, maxiter=50)`;
  :202 `WIN = pd.Timedelta(days=45)`, :213-214 `w = hist.loc[o - WIN: o]` /
  `preds["SARIMA"] = np.asarray(fitted.apply(w).forecast(H))`;
  :166-168 `last = (train_end - pd.Timedelta(hours=H)).normalize()` /
  `cand = pd.date_range(last - pd.Timedelta(days=n - 1), last, freq="1D", tz="UTC")` /
  `return [o for o in cand if o in hist.index][-n:]` (n = 365); GBM trenes én gang (:197-199).
  Ingen refit gjennom testperioden. Splitter (driver utenfor taggen, eds-revisjon/_skript/j2b_forecast.py:26-29):
  NO train_years [2021, 2022, 2023, 2024], SE [2022, 2023, 2024], train_end 2023-12-31 23:00, test 2025-01-01–2025-12-31.
  Anvendt med test-start 2026-10-16 uten kodeendring: train_end 2025-10-15 23:00, NO 2023–2025, SE 2024–2025
  (DEVIATIONS D-06).
- [steg 1] MAPE-definisjon: forecast.py:132-135, ordrett:
  `mask = np.abs(a) > 1e-6` / `return np.mean(np.abs((a[mask] - f[mask]) / a[mask])) * 100 if mask.any() else np.nan`.
  Tap per origin og sone = denne funksjonen over de 96 timene (lik snittet av v1.5 sine fire dags-MAPE
  når ingen time maskeres).
- [steg 2] felles kvantilsett: 0,01, 0,05, 0,10, 0,15, …, 0,90, 0,95, 0,99 (21 nivåer; native i
  Timestral-5M, Timestral-209M og Chronos-2; SARIMA fra gaussisk prediktiv fordeling, DEVIATIONS D-03).
  80 %-intervall = [q0,10, q0,90], 90 %-intervall = [q0,05, q0,95].
- [steg 4] MDE-verdi: 2,989 pp (n = 14, h = 4), se results/MDE_KHEPRI-TSFM_v1_2026-11-02.md.
