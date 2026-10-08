#!/bin/bash
# Host side: one throwaway container, labelled as mine, the lean tree mounted READ-ONLY, all work in
# the named volume confluence-lean-math (kept so later experiments reuse the Mathlib cache).
# Charles OK'd Docker for isolated replication (2026-10-08). This starts no Stafficy service.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"   # repo root, from playground/confluence/lean-docker/
docker volume create --label owner=confluence --label purpose=math-playground confluence-lean-math >/dev/null
exec docker run --rm --name confluence-lean-truffet \
  --label owner=confluence --label purpose=math-playground \
  -v "$REPO/lean":/src:ro \
  -v "$HERE/truffet-check.sh":/truffet-check.sh:ro \
  -v confluence-lean-math:/work \
  debian:bookworm-slim bash /truffet-check.sh
