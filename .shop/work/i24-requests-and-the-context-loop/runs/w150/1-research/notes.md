# w150 research: work run's Retires covers ranges (supervision r73)

Tools: `tools refs` ran (retires, 1 production reference). `tools tests-of` has no map: by search. Scenarios: pytest node ids from `--collect-only`. Probes ran with `-o addopts=""` (no xdist) to see prints.

## 1. Why each scenario is red today

- **Equality scenario** (`features/supervision.feature:898`). Command: `python3 -m pytest -q -rfEx "tests/scenarios/test_supervision.py::test_a_workitem_drafted_for_a_formulated_capabilityproposal_lists_under_its_retires_each_deprecated_scenario_of_a_requirement_it_accepts"`. **Passes** (run).
- **Range scenario** (`features/supervision.feature:907`). Command: same, node id `…whose_changes_name_a_range_lists_under_its_retires…in_the_range`. **Fails** (run) at `tests/scenarios/supervision_proposal_steps.py:72`, the Then: `assert '"it used to wait"' in held …`. The Retires section lacks "it used to wait".
  - Cause 1: `scripts/supervise_draft.py:30` `wanted = {a.split("#", 1)[1] for a in accepts}` gives `r3-r6`, compared by equality to tags `r4`, so nothing matches. `retires()` returns `[]` (probe, run).
  - Cause 2: the step's Given drops the range. `tests/scenarios/supervision_proposal_steps.py:17` `named()` is `re.findall(r"\w+#r\d+", …)`, so "changes naming thing#r3-r6" writes `changes: [thing#r3]` (probe, run). The work-item then accepts only `thing#r3`, so even a range-aware `retires()` would find no `r4` tag. The scenario cannot pass until the Given keeps the range.

## 2. What the system answers today

Probe `.shop/scratch/w150-1-research/probe_retires.py` (command: `python3 -m pytest -q -s -o addopts="" .shop/scratch/w150-1-research/probe_retires.py`), run. Feature file written in the scratch root: `it used to wait` @deprecated @r4, `it used to answer` @deprecated @r8, `it waits` @r4, `it used to do both` @deprecated @r2 @r3.

- `Drafts.retires("thing", ["thing#r4"])` → `[('it used to wait', 'r4')]`. Matches the equality scenario.
- `retires("thing", ["thing#r3-r6"])` → `[]`. The range scenario's case: nothing listed.
- `retires("thing", ["thing#r2-r9"])` → `[]`. A wider range also nothing.
- `retires("thing", ["thing#r1"])` → `[]`. Nothing tagged r1: correct.
- `retires("thing", ["thing#r2", "thing#r3"])` → `[('it used to do both','r2'), ('it used to do both','r3')]`. One scenario listed twice (D2).
- `retires("thing", ["thing#r2"])` → `[('it used to do both','r2')]`.
- `retires("other", ["other#r1"])` with no `features/other.feature` → `[]`. Silent when the feature file is absent (read: `supervise_draft.py:28-29`).

Step reading, probe `.shop/scratch/w150-1-research/probe_step_named.py` (command as above, run; imports the step module): `supervision_proposal_steps.named('thing#r3-r6')` → `['thing#r3']`; `named('thing#r1 and thing#r2')` → `['thing#r1', 'thing#r2']`.

Nearest case the scenario does not give: a range Given whose work-item accepts `thing#r3` only, so the assertion concerns a different accepted set than the scenario names (read from the step; follows from the probe).

## 3. Old assumptions

Old form: an accepted requirement is one id, `<cap>#r<n>`, matched by equality. Requirement r73 accepts ranges too (`r3-r6`). Places that still assume the single id:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_draft.py:Drafts.retires (line 30) | keeps `a.split("#",1)[1]` (`r3-r6`) and compares tags by equality | expand each range to its ids, as the other readers do | r73 equality scenario (run, passes); r73 range scenario (run, fails) | refs, then read |
| tests/scenarios/supervision_proposal_steps.py:named (line 17) | `\w+#r\d+` reads `thing#r3-r6` as `thing#r3` | the Given must keep the range so the work-item accepts it | r73 range scenario (run); the r72 scenarios that share the Given (by search) | probe run, search |
| scripts/supervise_draft.py:Drafts.draft_proposals (lines 45-53) | copies entries as written, ranges included, into `accepts` | none: the work-item keeps the range text; only `retires()` must read it | r72 scenarios and the r73 scenarios, through `work run` (by search, not counted) | refs |
| scripts/workqueue.py:add (lines 98-99) | writes one `- "title" (cap @tag)` line per pair in `retires` | a scenario tagged for two accepted ids would appear twice; the requirement lists each scenario | r73 equality scenario (run); none runs a duplicate | search |
| scripts/supervise_draft.py:Drafts.fix_work_item (line 77) | copies `accepts` raw | none (no retires) | r74 scenario (by search) | read |

