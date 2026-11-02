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
UTFYLTE FELT (fylles fra kilde; endringer i selve designet går kun via DEVIATIONS)
- [steg 1] origin-time: (fylles)
- [steg 1] treningsvindu- og refit-regel ordrett med fil:linje: (fylles)
- [steg 1] MAPE-definisjon: (fylles)
- [steg 2] felles kvantilsett: (fylles)
- [steg 4] MDE-verdi: se MDE-fila
