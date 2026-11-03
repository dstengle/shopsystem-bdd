---
id: capability/example.org/fixture/e2e/work-queue
title: Work queue
narrator: the person
group: service
language: codified-1
rests_on: []
retired: []
---

# Work queue

## Purpose
The queue's command, a toy for the end-to-end test.

## Behaviour

### [g1] `work start` starts a proposed initiative
- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`.
- [r2] When the person runs `work start` on an initiative that is `proposed`, `work` shall exit successfully.

```given
an initiative i1 that is `proposed`
```

## Not yet
## Dropped
