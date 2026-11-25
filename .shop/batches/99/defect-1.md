---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-99/d1
kind: defect
batch: batch-99
item: b607
date: 2026-11-25
---

# batch-99 d1

work ready refuses an item whose only lines are moves (work line --move-model, --move-term) with 'it has no requirement line': readiness_bar.well_formed counts lines, universal conditions, retirements and adapter blocks but not blocks.moves. Reproduce: an item with only a --move-model line, then work ready b<n>.
