#!/bin/bash
# Arkivnøkkel: issue-wrapper (fast kodenavn) — Khepri-TSFM v1, kalt av launchd.
# Vault-vakt først: uten den lager macOS en fantom-/Volumes/Vault på intern disk.
mount | /usr/bin/grep -q " on /Volumes/Vault " && test -w /Volumes/Vault || { echo "$(date -u +%FT%TZ) VAULT_FAIL" >&2; exit 1; }
source /Volumes/Vault/khepri-tsfm/env.sh || exit 1
cd /Volumes/Vault/khepri-tsfm/repo || exit 1
echo "$(date -u +%FT%TZ) issue start; df -h /: $(df -h / | tail -1)"
exec /Volumes/Vault/khepri-tsfm/.venv/bin/python issue.py
