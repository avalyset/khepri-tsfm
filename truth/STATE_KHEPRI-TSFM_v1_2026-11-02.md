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
| M1 | 1 kilder, 2 latens, 3 data | FERDIG (denne commit) | 2026-11-02 |
| M2 | 4 MDE, PREREG, OSF | PREREG låst (tagg prereg-v1); OSF-registrering pågår | 2026-11-02 |
| M3 | 7 kjøring, 8 analyse | ikke startet | |
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
