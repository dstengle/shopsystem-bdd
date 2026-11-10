---
id: capability/example.org/fixture/work-queue
title: Work queue
narrator: the person
group: service
language: codified-2
rests_on: []
retired: []
---

# Work queue

## Purpose
The queue's command, for the generation tests.

## Behaviour

### [g1] `work start` starts a proposed initiative
- [r1] While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to `started`.
- [r2] While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall exit successfully.

```given
an initiative i1 that is `proposed`
```

### [g2] `work start` refuses an initiative that is not proposed
- [r3] While an initiative is not `proposed`, if the person runs `work start` on the initiative, then `work` shall exit with an error naming the status of the initiative.

### [g3] `work list` prints the open work-items
- [r4] When the person runs `work list`, `work` shall print every work-item whose status is not `green`.

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
