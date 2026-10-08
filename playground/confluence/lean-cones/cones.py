"""For each Comparator challenge, measure the dependency cone of its SOLUTION module inside the
OAI library: how many OAI modules it transitively imports, and whether any of them import a
non-Mathlib external package (Carleson, SphereEversion, ...). Small, Mathlib-only cones are the
cheapest results to build and check in a container.

Reads the repo read-only; writes nothing outside this folder.
"""
import json
import pathlib
import re
import sys

LEAN = pathlib.Path(__file__).resolve().parents[3] / "lean"  # repo root/lean, from playground/confluence/lean-cones/
IMPORT = re.compile(r"^\s*import\s+(.+)$")


def module_path(mod):
    return LEAN / (mod.replace(".", "/") + ".lean")


def imports_of(mod, cache={}):
    if mod in cache:
        return cache[mod]
    p = module_path(mod)
    out = []
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            m = IMPORT.match(line)
            if m:
                out.extend(m.group(1).split())
            elif line.strip() and not line.strip().startswith(("--", "/-", "import", "module", "public", "prelude")) and out:
                # imports must come first; stop at the first real declaration once we have some
                break
    cache[mod] = out
    return out


def cone(root):
    seen, stack, externals = set(), [root], set()
    while stack:
        mod = stack.pop()
        if mod in seen:
            continue
        seen.add(mod)
        for imp in imports_of(mod):
            top = imp.split(".")[0]
            if top == "OAI":
                stack.append(imp)
            elif top not in ("Mathlib", "Init", "Std", "Lean", "Batteries", "Aesop", "Qq", "ProofWidgets", "Plausible", "LeanSearchClient", "ImportGraph"):
                externals.add(top)
    missing = [m for m in seen if not module_path(m).exists()]
    return seen, externals, missing


def main():
    rows = []
    for j in sorted((LEAN / "ComparatorChallenges").glob("*.json")):
        spec = json.loads(j.read_text())
        sol = spec["solution_module"]
        mods, ext, missing = cone(sol)
        rows.append((len(mods), j.stem, sol, sorted(ext), len(missing)))
    rows.sort()
    print(f"{len(rows)} challenges")
    print("smallest Mathlib-only cones:")
    shown = 0
    for n, name, sol, ext, miss in rows:
        if not ext and not miss:
            print(f"  {n:4d} modules  {name:40s} {sol}")
            shown += 1
            if shown >= 15:
                break
    with_ext = sum(1 for r in rows if r[3])
    print(f"challenges whose cone needs a non-Mathlib package: {with_ext} of {len(rows)}")
    print(f"challenges with an unresolved import inside OAI: {sum(1 for r in rows if r[4])}")


if __name__ == "__main__":
    sys.exit(main())
