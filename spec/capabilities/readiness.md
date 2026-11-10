---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/readiness
title: Readiness
narrator: a person or session readying an item
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r13, r14]
---

# Readiness

## Purpose
The questions move to the front (design goal 3): an item becomes `ready` only when it passes a mechanical bar, so
that nothing asks the person while it is built. Its requirement lines parse in the context's grammar, `model logic`
finds no L0 or L1 with them laid over `spec/`, `features generate` writes their scenarios, and every request line of
the item is settled. `work ready` checks the bar and asks nobody.

## Terms
- **relation row** (noun): a row of the `## Relations` table of a capability: from, word, to and cardinality. Kind of: text.
- **upstream entry** (noun): a bullet of the `## Upstreams` of `spec/index.md`: the id of a bounded context and the GitHub repository it is hosted on, if any. Kind of: text.
- **given block** (noun): the fenced `given` block of a requirement group, the example data its scenario starts from. Kind of: text.
- **malformed** (adjective of relation row): a relation row that is not four cells of a `## Relations` table, or whose from or to is no kind of the lexicon.
- **malformed** (adjective of upstream entry): an upstream entry that does not start with a bounded-context id, or whose `github:` is not `<owner>/<name>`.
- **malformed** (adjective of given block): a given block that is not example data in the form `spec_read_given` reads.

- **unworded** (adjective of item): an item one of whose groups `features generate` writes as a scenario holding a step with a bracketed placeholder, a fact no step words.

- **nonexistent** (adjective of requirement): a requirement named by an id that no capability holds as a live requirement.

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

### [g5] `work line --relation` writes a relation row onto an item
- [r5] Where `--relation` is given, when the person runs `work line` on an item, `work` shall write a relation row and commit the item.

### [g6] `work line --relation` refuses a malformed relation row
- [r6] Where `--relation` is given, if the person runs `work line` on a relation row that is malformed, then `work` shall exit with an error naming the relation row and change nothing.

### [g7] `work line --universal` writes a universal condition onto an item
- [r7] Where `--universal` is given, when the person runs `work line` on an item, `work` shall write a universal condition and commit the item.

### [g8] `work line --upstream` writes an upstream entry onto an item
- [r8] Where `--upstream` is given, when the person runs `work line` on an item, `work` shall write an upstream entry and commit the item.

### [g9] `work line --upstream` refuses a malformed upstream entry
- [r9] Where `--upstream` is given, if the person runs `work line` on an upstream entry that is malformed, then `work` shall exit with an error naming the upstream entry and change nothing.

### [g10] `work line --given` writes a given block onto an item
- [r10] Where `--given` is given, when the person runs `work line` on an item, `work` shall write a given block and commit the item.

### [g11] `work line --given` refuses a malformed given block
- [r11] Where `--given` is given, if the person runs `work line` on a given block that is malformed, then `work` shall exit with an error naming the given block and change nothing.

### [g12] `work ready` refuses an item with an unworded step
- [r12] While an item is `shaped` and the item is unworded, if the person runs `work ready` on the item, then `work` shall exit with an error naming the step.

### [g13] A line that retires another
- [r13] Where `--retires` is given, when the person runs `work line` on an item, `work` shall write a requirement and commit the item.

### [g14] A retired id that no capability holds
- [r14] Where `--retires` is given, if the person runs `work line` on a requirement that is nonexistent, then `work` shall exit with an error naming the requirement and change nothing.

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
