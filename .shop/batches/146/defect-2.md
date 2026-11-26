---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-146/d2
kind: defect
batch: batch-146
item: b744
date: 2026-11-26
---

# batch-146 d2

spec coupling resolves an import's module only from the importer's folder or the repository's root, so a file that imports a module by the folder it runs with on its path (a test 'import spec_grammar4', or once areas are packages 'from laying import lay' or 'from plumbing.shop_files import x' in scripts/<area>/) couples nothing, against checking#r147. Reproduce: modules.toml [a] modules=['src/a/*.py'], [b] modules=['src/b/*.py'], src/b/x.py 'import a.y' with src/a/y.py: no coupling of a by b.
