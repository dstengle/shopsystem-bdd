import re, glob, os
D = '.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/'
for f in sorted(glob.glob(D + '*.md')):
    n = os.path.basename(f)
    old = open('spec/capabilities/' + n).read()
    new = open(f).read()
    ids = lambda t: dict((m.group(1), m.group(2)) for m in re.finditer(r'^- \[r(\d+)\] (.*)$', t, re.M))
    o, w = ids(old), ids(new)
    ret = re.findall(r'retired: \[(.*?)\]', old)
    allold = [int(x) for x in o] + ([int(x) for x in re.findall(r'\d+', ret[0])] if ret else [])
    print(n, 'added', sorted(int(k) for k in w if k not in o), 'removed', sorted(int(k) for k in o if k not in w),
          'changed', [k for k in w if k in o and w[k] != o[k]], 'maxold', max(allold))
    nr = re.findall(r'retired: \[(.*?)\]', new)
    print('  retired', nr)
