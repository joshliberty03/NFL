# Usage: python3 merge.py ARTIFACT.html GITHUB.html OUT.html
# Keeps the artifact's page shell, swaps in GitHub's fresh data (__ZD blob + TI line).
import re,sys,json,gzip,base64
art,gh,out=sys.argv[1:4]
A=open(art).read(); G=open(gh).read()
zd=re.compile(r'const __ZD=\{.*?\};',re.S)
ti=re.compile(r'const TI=[^\n]*')
ga,gg=zd.search(A),zd.search(G); ta,tg=ti.search(A),ti.search(G)
assert ga and gg and ta and tg, "markers missing"
def keys(m): return sorted(json.loads(m.group(0)[len('const __ZD='):-1]))
assert keys(ga)==keys(gg), ("data keys differ",keys(ga),keys(gg))
B=lambda s:int(re.search(r'BUILT=(\d+)',s).group(1))
print("artifact built",B(A),"github built",B(G))
if B(G)<=B(A): print("NOTHING_NEW"); sys.exit(3)
Z=json.loads(gg.group(0)[len('const __ZD='):-1])
c=json.loads(gzip.decompress(base64.b64decode(Z['__BETTING__'])))['coaches']
fix={'BUF':'Joe Brady','ARI':'Mike LaFleur','ATL':'Kevin Stefanski'}
for t,n in fix.items(): assert c[t]['name']==n, ("coach reverted",t,c[t]['name'])
o=A[:ga.start()]+gg.group(0)+A[ga.end():]
o=ti.sub(lambda m:tg.group(0),o,count=1)
open(out,'w').write(o); print("wrote",out,len(o))
