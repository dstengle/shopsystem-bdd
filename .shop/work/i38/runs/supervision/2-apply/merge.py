import re
live = 'spec/capabilities/supervision.md'
draft = '.shop/work/i38/runs/i38/1-integrate/drafts/round-1/spec/capabilities/supervision.md'
pat = re.compile(r'^- \[r(\d+)\]')
d = {}
for l in open(draft).read().split('\n'):
    m = pat.match(l)
    if m:
        d[int(m.group(1))] = l
removed = {3, 5, 16, 112, 113}
out = []
liveids = set()
for l in open(live).read().split('\n'):
    m = pat.match(l)
    if l.startswith('retired: []'):
        l = 'retired: [r3, r5, r16, r112, r113]'
    if m:
        n = int(m.group(1))
        liveids.add(n)
        if n in removed:
            continue
        l = d.get(n, l)
    out.append(l)
    if m and n == 111:
        out += [d[i] for i in range(128, 134)]
    if m and n == 100:
        out.append("- [r134] **When** a round of the kind `intake` that `work run` started gives a question, `work run` shall leave the request's status as `work turn` writes it.")
t = '\n'.join(out)
t = t.replace('Retries, continuations after `PARTIAL`, refused', 'Retries, refused')
open(live, 'w').write(t)
print(sorted(set(d) - liveids))
