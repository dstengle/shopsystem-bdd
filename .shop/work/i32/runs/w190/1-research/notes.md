# Research of w190 (supervision r118, r119)

Scope: the two accepted scenarios, both under `features/supervision.feature` (lines 1458-1474). Tools: `tools refs` works; `tools tests-of` and `untested` have no map (`tools map` runs the suite, not done), so every test list below is `by search`. Probes ran in `.shop/scratch/w190-1-research/` only.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q -n 0 -p no:cacheprovider tests/scenarios/test_supervision.py::test_under_a_delegation_an_answer_to_a_reviewers_question_that_asks_for_a_change_makes_the_workitem_ready_again` (and the `..._accepts_..._done` node). Both fail at once with `StepDefinitionNotFoundError`:

- Given `i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer` (feature line 1462 and 1471). No step matches. Existing steps: `two_unanswered` (`supervision_delegation_steps.py:48`) needs "each with no answer" and two questions; `reviewer_asked` (`supervision_answers_steps.py:40`) needs "the reviewer having written findings.md". Missing: a step in `tests/scenarios/supervision_delegation_steps.py` (or `supervision_answers_steps.py`).

Read (not reached, pytest stops at the first undefined step):
- When `the session answering under the delegation answers "No, remove the old reader.", an answer that asks for a change, and every worker gives DONE` (1463) and the `... "Yes, keep it as it is.", an answer that accepts ...` (1472). Step `supervision_delegation_steps.py:66` matches only `answers "<a>", and every worker gives DONE$`; the extra clause is unmatched. Missing: a step with the change/accept clause, and a stand-in plan field that says which.
- Then `w1's transition from awaiting-answer to ready (done) was made once the session had answered`. No step in `tests/scenarios` (grep `transition from awaiting-answer` empty). Missing: a Then that reads the log for the move, after the session's answer.

