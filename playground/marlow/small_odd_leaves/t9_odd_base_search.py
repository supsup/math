import sys,time,collections,random
sys.path.insert(0,'/tmp/t9_ortools')
from ortools.sat.python import cp_model

def solve(m,limit=60,seed=1):
 k=(m-9)//2; C=4+k
 singleton={h:h if h<9 else (h-9)//2 for h in range(m)}
 lengths=[8]*k+[9]*4
 omitted=list(range(k))+[None]*4
 M=cp_model.CpModel()
 x={}
 z={}
 for c in range(C):
  for h in range(m):
   z[c,h]=M.NewBoolVar('z_%d_%d'%(c,h))
   for l in range(9):
    if l!=omitted[c] and singleton[h]!=l:
     x[c,h,l]=M.NewBoolVar('x_%d_%d_%d'%(c,h,l))
   M.Add(sum(x.get((c,h,l),0) for l in range(9))==2*z[c,h])
  M.Add(sum(z[c,h] for h in range(m))==lengths[c])
  for l in range(9):
   M.Add(sum(x.get((c,h,l),0) for h in range(m))==(0 if l==omitted[c] else 2))
 for h in range(m):
  M.Add(sum(z[c,h] for c in range(C))==4)
  for l in range(9):
   M.Add(sum(x.get((c,h,l),0) for c in range(C))==(0 if l==singleton[h] else 1))
 # Break cycle symmetry among 9-cycles by sorting hub 0 appearances.
 for c in range(k,C-1):
  M.Add(z[c,0]>=z[c+1,0])
 start=time.monotonic(); rounds=0
 while time.monotonic()-start<limit:
  S=cp_model.CpSolver();S.parameters.max_time_in_seconds=max(1,limit-(time.monotonic()-start));S.parameters.num_search_workers=8;S.parameters.random_seed=seed+rounds
  status=S.Solve(M)
  if status not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
   print('status',S.StatusName(status),'m',m,'round',rounds,'time',time.monotonic()-start,flush=True);return
  cuts=0; rows=[]
  for c in range(C):
   ed={(h,l) for h in range(m) for l in range(9) if (c,h,l) in x and S.Value(x[c,h,l])}
   unseen=set(ed); comps=[]
   while unseen:
    h,l=next(iter(unseen));hh={h};ll={l}; todo=[('h',h),('l',l)]
    while todo:
     t,v=todo.pop()
     if t=='h':
      for a,b in ed:
       if a==v and b not in ll:ll.add(b);todo.append(('l',b))
     else:
      for a,b in ed:
       if b==v and a not in hh:hh.add(a);todo.append(('h',a))
    ce={(a,b) for a,b in ed if a in hh and b in ll};unseen-=ce;comps.append((hh,ll))
   if len(comps)>1:
    for hh,ll in comps:
     M.Add(sum(x.get((c,h,l),0) for h in hh for l in ll)<=2*len(hh)-1)
     cuts+=1
   rows.append(ed)
  if not cuts:
   print('FOUND',m,'rounds',rounds,'time',time.monotonic()-start,flush=True)
   for c,ed in enumerate(rows):
    # leaf-> two hubs, trace alternating cycle
    by_l=collections.defaultdict(list);by_h=collections.defaultdict(list)
    for h,l in ed:by_l[l].append(h);by_h[h].append(l)
    h=min(by_h); l=min(by_h[h]); H=[];L=[]; seen=set()
    for j in range(len(ed)//2):
     H.append(h);L.append(l);seen.add((h,l));h=next(a for a in by_l[l] if a!=h);seen.add((h,l));l=next(a for a in by_h[h] if a!=l)
    assert len(seen)==len(ed) and h==H[0] and l==L[0]
    print(' ',repr((H,L)),flush=True)
   return rows
  rounds+=1
  if rounds%10==0:print('round',rounds,'cuts',cuts,'time',time.monotonic()-start,flush=True)
 print('TIMEOUT',m,rounds,flush=True)
if __name__=='__main__':solve(int(sys.argv[1]),int(sys.argv[2]) if len(sys.argv)>2 else 60)
