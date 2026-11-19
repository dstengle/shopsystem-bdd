---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/backlog
title: Backlog
narrator: a person or session keeping the backlog
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g23, r23, g24, r24, g28, r28, g29, r29, g30, r30, g31, r31, g5, r5, g15, r15, g22, r22, g37, r37, g38, r38, g25, r25, g26, r26, g27, r27, g39, r39, g40, r40, g41, r41, g42, r42, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g43, r43, g44, r44]
unbuilt: []
---

# Backlog

## Purpose
`work` keeps the backlog of a bounded context in the repository, so that any session can read or change it: one item
for each piece of work, whatever its provenance, from a raw idea to its delivery (design goals 1 and 2). It writes an
item, shapes it, rates it and records what it depends on, and prints the backlog in rank order with what blocks each
item. Adding an idea starts no work. The person reads an item by its title, not by its id (design goal 10).

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- Each item is the file `.shop/backlog/b<n>.md`, and each change to it is one commit of that file, whose history is
  its log. `work backlog` only reads, and commits nothing.
- An item's score is (value + urgency) / size, with low and small 1, medium 2, and high and large 3. Within a state
  items go by score from high to low, and a tie goes to the item added first (the lower `b<n>`). An item missing a
  rating has no score and ranks after the rated items of its state.
- `work backlog` prints every item, one table a state, in the order `in-batch`, `needs-input`, `ready`, `shaped`,
  `idea`, `delivered`, `refused`, `withdrawn`; a state with no items is left out.
- A row's `waiting on` column names each item it is blocked by, with that item's status, and for an item that is
  `needs-input` the first line of its question.
- An item is blocked by each item it depends on that is not `delivered`, a missing one included (printed `missing`).
  `work batch start` makes the glossary's exception: an item whose dependency it picks earlier in the same pick is
  not blocked there.
- `work depend` refuses a dependency on an item that is `refused` or `withdrawn`, which is never delivered and so
  would block for good (plan 2 rulings, Q1). `work depend <item> --drop <item>` drops a dependency the item has, one
  on an item there is not included; one it does not have is refused.
- For an item that is `in-batch`, the `waiting on` column says how far its batch is along, `in batch-1 (building): 1
  of 2 tasks done`, and `--json` gives its row a `batch` object (`name`, `status`, `tasks_done`, `tasks`); no other
  row has one.
- A command that commits pushes the branch checked out to its upstream remote (else `origin`), never prompting, and
  waits `$SHOPSYSTEM_PUSH_TIMEOUT` seconds (default 60) for the remote's answer: a push the remote rejects, or one it
  does not answer in that time, is printed `not pushed: <remote>: <reason>` and the commit is kept.

## Not yet
- Bugs' risk and likelihood ratings (design goal 2): not built, because the design gives them no part in the rank.
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g5 | items#g11 |
| r5 | items#r11 |
| g15 | items#g12 |
| r15 | items#r12 |
| g22 | items#g13 |
| r22 | items#r13 |
| g37 | items#g14 |
| r37 | items#r14 |
| g38 | items#g15 |
| r38 | items#r15 |
| g25 | items#g16 |
| r25 | items#r16 |
| g26 | items#g17 |
| r26 | items#r17 |
| g27 | dropped |
| r27 | dropped |
| g39 | items#g18 |
| r39 | items#r18 |
| g40 | items#g19 |
| r40 | items#r19 |
| g41 | items#g20 |
| r41 | items#r20 |
| g42 | items#g21 |
| r42 | items#r21 |
| g32 | items#g22 |
| r32 | items#r22 |
| g33 | items#g23 |
| r33 | items#r23 |
| g34 | items#g24 |
| r34 | items#r24 |
| g35 | items#g25 |
| r35 | items#r25 |
| g36 | items#g26 |
| r36 | items#r26 |
| g43 | items#g27 |
| r43 | items#r27 |
| g44 | items#g28 |
| r44 | items#r28 |
