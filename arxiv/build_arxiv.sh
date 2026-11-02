#!/bin/bash
# Arkivnøkkel: build_arxiv (fast kodenavn) — bygger arXiv-kilden fra manus/ og kompilerer den.
# Bruk: arxiv/build_arxiv.sh <utmappe>   (utmappen får main.tex, sections/ og main.pdf)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$1"; mkdir -p "$OUT/sections"
md2tex () {  # dropp arkivnøkkel-linja og HTML-kommentarer, fjern nummer i overskrifter, konverter
  /usr/bin/sed -e '1{/^Arkivnøkkel:/d;}' "$1" \
  | /usr/bin/perl -0pe 's/<!--.*?-->//gs; s/^(#+) [0-9]+(\.[0-9]+)* /$1 /mg; s/ \[NR\]//g' \
  | pandoc -f markdown -t latex --wrap=preserve
}
md2tex "$REPO"/manus/MANUS-01-INNLEDNING_KHEPRI-TSFM_v1_*.md > "$OUT/sections/introduction.tex"
md2tex "$REPO"/manus/MANUS-02-RELATEDWORK_KHEPRI-TSFM_v1_*.md | /usr/bin/perl -0pe 's/\\(sub)?section\{References.*//s' > "$OUT/sections/relatedwork.tex"
md2tex "$REPO"/manus/MANUS-03-METODE_KHEPRI-TSFM_v1_*.md > "$OUT/sections/method.tex"
/usr/bin/sed -e 's/\\ref{sec:method}/\\ref{methods}/g; s/\\ref{sec:related}/\\ref{related-work}/g' \
  "$REPO"/manus/MANUS-04-RESULTATER_KHEPRI-TSFM_v1_*.tex > "$OUT/sections/results.tex"
cp "$REPO/arxiv/main.tex" "$OUT/main.tex"
cp "$REPO/arxiv/references.tex" "$OUT/sections/references.tex"
cd "$OUT"
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1 || { tail -30 build.log; exit 1; }; done
/usr/bin/grep -c "LaTeX Warning: Reference" build.log || true
echo "OK: $OUT/main.pdf"
