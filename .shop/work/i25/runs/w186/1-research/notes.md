# Notes: research of w186

Scope: work-queue r14, r26, r27, r28 (`work answer`). Checkout HEAD 5d006fcd. Tools: `tools refs` and `tools map`-based queries; `tools tests-of` says "no map" (not made). Counts by search where stated. Probes in `.shop/scratch/w186-1-research/` (ignored by git).

## 1. Why each scenario is red today

None is red. Command `python3 -m pytest -q -rfE -v -k "reviewer or implementers_question" tests/scenarios/test_work_queue.py` gave **6 passed** (run):
- r14 outline, 3 rows: researcher→drafted, planner→researched, implementer→ready.
- r26 (`--change` → ready), r27 (`--accept` → done), r28 (no flag → refused, nothing changed).

Code that makes them pass (read): `scripts/workqueue_answer.py:31-72` (`answer`), `:24-28` (`asked_by_reviewer`), `:15-21` (`asked_from`, `ASKED_FROM` at :9); flags at `scripts/work:125-126`, passed at `scripts/work:50`. Steps: `tests/scenarios/work_queue_answer_steps.py:19-38, 41-45`; `with_items` Given `tests/scenarios/test_work_queue.py:70-84`.

## 2. What the system answers today

Command: `python3 -m pytest -q -s .shop/scratch/w186-1-research/probe_answer.py -p no:cacheprovider -o addopts=""` gave **10 passed** (run). Each case in its own scratch repo, `scripts/work --root` via subprocess.

| case | result (run) |
|---|---|
| reviewer, `--change --accept` together | rc 1, "cannot be given together"; file and log unchanged |
| reviewer, no flag, two lines | rc 1, line-break refusal first |
| reviewer, no flag, one line | rc 1, "must say whether it asks for a change (--change) or accepts..."; unchanged |
| reviewer, `--accept` | rc 0, `w1 done`; Answers line written; log `awaiting-answer -> done` by `work answer` |
| then `--change` on the done item | rc 1, "not awaiting-answer"; unchanged |
| reviewer question, no log.jsonl, `--accept` | rc 1, "log.jsonl gives no transition of w1 to awaiting-answer"; unchanged |
| reviewer, `--change`, empty text `""` | rc 0, `w1 ready`; Answers line is `- 2026-10-25: ` (empty) |
| researcher question, `--accept` given | rc 0, `w1 drafted`; flag ignored |
| capability-proposal awaiting-answer, `--change` | rc 0, `p1 awaiting-answer`; answer written, flag ignored |
| reviewer, `i1/w1` form, `--change` | rc 0, `i1/w1 ready` |
| reviewer, `--accept`, single item in initiative | rc 0, `w1 done`; no initiative.md written |

Read: the reviewer rule is keyed on log.jsonl's last move into awaiting-answer being from `done` (`workqueue_answer.py:24-28`). A reviewer question with a log line from another stage is not a reviewer's question.

## 3. Old assumptions

Old rule: an answer returns the item to the status of the stage that asked (`asked_from`). Places still making it:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/workqueue_answer.py:asked_from` (:49) | still called before the reviewer branch; for a reviewer's question returns `done`, then overwritten at :53 | r26/r27 replace that status for reviewers; the call is dead for them | r14 rows and r26-r28 (run); by search | read |
| `scripts/supervise_answers.py:answers` (:77-79) | a delegated answer that fully answers a work-item moves it to `asked_from(...)`: for a reviewer's question, `done` | no flag on this route; r26 `ready` never reached on it; `--change` not available here | none by search: no feature or step gives a delegated reviewer question | read; also branch review 3 finding 3 |
| `scripts/supervise.py:STAGES` (:36) and `MOVABLE` (:38), pulled at :206 | `done` is the review stage's start; the review's DONE moves `done -> green` (:157-171) | r27 `--accept` lands `done` and skips the review's end (`green`); the next `work run` pulls the item to review again | `tests/scenarios/supervision_then_workers.py:268-272` (review after green) only; none for an answer's `done` | read |
| `scripts/supervise_brief.py:findings_lines` (:98) | reads log.jsonl's `done -> awaiting-answer` then `awaiting-answer -> ready` pair for the r98 findings line | unchanged by r26; the pair is what `--change` writes | `tests/scenarios/supervision_answers_steps.py:50-57` (hand-written log, not `work answer`); by search | read |
| `spec/decisions/0063-a-ruling-returns-to-the-asking-stage.md:21` | a reviewer's question has one exit, `-> done` | conflicts with r26 `ready`; spec, not code | none | branch review 3 finding 2; read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` exits "no map" (I did not make one). By search:
- The deprecated r14 outline's reviewer row (asserting reviewer → done) is gone: removed by w176 (`a2d1083e`, per branch review 3). It can no longer pass by design; nothing live still asserts it.
- `tests/scenarios/test_work_queue.py:79` maps a reviewer to `done` in the Given's log. Consistent with `asked_by_reviewer`; sound.
- Verified sound: the six run tests above; the probes; `work_queue_answer_steps.py` expectations.
- None that can no longer pass.

