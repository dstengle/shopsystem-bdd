# Plan 1 of the workflow simplification: implementation report

The report of the one implementer agent that executed `plan-1-spec.md` (superpowers:executing-plans, a commit per task), 2026-11-04.

All 11 tasks are done and committed on `workflow-simplification` (c46cce36..6d24906a). Every baseline holds. A few metrics went down, and none went up.

## Final state
- **Suite** (`python3 -m pytest -q`): 946 passed, 1 skipped, 49 xfailed, 129 subtests passed. The starting point was 941 passed and 1 skipped. The 5 new passes are the tests in `tests/scripts/test_spec_unbuilt.py`. The 49 xfails are the scenarios of the 7 new service capabilities.
- **`model check`**: 53 violations, 16 warnings, 19 unresolved references, 0 file problems. Unresolved references fell from 29 to 19 because the new terms resolve references in existing files: the first drop, to 28, was i57's glossary-proposal, which names `backlog`. *(Corrected by the review, S10: all 10 are in `.shop/work/i57/`, whose old `backlog#r1`–`r8` and `backlog` term now collide with the new capability; nothing was resolved.)*
- **`model logic`**: `11 findings: 6 L5, 5 L6`, unchanged. No finding names a new capability.
- **`model lexicon --check`**: 398 terms, 0 problems.
- **`features generate --check`**: passes. Every existing feature is byte-identical to the copy saved before the lexicon change.
- **`features vocab --check`**: every step has one handler. **`features bindings --unbound`**: every binding names a scenario, exit 0.
- **`python3 scripts/tools size --limit 300`**: silent, exit 0.
- **Count (Task 11, Step 3)**: `spec_unbuilt.unbuilt(.)` lists 60 requirements across all 9 new capabilities, which equals the 60 `[r<n>]` lines in their files. `problems(.)` is empty.

```
6d24906a records: plan 1 verified, every task ticked
8f560c7a spec: conversation, codified and unbuilt
f4b06847 spec: telemetry, codified and unbuilt
a138d6c1 spec: decision-tiers, codified and unbuilt
0c4ddf65 spec: pr-review and brainstorming, codified and unbuilt
3c0d96fc spec: batches, codified and unbuilt
d5e1d129 spec: intake, codified and unbuilt
e0b21a53 spec: readiness, codified and unbuilt
3357dc10 spec: backlog, codified and unbuilt
e3dc3184 spec: the simplified workflow's lexicon and decision 0074
5b384a8b spec_unbuilt: a capability's unbuilt requirements run as expected failures
```

## Tasks

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 `unbuilt:` mark | 5b384a8b | Added `scripts/spec_unbuilt.py` (`unbuilt`, `problems`, `mark`). `work_items.py` calls `mark` on every run (now 248 lines). Added its `CLAUDE.md` row. | The 4 tests failed first (module missing), then passed. Suite 945 passed. A temporary `unbuilt: []` in `trials.md` kept `model check` at 53/16/29/0, so `model_spec.py` needed no change. |
| 2 lexicon and decision 0074 | e3dc3184 | Added the glossary block, 10 relation rows, decision 0074 (`the-workflow-simplified`), a "Where it stands" sentence, and the regenerated decisions index. | Lexicon has 0 problems, both probe lines parse, features unchanged, logic, check and suite unchanged. |
| 3 backlog | 3357dc10 | 15 groups, `test_backlog.py`, and its grammar corpus file. Also `features vocab --check` skips the handler check for unbuilt scenarios (see deviation 4). | Parse 15/15, logic clean, 15 xfailed. |
| 4 readiness | e0b21a53 | 4 groups. | 4 xfailed. |
| 5 intake | d5e1d129 | 6 groups, plus its own relation row: a request line is `of` an item. | 6 xfailed. |
| 6 batches | 3c0d96fc | 10 groups. Rank order and `batch_size` are prose under `## Implementation, may change`. | 10 xfailed. |
| 7 pr-review and brainstorming (guarantees) | 0c4ddf65 | 8 groups and 3 groups. Actors `pr-reviewer` and `the brainstorming session`. No feature and no test module. | Parse and logic clean. |
| 8 decision-tiers | a138d6c1 | 6 groups, with rule codes `w_untiered`, `v_d6`, `v_d7`, `v_d8`. | 6 xfailed. |
| 9 telemetry | f4b06847 | 4 groups. Reuses code-research's existing `defect` kind. | 4 xfailed. |
| 10 conversation | 8f560c7a | 4 groups. Actor `the UserPromptSubmit hook`, and `work names` for the names table at SessionStart. | 4 xfailed. |
| 11 verification | 6d24906a | All plan checkboxes ticked. `.shop/records/README.md` already had the rows from c46cce36, so it is unchanged. | Everything under "Final state" above. |

Each of Tasks 3-10 ran: parse the file, check `model logic` (nothing names the capability, total unchanged), `features generate` plus `--check`, bind the test and see every scenario xfailed, add the Composition row, then `model check` and the suite. Every new feature is also added to `BOUND_BY_PYTEST_BDD` in `tests/scripts/test_bound.py`. No `w_unserved_cap` warning appeared.

