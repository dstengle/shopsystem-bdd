---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-10-cnl-4-foundation-what-the-plan-did
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-10
---

# CNL 4 foundation: what the plan did

The plan `.shop/records/2026-11-10-cnl-4-foundation/plan-foundation.md` carried out. Tasks 1-4 (b198, b145, b199, and
b151's universal condition read in its own file's grammar) are on main; tasks 5-10 (b151, this repository's glossary
in 4.0) on the branch `plan-cnl4-glossary`. The gate G1-G8 held after each task: the suite 1664 passed and 1 skipped,
`model check` 0 violations and 151 warnings throughout, `features generate --check` and `features vocab --check`
clean, no file over 300 lines, `model decisions --check` with the same three failing decisions as on main (0086-0088).
G7 (`model logic --json`) was identical to main's after every task. Every line's facts were compared too (b208's
point that a refused line drops silently out of `model logic`): no line is refused at any step, and the facts are
main's except one renumbering in Task 8.

## Task 5: codified-1 lines under a codified-2 index

A codified-1 line is translated with the old lexicon's Vocab and its ids mapped to the layered Vocab's
(`scripts/spec_context_ids.py`); the session then decided that the glossary's and every capability's entries sit side
by side in the layered lexicon, only a pack's entries hidden by the context's own (`spec_rgl_vocab`). The live probe
(index codified-2 with `imports: [cli]`) refused nothing, and `model logic --json` and `features generate --check`
were main's. The review of Task 5 left b208-b212 as ideas.

## Task 6: the switch

`spec/index.md` says `language: codified-2` and `imports: [cli]`; its opening paragraph says so. The seven entries
v_t16 named are marked `Redefines: cli.` and kept, because codified-1 lines use them and the old pipeline reads no
pack: `change`, `command`, `reason`, `refuse`, `tool` (spec/index.md), `name` (role-boundaries), `output`
(supervision). Their removal is b213. The time pack was not needed.

`model parse` alone now reads grammar 4. One test parsed a codified-1 capability's lines that way,
`tests/scripts/test_revision_done.py::test_the_lines_of_q47_parse` (q47's lines are work-queue's): it now passes
`--capability work-queue`. This test file was outside the task's listed files; the change is the one Step 3
foresees for the skills. The skills that call `model parse` alone on such a line (shaping-items step 2,
raising-a-request step 3 and its description) are b214.

## Task 7: relation rows

Step 1 wrote `one` in the cardinality of the 25 rows whose word is a preposition and whose cardinality was blank.
Step 2 removed the 54 rows that no tree of a live requirement and no definition uses: every row whose word is a verb
or a noun (`adds`, `changes`, `removes`, `deletes`, `asker`, `upstream`), the 1.x rows the plan names, and the like
rows of the retired capabilities; six capabilities' emptied `## Relations` tables went with them (batch-measurement,
code-research, planning, red-green, spec-integration, work-queue). 44 rows remain.

Rows made `one` and kept (11): file in worktree, question on node, stage for node, stage with result, request line of
item, question on item, review finding on pull request (spec/index.md); scenario of item (batches); review of pull
request, commit of batch, commit for review finding (pr-review). The commit message says ten; it is eleven.

Rows kept though no live requirement uses them, put back after G1 (3): question on node, stage for node, stage with
result. `grammar/corpus/core.txt` is parsed over the live lexicon (`test_spec_grammar`'s two core tests), and q47's
lines (`test_the_lines_of_q47_parse`) read `stage for an initiative`. No used row was a verb or noun row, so none is
listed as kept for a line.

## Task 8: dead terms

A term was taken as live when a tree of a live requirement or universal condition decodes to it (every line is
codified-1, so the old Vocab), a kept relation row names it, a live term's `Frame:`, `Kind of:`, `This:`, kinds or
condition definition names it, a group's given block or a step handler's key names it, or it has `Redefines:`.

Removed: 152 entries: 62 kinds (nouns), 50 conditions (adjectives), 14 actors (proper nouns), 10 events (verbs), 8
attributes and 8 resources (nouns, exclusive or counted). 34 were in `spec/index.md`'s `## Glossary` and 118 in 15
capabilities' `## Terms`; review, spec-consistency and spec-migration are left with no `## Terms`.

Put back (4, all for `grammar/corpus/core.txt`, which is parsed over the live lexicon): `discard` (verb), `logged
stage` and `line count` (nouns), `outputless` (adjective of result). G7 was identical. The one change to a line's
facts is a renumbering: feature-file-tools#r13's `c_dangling_2` is now `c_dangling`, because design-model-check's
`dangling` (adjective of capability-proposal) was removed.

## Task 9: This: and senses

`This:` was added to `bounded context` and `session` (spec/index.md) and to `repository` (migration-tools).

Senses kept: `use` (verb, state; Frame: text uses thing) and `list` (verb, state; Frame: text lists thing).

Senses dropped (b215):

- `name` (verb, state; Frame: text names thing). The glossary's entry comes before role-boundaries' `name`, and the
  old grammar reads a verb's first sense, so trials#r4 and #r5 were refused (v_p1). v_t16 also named it against the
  CLI pack's `name`.
- `record` (verb, action; Frame: agent records thing in file). The old frame reader refuses the frame (v_t13 at
  "thing in file"): it reads only a `to` recipient.

`hold` and `include` are left to the rewords, as the plan says.

## Task 10

CLAUDE.md's module map was checked against the branch's diff to `scripts/`. `spec_context_ids.py` has its row, and
the rows of `spec_context.py` and `spec_rgl_vocab.py` were rewritten in Task 5. The `spec_steps`/`spec_steps_facts`
row now names the definition followed in the old vocabulary through `under`.

## Left open

- b208-b212 (Task 5's review) and b213-b215 (this plan) are ideas.
- The items' statuses are unchanged; the main session closes b151 after the merge.
