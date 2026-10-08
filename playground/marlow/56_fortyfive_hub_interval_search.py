"""Search a connected-cycle interval certificate for one 45-hub odd base.

Requires OR-Tools CP-SAT. Example:
  python3 playground/marlow/56_fortyfive_hub_interval_search.py 45 87 300 42
Prints status and, if feasible, a JSON raw-edge certificate. The saved walks
in the companion JSON are independently verifiable without OR-Tools.
"""

import json
import sys
from ortools.sat.python import cp_model

h, t, limit, seed = map(int, sys.argv[1:5])
k, j = (h-1)//2, (t-h)//2
r = k+j
assert h == 45 and 1 <= j <= k-1
S = [a for a in range(j) for _ in range(3)] + list(range(j,h))
assert len(S) == t
model = cp_model.CpModel()
edge_terms = {}
all_arcs = []
pointer = 0
for c in range(r):
    missing = {(pointer+i)%t for i in range(2*j+(c>=k))}
    pointer += len(missing)
    anchor = 0 if c<k else (1 if c==k else 0)
    arcs = []
    for a in range(h):
        if c>=k and a==c-k:
            arcs.append((a,a,model.NewConstant(1)))
    for b in range(t):
        if b in missing:
            arcs.append((h+b,h+b,model.NewConstant(1)))
    out_terms, in_terms = [], []
    for a in range(h):
        if c>=k and a==c-k:
            continue
        for b in range(t):
            if b in missing or S[b]==a:
                continue
            fwd = model.NewBoolVar(f'{c}_{a}_{b}_f')
            back = model.NewBoolVar(f'{c}_{a}_{b}_b')
            arcs.extend(((a,h+b,fwd),(h+b,a,back)))
            edge_terms.setdefault((a,b),[]).extend((fwd,back))
            if a == anchor:
                out_terms.append(b*fwd)
                in_terms.append(b*back)
    model.AddCircuit(arcs)
    model.Add(sum(out_terms)<sum(in_terms))
    all_arcs.append(arcs)
assert pointer == j*t
for a in range(h):
    for b in range(t):
        if S[b]!=a:
            model.Add(sum(edge_terms[a,b])==1)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = limit
solver.parameters.num_search_workers = 8
solver.parameters.random_seed = seed
status = solver.Solve(model)
print('status',solver.StatusName(status),'time',solver.WallTime(),'seed',seed,flush=True)
if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    witness = []
    for arcs in all_arcs:
        edges = set()
        for u,v,lit in arcs:
            if u!=v and solver.Value(lit):
                edges.add((min(u,v),max(u,v)-h))
        witness.append(sorted(map(list,edges)))
    print(json.dumps({'h':h,'t':t,'singleton_spokes':[[S[b],b] for b in range(t)],'cycle_edges':witness}),flush=True)
