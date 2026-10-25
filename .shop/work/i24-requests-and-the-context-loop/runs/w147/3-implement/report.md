# Report of w147 (implement)

## Budget

1. scripts/supervise_answers.py (new)
2. scripts/supervise.py
3. scripts/supervise_brief.py
4. scripts/supervise_worker.py
5. agents/delegation-answerer.md (new)
6. CLAUDE.md
7. tests/scenarios/supervision_delegation_steps.py (new)
8. tests/scenarios/test_supervision.py

## What changed
- New `scripts/supervise_answers.py` (mixin `Answers` of `Run`, row added to CLAUDE.md's module map): reads `delegation:` from the frontmatter of the request the initiative `fulfils`; for each open question of each awaiting-answer work-item/proposal starts one `delegation-answerer` session through `Workers.worker` (stage `answer`); writes an answer as `- <date>: <text>` + indented `by: work run, under the delegation "<d>"`; moves a work-item to its asking status once every question is answered; commits and pushes.
- `supervise.py` calls `answers()` first in `run()`; `supervise_brief.py` hands stage `answer` to `answer_brief` (question, delegation, files the question names, no other content); `supervise_worker.py` has TOOLS["answer"] (Read, Glob, Grep) and a ROLE entry; new `agents/delegation-answerer.md` (Read, Glob, Grep, Write; model sonnet).
- Steps: `tests/scenarios/supervision_delegation_steps.py`, imported in test_supervision.py.

## Red and green
- Red: `python3 -m pytest -q -n 0 -k "under_a_delegation or naming_that_delegation" tests/scenarios/test_supervision.py` gave 3 failed (undefined steps); after writing steps only, 3 failed on Then assertions (`AssertionError: ('Does scripts/log.py or scripts/queue.py own the log?', [])`, no session started; `ValueError: not enough values to unpack`), as no code read a delegation.
- Green: same command, 3 passed. `python3 -m pytest -q --work-item w147`: 145 passed, 1 skipped. test_supervision.py + tests/scripts/test_agents.py: 150 passed, 15 failed; the 15 are exactly the "expected" failures of the suite record (undefined steps of other work-items).
- Suite record at start: 798 passed, 3 failed (the three scenarios of this work-item) plus the expected failing list in the brief.

## Tests changed under an allowance
none

## Open questions
- A session that faults: raised as a Refused naming the node (not failed, not left); scenarios silent.
- A delegation with a double quote or line break, or not a one-line string; unreadable request: unreadable request gives no pass.
- The pass runs once at the start of `work run`, not again after a worker asks (plan D6's repeat not done; no scenario).
- A work-item with no logged move to awaiting-answer: `asked_from` raises Refused; the Givens write that log line.

## Plan code
The plan contained no code.

## Size check
`tools size --limit 300` printed nothing.

## Outside the file set
none

## Result
Under a request's delegation, `work run` has each open question answered or left by its own session, the answer naming the delegation. Surprise: the scenarios' work-item fixture has no log line of its move to awaiting-answer, so my Given writes it. Commit 8565af5. Files: the 8 above.
