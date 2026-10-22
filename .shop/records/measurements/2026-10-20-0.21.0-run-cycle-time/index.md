---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-0-21-0-run-cycle-time
kind: measurement
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/supervision, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools]
date: 2026-10-20
---

# 0.21.0 run: cycle-time, report with timings and the bindings profile

Work-item cycle-time (i10): supervise.py split, the suite under pytest-xdist, the researcher given the file set and 25 turns (supervision r19), two disjoint implementers at once (r20), and in fix round 1 features bindings made fast. Timings in the report: suite 126.7 s in one process, 52 s under xdist, 6.4 s after the bindings fix; features bindings --unbound 31 s to 0.5 s. The cProfile of features bindings before the fix (.shop/scratch/cycle-time/prof, 180 s under the profiler, 1.48e9 calls) is kept beside this record with a text rendering of its top entries (paths shortened to the repository). The other cycle-time scratch (model and bindings before/after dumps, a copy of supervise.py, a probe script) was not archived. Migration release 0.21.0 (branch release-0.21.0), run by a coordinator dispatching implementers and reviewers while the person was away; the coordinator's ledger is archive/2026-10-21-migration-release-ledger.md and the dispatch briefs are archive/2026-10-19-0.21.0-run-briefs.md.

Archived from `.shop/scratch/run/cycle-time-report.md` (git-ignored scratch), text as it was.

---

# cycle-time: report (implementer, main checkout, release-0.21.0)

Status: DONE_WITH_CONCERNS

