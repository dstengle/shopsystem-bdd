import re
d=open('.shop/scratch/3-formulate/drafts/round-2/supervision.feature').read().split('\n')
blocks={};cur=None
for l in d[3:]:
    if l.startswith('  # r'): continue
    m=re.match(r'  @(r\d+)$',l)
    if m: cur=m.group(1); blocks[cur]=[l]; continue
    if cur: blocks[cur].append(l)
for k in blocks:
    b=blocks[k]
    while b and not b[-1].strip(): b.pop()
    blocks[k]='\n'.join(b)+'\n\n'
f=open('features/supervision.feature').read()
def before(tag,text):
    global f
    i=f.index('  @'+tag+'\n'); f=f[:i]+text+f[i:]
before('r95',blocks['r111']); before('r80',blocks['r116']); before('r71',blocks['r114'])
before('r81',blocks['r115'])
before('r86',blocks['r83']+blocks['r112']+blocks['r113'])
open('features/supervision.feature','w').write(f)
