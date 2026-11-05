---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/readiness
title: Readiness
narrator: a person or session readying an item
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: []
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

## Implementation, may change
- An item's requirement lines stay on the item until its batch merges: in the item file's `## Requirements`, one
  `### <capability>` block for each codified capability they go into, term bullets first, then `#### [g<n>]` groups of
  `- [r<n>]` lines, each id the next free in its capability. `work line <item> --into <capability>` writes one line
  (`--term` a term bullet) and parses nothing: `work ready` is the check.
- The bar is checked on a copy of `spec/` under the temporary directory with the item's lines laid in, removed
  afterwards; `spec/` is never written. `model logic` refuses an L0, and an L1 naming one of the item's lines; an L1
  elsewhere in `spec/` is not the item's, and an L3 naming the item's line is printed as a warning and does not refuse.
- An item with no requirement line is not passing: the reason says to give it one with `work line`.
- `work ready` names every reason at once, one a line after `work ready: <item> is not passing:`: the request lines
  not settled first, then the lines that do not parse, the logic findings and the groups with no scenario. An item that
  is not `shaped` is refused first, naming its status, with no check run.
- `features generate` is run only on a `service` capability: each of the item's groups comes out as a scenario unless
  it is logic-only, and a group with a fact no step words is a reason. A `guarantees` capability has no scenarios.
- Each `check` design-decision that a capability of the item's lines rests on (`rests_on:`, matched by the id's last
  segment) runs its tests on the root checkout, as `model decisions --check` runs them, once a process: a failing one is
  the reason `design-decision <slug> (check) fails: <tests>: exit <code>` (or `names no test`), after the well-formed
  reasons. A decision no capability of the item rests on is not run (decision-tiers; plan 6, D13).

## Not yet
- A new capability, and a term for the glossary of `spec/index.md`, proposed by an item: its lines go only into a
  capability that has a codified file, and a term they need into that capability's own `## Terms`.
- The bar checked again when a batch picks the item, against `main` as it then stands and with the batch's other items
  laid in: waits for plan 4, which builds `batches`.
