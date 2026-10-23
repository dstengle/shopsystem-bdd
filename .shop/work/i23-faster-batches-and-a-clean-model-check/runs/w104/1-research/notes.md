# Research of w104: model check's own gaps

Method: `tools` from the plugin 0.24.0 scripts. `tools map` has no map, so `tests-of` and `untested` are unavailable; test lists below are `by search` (grep of tests/) unless stated. `refs` works. The worktree's `scripts/model` is the system under probe. Scratch: `.shop/scratch/w104-1-research/` (probe_model.py, probe_counts.py, probe_workitem.py; git-ignored).

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q --tb=short <node id>` for each of the 7 accepted scenarios (18 node ids, from `tests/scenarios/test_design_model_check.py`). Result: 5 failed, 13 passed (run).

- **a bounded context with no job gets no unserved-capability warning** (`::test_a_bounded_context_with_no_job_gets_no_unservedcapability_warning`): red. StepDefinitionNotFound for `Given a bounded context with one capability and no job` (line 77). The step `a bounded context with one capability` exists at `tests/scenarios/design_model_check_given.py:15`, not this text. Code also red: `scripts/model.lp:275-276` `w_unserved_cap` has no job guard; probe P1 prints it.
- **a malformed work directory or work file is a file problem** (Outline, 9 rows): 8 rows pass. Row `the part p1.md has the kind capability-proposal and the status built`: red, `AssertionError` at `tests/scenarios/design_model_check_problems.py:101`. The step `malformed_work` (lines 77-102) has no branch for this case and falls to the final assert. Code is correct already: probe P12 gives `file: .shop/work/i1/p1.md: status 'built' is not one of ...`. Red is test-side only.
- **a work-item accepting a requirement no scenario names is a file problem** (`::test_a_workitem_accepting_a_requirement_no_scenario_names_is_a_file_problem`): passes today (run). Keep as guard.
- **a work-item accepting a requirement of a guarantees capability ... is no file problem**: red. StepDefinitionNotFound `Given a capability thing in the guarantees group with requirement r2 that no scenario names` (line 319). The nearest steps are `design_model_check_given.py:57` (service group) and `design_model_check_problems.py:256` (other wording). Code red: `scripts/model_work.py:191` raises the problem with no group test. Probe P2 shows the file problem.
- **a green work-item accepting a retired id is no file problem**: red. StepDefinitionNotFound `Given a capability thing whose frontmatter lists r2 as retired` (line 327). Code red: `scripts/model_work.py:191` has no retired or green test. `self.retired` exists (`model_facts.py:49`, filled at `:189`). Probe P4 shows the file problem.
- **a work-item with no accepts and no check is v_w4, unless it is withdrawn** (Outline, 4 rows): all 4 pass (run).
- **a work-item accepting a requirement no scenario names yet, with no check, is not v_w4**: red. KeyError `'accepts thing#r2 and no check'` at `tests/scenarios/design_model_check_one_each.py:41`; `FIELDS` (lines 32-34) has no such key. Code red: `scripts/model_work.py:188-190` writes the `accepts` fact only for named scenarios, so `model.lp:65` `has_accepts` is false and `model.lp:236` `v_w4` fires. Probe P8 shows v_w4.

## 2. What the system answers today

Probes (run). Command for each: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w104-1-research/probe_model.py`, which builds each repo under `repos/` and runs `python3 scripts/model --root <repo> check`. Trimmed results:

- P1 one service capability, `@r1` scenario, no work: `warning w_unserved_cap ... (1)`, rc 1 (the rc comes from a v_e1 row, a fixture artefact: "- [r1] One." is not EARS). Red for the no-job scenario.
- P2 guarantees, r2 no scenario, drafted work `accepts [thing#r2]`, check true: `file: .shop/work/i1/w1.md: accepts ...thing#r2, which no scenario names yet`. Red.
- P3 service, same: same file problem, plus `v_s3` on r2. Passes today.
- P4 retired r2, service, green work accepts thing#r2: same file problem. Red.
- P5 retired r2, drafted work accepts thing#r2: same file problem. Correct under r27.
- P6 retired r2 on guarantees, green work: same file problem. Red (nearest case).
- P7 drafted work accepts `ghost#r2` (no capability ghost): `file: ...accepts capability/acme.com/shop/cart/ghost#r2, which no scenario names yet`; `0 unresolved references`. Nearest case; see D5.
- P8 service r2 no scenario, drafted, accepts thing#r2, no check: `v_w4 a work-item has no acceptance and no check (1)` plus the file problem. Red.
- P9 guarantees r2 no scenario, drafted, accepts thing#r2, no check: `v_w4` plus file problem. Red (nearest).
- P10 service r2 no scenario, withdrawn, accepts, no check: no file problem, no v_w4. Correct (withdrawn exemption).
- P11 r1 named by a scenario, drafted, accepts thing#r1, no check: no v_w4, no file problem. Correct.
- P12 part with kind capability-proposal and status built: `file: .shop/work/i1/p1.md: status 'built' is not one of approved, drafted, formulated, merged, withdrawn`. Correct.
- P13 guarantees, range `thing#r1-r2`, r2 no scenario, drafted: file problem on r2. Red for guarantees.
- P14 service, r2 only in a `@deprecated` scenario, drafted, accepts thing#r2: file problem on r2. Correct (deprecated names nothing).
- P15 bounded context only, no capability: `0 violations, 0 warnings`. Correct.
- P16 (probe_counts.py) the setup of `tests/scripts/test_model_output.py` (one capability, rests_on nope, stray feature, no job): `1 violations, 1 warnings, 1 unresolved references, 1 file problems`; the one warning is `w_unserved_cap`. Run.
- Work-item path (probe_workitem.py, `pytest -p work_items --work-item w1`, run): accepts `thing#r1` (named): `1 passed`, rc 0. Accepts `thing#r2` (unnamed only): `INTERNALERROR ... SystemExit: --work-item w1: w1 accepts none of the scenarios it collected`, rc 3.

