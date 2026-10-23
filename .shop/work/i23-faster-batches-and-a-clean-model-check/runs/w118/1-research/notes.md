# Research of w118: no w_unserved_cap while the context has no job

Scope: accepts `design-model-check#r111`. One accepted scenario. `tools tests-of` has no map (not made, per brief): every test list is `by search` or `run`. `tools refs w_unserved_cap` found no Python name (a label in `scripts/model.lp`).

## 1. Why each scenario is red today

Scenario: `features/design-model-check.feature:75` "a bounded context with no job gets no unserved-capability warning" (@r111).

- Command: `python3 -m pytest -q -n 0 "tests/scenarios/test_design_model_check.py::test_a_bounded_context_with_no_job_gets_no_unservedcapability_warning"` (run).
- Fails at the first undefined step: `Given "a bounded context with one capability and no job"` (line 77). No definition exists. The nearest step, `a bounded context with one capability` (`tests/scenarios/design_model_check_given.py:15`), is an exact match and does not match this text.
- Second undefined step (read): `Then the output does not give w_unserved_cap`. grep of `tests/scenarios` for `does not give` finds only `batch_measurement_then_steps.py:147`, a different step.
- Code behind it: `scripts/model.lp:275-276`: `w_unserved_cap(C) :- node(C, "capability"), not serves(C, _).`
  No Python emits `serves/2` or `of_job/2` (grep of `scripts/`: only `model.lp` lines 20-21, 80, 117, 278). So the rule fires for every capability, and the assertion would fail once the steps exist (section 2).
- Also read: `docs/design-model/grammar.md:198` has the same rule (`!serves`).

Missing: the two step definitions (Given in `design_model_check_given.py`, Then in `design_model_check_then.py`); and the behaviour at `scripts/model.lp:276`.

## 2. What the system answers today

Probes: `.shop/scratch/w118-1-research/probe_no_job.py`, run as `python3 -m pytest -q -n 0 .shop/scratch/w118-1-research/probe_no_job.py` (run). It builds repositories in its scratch directory and runs the worktree's `scripts/model --root <repo>`.

Probe A, the scenario's Givens (one capability `thing`, requirement r1 with scenario `@r1`, no job; the same as the existing `world.good()`):
- `model check` (run): rc=0, prints `warning w_unserved_cap  a capability serves no job  (1)` and `0 violations, 1 warnings, 0 unresolved references, 0 file problems`.
- `model check --json` (run): rc=0, `"warnings": [["w_unserved_cap", ["capability/ex.com/prod/ctx/thing"]]]`.
- `model facts` (run): capability, requirement and scenario facts only; no `serves` and no `job` node.

Nearest cases:
- Probe B, no capability, no job (run): `0 violations, 0 warnings`.
- Probe C, two capabilities `thing` and `other`, no job (run): `warning w_unserved_cap ... (2)`.
- `w_unserved_job` (`model.lp:278`) needs a `node(J, "job")`; no code emits one (grep, read). It cannot fire today.

## 3. Old assumptions

