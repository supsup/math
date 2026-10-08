#!/bin/bash
# Runs INSIDE the container. Generic version of truffet-check.sh.
#   $1 = challenge name (ComparatorChallenges/<name>.json)
#   /plan/modules.txt = the solution's OAI dependency cone, one module per line (from cones.py)
#   /plan/theorems.txt = the theorem names to #print axioms (from the challenge JSON)
# /src = coderefs/math/lean READ-ONLY; /work = named volume confluence-lean-math.
set -euo pipefail
NAME="$1"
export ELAN_HOME=/work/elan
export PATH="$ELAN_HOME/bin:$PATH"
TOOLCHAIN="$(cat /src/lean-toolchain)"
MATHLIB_REV=d13f23b723b8a846827a245b89c10fc7d3f11612

apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq curl git ca-certificates >/dev/null 2>&1
if [ ! -x "$ELAN_HOME/bin/elan" ]; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh
  sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain "$TOOLCHAIN"
fi
lean --version

P="/work/challenge-$NAME"
rm -rf "$P/OAI"
mkdir -p "$P"
cp /src/lean-toolchain "$P/lean-toolchain"
while read -r mod; do
  [ -z "$mod" ] && continue
  rel="${mod//.//}.lean"
  mkdir -p "$P/$(dirname "$rel")"
  cp "/src/$rel" "$P/$rel"
done < /plan/modules.txt
echo "== copied $(find "$P/OAI" -name '*.lean' | wc -l) module file(s)"

cat > "$P/lakefile.lean" <<EOF
import Lake
open Lake DSL

package ChallengeCheck where
  leanOptions := #[⟨\`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "$MATHLIB_REV"

@[default_target]
lean_lib OAI where
  globs := #[.submodules \`OAI]
EOF

ROOT_MODULE="$(head -1 /plan/modules.txt)"
{
  echo "import $ROOT_MODULE"
  echo
  while read -r thm; do [ -n "$thm" ] && echo "#print axioms $thm"; done < /plan/theorems.txt
  echo
  echo "-- NEGATIVE CONTROL: must show sorryAx"
  echo "theorem controlWithSorry : (1 : Nat) = 2 := by sorry"
  echo "#print axioms controlWithSorry"
} > "$P/Check.lean"

cd "$P"
# Reuse the Mathlib checkout from earlier runs instead of re-cloning ~1 GB of git history.
if [ ! -d .lake/packages/mathlib ] && [ -d /work/truffet/.lake/packages ]; then
  mkdir -p .lake && cp -a /work/truffet/.lake/packages .lake/packages
fi
echo "== $(date -u +%H:%M:%SZ) lake update"; lake update 2>&1 | tail -3
echo "== $(date -u +%H:%M:%SZ) cache"; lake exe cache get 2>&1 | tail -2
echo "== $(date -u +%H:%M:%SZ) build"; lake build 2>&1 | tail -12
echo "== $(date -u +%H:%M:%SZ) axioms"; lake env lean Check.lean
echo "== $(date -u +%H:%M:%SZ) done"
