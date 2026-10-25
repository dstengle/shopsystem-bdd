# Research notes: w188 (fix the findings of branch review 1 of i30)

Accepts: supervision#r19, supervision#r110, supervision#r117. Base checkout HEAD `0279766f` (clean worktree).
Method: `tools map` absent (no map). `tools tests-of` and `untested` unusable, so every test list is `by search`. `tools map` would write `.shop/scratch/tools/`, outside my allowed write place, so I did not run it. Counts by search are floors.

## 1. Why each scenario is red today

None is red. Each accepted scenario passes today.

- `python3 -m pytest -q -rfE "tests/scenarios/test_supervision.py::test_a_researcher_is_given_the_workitems_file_set_and_accepted_scenarios_and_a_limit_of_80_turns"` plus the two other node ids (r117, r110): `3 passed`. Run. The step code runs the checkout's `scripts/` (`tests/scenarios/conftest.py:11`).
- r19: `supervise_worker.py:53-54` `MAX_TURNS = {"research": 80}`, passed as `--max-turns` (`supervise_worker.py:222`). Then-step `supervision_then_workers.py:215-218`.
- r117: `supervise_rounds.py:112-114` writes the approval question when a gate gives no question. Then-step `supervision_rounds_steps.py:57-60`.
- r110: `supervise.py:208-215` loops `branch_review` → `fix_work_item` → green check, so a fixed work-item gets a second review in the same run. `supervise_draft.py:58-81` drafts the fix work-item. Then-step `supervision_proposal_steps.py:65-70`.

## 2. What the system answers today

Probe file: `.shop/scratch/w188-1-research/probe_r117.py`. Command: `python3 -m pytest -q -s -n 0 -W ignore .shop/scratch/w188-1-research/probe_r117.py`. Each case calls the scenario's own Background and Given steps, then `run_work` (`test_supervision.py:59`), which runs `scripts/work run i1` through `subprocess`. Run.

Scenario Givens and Whens: `supervision_given.repository` (initiative i1, started), `drafted_proposal` (p1 `drafted`), gate result set on the `initiative-round` stand-in, `run i1`.

