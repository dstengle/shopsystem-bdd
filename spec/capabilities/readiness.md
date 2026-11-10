---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/readiness
title: Readiness
narrator: a person or session readying an item
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g33, r33]
unbuilt: []
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
- **readiness bar** (noun): the checks `work ready` makes of an item on a copy of `spec/` with its lines laid in: its request lines settled, its lines parsed, no L0 and no L1 of `model logic` naming them, their scenarios written by `features generate`, and the `check` design-decisions its capabilities rest on passing. This: the readiness bar of the plugin that runs the command. Kind of: thing.
- **bar check** (noun): one check of the readiness bar. Kind of: thing.
- **pass** (verb, state): an item meets every bar check of the readiness bar. Forms: passes, passed. Frame: item passes readiness bar.
- **meet** (verb, state): an item gives a bar check what it asks. Forms: meets, met. Frame: item meets bar check.
- **the relation-row form** (artifact): four cells `| from | word | to | cardinality |` of a `## Relations` table, whose from and to are kinds of the lexicon.
- **the upstream-entry form** (artifact): a bounded-context id `bounded-context/<path>` and, after `github:`, `<owner>/<name>`.
- **the example-data form** (artifact): the rows of a given block, one a line: a thing with its code, a thing's attribute with its value, or two things related by a word of a relation row, as design-r2 section 9.1 sets them out.
- **requirement id** (noun): the id `<capability>#r<n>` of a requirement. Kind of: text.
- **universal condition id** (noun): the id `U<n>` of a universal condition. Kind of: text.
- **nonexistent** (adjective of requirement): a requirement named by an id that no capability holds as a live requirement.
- **`universal`** (proper noun): `spec/universal.md`, the file of the universal conditions, read as the capability named `universal`. Kind of: capability.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| bar check | of | readiness bar |  |
| relation row | in | item |  |
| universal condition | in | item |  |
| upstream entry | in | item |  |
| given block | in | item |  |
| requirement | in | item |  |
| capability | in | item |  |
| term | in | item |  |
| step | of | scenario |  |
| requirement id | of | requirement | one |
| universal condition id | of | universal condition | one |

## Behaviour

### [g23] `work ready` readies a shaped item that passes the readiness bar
- [r23] While an item is `shaped` and the item passes the readiness bar, when the person runs `work ready` on the item, `work` shall set the status of the item to `ready`.

### [g24] `work ready` refuses an item that does not pass the readiness bar, naming each bar check it does not meet
- [r24] While an item is `shaped` and the item does not pass the readiness bar, if the person runs `work ready` on the item, then `work` shall refuse the command and name every bar check of the readiness bar that the item does not meet.

### [g25] `work ready` refuses an item that is not shaped
- [r25] While an item is not `shaped`, if the person runs `work ready` on the item, then `work` shall refuse the command and name the status of the item.

### [g4] `work ready` asks no question
- [r4] When the person runs `work ready` on an item, `work` shall not ask a question.

### [g26] `work line --relation` writes a relation row in an item
- [r26] When the person runs `work line` with the `--relation` option set to a relation row on an item, `work` shall write the relation row in the item and commit the item.

### [g27] `work line --relation` refuses a relation row that does not conform to the relation-row form
- [r27] If the person runs `work line` with the `--relation` option set to a relation row that does not conform to the relation-row form, then `work` shall refuse the command and name the relation row.

### [g28] `work line --universal` writes a universal condition in an item
- [r28] When the person runs `work line` with the `--universal` option set to a universal condition on an item, `work` shall write the universal condition in the item and commit the item.

### [g29] `work line --upstream` writes an upstream entry in an item
- [r29] When the person runs `work line` with the `--upstream` option set to an upstream entry on an item, `work` shall write the upstream entry in the item and commit the item.

### [g30] `work line --upstream` refuses an upstream entry that does not conform to the upstream-entry form
- [r30] If the person runs `work line` with the `--upstream` option set to an upstream entry that does not conform to the upstream-entry form, then `work` shall refuse the command and name the upstream entry.

### [g31] `work line --given` writes a given block in an item
- [r31] When the person runs `work line` with the `--given` option set to a given block on an item, `work` shall write the given block in the item and commit the item.

### [g32] `work line --given` refuses a given block that does not conform to the example-data form
- [r32] If the person runs `work line` with the `--given` option set to a given block that does not conform to the example-data form, then `work` shall refuse the command and name the given block.

### [g34] `work line --retires` writes a requirement in an item
- [r34] When the person runs `work line` with the `--retires` option on an item, `work` shall write a requirement in the item and commit the item.

### [g35] `work line --retires` refuses a requirement id that no requirement has
- [r35] If the person runs `work line` with the `--retires` option set to a requirement id that no requirement has, then `work` shall refuse the command and name the requirement id.

### [g36] `work ready` refuses an item a term of which violates a rule
- [r36] While an item is `shaped` and a term in the item violates a rule, if the person runs `work ready` on the item, then `work` shall refuse the command and name the term and the rule.

### [g37] `work line --recodify` sets the language of a capability in an item
- [r37] When the person runs `work line` with the `--recodify` option set to a capability on an item, `work` shall set the language of the capability in the item to `codified-2` and commit the item.

### [g38] `work line --recodify universal` sets the language of the universal conditions in an item
- [r38] When the person runs `work line` with the `--recodify` option set to `universal` on an item, `work` shall set the language of the capability in the item to `codified-2` and commit the item.

### [g39] `work line --universal --retires` writes a universal condition in an item
- [r39] When the person runs `work line` with the `--universal` and `--retires` options on an item, `work` shall write a universal condition in the item and commit the item.

### [g40] `work line --universal --retires` refuses a universal condition id that no universal condition has
- [r40] If the person runs `work line` with the `--universal` option and the `--retires` option set to a universal condition id that no universal condition has, then `work` shall refuse the command and name the universal condition id.

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
