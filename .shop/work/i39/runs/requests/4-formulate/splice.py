import re
d = open('.shop/scratch/4-formulate/round-1/requests.feature').read().split('\n')
blocks = {}
cur = None
for line in d[3:]:
    m = re.match(r'  # \[(r\d+)\]', line)
    if m:
        cur = m.group(1)
        blocks[cur] = []
    if cur:
        blocks[cur].append(line)
txt = {k: '\n'.join(v).rstrip('\n') + '\n\n' for k, v in blocks.items()}
f = open('features/requests.feature').read()


def before(f, marker, ids):
    i = f.index(marker)
    return f[:i] + ''.join(txt[k] for k in ids) + f[i:]


f = before(f, '  @r4\n', ['r33', 'r34'])
f = before(f, '  @r13\n', ['r39', 'r41', 'r43'])
open('features/requests.feature', 'w').write(f)
