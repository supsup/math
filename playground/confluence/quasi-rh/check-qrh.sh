#!/bin/bash
# Host side: ./check-qrh.sh   — builds the shared solution module of DirichletSevenEighths and
# QuasiRiemannHypothesis (OAI.NumberTheory.DirichletL.Nonvanishing) with the repo's pins for
# rellich-kondrachov + PrimeNumberTheoremAnd + shared deps, and the repo's compatibility patches.
# Repo is mounted READ-ONLY; work lives in NEW volume confluence-lean-math-qrh.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=/Users/charles/projects/commander-worktrees/confluence/math
LOCK=/private/tmp/claude-501/-Users-charles-projects-stafficy-worktree/02e94678-0a90-4345-81bc-a3720fa37464/scratchpad/lean-docker.lock
GATE=/Users/charles/projects/commander-worktrees/confluence/skills-worktree/main/hooks/shared/claude/machine-free-gate.py
PLAN="$HERE/plan"
rm -rf "$PLAN"; mkdir -p "$PLAN"

python3 -I - "$PLAN" "$REPO/playground/confluence/lean-cones" <<'EOF'
import json, sys
sys.path.insert(0, sys.argv[2])
import cones
plan = sys.argv[1]
names = ["DirichletSevenEighths", "QuasiRiemannHypothesis"]
specs = [json.loads((cones.LEAN / "ComparatorChallenges" / f"{n}.json").read_text()) for n in names]
roots = {s["solution_module"] for s in specs}
if len(roots) != 1:
    sys.exit(f"refusing: solution modules differ {roots}")
root = roots.pop()
mods, ext, missing = cones.cone(root)
if ext != {"PrimeNumberTheoremAnd", "RellichKondrachov"} or missing:
    sys.exit(f"refusing: cone needs {sorted(ext)} / unresolved {missing}")
ordered = [root] + sorted(m for m in mods if m != root)
open(f"{plan}/modules.txt", "w").write("\n".join(ordered) + "\n")
thms = [t for s in specs for t in s["theorem_names"]]
open(f"{plan}/theorems.txt", "w").write("\n".join(thms) + "\n")
open(f"{plan}/challenge_modules.txt", "w").write("\n".join(s["challenge_module"] for s in specs) + "\n")
for n, s in zip(names, specs):
    print(f"{n}: solution {s['solution_module']} theorems {s['theorem_names']} permitted {s['permitted_axioms']}")
print(f"cone: {len(mods)} module(s), ext {sorted(ext)}")
EOF
cp "$HERE/verify-manifest.py" "$PLAN/verify-manifest.py"
mkdir -p "$HERE/out"

until mkdir "$LOCK" 2>/dev/null; do echo "lock held, waiting $(date -u +%H:%M:%SZ)"; sleep 30; done
trap 'rmdir "$LOCK"' EXIT
echo "== lock taken $(date -u +%H:%M:%SZ)"

python3 "$GATE" --wait --timeout 1800

docker volume create --label owner=confluence --label purpose=math-playground confluence-lean-math-qrh >/dev/null
docker run --rm --name confluence-lean-qrh \
  --label owner=confluence --label purpose=math-playground \
  -v "$REPO/lean":/src:ro \
  -v "$HERE/check-qrh-challenge.sh":/check-qrh-challenge.sh:ro \
  -v "$PLAN":/plan:ro \
  -v "$HERE/out":/out \
  -v confluence-lean-math-qrh:/work \
  debian:bookworm-slim bash /check-qrh-challenge.sh
