# migration-rebind-4 research notes

Work-item accepts migration-tools r14-r17. Accepted scenarios (features/migration-tools.feature, found by its @r tags):
- r17 Outline "writes a qualified supersedes ... <case>" (line 82; 2 examples)
- r14 "relocates adrs/ ... with git" (line 249)
- r15 Outline "on a repository with <change> refuses ..." (line 308; 3 examples)
- r16 "adds every file ... and writes spec/decisions/index.md" (line 323)

No `Scripts:` shortcut needed: `python3 /home/vscode/shopsystem-bdd/scripts/tools` used.
Analysis-tool map: none (`tools tests-of` and `untested` answer "no map"); searches are `by search`.
`tools refs` misses `scripts/migrate` (no .py name, imports not seen): counts for names it imports are `refs`-made but incomplete.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q tests/scenarios/test_migration_tools.py -k "qualified_supersedes or relocates_adrs or on_a_repository_with_change or adds_every_file"` (run)
Result: 4 passed, 3 failed.

- r17, both examples (`one decision`, `two decisions, the first qualified`): fails at line 88
  `And its by has the qualifier "(for artifacts)"`: StepDefinitionNotFoundError. Line 87 (`supersedes names ...`) passes.
  Missing: a step definition. No existing step matches "its by has the qualifier" (`migration_ledger_steps.py:223-227`
  matches only `its by is ...` and `by is "..."`). Behind it, code is already right: see section 2.
- r16: fails at line 329 `And spec/decisions/index.md is what \`model decisions\` would write`: StepDefinitionNotFoundError.
  Line 328 (the staged-status Then, `test_migration_tools.py:167`) passes.
  Missing: a step definition. The nearest step, `test_migration_tools.py:176`, matches "`model decisions --check` says ... is current", a different text.
  Behind it, the code already writes the index and stages it (`migrate_write.py:write_all`, probe below).
- r14: passes today, not red. r15: all three examples pass today.

So the red part is two undefined steps. No production change is shown necessary by any run.

## 2. What the system answers today

Probe file: `.shop/scratch/migration-rebind-4-1-research/probe_migrate.py` (16 tests, each builds a repo in its own scratch
subdirectory and runs the worktree's `scripts/migrate run --context example.org/acme/shop` there, then
`scripts/model --root <repo> decisions --check`).
Command: `python3 -m pytest -q -s -o addopts="" --whole-suite .shop/scratch/migration-rebind-4-1-research/probe_migrate.py`
(`--whole-suite` is needed: the work-item plugin, loaded through the environment, refuses a run with no accepted scenario
when not given it; `-o addopts=""` drops `-n auto`.) Result: 16 passed (run).

r17 (Givens as the scenario: ledger 0003-b, 0004-c, 0007-a with source alice):
- one decision, `decision/0003-b (for artifacts)`: rc 0; `supersedes: design-decision/example.org/acme/shop/b`;
  `by: "alice; supersedes design-decision/example.org/acme/shop/b (for artifacts)"`; model decisions --check rc 0 (run).
- two, first qualified: `supersedes: [.../b, .../c]`; by carries `(for artifacts)` for b only (run).
- two, second qualified: by carries `(for artifacts)` for c only (run).
- two qualified, joined by `and`: by has both qualifiers, each after `; supersedes` (run).
- entry with no `source:`, qualified supersedes: by is `"; supersedes design-decision/.../b (for artifacts)"` (run; see D2).
- target not in ledger, `decision/0009-z (for artifacts)`: `supersedes: decision/0009-z` written in the old form, not an id;
  by `"alice; supersedes decision/0009-z (for artifacts)"`; rc 0 (run; see D1).

r16:
- scenario (work/i1/w1.md, ledger with only 0007-a): `R work/i1/w1.md -> .shop/work/i1/w1.md`, `D spec/decisions.md`,
  `A spec/decisions/0007-a.md`, `A spec/decisions/index.md`; index written with the table row; model decisions --check rc 0 (run).
- no ledger at all: index still written and staged, one table header only (run).
- tracked index with hand-written text: overwritten, shown `M`, check rc 0 (run).
- untracked index already present: refused, "could not write spec/decisions/index.md: a file git does not hold is there",
  nothing changed, `?? spec/decisions/` remains (run).

r14:
- scenario (adrs/0001-use-x.md, short body): `A .shop/records/decision-arguments/0001-use-x.md`, `D adrs/0001-use-x.md`, not `R`,
  since migrate adds an id and the short body no longer matches for git's rename detection. The scenario uses `body()`
  (long text) so it passes (run). Nearest-case note, not a defect of the scenario.
- destination already tracked: refused, "could not move adrs/0001-use-x.md onto ...", nothing changed (run).
- `adrs/README.md` and nested `adrs/sub/0002-b.md`: README gets no id; nested gets `decision-argument/.../0002-b` (run).

