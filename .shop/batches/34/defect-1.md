---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-34/d1
kind: defect
batch: batch-34
item: b274
date: 2026-11-16
---

# batch-34 d1

Reported by the feed product's session on 0.35.0: model logic refuses holds-exactly on a returned object. '`feed` shall return a video list that holds exactly the videos from the channel ... to the caller' gives 'no translation of a negated restriction (not) on an object': the only half (no video not from the channel in the list) has no translation when the object is returned rather than printed. b274's note says each half is an onrel on a response's object.
