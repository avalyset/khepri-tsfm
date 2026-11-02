Arkivnøkkel: TSFMREPRO_KHEPRI-TSFM_v1_2026-11-02

Uavhengig TSFM-sjekk (tillegg til truth/REPRO_KHEPRI-TSFM_v1_2026-11-02.md, der TSFM-delen ikke kunne kjøres i skyen).
Eier: økt A. Utført 2026-11-02 ca. 09:06–09:09 UTC av en fersk Opus-subagent i egne prosesser, etter SES-sjekk
(SES-S1 pauset, ingen LAS). Ikke utdata fra analysis.py.

## Grunnlag
- Bare den GPG-signerte taggen `repro-ready` (tag-objekt 641b2e455d69172f1645865a633ca49c2424b979 → commit
  423329fcda300ba7b52f75ddc95d71787702c991; `git tag -v`: «Good signature from "Eirik Botten Nicolaysen <eirik@ecodeco.no>"»),
  pakket ut med `git archive`, og den lokale Hugging Face-cachen. Ingen filer fra arbeidstreet eller fra $V/.venv.
- Ny venv: `uv sync --frozen --offline --python 3.12` (rc 0; --offline lagt til av subagenten så uv ikke gikk på nett).
  Python 3.12.13, torch 2.15.0, timestral 1.0.0 (git a534bdbd…), chronos-forecasting 2.3.2. `HF_HUB_OFFLINE=1`, `python -I`,
  `torch.set_num_threads(8)`.
- Revisjoner fra PREREG §3.1 (prereg/PREREG_KHEPRI-TSFM_v1_2026-11-02.md:85 og :87): mistralai/Timestral-5M @
  bdd20cfc15a3fea0e4cb5ccef37f8d3ca7aa335f, amazon/chronos-2 @ 29ec3766d36d6f73f0696f85560a422f50e8498c.
- Eget skript (ikke repro_from_ci.py / run_arms.py / khepri_tsfm/models.py): data/CI_…parquet, NO4, holdout; 14 origins
  2026-10-16 – 2026-10-29; kontekst = 8192 timer til og med origin-timen; én origin om gangen (ingen batch), én modell per prosess.

## Resultat (NO4-holdout, 14 origins × 96 timer; kvantiler = alle 21 nivåer)

| | Timestral-5M | Chronos-2 |
|---|---|---|
| maks \|Δ\| punkt (g/kWh) | 7.820e-4 | 3.815e-6 |
| snitt \|Δ\| punkt (g/kWh) | 1.898e-5 | 3.605e-7 |
| maks \|Δ\| kvantiler (g/kWh) | 3.456e-3 | 4.959e-5 |
| snitt \|Δ\| kvantiler (g/kWh) | 2.356e-5 | 1.921e-6 |
| største MAPE-endring per origin (pp) | +1.263e-4 (origin 2026-10-22) | +1.250e-6 (origin 2026-10-17) |

- For Timestral-5M er origin 2026-10-22 omtrent to størrelsesordener større enn de andre (punkt 3.8e-6 – 2.7e-5 på de 13 andre).
  Kjøringen her er én origin om gangen med float64-inndata; step 7 kjørte ni soner i én batch (float32). Avvikene er på
  flyttallsnivå og endrer ingen tabellcelle i RESULTATER (3 desimaler).
- `point` = `q0.50` i PRED-filene for alle origins; nivåene er de samme 21 som kolonnene.
- Toppminne: 575 MB (Timestral-5M), 1187 MB (Chronos-2).

## Filer ($V/tmp/tsfmrepro/, ikke i repoet; sha256 i SHA256SUMS.txt, kontrollert med `shasum -c`: alle OK)
- indep_repro.py f1111ec402138d7483c8b2edac6e32469328bc1faa77d5d4c952bec2aace15a9
- summary_timestral5m.json 48ce91167e12e879567a3a631835d5365285da6b45b571fc25cfafca3f9322be
- summary_chronos2.json e62e3c8dca186ade4bbdf66187e009e71f8ea18758f697731327ca36b5505d0a
- per_origin_timestral5m.csv 712feabc31204b3e457afbc93fbb00d1a67a7b03f24927de260382eca9e567c9
- per_origin_chronos2.csv 89596349e8bd9cec134042ffe8ae1de077b6fecccd8b284d4368f6f99839c705
