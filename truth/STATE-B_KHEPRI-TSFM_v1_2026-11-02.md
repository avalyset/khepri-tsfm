Arkivnøkkel: STATE-B_KHEPRI-TSFM_v1_2026-11-02

- 2026-11-02 08:28:43 UTC: push OK til grenen claude/focused-mayer-kv2xv5 (B skriver ikke til main). git pull OK.
- røyktest ferdig 2026-11-02 08:29 UTC. uv sync OK. IKKE nåbar: arxiv.org (WebFetch), doi.org, crossref, mdpi, pnas, huggingface.co. Nåbar: github.com.
  Følge: fase 1 uten fulltekstlesing av artiklene (bare bibliografisk omtale), fase 2 uten TSFM-rekjøring.
- 2026-11-02T08:39:02Z VARSEL TIL A FØR TAGGEN repro-ready: analysis.py:22 importerer `from khepri import forecast` (Khepri v1.5).
  Pakken khepri finnes verken i repoet, i pyproject.toml eller i uv.lock (`import khepri` → ModuleNotFoundError i sky-miljøet
  etter `uv sync --frozen`). Uten den i taggen kan B ikke kjøre analysis.py uendret. Forslag: legg Khepri v1.5 (tagg v1.5,
  9e2214f) inn i taggen som avhengighet (git-URL med commit i pyproject/uv.lock) eller som vendret kopi. B henter den ikke selv.
- Merk: prediksjonsfilene ligger i predictions/PRED-*, ikke results/PRED-* som i Bs oppdrag; B globber begge.
- Git: B merger origin/main inn i grenen claude/focused-mayer-kv2xv5 (force-push etter rebase ble nektet). Grenen er
  ellers bare Bs filer på toppen av main.
