d = open('.shop/scratch/3-formulate/drafts/round-1/supervision.feature').read().splitlines()
new = "\n".join(l for l in d if not l.lstrip().startswith("#")).strip("\n") + "\n\n"
p = 'features/supervision.feature'
s = open(p).read()
m = "  @r74\n  Scenario: a kept branch"
assert s.count(m) == 1
open(p, 'w').write(s.replace(m, new + m))
