f = 'features/requests.feature'
L = open(f).read().split('\n')
d = open('.shop/scratch/29-formulate/drafts/round-1/requests.feature').read().split('\n')[4:]
while d and d[-1] == '':
    d.pop()
i = L.index('  # formulates [r70] of spec/capabilities/requests.md')
L[i:i] = d + ['']
open(f, 'w').write('\n'.join(L))
