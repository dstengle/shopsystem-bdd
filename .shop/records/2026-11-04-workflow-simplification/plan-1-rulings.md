---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-1-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Plan 1 of the workflow simplification: rulings on the review, and the gaps left for later plans

`plan-1-review.md` asked the person eleven questions (P1-P11) and left two choices open (S3 and S10). The person was
not available and asked that the work go on without waiting for them. Each ruling below was **ruled by the main
session without the person, 2026-11-04; revisit.** The fixes that follow from them, and from S1-S9 and the minor
findings, are on branch `workflow-simplification` after `37fbb619`: `85d9c518` (`spec_unbuilt`) and `1533b70a` (the spec and its features).

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-04; revisit) | What was done |
|---|---|---|---|
| P10 | May lines that were never merged be fixed in place? | Yes. Retire, never edit, starts at the merge to `main`. | S1-S8 and the lines below are edited in place, with no retired ids and no new ids for changed lines. |
| P6 | Should the unbuilt xfail be strict? | Yes. An unbuilt scenario that passes fails the suite. | `spec_unbuilt.mark` uses `strict=True`. A test runs pytest on a passing unbuilt scenario and expects `XPASS(strict)` and exit 1. |
| P1 | The traceability chain has no line. | Add it: the batch's pull request and its commits name their items. | batches r11 (the pull request cites every `in-batch` item) and r13 (`work batch review` refuses an `uncited` commit of an item). The relation word is `cites`, because `names` reads two ways in the step grammar (the relation, and role-boundaries' `name` event). |
| P2 | Parts of the backlog view are missing. | Add what the grammar can say now. What it can't say goes to the capability's `## Not yet`, naming plan 2. | backlog r17: a `needs-input` item's question is printed. The grammar has no ordering or grouping, so tables by state, rank order and the WSJF score, and how far a batch is along are in backlog's `## Not yet` for plan 2. |
| P3 | `needs-input` → `shaped` and the park's question have no line. | Add them. | backlog r16: `work answer` takes a `needs-input` item to `shaped`. batches r6: a park also writes a question on the item. The glossary gains the row `question on item`. |
| P4 | Bugs' risk and likelihood aren't in the lexicon. | Add them if the design gives them a part in the rank. Otherwise note them for plan 2. | The design gives them no part in the rank: the score is (value + urgency) / size. So they are noted in backlog's `## Not yet` for plan 2. |
| P5 | The tier-1 checks are out of the readiness bar. | Leave them out of `passing` for now. | decision-tiers' `## Not yet` says plan 6 adds them to the bar. |
| P7 | Do the rating values leak into the CLI? | Accept the qualified values (`high-value`, `low-urgency`, `small`) in the CLI. | No change. |
| P8 | `intake#r1` loses who asked. | Accept it. Put the tie to the asker in intake's `## Not yet`. | Done. |
| P9 | New lines lean on terms of capabilities that will retire. | Lift `fix now`, `measurement`, `defect` and `failing` into the glossary, with definitions that don't depend on those capabilities. | `triage` (with its value `fix now`) moved from review, `defect` from code-research and `failing` from analysis-tools. `measurement` is redefined: the figures of one batch, of one earlier delivery or of a trial. |
| P11 | Two inverse relation rows for one fact. | Accept them. | No change: `item proposes requirement` and `requirement proposed by item` stay. |
| S3 | `intake#r6` adds nothing, and the rule it means is missing. | Option (a): settled request lines are part of `passing`. | `passing` is now defined in the controlled language: "An item is passing when the item is well-formed and every request line of the item is settled." The old prose became `well-formed`. With the rule in `passing`, intake r6 is the refusal of option (b), and `model logic` finds no L1 against `readiness#r1`. |
| S10 | Frozen `.shop/work/` references now point at the new capabilities. | Don't change resolution now. | Left for plan 9 (below). |

## Known gaps for later plans

