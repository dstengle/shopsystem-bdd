p = "features/supervision.feature"
d = open(".shop/scratch/4-formulate/drafts/round-1/supervision.feature").read()
d = "\n".join(l for l in d.split("\n") if not l.lstrip().startswith("# [r")).strip("\n") + "\n\n"
s = open(p).read()
k = "  @r130\n"
assert s.count(k) == 1
open(p, "w").write(s.replace(k, d + k))
