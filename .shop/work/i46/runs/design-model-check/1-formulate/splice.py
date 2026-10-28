p = 'features/design-model-check.feature'
d = '.shop/scratch/drafts/2026-10-28-design-model-check/round-1/design-model-check.feature'
s = open(p).read()
new = open(d).read().split('\n', 4)[4]
lines = [l for l in new.split('\n') if not l.startswith('  # r12')]
new = '\n'.join(lines).strip('\n') + '\n\n'
i = s.index('  @r110\n')
open(p, 'w').write(s[:i] + new + s[i:])
