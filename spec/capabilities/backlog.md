---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/backlog
title: Backlog
narrator: a person or session keeping the backlog
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r6, r7, r8, r17]
---

# Backlog

## Purpose
`work` keeps the backlog of a bounded context in the repository, so that any session can read or change it: one item
for each piece of work, whatever its provenance, from a raw idea to its delivery (design goals 1 and 2). It writes an
item, shapes it, rates it and records what it depends on, and prints the backlog in rank order with what blocks each
item. Adding an idea starts no work. The person reads an item by its title, not by its id (design goal 10).

## Terms
- **title** (kind): the name of an item that the person reads beside its id.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| title | of | item | one |

## Behaviour

### [g1] `work idea` writes an item
- [r1] When the person runs `work idea`, `work` shall write an item that is `idea` and commit the item.

### [g2] `work shape` shapes an idea
- [r2] When the person runs `work shape` on an item that is `idea`, `work` shall set the status of the item to
  `shaped`.

### [g3] `work shape` refuses an item that is not an idea
- [r3] If the person runs `work shape` on an item that is not `idea`, then `work` shall exit with an error naming the
  status of the item and change nothing.

### [g4] `work rate` sets an item's ratings
- [r4] Where `--value high-value --urgency low-urgency --size small` is given, when the person runs `work rate` on an
  item, `work` shall set the value of the item to `high-value`, set the urgency of the item to `low-urgency`, set the
  size of the item to `small` and commit the item.

### [g5] `work depend` records a dependency
- [r5] When the person runs `work depend` on an item, `work` shall write a dependency of the item and commit the item.

### [g6] `work backlog` prints the backlog, each item by its title
- [r6] When the person runs `work backlog`, `work` shall print every item, the title of the item, the status of the
  item, the provenance of the item, the value of the item, the urgency of the item and the size of the item.

### [g7] `work backlog` marks a blocked item
- [r7] While a dependency is on an item that is not `delivered` and the dependency is of an item that is blocked, when
  the person runs `work backlog`, `work` shall print the item and print the dependency.

### [g8] `work backlog --json` prints one JSON object
- [r8] Where `--json` is given, when the person runs `work backlog`, `work` shall print a JSON object and exit
  successfully.

### [g9] `work withdraw` withdraws an idea
- [r9] When the person runs `work withdraw` on an item that is `idea`, `work` shall set the status of the item to
  `withdrawn`.

### [g10] `work withdraw` withdraws a shaped item
- [r10] When the person runs `work withdraw` on an item that is `shaped`, `work` shall set the status of the item to
  `withdrawn`.

### [g11] `work withdraw` withdraws a ready item
- [r11] When the person runs `work withdraw` on an item that is `ready`, `work` shall set the status of the item to
  `withdrawn`.

### [g12] `work withdraw` withdraws an item that needs input
- [r12] When the person runs `work withdraw` on an item that is `needs-input`, `work` shall set the status of the
  item to `withdrawn`.

### [g13] `work refuse` refuses an idea
- [r13] When the person runs `work refuse` on an item that is `idea`, `work` shall set the status of the item to
  `refused`.

### [g14] `work refuse` refuses a shaped item
- [r14] When the person runs `work refuse` on an item that is `shaped`, `work` shall set the status of the item to
  `refused`.

### [g15] `work show` names an item by its title
- [r15] When the person runs `work show` on an item, `work` shall print the title of the item.

### [g16] `work answer` returns an item that needs input to shaped
- [r16] When the person runs `work answer` on an item that is `needs-input`, `work` shall set the status of the item
  to `shaped` and commit the item.

### [g17] `work backlog` prints the question of an item that needs input
- [r17] While an item is `needs-input`, when the person runs `work backlog`, `work` shall print the item and print the
  question on the item.

## Not yet
- The backlog printed as tables by state, in rank order (the WSJF score, ties to the item added first), and for an
  item in a batch how far the batch is along (design goal 2): the grammar has no order and no grouping of what is
  printed, so these wait for plan 2, which builds `work backlog` and may extend it.
- Bugs' risk and likelihood ratings (design goal 2): the design gives them no part in the rank, so plan 2 decides
  whether they are attributes of an item and what reads them.
