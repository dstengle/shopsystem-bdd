import re
f = 'features/requests.feature'
d = '.shop/scratch/drafts/requests-deda9fa6/round-1/requests.feature'
lines = open(f).read().split('\n')
dr = open(d).read().rstrip('\n').split('\n')
blocks = {}
cur = None
for l in dr:
    m = re.match(r'\s*# formulates \[(r\d+)\]', l)
    if m:
        cur = m.group(1)
        blocks[cur] = []
        continue
    blocks[cur].append(l)
for k in blocks:
    while blocks[k] and blocks[k][-1] == '':
        blocks[k].pop()


def span(tag):
    i = next(n for n, l in enumerate(lines)
             if l.strip().startswith('@' + tag + ' ') or l.strip() == '@' + tag)
    j = i + 1
    while j < len(lines) and not (lines[j].strip().startswith('@') or lines[j].strip().startswith('#')):
        j += 1
    e = j
    while lines[e - 1].strip() == '':
        e -= 1
    return i, e


for tag in ['r43', 'r41', 'r39']:
    i, e = span(tag)
    lines[i:e] = blocks[tag]
i, e = span('r13')
ins = []
for t in ['r50', 'r51', 'r53', 'r54']:
    ins += [''] + blocks[t]
lines[e:e] = ins
i, e = span('r34')
lines[e:e] = [''] + blocks['r55']
open(f, 'w').write('\n'.join(lines))
