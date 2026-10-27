W=/home/vscode/shopsystem-bdd/.shop/worktrees/i39-1-integrate
D=$W/.shop/scratch/1-integrate/drafts/round-1/spec
sec() { awk -v s="$2" '$0 ~ "^## "s {f=1;next} /^## /{f=0} f' "$1"; }
for c in requests supervision work-queue spec-integration design-model-check; do
  echo "== $c"
  diff <(sec $W/spec/capabilities/$c.md Behaviour) <(sec $D/capabilities/$c.md Behaviour) | cut -c1-80
done
echo "== glossary"
diff <(sec $W/spec/index.md Glossary) <(sec $D/index.md Glossary) | cut -c1-140
echo "== requests implementation"
diff <(sec $W/spec/capabilities/requests.md Implementation) <(sec $D/capabilities/requests.md Implementation) | cut -c1-120
head -9 $D/capabilities/requests.md
