# Review of w176: DONE_WITH_CONCERNS

Verdict: the code does what r14 and r26-r28 ask, and the r14/r26/r27/r28 scenarios pass. One Critical finding: the commit retires a deprecated scenario that w176.md does not list under Retires. The retirement itself is sound (the reviewer row of the retired outline expects what r28 now refuses, and w174, which w176 redrafts, listed exactly this entry), but under the rules only the person can sanction it. So the work-item goes to the person.

## Commits reviewed

- Claim: `9c79765c work: w176 ready -> claimed`. Done: `e0ce90ce work: w176 claimed -> done`. Branch `work/w176` is gone, so I took the commits between these two on HEAD.
- In that range, `641f95a9` (supervision r9 r67 r82 r100 r101), `d959d612` (w178 done, i26) and `5bf9646a` (branch review 6 of i28) belong to other work. w176's one commit is `a2d1083e work answer: --change and --accept for a reviewer's question (r14, r26-r28)`.
- The implementer's result lists `35f79e86`. That commit exists with the same message, its parent is the claim commit, and `git diff 35f79e86 a2d1083e` on the four files is empty. So `a2d1083e` is `35f79e86` rebased onto `5bf9646a`, and there is no difference in content.
- Files: `features/work-queue.feature` (-15), `scripts/work` (+4/-2), `scripts/workqueue_answer.py` (+15/-2), `tests/scenarios/work_queue_answer_steps.py` (+29). All are in the fileset.

## Removed and weakened tests

Searched for: deleted test functions or step defs, dropped parametrize rows or Examples rows, removed or loosened asserts, added skip or xfail. The diff of `tests/` only adds lines. The one removal is the feature outline below; its test comes from `scenarios()` in `test_work_queue.py`.

- `test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated` (4 rows: researcher→drafted, planner→researched, implementer→ready, reviewer→done) was removed with its outline. Before, it proved that an answer returns the item to the asking stage's start status, for all four askers. The three stage rows are still asserted by the live @r14 outline (feature 285-297). The reviewer row expected `done` with no verdict, which r28 now refuses. The plan lists this test under "Tests the decisions break" (part 4, D3). The removal of the scenario itself is Finding 1.

## Allowances

The report's `## Tests changed under an allowance` says "none". The diff agrees: no existing test was changed.

## Cannot verify

- The report says the suite at start had 868 passed and 3 failed, and that the red run had 3 failures from StepDefinitionNotFoundError. Neither can be checked from the commits. The green state can: the focused run passed (6 passed).
- That the outline was removed with `features retire`, as the report says, and not by hand. The diff shows the scenario block removed cleanly, with no other feature lines touched.

## Findings

### 1. Critical: deprecated scenario retired, but w176 lists no Retires (fix now)

- **Where:** `features/work-queue.feature:285-298` (old numbering). The removed scenario is "answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)" (@r14 @deprecated).
- **What is wrong:** w176.md has no `## Retires` section. A change under `features/` is allowed only when it removes a deprecated scenario that the work-item lists under Retires.
- **What the plan says:** the plan takes the retirement as decision D3 and says so openly (part 1 and part 5). w174, which w176 redrafts, has this very entry under `## Retires` (w174.md:13-15). The plan names the cause: `supervise_draft.retires` did not carry it over when w176 was drafted.
- **Why it matters:** retiring a scenario is the person's call, carried by the work-item, not an implementer's decision.
- **On the substance:** the retirement is right. Its reviewer row (`a reviewer | done`, with no verdict) contradicts r28, and its other three rows are the live r14 outline's.
- **Fix:** the person sanctions it by adding w176's `## Retires` entry (as in w174) or a ruling. Separately, consider why drafting did not carry w174's Retires into its redraft. That is supervision, out of w176's scope.

### 2. Minor: missing space in `scripts/work` (drop)

- **Where:** `scripts/work:127`, `o =sub.add_parser("note", ...)`.
- **What is wrong:** a space was lost by accident while the flags were being added. Ruff does not flag it in this config.
- **Fix:** `o = sub.add_parser(`. Cosmetic.

### 3. Minor: `--change`/`--accept` ignored silently on a non-reviewer question (observation)

- **Where:** `scripts/workqueue_answer.py:50`. The flags are read only inside `if not proposal and asked_by_reviewer(...)`.
- **What happens:** on a researcher's, planner's or implementer's question, or on a capability-proposal, the flags are dropped with no word, and the item moves by r14 or r24.
- **Reproduction:** read from the code. With `--change` on an implementer's question, `answer` returns `asked_from(...)` = `ready`. The flag has no effect and nothing says so.
- **Why it is only an observation:** no line names this case (plan part 5 lists it as open), and the result is still what r14 asks for.
- **Fix if wanted:** a line, through integrating-a-proposal, that refuses or ignores the flags there.

Not findings, checked:

- **Both flags refused (D1):** this is the r7 refusal. It runs before any write, so nothing changes.
- **r28 refusal:** it is raised before `write()` and the commit, so "nothing changes" holds. The r28 scenario checks the file and log.jsonl and passes.
- **Delegated reviewer answer:** the path through `supervise_answers.py` still lands `done` with no verdict (D2). That is supervision's (r77/r78), which w176 does not accept. Recorded as an open case in the plan and the report.
- **Code no line asks for:** none. The flags, both refusals and the transitions trace to r26, r27, r28 and r7, and to the Implementation note naming `--change`/`--accept`.

## Checks

- `tools check --base 9c79765c`:
  - ruff: 2 errors, both in files w176 did not touch (`tests/scenarios/supervision_intake_steps.py:84`, `tests/scenarios/test_supervision.py:14`, from `641f95a9`).
  - vulture: 1 hit, in `scripts/supervise_intake.py:51`, also not w176's.
  - import-linter: no contracts.
  - None in w176's files.
- `tools size --limit 300`: no output. No tracked Python file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w176 ready -> claimed$"` (and the same for `claimed -> done`), `git log --oneline -15`
- `git log --stat 9c79765c..e0ce90ce`, `git show a2d1083e`
- `git diff --stat 9c79765c 35f79e86`, `git diff 35f79e86 a2d1083e -- <four files>`, `git log --format='%H %P' -1` on both commits
- `grep` on `spec/capabilities/work-queue.md`, `features/work-queue.feature`, `w174.md`, `w176.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9c79765c`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q tests/scenarios/test_work_queue.py -k "reviewer or researcher or deprecated"`: 6 passed
