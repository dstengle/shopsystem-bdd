# Review of w176 (second review): DONE

Verdict: the commit does what r14 and r26-r28 ask, and their scenarios pass. The one Critical finding of the first review (5-review) was the retired deprecated @r14 outline, which w176.md does not list under Retires. The person has now answered it: "Sanctioned: w176 retires the deprecated @r14 outline at features/work-queue.feature:285-298" (w176.md `## Answers`, under the person's delegation, 2026-10-25). So the retirement is sanctioned, and no finding is Critical or fix now.

## Commits reviewed

- Claim: `9c79765c work: w176 ready -> claimed`. Done: `e0ce90ce work: w176 claimed -> done`. The branch `work/w176` is gone, so I took the commits between those two on HEAD.
- In that range, `641f95a9`, `d959d612` (w178) and `5bf9646a` (branch review of i28) belong to other work. w176's one commit is `a2d1083e work answer: --change and --accept for a reviewer's question (r14, r26-r28)`.
- The implementer's result lists `35f79e86`. Its parent is the claim commit `9c79765c`, and `git diff 35f79e86 a2d1083e` on the four files is empty. So `a2d1083e` is the same commit rebased, with no difference in content.
- No later commit touches the four files (`git log e0ce90ce..HEAD -- <files>` is empty).
- Files changed: `features/work-queue.feature` (-15), `scripts/work` (+4/-2), `scripts/workqueue_answer.py` (+15/-2), `tests/scenarios/work_queue_answer_steps.py` (+29). All four are in the fileset.

## Removed and weakened tests

Searched the diff for: deleted test functions or step definitions, Examples or parametrize rows dropped, asserts removed or loosened, skip or xfail added. Under `tests/`, the diff only adds lines.

- `test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated` (4 rows) was removed with its deprecated outline. It proved that an answer returns the work-item to the status the asking stage started from: researcher→drafted, planner→researched, implementer→ready, reviewer→done.
  - The first three rows are still asserted by the live @r14 outline (feature 285-297).
  - The reviewer row expected `done` with no verdict, which r28 now refuses.
  - The plan lists this test under "Tests the decisions break" (part 4, D3), and the person has sanctioned the retirement (w176.md `## Answers`).

## Allowances

The report's `## Tests changed under an allowance` says "none". The diff agrees: no existing test was changed.

## Cannot verify

- The report's suite count at the start (868 passed, 3 failed) and its red run (3 StepDefinitionNotFoundError). Neither can be checked from the commits. The green state can: my focused run gave 6 passed.
- That the outline was removed with `features retire` and not by hand. The diff shows only that scenario block removed, with no other feature line touched.

## Findings

### 1. Deprecated @r14 outline retired with no Retires entry: sanctioned (no longer a finding)

- **Where:** `features/work-queue.feature:285-298` (old numbering).
- **Grade:** this was Critical in 5-review. The person's answer in w176.md sanctions the retirement.
- **What remains:** w176.md still has no `## Retires` section. The sanction is recorded under `## Answers` instead.
- **Triage:** drop. The cause, that drafting by `work add` does not carry a Retires entry into a redraft, is supervision's and outside w176.

### 2. Minor: missing space at `scripts/work:127` (drop)

- **Where:** `scripts/work:127`, `o =sub.add_parser("note", ...)`.
- **What is wrong:** a space was lost while the flags were being added. Ruff does not flag it in this configuration.
- **Fix:** `o = sub.add_parser(`. Cosmetic only.

### 3. Minor: `--change`/`--accept` silently ignored on a non-reviewer question or a capability-proposal (observation)

- **Where:** `scripts/workqueue_answer.py:50`. The flags are read only inside `if not proposal and asked_by_reviewer(...)`.
- **What happens:** for a researcher's, planner's or implementer's question, or for a capability-proposal, the flag has no effect and nothing says so. The item moves by r14 or r24.
- **Reproduction:** read from the code. With `--change` on an implementer's question, the status is `asked_from(...)`, which is `ready`.
- **Why it is only an observation:** no line names this case (the plan lists it in part 5), and the result is what r14 asks for.
- **Fix if wanted:** a line, through integrating-a-proposal, that refuses the flags there or ignores them.

## Not findings, checked

- **Risk: the delegated answer path breaks on a reviewer's question now that r28 refuses.**
  - Checked: `supervise_answers.py:79` calls `workqueue_answer.asked_from`, not `answer`, so the new refusal does not reach it.
  - It still lands `done` with no verdict. That is supervision r77/r78, which w176 does not accept (plan D2, report open questions).
- **Both flags refused:** this is the r7 refusal ("cannot do what it was asked"). It is raised before any write.
- **r28 "nothing changes":** the refusal is raised before `write()` and before the log line is written. The r28 scenario checks w1.md and log.jsonl and passes.
- **Code no line asks for:** none.
  - The flags trace to r26/r27 and to the Implementation note naming `--change`/`--accept`.
  - The no-verdict refusal traces to r28, and the both-flags refusal to r7.
- **Purpose and decisions:** the reviewer's `done`-from-review guard in decision 0063 (work rule) is not contradicted. r26 and r27 refine the answer path that decision 0064 gives.

## Checks

- `tools check --base 9c79765c`:
  - ruff: 10 errors, none in w176's files. They are in `.shop/work/i29/runs/.../splice.py` (untracked scratch from other work), `tests/scenarios/supervision_intake_steps.py:84` and `tests/scenarios/test_supervision.py:14` (from `641f95a9`).
  - vulture: 1 hit, `scripts/supervise_intake.py:51`, not w176's.
  - import-linter: no contracts.
- `tools size --limit 300`: no output. No tracked Python file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w176 ready -> claimed$"`, and the same for `claimed -> done`
- `git log --oneline -12`
- `git log --format='%h %s' 9c79765c..e0ce90ce`
- `git log e0ce90ce..HEAD -- <four files>`
- `git show a2d1083e`
- `git log --format='%H %P' -1 35f79e86`
- `git diff 35f79e86 a2d1083e --stat -- <four files>`
- `grep` on `spec/capabilities/work-queue.md`, `scripts/supervise_answers.py` and `scripts/*.py`
- `sed -n` on `features/work-queue.feature:283-325` and the capability's Implementation section
- `cat spec/decisions/0063-...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9c79765c`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_work_queue.py -k "reviewer or researcher"`: 6 passed
