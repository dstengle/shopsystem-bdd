p = 'features/design-model-check.feature'
d = '.shop/scratch/drafts/2026-10-28-design-model-check/round-2/design-model-check.feature'
s = open(p).read()
new = ''.join(l + '\n' for l in open(d).read().split('\n') if not l.startswith('  # ')).strip('\n') + '\n\n'
i = s.index('  @r24\n  Scenario Outline: a frontmatter reference')
open(p, 'w').write(s[:i] + new + s[i:])