r15:
- staged change (`git add README.md`): refused, naming README.md (run).
- ignored file only (`.gitignore`): migrates (run).
- tracked README deleted: refused naming README.md (run).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/migrate_ledger.py:decision_text | `by` is the entry's source, plus `; supersedes <id> <qualifier>` per qualified target; supersedes is the id(s) | already the r17 form (run); the work-item needs no change here | the r17 Outline and the r2 "keeps both" scenario (features line 73), by search; read the Outline's Then at line 87 passes | refs (2 refs of supersedes_of, decision_text 1 ref in migrate_ledger.py) and search |
| scripts/migrate_ledger.py:supersedes_of | splits supersedes into (id, qualifier), qualifier is the text after the reference | already gives r17's split (run); unchanged | r17 Outline; features line 215 (`model check` scenario with a qualified supersedes), by search | refs |
| tests/scenarios/migration_ledger_steps.py:217-220 (`supersedes is {ident} alone`) | asserts supersedes equals one id | the r17 wording is "names ... and nothing else"; no accepted step uses this text | none (by search: no feature line matches its text) | search of features |
| tests/scenarios/migration_ledger_steps.py:223-227 (`its by is "..."`) | asserts by equals the given string exactly | for an entry with a qualified supersedes, by is no longer the source alone; no accepted scenario checks it that way (accepted r17 uses `has the qualifier`) | the plain-source scenarios at features lines 31, 39, 73 (by search) | search of features |
| scripts/migrate_write.py:write_all (index written last, `git add -f`) | writes spec/decisions/index.md from render_decisions and adds every written file | already the r16 behaviour (run); unchanged | r16 scenario and tests/scripts/test_migrate_write.py (read: asserts add of spec/decisions/0007-a.md only) | refs (write_all 1 ref) and search |

## 4. Tests the requirements make impossible to keep

`tools tests-of` answers "no map" (the map is a full-suite coverage run, not made here). Found by search.
- By search, tests asserting by = source exactly: migration_ledger_steps.py:87, :118, :227; they run entries with no
  qualified supersedes (read). They still pass under r17. Sound.
- By search, tests asserting supersedes is an old qualified form: migration_spec_steps.py:163-168 builds `supersedes: decision/0003-b (for artifacts)`
  as input. That is input, not an assertion of output; the features line 215 scenario checks `model check` is clean, which
  r17 keeps (read; not run). Sound.
- tests/scripts/test_migrate_write.py:47-54 and test_migrate_layout.py:30-34: no supersedes or index assertion that r16/r17 change (read).
- tests/scripts/test_model.py:178-182 (index written with no decision yet): consistent with the probe (read).
- Result: none of the tests can no longer pass as they are. The two existing steps are not red, only missing.

## 5. A step the work-item skips

none. The work-item adds no path; it adds two step definitions. Probes show the existing path (migrate run, then model
decisions --check) already writes, adds and checks the index (run).

## 6. Defects

D1. A supersedes naming a decision not in the ledger is written in the old form and not refused.
Reproduction (probe `test_r17_target_not_in_ledger`, run): ledger 0007-a with `supersedes: decision/0009-z (for artifacts)` and
no 0009-z entry. Result: rc 0, `spec/decisions/0007-a.md` has `supersedes: decision/0009-z` and
`by: "alice; supersedes decision/0009-z (for artifacts)"`; `model decisions --check` rc 0.

D2. An entry with no source and a qualified supersedes gets a by that starts with `; `.
Reproduction (probe `test_r17_no_source_qualified`, run): `by: "; supersedes design-decision/example.org/acme/shop/b (for artifacts)"`.

## 7. The file set

Must change (for the four accepted scenarios to pass):
- tests/scenarios/migration_ledger_steps.py (227 lines, 73 under the limit): add a Then for `its by has the qualifier "<q>"`
  (r17). Read: `:223-227` shows the existing by steps do not match the text.
- tests/scenarios/test_migration_tools.py (225 lines, 75 under): add a Then for `spec/decisions/index.md is what \`model decisions\` would write`
  (r16), beside the step at :176. Search: the step text is absent (grep of tests/scenarios).
Production: none. Probes show scripts/migrate, migrate_layout.py (131), migrate_ledger.py (123), migrate_spec.py (132),
migrate_write.py (126) already do r14-r17.
Must keep passing (on the path, unchanged): scripts/migrate (63), scripts/model (132, `load_model` reads it), scripts/model_report.py
(80, render_decisions), scripts/model_facts.py (265, read by model decisions; not edited); tests/scenarios/migration_old.py (81),
tests/scenarios/migration_spec_steps.py (209), tests/scenarios/migration_safety_steps.py (120).
All of these are under the 300-line limit (`tools size --limit 300` printed only scripts/measure and tests/scripts/test_measure.py, which are off this path).
