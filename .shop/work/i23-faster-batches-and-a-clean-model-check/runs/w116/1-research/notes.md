# w116 research notes

Work-item w116 accepts design-model-check#r27. Four accepted scenarios, all in features/design-model-check.feature:
malformed work directory or file (outline, @r27); work-item accepting an unnamed requirement (file problem);
guarantees requirement accepted, no scenario (no file problem); green work-item accepting a retired id (no file problem).
No tool map exists (`tools tests-of` answered "no map"); `tools map` runs the suite, not run. Test lists below are `by search`.
Probes: `.shop/scratch/w116-1-research/probe_r27.py`, `probe_r27_accepts.py`, run `python3 -m pytest -q -s -n 0 <path>`.
Probe Behaviour lines are not EARS, and work-items sit directly under the initiative: `v_e1` and `v_b1` lines in probe output are probe noise.

## 1. Why each accepted scenario is red today

Command: `python3 -m pytest -q "tests/scenarios/test_design_model_check.py::<node>"` (run).

- **Outline "a malformed work directory or work file is a file problem"**: 8 of 9 rows pass. The row
  "the part p1.md has the kind capability-proposal and the status built" fails: AssertionError at
  tests/scenarios/design_model_check_problems.py:101. `malformed_work` (:76-102) has no branch for that case.
  Code already right: scripts/model_work.py:11 STATUSES lists no `built` (probe built-proposal shows the file problem).
  Missing: the step branch only.
- **"a work-item accepting a requirement no scenario names is a file problem"**: passes (run).
- **"a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem"**:
  StepDefinitionNotFoundError, Given "a capability thing in the guarantees group with requirement r2 that no scenario names"
  (feature line 319). Existing step design_model_check_given.py:57 is service-group only.
  Code gap: scripts/model_work.py:184-192 (work-item branch of `read_part`) reports every unnamed accepted
  requirement unless withdrawn; it does not read the capability's `group` fact (written at scripts/model_facts.py:178-179).
  Probe repro (probe_r27, group guarantees) prints the file problem.
- **"a green work-item accepting a retired id is no file problem"**: StepDefinitionNotFoundError, Given
  "a capability thing whose frontmatter lists r2 as retired" (feature line 327). The next Given
  "a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2" also has no step: the only one is
  design_model_check_problems.py:105, drafted and no status word.
  Code gap: scripts/model_work.py:191 does not test retired ids (`self.retired`, scripts/model_facts.py:49, 189) or status green.

## 2. What the system answers today

Probe commands: `python3 -m pytest -q -s -n 0 .shop/scratch/w116-1-research/probe_r27.py` (run, 3 tests passed),
`python3 -m pytest -q -s -n 0 .shop/scratch/w116-1-research/probe_r27_accepts.py` (run, 1 passed). Each
result is the `model check` exit code and the file problem lines.

