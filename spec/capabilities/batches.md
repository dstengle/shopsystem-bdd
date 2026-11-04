---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches
title: Batches
narrator: a person or session building a batch
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]
---

# Batches

## Purpose
Ready items are built together in batches, like a sprint (design goal 5): a batch takes several ready, unblocked items
in rank order, which may be unrelated, writes its own plan of tasks and builds them on one branch closed by one pull
request. The plan and each task's status are on disk, so a session can stop and any later session carry on. A
question while building parks its item and the rest of the batch carries on. The person merges; the merge delivers.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| commit | of | item | one |
| pull request | with | commit | |

## Behaviour

### [g1] `work batch start` picks ready items
- [r1] While an item is `ready` and the item is passing and the item is not blocked, when the person runs `work batch
  start`, `work` shall write a batch that is `building`, write a batch plan and set the status of the item to
  `in-batch`.

### [g2] A ready item that is no longer passing is returned
- [r2] While an item is `ready` and the item is not passing, when the person runs `work batch start`, `work` shall
  set the status of the item to `shaped`.

### [g3] A blocked item is not picked
- [r3] While an item is `ready` and the item is blocked, when the person runs `work batch start`, `work` shall not set
  the status of the item to `in-batch`.

### [g4] `work batch status` prints where the batch stands
- [r4] When the person runs `work batch status` on a batch, `work` shall print every item in the batch, every task of
  the batch and the status of the task.

### [g5] `work batch resume` carries on without a person
- [r5] While a batch is `building`, when a session runs `work batch resume` on the batch, `work` shall use the batch
  plan, and `work` shall not ask a question.

### [g6] A park leaves the rest building
- [r6] When a batch parks an item that is `in-batch`, `work` shall set the status of the item to `needs-input`, and
  `work` shall not set the status of the batch to `abandoned`.

### [g7] A parked item's commits stay out of the pull request
- [r7] While an item in a batch is `needs-input`, when the person runs `work batch review` on the batch, `work` shall
  publish a pull request of the batch with no commit of the item.

### [g8] `work batch review` publishes the pull request
- [r8] While a batch is `building` and every task of the batch is `done`, when the person runs `work batch review` on
  the batch, `work` shall publish a pull request of the batch and set the status of the batch to `in-review`.

### [g9] The merge delivers
- [r9] While an item in a batch is `in-batch`, when the person merges the pull request of the batch, `work` shall set
  the status of the item to `delivered`.

### [g10] `work batch abandon` returns the batch's items
- [r10] When the person runs `work batch abandon` on a batch that is `building`, `work` shall set the status of the
  batch to `abandoned` and set the status of every item in the batch to `ready`.

## Implementation, may change

- `work batch start` takes the ready items in rank order (the backlog's WSJF, ties to the item added first), up to
  `batch_size` of `.shop/delivery.toml` (a new key, default 4).
- A batch keeps each item's commits apart (one worktree or one commit series an item); a parked item's commits stay on
  its own branch for when it returns.
