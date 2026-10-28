d = open('.shop/work/i50/runs/i50/1-integrate/drafts/round-1/spec/capabilities/supervision.md').read()
p = 'spec/capabilities/supervision.md'
s = open(p).read()
a = s.index('## Behaviour\n')
b = s.index('\n## Implementation, may change')
open(p, 'w').write(s[:a] + d.rstrip('\n') + '\n' + s[b:])
