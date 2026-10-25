# research of w196

Method: no coverage map (`tools tests-of` says "no map"; `tools map` runs the suite, not run), so every test list is `by search`. `tools refs` used for `Drafts.retires` (1 ref, `refs`) and `workqueue.add`/`draft_proposals` (refs misses calls through a module or `self`; those callers are `by search`). Probes: `.shop/scratch/w196-1-research/probe_retires.py` (4 tests, run with `-n 0`). Scratch is git-ignored; `git status --porcelain` is empty.

## 1. Why each scenario is red today

Command for all six: `python3 -m pytest -q -p no:warnings "tests/scenarios/test_supervision.py::<node>"` (nodes from `--collect-only`). Run: 4 failed, 2 passed.

- **1021** `test_a_workitem_drafted_for_a_formulated_capabilityproposal_lists_under_its_retires_each_deprecated_scenario_of_a_requirement_it_accepts_deprecated`: **passes today** (run). Passes by tag, not by `Deprecated for:` (see 2, probe b).
- **1031** range variant of the (deprecated) r73 scenario: **passes today** (run), same reason.
- **1041** `test_a_workitem_lists_under_its_retires_each_deprecated_scenario_whose_deprecated_for_line_names_a_scenario_of_a_requirement_it_accepts`: `StepDefinitionNotFoundError` at line 1045, `features/thing.feature has the scenario "it used to wait", tagged @deprecated and @r9, deprecated for "it waits"`. Only `supervision_proposal_steps.py:30` matches the `tagged @deprecated and @rN, the scenario ...` shape; no step writes a `Deprecated for:` line. Line 1046 has the same shape (read). Behaviour once the steps exist: wrong (probe a).
- **1052** range variant of 1041: undefined step at line 1056 (same shape; line 1057 read as same). Code: `supervise_draft.py:Drafts.retires` matches by own tag, not by the replacement.
- **1063** `test_when_every_workitem_is_green_or_withdrawn_one_workitem_is_drafted_...`: undefined Given at line 1065 (`i1's work-item w1 is green, part of ..., and i1's work-item w2, drafted after w1, is green, part of ... p2 and accepting other#r4`). Also undefined by grep (read): 1066 `i1's work-item w3 is withdrawn`, 1067 `i2's work-item w4 is ready, accepting thing#r7`, 1068 `features/other.feature has ...`, 1069-1070 `deprecated for "..."` Givens, 1073 Then `one work-item was drafted in i1, part of p2, listing ...`. Code missing: no retire drafting exists anywhere: `supervise_draft.py` has no function that reads a replacement's work-item status; `supervise.py:Run.draft()` (line 246) calls only `draft_proposals`.
- **1076** `test_the_workitem_retiring_deprecated_scenarios_..._before_the_branch_review_starts_...`: undefined Given at line 1078 (`i1's work-item w1 is green, part of ... p1 and accepting thing#r2, and w2 is withdrawn`; the existing `green_and_withdrawn` step says `i1's work-items w1 is green, part of ..., and w2 is withdrawn`, plural and different wording). Also undefined (read): 1079 `features/thing.feature has the scenario "it waits", tagged @r2, and the scenario "it used to wait", tagged @deprecated, deprecated for "it waits"`; Thens 1082 `the work-item retiring "it used to wait" was drafted in i1 before `work run` started the branch review of i1` and 1083 `... before `work run` ran `measure initiative` on i1`. 1080 exists (`supervision_analysis_steps.py:17`). Code missing: as 1063.

## 2. What the system answers today

Probes (`python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w196-1-research/probe_retires.py`, run):

- **a** — the 1041 layout (`it waits` @r2, `it answers` @r5, `it used to wait` @deprecated @r9 deprecated for `it waits`, `it used to answer` @deprecated @r2 deprecated for `it answers`), `retires(thing, [thing#r2])`:
  `[('it used to answer', 'r2')]`. Wrong on both counts: `it used to wait` (replacement `it waits` is @r2) is not listed; `it used to answer` (replacement is @r5) is.
- **b** — the 1021 layout (no `Deprecated for:` line anywhere), `retires(thing, [thing#r2])`: `[('it used to wait', 'r2')]`. Today's rule ignores the line; under the r73 text nothing names a replacement, so the list would be empty.
- **c** — one deprecated scenario `@deprecated @r2 @r3` deprecated for `it waits` (@r2), accepts `thing#r2-r3`: `[('it used to wait', 'r2'), ('it used to wait', 'r3')]`. The scenario is listed twice (`Drafts.retires` appends per matching tag).
- **d** — layout a through the existing reader, `features deprecated --json` (run in the scratch store): exit 0, `it used to wait` → `deprecated_for: it waits`, `replacement.tags: [r2]`; `it used to answer` → `it answers`, `[r5]`. The existing reader (`features_report.py:deprecated_entry`) already resolves the replacement by title across files; the r73 fix can reuse that reading.

