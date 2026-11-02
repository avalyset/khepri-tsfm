Arkivnøkkel: RESULTATER_KHEPRI-TSFM_v1_2026-11-02

Generert av analysis.py (låst i PREREG). Tap = Khepri v1.5 MAPE over 96 t per origin og sone; testserie = sone-gjennomsnittlig tap per origin; DM med HLN-korreksjon, h = 4, t(n-1). Negativ differanse = TSFM har lavere tap.

MDE (holdout, n = 14): 2.989 pp. En holdout-forskjell innenfor ±MDE rapporteres som «ikke avgjort», aldri som likhet.

## DM-tester, retro

| TSFM | mot | n | snitt-tap TSFM | snitt-tap base | diff pp | HLN-stat | p | p (Holm) | vurdering |
|---|---|---|---|---|---|---|---|---|---|
| Timestral-5M | SARIMA | 361 | 6.253 | 7.561 | -1.308 | -13.30 | 0.0000 | 0.0000 |  |
| Timestral-5M | GBM | 361 | 6.253 | 7.347 | -1.094 | -9.86 | 0.0000 | 0.0000 |  |
| Timestral-209M | SARIMA | 361 | 6.213 | 7.561 | -1.347 | -12.77 | 0.0000 | 0.0000 |  |
| Timestral-209M | GBM | 361 | 6.213 | 7.347 | -1.134 | -9.97 | 0.0000 | 0.0000 |  |
| Chronos-2 | SARIMA | 361 | 6.395 | 7.561 | -1.166 | -12.65 | 0.0000 | 0.0000 |  |
| Chronos-2 | GBM | 361 | 6.395 | 7.347 | -0.952 | -7.79 | 0.0000 | 0.0000 |  |

### Per sone, retro (beskrivende, snitt MAPE %)

| sone | snaive_week | SARIMA | GBM | Timestral-5M | Timestral-209M | Chronos-2 |
|---|---|---|---|---|---|---|
| NO1 | 2.969 | 2.460 | 2.307 | 2.108 | 2.120 | 2.131 |
| NO2 | 4.194 | 3.964 | 3.423 | 3.151 | 3.111 | 3.182 |
| NO3 | 8.139 | 6.874 | 6.583 | 5.868 | 5.773 | 5.910 |
| NO4 | 10.104 | 7.242 | 10.158 | 6.171 | 6.133 | 6.339 |
| NO5 | 1.029 | 0.722 | 1.256 | 0.605 | 0.593 | 0.629 |
| SE1 | 14.322 | 11.638 | 10.758 | 10.096 | 10.031 | 10.266 |
| SE2 | 13.293 | 10.416 | 9.568 | 8.920 | 8.965 | 9.028 |
| SE3 | 5.445 | 4.543 | 4.526 | 3.860 | 3.753 | 3.896 |
| SE4 | 22.605 | 20.187 | 17.545 | 15.495 | 15.441 | 16.174 |

## DM-tester, holdout

| TSFM | mot | n | snitt-tap TSFM | snitt-tap base | diff pp | HLN-stat | p | p (Holm) | vurdering |
|---|---|---|---|---|---|---|---|---|---|
| Timestral-5M | SARIMA | 14 | 8.415 | 9.332 | -0.917 | -1.98 | 0.0693 | 0.1385 | ikke avgjort (innenfor ±MDE) |
| Timestral-5M | GBM | 14 | 8.415 | 9.223 | -0.808 | -5.00 | 0.0002 | 0.0012 | ikke avgjort (innenfor ±MDE) |
| Timestral-209M | SARIMA | 14 | 8.005 | 9.332 | -1.326 | -3.79 | 0.0023 | 0.0068 | ikke avgjort (innenfor ±MDE) |
| Timestral-209M | GBM | 14 | 8.005 | 9.223 | -1.218 | -17.97 | 0.0000 | 0.0000 | ikke avgjort (innenfor ±MDE) |
| Chronos-2 | SARIMA | 14 | 8.494 | 9.332 | -0.838 | -1.89 | 0.0810 | 0.1385 | ikke avgjort (innenfor ±MDE) |
| Chronos-2 | GBM | 14 | 8.494 | 9.223 | -0.729 | -4.95 | 0.0003 | 0.0012 | ikke avgjort (innenfor ±MDE) |

### Per sone, holdout (beskrivende, snitt MAPE %)

| sone | snaive_week | SARIMA | GBM | Timestral-5M | Timestral-209M | Chronos-2 |
|---|---|---|---|---|---|---|
| NO1 | 3.983 | 3.108 | 2.437 | 2.442 | 2.430 | 2.396 |
| NO2 | 2.666 | 3.902 | 4.129 | 3.122 | 3.274 | 3.298 |
| NO3 | 12.053 | 9.343 | 7.820 | 8.022 | 7.737 | 8.294 |
| NO4 | 11.664 | 7.480 | 9.288 | 6.984 | 6.998 | 7.314 |
| NO5 | 0.000 | 0.000 | 0.047 | 0.000 | 0.000 | 0.000 |
| SE1 | 28.189 | 20.420 | 19.699 | 20.001 | 18.193 | 19.260 |
| SE2 | 17.065 | 14.956 | 13.705 | 13.875 | 13.679 | 13.652 |
| SE3 | 7.342 | 6.395 | 5.918 | 5.262 | 5.014 | 5.544 |
| SE4 | 22.457 | 18.381 | 19.962 | 16.024 | 14.722 | 16.686 |

## Sensitivitet S1: seks soner uten utfylte timer (NO1, NO4, SE1, SE2, SE3, SE4)

Beskrivende; MDE-regelen gjelder bare primæranalysen.

