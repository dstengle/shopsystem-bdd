D = '.shop/work/i43/runs/i43/1-integrate/drafts/round-1/spec/capabilities/'


def line(d, rid):
    for l in open(D + d + '.md').read().split('\n'):
        if l.startswith('- [%s]' % rid):
            return l
    raise SystemExit(rid)


p = 'spec/capabilities/supervision.md'
L = open(p).read().split('\n')
i = next(k for k, l in enumerate(L) if l.startswith('- [r27]'))
L[i + 1:i + 1] = [line('supervision', 'r%d' % n) for n in (154, 155, 156, 157)]
j = next(k for k, l in enumerate(L) if l.startswith('## Not yet'))
k = j - 1
while L[k] == '':
    k -= 1
L.insert(k + 1, '- r155: how a run exited is given as its exit code.')
open(p, 'w').write('\n'.join(L))

p = 'spec/capabilities/review.md'
L = open(p).read().split('\n')
out = []
for l in L:
    if l.startswith('- [r9]'):
        out.append(line('review', 'r34'))
    else:
        out.append('retired: [r9]' if l == 'retired: []' else l)
        if l.startswith('- [r13]'):
            out.append(line('review', 'r32'))
        if l.startswith('- [r12]'):
            out.append(line('review', 'r33'))
open(p, 'w').write('\n'.join(out))
