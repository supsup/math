"""Independent Python replication of OAI.TruffetV4Counterexample.finite_execution_not_optimal
(lean/ComparatorChallenges/TruffetCounterexample.lean), transcribing the challenge's DEFINITIONS
one for one. Coeff = WithBot R  ->  float, with BOT = -inf. Max-plus: "+" is ordinary +, with
BOT absorbing (BOT + x = BOT), matching WithBot addition.

Each of the theorem's 13 conjuncts is checked separately and printed. crossRowRestriction is
a "for all alpha exists w" statement; it is checked by exhibiting a witness family w(alpha)
and testing it over a sweep of alpha, which is evidence, not a proof (the Lean proof is the proof).
"""
import itertools
import math

BOT = -math.inf
VARS = (0, 1)        # Var = Fin 2
ROWS = (0, 1)        # RowIndex = Fin 2
K = (0, 1, 2)        # Fin 3 (column 2 is the constant column)


def add(a, b):
    return BOT if a == BOT or b == BOT else a + b


def column(j):
    return j


NULL = (BOT, BOT, BOT)


class State:
    def __init__(self, rows, cost, remaining):
        self.rows = rows            # tuple of (lhs, rhs), each a 3-tuple
        self.cost = cost
        self.remaining = remaining  # function Var -> bool

    def __eq__(self, other):
        return (self.rows == other.rows and self.cost == other.cost
                and all(self.remaining(j) == other.remaining(j) for j in VARS))


def well_formed(s):
    for j in VARS:
        if not s.remaining(j):
            if s.cost[column(j)] != BOT:
                return False
            for i in ROWS:
                lhs, rhs = s.rows[i]
                if lhs[column(j)] != BOT or rhs[column(j)] != BOT:
                    return False
    return True


def ev(f, w):
    return max(add(f[0], w[0]), add(f[1], w[1]), add(f[2], w[2]))


def feasible(s, w):
    return all(ev(s.rows[i][1], w) <= ev(s.rows[i][0], w) for i in ROWS)


def lower(s, i, j):
    lhs, rhs = s.rows[i]
    return lhs[column(j)] != BOT and rhs[column(j)] < lhs[column(j)]


def upper(s, i, j):
    lhs, rhs = s.rows[i]
    return rhs[column(j)] != BOT and lhs[column(j)] < rhs[column(j)]


def dominating(s, j):
    return s.remaining(j) and any(lower(s, i, j) for i in ROWS) and any(upper(s, i, j) for i in ROWS)


def eligible(s, i, j):
    return s.remaining(j) and lower(s, i, j) and ((not any(dominating(s, k) for k in VARS)) or dominating(s, j))


def bounded(s):
    return all((not s.remaining(j)) or any(lower(s, i, j) for i in ROWS) or any(upper(s, i, j) for i in ROWS)
               for j in VARS)


def stop(s):
    return all(s.rows[i][1][2] <= s.rows[i][0][2] for i in ROWS)


def switch(s):
    return (all((not s.remaining(j)) or s.cost[column(j)] == BOT for j in VARS)
            and not stop(s)
            and any(s.remaining(j) for j in VARS)
            and not any(s.remaining(j) and lower(s, i, j) for i in ROWS for j in VARS)
            and any(s.remaining(j) and upper(s, i, j) for i in ROWS for j in VARS))


def failure(s):
    return (not stop(s)) and (
        (not any(s.remaining(j) for j in VARS))
        or ((not any(s.remaining(j) and lower(s, i, j) for i in ROWS for j in VARS))
            and (not any(s.remaining(j) and upper(s, i, j) for i in ROWS for j in VARS))))


def unbotD(default, x):
    return default if x == BOT else x


def lower_form(s, i, j):
    lhs, rhs = s.rows[i]
    shift = -unbotD(0.0, lhs[column(j)])
    return tuple(BOT if k == column(j) else add(rhs[k], shift) for k in K)


def substitute(f, j, g):
    return tuple(BOT if k == column(j) else max(f[k], add(f[column(j)], g[k])) for k in K)


def cleanup(r):
    lhs, rhs = r
    return (NULL, NULL) if all(rhs[k] <= lhs[k] for k in K) else r


def advance(s, i, j):
    g = lower_form(s, i, j)
    rows = tuple(cleanup((substitute(s.rows[r][0], j, g), substitute(s.rows[r][1], j, g))) for r in ROWS)
    rem = s.remaining
    return State(rows, substitute(s.cost, j, g), lambda k, rem=rem, j=j: rem(k) and k != j)


