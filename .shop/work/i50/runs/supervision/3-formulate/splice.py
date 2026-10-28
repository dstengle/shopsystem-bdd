p = 'features/supervision.feature'
L = open(p).read().split('\n')
frag = open('.shop/scratch/3-formulate/drafts/supervision.fragment.feature').read().rstrip('\n').split('\n')
if frag[0].strip().startswith('# [r173]'):
    frag = frag[1:]
i = next(k for k, l in enumerate(L) if l.strip() == '@r117')
j = next(k for k in range(i + 1, len(L)) if L[k].strip().startswith('@r'))
L[j:j] = frag + ['']
open(p, 'w').write('\n'.join(L))
