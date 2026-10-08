#!/bin/bash
# Host side: ./check.sh <ChallengeName>   e.g. ./check.sh FourRowPermanent
# Computes the solution's dependency cone (lean-cones/cones.py), refuses cones that need a non-Mathlib
# package (the minimal project only requires Mathlib), then runs check-challenge.sh in a throwaway
# container labelled owner=confluence, with the lean tree READ-ONLY and work in confluence-lean-math.
set -euo pipefail
NAME="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"   # repo root, from playground/confluence/lean-docker/
PLAN="$(mktemp -d)"
python3 -I - "$NAME" "$PLAN" "$HERE/../lean-cones" <<'EOF'
import json, sys
sys.path.insert(0, sys.argv[3])
import cones
name, plan = sys.argv[1], sys.argv[2]
spec = json.loads((cones.LEAN / "ComparatorChallenges" / f"{name}.json").read_text())
mods, ext, missing = cones.cone(spec["solution_module"])
if ext or missing:
    sys.exit(f"refusing {name}: cone needs {sorted(ext)} / unresolved {missing}")
root = spec["solution_module"]
ordered = [root] + sorted(m for m in mods if m != root)
open(f"{plan}/modules.txt", "w").write("\n".join(ordered) + "\n")
open(f"{plan}/theorems.txt", "w").write("\n".join(spec["theorem_names"]) + "\n")
print(f"{name}: {len(mods)} module(s), theorems {spec['theorem_names']}, permitted {spec['permitted_axioms']}")
EOF
docker volume create --label owner=confluence --label purpose=math-playground confluence-lean-math >/dev/null
exec docker run --rm --name "confluence-lean-$(echo "$NAME" | tr 'A-Z' 'a-z')" \
  --label owner=confluence --label purpose=math-playground \
  -v "$REPO/lean":/src:ro \
  -v "$HERE/check-challenge.sh":/check-challenge.sh:ro \
  -v "$PLAN":/plan:ro \
  -v confluence-lean-math:/work \
  debian:bookworm-slim bash /check-challenge.sh "$NAME"