Read: `serves/2` is never produced (grep of `scripts/model*.py`: none), so `w_unserved_cap` fires for every capability. Jobs are not read in this context (`model_facts.py:24-26` lists job kinds only; r19 lists no job file), so "no job" is always true here.

Nearest cases not probed: two capabilities with no job (same rule, read).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model_work.py:read_part` accepts loop, 184-192 | `accepts` fact only for requirements a scenario names; problem for every unnamed one not `withdrawn` | `accepts` fact for every accepted requirement; problem only if not withdrawn, not guarantees, and not retired-and-green | by search: `tests/scripts/test_model_withdrawn.py:17` (passes); `tests/scenarios/design_model_check_problems.py:105`; `design_model_check_one_each.py:32` | refs (read_part: 1 use, in `read_work`); read |
| `scripts/model.lp:65` `has_accepts`, `:236` `v_w4` | true only with an `accepts` fact (named) or a check | an unnamed accept also satisfies v_w4 | by search: `design_model_check_one_each.py` (red row) | read; probe P8 |
| `scripts/model.lp:275-276` `w_unserved_cap` | fires for every capability (serves/2 never produced) | silent while the context has no job | by search: `tests/scripts/test_model_output.py:14-18` (run, passes today; breaks, see Part 4) | read; probe P16 |
| `scripts/supervise_brief.py:accepted_scenarios` 89-96 | lists the scenario lines of each accepted requirement; none for an unnamed one | same; brief has no "Accepted scenarios:" line for an unnamed accept | by search: `tests/scenarios/supervision_then_workers.py:217` (named case only) | read |
| `scripts/work_items.py:pytest_collection_modifyitems` 99-107 | refuses a run that collects scenarios when none is one the work-item accepts | an unnamed-only accept is refused at test time | by search: `tests/scripts/test_work_items.py:67-69`, `:79-83` (refusal of other#r1; not run) | read; probe_workitem (run) |
| `scripts/work_items.py:expect_red` 77-89 | keys xfail on scenario tags from `acceptors` | unnamed accepts never match a scenario tag, so nothing is marked; no change needed | none found by search | read |
| `scripts/model_work.py:164-169` retired ids on proposals | `SETTLED` proposals may name a retired id | unchanged; the green exemption is for work-items, not proposals | by search: `tests/scripts/test_model_reading.py:59` (not read) | read |

## 4. Tests the requirements make impossible to keep

Test lists by search (`tests-of` has no map). Sources: `grep` of `tests/` for `warning`, `accepts`, `v_w4`, `w_unserved`, `names yet`, `accepts\(`, `--work-item`.

- `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts`: ran, passes today. Asserts `1 violations, 1 warnings, 1 unresolved references, 1 file problems`. Its one warning is `w_unserved_cap` (P16). After r111 the context has no job, so the warning goes and the line reads `0 warnings`. It cannot pass as written. Mechanism: `model.lp:275-276`.
- `tests/scripts/test_model_output.py::test_exit_codes_of_check`: ran, passes. The "a warning alone exits 0" case uses `w_uncited_obs`, so it stays. Sound.
- `tests/scripts/test_model_output.py::test_rows_of_a_violated_relation_are_limited`: ran, passes; no warning count. Sound.
- `tests/scripts/test_model_withdrawn.py::NotReadTest::test_r27_a_withdrawn_work_item_accepting_a_requirement_no_scenario_names_is_no_file_problem`: ran, passes. Its capability is service with no retired id, so drafted still gives 1 problem and withdrawn 0. Sound.
- `tests/scripts/test_work_items.py` (7 tests): read; the plugin is not edited and the refusal is for `other#r1`. Sound.
- `tests/scripts/test_model.py` (213 lines): by search, no assertion on accepts, v_w4 or w_unserved. Sound by search; not run.
- Scenario test `design_model_check_problems.py:105-110` (the file-problem scenario for a service requirement accepted without scenario): pass today (run) and stay passing under the change. Sound.

## 5. A step the work-item skips

- **Accept-only path**: a work-item accepting only an unnamed requirement is refused by `pytest --work-item` (run, probe_workitem: rc 3, "accepts none of the scenarios it collected"). Its own test step cannot run. With the change, `v_w4` is satisfied by such an accept alone, so model check passes a work-item with no check and no test for it (read, from `model.lp:236` once `accepts` is written for unnamed requirements).
- **Brief**: `supervise_brief.accepted_scenarios` gives the researcher no scenario line for an unnamed accept (read).
- **Retired and green**: the same pytest refusal applies, since the retired id has no scenario (read; not run).
- **Guarantees exemption**: `work_items.py:expect_red` never marks an unnamed requirement's scenarios xfail, since none exists to mark (read).

## 6. Defects

Each shows today's behaviour the requirements change. Reproduction: `python3 scripts/model --root <repo> check` on the repo built by `probe_model.py` (named case).

### D1 warning for a context with no job
Repo: `spec/index.md` (id `bounded-context/acme.com/shop/cart`), `spec/capabilities/thing.md` (group service, `- [r1] **When** asked, \`thing\` shall answer.`), `features/thing.feature` with `@r1`. Output: `warning w_unserved_cap  a capability serves no job  (1)`. Wrong under r111 (run: P1).

### D2 guarantees requirement accepted without a scenario
As P2 with group guarantees. Output: `file: .shop/work/i1/w1.md: accepts capability/acme.com/shop/cart/thing#r2, which no scenario names yet`, rc 1. r27 says no file problem (run).

### D3 green work-item accepting a retired id
As P4: capability lists `retired: [r2]`, green work `accepts: [thing#r2]`. Output: the same file problem, rc 1. r27 says no file problem (run).

### D4 unnamed accept without check is v_w4
As P8: service r2 with no scenario, drafted work `accepts: [thing#r2]`, no check. Output: `v_w4 a work-item has no acceptance and no check (1)`. r106 says not v_w4 (run).

### D5 accept of a requirement no capability has
As P7: `accepts: [ghost#r2]`, no capability `ghost`. Output: `accepts capability/.../ghost#r2, which no scenario names yet`, and `0 unresolved references`. The message names the wrong cause; no row says the requirement does not exist (run). Whether this is wrong under r27 is for the plan (see questions).

## 7. The file set

Production:
- `scripts/model_work.py`: `read_part` accepts loop 184-192: write `accepts` for every accepted requirement; problem only if not withdrawn, not guarantees (`self.caps[cap]["group"]`), and not retired-and-green (`self.retired`, status `green`). 211 lines, room 89.
- `scripts/model.lp`: `w_unserved_cap` (275-276) guarded by a job node; `v_w4`/`has_accepts` (65, 236) unchanged. 304 lines; not Python, so the 300 limit does not apply.

On the path, not edited: `scripts/model` (137 lines, room 163), `scripts/model_check.py` (139, room 161), `scripts/model_facts.py` (275, room 25; holds `caps`, `retired`), `scripts/model_parse.py` (271, room 29), `scripts/work_items.py` (109, room 191; refusal of unnamed-only accept), `scripts/supervise_brief.py` (110, room 190).

Tests that must change:
- `tests/scenarios/design_model_check_given.py` (228, room 72): add steps `a bounded context with one capability and no job`, `a capability thing in the guarantees group with requirement r2 that no scenario names`, `a capability thing whose frontmatter lists r2 as retired`.
- `tests/scenarios/design_model_check_problems.py` (289, room 11): add the branch for `the part p1.md has the kind capability-proposal and the status built` in `malformed_work` (lines 77-102). A branch of more than 11 lines would take the file over 300; the plan must split it first.
- `tests/scenarios/design_model_check_one_each.py` (47, room 253): add `FIELDS` key `accepts thing#r2 and no check`.
- `tests/scripts/test_model_output.py` (74, room 226): `test_check_ends_with_the_four_counts` expects `1 warnings`; it must change or its setup must, once r111 holds.

Size: `tools size --limit 300` prints nothing (no tracked Python file over 300) (run).

Not in the set: `features/design-model-check.feature` (scenarios exist); `spec/capabilities/design-model-check.md` (r27, r106, r111 are in it already, read).

## Questions for the plan

- What is the `accepts` fact for a requirement: a scenario id as today, or a requirement id as well? `model facts` has no test of `accepts(`, so either shape passes the tests.
- D5: should a work-item accepting a requirement no capability has be an unresolved reference, or stay a file problem with a different message?
- The job guard: this context never reads jobs, so "no job" is always true here. Does r111 mean a guard on job nodes, or a fixed silence?
- `test_check_ends_with_the_four_counts` expects a warning that r111 removes: change the expected count, or the setup?
