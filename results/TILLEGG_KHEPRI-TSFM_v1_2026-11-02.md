Arkivnøkkel: TILLEGG_KHEPRI-TSFM_v1_2026-11-02

Denne fila er IKKE utdata fra analysis.py. Den holder to håndførte tillegg til RESULTATER_KHEPRI-TSFM_v1_2026-11-02.md, flyttet uendret hit 2026-11-02 slik at RESULTATER er byte-lik utdata fra analysis.py (M3, commit 315e487).

## Tillegg (ikke fra analysis.py): SARIMA-fallbacks

Telt fra kolonnen `fallback` i PRED-SARIMA_KHEPRI-TSFM_v1_2026-11-02.parquet (v1.5-regelen: diurnal persistens ved feil i apply()/forecast()).

- retro: 0 fallback-origins av 3249 (sone × origin)
- holdout: 0 fallback-origins av 126 (sone × origin)

## Tillegg: NO5-holdouten er uinformativ

Khepri v1.5-CI for NO5 er konstant 24,0 g/kWh i hele holdout-vinduet (data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet), så holdout-MAPE for NO5 er 0,000 for alle armer unntatt GBM (0,047). NO5 inngår i sone-snittet etter PREREG, men gir ingen informasjon om rangering på holdout.
