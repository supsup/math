"""Re-check of statement_match.py's one 'DIFFERS' for HadamardCubeFiber.

statement_match.py strips proofs only for kind == "theorem" and only at ":= by". The target is a
`lemma` whose solution proof is a TERM (":=\n  ratio_cubeFiber_sum_zero ..."), so both rules miss it
and the full bodies (sorry vs term) get compared. Here: cut every challenge lemma/theorem at its first
" :=" and compare the FULL normalized statement (no 300-char truncation). Negative control: a copy of
the challenge statement with one token changed (`a ≠ b` -> `a = b`) must be reported as different.
"""
import pathlib, sys
SM = pathlib.Path(__file__).resolve().parents[1] / "lean-docker"
sys.path.insert(0, str(SM))
import statement_match as sm

sm.configure("HadamardCubeFiber")
ch = sm.declarations(sm.CHALLENGE.read_text())
sol = {}
for f in sm.SOLUTION:
    sol.update(sm.declarations(f.read_text()))

def stmt(body):
    return body[:body.find(" :=")].strip()

bad = 0
for name, (kind, body) in ch.items():
    a, b = body, sol[name][1]
    if kind in ("theorem", "lemma"):
        a, b = stmt(a), stmt(b)
    same = a == b
    bad += not same
    print(f"{'SAME' if same else 'DIFF'} {kind:8s} {name}  ({len(a)} chars)")
name = "rowRatio_cubeFiber_sum_zero"
mutant = stmt(ch[name][1]).replace("(hne : a ≠ b)", "(hne : a = b)")
assert mutant != stmt(ch[name][1])
print("negative control (mutated hne) detected as different:", mutant != stmt(sol[name][1]))
print("all challenge declarations match:", bad == 0)