| case (gate result) | exit | what came back (`p1.md ## Questions`) |
|---|---|---|
| a: `{"status":"DONE","questions":[]}` (the scenario's own) | 0 | one line: `Are the lines of p1 approved as drafted? Readings: approve p1 as drafted (recommended), or change its lines.` |
| b: `{"status":"DONE"}` (key absent) | 0 | same one question as a |
| c: `{"status":"DONE","questions":""}` | 0 | one line `- ` (empty) |
| d: `{"status":"DONE","questions":[""]}` | 0 | one line `- ` (empty) |
| e: `{"status":"DONE","questions":0}` | 1 | stderr: `work: the gate round of p1 (...1-gate) faulted, and p1 keeps its status drafted: initiative-round's result file ... gives its questions as 0, not a list of questions` |

Nearest cases not given by the scenario: b (absent key) and e (non-list) behave as r117 wants or refuse. c and d write an empty question (see defect D1). Not probed: a gate whose p1 already has answers, and the status p1 reaches (not printed by the probe).

Read: `supervise_worker.py:208-213` turns a string `questions` into a one-item list and refuses other non-lists. So the string case is one question, as the work-item's Implementation section says.

## 3. Old assumptions

Requirement r117 changes one assumption: an empty gate used to go straight to apply. r19 changes the researcher's turn limit. r110 changes one-review-per-run.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_rounds.py:due` (lines 45-48) | an `awaiting-answer` proposal with as many answers as questions, zero included, goes to apply (r70). An empty gate gave zero questions, so it went to apply with no decision | r117: a gate with no question now writes one, so the proposal waits for its answer. This rule is unchanged but no empty gate reaches it any more | `none` measured: no map; `by search` no test sets an empty gate and expects apply (see 4) | read, by search |
| `agents/code-scout.md:24` | tells the researcher `work run gives you 40 turns (--max-turns 40)` | r19: the researcher gets 80 (`supervise_worker.py:54`). The text is false | `none` (no test reads the agent text; `grep -n turn tests/scripts/test_agents.py` gives nothing) | search (`git grep -n "40 turns\|max-turns 40"`) |
| `README.md:174` | the 0.24 release note: "A researcher's limit is 40 turns... up from 25" | history: r19 changed it later. Not a rule | `none` | search |
| `scripts/supervise.py:pull_through` (lines 208-218) | r110 loop: fix, push, pull, re-review, once per fix | the loop is already there and bounded only by the findings (see D3) | `none` measured | read |

## 4. Tests the requirements make impossible to keep

`by search` (no map). Searched `tests/scenarios/` and `tests/scripts/` for the old 40-turn limit, for gate results with no question that expect apply, and for `turn` in agent tests.

- r19: the old scenario "a limit of 40 turns (deprecated)" was already retired (`cd134f29`, by the findings file). Nothing in the tree asserts 40. Sound.
- r117: the only gate result with no question is `supervision_rounds_steps.py:52-54` (`gate_result_no_question`), used by the r117 scenario, which asserts the new question. I did not read every default `initiative-round` stand-in plan in the other supervision steps. Not verified.
- r110: the `reviewer_lists` given (`supervision_proposal_steps.py:44-50`) and the r110 Then (`:65-70`) match the loop. Sound.
- `tests/scripts/test_agents.py`: iterates the agent files for shape (lines 26-83), asserts no turn text. Sound, nothing to change.

## 5. A step the work-item skips

Read only. `fix_work_item` (`supervise_draft.py:76`) drafts with `workqueue.add`, the function `work add` runs (its docstring), and `supervise.py:211` pushes after it. Whether `workqueue.add` commits was not probed. Nothing else found. A probe of the fix drafted by hand would show it.

## 6. Defects

### D1. A gate result with an empty question writes an empty question

Reproduction: probe `probe_r117.py`, cases c and d above. Command: `python3 -m pytest -q -s -n 0 -W ignore .shop/scratch/w188-1-research/probe_r117.py`. Came back: exit 0; `p1.md` `## Questions` holds `- ` with no text. r117 does not fire, because `supervise_rounds.py:111` builds `asked` as `[""]`, which is not empty. Not fixed; the plan decides.

### D2. The researcher is told a false turn limit

Read. `agents/code-scout.md:24` says 40 turns, `supervise_worker.py:54` gives 80. Reproduction: `git grep -n "40 turns\|max-turns 40"` lists this line and `README.md:174` (history). The branch review's findings file (`.shop/work/i30/runs/branch-review/1/findings.md`, finding 1, "Important, fix now") names this same line.

### D3. The r110 loop has no bound

Read. `supervise.py:210-215` loops while a review lists fix-now findings and each fix turns green. Nothing caps it. Findings observation 2 says the same. Not probed.

## 7. The file set

Scenarios pass today, so none of the files is needed for them. The fix the findings file names (its finding 1) is one file.

- `agents/code-scout.md`: line 24, `40 turns (--max-turns 40)` to `80 turns (--max-turns 80)`. Search: `git grep` in part 3 and findings file. No test reads it (part 4).
- `README.md`: no change; line 174 is a release note (history).
- Keeping passing: `tests/scripts/test_agents.py` (iterates the agent files; no turn text, so the sentence change does not break it). Read.

Modules on the change path, with lines (`wc -l`) and room under 300 (`tools size --limit 300` prints nothing; the whole tree is under the limit):

| file | lines | room |
|---|---|---|
| `agents/code-scout.md` | 90 | 210 (no code limit; this is text, the size tool counts .py only) |
| `scripts/supervise_worker.py` | 251 | 49 |
| `scripts/supervise_rounds.py` | 150 | 150 |
| `scripts/supervise_draft.py` | 81 | 219 |
| `scripts/supervise.py` | 265 | 35 |
| `scripts/supervise_brief.py` | 167 | 133 |
| `scripts/workqueue.py` | 290 | 10 |
| `tests/scenarios/test_supervision.py` | 260 | 40 |
