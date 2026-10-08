"""Does the Truffet SOLUTION define the same things, and state the same theorem, as the CHALLENGE?

Comparator (leanprover/comparator) checks this at the level of compiled terms. Without it, this is a
weaker TEXTUAL check: split both sides into top-level declarations, normalize whitespace, and compare
each challenge declaration with the solution's declaration of the same name. For the theorem, compare
only the statement (everything before ':= by'), since the challenge's proof is `sorry`.

A textual match is strong evidence the statements agree; a textual mismatch is not automatically a
semantic difference (formatting, notation), so mismatches are printed for a human to read.
"""
import pathlib
import re

LEAN = pathlib.Path(__file__).resolve().parents[3] / "lean"  # repo root/lean, from playground/confluence/lean-docker/
CHALLENGE = LEAN / "ComparatorChallenges/TruffetCounterexample.lean"
SOLUTION = [LEAN / "OAI/Optimization/Tropical/TruffetModel.lean",
            LEAN / "OAI/Optimization/Tropical/TruffetCounterexample.lean"]


def configure(name):
    """Point CHALLENGE/SOLUTION at any Comparator challenge, using the cone from lean-cones/cones.py."""
    global CHALLENGE, SOLUTION
    import json
    import sys as _sys
    _sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "lean-cones"))
    import cones
    spec = json.loads((LEAN / "ComparatorChallenges" / f"{name}.json").read_text())
    mods, _, _ = cones.cone(spec["solution_module"])
    CHALLENGE = LEAN / "ComparatorChallenges" / f"{name}.lean"
    SOLUTION = [cones.module_path(m) for m in sorted(mods)]

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+)?(abbrev|def|structure|theorem|lemma|instance)\s+(\S+)", re.M)


def declarations(text):
    """[(name, (kind, normalized text up to the next top-level declaration or command))].
    A LIST, not a dict: one file can declare the same short name in several namespaces
    (log-BM's solution has five `abbrev Space`), and a dict kept only the last."""
    out = []
    starts = [(m.start(), m.group(1), m.group(2)) for m in DECL.finditer(text)]
    # A body also ends at commands that are not declarations; `variable (...)` used to be
    # glued onto the declaration above it (log-BM: `abbrev Space ... variable (mu ...)`).
    ends = [m.start() for m in re.finditer(
        r"^(?:end\b|namespace\b|section\b|noncomputable section|variable\b|open\b|universe\b|set_option\b|attribute\b|#)",
        text, re.M)]
    for idx, (pos, kind, name) in enumerate(starts):
        nxt = [p for p in [s[0] for s in starts[idx + 1:]] + ends if p > pos]
        body = text[pos:min(nxt) if nxt else len(text)]
        norm = normalize(body)
        if kind == "instance" and name[0] in ":{([":
            # An anonymous instance has no name; the regex took its first binder
            # ("{Carrier"), so two anonymous instances in one file collided. Key it
            # by the class it instantiates: the head after the last top-level ':'.
            name = "instance " + instance_head(norm)
        out.append((name, (kind, norm)))
    return out


def instance_head(norm):
    sig = re.split(r"\s?\bwhere\b", statement_only(norm), maxsplit=1)[0]
    depth, colon = 0, -1
    for i, ch in enumerate(sig):
        if ch in "([{\u27e8":
            depth += 1
        elif ch in ")]}\u27e9":
            depth -= 1
        elif ch == ":" and depth == 0:
            colon = i
    return sig[colon + 1:].strip() if colon >= 0 else sig


def normalize(body):
    body = re.sub(r"^\s*noncomputable\s+", "", body)
    # Comments and doc comments are not part of a statement; the next
    # declaration's /-- doc -/ used to be glued onto the previous body.
    body = re.sub(r"/-.*?-/", " ", body, flags=re.S)
    body = re.sub(r"--[^\n]*", " ", body)
    body = " ".join(body.split())
    # Spacing next to brackets, colons and commas is not meaningful:
    # "(m:ℕ)(G:" and "(m : ℕ) (G :" are the same binder list.
    return re.sub(r" ?([()\[\]{}:,]) ?", r"\1", body)


def statement_only(body):
    # The statement ends at the first ":=" outside brackets. Cutting at ":= by"
    # missed term-mode proofs (":= foo bar") and compared the whole proof.
    depth = 0
    for i, ch in enumerate(body):
        if ch in "([{⟨":
            depth += 1
        elif ch in ")]}⟩":
            depth -= 1
        elif depth == 0 and body.startswith(":=", i):
            return body[:i].strip()
    return body


def main():
    ch = dict(declarations(CHALLENGE.read_text()))
    # Names are short names as written, so one name can occur in several solution
    # files (EuclideanRamseyNine has two nine_circle_configuration theorems). Keep
    # every occurrence: a dict used to keep whichever file was read last.
    sol = {}
    for f in SOLUTION:
        for name, decl in declarations(f.read_text()):
            sol.setdefault(name, []).append((f.name, decl))
    print(f"challenge declarations: {len(ch)}; solution declarations: {len(sol)}")
    same, differ, missing = [], [], []
    for name, (kind, body) in ch.items():
        if name not in sol:
            missing.append(name)
            continue
        cands = sol[name]
        strip = statement_only if kind in ("theorem", "lemma") else (lambda x: x)
        a = strip(body)
        hits = [fn for fn, (_, b) in cands if strip(b) == a]
        if len(cands) > 1:
            print(f"NOTE: {name} occurs in {len(cands)} solution files "
                  f"({', '.join(fn for fn, _ in cands)}); identical in: {', '.join(hits) or 'none'}")
        b = strip(cands[0][1][1]) if not hits else a
        # Keep the compared strings: printing the raw bodies showed proofs that
        # were never compared and misled a reader into a stale note.
        if a == b:
            same.append(name)
        else:
            differ.append((name, a, b))
    print(f"identical: {len(same)}  differ: {len(differ)}  missing from solution: {len(missing)}")
    for n, a, b in differ:
        print(f"--- DIFFERS: {n} (compared text)\n  challenge: {a[:300]}\n  solution:  {b[:300]}")
    for n in missing:
        print(f"--- MISSING in solution: {n}")
    extra = sorted(set(sol) - set(ch))
    print(f"solution-only declarations (helpers, allowed): {len(extra)}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        configure(sys.argv[1])
    main()
