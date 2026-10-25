import re
d = open('.shop/scratch/3-formulate/drafts/round-1/supervision.feature').read()
parts = re.split(r'\n(?=  # r\d+ )', d)
blk = {re.search(r'@(r\d+)', p).group(1): p.rstrip('\n') for p in parts[1:]}


def strip(b):
    return '\n'.join(l for l in b.split('\n') if not l.lstrip().startswith('# r'))


f = open('features/supervision.feature').read()
marker = "\n  @r20\n"
assert f.count(marker) == 1
f = f.replace(marker, "\n" + strip(blk['r19']) + "\n" + marker, 1)
f = f.rstrip('\n') + "\n\n" + strip(blk['r117']) + "\n\n" + strip(blk['r110']) + "\n"
open('features/supervision.feature', 'w').write(f)