| splitt | TSFM | mot | n | diff pp | HLN-stat | p |
|---|---|---|---|---|---|---|
| retro | Timestral-5M | SARIMA | 361 | -1.639 | -11.99 | 0.0000 |
| retro | Timestral-5M | GBM | 361 | -1.369 | -8.48 | 0.0000 |
| retro | Timestral-209M | SARIMA | 361 | -1.674 | -11.13 | 0.0000 |
| retro | Timestral-209M | GBM | 361 | -1.403 | -8.45 | 0.0000 |
| retro | Chronos-2 | SARIMA | 361 | -1.442 | -11.35 | 0.0000 |
| retro | Chronos-2 | GBM | 361 | -1.171 | -6.72 | 0.0000 |
| holdout | Timestral-5M | SARIMA | 14 | -1.025 | -1.51 | 0.1544 |
| holdout | Timestral-5M | GBM | 14 | -1.070 | -5.53 | 0.0001 |
| holdout | Timestral-209M | SARIMA | 14 | -1.617 | -3.04 | 0.0095 |
| holdout | Timestral-209M | GBM | 14 | -1.662 | -8.33 | 0.0000 |
| holdout | Chronos-2 | SARIMA | 14 | -0.981 | -9.72 | 0.0000 |
| holdout | Chronos-2 | GBM | 14 | -1.026 | -4.66 | 0.0004 |

## H1 og H2 (retro)

- Timestral-5M: slår SARIMA i 9 av 9 soner (H1 støttet); minst fordel i pp: NO5 (H2 støttet); minst relativ fordel: SE1.
- Timestral-209M: slår SARIMA i 9 av 9 soner (H1 støttet); minst fordel i pp: NO5 (H2 støttet); minst relativ fordel: SE1.
- Chronos-2: slår SARIMA i 9 av 9 soner (H1 støttet); minst fordel i pp: NO5 (H2 støttet); minst relativ fordel: SE1.

## RQ3: NO4 og NO5 (retro og holdout, beskrivende)

- retro NO4: snaive_week 10.104, SARIMA 7.242, GBM 10.158, Timestral-5M 6.171, Timestral-209M 6.133, Chronos-2 6.339
- retro NO5: snaive_week 1.029, SARIMA 0.722, GBM 1.256, Timestral-5M 0.605, Timestral-209M 0.593, Chronos-2 0.629
- holdout NO4: snaive_week 11.664, SARIMA 7.480, GBM 9.288, Timestral-5M 6.984, Timestral-209M 6.998, Chronos-2 7.314
- holdout NO5: snaive_week 0.000, SARIMA 0.000, GBM 0.047, Timestral-5M 0.000, Timestral-209M 0.000, Chronos-2 0.000

## RQ4: kalibrering (holdout, TSFM mot SARIMA)

| arm | CRPS (g/kWh) | dekning 80 % | dekning 90 % |
|---|---|---|---|
| Chronos-2 | 1.1198 | 0.806 | 0.905 |
| SARIMA | 1.4165 | 0.835 | 0.911 |
| Timestral-209M | 1.0733 | 0.838 | 0.921 |
| Timestral-5M | 1.1114 | 0.838 | 0.915 |

| TSFM | n | CRPS-diff mot SARIMA | HLN-stat | p |
|---|---|---|---|---|
| Timestral-5M | 14 | -0.3052 | -11.75 | 0.0000 |
| Timestral-209M | 14 | -0.3432 | -11.23 | 0.0000 |
| Chronos-2 | 14 | -0.2967 | -8.52 | 0.0000 |

## RQ5: kontamineringsindikator (beskrivende)

Fordel = tap(base) − tap(TSFM). Indikator = fordel retro − fordel holdout; HAC-SE (lag 0..3) kombinert som uavhengige perioder. z > 1,96 rapporteres som «mulig kontaminering».

| TSFM | mot | fordel retro | fordel holdout | indikator | HAC-SE | z | mulig kontaminering |
|---|---|---|---|---|---|---|---|
| Timestral-5M | SARIMA | 1.308 | 0.917 | 0.391 | 0.360 | 1.09 | nei |
| Timestral-5M | GBM | 1.094 | 0.808 | 0.286 | 0.164 | 1.75 | nei |
| Timestral-209M | SARIMA | 1.347 | 1.326 | 0.021 | 0.282 | 0.07 | nei |
| Timestral-209M | GBM | 1.134 | 1.218 | -0.084 | 0.124 | -0.68 | nei |
| Chronos-2 | SARIMA | 1.166 | 0.838 | 0.328 | 0.344 | 0.95 | nei |
| Chronos-2 | GBM | 0.952 | 0.729 | 0.223 | 0.164 | 1.36 | nei |

## Antall origins per arm

- retro: Chronos-2 361, GBM 361, SARIMA 361, Timestral-209M 361, Timestral-5M 361, snaive_week 361
- holdout: Chronos-2 14, GBM 14, SARIMA 14, Timestral-209M 14, Timestral-5M 14, snaive_week 14

## Tillegg (ikke fra analysis.py): SARIMA-fallbacks

Telt fra kolonnen `fallback` i PRED-SARIMA_KHEPRI-TSFM_v1_2026-11-02.parquet (v1.5-regelen: diurnal persistens ved feil i apply()/forecast()).

- retro: 0 fallback-origins av 3249 (sone × origin)
- holdout: 0 fallback-origins av 126 (sone × origin)

## Tillegg: NO5-holdouten er uinformativ

Khepri v1.5-CI for NO5 er konstant 24,0 g/kWh i hele holdout-vinduet (data/CI_KHEPRI-TSFM_v1_2026-11-02.parquet), så holdout-MAPE for NO5 er 0,000 for alle armer unntatt GBM (0,047). NO5 inngår i sone-snittet etter PREREG, men gir ingen informasjon om rangering på holdout.
