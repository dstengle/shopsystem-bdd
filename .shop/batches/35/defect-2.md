---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-35/d2
kind: defect
batch: batch-35
item: b275
date: 2026-11-16
---

# batch-35 d2

spec_lf_ordered.member takes the first attribute entry whose term is the order's word, not the entry of the member kind: with release (attribute of repository) listed before release (attribute of upgrade step), features generate crashes with StopIteration on '`migrate` shall print every upgrade step, ordered by release, in ascending order'. Reproduce: a capability holding that line, features generate --root on a copy of spec/. Found shaping b285.
