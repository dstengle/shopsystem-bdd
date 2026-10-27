D = '.shop/work/i41/runs/i41/1-integrate/drafts/round-1/spec/capabilities/supervision.md'
S = 'spec/capabilities/supervision.md'
d = open(D).read().split('\n')
s = open(S).read().split('\n')
si = s.index('## Behaviour')
di = d.index('## Behaviour')
se = next(i for i in range(si + 1, len(s)) if s[i].startswith('## '))
beh = d[di:]
while beh and beh[-1] == '':
    beh.pop()
out = s[:si] + beh + [''] + s[se:]
out = ['retired: [r3, r5, r16, r112, r113, r80, r114, r71]' if l.startswith('retired:') else l for l in out]
open(S, 'w').write('\n'.join(out))
