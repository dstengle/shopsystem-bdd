---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-116/d1
kind: defect
batch: batch-116
item: b688
date: 2026-11-26
---

# batch-116 d1

The readiness bar reads the lexicon after the lay against the pack kinds read before it (readiness_bar._laid computes outer = spec_rgl_vocab.outer(copy) once, before backlog_lines.lay_onto), so an item that imports a pack and retires the entries of the pack's nouns gets 'Kind of: text is not a kind' for every term of those kinds. Reproduce: shop work ready b618 (about 200 v_t4/v_t13 reasons); with outer read again after the lay it passes.
