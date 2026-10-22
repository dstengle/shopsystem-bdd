# migrate-kb-2 research notes

Work-item: .shop/work/i8-model-in-consumers/migrate-kb-2.md (accepts migration-tools#r1-r17). Base 31e9ed3.
CLAUDE.md: none in the worktree or the plugin repo. The work-item says every module stays under 300 lines.
Tools: `tools tests-of` and `untested` answer "no map" (a map runs the whole suite, which I may not run).
Counts of tests by search are floors. `tools refs` answered for named functions.
Git status at start and end: clean. `.shop/scratch/` is git-ignored.
Probe repos and files: `.shop/scratch/migrate-kb-2-1-research/` (probe_migrate.py, probe_steps.py).

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --tb=line -p no:cacheprovider tests/scenarios/test_migration_tools.py`
Result: 43 collected, 37 passed, 6 failed. The file holds exactly the accepted scenarios' tests.

- `test_run_rewrites_a_decision_files_by_that_names_old_a_path_it_moved[docs/superpowers/specs/s1.md-...]`:
  StepDefinitionNotFound `a repository on the old system with docs/superpowers/specs/s1.md` (run).
  Missing Given: test_migration_tools.py defines only the plans+specs+requests Given (line 78). Code behaviour: see D2.
- `...[adrs/0001-use-x.md-...]`:
  StepDefinitionNotFound `its spec/decisions.md has the entry `## decision/0007-a`, whose source is "alice, from adrs/0001-use-x.md"` (run).
  Missing Given: migration_ledger_steps.py:90 defines only the form with no source clause. Code behaviour: see D2.
- `test_run_keeps_both_decisions_an_entrys_supersedes_names...`:
  StepDefinitionNotFound on the three-entry Given (run). migration_ledger_steps.py:133 defines the two-entry form only.
  Also missing: "the entry 0007-a has supersedes naming X and Y" (migration_ledger_steps.py:159 takes the colon form only).
  Two further steps cannot pass as written (see part 4): the `is `superseded`` Then, and the `0003-b.md's and spec/...` Then.
  Code behaviour: D1 (the second target is lost).
- `test_run_gives_a_decision_file_its_entrys_supersedes_and_revisit_when...status_superseded`:
  AssertionError `superseded` at migration_ledger_steps.py:170 (run). The step's `{status}` keeps the backticks of
  "is `superseded`", so it compares "superseded" with "`superseded`" (read; probe_steps run: status '`superseded`').
  The code writes status superseded for 0003-b (probe test_two_supersedes, run). Fault is in the test step.
- `test_run_rewrites_a_frontmatter_id_and_a_supersedes_that_name_a_ledger_entry_it_numbered`:
  AssertionError `superseded` at migration_ledger_steps.py:170 (run), same cause. Its earlier Thens (id, rests_on,
  supersedes of 0008-b) pass today: the run got past them.
- `test_run_gives_a_moved_readmemd_no_id_kind_or_about`:
  StepDefinitionNotFound `a repository on the old system with records/logs/README.md` (run).
  Missing Given and missing Then: "has the content ... had, with no id, no kind and no about" matches no step (read).
  Code behaviour: the moved README gets no id (probe test_readme_under_records, run).

The other 37 accepted tests pass today (run).

## 2. What the system answers today

Probe file: .shop/scratch/migrate-kb-2-1-research/probe_migrate.py. Each runs `python3 <worktree>/scripts/migrate run --context example.org/acme/shop` in a throwaway git repository under the scratch directory.
Command (run): `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/migrate-kb-2-1-research/probe_migrate.py`

- test_two_supersedes (run). Ledger: 0003-b, 0004-c, and 0007-a with `supersedes: decision/0003-b and decision/0004-c`.
  rc 0. 0007-a.md: `supersedes: design-decision/example.org/acme/shop/b`; `by: "alice; supersedes design-decision/example.org/acme/shop/b and decision/0004-c"`.
  0003-b status superseded; 0004-c status accepted.
- test_by_path_and_body_path (run). Ledger source `alice, from adrs/0001-use-x.md`; body "see work/i1/w1.md".
  rc 0. by: `"alice, from adrs/0001-use-x.md"` (not rewritten). Body still says work/i1/w1.md. adrs file moved to .shop/records/decision-arguments/0001-use-x.md.
- test_by_path_docs_specs (run). Source `alice, from docs/superpowers/specs/s1.md`. rc 0. by unchanged.
- test_readme_under_records (run). records/logs/README.md moved to .shop/records/logs/README.md with its content unchanged, no frontmatter.
- test_supersedes_dangling (run). Ledger `supersedes: decision/0009-z` with no such entry. rc 0. Output `supersedes: decision/0009-z` written as is, no message.
- probe_steps.py (run): `parse` on "spec/decisions/{name}.md's status is {status}":
  on "spec/decisions/0003-b.md's and spec/decisions/0004-c.md's status is `superseded`" gives name "0003-b.md's and spec/decisions/0004-c" and status '`superseded`'.
  On the plain line gives status '`superseded`'.

Nearest cases the scenarios do not state, not probed (budget): a supersedes with a qualifier and two targets; a ledger already holding spec/decisions/ files.

## 3. Old assumptions

Refs (run, `tools refs`): supersedes_of: 2 references, both in migrate_ledger.py (86, 107). rewrite_text: 1 reference, migrate_spec.py:127. decision_text: 1 reference, migrate_ledger.py:111.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| migrate_ledger.py:supersedes_of | takes one id: split at the first whitespace, the rest is the qualifier | r2 two targets: the second becomes part of the qualifier (D1) | by search: every ledger scenario in test_migration_tools.py (plan_ledger runs for each) | refs, probe test_two_supersedes |
| migrate_ledger.py:decision_text (supersedes line) | writes one scalar `supersedes: <id>` | r2 two targets need both ids; migration_ledger_steps.py:153-156 and 181-184 compare the scalar | by search: r2 supersedes, r17 qualified, r5 numbered scenarios | refs, read |
| migrate_ledger.py:decision_text (by) | `by` = source raw, plus `; supersedes <id> <qualifier>` | r5: a path in by must name the moved file (adrs, docs/superpowers/specs) | by search: none passes; the r5 by scenario fails at its Given | read, probe test_by_path_and_body_path |
| migrate_ledger.py:plan_ledger (superseding set) | one target per entry, so only the first target is "superseded" | r2: each of two targets is superseded (0004-c stays accepted, D1) | by search: r2 keeps-both scenario (fails at its Given) | read, probe test_two_supersedes |
| migrate_spec.py:plan_references | walks tracked files only; ledger decision files are in plan.texts but untracked, so never rewritten | r5: their by and body paths must be rewritten (D2) | by search: none executes the rewrite of a decision text | read (plan_references loop), probe test_by_path_and_body_path |
| migrate_spec.py:rewrite_text | rewrites paths, links and renamed ids of a text it is given | fed decision texts it would rewrite by and body; not called for them today | by search: r5 README/notes scenario (passes) | refs |
| migrate_layout.py:record_kind / plan_ids | README.md under records/ gets no kind, so no id | r9 README: already no id (probe) | tests/scripts/test_migrate_layout.py (4 pass); by search: r9 README scenario (fails only at its step) | read, probe test_readme_under_records |
| scripts/model_work.py:40 and model_report.py:26 | read `supersedes` with as_list: a scalar or a `[a, b]` list | r2 two targets written as `[a, b]` is read by these | none (by search: no test of migrate writes a list) | read, grep |

## 4. Tests the requirements make impossible to keep

No map, so `tools tests-of` gave no answer. Searched by test: tests/scenarios/migration_*.py and test_migration_tools.py, and grep of tests/ for supersedes, migrate and superseded (by search).

- migration_ledger_steps.py:167-170 `spec/decisions/{name}.md's status is {status}`:
  cannot pass as written for any code: `{status}` keeps the backticks (run, probe_steps). Used by 3 scenario tests (2 fail at this step, 1 never reaches it).
- The same step for `spec/decisions/0003-b.md's and spec/decisions/0004-c.md's status is `superseded``:
  `{name}` captures "0003-b.md's and spec/decisions/0004-c", so the path opened is wrong (run, probe_steps). Cannot pass as written, with or without the backticks fixed.
- migration_ledger_steps.py:153-156 and 181-184 (`supersedes is {ident}`, `supersedes is {ident} alone`): compare a scalar.
  They pass today (run). They keep passing only if a single target stays a scalar. If r2 writes every supersedes as a list, they fail. Both readings are in part 7's note.
- Checked and sound (run): migration_ledger_steps.py:146-150, 102-118, 127-136; migration_spec_steps.py:190 (Behaviour numbering); migration_old.py:Old.keep/commit; test_migration_tools.py:200-205 (nothing changed under r7). These are in the 37 passing tests.
- tests/scripts/test_migrate_layout.py: 4 pass (run). Its FakePlan gives plan_ids a read() and texts: keep that contract.

## 5. A stage the work-item skips

r5's rewrite of a decision file's by and body: the existing way gives this stage to every tracked text file (plan_references), and a new decision file never reaches it.
Effects only that stage produces: the rewrite of a repository path, a relative Markdown link and a renamed frontmatter id in a decision file.
Existing-way check (run): test_run_rewrites_a_repository-relative_path... (README, notes/n1.md) passes today, so the stage works for tracked files.
Refusals: none in that stage. The `quoted()` check that refuses an unreadable by runs in decision_text before any rewrite; a rewrite after it does not re-check (read).
The rename of supersedes/rests_on ids is done in decision_text and by plan.renamed, not by the stage (read: supersedes_of uses plan.renamed).

## 6. Defects

Each reproduces by probe test_two_supersedes / test_by_path_and_body_path / test_supersedes_dangling (run, see part 2).

### D1: a supersedes naming two decisions loses one
Reproduce: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/migrate-kb-2-1-research/probe_migrate.py -k two`.
Ledger 0007-a `supersedes: decision/0003-b and decision/0004-c`. rc 0. 0007-a.md `supersedes: ...b` only; by `"alice; supersedes ...b and decision/0004-c"`; 0004-c status accepted.

### D2: by and body paths of a decision file not rewritten
Reproduce: `... -k by_path` (test_by_path_and_body_path, test_by_path_docs_specs).
Ledger source `alice, from adrs/0001-use-x.md`: rc 0; by `"alice, from adrs/0001-use-x.md"`; the adr file itself moved to decision-arguments. Body "see work/i1/w1.md" unchanged.

### D3: a supersedes naming no entry is written and reported as nothing
Reproduce: `... -k dangling`. Ledger `supersedes: decision/0009-z`: rc 0, `supersedes: decision/0009-z` in 0007-a.md, no message. Reported only: the requirements r6/r7 bear on it; I do not judge the plan.

## 7. The file set

Line counts by `wc -l` (run). Room = 300 - lines (work-item limit; no CLAUDE.md).

- scripts/migrate_ledger.py: supersedes_of, decision_text, plan_ledger for r2 two targets and r5 by. Found by refs, probes. (113 lines; room 187)
- scripts/migrate_spec.py: plan_references also rewrites created decision texts (r5). Found by read, probe. (129; room 171)
- scripts/migrate_layout.py: no change required (README passes); may change if plan.created shape changes. Found by read, probe. (156; room 144)
- scripts/migrate: no change expected: plan_references already runs after plan_ledger in cmd_run (read). (50; room 250)
- tests/scenarios/test_migration_tools.py: add Givens for docs/superpowers/specs/s1.md and records/logs/README.md, and the README Then. Found by run. (205; room 95)
- tests/scenarios/migration_ledger_steps.py: strip backticks in status step; `and` form; three-entry and naming Givens; source Given. Found by run, probe_steps. (190; room 110)
- tests/scenarios/migration_spec_steps.py: may take the README Then and the source Given. Found by run. (209; room 91)
- tests/scripts/test_migrate_layout.py: keeps passing (4 pass); changes only with plan_ids. Found by run. (46; room 254)

Modules on the change path, not edited:
- scripts/migrate_layout.py: loaded by migrate (above). (156; room 144)
- scripts/model: load_model; frontmatter and section read by migrate and tests. (132; room 168)
- scripts/model_parse.py: frontmatter, as_list, split_list. (271; room 29)
- scripts/features: `deprecate` run by migrate for @holding (plan_holding). (143; room 157)
- scripts/features_edit.py: cmd_deprecate. (112; room 188)
- tests/scenarios/migration_old.py: Old repo, front, load_model. (81; room 219)
- features/migration-tools.feature: 322 lines, a feature file, not edited; the limit covers code and test files.

## Notes for the plan (two readings, not decided)

- One supersedes target: keep the scalar line (the scalar Thens pass) or always write a `[a, b]` list (model reads both). The plan chooses; the scalar Thens break under the second.
- The `by` of a qualified two-target supersedes is not in any scenario.
