---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-35/d1
kind: defect
batch: batch-35
item: b275
date: 2026-11-16
---

# batch-35 d1

value-compare and value-same take one attribute entry on both sides, so two entries of one attribute word do not compare: 'While the release of this repository is after the release of `migrate`, when the SessionStart hook runs `migrate status --hook`, `migrate` shall print `update the plugin`.' does not parse (after 'the release of' only a repository may follow), although b275's note and grammar/language.md's ordered-comparison section say the release of a repository and of a tool (both by number) compare. Reproduce: python3 scripts/model parse on that line. Found shaping b284.
