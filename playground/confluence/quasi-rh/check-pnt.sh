#!/bin/bash
# Host side: ./check-pnt.sh <ChallengeName>   (written for SiegelZeros)
# Like playground/confluence/lean-docker/check.sh, but ADMITS a cone whose only external package is
# PrimeNumberTheoremAnd, and builds it with the repo's pins + the repo's PNT compatibility patch.
# Repo is mounted READ-ONLY; work lives in volume confluence-lean-math-pnt (NOT confluence-lean-math).
set -euo pipefail
NAME="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=/Users/charles/projects/commander-worktrees/confluence/math
LOCK=/private/tmp/claude-501/-Users-charles-projects-stafficy-worktree/02e94678-0a90-4345-81bc-a3720fa37464/scratchpad/lean-docker.lock
GATE=/Users/charles/projects/commander-worktrees/confluence/skills-worktree/main/hooks/shared/claude/machine-free-gate.py
PLAN="$HERE/plan-$NAME"
rm -rf "$PLAN"; mkdir -p "$PLAN"

python3 -I - "$NAME" "$PLAN" "$REPO/playground/confluence/lean-cones" <<'EOF'
import json, sys
sys.path.insert(0, sys.argv[3])
import cones
name, plan = sys.argv[1], sys.argv[2]
spec = json.loads((cones.LEAN / "ComparatorChallenges" / f"{name}.json").read_text())
mods, ext, missing = cones.cone(spec["solution_module"])
if ext != {"PrimeNumberTheoremAnd"} or missing:
    sys.exit(f"refusing {name}: cone needs {sorted(ext)} / unresolved {missing}")
root = spec["solution_module"]
ordered = [root] + sorted(m for m in mods if m != root)
open(f"{plan}/modules.txt", "w").write("\n".join(ordered) + "\n")
open(f"{plan}/theorems.txt", "w").write("\n".join(spec["theorem_names"]) + "\n")
open(f"{plan}/challenge_module.txt", "w").write(spec["challenge_module"] + "\n")
print(f"{name}: {len(mods)} module(s), ext {sorted(ext)}, theorems {spec['theorem_names']}, permitted {spec['permitted_axioms']}")
EOF
cp "$HERE/verify-manifest.py" "$PLAN/verify-manifest.py"

# Serialise Docker use with the shared lock (never delete someone else's lock).
until mkdir "$LOCK" 2>/dev/null; do echo "lock held, waiting $(date -u +%H:%M:%SZ)"; sleep 30; done
trap 'rmdir "$LOCK"' EXIT
echo "== lock taken $(date -u +%H:%M:%SZ)"

python3 "$GATE" --wait --timeout 1800

docker volume create --label owner=confluence --label purpose=math-playground confluence-lean-math-pnt >/dev/null
docker run --rm --name "confluence-lean-pnt-$(echo "$NAME" | tr 'A-Z' 'a-z')" \
  --label owner=confluence --label purpose=math-playground \
  -v "$REPO/lean":/src:ro \
  -v "$HERE/check-pnt-challenge.sh":/check-pnt-challenge.sh:ro \
  -v "$PLAN":/plan:ro \
  -v confluence-lean-math-pnt:/work \
  debian:bookworm-slim bash /check-pnt-challenge.sh "$NAME"
