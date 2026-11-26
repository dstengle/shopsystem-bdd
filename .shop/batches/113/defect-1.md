---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-113/d1
kind: defect
batch: batch-113
item: b672
date: 2026-11-26
---

# batch-113 d1

The readiness bar refuses an item whose Requirements hold only an import and retirements ('it has no requirement line'): readiness_bar.well_formed counts moves and adapters but not blocks.imports nor blocks.retirements. Reproduce: work ready b618.
