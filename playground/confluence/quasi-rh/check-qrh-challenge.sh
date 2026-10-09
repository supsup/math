#!/bin/bash
# Runs INSIDE the container. /src = repo lean/ READ-ONLY; /work = volume confluence-lean-math-qrh;
# /plan = modules/theorems; /out = host scratch for full logs.
set -euo pipefail
export ELAN_HOME=/work/elan
export PATH="$ELAN_HOME/bin:$PATH"
TOOLCHAIN="$(cat /src/lean-toolchain)"

apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq curl git ca-certificates python3 >/dev/null 2>&1
if [ ! -x "$ELAN_HOME/bin/elan" ]; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh
  sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain "$TOOLCHAIN"
fi
lean --version

P=/work/challenge-DirichletL-Nonvanishing
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
CH_RELS=()
while read -r ch; do
  [ -z "$ch" ] && continue
  rel="${ch//.//}.lean"; mkdir -p "$P/$(dirname "$rel")"; cp "/src/$rel" "$P/$rel"; CH_RELS+=("$rel")
done < /plan/challenge_modules.txt

# Requires copied verbatim from the repo lakefile, in the repo's order: rellich-kondrachov
# (lines 14-15) before the shared-deps block (lines 71-86, shared deps last).
cat > "$P/lakefile.lean" <<'EOF'
import Lake
open Lake DSL

package ChallengeCheck where
  leanOptions := #[⟨`autoImplicit, false⟩]

require «rellich-kondrachov» from git
  "https://github.com/abenenson/rellich-kondrachov.git" @ "70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23"

-- Declare shared dependencies last: Lake resolves later requirements first.
-- These pins override the older versions in the upstream packages' manifests.
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
cat "$P/Check.lean"

cd "$P"
if [ ! -f lake-manifest.json ]; then
  echo "== $(date -u +%H:%M:%SZ) lake update"; lake update 2>&1 | tail -30
else
  echo "== manifest present from an earlier run; not re-resolving"
fi
cp lake-manifest.json /out/resolved-lake-manifest.json
echo "== $(date -u +%H:%M:%SZ) verify resolved pins against repo manifest"
python3 -I /plan/verify-manifest.py lake-manifest.json /src/lake-manifest.json

# Patch exactly as lean/lakefile.lean post_update does (lines 293-335): preflight EVERY listed
# dependency before changing any (HEAD must equal the pin; `apply --check --reverse` => already
# applied; else `apply --check` => to apply; else conflict => stop), then apply and verify with
# `apply --check --reverse`. Order follows the post_update list (PNT before rellich-kondrachov).
declare -A REV=(
  [PrimeNumberTheoremAnd]=c39a751132c88b6e8080b74c74023fd95b3d8be0
  [rellich-kondrachov]=70f85d4c1bf99c6e7d61e8be4daa6f3664d08d23 )
ORDER=(PrimeNumberTheoremAnd rellich-kondrachov)
TODO=()
for label in "${ORDER[@]}"; do
  D="$P/.lake/packages/$label"; PATCH="/src/patches/$label-lean4341.patch"
  [ -f "$PATCH" ] || { echo "STOP: missing patch $PATCH"; exit 6; }
  HEAD="$(git -C "$D" rev-parse HEAD)"
  [ "$HEAD" = "${REV[$label]}" ] || { echo "STOP: $label HEAD $HEAD != ${REV[$label]}"; exit 3; }
  echo "== $label origin $(git -C "$D" remote get-url origin) HEAD $HEAD"
  if git -C "$D" apply --check --reverse "$PATCH" 2>/dev/null; then
    echo "== $label: compatibility patch already applied"
  elif git -C "$D" apply --check "$PATCH"; then
    TODO+=("$label")
  else
    echo "STOP: $label compatibility patch conflicts"; exit 5
  fi
done
for label in "${TODO[@]}"; do
  D="$P/.lake/packages/$label"; PATCH="/src/patches/$label-lean4341.patch"
  git -C "$D" apply "$PATCH"
  git -C "$D" apply --check --reverse "$PATCH" || { echo "STOP: $label patch verification failed"; exit 4; }
  echo "== $label: applied compatibility patch $(basename "$PATCH")"
done
for label in "${ORDER[@]}"; do
  git -C "$P/.lake/packages/$label" status --short | wc -l | xargs echo "== $label dirty paths after patch:"
done

echo "== $(date -u +%H:%M:%SZ) cache"; lake exe cache get 2>&1 | tail -3
echo "== $(date -u +%H:%M:%SZ) build start"
T0=$(date +%s)
set +e
lake build 2>&1 | tee /out/build.log | grep -vE '^. \[[0-9]+/[0-9]+\] (Replayed|Built|Fetched)' | tail -80
RC=${PIPESTATUS[0]}
set -e
T1=$(date +%s)
L=/out/build.log
echo "== build exit=$RC duration=$((T1-T0))s"
echo "== built lines: $(grep -cE '\] Built ' $L)  replayed: $(grep -cE '\] Replayed ' $L)  last job: $(grep -oE '\[[0-9]+/[0-9]+\]' $L | tail -1)"
echo "== built PNT: $(grep -cE '\] Built PrimeNumberTheoremAnd' $L)  built RK: $(grep -cE '\] Built (RellichKondrachov|MathlibExtensions)' $L)  built OAI: $(grep -cE '\] Built OAI' $L)  built Mathlib: $(grep -cE '\] Built Mathlib' $L)"
tail -3 $L
[ "$RC" = 0 ] || exit "$RC"
echo "== $(date -u +%H:%M:%SZ) axioms"; if lake env lean Check.lean; then echo "check-exit=0"; else echo "check-exit=$?"; fi
for rel in "${CH_RELS[@]}"; do
  echo "== $(date -u +%H:%M:%SZ) challenge statement file elaborates? $rel"
  if lake env lean "$rel"; then echo "challenge-elab $rel exit=0"; else echo "challenge-elab $rel exit=$?"; fi
done
echo "== $(date -u +%H:%M:%SZ) done"
