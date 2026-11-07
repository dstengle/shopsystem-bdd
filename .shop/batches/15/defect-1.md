---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-15/d1
kind: defect
batch: batch-15
item: b84
date: 2026-11-07
---

# batch-15 d1

features generate writes no scenario for a negated response with a recipient ('`feed` shall not return the video to the caller'), so its group has none and model check reports v_s3 (reported from a consumer on plugin 3.0.0, its g2 r6). Cause: spec_steps.then() words a recipient pair only when positive (SDoesTo), and spec_typed_verbs generates e__SDoesTo but no negated form, so a negated pair falls to SDoesNot with the pair as one object, which no step fun takes. Reproduce: a verb whose Frame: has a recipient, a line '<actor> shall not <verb> the <object> to the <recipient>.', features generate: no scenario for its group.
