# Plan of w177 (requests: questions and answers written through work)

## 1. What goes green

All from the research notes, section 1 (runs of the node ids in `tests/scenarios/test_requests.py`).

- **requests#r20**: "the upstream asking a question on a line in its turn writes the question in the request". Red: the When `the upstream asks the question "Which queue?" on line 1 of q1` has no step definition, `scripts/work` has no question subcommand, and `workqueue_request.py` has nothing that writes `## Questions`.
- **requests#r21**: "the asker answering a question in its turn writes the answer in the request". Red: the Given `q1 holds the upstream's question ...`, the When `the asker answers that question with ...` and the Then `q1 holds the answer ... to the question ...` are all undefined, and nothing writes an answer. `work answer q1` is the work-item command and refuses.
- **requests#r4**: "outcome writing a line outcome leaves the request's lines and answers as the asker wrote them". Red: the Given with a question and an answer, and the Then `q1's answers are as they were`, are undefined. The production side already holds: probe 3 shows `work outcome` leaves hand-written Questions and Answers alone.
- **requests#r5**: "the asker answering a question leaves the request's questions and line outcomes as they were and writes no resolution". Red: the Given with a question, the answer When and the Then `q1's questions are as they were` are undefined, and there is no answer writer.
- **requests#r12**: "a change to a request commits the request on the current branch". Red: the ask When is undefined. The commit itself exists (`_change` → `workqueue.committed`).

Retired. The work-item's Retires list removes these deprecated scenarios. All three pass today.
- "outcome writing a line outcome leaves the request's lines as the asker wrote them (deprecated)" (@r4, features/requests.feature:70)
- "turn passing a request leaves its line outcomes as they were and writes no resolution (deprecated)" (@r5, :87)
- "a command that changes a request commits the request on the current branch (deprecated)" (@r12, :206)

## 2. Where the change lands

- `scripts/workqueue_request.py`: two new writers, each going through `_change`, so each is committed on the current branch (r12):
  - an ask writer: refused in the asker's turn; appends the next numbered entry under `## Questions`, naming the line it is on and the upstream's words.
  - a reply writer: refused in the upstream's turn; writes the entry numbered n under `## Answers` as the answer to question n.
  - The new-request template also gets empty `## Questions` and `## Answers` sections.
  - The module docstring names the two new sections and their entry form.
- `scripts/work`: two subcommands, `ask` and `reply` (Decision 1), parsed and dispatched in `main` the way `outcome` is. A Refused exits with an error, as with the other request commands.
- `tests/scenarios/requests_write_steps.py`:
  - Givens: the question on a line, and the question with the asker's answer to it.
  - Whens: the upstream asks; the asker answers that question. Each runs the new subcommand.
  - Thens: holds the question on line n; holds the answer to the question; questions are as they were; answers are as they were.
- `tests/scenarios/requests_steps.py`: `write_request` can write `## Questions` and `## Answers` entries when a Given supplies them, in the same entry form the writers use (Decision 3).
- `features/requests.feature`: remove the three deprecated scenarios from part 1.
- `CLAUDE.md`: the module-map row for `scripts/workqueue_request.py` adds `ask` and `reply` to its commands. This is added to the researcher's set because the map names that module's commands.

Not in the set:
- `scripts/supervise_intake.py`: its brief's `outcome <n> question` route. No accepted requirement or scenario asks for it, and it is supervision's concern (open case 5).
- `scripts/workqueue_answer.py`: untouched (Decision 1).
- `tests/scenarios/test_requests.py`: it binds the whole feature, so it needs no edit.

## 3. Decisions

1. **The two commands are new: `work ask <request> <line> <question>` and `work reply <request> <question number> <answer>`. `work answer` is not overloaded.**
   - Rests on: design-decision/requests-written-through-work (0067), "each part is written by its own command", and the capability's Implementation, which says how `work` keeps and writes a request is `work`'s own.
   - Overloading `work answer` by the form of the id would change what the existing work-item command returns for a `q<n>` argument. That command belongs to work-queue's requirements, not this item's.
   - The command's name is not something the narrator sees come back, stored or refused. The scenarios speak only of "asks" and "answers".
2. **Questions are numbered in the order asked, and each entry names its line.** The n-th answer answers the n-th question and is written under the same number.
   - Rests on: requests#r20 ("on a line"), requests#r21, and the Implementation line on r20 and r21 ("the n-th answering the n-th").
   - So two questions on one line do not overwrite each other, which keying by line number would do (notes section 3, `_numbered`).
3. **The entry form follows the request's other sections, `<n>. <text>`.** A question's text carries its line number before the question's words. An answer's text is the asker's words only.
   - Rests on: the capability's Implementation (sections `## Questions` and `## Answers`) and `model_requests.SECTIONS`, which already accepts both sections, so `model check` holds.
   - The implementer names the exact separator, and the steps read the same form.
4. **Ask is refused in the asker's turn and reply in the upstream's turn.** Each refusal names whose turn it is and changes nothing. The turn is read from the request's `turn` field, as `outcome` does it (no command takes a side).
   - Rests on: requests#r16 and 0067 ("in its side's turn only").
5. **Asking writes only the question.** It does not set the line's outcome to `question`, and replying does not touch Outcomes, Questions or Resolution.
   - Rests on: 0067 ("each part is written by its own command") and requests#r5. The r21 and r5 scenarios give the `question` outcome in their Given, and `work outcome` writes it.

## 4. Tests the decisions break

None. Checked against notes section 4 and by search:
- No test asserts that a request has no Questions or Answers section, or uses a `work ask` or `work reply` name.
- No test inspects the subcommand list of `scripts/work`.
- The new-request template gaining two empty sections leaves the r1 Thens holding, since they read Lines, asker and origins.
- `accepted_lines` reads only Outcomes and Lines.
- The steps the three removed scenarios used (the `work turn` and `work outcome` Whens, `gives line 1 the line outcome question`, `has no resolution`, the git Givens and Thens) are still used by live scenarios: r7, r18, r16, the new r5 and r12. Removing them leaves no dead step.

## 5. Open cases

The scenarios are silent on these. The implementer names each one and does not choose it:
1. A question on a line the request does not have (like D1 for `outcome`).
2. A reply to a question number that has no question, or to a question that already has an answer.
3. An empty question or answer text.
4. Whether the reply command should also refuse when the request is `delivered`, `accepted` or `refused`.
5. `scripts/supervise_intake.py` still tells an intake session to put a question's text in its result rather than run `work ask`. That is a supervision line, not this work-item's.
6. Defects from the notes that sit outside the accepted set: D1 (an outcome on a missing line), D2 (an empty request), D3 (an empty `--delegation` accepted, against r22), D4 (`turn` run out of turn) and D5 (any outcome word accepted).
7. The scratch directory `.shop/scratch/w177-1-research/` left by the research stage. It is not part of this change.
