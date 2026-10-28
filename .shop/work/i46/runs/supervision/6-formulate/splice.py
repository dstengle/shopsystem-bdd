import re
draft = open('.shop/scratch/6-formulate/drafts/supervision.feature').read()
blocks = {}
for b in re.split(r'\n\n(?=  # r)', draft.strip('\n')):
    lines = [l for l in b.split('\n') if not l.startswith('  # r')]
    blocks[re.match(r'  @r(\d+)', lines[0]).group(1)] = '\n'.join(lines).rstrip('\n')
place = {'68': '171', '166': '172'}
path = 'features/supervision.feature'
src = open(path).read().split('\n')
out = []
for i, l in enumerate(src):
    m = re.match(r'  @r(\d+)\b', l)
    if m and m.group(1) in place and not src[i-1].startswith('  @'):
        out.extend(blocks[place[m.group(1)]].split('\n') + [''])
    out.append(l)
open(path, 'w').write('\n'.join(out))
