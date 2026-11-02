Arkivnøkkel: REPRO_KHEPRI-TSFM_v1_2026-11-02

Eier: økt B (sky, x86_64 Linux, Python 3.12.3). Uavhengig reproduksjon fra taggen repro-ready. Rapporterer, retter ikke.

## Grunnlag
- Tagg repro-ready → commit 423329fcda300ba7b52f75ddc95d71787702c991 (tagget 2026-11-02 08:58:37 UTC, GPG-signert; signaturen
  ikke verifisert i sky-økta, ingen nøkkel). Funnet av taggvakten 08:59:16 UTC. Sjekket ut som egen worktree; bare innholdet i taggen brukt.
- `uv sync --frozen` mot taggens uv.lock: OK 08:59:51–08:59:52 UTC.
- Glob: analysis.py (1 treff); predictions/PRED-*_KHEPRI-TSFM_v1_*.parquet (6 treff, ett per arm);
  results/PRED-*_KHEPRI-TSFM_v1_*.parquet (0 treff; prediksjonene ligger i predictions/); data/CI_KHEPRI-TSFM_v1_*.parquet (1 treff).

## sha256-kontroll (mot STATE og manifestet i taggen)
| Fil | sha256 | Mot | Utfall |
|---|---|---|---|
| PRED-Chronos-2 | b643e82093061d324d1b1565a0154c33f9455e10f9ef1ff79b3937dd58d821d3 | predictions/PRED_KHEPRI-TSFM_v1_2026-11-02.sha256 | lik |
| PRED-GBM | 176de684adda5553c049ce63b4e3c597252dc05a362d97d7f2c799964a0f7343 | samme | lik |
| PRED-SARIMA | 0723656c5c4ce047612a8240becee9d59565db98bcee6763ec6871bc8a760d0e | samme | lik |
| PRED-Timestral-209M | 0f48d616284e9248b4626b19d6fa8f302169a57de193b228ec2469a2b17deb5d | samme | lik |
| PRED-Timestral-5M | cfa2d315c7b9ca2c1df9911edd7f6a514c2f04c0be691fa8edda4c870bb89456 | samme | lik |
| PRED-snaive_week | 5cbfa2d01689d979fbf05c626c96bc6740b0e3e88bb8c73b4ccbae290909caf1 | samme | lik |
| data/CI_…parquet | ab308ae9f49fb9a4229d3ef089bb8b005fd149101a1e9596c9295c3e5cfa95f0 | STATE (Steg 3), data/CI_….sha256 | lik |
| data/CI_…meta.json | 97f1cf6d7c640968ec800ebefb578680bdcdf44a8269dea6bdb6f0638a5f7929 | STATE (Steg 3), data/CI_….sha256 | lik |
| results/RESULTATER_…md (As) | 2883d030b1832fa05e815b262490148d91296be652a48a6e7700535470c7a76a | STATE (RESULTATER byte-lik) | lik |
Ingen avvik, så reproduksjonen ble kjørt.

## Kjøring
- `uv run --frozen python analysis.py predictions results/MDE_KHEPRI-TSFM_v1_2026-11-02.json <scratch>/RESULTATER_B`,
  analysis.py uendret (fra taggen), 2026-11-02 ca. 09:00 UTC, rc 0, 16 s.
- Utdata (bare i Bs scratch, ikke i repoet): RESULTATER_B.md sha256 68fc6b63a22e20ce8061839897b8410445e3711cb491b78bc89437a890ac7819,
  RESULTATER_B.json sha256 7be6f1fc56001a4b44670e16916c0b875efcfac82cbcc3724f70b107d06af934.

## Sammenligning med results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.{md,json}
- **Markdown, alle tabeller celle for celle: 467 celler, 467 like, 0 avvik.** Hele md-fila er identisk bortsett fra linje 1
  (arkivnøkkelen, som analysis.py lager fra utfilnavnet: «RESULTATER_B» mot «RESULTATER_KHEPRI-TSFM_v1_2026-11-02»).
  Derfor ulik sha256 for md. Med samme utfilnavn ville md vært byte-lik.
- **JSON, full presisjon: 921 blader, 854 like, 67 avvik, alle i siste flyttallssiffer.** Maks |Δ| 4,3e-14
  (dm/holdout[3].dm_hln), maks relativ |Δ| 3,0e-14. Fordeling: dm/retro 12, dm/holdout 15, dm_s1/retro 14,
  dm_s1/holdout 16, contamination 2, calibration_dm 8. Alle per-sone-tap, MDE, antall origins og beslutninger er bitlike.
  Avvikene sitter bare i DM-HLN-statistikk, standardfeil og p-verdier. De ligger på avrundingsnivå (x86 mot M1) og
  endrer ingen celle i markdown.

## TSFM-sammenligning (Timestral-5M og Chronos-2 på NO4-holdout)
- **IKKE GJORT.** huggingface.co var ikke nåbar i fase 0 (proxy 403, truth/CLOUDSMOKE_KHEPRI-TSFM_v1_2026-11-02.md), så vektene
  med revision=bdd20cfc… og 29ec3766… kunne ikke lastes. Ingen omvei forsøkt. Maks |Δ|, snitt-|Δ| og MAPE-endring per origin
  er derfor ikke målt. (STATE oppgir at A har kjørt repro_from_ci.py lokalt med |Δ| 0,0. Det er As egen kontroll, ikke uavhengig.)

## Andre kontroller
- `uv run --frozen pytest -q` (taggens tests/): 27 passed, 4,6 s, 09:00 UTC.
- khepri_v15/ (D-11): om den er byte-lik med Khepri v1.5 (tagg v1.5, 9e2214f), er IKKE kontrollert. Khepri-repoet er utenfor
  sky-øktas tilgang. Kontrollen hviler på As cmp-sjekk (DEVIATIONS D-11).
- Repro av v1.5-tabellene (REPRO-V15) og repro fra CI (repro_from_ci.py) er ikke kjørt av B. De ligger utenfor oppdraget
  (RESULTATER-tabellene), og repro_from_ci trenger TSFM-vektene.
