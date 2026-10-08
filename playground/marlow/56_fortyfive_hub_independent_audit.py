import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
source=root/'56_fortyfive_hub_odd_seeds.json'
seeds=json.loads(source.read_text());h,k=45,22
assert set(seeds)=={str(h+2*j) for j in range(1,k)}


def check(t,singles,cycles,kind,interval=False):
    assert len(singles)==t and len(cycles)==(k*t+h-1)//h
    used=set()
    for a,b in singles:
        assert 0<=a<h and 0<=b<t and (a,b) not in used,(kind,'singleton',a,b)
        used.add((a,b))
    for color,walk in enumerate(cycles):
        H,L=walk['hubs'],walk['leaves']
        assert 2<=len(H)==len(L)<=h
        assert len(set(H))==len(H) and len(set(L))==len(L)
        for i,a in enumerate(H):
            for b in (L[i],L[i-1]):
                assert 0<=a<h and 0<=b<t and (a,b) not in used,(kind,color,a,b)
                used.add((a,b))
    assert used=={(a,b) for a in range(h) for b in range(t)}
    assert len(singles)+len(cycles)==t+(k*t+h-1)//h
    return len(used)

# Every odd JSON witness is independently decoded as an alternating walk.
for t in range(47,88,2):
    j=(t-h)//2; data=seeds[str(t)]
    singles=[tuple(e) for e in data['singleton_spokes']]
    assert singles==[(a,b) for b,a in enumerate([hub for hub in range(j) for _ in range(3)]+list(range(j,h)))]
    cycles=data['cycles'];assert len(cycles)==k+j
    pointer=0
    for c,walk in enumerate(cycles):
        n=h-(c>=k)
        assert len(walk['hubs'])==len(walk['leaves'])==n
        assert set(walk['hubs'])==(set(range(h))-{c-k} if c>=k else set(range(h)))
        missing={(pointer+i)%t for i in range(2*j+(c>=k))};pointer+=len(missing)
        assert set(range(t))-set(walk['leaves'])==missing,(t,c)
    assert pointer==j*t
    check(t,singles,cycles,f'odd t={t}')
print('odd JSON: all 21 walk partitions, interval omissions, singleton degrees, and cycle supports verified')

# Independent even weave (all 23 bases) and square offset base.
def base(b):
    if b%2==0:
        m=b//2
        singles=[(h-1,leaf) for leaf in range(b)]
        cycles=[{'hubs':list(range(h-1)),
                 'leaves':[2*((shift+r)%m)+q for r in range(k) for q in (0,1)]}
                for shift in range(m)]
    elif b==h:
        singles=[(a,a) for a in range(h)]
        cycles=[{'hubs':[(-i)%h for i in range(h)],
                 'leaves':[((-i+d)%h) for i in range(h)]}
                for d in range(1,h,2)]
    else:
        data=seeds[str(b)]
        singles=[tuple(edge) for edge in data['singleton_spokes']]
        cycles=list(data['cycles'])
    return singles,cycles

for b in range(44,89):
    singles,cycles=base(b)
    check(b,singles,cycles,f'base {b}')
print('all 45 base residues independently checked (including 23 even weaves and offset square)')

# Spot-check long offsets; validate the new block itself and exact total coverage.
for b in (44,45,46,47,55,57,87,88):
    for q in (1,3,11):
        singles,cycles=base(b)
        singles=list(singles);cycles=list(cycles)
        for block in range(q):
            start=b+h*block
            singles.extend((a,start+a) for a in range(h))
            cycles.extend({'hubs':[(-i)%h for i in range(h)],
                           'leaves':[start+((-i+d)%h) for i in range(h)]}
                          for d in range(1,h,2))
        check(b+h*q,singles,cycles,f'lift {b}+45*{q}')
print('24 lifted partitions independently checked at q=1,3,11')
print('sha256',hashlib.sha256(source.read_bytes()).hexdigest())