Code behind them (read): `scripts/supervise_answers.py`
- `Answers.answers` (l.60-82) writes the answer, then moves the item to `workqueue_answer.asked_from(...)` (l.79). It never returns `ready` or `done` by the answer's kind. Missing: a branch for a reviewer's question (log's last move into awaiting-answer from `done`) that decides ready on change, done on accept.
- `Answers.ask` / `answer_brief` (l.90-128) ask the session only for `answer`, one line. No change/accept field exists in the brief, the result contract or `ask`. Missing: a verdict field in the brief (l.118-127) and read in `ask` (l.107-110).

## 2. What the system answers today

Probe `probe_delegation.py` (`.shop/scratch/w190-1-research/`), run as `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w190-1-research/probe_delegation.py`. It calls `workqueue_answer.answer` on a scratch repo, the log's last move into awaiting-answer given per case. Run, results:

- reviewer's question (log `ready→claimed→done→awaiting-answer`), `change=True`: returned `ready`, file `ready`.
- same, `accept=True`: returned `done`, file `done`.
- same, neither flag: Refused, "the answer must say whether it asks for a change (--change) or accepts the work-item as it is (--accept)".
- log `drafted→awaiting-answer`, `change=True`: returned `drafted`; the flag is ignored.
- `asked_from` with last move `done→awaiting-answer`: `done`. `asked_by_reviewer`: True.

Read: `answers()` does not call `workqueue_answer.answer` at all. So the library's `ready` route is not reached on the delegation path. On the delegation path `asked_from` gives `done` for a reviewer's question on either answer, so a change answer lands at `done`, not `ready` (see defect D1).

Nearest cases, read (not run):
- Log with no move into awaiting-answer (the existing `reviewer_asked` step writes none): `asked_from` raises Refused "log.jsonl gives no transition ... has no status to return it to"; `answers()` calls it once every question is answered, so the run exits with that error (see D2).
- The scenario's own helper `asked_by_the_log` (`supervision_delegation_steps.py:32-36`) writes `drafted→awaiting-answer`, so a scenario that reuses it gives `drafted`, not `ready` or `done`.
- Answer with a line break: `ask` returns None, the question is left (l.110).
- Session with outcome other than DONE, or no `answer`: None, left (l.108-109).

## 3. Old assumptions

Table. "tests" column: `by search` (no map); `none` where no test executes the place.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_answers.py:Answers.answers` l.79 | moves the item to `asked_from` whatever the answer says | must move a reviewer's item to `ready` on change, `done` on accept | by search: `supervision_delegation_steps.py` r77/r78 steps (not run) | read; `refs asked_from` |
| `scripts/workqueue_answer.py:asked_from` l.15-21 | maps `claimed`→`ready`, else returns the logged `before` | a reviewer's `done` must not return as `done` on change | by search: `work_queue_answer_steps.py` (not run) | `refs asked_from` (1 caller) |
| `scripts/workqueue_answer.py:answer` l.46-53 | the one place that decides ready on `--change`, done on `--accept`, and refuses neither | the rule r118/r119 need, but reached only by `work answer` | by search: `work_queue_answer_steps.py:19-45` (not run) | read |
| `scripts/supervise_answers.py:Answers.ask` / `answer_brief` l.90-128 | session's result carries `answer` only | must carry the change/accept verdict | by search: `supervision_delegation_steps.py:66-86` stub plans (not run) | read |
| `scripts/supervise_answers.py:Answers.answers` l.74-75 | writes `date: answer` and `by: work run, under the delegation` | a verdict is not recorded | by search: `supervision_delegation_steps.py:165-175` (not run) | read |
| `scripts/supervise_brief.py:findings_lines` l.102-103 | needs the log's `done→awaiting-answer` then `→ready` to name the findings | r118 must leave a log line `awaiting-answer→ready` after `done→awaiting-answer` for r98 | by search: `supervision_answers_steps.py:50-57` (not run) | read |
| `scripts/supervise.py` STAGES l.36-37 and MOVABLE l.39 | `done` starts the review stage | r119's `done` is a status the review stage starts from | by search: `supervision_review_steps.py` (not run) | read |
| `scripts/supervise.py:pull_through` l.208 | branch review and set-done only when every work-item is `green` or `withdrawn` | r119 puts a work-item at `done`, so the initiative is not closed (see Conflict C2) | by search: `supervision_analysis_steps.py` (not run) | read |

## 4. Tests the requirements make impossible to keep

By search (no map). Read: `tests/scenarios/supervision_delegation_steps.py` (all, 175 lines), `supervision_answers_steps.py` (all), `work_queue_answer_steps.py:19-45`, `supervision_review_steps.py` (headers). None asserts the status an answer leaves a work-item in: the r77/r78 scenarios check the Answers bullet, the session's brief, the left question. The r98 scenario (`supervision_answers_steps.py:50-57`) writes its own log and is not affected by changing `answers()`. Verdict: none can no longer pass as written, as far as read; not run, so this is "none found by reading".

## 5. A step the work-item skips

The delegation path (`answers()`) skips `workqueue_answer.answer`, which has the reviewer's change/accept rule and its refusals. Effects only that step makes:
- refusal: a reviewer's answer with neither flag is refused (run: probe `rev_noflag`). The delegation path has no such refusal.
- effect: a commit `work answer: w1 awaiting-answer -> <status>` and a log line `by: work answer` (read, `workqueue_answer.py:71`). The delegation path writes `by: work run`.
- refusal: `workqueue.agrees` not `awaiting-answer` (read, l.46-47).
- refusal: answer with a line break (read, l.34-35).
- refusal: `--change` and `--accept` together (read, l.36-37).

## 6. Defects

D1. A change answer to a reviewer's question returns the work-item to `done`, not `ready`.
- Reproduction (run, library): `probe_delegation.py::test_asked_from_done` prints `asked_from with last before=done -> done`.
- Reproduction (read): `supervise_answers.py:79` moves to `asked_from(...)`, which gives `done`. No change-branch exists on this path.
- Not run through `work run` (the r118 Given is undefined, so the scenario cannot run).

D2. (read, not run) A work-item every question of which is answered, with no move into awaiting-answer in its log, makes `asked_from` raise Refused, and the run exits with that error. Trigger: `supervision_answers_steps.py:reviewer_asked` writes no log. Whether this is wrong depends on the reading of r118 (Conflict C1).

## Conflicts for the plan (both readings given, not decided)

C1. How a question counts as a reviewer's. (a) The log's last move into awaiting-answer is `done` (what `workqueue_answer.asked_by_reviewer` and `supervise_brief.py:103` read). (b) The Given's text alone. The step helper `asked_by_the_log` writes `drafted`, so the r118/r119 steps must write a `done` log to get (a).
C2. r119 `done` on accept. (a) `done` is in MOVABLE and starts the review stage (`supervise.py:36-39`), so the reviewer runs again on the accepted item. (b) The item is kept `done` and not pulled again, a new rule. Also `pull_through` l.208 needs every work-item green or withdrawn before the branch review and set-done, so a `done` item keeps the initiative open (r105).
C3. How work run learns the verdict. (a) a new field of the answering session's result (`change`/`accept`); the brief (`supervise_answers.py:118-127`) gets the instruction. (b) read the answer text. The scenario answers ("No, remove the old reader." / "Yes, keep it as it is.") carry no marker, so (a) is what fits the Given.

## 7. The file set

Changes (production):
- `scripts/supervise_answers.py` (128 lines; room 172): reviewer branch in `answers()` (ready on change, done on accept); verdict field in `answer_brief` and `ask`; the answer's by-line. Found by read of the file; `refs` gives no callers of `answers` (method via `Run`).
- `scripts/workqueue_answer.py` (72; room 228): probably reuse its `asked_by_reviewer` and the change/accept rule for `answers()`, or a helper it exports. Found by `refs asked_from`, read l.24-53.
- `scripts/supervise.py` (265; room 35): only if C2 is decided as a guard in `pull` or `STAGES`. Found by read l.33-39, 208.

Changes (tests):
- `tests/scenarios/supervision_delegation_steps.py` (175; room 125): the undefined reviewer's-question Given, the change/accept clause regex, the transition Then, and a `done` log helper for C1. Found by the undefined-step run and by read of l.14-86.
- `tests/scenarios/supervision_answers_steps.py` (88; room 212): if the reviewer Given is put beside `reviewer_asked`. Optional.

Must keep passing, no change expected:
- `tests/scripts/stub_claude.py` (273; room 27): stand-in fields are generic (l.256), so a verdict field needs no stub change. Read.
- `scripts/supervise_brief.py` (167; room 133): the r98 route, only the log shape matters. Read.
- `scripts/supervise_worker.py` (251; room 49), `scripts/supervise_done.py` (36): on the path of the review stage and set-done; no change expected. Read.
- `tests/scenarios/test_supervision.py` (260; room 40), `tests/scenarios/supervision_world.py` (173; room 127): collection and the shared world. Read.

Sizes are `wc -l` as the working tree has them; limit 300 (CLAUDE.md size rule).
