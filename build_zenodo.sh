#!/bin/bash
# Arkivnøkkel: build_zenodo (fast kodenavn) — bygger ZENODO-tarballen for Khepri-TSFM v1.
# Innhold: git archive av <ref>, pluss prereg-bevis/: PREREG-tarballen med sha256, alle .ots-bevis
# (oppgradert der mulig) og tagg-objektene prereg-v1 og repro-ready med GPG-signatur.
# Bruk: ./build_zenodo.sh <git-ref> <ut.tar.gz>
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
V=/Volumes/Vault/khepri-tsfm
REF="$1"; OUT="$2"
WORK="$V/tmp/zenodo-build"; rm -rf "$WORK"; mkdir -p "$WORK/khepri-tsfm/prereg-bevis"
git -C "$REPO" archive --prefix=khepri-tsfm/ "$REF" | tar -x -C "$WORK"
E="$WORK/khepri-tsfm/prereg-bevis"
cp "$V/PREREG_KHEPRI-TSFM_v1_2026-11-02.tar.gz" "$V/PREREG_KHEPRI-TSFM_v1_2026-11-02.tar.gz.sha256" \
   "$V/PREREG_KHEPRI-TSFM_v1_2026-11-02.tar.gz.ots" "$E/"
cp "$V/data/raw/entsoe-rest-2026/SHA256SUMS_raw2026.txt" "$V/data/raw/entsoe-rest-2026/SHA256SUMS_raw2026.txt.ots" "$E/"
for t in prereg-v1 repro-ready; do
  git -C "$REPO" cat-file tag "$t" > "$E/tag-$t.txt"
  git -C "$REPO" tag -v "$t" > "$E/tag-$t.verify.txt" 2>&1 || true
done
gpg --armor --export C96D4E5C5636088C > "$E/gpg-C96D4E5C5636088C.asc"
# .ots in the archive are copied from the working copy only if newer (upgraded) than in git
for o in $(cd "$WORK/khepri-tsfm" && find . -name '*.ots'); do
  if [ -f "$REPO/$o" ] && ! cmp -s "$REPO/$o" "$WORK/khepri-tsfm/$o"; then cp "$REPO/$o" "$WORK/khepri-tsfm/$o"; echo "oppgradert ots: $o"; fi
done
(cd "$WORK" && COPYFILE_DISABLE=1 tar --no-xattrs -czf "$OUT" khepri-tsfm)
shasum -a 256 "$OUT"
