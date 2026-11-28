---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-181/d1
kind: defect
batch: batch-181
item: b898
date: 2026-11-28
---

# batch-181 d1

After an item retires an area, the lay takes area: out of each capability of the area, but every reader falls back to the capability's file stem when area: is missing (backlog_retire_area.capabilities, spec_composition.held, domain_model, adapter_uses, spec_vocabulary), so a capability whose file name is the retired area's name is still read as in that area, against applying#r50. Repro: work line b899 --retire-area laying, apply b899; spec/capabilities/laying.md keeps no area: yet capabilities(root, 'laying') and spec_composition.held still give it area laying.
