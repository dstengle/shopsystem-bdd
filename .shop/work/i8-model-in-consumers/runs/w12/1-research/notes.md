# Research notes: migrate-run (work-item i8, accepts migration-tools#r1-r11)

Method. No `CLAUDE.md` in the worktree (Glob for it: none), so module map and size limit are "no limit stated".
Analysis tools: `tools probe` ok (no virtualenv). `tools refs` works on `.py` only: `scripts/model`, `scripts/features`,
`scripts/plan`, `scripts/measure` are extensionless and refs reports them "nothing defined". `tools tests-of` / `untested`:
no coverage map exists (`.shop/scratch/tools/coverage` absent), so every test list below is `by search`.
Probes run against the worktree's own `scripts/` (through subprocess in scratch repositories), not the checkout's data.
Scratch: `.shop/scratch/migrate-run-1-research/` (ignored by git: `!! .shop/scratch/`). `__pycache__` from my pytest runs is ignored too.
Scenarios: 10 in `features/migration-tools.feature`; r11 has no scenario of its own (it is tagged on r2's scenario).

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -p no:warnings --tb=short .shop/scratch/migrate-run-1-research/probe_red.py`
(the probe calls pytest-bdd `scenarios("<worktree>/features/migration-tools.feature")`, as a test module would). `run`.
All 10 fail at their first Given, `StepDefinitionNotFoundError`; no When or Then is reached.

- r1 "run moves decisions/ ... with git": `Given a repository on the old system with decisions/0001-d0.md, work/i1/w1.md and records/logs/r1.md`
- r2 (+r11) "run replaces a ledger ...": `Given ... spec/decisions.md has nothing but the entry ## decision/0007-a`
- r3 "run deprecates a @holding scenario": `Given ... features/thing.feature has a scenario "s1" tagged @holding`
- r4 "run gives spec/index.md the id": `Given ... spec/index.md gives no id`
- r5 "run rewrites a repository-relative path ...": `Given ... with work/i1/w1.md`
- r6 "after run, model check reports no violation ...": `Given ... decisions/, work/, records/, docs/superpowers/plans/ ... a @holding scenario`
- r7 "run that cannot make two of its changes ...": `Given ... .shop/work/i1/w1.md already exists`
- r8 "run moves docs/superpowers/plans/ ...": `Given ... docs/superpowers/plans/p1.md and docs/superpowers/specs/s1.md`
- r9 "run gives a capability ... the type-first id": `Given ... spec/capabilities/thing.md with no id`
- r10 "run numbers each Behaviour line ...": `Given ... thing.md whose retired: lists r4`

What is missing, by file: `scripts/migrate` does not exist (no file, no `migrate` command anywhere in `scripts/`).
`tests/scenarios/test_migration_tools.py` does not exist (no `scenarios("migration-tools.feature")`, no step definitions).
`tests/scripts/test_bound.py` lists five feature files; `features/migration-tools.feature` is not among them (its comment says it joins at i8).
Whens and Thens are undefined too (read of the feature file; not reached in the run).
Probe-only: pytest warns "Unknown pytest.mark.r7 ..." because `r<n>` markers are registered in `tests/scenarios/conftest.py`, not in the probe's path.

## 2. What the system answers today

Probe file `probe_today.py` (run, `python3 -m pytest -q -s -p no:warnings .../probe_today.py`) and `probe_more.py` (run). Each entry: command, result, `run`.

2.1 r3 Given/When, `features deprecate` on a @holding scenario. Repo: `spec/index.md` (id bounded-context/ex.com/prod/ctx),
`spec/capabilities/thing.md` (one [r1] line), `features/thing.feature` with `@r1 s2` and `@holding s1`.
- `model check` before: `v_s1 a scenario names no requirement`; `file: ... 's1' is tagged @holding; the tag is @deprecated`; rc=1. (run)
- `features deprecate s1 --for-removal`: rc=0, prints `features/thing.feature: s1 (deprecated)`. Result tag line `@holding @deprecated`,
  title `Scenario: s1 (deprecated)`, line `Deprecated for: removal`. (run)
- `model check` after that: rc=1, `file: ... 's1 (deprecated)' is tagged @holding`. (run)
- Same repo with `@holding` replaced by `@deprecated` by hand: `model check` rc=0, 0 violations, 0 file problems, one warning
  `w_unserved_cap` (a warning, not counted as a problem). (run)
  So `features deprecate` alone does not reach r3's end state; a `@holding` tag must also go.

2.2 Old layout (r1, r4, r6 Givens), repo with `decisions/0001-d0.md`, `work/i1/w1.md`, `records/logs/r1.md`, `spec/decisions.md`, thing.md without id:
`model check` rc=1 with `file:` lines `spec/decisions.md`, `decisions/`, `work/`, `records/` each "the layout has no X; run scripts/migrate",
and `spec/index.md is missing: no bounded-context is named`. With `spec/index.md` id given: the index problem goes, the four layout problems stay. (run)
Thing.md without `id:` gave no problem: `model` takes `capability/<path>/<name>` from the path (scripts/model:523-524) (run: no line).

2.3 r9 Given, a record with an id and no kind: `.shop/records/logs/run1-test-log.md` with `id: measurement/...` only:
`file: ... kind None is not a record kind`, rc=1. (run). So r9's id alone leaves model check failing; the kind key must be written too.
An existing archived plan, `.shop/records/archive/plans/2026-10-17-0.19.0-type-first-ids.md`, carries `id`, `kind`, `about`, `date` (read).

2.4 r9/r5: a capability with `rests_on: [decision/0007-a]` and a decision file `spec/decisions/0007-a.md` with id `design-decision/.../a`:
`unresolved: spec/capabilities/thing.md: decision/0007-a is not a design-decision in this repository`, rc=1. (run). Old-form refs are unresolved, as r5 assumes.

2.5 r2 Then, a decision file with frontmatter `id, summary, date, status, by` and `## Decision` (no revisit_*, no supersedes, no source):
`model check` raises nothing for it; `model decisions` writes `spec/decisions/index.md` (rc=0). (run). `by` is free text; model reads `source` as ids (scripts/model:628-629) and ignores `by` (read).

2.6 r6 with work: `.shop/work/i1/w1.md` (no initiative.md):
`file: .shop/work/i1: no initiative.md`. (run). Every directory under `.shop/work/` needs `initiative.md` (scripts/model:666-672, read).
The r6 scenario's Given names `work/` but not an `initiative.md`; migrate's r1 moves the directory only. Gap, see 6/7.

2.7 r10 Givens: Behaviour lines `- [r1]`, `- **When** ...` (no id), `- [r3]`, `- **When** ...` (no id), with retired r4 in another capability:
`v15a a requirement has no id` for each no-id line (`#line2`), `v_s3 a requirement has no scenario` for `#r3` and `#line2`; rc=1. (run).
So r6 cannot pass with unnumbered Behaviour lines; r10's numbering is required for r6. Expected r10 result by arithmetic: highest id ever used is 4 (retired r4), so the no-id lines become r5 and r6.

2.8 `features deprecate` nearest cases (run, repo with `features/thing.feature` (s2 @r1, s1 @holding) and `features/other.feature` (s1 @r1)):
- no `--for` / `--for-removal`: rc=2, argparse `one of the arguments --for --for-removal is required`. migrate must pass one of them.
- `deprecate s1 --for-removal` with s1 in two files, no `--file`: rc=1, `title 's1' is in several scenarios: features/other.feature, features/thing.feature`.
- `deprecate s2 ... --file features/thing.feature` once: rc=0. Again: rc=1, `does not have the title 's2'` (the title now carries "(deprecated)").
- A feature file with a `Rule:` block: `features count --by-tag` rc=1, `line 3: Rule: blocks are not supported`. The whole `--dir` is refused, not one file (read: `load()` raises for any file). (run)

2.9 `git mv` nearest cases (run in a scratch `git init`, files staged with `git add`, no commit):
- `git mv a.md b.md` with b.md present: rc=128 `fatal: destination exists`.
- `git mv c.md d.md` with c.md untracked: rc=128 `fatal: not under version control`.
- `git mv work .shop/work` with `.shop/` absent: rc=128 `renaming 'work' failed: No such file or directory`.
- `git mv c.md nodir/d.md` with `nodir/` absent: rc=128 `renaming 'c.md' failed`.
- `git mv decisions spec/decisions` with `spec/decisions/` present: rc=0, result `spec/decisions/decisions/0001-d0.md` (nested, not moved onto the directory).

2.10 `tests/scripts/test_bound.py` as it is today: 1 passed (run, about 60 s).

## 3. Old assumptions

Requirements that change or replace an old form. Found by `Grep` over `scripts/` and `tests/` (by search), then reads. `tests` column: by search (no map).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/plan:find_file (186-196) | reads the live plan only at `docs/superpowers/plans/*-slices.md`; refuses 0 or >1 | r8 moves `docs/superpowers/plans/` to `.shop/records/archive/plans/`; a migrated repo's plan is refused "found 0" | tests/scripts/test_plan.py:580-585 (archive), 632-645 (named or one plan) | search |
| scripts/plan:staleness (333) | changes outside `docs/superpowers/plans/` count as "outside" | path moves under r8 | none (`by search`: test_plan.py:565 names the path in a row; not sure it is run) | search |
| scripts/measure:cmd_batch (363, 414, 623) | default plan glob, tasks path and `--archive-dir` default `docs/superpowers/plans/archive` | r8: archive is `.shop/records/archive/plans/`; the default dir is gone after migrate | tests/scripts/test_measure.py: e.g. 173-266 (batch), 464-477, 518-521 | search |
| scripts/measure:cmd_batch (405) and docstring (52) | writes facts to `docs/superpowers/measurements/<name>.json` | not in the final layout (`.shop/records/measurements/` exists in this repo) and migrate does not move it; measure would recreate the old dir | test_measure.py:323-336 (default output), 507-520 | search |
| scripts/model:read_layout OLD_LAYOUT (119, 467-472) | names each old path as "run scripts/migrate" | after a migrate run none exists: no problem (r6) | tests/scenarios/test_design_model_check.py:653-655 | search |
| scripts/model:read_features (589-591) | `@holding` in a feature file is a file problem | r3 wants no @holding left; this is the check that fails when `features deprecate` is used alone (2.1) | tests/scenarios/test_design_model_check.py:176-180 | search |
| scripts/features:cmd_deprecate (380-397) | adds `@deprecated`, "(deprecated)" title, `Deprecated for:`; keeps `@holding` | r3 says "as features deprecate does" and "no @holding left": the two differ | tests/scenarios/test_feature_file_tools.py:648-771 (no @holding case) | search |
| scripts/model:read_records (633-664) | a record with id needs a `kind` in RECORD_KINDS | r9 writes the id; kind not required by r9 (2.3) | none (`by search`: test_design_model_check.py:279, 1305-1307 write `kind:`) | search |
| scripts/model:read_work (666-) | each `.shop/work/<dir>` needs `initiative.md` | r1 moves `work/` dirs without writing `initiative.md` (2.6) | test_design_model_check.py:228-257 (no initiative cases) | search |
| scripts/model:read_capabilities Behaviour (557-576) | a no-id Behaviour line is a `#line` requirement, violation v15a | r10 gives those lines ids | none (`by search`: no test names v15a with an old-form line) | search |
| scripts/model:read_capabilities rests_on (536-539) | `decision/<name>` is unresolved (2.4) | r5 rewrites them to design-decision ids in files | none (`by search`) | search |
| scripts/model:read_index (474-490) | spec/index.md id must be bounded-context/<owner>/<product>/<name> | r4 writes it from `--context` | tests/scenarios/test_design_model_check.py (index cases) | search |
| scripts/workqueue.py, scripts/work, scripts/supervise.py | read or write `.shop/work/` (already final layout) | none | test_work_queue.py, test_supervision.py | search |

Also: scripts/features and scripts/model have no `.py`, so `import` cannot name them; reuse by path only (read). The work-item's "reuses scripts/model's reading of frontmatter" means loading `scripts/model` by file path (importlib) or by subprocess.

## 4. Tests the requirements make impossible to keep

None. `by search`, and read of each listed test:
- tests/scenarios/test_feature_file_tools.py deprecate tests (648-771): sound as is; `features deprecate` is not changed by the work-item, and no test pins `@holding` through it.
- tests/scenarios/test_design_model_check.py:176-180 and 653-655: sound; `@holding` and OLD_LAYOUT behaviour is unchanged.
- tests/scripts/test_plan.py and test_measure.py: their old-path fixtures run in temporary directories and test only `plan`/`measure` code, which the work-item does not change; sound (read, not run).
- tests/scripts/test_bound.py: passes today (run); it stays green when the migration feature is added to its list and bound once.
Not checked: the full suite was not run (by rule).

## 5. A stage the work-item skips

The work-item's migrate reuses `features deprecate` and `git mv`, and r6 requires `model check` after the run; migrate itself runs neither check.

5a. `features deprecate` (existing way, `scripts/features:cmd_deprecate` via `write_checked`). If migrate converts @holding by its own code instead, these are lost (all shown by 2.8 run):
  - refusal: no `--for`/`--for-removal` (rc=2);
  - refusal: title in several files, unless `--file` (rc=1);
  - refusal: already deprecated / title not found (rc=1);
  - refusal: any `Rule:` block in `--dir` refuses the whole directory (rc=1);
  - effects: "(deprecated)" appended to the title; `Deprecated for: removal` line at the first step's indent; `@deprecated` added to the last tag line; text re-parsed by `write_checked` before any write (read).

5b. `git mv` (existing way: plain `git mv`). Refusals: destination exists; source untracked; a missing parent (file or directory); a directory moved onto an existing directory nests inside it, rc=0 (2.9, run). Effects: the rename is staged only, no commit (`A` in status, run); and the moves are not atomic: when one fails, earlier moves stay (run: `A b.md` staged, `c.md` failed). r7 needs every check before the first `git mv`.

5c. `model check` (existing way, `scripts/model`). Not run by migrate; these are effects only it produces, all shown in 2.2-2.7 (run): the layout problems, `no initiative.md`, `kind None is not a record kind`, `decision/<name>` unresolved, `v15a` for no-id lines, `@holding`. r6 is a claim about this stage, so migrate's output must make each of them go away by construction.

## 6. Defects

D1. `features deprecate` lands a file that `model check` rejects, with no refusal.
Reproduction (run): repo with `features/thing.feature` containing `@holding` on scenario `s1` (plus an `@r1` scenario).
  `python3 <worktree>/scripts/features deprecate s1 --for-removal` -> rc=0, `features/thing.feature: s1 (deprecated)`.
  The scenario now carries `@holding @deprecated` (tag line `  @holding @deprecated`).
  `python3 <worktree>/scripts/model check` -> rc=1, `file: features/thing.feature: scenario 's1 (deprecated)' is tagged @holding; the tag is @deprecated`.
Note: whether this is a defect depends on whether `@holding` should be deprecated by `features deprecate` at all; the capability feature-file-tools does not say. Conflict with r3 in part 6 of the notes only; no judgement made.

Other probes (2.1-2.10) showed no further wrong behaviour; the rest are refusals or reported problems the contracts describe.

## 7. The file set

Changed by the work-item:
- scripts/migrate (new): the `migrate run --context` script; stdlib only (`spec/capabilities/migration-tools.md` Implementation); reuses `scripts/model` and `scripts/features` by path (the file has no `.py`, read).
- tests/scenarios/test_migration_tools.py (new): `scenarios("migration-tools.feature")` once (test_bound requires exactly one test per scenario) and the step definitions; the `run` fixture in tests/scenarios/conftest.py runs `scripts/<name>` by path (read: `SCRIPTS / script`), so no fixture change is needed.
- tests/scripts/test_bound.py: add `features/migration-tools.feature` to BOUND_BY_PYTEST_BDD (its comment says i8 adds it) (read, run today: passes).

Not changed, but on the change's path (line counts by `wc -l`; room: no limit stated, CLAUDE.md absent, no size rule in pyproject/setup.cfg/.importlinter):
- scripts/model: 1035 lines; no limit stated. Read by migrate for frontmatter and layout (reuse by path).
- scripts/features: 657 lines; no limit stated. `deprecate` reused.
- tests/scenarios/conftest.py: 169 lines; no limit stated. `run` fixture used by the new tests.
- tests/scripts/test_bound.py: 31 lines; no limit stated (edited above).
- scripts/migrate: new, 0 lines today; no limit stated.
- tests/scenarios/test_migration_tools.py: new; no limit stated.

Open points for the plan (both readings given, not chosen):
- r3: "as features deprecate does" + "no @holding tag left" vs the probe 2.1 output (features keeps @holding). Reading A: migrate runs `features deprecate` then removes `@holding`. Reading B: migrate sets `@deprecated` itself and drops `@holding`. The r3 scenario's copy (`features deprecate` run on a copy) would then keep @holding, which contradicts r3; reading A makes the scenario's expected file differ from the copy.
- r6: model check needs `initiative.md` in each `.shop/work/<dir>` and `kind:` on moved records; neither is in r1-r11. Reading A: migrate writes them. Reading B: the scenario's fixture supplies them.