- **The generator drops parts of a statement (S2), and it needs fixing in the generator.** On this branch the lines were
  reworded so that their point is a Given or a Then. The class of gap stays:
  - A `no` object in a negative response loses its relation. `… shall not publish a commit of the item` gives "does
    not publish the commit c1" with no tie to the item. batches r7 now puts the commit in its precondition.
  - A `no` in a precondition gives no Given. "the commit cites no item" gave nothing, so batches r13 uses the
    condition `uncited`.
  - An `every` in a precondition gives no Given. batches r8's "every task of the batch is `done`" gives none. r12 is
    the refusal the scenario lacked.
  - A modifier on a definite in a response becomes a Given. "publish the commit that cites the item" made the citing a
    precondition.
  - When the precondition mentions two items, "the item" in a response binds to the item mentioned last. backlog r7 is
    ordered for this.

  Owner: the plan that next touches `spec_steps` (plan 2 at the earliest). That plan should check every new line's
  scenario against its point.
- **A scenario uses an item it never sets up.** For example backlog g4, g5, g6 and g15, readiness g4 and conversation
  g4. The old features do the same. Plan 2's handlers absorb it (review, open problem 4).
- **M3, weak lines:**
  - telemetry r4 checks only that the two names are printed;
  - conversation r2 gives `--session --transcript` with no values;
  - readiness r4, batches r5 and intake r5 say "does not ask the question q1".

  The plans that build them (7, 8, 3, 4, 3) strengthen them where their handlers show how. A line that changes after
  the merge is retired and replaced.
- **M4, the grammar corpus:** the nine `grammar/corpus/<cap>.txt` files use the fixture vocabulary, as
  `test_spec_grammar` requires, so they exercise none of the new terms. A later grammar change should add a corpus
  over the live lexicon.
- **M7, scenario names:** a batch plan is named `b2` next to the batch `b1`, while items are `b<n>` in the glossary.
  This is generator naming. Plan 2 decides whether instance letters follow the kind's id form.
- **S10, frozen `.shop/work/` references:** all ten references in `.shop/work/i57/` that stopped being unresolved now
  resolve against the new `backlog` capability and the `backlog` term by collision. Resolution is unchanged on this
  branch. Plan 9, which freezes `.shop/work/`, decides whether frozen history is left out of reference resolution or
  read as of its own release. The implementation report's explanation is corrected in place.
- **The `blocked` condition** keeps its prose definition, because "not in the same batch" can't be said yet. Its prose
  now uses the `dependency` kind (M1).
- **An existing timing flake:** `tests/scripts/test_revision_done.py::test_model_logic_on_the_live_spec_is_fast` fails
  about one full-suite run in three under xdist, both at `37fbb619` and after these fixes. Measured alone, `model
  logic` takes 1.3-1.4 s of CPU either way. It is not caused by this branch, and it is not skipped.

## The other findings

| Finding | Done |
|---|---|
| S1 | batches r7 says that the parked item's commit is not published. The commit is in the precondition, so the scenario ties it to the item. |
| S4 | batches r10 readies only the items that are `in-batch`. |
| S5 | batches r9 also sets the batch `merged`. |
| S6 | decision-tiers r6 needs a superseder that is `accepted`. |
| S7 | pr-review r3 holds while the pull request is `unreviewed`, a new condition of pr-review: the first review only. r6 is the re-review. |
| S8 | backlog r7 prints the blocked item and the dependency that blocks it, using the `dependency` kind. |
| S9 | `test_the_repository_lists_no_unbuilt_id_it_lacks` holds `spec_unbuilt.problems` at `[]` on the repository. |
| M1 | One form of dependency: the `dependency` kind with its `of` and `on` rows, moved to the glossary. The row `item depending on item` is removed. |
| M2 | batches g1's title names the cap: "picks ready items, up to `batch_size`". |
| M5 | Tests that `mark` leaves the same id of another capability alone, and that `features vocab --check` wants no handler for an unbuilt scenario. |
| M6 | `problems()` names an `unbuilt:` given on a capability that is not codified. |
| M8 | The implementation report lists the pytest deviation (12). The git-ignored ledger names `6d24906a`. The report and review are committed and indexed. |
