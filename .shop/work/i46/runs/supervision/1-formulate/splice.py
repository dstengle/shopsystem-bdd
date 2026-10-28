import re
draft = open('.shop/scratch/drafts/2026-10-28-supervision/round-1/supervision.feature').read()
blocks = {}
for b in re.split(r'\n\n(?=  # r)', draft.strip('\n')):
    lines = [l for l in b.split('\n') if not l.startswith('  # r')]
    m = re.match(r'  @r(\d+)', lines[0])
    blocks[m.group(1)] = '\n'.join(lines).rstrip('\n') + '\n'
place = {
    '68': ['159'],
    '108': ['164', '168', '170', '169', '165', '166', '167'],
    '109': ['161'],
    '78': ['163', '162'],
}
path = 'features/supervision.feature'
src = open(path).read().split('\n')
out = []
for i, l in enumerate(src):
    m = re.match(r'  @r(\d+)\b', l)
    if m and m.group(1) in place and not (i > 0 and src[i - 1].startswith('  @')):
        for r in place[m.group(1)]:
            out.extend(blocks[r].split('\n')[:-1] + [''])
    out.append(l)
open(path, 'w').write('\n'.join(out))
