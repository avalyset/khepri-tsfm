Arkivnøkkel: MDE_KHEPRI-TSFM_v1_2026-11-02

Steg 4. Beregnet 2026-11-02 FØR noen TSFM-prediksjon på ekte CI-data (`mde.py`, utdata i
`results/MDE_KHEPRI-TSFM_v1_2026-11-02.json`).

- Kilde: lagrede per-(origin, dag)-MAPE-rader for Khepri v1.5 sin 2025-test som reproduserer
  de publiserte tabellene: SARIMA fra `eds-revisjon/_data/s2-j2b`, GBM fra
  `eds-revisjon/_data/s2-ren/*_std_ren365` (DEVIATIONS D-05). Ingen TSFM.
- Serie: d_t = sone-gjennomsnittlig tap(SARIMA) − tap(GBM) per origin t, tap = MAPE over 96 t
  (= snittet av de fire dags-MAPE), 9 soner, 361 origins (2025-01-01 – 2025-12-27).
  Snitt d = +0,2141 pp (GBM bedre i snitt, samsvarer med de publiserte tabellene).
- Langtidsvarians: rektangulær kjerne, lag 0..h−1, h = 4: σ²_LR = 7,6455 (pp²).
- Formel: MDE = (t_{0,975; n−1} + t_{0,80; n−1}) / HLN(n, h) · √(σ²_LR / n),
  HLN(n, h) = √((n + 1 − 2h + h(h−1)/n) / n); α = 0,05 tosidig, styrke 0,8.
- n = antall holdout-origins = 14 (2026-10-16 – 2026-10-29; siste komplette time ved uttak
  2026-11-02 05:00 UTC).

**MDE (holdout, n = 14, h = 4) = 2,989 pp** sone-gjennomsnittlig MAPE.
Til sammenligning ved n = 361 (retro): 0,413 pp.

Regel: en holdout-forskjell med |snitt-diff| < 2,989 pp rapporteres som «ikke avgjort»,
aldri som likhet.