The requirement says: while a bounded context has no job, the rule prints nothing. Today the rule assumes `serves` facts exist, and nothing emits them.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model.lp:276` `w_unserved_cap` | warns every capability with no `serves` fact | must print nothing while the context has no job; no job can be read, so the rule must be gated on a job or removed for a bounded-context check | `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts` (run: passes today, asserts `1 warnings`); the scenario (red) | search (`grep w_unserved` over `tests/`, `scripts/`) |
| `scripts/model_facts.py` (no `serves`/`of_job` emitter) | emits no `serves` or `of_job` fact, so the rule holds for every capability | a gate on "the context has a job" needs a job fact that r19 does not read; without one the gate is always closed | none (no test asserts absence of `serves`) | search (`grep serves\|of_job` over `scripts/`) |
| `scripts/model_check.py:112-132` warning print and count | counts `w_` findings from the solve | no change: the count falls with the rule | `test_check_ends_with_the_four_counts`; `design_model_check_reading.py` JSON keys | read |
| `scripts/model_check.py:96-102` `rules` | lists each rule's label and kind, from `model.lp` labels | no change: `w_unserved_cap` keeps its label | `design_model_check_trace.py` rules scenarios (search; not run) | read |
| `docs/design-model/grammar.md:198` | the grammar's copy of the rule, `!serves` | disagrees with `model.lp` after the change; docs only | none | search |

## 4. Tests the requirements make impossible to keep

Search (no map): `grep warning|serves|unserved|rules` over `tests/`.

- `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts` (lines 14-18): asserts `1 violations, 1 warnings, 1 unresolved references, 1 file problems`. Its fixture is one capability `thing` with no job and no feature file; the one warning is `w_unserved_cap` (read of the fixture, consistent with probe A). After the requirement the count is `0 warnings`. This test cannot pass as written. Green today (run: `1 passed`).
- `test_exit_codes_of_check` (lines 31-44): asserts exit 0 with a warning alone. Its warning comes from `self.observation()` (`w_uncited_obs`), so it stays green. Read; not run separately.
- `design_model_check_problems.py:297-300` (`w_uncited_obs ... (1)`): the assertion is `in out`, so an absent `w_unserved_cap` does not change it. Sound (read).
- `design_model_check_reading.py:156-168` (JSON keys, labels): the key set is unchanged; `labels` covers only printed codes. Sound (read).
- `design_model_check_trace.py` rules tests: the label stays. Sound (read).
- `tests/scripts/test_model.py` (213 lines): no `warning` or `unserved` text (grep). Not run.

## 5. A step the work-item skips

none. The requirement changes one rule's condition and adds no path; the plain and `--json` outputs both read the same solve.

## 6. Defects

### D1: every capability is warned as serving no job, though no job can be read

Repro (run, `test_one_capability_no_job` and `test_two_capabilities_no_job` in `.shop/scratch/w118-1-research/probe_no_job.py`):
- `model check` with one capability `thing` and a scenario: `warning w_unserved_cap  a capability serves no job  (1)`, exit 0.
- Two capabilities: `(2)`.
- Cause: `model.lp:276` with no `serves` fact (section 3).

This is the behaviour r111 changes. What the plan does about it is not judged here.

### D2: `w_unserved_job` can never fire (read)

`model.lp:278` needs `node(J, "job")`. No code emits a `job` node: r19 does not list job files among the files `model` reads. Read only; not run.

## 7. The file set

Must change:
- `scripts/model.lp` (304 lines; not a tracked `.py`, so `tools size` does not count it; a 300-line room would be -4). Change line 276, `w_unserved_cap`, so that a context with no job gives no warning. Found by the rule and probe A. Keep the label at line 275.
- `tests/scenarios/design_model_check_given.py` (239 lines; room 61). Add `@given("a bounded context with one capability and no job")` calling `world.good()`. Found by the step error in section 1.
- `tests/scenarios/design_model_check_then.py` (221 lines; room 79). Add `@then("the output does not give {code}")` asserting the code is absent from `context["result"].stdout`. Found by grep (no existing step).
- `tests/scripts/test_model_output.py` (74 lines; room 226). Line 18 expects `1 warnings`; after the change that becomes `0 warnings`, or the fixture changes, the planner's choice. Found by the run in section 4.

On the path, unchanged:
- `scripts/model_check.py` (139 lines; room 161). Prints and counts solve results; no change needed.
- `scripts/model_facts.py` (275 lines; room 25). Emits no `serves` fact today. A gate that needs a job fact would change it, but r19 reads no job file. Unchanged in the gate-closed reading.
- `scripts/model` (137 lines; room 163). Entry point; unchanged.
- `tests/scenarios/test_design_model_check.py` (53 lines; room 247). Binds scenarios by file; unchanged.
- `docs/design-model/grammar.md` (308 lines, docs). Not Python; line 198 would disagree with `model.lp` afterwards. Not required for the scenario; planner's call.

Two readings, not decided here:
- Reading A: gate on "the bounded context has a job". No job fact can be emitted under r19, so the rule never fires.
- Reading B: no `w_unserved_cap` warning in a bounded-context check at all, since jobs are product-level and deferred ("Not yet" in the capability).
Both give the scenario's result and both change `test_model_output.py` line 18.
