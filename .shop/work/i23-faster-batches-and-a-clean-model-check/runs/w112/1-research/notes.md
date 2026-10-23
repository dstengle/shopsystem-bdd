# w112 research notes

Tools: `tools refs` works. `tools tests-of` and `tools untested` have no map (`tools: no map`); I did not make one (it runs the whole suite). Every test list below is `by search` (grep over tests/) or `read`. Probes: `.shop/scratch/w112-1-research/probe_w112.py` (P1-P9), `probe_w112_plugin.py` (P10-P12), `probe_w112_p10noxdist.py` (P10 rerun). Each is `run` with `python3 -m pytest -q -s -n 0 <path>`. Fixture note: my work-items sit in an initiative whose first part is not a capability-proposal, so P2-P7 also print v_b1 and v_k3; those are fixture noise, not answers.

## 1. Why each accepted scenario is red today

Command: `python3 -m pytest -q --tb=short <18 node ids>` (ids from `--collect-only` of `tests/scenarios/test_design_model_check.py`). Run: 13 passed, 5 failed.

- r111 "a bounded context with no job gets no unserved-capability warning": StepDefinitionNotFoundError, Given "a bounded context with one capability and no job" (feature line 77). No such step: `tests/scenarios/design_model_check_given.py:15` has "a bounded context with one capability" only. Behind it: `scripts/model.lp:276` `w_unserved_cap(C) :- node(C,"capability"), not serves(C,_).` has no job condition; P1 prints the warning.
- r27 "a green work-item accepting a retired id is no file problem": StepDefinitionNotFoundError, Given "a capability thing whose frontmatter lists r2 as retired" (line 327). No such step (`design_model_check_given.py:52` is the r4 variant). Code: `scripts/model_work.py:191` `if not found and data.get("status") != "withdrawn":` has no green-and-retired exemption; P4 prints the file problem.
- r27 "a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem": StepDefinitionNotFoundError, Given "a capability thing in the guarantees group with requirement r2 that no scenario names" (line 319). No such step (`design_model_check_given.py:57` is service group). Code: same line `model_work.py:191`, no group test; P3 prints the file problem.
- r106 "a work-item accepting a requirement no scenario names yet, with no check, is not v_w4": KeyError 'accepts thing#r2 and no check' at `tests/scenarios/design_model_check_one_each.py:41`; `FIELDS` (line 32) has no such key. Code: `scripts/model_work.py:184-192` writes the `accepts` fact only when a scenario is found (`found`); no fact, so `model.lp:65` `has_accepts` is false and `v_w4` (`model.lp:236`) fires. P2.
- r27 outline row "the part p1.md has the kind capability-proposal and the status built": AssertionError at `tests/scenarios/design_model_check_problems.py:101` (`assert case == "initiative.md has a date written 16/10/2026", case`): the given has no branch for this row. Code already prints the file problem (P9), so the gap is in the step only.

Passing today (13, run): 8 malformed-work rows; r27 "accepting a requirement no scenario names is a file problem" (service group); the 4 v_w4 outline rows.

## 2. What the system answers today

Probes run against `scripts/model` in the worktree, on repositories under `.shop/scratch/w112-1-research/repos/`.

- P1 (run): one capability, one scenario, no job. `model check`: `warning w_unserved_cap  a capability serves no job  (1)`, exit 0. Red for r111.
- P2 (run): drafted w1 accepts `thing#r2` (service, no scenario), no check. `v_w4` printed for w1; `file: .shop/work/i1/w1.md: accepts ...thing#r2, which no scenario names yet`; `v_s3` for r2. Red for r106.
- P3 (run): drafted w1 accepts `thing#r2`, r2 in a guarantees capability, no scenario, check set. File problem printed. Spec r27 says no problem. Red.
- P4 (run): green w1 accepts `thing#r2`, r2 listed as retired, no scenario. File problem printed. Spec r27 says no problem. Red.
- P5 (run): drafted w1 accepts retired `thing#r2`, no scenario. File problem printed: correct by r27 (only green is exempt).
- P6 (run): green w1 accepts non-retired `thing#r2`, no scenario. File problem printed: correct.
- P7 (run): withdrawn w1 accepts `thing#r2`, no scenario, no check. No file problem and no v_w4: correct.
- P8 (run): `model facts` with w1 accepting r1 (scenario named) and r2 (not): `accepts("work-item/ex.com/prod/ctx/w1", "features/thing.feature:it answers").`; no accepts fact for r2.
- P9 (run): part p1.md kind capability-proposal, status built. `file: .shop/work/i1/p1.md: status 'built' is not one of approved, drafted, formulated, merged, withdrawn`, exit 1. Correct.
- P10 (run): `pytest -p work_items --work-item w1` in a consumer whose only scenario is r1 and whose w1 accepts only guarantees `thing#r2` (no scenario). Refused: `SystemExit: --work-item w1: w1 accepts none of the scenarios it collected`, exit 3 (INTERNALERROR). The consumer sits under the worktree, so pytest took the worktree's pytest.ini (its addopts add `-n`); the rerun with `-o addopts=` shows the message above.
- P11 (run): accepts `thing#r1, thing#r2` (r2 unnamed): 1 passed, the r1 scenario runs.
- P12 (run): accepts `thing#r1`: 1 passed.

