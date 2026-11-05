---
id: capability/example.org/fixture/work-queue
title: Work queue
narrator: the person
group: service
language: codified-1
rests_on: []
retired: []
---

# Work queue

## Purpose
The queue's command, for the generation tests.

## Behaviour

### [g1] `work start` starts a proposed initiative
- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`.
- [r2] When the person runs `work start` on an initiative that is `proposed`, `work` shall exit successfully.

```given
an initiative i1 that is `proposed`
```

### [g2] `work start` refuses an initiative that is not proposed
- [r3] If the person runs `work start` on an initiative that is not `proposed`, then `work` shall exit with an error naming the status of the initiative.

### [g3] `work list` prints the open work-items
- [r4] When the person runs `work list`, `work` shall print every work-item whose status is not `green` or `withdrawn`.

```given
the file `spec/index.md` holds:
  | term | category |
  | initiative | kind |
the file `notes.md` holds:
  The first line.
  The second line.
```

## Not yet
## Dropped
