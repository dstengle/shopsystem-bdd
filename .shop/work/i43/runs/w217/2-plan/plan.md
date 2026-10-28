# plan of w217: fix finding 1 of branch review 1 of i43 (supervision r154-r157)

## 1. What goes green

The work-item accepts supervision#r154 to #r157. Every scenario tagged for them is green today (research notes part 1: `python3 -m pytest -q --work-item w217 -rfEx`, 187 passed, 0 failed). They stay green:

- r154, "before the branch review starts, <run> is run at the initiative branch's head" (seven rows): green, untouched.
- r155, "the branch reviewer is given each run made before it, with its command, how it exited and its output, and the commit they ran at": green, untouched.
- r156, "the branch reviewer is given the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less .shop/": green. It does not see the defect, because its step `gives_work_items` (tests/scenarios/supervision_branch_steps.py:144) builds only `work: <name> ...` subjects.
- r157, "the branch reviewer is given as files to read the work-items' capabilities, the design-decisions they rest on, and each work-item's plan, report and review findings": green, untouched.

What actually has to change is the defect from the findings (branch review 1, finding 1, triaged fix now). Under r156, a commit of one of the initiative's work-items is given as `none` when `work answer`, `work withdraw`, `work retry` or `work add` made it. Those subjects are `work answer: <name> awaiting-answer -> <s>`, `work withdraw: <name> <s> -> withdrawn`, `work retry: <name> failed -> <s>` and `work add: <initiative>/<name> drafted`. The four new unit cases in part 2 are red today, since each gives `none` where `w1` is expected. They go green with the fix.

The work-item retires nothing, so no deprecated scenarios are involved.

## 2. Where the change lands

- `scripts/supervise_review_read.py`: change the commit-subject matching (TRANSITION, line 11) so that it also takes the work-item name from these subjects:
  - the `work answer:`, `work withdraw:` and `work retry:` transition subjects;
  - the `work add: <initiative>/<name> drafted` subject.

  Keep the owner check at line 42 as it is: a name counts only when it is one of the initiative's work-items, else the commit gets `none`.
- `tests/scripts/test_supervise_review_read.py`: add unit cases. Each one commits a single subject and expects `w1`:
  - `work answer: w1 awaiting-answer -> ready`;
  - `work withdraw: w1 ready -> withdrawn`;
  - `work retry: w1 failed -> ready`;
  - `work add: i1/w1 drafted`.

  Add one more case for a proposal's answer, `work answer: supervision`, expecting `none`. Update the module docstring so it names these cases.

This is the researcher's file set, unchanged. Neither file is near the 300-line limit (64 and 33 lines).

## 3. Decisions

1. **Which commits belong to a work-item.** Commits made by `work answer`, `work withdraw`, `work retry` and `work add` belong to the work-item they name, when that name is one of the initiative's work-items. Rests on supervision#r156 ("each with the work-item it belongs to"): each of these commits changes or creates that work-item's file and status. The fix-now triage of finding 1 supports it.
2. **A proposal's answer stays `none`.** `work answer: <name>` with no transition (workqueue_answer.py:74, written only for a capability-proposal) is still given as `none`. Its name is a proposal, not a work-item, so it fails the owner check. Rests on supervision#r156: the commit belongs to no work-item.
3. **Unit cases, not a scenario row.** The new cases go in `tests/scripts/test_supervise_review_read.py`. `features/supervision.feature` is not changed: a scenario changes only through a formulate round, and the file is outside the file set. This is reading A in the research notes. Rests on design-decision/the-file-set-is-the-claim.
4. **No shared pattern with measure.** `scripts/measure_build.py:81,88` reads transitions by a similar subject pattern, but it is not changed and does not share the new pattern. supervision#r156 does not ask for it, and the file is outside the file set (design-decision/the-file-set-is-the-claim). If it is still wanted, it is a later work-item.
5. **Other findings left alone.** Findings 2 to 9 are not fixed here: none of them is triaged fix now. Finding 2 (the "run every command" line in supervise_review.py) belongs to review r32, which w217 does not accept. Finding 4 (the agent's exception for `work`'s own commits) and finding 7 (`Head:` read from the root) are outside the file set.

## 4. Tests the decisions break

None. What I checked:

- `test_a_proposals_transition_commit_belongs_to_no_work_item`: its subjects are `work: supervision approved -> awaiting-answer` and `work: w1 ready -> claimed`. They still give `none` and `w1` under decisions 1 and 2.
- The r156 steps (supervision_branch_steps.py:134-165) use only `work:` subjects and the `notes.txt` commit, so the fix does not change them.
- The r154, r155 and r157 steps do not execute the matching code.

This rests on the research notes, part 3, and on my own read of the unit test file.

## 5. Open cases

The implementer names these cases rather than choosing them silently:

- A `work add: <other initiative>/w1 drafted` subject in the range, where w1 is also one of this initiative's work-items. The scenarios and finding 1 do not say whether the initiative part of the subject must match this initiative.
- A subject that has the shape of a transition but comes from a command other than these four, such as a future `work <verb>: <name> a -> b`. Nothing says whether it is taken.
- Merge commits and the implementer's own commits keep the attribution they have today. The fix changes only how subjects are read.
