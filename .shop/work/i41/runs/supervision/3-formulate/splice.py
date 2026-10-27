d = open('.shop/scratch/drafts/3-formulate-supervision/round-1/features/supervision.feature').read().splitlines()
d = [l for l in d if not l.startswith('# r')]
while d and d[-1] == '':
    d.pop()
f = open('features/supervision.feature').read().split('\n')
i = f.index('  @r80 @deprecated')
open('features/supervision.feature', 'w').write('\n'.join(f[:i] + d + [''] + f[i:]))
