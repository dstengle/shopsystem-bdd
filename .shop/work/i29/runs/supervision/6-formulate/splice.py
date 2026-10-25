import re
d = open('.shop/scratch/drafts/i29-supervision/round-1/supervision.feature').read().splitlines()
keep = [l for l in d if not l.startswith('  # r')]
f = open('features/supervision.feature').read().rstrip('\n')
open('features/supervision.feature', 'w').write(f + '\n\n' + '\n'.join(keep).strip('\n') + '\n')
