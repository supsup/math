#!/bin/bash
# Runs INSIDE the container (debian:bookworm-slim). Builds the 2-module Truffet cone against the
# pinned Mathlib and prints the axioms of the main theorem.
#
#   /src  = coderefs/math/lean, mounted READ-ONLY
#   /work = the named volume confluence-lean-math (elan, the Mathlib cache, build output)
#
# Started from the host by run-truffet.sh. Nothing here writes to /src.
set -euo pipefail

export ELAN_HOME=/work/elan
export PATH="$ELAN_HOME/bin:$PATH"
TOOLCHAIN="$(cat /src/lean-toolchain)"
MATHLIB_REV=d13f23b723b8a846827a245b89c10fc7d3f11612

echo "== $(date -u +%H:%M:%SZ) packages"
apt-get update -qq >/dev/null
apt-get install -y -qq curl git ca-certificates >/dev/null

if [ ! -x "$ELAN_HOME/bin/elan" ]; then
  echo "== $(date -u +%H:%M:%SZ) installing elan with $TOOLCHAIN"
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh
  sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain "$TOOLCHAIN"
fi
lean --version

P=/work/truffet
mkdir -p "$P/OAI/Optimization/Tropical"
cp /src/lean-toolchain "$P/lean-toolchain"
cp /src/OAI/Optimization/Tropical/TruffetModel.lean /src/OAI/Optimization/Tropical/TruffetCounterexample.lean \
   "$P/OAI/Optimization/Tropical/"
cat > "$P/lakefile.lean" <<EOF
import Lake
open Lake DSL

package TruffetCheck where
  leanOptions := #[⟨\`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "$MATHLIB_REV"

@[default_target]
lean_lib OAI where
  globs := #[.submodules \`OAI]
EOF
cat > "$P/Check.lean" <<'EOF'
import OAI.Optimization.Tropical.TruffetCounterexample

#check @OAI.TruffetV4Counterexample.finite_execution_not_optimal
#print axioms OAI.TruffetV4Counterexample.finite_execution_not_optimal

-- NEGATIVE CONTROL: a theorem proved with `sorry` must show sorryAx, so the line above
-- reporting no sorryAx is evidence and not an instrument that cannot say it.
theorem controlWithSorry : (1 : Nat) = 2 := by sorry
#print axioms controlWithSorry
EOF

cd "$P"
echo "== $(date -u +%H:%M:%SZ) lake update (resolves mathlib at the pinned rev)"
lake update 2>&1 | tail -5
echo "== $(date -u +%H:%M:%SZ) mathlib cache"
lake exe cache get 2>&1 | tail -5
echo "== $(date -u +%H:%M:%SZ) building the cone"
lake build 2>&1 | tail -15
echo "== $(date -u +%H:%M:%SZ) axioms"
lake env lean Check.lean
echo "== $(date -u +%H:%M:%SZ) done"