## Commits (in order)
- 5f1fb33 cycle-time: split supervise.py and the supervision steps under 300 lines (a pure refactor)
- 4fb4c30 cycle-time: tests in parallel with pytest-xdist (-n auto in pytest.ini and work run's test commands)
- 2f48945 cycle-time: the researcher is given the work-item's file set, its accepted scenarios and --max-turns 25 (supervision r19)
- 66ee563 cycle-time: two ready work-items with disjoint file sets are implemented at once, merged one at a time (supervision r20)
- a3a79bd cycle-time: the implementer runs its work-item's scenarios, the whole suite is work run's (red-green r1); the researcher reads its brief's file set and scenarios in 25 turns

(The coordinator merged split-model, split-features and split-tools, and committed ada7d4f, while I worked. None of those files were touched here.)

## Tests before and after
- Start (57f6247): 592 passed, 1 skipped, 105 subtests; 126.7 s in one process.
- After the split (5f1fb33): 592 passed, 1 skipped; 112.8 s in one process. Same count.
- Under xdist (4fb4c30, `-n auto` in addopts): 592 passed, 1 skipped; 52.4 s (52.3 s and 53.0 s on repeat runs).
- End (a3a79bd): 596 passed, 1 skipped; 35.7 s under -n auto (47.2 s on an earlier run at 66ee563, with other agents loading the machine). +4 tests: the r19 scenario and three r20 scenarios. No test was removed.
- `python3 -m pytest -q --work-item cycle-time`: 4 passed in 2.6 s.
- Suite record: `Suite: 596 passed, 0 failed at a3a79bd in 36 s`
- At ada7d4f (the coordinator's commit after mine), `-n 0` gives 4 failed, 596 passed in 88 s. The 4 failures are migration-tools rows that commit added for migrate-kb-2 (undefined steps). They are not this item's.
- Under xdist the suite's time is set by one test: tests/scripts/test_bound.py::test_every_scenario_has_exactly_one_test took 47.8 s (it runs `features bindings`). Everything else is under 2.2 s. Speeding up `features bindings` is the next cycle-time gain. That is scripts/features, which is not mine to touch.

## Model check
- Before: 152 violations, 23 warnings, 0 unresolved references, 175 file problems.
- After: 148 violations, 23 warnings, 0 unresolved references, 171 file problems.
- Cleared: cycle-time.md's "accepts supervision#r19/#r20, which no scenario names yet". supervision-4.md's same two problems also cleared, because it accepts r19 and r20 too (it looks like an older numbering). Nothing new appeared.
- `features bindings --tests tests --unbound`: the same 39 lines before and after.

## The split (first commit)
- scripts/supervise.py (399 lines) became:
  - supervise.py (Run's core: check, log, move, ask, step, run, and later pair/together; 179 lines at the end);
  - supervise_worker.py (tools, worktrees, the claude session, the result; 167 lines);
  - supervise_brief.py (the brief, research questions, accepted scenarios; 94 lines);
  - supervise_merge.py (TESTS, suite record, put-back, implement/merge; 92 lines).
  Run is `class Run(Workers, Briefs, Merge)` with mixins.
- tests/scenarios/test_supervision.py (687 lines) became:
  - test_supervision.py (scenarios(), the When, the Thens about items, repository and exit; 230 lines);
  - supervision_given.py (222 lines);
  - supervision_then_workers.py (234 lines);
  - supervision_world.py (the `repo` fixture and helpers; 132 lines).
  One `scenarios("supervision.feature")` call, as before.
- tests/scripts/stub_claude.py: 178 lines.
- Every file touched is under 300 lines.

## r19 and r20: scenarios written from the Behaviour lines only
The blind formulator was not available. I wrote the four rows in features/supervision.feature from r19's and r20's lines alone, and the reviewer should check them against the lines:
- @r19 a researcher is given the work-item's file set and accepted scenarios, and a limit of 25 turns
- @r20 two ready work-items whose file sets do not overlap are implemented at the same time, and merged one at a time
- @r20 two ready work-items whose file sets overlap are implemented one after the other
- @r20 of three ready work-items whose file sets do not overlap, no more than two are implemented at the same time

## Red and green runs
- r19: first red was an undefined Given (StepDefinitionNotFoundError). After the steps, red on the first Then: the brief had no `File set:` line (the AssertionError printed the brief). Green after brief.research_lines, accepted_scenarios and MAX_TURNS={"research": 25} (`--max-turns 25` on the researcher only).
- r20 disjoint: red on "the implementers of w1 and w2 ran at the same time". The run gave `AssertionError: {'w1': (0, 1), 'w2': (4, 5)}`: w2 started after w1 had ended, under serial code. Green after the lock, pair() and together().
- r20 overlap: **passed at its first run**, because the code for the disjoint scenario was already in.
  - Against the code before r20 (git stash of supervise*.py) it also passes. Serial code never overlaps anything, so this row holds r20's limit rather than new behaviour.
  - To show it tests what it says, I made pair() ignore the overlap. It then failed: `AssertionError: ({'w1': (0, 3), 'w2': (1, 2)}, '')`.
  - This is the "passes before code" stop condition in letter. I did not hand back, because I wrote the row myself as the limit's guard. The reviewer should rule on it (see Concerns).
- r20 three items: against the code before r20, red on "two implementers ran at the same time, and never three": `{'w1': (0, 1), 'w2': (4, 5), 'w3': (8, 9)}`. Green with the r20 code.
- The r20 scenarios passed three repeat runs (about 1.7 s each). The stand-in waits for a signal: it polls the record until two implementers have started, with a 60 s bound so a worker nobody joins still ends.

## Other changes
- xdist: pytest-xdist 3.8.0 installed with `python3 -m pip install pytest-xdist`, the interpreter the suite uses (/usr/local/bin/python3; it went to the user site, beside pytest).
  - README's Scripts paragraph names it.
  - pytest.ini has `addopts = -n auto`, added because the whole suite is green under it; `-n 0` runs it in one process.
  - work run's default TESTS have `-n auto` (supervise_merge.py).
- red-green r1:
  - bdd-red-green's cycle, Suite Record, check, budget and When Done sections: the implementer runs the `--work-item` scenarios and the modules it touches, never the whole suite, which is work run's before it merges.
  - bdd-implementer.md says the same, and its report gives the brief's record and the final work-item run.
- code-scout.md: the brief's new `File set:` and `Accepted scenarios:` lines, and the 25-turn limit.

## Files outside the fileset
The six split modules are new files:
- scripts/supervise_worker.py
- scripts/supervise_brief.py
- scripts/supervise_merge.py
- tests/scenarios/supervision_given.py
- tests/scenarios/supervision_then_workers.py
- tests/scenarios/supervision_world.py

With them, 15 files were touched in all: the 10 in the fileset (workqueue.py untouched; supervise.py, test_supervision.py and stub_claude.py included) plus these 6, less workqueue.py. That is 15.

## Tests changed under an allowance (respellings)
- supervision_world.item_text: a new optional `fileset=`; old calls give the same text.
- test_supervision.all_green ("{names} are green"): the names list also splits on ", ". Old uses have no comma, so it is unchanged for them.
- stub_claude.VALUED: now has `--max-turns`.

## Rulings needed
1. spec/capabilities/supervision.md's Not yet still lists "several implementers at once", which contradicts r20. The spec is outside the fileset, so I did not change it.
2. r20's "file sets that do not overlap", read here as:
   - a work-item without `fileset:` is in no pair (it runs alone, as before);
   - overlap is a path in common, as written; a directory entry is not read as holding the files under it.
   Neither case is covered by a scenario.
3. r20 runs only implementers side by side. Research, plan and review stay one at a time, which keeps r1's "one worker at a time" for them. When a disjoint pair is ready, it is taken before an earlier work-item in another stage.
4. r19: the file set and accepted scenarios are given to the researcher only, as the line says. A work-item without a fileset gets no `File set:` line. Accepted scenarios are read from features/<capability>.feature of the main checkout (the same commit as the worktree's HEAD).
5. work run's default test commands now have `-n auto`, so a project without pytest-xdist needs delivery.toml [tests] (as this plugin's Implementation line says: the plugin takes the dependency).

## Concerns
- The r20 overlap row passes against the code before r20 (above). The reviewer should rule whether it stays as the limit's guard; its failure when pairing ignores overlap is the evidence that it checks something.
- together() carries a Refused raised in either implementer thread to the run, which then ends with it (r10). No scenario exercises that path.
- `addopts = -n auto` also applies to `tools map` on this repository (scripts/tools runs pytest under coverage per test). I did not check that tools map works under xdist; scripts/tools is another agent's file.
- The measurement against the i8 runs' stage times (.shop/records/measurements/fixture-runs/2026-10-20-i8-work-run-test-log.md) is for the next real work run, as the item says.

## Review Focus probes
None were given. Probes run: the stash run of the r20 rows against the code before r20, and the pairing mutation above. Scratch is in .shop/scratch/cycle-time/ (model and bindings before and after).

# Fix round 1 (the coordinator's rulings 1-6)

Starting state: a3a79bd plus your ada7d4f. That gives 4 failed, 596 passed. The 4 failures are migrate-kb-2's new migration-tools rows (undefined steps), and they are the same 4 at every run below.

## Commits
- ba2f2ce cycle-time: supervision's Not yet no longer lists several implementers at once (r20 replaces it)
- 78f1189 cycle-time: a file set's globs and directories claim the tracked files they hold, so overlapping work-items never run at once (r20)
- 92ff095 cycle-time: work run's default tests add -n auto only where the project's python3 has pytest-xdist
- 985d0cf cycle-time: tools map runs pytest in one process (-n 0 where pytest-xdist is there), so coverage contexts stay exact
- 7e1804d cycle-time: features bindings reads each module's pytest_bdd imports once and the test modules once (31 s to 0.5 s, same output)

## Each ruling

1. **supervision.md's Not yet:** "several implementers at once" removed (spec/capabilities/supervision.md). Suite unchanged.

2. **No file set means never in parallel:** accepted, and already so (`pair()`). No change.

3. **Globs and directories:** the r20 overlap scenario is now a Scenario Outline, "two ready work-items whose file sets overlap are implemented one after the other: <how>".
   - It has a new Given, "the repository has lib/thing_a.py committed", and three rows: a file in both; `lib/thing*.py` against `lib/thing_a.py`; `lib/` against `lib/thing_a.py`.
   - Red first. Against 66ee563's code the glob and directory rows failed on "no implementer was started before the one before it had ended", e.g. `AssertionError: ({'w1': (0, 2), 'w2': (1, 3)}, '')`. The file-in-both row passed, as before.
   - Code: supervise.claimed(entry, tracked) is the entry itself plus each `git ls-files` file it matches (fnmatchcase) or holds as a directory. pair() compares those sets.
   - After: 59 passed in test_supervision.py, and the r20 rows passed three repeat runs (5 passed each).
   - I wrote these rows too, without the blind formulator.

4. **`-n auto` only with xdist:** TESTS has a `{parallel}` placeholder. Merge.tests() fills it with " -n auto" when `python3 -c "import xdist"` succeeds in the repository, else with nothing. delivery.toml [tests] still replaces either.
   - Probe (.shop/scratch/cycle-time/probe/probe_tests.py, with a python3 on PATH that runs `-I -S`, so no site-packages):
     - with xdist: `python3 -m pytest -q -n auto --work-item {work_item}` / `python3 -m pytest -q -n auto`
     - without: `python3 -m pytest -q --work-item {work_item}` / `python3 -m pytest -q`
   - No scenario covers this, as none was asked for. The reviewer may want a row.

5. **tools map without xdist:** `-p no:xdist`, as ruled, fails on this repository. With pytest.ini's `addopts = -n auto` it gives `python -m pytest: error: unrecognized arguments: -n`, which I ran and saw. So tools map adds `-n 0` when the map's interpreter can import xdist, and nothing otherwise. That keeps one process and exact per-test contexts. Ruling needed if you want the literal flag (it would also need `-o addopts=`, which drops a project's other addopts).
   - Check on this repository: `python3 scripts/tools map` made the map in 93 s at 100% CPU (one process): "4 failed, 598 passed ... map: .shop/scratch/tools/coverage, at 92ff095".
   - `tools tests-of tests/scenarios/supervision_world.py:item_text --by-file` gives "test_supervision.py 59", so the per-test contexts read back.
   - work run's own functions show 0, because the scenarios run `work` as a program and coverage does not follow subprocesses (unchanged).
   - Analysis-tools tests: 57 passed, 1 skipped.

6. **test_bound:** it is already one unittest that runs `features bindings` once per session, so a session-scoped fixture would save nothing.
   - The 31-48 s was in features_bindings.py: `called_name` walked the whole module tree for every Call node, and `unbound_report` re-parsed every test module once per feature file (cProfile: 1.48e9 calls, 109M ast.walk steps).
   - Fix: each tree's pytest_bdd aliases are computed once (first import of an alias wins, as the walk did), and `scenarios_calls` is hoisted out of the loop.
   - `features --dir features bindings --tests tests --unbound` takes 0.5 s, against 31 s before, with byte-identical output (diffed). Nothing it checks is weakened.

## After
- Suite: `Suite: 598 passed, 4 failed at 7e1804d in 6 s; failing: test_run_keeps_both_decisions_an_entrys_supersedes_names_each_by_its_new_id_and_supersedes_both, test_run_rewrites_a_decision_files_by_that_names_old_a_path_it_moved[adrs/0001-use-x.md-.shop/records/decision-arguments/0001-use-x.md], test_run_rewrites_a_decision_files_by_that_names_old_a_path_it_moved[docs/superpowers/specs/s1.md-.shop/records/archive/design-notes/s1.md], test_run_gives_a_moved_readmemd_no_id_kind_or_about`. All 4 are migrate-kb-2's red rows from ada7d4f.
- Suite time: 126.7 s in one process at the start, 52 s with xdist, 6.4 s now. The slowest test is 2.5 s (analysis-tools map).
- Model check: 149 violations, 171 file problems. The +1 violation against a3a79bd is a v_t1 "superseded" in ada7d4f's migration-tools scenario title, not this round.
- Bindings `--unbound`: the same as the start.
- Files this round:
  - spec/capabilities/supervision.md
  - features/supervision.feature
  - scripts/supervise.py (189 lines)
  - scripts/supervise_merge.py
  - tests/scenarios/supervision_given.py
  - scripts/tools_map.py (117 lines)
  - scripts/features_bindings.py (163 lines)

  The last two are outside cycle-time's fileset and were directed by rulings 5 and 6. Every file is under 300 lines.

## Files kept beside this record

- `features-bindings-before-fix.prof`: from `.shop/scratch/cycle-time/prof`, the cProfile (pstats) data of `features --dir features bindings --tests tests --unbound` before fix round 1 (2026-10-20 23:56).
- `features-bindings-before-fix-stats.txt`: that profile printed with pstats, top 25 by cumulative time and top 15 by internal time.