Already expand ranges, the shape to reuse (not old assumptions): `scripts/model_parse.py:expand` (lines 96-105), `scripts/model_work.py:190` (uses `expand`), `scripts/supervise_brief.py:accepted_scenarios` (lines 94-101), `scripts/work_items.py:requirements` (line 45).

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map: by search (`retires` is called only from `draft_proposals`, which `scripts/supervise.py:222` calls).

- Tests asserting the old range behaviour: `none`. Searched `tests/` for `#r\d+-r\d+`: the range texts are in `tests/scripts/test_model_reading.py:29,147` (proposal parse, not retires) and `tests/scripts/test_work_items.py:53` (the plugin's option, not retires). None reaches `retires()`.
- Equality scenario (`test_supervision.py`): passes today (run). A range-aware `retires()` keeps it passing (read): `r4` is still listed, `r8` tagged scenarios still excluded.
- r72 scenarios (`test_supervision.py`, "one work-item for each capability…" and the rounds scenarios with a formulated proposal): go through `draft_proposals` and `retires()` with single-id accepts; nothing changes for them (read; by search, not run).
- No test asserts the duplicate listing: `none`.

## 5. A step the work-item skips

The range path already exists elsewhere: `model_parse.expand`, `supervise_brief.accepted_scenarios` and `work_items.requirements` each expand `r<a>-r<b>` before matching tags. `Drafts.retires` skips that step. Effects only it produces (probe run): a range gives `[]` (no Retires line, no error, no fault); a missing feature file gives `[]` silently (read). No other refusal or effect of the step.

## 6. Defects

**D1. A range in accepts lists no retired scenario.** Reproduction: `python3 -m pytest -q -s -o addopts="" .shop/scratch/w150-1-research/probe_retires.py`; `retires("thing", ["thing#r3-r6"])` → `[]`, with `it used to wait` @deprecated @r4 in features/thing.feature. Scenario run: `tests/scenarios/test_supervision.py::…in_the_range` fails at `supervision_proposal_steps.py:72`.

**D2. A scenario tagged for two accepted requirements is listed twice.** Reproduction: same probe; `retires("thing", ["thing#r2", "thing#r3"])` → `[('it used to do both','r2'), ('it used to do both','r3')]`. The Retires section would hold two lines for one scenario (`workqueue.py:99`). Not covered by a scenario.

**D3. The range scenario's Given drops the range.** Reproduction: `python3 -m pytest -q -s -o addopts="" .shop/scratch/w150-1-research/probe_step_named.py` → `named('thing#r3-r6')` → `['thing#r3']`. The fixture cannot exercise a range. (A fixture defect, not product.)

Observed, not probed: the failing range run's stderr carried `…4-review/session.json is not a session.json of a shape measure knows`. Not investigated; not related to r73.

## 7. The file set

- `scripts/supervise_draft.py` (80 lines; room 220): `retires()` expands each accepted range to its ids (as `model_parse.expand` does) and lists each deprecated scenario once. Found by refs, read, D1/D2.
- `tests/scenarios/supervision_proposal_steps.py` (82 lines; room 218): `named()` keeps the `-r<m>` of a range, so the Given writes `changes: [thing#r3-r6]`. Found by probe_step_named. The r72 Given still gives single ids unchanged.

Modules on the change's path, edited or not:
- `scripts/supervise.py` (234; room 66): calls `draft_proposals()` at line 222. Not edited.
- `scripts/workqueue.py` (286; room 14): `add()` writes the Retires lines. Not edited.
- `scripts/model_parse.py` (271; room 29): `expand()`, if reused. Not edited.
- `scripts/features_gherkin.py` (175; room 125): `Feature` parses tags. Not edited.
- `scripts/supervise_brief.py` (115; room 185): `accepted_scenarios` already expands. Not edited.
- `tests/scenarios/test_supervision.py` (249; room 51): holds the two r73 scenarios. Not edited.

`git status --porcelain` is empty now; the scratch directory does not show in it.