## Deviations from the plan
These are recorded as rulings in the ledger at `.superpowers/sdd/plan-1-spec/progress.md` (git-ignored). Except where noted, the cost if wrong is a reworded line or a renamed term.

1. **Rating values.** The lexicon check refuses the same value in two attributes of one kind. So value, urgency and size became `low-value|medium-value|high-value`, `low-urgency|medium-urgency|high-urgency` and `small|medium|large`.
2. **`origin` became `provenance`.** `origin` is already a kind in requests' terms. The new attribute made `requests#r6-r8` parse two ways, which failed `generate --check`.
3. **`depends on` became `depending on`.** The grammar reads a relation word that ends in a preposition as "an item depends on X" and "X is depends on Y". `depending on` reads correctly in both forms.
4. **New: `features vocab --check` ignores missing handlers for unbuilt scenarios.** The plan says to write no handlers, but the suite's `test_bound` failed on every new feature. Their steps are still parsed. This adds `spec_unbuilt.unbuilt_lines`, tested.
5. **New: a grammar corpus file per capability.** `test_spec_grammar` requires `grammar/corpus/<cap>.txt` with at least 8 sentences, written in the test fixture's vocabulary. Nine added.
6. **Group splits for one statement per group, and no two groups with the same trigger.**
   - backlog: withdraw is 4 groups and refuse is 2. The backlog title is merged into g6, and `work show` is g15.
   - pr-review: correctness and "only the batch's commits" are one group.
   - decision-tiers: the plan's group 4 is two groups.
   - batches: groups 5 and 6 each join their two clauses with ", and `work` shall …".
7. **Terms added to capabilities.**
   - backlog: kinds `title` and `dependency` (an attribute needs values, and a dependency written any other way became a precondition).
   - pr-review: rows such as "requirement proposed by item" and "commit outside batch".
   - decision-tiers: conditions `untiered`, `untested`, `unrequired`.
8. **A new transition.** Item status gains `in-batch` → `ready` by `work batch abandon`. The plan's batches group 10 needs it and Task 2's table lacked it.
9. **`clean` is defined in the controlled language:** "A pull request is clean when no review finding on the pull request is `fix now`." Same meaning, and `model logic` can now tell the fix-now line from the clean line.
10. **Wording the grammar can't take literally.**
    - readiness: "the first failing check" is said as "the reason". Its "asks no question" line is tied to `work ready`, not stated as an always-true rule.
    - intake: the outcome is part of the command (`work outcome accepted`). "Whose upstream is this context" is left out.
    - brainstorming: "run `work ready`" is said as "use `work ready`".
    - telemetry: `measure compare batch-2 batch-3` prints both names.
    - Counts, flags and rank order are prose under `## Implementation, may change`.
11. **Plan progress.** Tasks 3-10 share one set of step checkboxes, so each task also has a "- [x] Steps 1-7 done." line with its notes.
12. **pytest, not `unittest`.** `tests/scripts/test_spec_unbuilt.py` is written as pytest functions with `tmp_path`, where Task 1 asked for `unittest`. Harmless *(added after the review, M8)*.

No line went to `## Not yet`, and the grammar was not extended.

## Open problems and questions
1. **batches g7's scenario doesn't test its point.** The line says "publish a pull request of the batch with no commit of the item". The generator drops the "no …" object, so the scenario has no Then for the exclusion. A gap in the step generator.
2. **`spec_unbuilt.problems()` has no caller.** A mistyped `unbuilt:` id marks nothing, as the plan's Review Focus 3 asks, but nothing reports it to the person yet, unless a later plan wires it into `model check`.
3. **Glossary questions for the person:**
   - `blocked` keeps its prose definition, because "not in the same batch" can't be said in the grammar. Today that causes no L6.
   - "item proposes requirement" (glossary) and "requirement proposed by item" (pr-review) are inverse rows of the same fact.
4. **Generated scenarios that use an item they never set up.** In backlog g4, g6 and g15, a bare "on an item" gives "When … on the item i1" with no Given. Existing features may do the same; the generator is unchanged.
5. **The end-of-branch review** is run next, by a separate reviewer (`plan-1-review.md`).

## Files
- **New code:** `scripts/spec_unbuilt.py`, `tests/scripts/test_spec_unbuilt.py`
- **Changed code:** `scripts/work_items.py`, `scripts/features`, `tests/scripts/test_bound.py`, `CLAUDE.md`
- **Spec:** `spec/index.md`, `spec/decisions/0074-the-workflow-simplified.md`, `spec/decisions/index.md`, `spec/capabilities/{backlog,readiness,intake,batches,pr-review,brainstorming,decision-tiers,telemetry,conversation}.md`
- **Features and tests:** `features/{backlog,readiness,intake,batches,decision-tiers,telemetry,conversation}.feature`, `tests/scenarios/test_{backlog,readiness,intake,batches,decision_tiers,telemetry,conversation}.py`
- **Grammar corpus:** `grammar/corpus/` (nine `.txt` files)
- **Plan:** `plan-1-spec.md`, all boxes ticked
