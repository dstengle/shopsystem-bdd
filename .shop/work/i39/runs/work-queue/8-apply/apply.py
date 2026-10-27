import re
d = open('.shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/spec/capabilities/work-queue.md').read().split('\n')
s = open('spec/capabilities/work-queue.md').read()
i = d.index('## Behaviour')
beh = '\n'.join(d[i + 1:]).strip('\n')
a = s.index('## Behaviour\n') + len('## Behaviour\n')
b = s.index('\n## Implementation')
s = s[:a] + beh + '\n' + s[b:]
fm = [l for l in d if l.startswith('rests_on:') or l.startswith('retired:')]
s = re.sub(r'^rests_on:.*$', lambda m: fm[0], s, count=1, flags=re.M)
s = re.sub(r'^retired:.*$', lambda m: fm[1], s, count=1, flags=re.M)
s = s.replace('`show --status`', '`list --status`')
open('spec/capabilities/work-queue.md', 'w').write(s)