| case (given / when) | today | nearest case |
|---|---|---|
| p1 kind capability-proposal, status `built` | rc 1, file problem naming `.shop/work/i1/p1.md`: status 'built' is not one of approved, drafted, formulated, merged, withdrawn | `delivered`: same refusal; `formulated`: no file problem |
| w1 kind work-item, status `built` | rc 1, file problem naming w1.md (status not in the work-item lifecycle) | none |
| guarantees thing r2 unnamed, w1 drafted accepts thing#r2 | file problem "accepts ...thing#r2, which no scenario names yet" (fails r27) | service group: same file problem plus v_s3 |
| retired r2, w1 green accepts thing#r2 | file problem "which no scenario names yet" (fails r27) | drafted: same; withdrawn: no file problem (model_work.py:191 exemption) |
| retired r2, w1 green accepts thing#r1 (named live) | no file problem | — |
| w1 green accepts thing#r9 (no such requirement) | file problem "which no scenario names yet", not "unresolved" | — |
| w1 green, retired r2, no accepts, check set | no file problem | — |
| guarantees r2 unnamed, w1 drafted accepts thing#r2, no check | file problem AND `v_w4` "no acceptance and no check" (see 5) | — |
| service r2 unnamed, same | file problem, `v_s3`, `v_w4` | — |
| service r2 named by @r2, same, no check | no `v_w4`, no file problem | — |

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:read_part, work-item branch, lines 184-192 | every accepted requirement needs a named scenario, unless the work-item is withdrawn | guarantees requirements (no scenario) and a green work-item's retired id must pass | by search: tests/scripts/test_model_withdrawn.py:17-26 (withdrawn 0, drafted 1; service group, unaffected); tests/scenarios/design_model_check_problems.py:105-110, 309-330 | read; probes P2, P3 |
| scripts/model_work.py:188-190 `accepts` fact written only when a scenario names it (`has_sc`) | no `accepts` fact for an unnamed requirement, so `has_accepts` is false | r106: accepts counts whether or not named (model.lp:65 has_accepts, model.lp:236 v_w4). Not required for the four accepted scenarios; needed for r106 | by search: none names an unnamed accepted requirement with no check (tests/scenarios/design_model_check_one_each.py FIELDS accept only thing#r1, which a scenario names) | read; probe P5 |
| scripts/model.lp:54-55 `closed(P)` names built, delivered, ruled, refused for a capability-proposal (and green, merged) | a proposal in those statuses counts as closed, though the file form refuses them | r27: model.lp names only the statuses the file form accepts for a proposal (drafted, approved, merged, formulated, withdrawn) | by search: none (no test names built, delivered, ruled or refused) | read |
| scripts/model.lp:54 `closed` for non-proposal parts names built, delivered, ruled, refused | no work-item or initiative lifecycle has them (scripts/model_work.py:9-14), so dead | as above | by search: none | read |
| scripts/model_work.py:164-166, SETTLED at :15, retired set | retired ids: settled proposals may name them; adds of a retired id is v15c | a green work-item's retired accept must not be refused; the retired set is read here | by search: tests/scripts/test_model_reading.py:58-64 (v15c); tests/scripts/test_model.py:154 (retired guarantees capability, not read in full) | read |
| scripts/work_items.py:99-107 `pytest_collection_modifyitems`, "accepts none of the scenarios it collected" | a `--work-item` run is refused when the work-item accepts no collected scenario | a guarantees-only accepting work-item now passes the file check but is refused by `work run` (see conflict below) | tests/scripts/test_work_items.py:67-69, 79-83 (other#r1, a requirement with no scenario collected); tests/scenarios/supervision_tests_steps.py:168-172 (by search) | read |
| scripts/supervise_brief.py:89-100 `accepted_scenarios` | lists the scenarios tagged with accepted requirements | a guarantees requirement has none, so the brief lists none | by search: none | read |

Conflict for the plan (both readings, not decided): for a guarantees requirement with no scenario, the file check
passes but `work run --work-item` refuses ("accepts none of the scenarios it collected"). Either the refusal stays
(the work-item has nothing to run), or the scoping allows zero scenarios. Each is a change to scripts/work_items.py.

## 4. Tests the requirements make impossible to keep

`tools tests-of` cannot answer (no map). By search over tests/:

- tests/scripts/test_model_withdrawn.py:17-26 (service group; drafted gives 1 file problem, withdrawn gives 0): read, sound
  under r27: r27 exempts only guarantees and a green retired id.
- tests/scripts/test_work_items.py:67-69, 79-83 (other#r1 accepted, nothing collected, refused): read, sound: the requirement
  is not guarantees and not retired.
- tests/scenarios/design_model_check_one_each.py FIELDS and tests/scripts/test_model_reading.py:58-64 (v15c): read, sound.
- tests/scenarios/design_model_check_problems.py:105-110 (drafted work-item accepts thing#r2 with no scenario naming it): read, sound.
- No test asserts the file problem for a guarantees requirement or for a green retired id (grep "no scenario names yet"
  in tests/: only test_model_withdrawn.py). So none is impossible to keep. Not run: the tests above.

## 5. A step the work-item skips

The existing way for an accepted requirement writes an `accepts` fact (scripts/model_work.py:188-190) and checks the
scenario. The new paths (guarantees, green retired) take neither the scenario nor the fact.
Effects only that step produces (probe P5, run, probe_r27_accepts.py):
- the `accepts` fact is what suppresses `v_w4` (model.lp:65, 236): without it, a guarantees or a green-retired work-item
  with no check gets `v_w4 a work-item has no acceptance and no check`. Run: guarantees-drafted-no-check printed `v_w4`;
  green-retired-no-check printed `v_w4`.
- the file problem "accepts ..., which no scenario names yet" is the only other effect (run).
- a withdrawn work-item skips both (read, model_work.py:191 and :188): not run.

## 6. Defects

### D1 guarantees requirement accepted by a work-item is refused
Repro (run, probe_r27 `test_work_item_accepting_guarantees_requirement_no_scenario_names`): capability thing, group guarantees,
requirement `- [r2] Two.`, initiative i1, work-item w1 drafted, `accepts: [thing#r2]`. `python3 scripts/model --root <repo> check`
gives rc 1 and `file: .shop/work/i1/w1.md: accepts capability/ex.com/prod/ctx/thing#r2, which no scenario names yet`.
r27 says no file problem.

### D2 green work-item accepting a retired id is refused
Repro (run): capability thing, requirement r1 with scenario @r1, `retired: [r2]`; work-item w1 status green, `accepts: [thing#r2]`:
rc 1, `file: .shop/work/i1/w1.md: accepts ...thing#r2, which no scenario names yet`. r27 says no file problem.

### D3 accepted requirement with no capability: file problem text names no scenario (not stated by spec)
Repro (run): green w1 `accepts: [thing#r9]`, no r9: `file: ... accepts ...thing#r9, which no scenario names yet`. The spec
does not say whether this is a file problem or unresolved (r22 and r9 cover scenarios and proposals only). Reported, not judged.

### D4 accepted requirement with no check is `v_w4` (r106)
Repro (run, probe_r27_accepts): service requirement r2 named by @r2 and no check: no `v_w4`; the same unnamed: `v_w4`
plus file problem; guarantees unnamed: `v_w4`. r106 says an accepted requirement counts toward showing completion
whether or not a scenario names it (model.lp:65 note). Its scenario is not in w116's accepted list; not run by me.

## 7. The file set

Production files w116 must change for its four scenarios:
- scripts/model_work.py (211 lines, room 89): work-item branch lines 184-192, exempt a guarantees requirement (group fact) and
  a green work-item's retired id (`self.retired`). Found by read and probes P2, P3.
- scripts/model.lp (304 lines; not Python, so CLAUDE.md's 300 limit does not apply and `tools size` does not list it): lines 54-55,
  drop built, delivered, ruled, refused from the capability-proposal `closed` rule. Found by read.

Test files the change must change:
- tests/scenarios/design_model_check_given.py (228 lines, room 72): new steps for guarantees r2 unnamed, a retired r2 capability,
  and the green work-item accepting thing#r2.
- tests/scenarios/design_model_check_problems.py (289 lines, room 11): `malformed_work` branch for the built case (three lines fit).

Files that keep passing and need no change: tests/scripts/test_model_withdrawn.py (30 lines, room 270),
tests/scripts/test_work_items.py (98, room 202), tests/scripts/test_model.py (213, room 87), scripts/work_items.py (109, room 191) and
scripts/supervise_brief.py (110, room 190). The last two change only if the conflict in part 3 resolves to allow zero scenarios.

Modules on the change's path, with lines and room under 300:
- scripts/model (137, room 163): entry script, runs model_check.
- scripts/model_check.py (139, room 161).
- scripts/model_facts.py (275, room 25): reads groups and retired ids (no change needed).
- scripts/model_parse.py (271, room 29).
- scripts/model_work.py (211, room 89): edited.
- scripts/model.lp (304, not Python): edited.

`tools size --limit 300` printed nothing: no tracked Python file over the limit.
`git status --porcelain` printed nothing at the end: the scratch directory is ignored.
