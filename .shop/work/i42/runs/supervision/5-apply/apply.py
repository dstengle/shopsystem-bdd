import re
d=open('.shop/work/i42/runs/supervision/3-integrate/drafts/round-1/spec/capabilities/supervision.md').read()
L={m.group(1):m.group(0) for m in re.finditer(r'^- \[(r\d+)\].*$',d,re.M)}
p='spec/capabilities/supervision.md'
s=open(p).read()
s=s.replace('r114, r71]','r114, r71, r140]',1)
s=re.sub(r'^- \[r140\].*$',lambda m:L['r150']+'\n'+L['r151'],s,flags=re.M)
i=s.index('- [r86]')
s=s[:i]+'\n'.join(L[k] for k in('r149','r152','r153'))+'\n'+s[i:]
open(p,'w').write(s)
