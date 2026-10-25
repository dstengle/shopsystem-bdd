# Review of w177 (requests: questions and answers written through work)

**Verdict: DONE.** No Critical finding and nothing to fix now. The change is what the plan asked for. Two observations and two Minor findings follow.

## Commits reviewed

The branch `work/w177` is gone. So the commits are those between `87424bc6 work: w177 ready -> claimed` and `1e8ddfdc work: w177 claimed -> done` on HEAD, less `work run`'s own `work:` commits:

- `db4d07f2` work ask and reply write a request's questions and answers; retire three deprecated request scenarios

This matches the implementer's `result.json` and `report.md` (`db4d07f2`).

Files changed: CLAUDE.md, features/requests.feature, scripts/work, scripts/workqueue_request.py, tests/scenarios/requests_write_steps.py. All are in the work-item's fileset. `requests_steps.py` was in the fileset and was not touched; the report says why.

## Removed and weakened tests

None outside the Retires list. I searched the diff for removed `def test_`, step functions, `assert` lines, parametrize cases, `skip` and `xfail`, and features lines.

- `features/requests.feature`: three scenarios were removed. Each is tagged `@deprecated` and listed under the work-item's Retires, and each has a live replacement that stays in the feature:
  - @r4 "outcome writing a line outcome leaves the request's lines as the asker wrote them (deprecated)"
  - @r5 "turn passing a request leaves its line outcomes as they were and writes no resolution (deprecated)"
  - @r12 "a command that changes a request commits the request on the current branch (deprecated)"
- The binding is `tests/scenarios/test_requests.py`. It calls `scenarios("requests.feature")` for the whole file, so no binding needed removing.
- The step definitions those scenarios used are still used by live scenarios, as the plan says. No step was removed, and no `assert` was removed or loosened.

## Allowances

The report's `## Tests changed under an allowance` says "none". No test was changed, so nothing needed an allowance.

## Cannot verify

- The report's red and green runs: 5 failed before; 147 passed and 1 skipped after; the suite at start was 859 passed and 5 failed. As instructed, I did not run the suite. `work run` ran it before it merged.

## Findings

### 1. Observation: `work reply` writes an answer to a question that does not exist, and replaces an earlier answer
- **Work-item:** w177
- **Where:** scripts/workqueue_request.py, `reply` (around line 120), using `_numbered` (line 65).
- **What is wrong:** `reply` checks only the turn.
  - `work reply q1 7 "x"` on a request with one question writes `7. x` under `## Answers`.
  - A second reply to question 1 replaces the first answer, because `_numbered` drops the old entry with that number.
- **Why it matters:** an answer can be written that answers nothing. No line names this case; it is the plan's open case 2, which the implementer left unchosen as the plan said.
- **Fix:** a line that refuses a reply to a question number with no question, written through integrating-a-proposal first. Then a refusal in `reply`.
- **Reproduction:** read from the code rather than run. My shell cannot set up a git repository in scratch.
  - `reply` → `_with_entries(text, "Answers", _numbered(_entries(text, "Answers"), number, answer))`.
  - Nothing reads `Questions` before writing.
- **Triage:** observation.

### 2. Observation: `work ask` accepts a line the request does not have, and question text with newlines
- **Work-item:** w177
- **Where:** scripts/workqueue_request.py, `ask` (around line 110).
- **What is wrong:** `work ask q1 9 "x"` on a two-line request writes `1. line 9: x`. A question containing `\n## Outcomes` would add a section heading inside the request.
- **Why it matters:** this is hardening. No client sends either input today, and these are the plan's open cases 1 and 3, the same as D1 for `outcome`.
- **Fix:** a line refusing a question on a missing line, then the refusal in `ask`.
- **Reproduction:** read from the code. `ask` uses `len(entries) + 1` and `number` as given, with no check against `## Lines`.
- **Triage:** observation.

### 3. Minor: the answer step hardcodes the request and the question number
- **Work-item:** w177
- **Where:** tests/scenarios/requests_write_steps.py, `the_asker_answers` (around line 150): `run("work", "reply", "q1", "1", answer)`.
- **What is wrong:** the step ignores which request and which question "that question" refers to. It holds only because every scenario using it has `q1` with one question.
- **Why it matters:** a later scenario with a second question or another request would answer the wrong one without failing loudly.
- **Fix:** keep the request id and question number in `context` in the Given (`add_sections`) and read them in the When.
- **Triage:** drop (polish).

### 4. Minor: the intake brief still sends questions through the result, not `work ask`
- **Work-item:** w177
- **Where:** scripts/supervise_intake.py:61, which is outside the commits.
- **What is wrong:** the brief tells an intake session to put a question's text in its result's `questions`. `work ask` now exists for that.
- **Why it matters:** this is a supervision line, not one this work-item accepts. The plan names it as open case 5.
- **Fix:** a supervision line through integrating-a-proposal.
- **Triage:** drop for this work-item. It is named so that it is not lost.

### Checked and found sound

- **r16 (refused in the other side's turn):** `ask` refuses when `turn` is `asker`, and `reply` refuses when it is `upstream`. Both raise inside `edit` before `_change` writes or commits anything, the same pattern as `outcome`.
- **r12 (committed):** both writers go through `_change` → `workqueue.committed`.
- **r5 (upstream's part):** `reply` touches only `## Answers`, and `ask` touches only `## Questions`.
- **Code no line asks for:** none.
  - The new-request template now carries empty `## Questions` and `## Answers`. That is the form the capability's Implementation section gives.
  - `model_requests.SECTIONS` already accepts both sections, so `model check` holds.
- **CLAUDE.md:** the module-map row is updated to name `ask` and `reply`.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w177 ready -> claimed$"` → 87424bc6. `work/w177` is not a revision; the branch is gone.
- `git log --format='%H %s' -1 --grep="^work: w177 claimed -> done$"` → 1e8ddfdc
- `git log --stat 87424bc6..1e8ddfdc`, `git diff 87424bc6 db4d07f2`
- grep of `_numbered`, `_entries`, `_with_entries`, `_change` and `field` in scripts/workqueue_request.py. The risk: helpers that write the wrong section or commit before the refusal. Verified that they do not.
- grep of `write_request` and `sections` in tests/scenarios/requests_steps.py. The risk: the Givens adding duplicate `## Questions` headings. Verified: the fixture writes neither section.
- grep of `SECTIONS` in scripts/model_requests.py: Questions and Answers are accepted.
- grep of `question` in scripts/supervise_intake.py (finding 4).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 87424bc6…`:
  - **ruff:** all checks passed.
  - **vulture:** `tests/scenarios/requests_write_steps.py:76 unused variable 'named'`. This was already there before the commits (`git show 87424bc6:tests/scenarios/requests_write_steps.py` has it at line 76) and is not in the diff.
  - **import-linter:** the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output. No file is over the limit.
