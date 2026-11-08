---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-13/d1
kind: defect
batch: batch-13
item: b82
date: 2026-11-08
---

# batch-13 d1

v_t11 reports a prepositional verb as having no Frame: although its entry has one ('Frame: viewer subscribes to channel.', 'Frame: caller asks for video list.'), reported from feed on 3.0.0 (2026-11-08 upgrade report, finding 4). spec_frames.frame takes the words after the verb form ('to channel') as the object and finds no kind, so it returns None; the verb-frames design's own example is 'Frame: user subscribes to channel.' (a prepositional verb: the preposition is part of the verb). Reproduce: a verb entry 'subscribe (verb) ... Frame: viewer subscribes to channel.' with kinds viewer and channel; model check prints v_t11 subscribe.
