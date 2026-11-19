---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/readiness
title: Readiness
narrator: a person or session readying an item
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g33, r33, g43, r43, g49, r49, g23, r23, g24, r24, g25, r25, g4, r4, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g42, r42, g44, r44, g45, r45, g46, r46, g47, r47, g48, r48, g50, r50, g51, r51, g52, r52, g53, r53, g54, r54, g55, r55, g56, r56, g57, r57, g58, r58]
unbuilt: []
---

# Readiness

## Purpose
The questions move to the front (design goal 3): an item becomes `ready` only when it passes a mechanical bar, so
that nothing asks the person while it is built. Its requirement lines parse in the context's grammar, `model logic`
finds no L0 or L1 with them laid over `spec/`, `features generate` writes their scenarios, and every request line of
the item is settled. `work ready` checks the bar and asks nobody.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change
- An item's requirement lines stay on the item until its batch merges: in the item file's `## Requirements`, one
  `### <capability>` block for each codified capability they go into, term bullets first, then `#### [g<n>]` groups of
  `- [r<n>]` lines, each id the next free in its capability. `work line <item> --into <capability>` writes one line
  (`--term` a term bullet) and parses nothing: `work ready` is the check.
- The bar is checked on a copy of `spec/` under the temporary directory with the item's lines laid in, removed
  afterwards; `spec/` is never written. `model logic` refuses an L0, and an L1 naming one of the item's lines; an L1
  elsewhere in `spec/` is not the item's, and an L3 naming the item's line is printed as a warning and does not refuse.
- An item with no requirement line is not passing, unless it retires a requirement (`work line --no-line --retires`):
  the reason says to give it one with `work line`.
- `work ready` names every reason at once, one a line after `work ready: <item> is not passing:`: the request lines
  not settled first, then the lines that do not parse, the logic findings and the groups with no scenario. An item that
  is not `shaped` is refused first, naming its status, with no check run.
- `features generate` is run only on a `service` capability: each of the item's groups comes out as a scenario unless
  it is logic-only, and a group with a fact no step words is a reason. A `guarantees` capability has no scenarios.
- Each `check` design-decision that a capability of the item's lines rests on (`rests_on:`, matched by the id's last
  segment) runs its tests on the root checkout, as `model decisions --check` runs them, once a process: a failing one is
  the reason `design-decision <slug> (check) fails: <tests>: exit <code>` (or `names no test`), after the well-formed
  reasons. A decision no capability of the item rests on is not run (decision-tiers; plan 6, D13).
- A chore is kept in the item file's `## Chore` section: `Files:` with a `- <path>` bullet for each file or
  directory its work changes, then the line ``Check: `<command>` ``. `work chore` refuses a `--file` under `spec/`,
  `features/` or `.shop/` (requirement lines own the first two, `work` the third), or outside the repository, naming
  it; run again on an item that holds a chore, it replaces the chore (b316).
- An item that holds a chore and requirement lines too, written into its file by hand, is not passing: the reason is
  `it holds a chore and requirement lines, which exclude each other: take one of them out` (b316).

## Not yet
- A new capability, and a term for the glossary of `spec/index.md`, proposed by an item: its lines go only into a
  capability that has a codified file, and a term they need into that capability's own `## Terms`.
- The bar checked again when a batch picks the item, against `main` as it then stands and with the batch's other items
  laid in: waits for plan 4, which builds `batches`.
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g23 | items#g1 |
| r23 | items#r1 |
| g24 | items#g2 |
| r24 | items#r2 |
| g25 | items#g3 |
| r25 | items#r3 |
| g4 | items#g4 |
| r4 | items#r4 |
| g26 | drafting#g1 |
| r26 | drafting#r1 |
| g27 | drafting#g2 |
| r27 | drafting#r2 |
| g28 | drafting#g3 |
| r28 | drafting#r3 |
| g29 | drafting#g4 |
| r29 | drafting#r4 |
| g30 | drafting#g5 |
| r30 | drafting#r5 |
| g31 | drafting#g6 |
| r31 | drafting#r6 |
| g32 | drafting#g7 |
| r32 | drafting#r7 |
| g34 | drafting#g8 |
| r34 | drafting#r8 |
| g35 | drafting#g9 |
| r35 | drafting#r9 |
| g36 | items#g5 |
| r36 | items#r5 |
| g37 | drafting#g10 |
| r37 | drafting#r10 |
| g38 | drafting#g11 |
| r38 | drafting#r11 |
| g39 | drafting#g12 |
| r39 | drafting#r12 |
| g40 | drafting#g13 |
| r40 | drafting#r13 |
| g41 | items#g6 |
| r41 | items#r6 |
| g42 | drafting#g14 |
| r42 | drafting#r14 |
| g44 | drafting#g15 |
| r44 | drafting#r15 |
| g45 | drafting#g16 |
| r45 | drafting#r16 |
| g46 | items#g7 |
| r46 | items#r7 |
| g47 | drafting#g17 |
| r47 | drafting#r17 |
| g48 | drafting#g18 |
| r48 | drafting#r18 |
| g50 | items#g8 |
| r50 | items#r8 |
| g51 | drafting#g19 |
| r51 | drafting#r19 |
| g52 | drafting#g20 |
| r52 | drafting#r20 |
| g53 | drafting#g21 |
| r53 | drafting#r21 |
| g54 | items#g9 |
| r54 | items#r9 |
| g55 | drafting#g22 |
| r55 | drafting#r22 |
| g56 | drafting#g23 |
| r56 | drafting#r23 |
| g57 | drafting#g24 |
| r57 | drafting#r24 |
| g58 | items#g10 |
| r58 | items#r10 |