Read (not probed, the path needs the whole `work run` harness):
- r123 path: no code. `draft()` (`supervise.py:246`) runs before `pull` and calls only `draft_proposals`; nothing writes a work-item for a green replacement. Today the 1063 Then would fail.
- Nearest cases the scenarios give: the store holds a deprecated scenario with no line (b), with a replacement whose requirement is not accepted (a), with two accepted tags (c), with a replacement in another file (1063's `it used to answer` in `other.feature`: `retires` reads only `features/<capability>.feature`, so it would never find it).
- Empty/absent: `retires` returns `[]` when the capability's feature file is absent (`supervise_draft.py:29`) and for a `removal` line (read).

## 3. Old assumptions

The old form: a deprecated scenario is retired by the requirement its own tag names, found in its capability's file.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_draft.py:Drafts.retires` | reads `features/<capability>.feature` only; matches a scenario whose own tag is an accepted requirement's | r73: match the `Deprecated for:` line's replacement title, its @r tag, in any feature file; a tag of the deprecated scenario counts for nothing | features/supervision.feature 1021, 1031 (pass today); 1041, 1052 (red); 1017 (no deprecated) | by search (refs: 1 call, `supervise_draft.py:54`) |
| `scripts/supervise_draft.py:Drafts.draft_proposals` (its `retires=` argument, line 54) | passes `self.retires(capability, accepts)` for each proposal's capability | same call, new `retires` reading; the list may also need de-duplication (probe c) | 1017, 1021, 1031, 1041, 1052 | by search (called as `self.draft_proposals()` from `supervise.py:248`) |
| `scripts/workqueue.py:add`, the `retires` pairs (lines 102-103) | writes `- "title" (<under> @<tag>)` with the tag the scenario matched | the tag written is the one the old rule matched; under r73 it would be the replacement's tag or the deprecated scenario's own @r; a r123 item may have an `under` other than the scenario's file's capability (1063) | 1017, 1021, 1031 (titles only checked) | by search (`scripts/work:21` `work add` has no retires argument, so only `work run` writes Retires) |
| `tests/scenarios/supervision_proposal_steps.py:thing_feature_deprecated` (line 30) | writes `@deprecated` plus its tag and no `Deprecated for:` line | the link the rule reads is the line; the helper leaves it out | 1021, 1031 (pass today); would turn red | by search |
| `tests/scenarios/supervision_proposal_steps.py:drafted` (line 73) and `supervision_analysis_steps.py:nothing_drafted` (line 44) | count every `work add: i1/wN drafted` commit as a proposal's work-item | r123 and r124 add work-items that retire scenarios and are part of no proposal of the initiative's own; the r121 "nothing drafted" Then would count a retire item | 1099 (r121, Outline x4), 1091 (r74) | by search |
| `scripts/supervise.py:Run.pull_through` (lines 214-224), `all(s in ("green","withdrawn"))` before the branch review | branch review and measure only when every item is green, on the items as they stand | r124: retire drafting after the pull and before the review; the new item is not green, so this run goes no further to review | 1076 (red), 1085-1100 (r74, r121: pass by search, run not) | by search |
| `scripts/features_report.py:deprecated_entry` / `cmd_deprecated` | already reads `Deprecated for:` and resolves the replacement | none: already the new rule; reuse | feature-file-tools deprecated scenarios | by search |

No other production place reads the old form (`grep -rn "Retires|retire"` over `scripts/`, `skills/`, `agents/`): the agents (`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`) and `skills/bdd-red-green` treat Retires as a list of titles to `features retire "<title> (deprecated)"`, and read no tag. Read: `features retire` locates by title across files; a title in two files is refused (`features_gherkin.py:locate`), which a cross-capability r123 item can hit.

## 4. Tests the requirements make impossible to keep

Lists by search (no map).

- `tests/scenarios/test_supervision.py` scenario 1021 (`...lists_under_its_retires_each_deprecated_scenario_of_a_requirement_it_accepts_deprecated`) and 1031 (range variant): **they pass today and would fail under r73**, because the step `thing_feature_deprecated` writes no `Deprecated for:` line, so the new rule lists nothing (read, from probe b). The step must write a replacement line, which the scenario's Given does not state (see question below).
- Scenario 1017 (`two_drafted`, `supervision_proposal_steps.py:82`): checks `work add` drafts exactly two items; unaffected while no scenario is deprecated. Kept: the no-deprecated path returns `[]` (read).
- `supervision_proposal_steps.py:retires_listed` (line 89): checks `"it used to wait"` listed and not `"it used to answer"` nor `"it waits"`. Passes under the new rule (read) once the step writes the lines. Kept.
- `supervision_analysis_steps.py:nothing_drafted` (line 44, scenario 1099 r121 Outline): asserts no work-item was drafted at all. Kept only while no deprecated scenario has a green replacement; a retire item under r123 breaks it (read).
- Nothing else in `tests/scripts/` names `retires`, `Drafts` or `supervise_draft` (grep). Checked: `tests/scripts/test_supervise_change.py`, `test_supervise_answers.py`, `test_features_deprecating.py` (features reader, unaffected).

## 5. A step the work-item skips

The new retire path (r123) is a second drafting path. The existing one has steps the new path must also have:

- **Push.** `Run.draft()` (`supervise.py:246-249`) pushes after `draft_proposals` drafts (r38). A retire item drafted outside `draft()` needs the same `self.push()`, or the branch review's verification (r51, `supervise_review.py`) sees an unpushed commit. Read.
- **Guard against re-drafting.** `draft_proposals` skips a capability that already has a work-item for the proposal (`have`, `supervise_draft.py:40, 51`). The retire path has no such guard: a deprecated scenario stays in `features/` until the retiring item turns green and `features retire` runs, so every later `work run` with all items green would draft again. Read. Overlap with r73 (a scenario listed by an accepting item and by a retire item) and across initiatives (`retires` is global, r123 says "of any initiative") is read too.
- **Refusals the path would raise.** `workqueue.add` refuses if the initiative is `done` or `abandoned` (workqueue.py:91-93) or a value has a newline; `draft()` does not catch `Refused`, so it reaches `pull_through`'s `finally` and the run's exit. Read.
- **Ordering.** `draft()` runs at `pull_through` line 210, before `pull(MOVABLE)`; items are not yet green when it runs in a run that makes them green. A retire drafted there misses r123's "every item green" in that run. r124 wants it before the branch review: the place is after `pull` (line 211) and before the review check (line 214), then pull again and re-check line 214. Read. The plan decides whether the review waits for the retire item.

## 6. Defects

### D1: `Drafts.retires` lists the wrong deprecated scenarios

Reproduction: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w196-1-research/probe_retires.py::test_a_layout_of_the_r73_scenario_at_line_1040` (run). Output: `retires(thing, [thing#r2]) -> [('it used to answer', 'r2')]`. Expected under r73: `it used to wait` (deprecated for `it waits`, which is @r2), and not `it used to answer` (deprecated for `it answers`, @r5). This is the behaviour the work-item changes; shown as today's answer.

### D2: a scenario with two accepted tags is listed twice

Reproduction: `... ::test_c_one_deprecated_scenario_tagged_with_two_accepted_requirements` (run). Output: `[('it used to wait', 'r2'), ('it used to wait', 'r3')]`: one entry per matching tag, so two `- "it used to wait"` lines in the Retires section.

## 7. The file set

Production files the work-item changes:

- `scripts/supervise_draft.py` (81 lines; room 219): `retires` reads each deprecated scenario's `Deprecated for:` line and the replacement's @r tags in any feature file (reuse `features_report.deprecated_entry`'s reading, or `features_gherkin.load`); de-duplicate (D2); new r123 function: green replacements of any initiative, last-drafted item, retire item draft, re-drafting guard. Read: `supervise_draft.py` whole.
- `scripts/supervise.py` (271 lines; room 29): `pull_through` call of the retire drafting between `pull(MOVABLE)` and the review check (line 211-214), its push. Read: lines 193-257.
- `tests/scenarios/supervision_proposal_steps.py` (168 lines; room 132): `thing_feature_deprecated` writes `Deprecated for:` (1021, 1031); new steps for the 1041/1052 shape (`tagged @deprecated and @rN, deprecated for "X"`) and for 1063/1076 Givens and Thens. Read.
- `tests/scenarios/supervision_given.py` (265 lines; room 35) or a new `tests/scenarios/supervision_retire_steps.py` (new file, under 300): the `has the scenario "...", tagged @r2, and the scenario "...", tagged @deprecated, deprecated for "..."` shapes and `i2's work-item w4 ...`, `features/other.feature has ...`. A new module needs one import line in `tests/scenarios/test_supervision.py` (261 lines; room 39), which has `from .supervision_X import *` lines (read, lines 25-30). Read.
- `tests/scenarios/supervision_analysis_steps.py` (104 lines; room 196): the two r124 Thens (`drafted before ... branch review`, `before ... measure initiative`) and the `drafted` helper's use by `nothing_drafted` (D: keep it counting only proposal items, or not). Read.

On the change's path, not edited (rooms from line counts): `scripts/workqueue.py` (294; room 6: `add`, `items`, `frontmatter` used; no change expected, so no room needed for it); `scripts/model_parse.py` (271; room 29: `expand`); `scripts/features_gherkin.py` (175; room 125: `Feature`, `load`, `locate`); `scripts/features_report.py` (116; room 184: `deprecated_entry`, reuse); `scripts/supervise_review.py` (82; room 218: branch review and push verification, not edited, read); `tests/scenarios/supervision_world.py` (173; room 127: `item_text`, `write`, `commit_all`, read).

Line counts by `wc -l`. `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing: no tracked Python file is over 300 lines (run).