## 5. A step the work-item skips

- `work answer` transitions with `workqueue.move` directly (`workqueue_answer.py:67`), not `workqueue.moved_to` (`workqueue.py:242`), so the r23 check (`workqueue_done.becomes`) does not run. Effect: none today, since `done` is neither green nor withdrawn (`workqueue_done.py:31`). Read; probe `reviewer, --accept` shows no initiative.md (run).
- The review's end step is skipped: the `done -> green` move with its commit by `supervise` (`supervise.py:157-171`) does not run on `--accept`. Read; see §3 row 3.

## 6. Defects

### D1: empty answer accepted and moves the item
Commands: `scripts/work --root <repo> answer w1 "" --change` on an awaiting-answer reviewer's question.
Came back: rc 0, `w1 ready`; the Answers section gets `- 2026-10-25: ` with no text; log `awaiting-answer -> ready`. Run. Compare `supervise_answers.py:108` refuses an empty session answer.

### O1: a flag on a capability-proposal or another asker is ignored silently (observation, run)
`answer p1 "x" --change` → rc 0; `answer w1 "x" --accept` on a researcher's question → `drafted`. Not in the four scenarios; r26/r27 say reviewer's question only.

### O2: reviewer `--accept` returns the item to `done`, the review's own start (read, see §3 row 3, §5)
Whether this is a defect is a reading question; see Questions.

## 7. The file set

For the four accepted scenarios: **none** — they pass today (run). Files the branch review named that are not in these scenarios (for the plan to decide):
- `scripts/workqueue_answer.py` — 72 lines (room 228) — D1 refusal; drop `asked_from` call for reviewers (§3 row 1).
- `scripts/supervise_answers.py` — 128 lines (room 172) — §3 row 2, delegated reviewer route.
- `scripts/supervise.py` — 260 lines (room 40) — §3 row 3 only if the review's end is to be taken on `--accept`.
- `scripts/supervise_brief.py` — 162 lines (room 138) — read only, no change expected.
- `scripts/work` — 171 lines (room 129) — only if the flags' help text changes.
- `scripts/workqueue.py` — 290 lines (room 10) — `moved_to`, read only.
- `scripts/workqueue_done.py` — 67 lines (room 233) — read only.
- `tests/scenarios/work_queue_answer_steps.py` — 71 lines — only if D1 changes.
- `tests/scenarios/test_work_queue.py` — 288 lines by read (room 12) — no change expected.
- `spec/decisions/0063-a-ruling-returns-to-the-asking-stage.md` — spec, not a module — finding 2.
- `.shop/work/i25/w176.md` — record, no `## Retires` (branch review 3 finding 1) — not a code change.

Size limit: 300 (CLAUDE.md).

## Questions for the plan
1. `--accept`: does `done` end the review (the scenario's wording, decision 0063), or should it land `green` (the review's own end)? Both readings are in §3 and §5. Today a reviewer's accept is re-reviewed by the next `work run`.
2. Should an empty answer be refused (D1)?
3. Should delegated reviewer answers take the flags, or stay on `done` (§3 row 2)?
