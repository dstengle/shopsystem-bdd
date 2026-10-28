import re

p = 'features/supervision.feature'
t = open(p).read()
d = open('.shop/scratch/6-formulate/drafts/round-1/supervision.feature').read()
blocks = {}
for m in re.finditer(r'  (@r\d+)\n  Scenario:.*?(?=\n  # r|\Z)', d, re.S):
    blocks[m.group(1)] = m.group(0).rstrip() + '\n'


def after(t, anchor, new):
    i = t.index(anchor)
    j = t.index('\n\n  @', i)
    return t[:j + 1] + '\n' + '\n'.join(new) + t[j + 1:]


t = after(t, "followed by a new integrate round for the proposal (deprecated)", [blocks['@r150'], blocks['@r151']])
t = after(t, "the proposal is formulated\n    Pins that a capability-proposal whose lines",
          [blocks['@r149'], blocks['@r152'], blocks['@r153']])
open(p, 'w').write(t)
