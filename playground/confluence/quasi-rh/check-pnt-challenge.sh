#!/bin/bash
# Runs INSIDE the container. Variant of check-challenge.sh for a cone needing PrimeNumberTheoremAnd.
# /src = repo lean/ READ-ONLY; /work = volume confluence-lean-math-pnt; /plan = modules/theorems.
set -euo pipefail
NAME="$1"
export ELAN_HOME=/work/elan
export PATH="$ELAN_HOME/bin:$PATH"
TOOLCHAIN="$(cat /src/lean-toolchain)"
PNT_URL=https://github.com/AlexKontorovich/PrimeNumberTheoremAnd.git
PNT_REV=c39a751132c88b6e8080b74c74023fd95b3d8be0
PATCH=/src/patches/PrimeNumberTheoremAnd-lean4341.patch

apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq curl git ca-certificates python3 >/dev/null 2>&1
if [ ! -x "$ELAN_HOME/bin/elan" ]; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh
  sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain "$TOOLCHAIN"
fi
lean --version

P="/work/challenge-$NAME"
rm -rf "$P/OAI" "$P/ComparatorChallenges"
mkdir -p "$P"
cp /src/lean-toolchain "$P/lean-toolchain"
while read -r mod; do
  [ -z "$mod" ] && continue
  rel="${mod//.//}.lean"
  mkdir -p "$P/$(dirname "$rel")"
  cp "/src/$rel" "$P/$rel"
done < /plan/modules.txt
echo "== copied $(find "$P/OAI" -name '*.lean' | wc -l) module file(s)"
CH_REL="$(sed 's#\.#/#g' /plan/challenge_module.txt).lean"
mkdir -p "$P/$(dirname "$CH_REL")"; cp "/src/$CH_REL" "$P/$CH_REL"

# Require lines copied verbatim from the repo lakefile (lines 73-86), same order: shared deps last.
cat > "$P/lakefile.lean" <<'EOF'
import Lake
open Lake DSL

package ChallengeCheck where
  leanOptions := #[⟨`autoImplicit, false⟩]

require PrimeNumberTheoremAnd from git
  "https://github.com/AlexKontorovich/PrimeNumberTheoremAnd.git" @ "c39a751132c88b6e8080b74c74023fd95b3d8be0"
require leancert from git
  "https://github.com/alerad/leancert.git" @ "7f91b6eb3567437f6cfac03ed279706603ee22f4"
require LeanArchitect from git
  "https://github.com/hanwenzhu/LeanArchitect.git" @ "468e8f58fb4ad6e6ad672a08da6d0d0531e95a97"
require PrimeCert from git
  "https://github.com/b-mehta/PrimeCert.git" @ "0803c2f6bd289c09704c7d352bb8fcf770cbb9b2"
require «doc-gen4» from git
  "https://github.com/leanprover/doc-gen4.git" @ "953c8992d174b4e56955e01e101d46668c68f2bb"
require checkdecls from git
  "https://github.com/PatrickMassot/checkdecls.git" @ "3d425859e73fcfbef85b9638c2a91708ef4a22d4"
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

@[default_target]
lean_lib OAI where
  globs := #[.submodules `OAI]
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
if [ ! -f lake-manifest.json ]; then
  echo "== $(date -u +%H:%M:%SZ) lake update"; lake update 2>&1 | tail -20
else
  echo "== manifest present from an earlier run; not re-resolving"
fi
echo "== $(date -u +%H:%M:%SZ) verify resolved pins against repo manifest"
python3 -I /plan/verify-manifest.py lake-manifest.json /src/lake-manifest.json

# Patch exactly as lean/lakefile.lean post_update does (lines 293-335): HEAD must equal the pin;
# `git -C <dep dir> apply --check --reverse <patch>` => already applied; else `apply --check` =>
# `git -C <dep dir> apply <patch>` then verify with `apply --check --reverse`; else conflict => stop.
D="$P/.lake/packages/PrimeNumberTheoremAnd"
HEAD="$(git -C "$D" rev-parse HEAD)"
[ "$HEAD" = "$PNT_REV" ] || { echo "STOP: PNT HEAD $HEAD != $PNT_REV"; exit 3; }
echo "== PNT origin $(git -C "$D" remote get-url origin) HEAD $HEAD"
if git -C "$D" apply --check --reverse "$PATCH" 2>/dev/null; then
  echo "== PNT: compatibility patch already applied"
elif git -C "$D" apply --check "$PATCH"; then
  git -C "$D" apply "$PATCH"
  git -C "$D" apply --check --reverse "$PATCH" || { echo "STOP: patch verification failed"; exit 4; }
  echo "== PNT: applied compatibility patch $(basename "$PATCH")"
else
  echo "STOP: compatibility patch conflicts"; exit 5
fi
git -C "$D" status --short | wc -l | xargs echo "== PNT dirty paths after patch:"

echo "== $(date -u +%H:%M:%SZ) cache"; lake exe cache get 2>&1 | tail -3
echo "== $(date -u +%H:%M:%SZ) build start"
T0=$(date +%s)
set +e
lake build 2>&1 | tee /work/build-$NAME.log | grep -vE '^. \[[0-9]+/[0-9]+\] (Replayed|Built|Fetched)' | tail -60
RC=${PIPESTATUS[0]}
set -e
T1=$(date +%s)
echo "== build exit=$RC duration=$((T1-T0))s"
echo "== built lines: $(grep -cE '\] Built ' /work/build-$NAME.log)  replayed: $(grep -cE '\] Replayed ' /work/build-$NAME.log)  last job: $(grep -oE '\[[0-9]+/[0-9]+\]' /work/build-$NAME.log | tail -1)"
echo "== built PNT modules: $(grep -E '\] Built PrimeNumberTheoremAnd' /work/build-$NAME.log | wc -l)  built OAI modules: $(grep -E '\] Built OAI' /work/build-$NAME.log | wc -l)"
tail -3 /work/build-$NAME.log
[ "$RC" = 0 ] || exit "$RC"
echo "== $(date -u +%H:%M:%SZ) axioms"; if lake env lean Check.lean; then echo "check-exit=0"; else echo "check-exit=$?"; fi
echo "== $(date -u +%H:%M:%SZ) challenge statement file elaborates?"
if lake env lean "$CH_REL"; then echo "challenge-elab exit=0"; else echo "challenge-elab exit=$?"; fi
echo "== $(date -u +%H:%M:%SZ) done"
