Arkivnøkkel: CLOUDSMOKE_KHEPRI-TSFM_v1_2026-11-02

Eier: økt B (sky, x86_64 Linux). Fase 0 røyktest. Alle tider UTC 2026-11-02.

| Test | UTC | Resultat |
|---|---|---|
| (a) git pull | 08:27:57 | OK: `git pull --rebase origin main`, «Already up to date» (HEAD 7be8556 = origin/main). |
| (a) git push | se commit-tid for denne fila | Pusher til grenen `claude/focused-mayer-kv2xv5` (sky-øktas tildelte gren; main skrives ikke av B). Utfall i STATE-B. |
| (b) WebFetch https://arxiv.org/abs/2510.01521, kontrollstreng «CarbonX» | ca. 08:27:30 | IKKE TILGJENGELIG: «getaddrinfo ENOTFOUND arxiv.org» (utenfor øktas tillatte domener). Kontrollstrengen ble ikke sett. |
| (c) `uv sync --frozen` mot uv.lock | 08:26:32–08:27:05 | OK, rc 0, 32,8 s. Python 3.12.3 (A: 3.12.13), torch 2.15.0+cu132, lightgbm 4.6.0, statsmodels 0.14.6, timestral 1.0.0 fra git @ a534bdbd. Importtest av torch/lightgbm/chronos/timestral/statsmodels OK. |
| (d) https://huggingface.co/api/models/mistralai/Timestral-5M | 08:26:31 | IKKE NÅBAR: proxy svarer 403 på CONNECT (curl rc 56). |

Andre nettverksfunn (ingen omveier forsøkt):
- curl 08:27:11: arxiv.org, export.arxiv.org, doi.org, api.crossref.org: proxy 403.
- WebFetch ca. 08:28: www.mdpi.com og www.pnas.org: ENOTFOUND. github.com: OK (200).

Konsekvenser:
- Fase 1: ingen av de oppgitte artiklene kan leses i fulltekst fra denne økta. Manus får bare
  bibliografisk omtale av dem, merket «not read», uten innholdspåstander (se SOURCES).
- Fase 2: TSFM-rekjøring (Timestral-5M, Chronos-2) kan ikke gjøres, fordi huggingface.co ikke er nåbar.
  Bare analysis.py-reproduksjonen fra lagrede prediksjoner gjøres.
