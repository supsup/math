"""Finite UNSAT probe for one rigid four-leaf surgery at p = 1 mod 4.

Run: python3 -I playground/marlow/36_p1_two_page_probe.py
The model is a relaxation of the surgery; UNSAT has a narrow meaning.
See 36_p1_two_page_boundary.md before interpreting results.
"""

import sys,time

def prime_root(p):
 for g in range(2,p):
  if len({pow(g,i,p) for i in range(p-1)})==p-1:return g

def model(p,a=0,b=1):
 g=prime_root(p); k=(p-1)//2
 S=[]
 for cen in (a,b):
  seq=[(cen+pow(g,i,p))%p for i in range(p-1)]
  for i,u in enumerate(seq):
   v=seq[(i+1)%(p-1)];d=min((v-u)%p,(u-v)%p)
   S.append((cen,i,u,v,d))
 groups=[]
 for u in range(p): groups.append([i for i,e in enumerate(S) if u in e[2:4]])
 # The first occurrence of the shared slot is overwritten by the second page.
 shared = [i for i,e in enumerate(S) if sum(1 for f in S if set(e[2:4]) == set(f[2:4])) == 2]
 assert len(shared)==2
 first_shared = next(i for i in shared if S[i][0] == a)
 for d in range(1,k+1):
  G=[i for i,e in enumerate(S) if e[4]==d]
  groups.append([i for i in G if i != first_shared])
 vgroups=[[] for _ in S]
 for G in groups:
  for i in G:vgroups[i].append(G)
 return g,S,groups,vgroups

def solve(p,limit=20):
 g,S,groups,vgroups=model(p);n=len(S); a,b=0,1
 print('p',p,'g',g,'n',n,flush=True)
 # colors 0,1 miss a; 2,3 miss b
 base=[]
 for cen,ix,u,v,d in S:
  m=15
  if u==a or v==a:m&=12
  if u==b or v==b:m&=3
  base.append(m)
 # Symmetry: swap the two new leaves whose singleton hub is a.
 first=next(i for i,e in enumerate(S) if b in e[2:4]);base[first]=1
 ct=0;deadline=time.monotonic()+limit
 def propagate(masks):
  changed=True
  while changed:
   changed=False
   for G in groups:
    used=0
    for i in G:
     m=masks[i]
     if bin(m).count("1")==1:
      if used&m:return None
      used|=m
    for i in G:
     m=masks[i]
     if bin(m).count("1")>1:
      nm=m&~used
      if nm==0:return None
      if nm!=m:masks[i]=nm;changed=True
    # all groups size 2 or 4; for size4 each color must occur
    if len(G)==4:
     for c in (1,2,4,8):
      q=[i for i in G if masks[i]&c]
      if not q:return None
      if len(q)==1 and masks[q[0]]!=c:masks[q[0]]=c;changed=True
  return masks
 def dfs(masks):
  nonlocal ct
  ct+=1
  if ct%100000==0:print('nodes',ct,flush=True)
  if time.monotonic()>deadline:return 'timeout'
  masks=propagate(masks)
  if masks is None:return None
  opts=[(bin(m).count("1"),-len(vgroups[i]),i) for i,m in enumerate(masks) if bin(m).count("1")>1]
  if not opts:return masks
  _,_,i=min(opts)
  for c in (1,2,4,8):
   if masks[i]&c:
    nxt=masks.copy();nxt[i]=c;r=dfs(nxt)
    if r is not None:return r
  return None
 sol=dfs(base)
 print('nodes',ct,'result',str(sol) if sol=='timeout' or sol is None else 'SAT',flush=True)
 if isinstance(sol,list):
  for cen in (a,b):
   print('center',cen,'colors',[sol[i].bit_length()-1 for i,e in enumerate(S) if e[0]==cen])
 return sol

if __name__=='__main__':
 if len(sys.argv)>1:
  for p in map(int,sys.argv[1:]):solve(p,limit=30)
 else:
  for p in (5,13,17,29):
   assert solve(p,limit=30) is None
