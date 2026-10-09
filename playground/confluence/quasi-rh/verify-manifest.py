"""Every package Lake resolved in the minimal project must appear in the repo's lake-manifest.json
with the SAME url and rev. Any difference is a pin that was not reproduced: exit 1."""
import json
import sys

mine = {p["name"]: p for p in json.load(open(sys.argv[1]))["packages"]}
repo = {p["name"]: p for p in json.load(open(sys.argv[2]))["packages"]}
bad = 0
for name, p in sorted(mine.items()):
    r = repo.get(name)
    if r is None:
        print(f"MISMATCH {name}: resolved rev {p.get('rev')} but absent from repo manifest"); bad += 1
    elif (p.get("rev"), p.get("url")) != (r.get("rev"), r.get("url")):
        print(f"MISMATCH {name}: resolved {p.get('url')}@{p.get('rev')} vs repo {r.get('url')}@{r.get('rev')}"); bad += 1
    else:
        print(f"ok {name} {p.get('rev')} {p.get('url')}")
print(f"{len(mine)} resolved package(s), {bad} mismatch(es)")
sys.exit(1 if bad else 0)
