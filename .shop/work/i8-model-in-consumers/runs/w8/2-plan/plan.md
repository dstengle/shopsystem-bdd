# Plan: migrate-kb-2 (migration-tools#r1-r17)

From research notes `.shop/work/i8-model-in-consumers/runs/migrate-kb-2/1-research/notes.md` (base 31e9ed3).
Today `tests/scenarios/test_migration_tools.py` collects 43 tests: 37 pass and 6 fail. These 6 are all this work turns green.
The work-item adds a limit: every module stays under 300 lines.

## 1. What goes green

- **migration-tools#r2**: "run keeps both decisions an entry's supersedes names, each by its new id, and supersedes both".
  This is red today because its three-entry Given and its "supersedes naming X and Y" Given have no step.
  Under those, the code has defect D1: `supersedes_of` keeps only the first target. The second target lands in `by`, and 0004-c stays accepted.
  Its last Then ("0003-b.md's and 0004-c.md's status is `superseded`") can't pass as written. The status step captures a wrong name and keeps the backticks.
- **migration-tools#r2**: "run gives a decision file its entry's supersedes and revisit_when, and the entry it supersedes the status `superseded`".
  This is red only because of the status step: its `{status}` keeps the backticks, so it compares `superseded` with `` `superseded` ``. The code is already right.
- **migration-tools#r5**: "run rewrites a frontmatter id and a supersedes that name a ledger entry it numbered".
  Same cause, the same status step. Its earlier Thens pass.
- **migration-tools#r5**: "run rewrites a decision file's by that names <old>, a path it moved", for both rows: adrs/0001-use-x.md and docs/superpowers/specs/s1.md.
  This is red because two Givens have no step: the source Given ("whose source is \"alice, from <old>\"") and the plain "with docs/superpowers/specs/s1.md" Given.
  Under those, the code has defect D2: `plan_references` walks only tracked files. The decision files that `plan_ledger` creates never reach the rewrite, so `by` keeps the old path.
- **migration-tools#r9**: "run gives a moved README.md no id, kind or about".
  This is red because neither its Given (records/logs/README.md) nor its Then ("has the content … had, with no id, no kind and no about") has a step.
  The code is already right: a probe showed the moved README gets no frontmatter.

This work-item retires no deprecated scenarios.

## 2. Where the change lands

- `scripts/migrate_ledger.py`:
  - `supersedes_of` reads a supersedes value as one or more decision targets, each with an optional qualifier.
  - `plan_ledger` marks every target superseded.
  - `decision_text` writes one or more targets (decision 1) and puts in `by` only a real qualifier (r17).
  - About 113 lines today.
- `scripts/migrate_spec.py`: `plan_references` also passes each decision text that `plan_ledger` created through `rewrite_text` (decision 3). About 129 lines today.
- `tests/scenarios/migration_ledger_steps.py`:
  - The status step strips backticks.
  - A new step covers two decision files' status in one line.
  - New Givens: the three-entry Given, the "supersedes naming X and Y" Given, and the source-with-quotes Given.
  - A "supersedes names X and Y, and nothing else" Then.
  - About 190 lines today, with room for 110.
- `tests/scenarios/test_migration_tools.py` or `tests/scenarios/migration_spec_steps.py`:
  - The Given "with docs/superpowers/specs/s1.md" (or one generalised "with <path>" Given that the existing fixed Givens still match).
  - The Given "with records/logs/README.md".
  - The README Then.
  - The implementer places these where there is room: test_migration_tools.py has 205 lines, migration_spec_steps.py has 209.

Removed from the researcher's set because nothing changes in them: `scripts/migrate`, `scripts/migrate_layout.py`, `tests/scenarios/migration_old.py` and `tests/scripts/test_migrate_layout.py`.
- `scripts/migrate` already runs `plan_references` after `plan_ledger`.
- A probe showed the README already gets no id.
- `test_migrate_layout.py` passes, and `plan_ids` keeps its contract.

The implementer reopens one of these files only if the shape of `plan.created` or `plan.texts` has to change.

## 3. Decisions

1. **How `supersedes` is written.**
   - An entry naming one decision keeps the scalar `supersedes: <id>`, as today.
   - An entry naming two or more decisions gets a list of their new ids. `model`'s `as_list` reads that form (`model_work.py` and `model_report.py` already use it).
   - This rests on r2 ("whose supersedes … are the entry's": one target stays one value, two keep both) and on r17 ("the decision's id alone").
   - The existing scalar Thens ("supersedes is X", "supersedes is X alone") stay valid.
2. **How a supersedes value is split into targets.**
   - Each `decision/<…>` reference in the value is a target.
   - The word "and" between two references separates them; it is not a qualifier.
   - Text after a reference that is not another reference is that target's qualifier, as today.
   - Every target is renamed through `plan.renamed`, and each target's entry gets status `superseded`.
   - `by` gets "; supersedes <id> <qualifier>" only for a target that has a qualifier. With no qualifier, `by` is the source alone.
   - This rests on r2 and r17, and on the work-item's trial row ("a `supersedes` naming two decisions keeps both").
3. **A decision file's text goes through r5's rewrite.**
   - The decision files `plan_ledger` creates are rewritten by the same `rewrite_text` stage as tracked text files, in both `by` and body.
   - This rests on r5 and r16: the file is added to git, so it is one of the repository's tracked text files after the run.
   - It also rests on r6 and design-decision/references-are-ids.
   - The `quoted()` check runs before the rewrite. The rewritten `by` must still be one `model` reads as it is. Paths add no quoting hazard, but the implementer confirms the check still holds after the rewrite, or moves the rewrite before it.
4. **The status step strips backticks** around its expected status.
   - The two-file Then gets its own step, matched before the one-file step, which checks each named file.
   - This is a test repair: the feature text is accepted and unchanged.

## 4. Tests the decisions break

None.
- Decision 1 keeps a single target as a scalar, so `migration_ledger_steps.py`'s "supersedes is {ident}" and "supersedes is {ident} alone" steps (153-156, 181-184) keep passing.
- Decision 4 repairs the status step (167-170). It is not a test the code breaks: it can't pass today for any code.
- I checked the notes' part 4 list, the steps the notes judged sound (146-150, 102-118, 127-136, the Behaviour numbering step, `Old.keep`/`commit`, the r7 "nothing changed" step), and `tests/scripts/test_migrate_layout.py`. None of them asserts the old one-target parsing or an un-rewritten decision text.

## 5. Open cases

- A supersedes naming two targets where one or both carry a qualifier: what `by` reads, and where a qualifier ends. No scenario states it.
- Separators other than "and" between targets (a comma, "and" with a list of three): no scenario states them.
- Defect D3: a supersedes naming no ledger entry (`decision/0009-z`) is written as is, exits 0 and says nothing. No scenario here covers it; r6/r7 bear on it, and this work leaves it as it is.
- Whether `model check` (r6) resolves each id in a supersedes list as it does a scalar. No r6 row has two targets. The implementer names what it sees.
- `rewrite_text` on a decision body might also rewrite old `decision/<…>` ids written in prose. The scenarios pin only `by`.
- A ledger whose spec/decisions/ already holds files: not probed.
