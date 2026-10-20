---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-decision-files-taught-test-log
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
date: 2026-10-20
---

# Test log: the writers write decision files, on the final layout

Case T-integrate on the final layout (spec spec-integration r20 to r22): a shelf fixture (`spec/index.md`,
`spec/capabilities/keep-items.md`, `spec/decisions/` with a generated index, `features/`, one approved note
`docs/notes/2026-10-02-listing.md` making one decision). Harness: `/home/vscode/scratch/shopsystem-bdd/final/`
(`make_final.py`, `run.sh`, `score.py`). Plugin: this working copy at commit 58f6b40, `claude -p --model sonnet
--plugin-dir`, the person's yes given in the prompt (they are away), "apply and commit spec/, then stop".

## First attempt (not scored)

The note said the list was "in the order added, not alphabetical". The run wrote `## Context` and
`## Alternatives`: the note itself weighed two options, so the section check was the fixture's fault. The
note was reworded to state the decision with no alternative, and the three runs below made on it.

## Runs t1 to t3

| run | decision file | sections | source | by | index in the spec commit | `model decisions --check` | files under .superpowers/ or docs/superpowers/ | tree |
|---|---|---|---|---|---|---|---|---|
| t1 | `0002-list-in-order-added.md` | Decision only | `[]` | words | yes | 0 | none | clean |
| t2 | `0002-list-in-added-order.md` | Decision only | `[]` | words | yes | 0 | none | clean |
| t3 | `0002-list-in-order-added.md` | Decision only | `[]` | words | yes | 0 | none | clean |

3 of 3 pass. In each, the spec commit holds the new capability, the decision file, `spec/decisions/index.md`
and `spec/index.md`, and `.gitignore` gained `.shop/scratch/` in a commit of its own. `model check` of the
result: one violation, the added line with no scenario (expected, formulation is next).

Not measured: a note whose decision cites a record (`source` with ids); a delegation recorded in `by`
(t1 and t3 wrote it in the commit message, `by` held the person and the note).
