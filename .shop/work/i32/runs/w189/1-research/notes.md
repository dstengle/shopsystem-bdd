# Research of w189: review#r31

Work-item w189 accepts review#r31: a branch review's result `questions` carry only the findings it triages fix now.
Spec line already in the worktree (review.md, commit cb357911). Method: text search; `tools tests-of` has no map
("tools: no map: make one with tools map", not made); `tools refs` resolves no method call (0 references for
`fix_work_item`, `lists_nothing`, both called through `self.`), so callers are by search. Probes run in
`.shop/scratch/w189-1-research/`. A plain pytest run collects 0 of the 203 supervision scenarios (the session's pytest
options carry `--work-item`), so scenarios ran with `--whole-suite -n 0 -m ""`.

## 1. Why each scenario is red today

None. No feature tags `@r31` for review: `@r31` appears only in features/migration-tools.feature and
features/supervision.feature, neither for review#r31. review is `group: guarantees`, and it has no feature file
(`features/review*` absent), so the work-item needs no scenario (ledger: formulate round 4, review). Nothing to run red.

## 2. What the system answers today

Probes (no scenario accepts r31; these are its nearest cases):

- `python3 -m pytest -q --whole-suite -n 0 -m "" <node ids>` on the three supervision scenarios that carry a branch
  review's questions: `test_a_kept_branch_reviews_findings_to_fix_now_..._the_workitem_they_concern`,
  `test_when_every_workitem_is_green_or_withdrawn_and_the_kept_branch_review_lists_nothing_to_fix_now_...`,
  `test_a_kept_branch_review_that_ended_partial_..._no_measure_initiative_is_run`, with tests/scripts/test_agents.py.
  Result: 11 passed, 18 subtests passed. `run`.
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w189-1-research/probe_r31.py`: calls
  `supervise.Run.fix_work_item` on a kept review whose result.json `questions` hold one line each (store is its own git
  repository in scratch). Result, `run`:
  - `["Important, w1, thing.py:3: wrong answer, fix now"]` → True, drafts `w2` (the fix-now case).
  - `["Critical, w1, thing.py:9: a change under features/ outside Retires, not fix now"]` → True, drafts `w2`.
  - `["w1: check \`python3 -m pytest -q x\` cannot be verified from the commits"]` → True, drafts `w2`.
  - `[]` → False, drafts nothing.
- `read`: `lists_nothing` (supervise_analysis.py:19-26) needs status `DONE` and empty `questions`; a `DONE` review never
  carries Critical or unverifiable lines under the agent's status rule, so today's outcome is the same either way.

## 3. Old assumptions

Old form: a branch review's `questions` = fix-now findings **plus** Critical findings **plus** unverifiable checks.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| agents/bdd-branch-reviewer.md:74 (the `questions` rule) | tells the reviewer to list each fix-now or Critical finding and each unverified check | must list only fix-now findings | none (no test reads the prompt text; test_agents.py checks frontmatter only) | search |
| scripts/supervise_draft.py:58 `fix_work_item` | drafts one work-item for any question line naming a work-item of the initiative | input narrows to fix-now lines; the code itself needs no change, but today it drafts Critical and check lines (probe) | supervision.feature:1016 (run, passes); :1450 (not run) | search; `refs` gave 0 |
| scripts/supervise.py:210 and :216 `pull_through` | calls `fix_work_item(kept)` in a loop, then `lists_nothing(kept)` | same inputs as above | supervision.feature:1016, :1450, :1024, :1033 (run) | search |
| scripts/supervise_analysis.py:19 `lists_nothing` | `DONE` and empty `questions` = nothing to fix now | unchanged in outcome: `DONE` already excludes Critical and unverified checks; empty `questions` now means no fix-now finding | supervision.feature:1024, :1033 (run, pass) | search |
| scripts/supervise_review.py:44 `branch_review` (brief text, line 52-58) | sends the brief with "`questions`" and no content rule; calls `self.session` directly, so no worker result check (supervise_worker.py:208-213) runs on it | none to change | none executes the brief text by content | read |
| skills/analyzing-a-batch/SKILL.md:20 | reads the branch review's Critical and Important findings from findings.md | not on `questions`; unchanged | none (skill text) | search |

Places the change does not touch: `scripts/supervise.py` `show` and `work status` print work-item questions only, not a
branch review's (read: supervise.py:188-231). So a Critical or unverified-check line, once dropped from `questions`,
appears nowhere but findings.md and the `status` `DONE_WITH_CONCERNS`.

## 4. Tests the requirement makes impossible to keep

None found. `tests-of` has no map, so this list is by search: every test that feeds `bdd-branch-reviewer` a result
(tests/scenarios/supervision_proposal_steps.py:48-49 `FIX_NOW`, all `Important`, and `[]`;
supervision_analysis_steps.py:19 `[]`, :40 `PARTIAL` with `[]`). All still pass under r31 (they stub the result file).
Searched tests/scenarios/supervision*.py and tests/scripts/*.py for `Critical`, `cannot verify`, `unverif`: no test
asserts a Critical or unverified line in `questions`. Verified sound.

## 5. A step the work-item skips

The step the requirement drops: a branch review's Critical findings and unverified checks go to `questions`. Effects
that only that step produces today (`run`, probe above):
- a drafted fix work-item (`w2`, status `drafted`, `findings:` naming findings.md) for a Critical line and for an
  unverified-check line. Nothing else in the code reads those lines (read: `work status` shows work-item questions only).
- with the findings file, the only place the person sees either under r31 (plus `DONE_WITH_CONCERNS` in result.json).

Conflict for the plan (both readings given, not decided): review#r6 says a branch review that cannot verify a check
**fails the review**. Under r31 that check is no longer in `questions`. The agent's status rule still makes it
`DONE_WITH_CONCERNS`, so the fail stays in `status`, not in `questions`. Reading A: status carries the fail, and
`questions` is fix-now only, as r31 says. Reading B: the unverified check still reaches `questions`, which r31 forbids.

## 6. Defects

D1. A line that is not fix-now becomes a drafted fix work-item.
Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w189-1-research/probe_r31.py`
(tests `test_critical_observation_question_drafts_today`, `test_unverifiable_check_question_drafts_today`): each
returns True and writes `.shop/work/i1/w2.md` with `status: drafted`. Against supervision#r74 ("findings to fix now
become one work-item"), the drafted work-item is wrong for these lines. Not judged here; see section 5.

## 7. The file set

- `agents/bdd-branch-reviewer.md`: line 74, the `questions` rule becomes "each fix-now finding, in one line (grade,
  work-item, file:line, what is wrong), else empty"; line 71's status rule stays. Found by search (grep of `questions`
  under agents/). It is markdown, not Python: no line limit applies.
- No test file: no scenario accepts r31, and every test that passes today keeps passing (section 4).
- No `scripts/` file: `fix_work_item` and `lists_nothing` read `questions` as it comes; the change narrows their input.

Modules on the change's path, edited or not (Python, limit 300 from CLAUDE.md):
- scripts/supervise.py: 265 lines, room 35.
- scripts/supervise_draft.py: 81 lines, room 219.
- scripts/supervise_analysis.py: 80 lines, room 220.
- scripts/supervise_review.py: 82 lines, room 218.