def forced_singleton_step(s, s2, i, j):
    parts = {
        "wellFormed s": well_formed(s),
        "wellFormed s'": well_formed(s2),
        "bounded s": bounded(s),
        "not stop s": not stop(s),
        "not switch s": not switch(s),
        "not failure s": not failure(s),
        "eligible exactly (i,j)": all(eligible(s, r, k) == (r == i and k == j) for r in ROWS for k in VARS),
        "substituted cost not all BOT": any(x != BOT for x in substitute(s.cost, j, lower_form(s, i, j))),
        "s' = advance s i j": s2 == advance(s, i, j),
    }
    return all(parts.values()), parts


INITIAL = State(
    rows=(((0.0, 0.0, BOT), (BOT, BOT, 0.0)),
          ((0.0, BOT, BOT), (BOT, 1.0, -2.0))),
    cost=(0.0, BOT, BOT),
    remaining=lambda _j: True)

MIDDLE = State(
    rows=((NULL, NULL),
          ((0.0, BOT, BOT), (BOT, BOT, 1.0))),
    cost=(0.0, BOT, BOT),
    remaining=lambda j: j == 0)

FINAL = State(
    rows=((NULL, NULL), (NULL, NULL)),
    cost=(BOT, BOT, 1.0),
    remaining=lambda _j: False)

OUTPUT = (1.0, 0.0, 0.0)
BETTER = (0.0, -1.0, 0.0)


def cross_row_restriction_evidence(s):
    """For each ordered pair i != r and a sweep of alpha, find w with eval(lhs_i, w) < alpha + eval(rhs_r, w)
    by a small search over w; report whether every sampled alpha got a witness."""
    alphas = [-1e6, -1e3, -50, -5, -1, 0, 1, 5, 50, 1e3, 1e6]
    for i, r in itertools.permutations(ROWS, 2):
        for a in alphas:
            found = False
            for scale in (1, 10, 1e3, 1e6, 1e9):
                for w in itertools.product((-scale, 0.0, scale), repeat=3):
                    if ev(s.rows[i][0], w) < add(a, ev(s.rows[r][1], w)):
                        found = True
                        break
                if found:
                    break
            if not found:
                return False, (i, r, a)
    return True, None


def main():
    ok_step1, parts1 = forced_singleton_step(INITIAL, MIDDLE, 0, 1)
    ok_step2, parts2 = forced_singleton_step(MIDDLE, FINAL, 1, 0)
    crr, counter = cross_row_restriction_evidence(INITIAL)
    conj = [
        ("crossRowRestriction initial (sampled evidence)", crr),
        ("ForcedSingletonStep initial middle 0 1", ok_step1),
        ("ForcedSingletonStep middle finalState 1 0", ok_step2),
        ("no remaining var in finalState", not any(FINAL.remaining(j) for j in VARS)),
        ("stop finalState", stop(FINAL)),
        ("feasible initial output", feasible(INITIAL, OUTPUT)),
        ("feasible initial better", feasible(INITIAL, BETTER)),
        ("output 2 = 0", OUTPUT[2] == 0),
        ("better 2 = 0", BETTER[2] == 0),
        ("output 1 = eval (lowerForm initial 0 1) output", OUTPUT[1] == ev(lower_form(INITIAL, 0, 1), OUTPUT)),
        ("output 0 = eval (lowerForm middle 1 0) output", OUTPUT[0] == ev(lower_form(MIDDLE, 1, 0), OUTPUT)),
        ("eval initial.cost output = eval final.cost output", ev(INITIAL.cost, OUTPUT) == ev(FINAL.cost, OUTPUT)),
        ("eval initial.cost better < eval final.cost output", ev(INITIAL.cost, BETTER) < ev(FINAL.cost, OUTPUT)),
    ]
    for name, val in conj:
        print(f"  [{'OK ' if val else 'NO '}] {name}")
    for label, parts in (("step 1", parts1), ("step 2", parts2)):
        bad = [k for k, v in parts.items() if not v]
        print(f"  {label} sub-conditions failing: {bad or 'none'}")
    if counter:
        print("  crossRowRestriction: no witness found at", counter)
    print(f"costs: algorithm's output costs {ev(FINAL.cost, OUTPUT)}, 'better' costs {ev(INITIAL.cost, BETTER)}")
    print("ALL 13 CONJUNCTS HOLD" if all(v for _, v in conj) else "SOME CONJUNCT FAILS")

    # a negative control: the replication must be able to say NO
    broken = State(INITIAL.rows, INITIAL.cost, INITIAL.remaining)
    print("control: ForcedSingletonStep initial middle with the WRONG pivot (1,1):",
          forced_singleton_step(INITIAL, MIDDLE, 1, 1)[0])
    print("control: feasible initial (5,5,0):", feasible(broken, (5.0, 5.0, 0.0)))


if __name__ == "__main__":
    main()
