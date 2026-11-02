Arkivnøkkel: LATENS_KHEPRI-TSFM_v1_2026-11-02

Steg 2. Målt 2026-11-02 på Eiriks Mac (Apple M1, 16 GB, CPU, torch.set_num_threads(8)), venv $V/.venv (uv.lock).
Skript: latency.py (syntetisk random walk, seed 20261102, lengde 8192, 1 oppvarming + 10 tidsmålte kall; hver arm i egen prosess, topp-RSS = ru_maxrss).
SARIMA: én tilpasning med v1.5-koden (order (2,0,1)(1,1,0,24), NO1, train 2021-01-01..2023-12-31 23:00) og 5 × apply()+get_forecast(96) på origin 2025-03-01. Ekte publisert baseline-serie, ingen TSFM.

| Arm | lasting s | 1 serie median s | 1 serie maks s | batch 9 median s | batch 9 maks s | topp-RSS MB |
|---|---|---|---|---|---|---|
| Timestral-5M | 0.59 | 0.047 | 0.048 | 0.143 | 0.147 | 334 |
| Timestral-209M | 3.09 | 0.361 | 0.404 | 1.800 | 1.961 | 1800 |
| Chronos-2 | 8.59 | 0.152 | 0.163 | 0.922 | 0.938 | 1352 |

| SARIMA (v1.5-kode) | verdi |
|---|---|
| tilpasning, NO1 26 280 timer | 17,8 s |
| apply + get_forecast(96) per origin, median | 0,073 s |
| apply + get_forecast(96) per origin, maks | 0,177 s |
| topp-RSS | 3086 MB |

## Kvantiler
Timestral-5M, Timestral-209M og Chronos-2 leverer alle de samme 21 nivåene: 0.01, 0.05, 0.10, …, 0.95, 0.99 (målt fra model.config.quantile_knots / pipeline.quantiles).
Felles sett (DECISIONS [steg 2]) = alle 21. SARIMA leverer dem fra den gaussiske prediktive fordelingen (get_forecast: predicted_mean + z_q · se_mean); punktprognosen er identisk med v1.5 sin forecast(H).

## Anslag steg 7 (9 soner, 361 retro- + ~14 holdout-origins)
- SARIMA: 18 tilpasninger × ~18 s + 9 × 375 × ~0,07 s ≈ 10 min.
- GBM: 18 treninger (3 frø × 365 origins × 96 rader) + prediksjon, anslått < 15 min (ikke målt her).
- TSFM, batch over 9 soner per origin: 375 × (0,14 + 1,80 + 0,92) s ≈ 18 min.
- Totalt anslag steg 7: < 1 t. Under 6 t-grensen; steg 7 går.