Nearest cases the scenarios do not give: P5, P6, P7, P8 and P11 above. Also not run: a guarantees requirement that a scenario does name, and a work-item accepting a requirement of a second capability.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:read_part (184-192) | writes `accepts` fact only for requirements a scenario names; else file problem unless withdrawn | r106: fact for every accepted requirement; r27: exempt guarantees and green-retired | by search: tests/scripts/test_model_withdrawn.py:NotReadTest (service, drafted: 1 problem, stays); tests/scenarios/design_model_check_problems.py work-item rows (stay) | refs (read_part: 1 ref, model_work.py:125); read |
| scripts/model.lp:65, :236 (has_accepts, v_w4) | assumes `accepts(W,S)` second argument is a scenario node | an unnamed requirement needs another second argument or a second relation | by search: design_model_check_one_each.py rows (4 pass; stay) | grep `accepts` in scripts; read |
| scripts/model.lp:276 (w_unserved_cap) | fires for every capability with no `serves` fact; model_facts emits no `serves` and no job node (grep), so it fires in every context | r111: no warning with no job | by search: tests/scripts/test_model_output.py:CheckOutputTest.test_check_ends_with_the_four_counts (run: passes today; asserts "1 warnings", which this gives 0) | grep `serves` / `unserved`; run P1 |
| scripts/work_items.py:accepted, pytest_collection_modifyitems (99-107) | every accepted pair must match a scenario tag, else refuses the run | an accepted unnamed requirement makes a work-item with no other accept refused | by search: tests/scripts/test_work_items.py:test_a_work_item_none_of_whose_scenarios_are_collected_is_refused (other#r1, stays); no test of an unnamed accept | read; run P10 |
| scripts/work_items.py:acceptors, expect_red (56-89) | pairs keyed by scenario tags; unnamed requirement is never xfailed under --whole-suite | an unnamed accepted requirement of another work-item is not expected to fail | none found (grep for whole-suite, expect_red, acceptors, xfail in tests/: only supervision_tests_steps.py and supervision_given.py use --whole-suite, none asserts xfail for an unnamed requirement) | read; refs (acceptors: 1 production ref) |
| scripts/supervise_brief.py:accepted_scenarios (89-107) | reads tags from features/<cap>.feature; unnamed requirement gives no line | the brief's "Accepted scenarios" omits it silently | none (refs accepted_scenarios: 1 production, 0 test files) | refs; read |
| scripts/workqueue.py:74-93 (work add --accepts) | writes `accepts:` with no scenario check | legal for guarantees and green-retired after r27 | by search: tests/scenarios/test_work_queue.py:208 (asserts accepts field; stays) | grep `accepts`; read |
| docs/design-model/grammar.md:198 | `w_unserved_cap(C) :- node(C,"capability"), !serves(C,_).` | r111 changes this rule | none (doc) | grep `w_unserved` |

## 4. Tests the requirements make impossible to keep

Found by search (`tools tests-of` has no map). Grep over tests/ for accepts, unserved, warning, v_w4, whole-suite, expect_red, xfail.

- tests/scripts/test_model_output.py, CheckOutputTest.test_check_ends_with_the_four_counts (line 14-18): asserts `1 violations, 1 warnings, 1 unresolved references, 1 file problems` for one capability with no job. The one warning is w_unserved_cap. r111 makes it 0 warnings. Run: passes today. Impossible to keep as it stands.
- tests/scripts/test_model_output.py, test_exit_codes_of_check (line 37): "a warning alone exits 0". The warning is w_uncited_obs (observation with no initiative), not w_unserved_cap. Read; stays.
- tests/scripts/test_model_withdrawn.py, NotReadTest.test_r27_... (lines 17-26): service group, drafted gives 1 problem, withdrawn 0. Run: passes. Stays: the new exemptions are for guarantees and green-retired only.
- tests/scenarios/design_model_check_problems.py, "a work-item accepting a requirement no scenario names is a file problem" (service): stays (run).
- tests/scenarios/design_model_check_one_each.py, v_w4 rows: the 4 that pass today stay (run).
- tests/scripts/test_work_items.py (lines 25-90): read. Accepted pairs are scenario-named or `other#r1` with none; all stay.
- tests/scenarios/supervision_tests_steps.py:148-172: w1 accepts `other#r1`, expects "w1 accepts none of the scenarios it collected". Read; stays, unless `other` gains a scenario.
- Nothing asserts a file problem for a guarantees or green-retired accept, or a v_w4 for an unnamed accept (by search); nothing to break there.

## 5. A step the work-item skips

The work-item's accepts path skips the scenario lookup (`model_work.py:184-188`, `found` from `has_sc` facts). The lookup alone produces:
- the `accepts` fact, which is what satisfies v_w4 (`has_accepts`). P8 (named, fact written) against P2 (unnamed, no fact, v_w4 printed).
- the work_items plugin's view of the requirement as a scenario-tagged pair. P10: an unnamed accept gives the refusal `accepts none of the scenarios it collected`. Run.
- Refusals: the r27 file problem (P2, P4, P6) only; nothing else refuses on the lookup. Read.

## 6. Defects

Each is an outcome today that the spec text already excludes. Reproduce with the probe named.

D1. A `model check` on a context with no job prints `warning w_unserved_cap`. Spec r111. P1: `warning w_unserved_cap  a capability serves no job  (1)`, exit 0.

D2. A drafted work-item accepting a requirement no scenario names, with no check, gets v_w4. Spec r106 says accepts counts. P2: `v_w4  a work-item has no acceptance and no check  (1)` with `work-item/ex.com/prod/ctx/w1`.

D3. A work-item accepting a guarantees requirement no scenario names gets a file problem. Spec r27 exempts guarantees. P3: `file: .shop/work/i1/w1.md: accepts capability/ex.com/prod/ctx/thing#r2, which no scenario names yet`.

D4. A green work-item accepting a retired id gets a file problem. Spec r27 exempts a retired id when green. P4: same message as D3.

## 7. The file set

Production:
- scripts/model_work.py: `read_part` writes accepts facts for unnamed requirements (r106); exempts guarantees and green-retired from the r27 problem (uses `self.caps` group and `self.retired`, which `read_capabilities` fills first). Found: refs, read 184-192.
- scripts/model.lp: `w_unserved_cap` gets a job condition (line 276). `v_w4` probably unchanged (lines 65, 236). Found: grep.

Tests:
- tests/scenarios/design_model_check_given.py: three Givens (no job; r2 retired in frontmatter; guarantees r2 unnamed). Found: grep of the step texts, none exists.
- tests/scenarios/design_model_check_one_each.py: `FIELDS` key "accepts thing#r2 and no check". Found: KeyError, run.
- tests/scenarios/design_model_check_problems.py: `malformed_work` branch for "the part p1.md has the kind capability-proposal and the status built". Found: AssertionError, run. Room is 11 lines: a short branch fits, a longer one needs a new module.
- tests/scripts/test_model_output.py: `test_check_ends_with_the_four_counts` expects "1 warnings" and must change with r111. Found: by search, run.

On the change's path, edited or not (line counts by `wc -l`):
- scripts/model: 137 (room 163)
- scripts/model_check.py: 139 (room 161)
- scripts/model_facts.py: 275 (room 25); holds `self.caps` and `read()` order; read only
- scripts/model_work.py: 211 (room 89)
- scripts/model_parse.py: 271 (room 29); `expand`, `as_list`; read only
- scripts/model.lp: 304 lines; not a tracked Python file, so the 300 limit of `tools size` does not apply
- scripts/work_items.py: 109 (room 191); not required by the scenarios; a change here is a choice (section 3 rows 4-5)
- scripts/supervise_brief.py: 110 (room 190); read only
- tests/scenarios/design_model_check_given.py: 228 (room 72)
- tests/scenarios/design_model_check_one_each.py: 47 (room 253)
- tests/scenarios/design_model_check_problems.py: 289 (room 11)
- tests/scripts/test_model_output.py: 74 (room 226)
- tests/scripts/test_model_withdrawn.py: 30 (room 270); passes unchanged
- tests/scenarios/conftest.py: 176 (room 124); `World.model`, `World.work_item`; read only
- `tools size --limit 300` (run): prints no tracked Python file over 300.
- docs/design-model/grammar.md:198: the same rule as model.lp:276; doc, not Python.
