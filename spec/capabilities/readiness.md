---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/readiness
title: Readiness
narrator: a person or session readying an item
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4]
---

# Readiness

## Purpose
The questions move to the front (design goal 3): an item becomes `ready` only when it passes a mechanical bar, so
that nothing asks the person while it is built. Its requirement lines parse in the context's grammar, `model logic`
finds no L0 or L1 with them laid over `spec/`, `features generate` writes their scenarios, and every request line of
the item is settled. `work ready` checks the bar and asks nobody.

## Behaviour

### [g1] `work ready` readies a passing item
- [r1] While an item is `shaped` and the item is passing, when the person runs `work ready` on the item, `work` shall
  set the status of the item to `ready`.

### [g2] `work ready` refuses an item that is not passing
- [r2] While an item is `shaped` and the item is not passing, if the person runs `work ready` on the item, then
  `work` shall exit with an error naming the reason and change nothing.

### [g3] `work ready` refuses an item that is not shaped
- [r3] If the person runs `work ready` on an item that is not `shaped`, then `work` shall exit with an error naming
  the status of the item and change nothing.

### [g4] `work ready` asks no question
- [r4] When the person runs `work ready` on an item, `work` shall not ask a question.
