# Review of w146: work run starts a proposal's gate round and writes the questions its result gives

**Verdict: DONE_WITH_CONCERNS.** The change does what r68 and r85 ask, and both scenarios pass. No test was removed or weakened, and nothing under `features/` changed. One Important finding is triaged fix now. A gate round whose result is not `DONE` (for example `BLOCKED` with no questions) still moves the proposal to `awaiting-answer`. If that result gives no questions, `due()` then starts apply and formulate at once, so the person never sees the gate.

## Commits reviewed

The branch `work/w146` is gone. The commits are those between `aa4ada2 work: w146 ready -> claimed` and `db142c6 work: w146 claimed -> done` on HEAD, less the `work:` commits and w148's commits (`fd180a0`, w148's own `work:` commits):

- `bbca36c` work run starts a drafted proposal's gate round and writes its result's questions under ## Questions. It touches `scripts/supervise.py`, `scripts/supervise_brief.py`, `scripts/supervise_rounds.py`, `scripts/supervise_worker.py` and `tests/scenarios/supervision_rounds_steps.py` (+59 −5). All five are in the work-item's fileset.

The implementer's result names `c71999a`, which has the same subject and the same five-file change. `git diff c71999a bbca36c -- scripts tests` shows only w148's files (`workqueue_request.py`, `test_work_queue.py`, `work_queue_request_steps.py`). So `bbca36c` is `c71999a` rebased onto w148 at merge. They are the same commit, and this is not a finding.

## Removed and weakened tests

None. I searched the diff for deleted `def test_`/step functions, removed `assert` lines, changes to parametrize lists, and `skip`/`xfail`. The only test file in the diff, `tests/scenarios/supervision_rounds_steps.py`, gains 49 lines and loses none. The change to `move()` in `scripts/supervise.py` keeps one-question callers as they were: `outcome()` (supervise_worker.py:235-242) never returns an empty string, so `if question:` and the new loop behave the same for them.

## Allowances

The report's `## Tests changed under an allowance` says "none". The diff agrees: no existing test changed.

## Cannot verify

- The report's run counts: "144 passed, 1 skipped" for `--work-item w146`, and "798 passed, 2 failed" for the suite at start. I did not run the whole suite, by rule. I ran the two w146 scenarios: 2 passed.
- Whether the real `initiative-round` agent, given the new brief line, returns its questions as the strings r68 asks for. This is agent behaviour; the scenario uses a stand-in.

## Findings

### F1. Important, fix now (w146): a gate round that does not end `DONE` still moves the proposal to `awaiting-answer`, and with no questions the proposal goes through apply and formulate without the person's gate

- **Where:** `scripts/supervise_rounds.py:64-65` (`round()`), together with `due()` at lines 27-34.
- **What is wrong:** `round()` never reads the result's `status`. Only a Fault (session or result-file problem) keeps the proposal's status. A gate result such as `{"status": "BLOCKED", "summary": "..."}` therefore moves the proposal `drafted -> awaiting-answer` with zero questions. `due()` then counts Answers (0) ≥ Questions (0) and starts the apply round at once. Apply ignores its own status the same way, which already happened before this change, so the proposal moves on to `approved` and then `formulated`. Its work-items are then drafted.
  - The client sends `BLOCKED` today: `agents/initiative-round.md` lines 47 and 55 (the drafts of an earlier round missing, a dispatch with no reply twice).
  - The implementer's report confirms the first half ("A non-DONE gate result still moves to awaiting-answer").
  - The researcher's probe_zero (notes §6 D1, run) shows the second half: an `awaiting-answer` proposal with no questions went `-> approved -> formulated` in one `work run`.
  - I verified the chain by reading `round()`, `due()` and `worker()` (supervise_worker.py:201-206). I did not run it end to end with a `BLOCKED` stand-in.
- **Why it matters:** the gate is the person's decision on the proposal. The capability's Purpose says `work run` "takes no judgment; what nobody may decide goes to the person as a question". Here a gate that could not be given ends with the proposal applied to `spec/` and formulated without anything being put to the person. That is a wrong answer.
- **Fix:** a line first, through integrating-a-proposal, since no Behaviour line settles a round's non-`DONE` outcome; r69 says only "when the gate round ends". For example: "If a round's result gives an outcome other than `DONE`, `work run` shall keep the proposal's status and put the result's questions, or its outcome and summary, to the person." Then make `round()` refuse, or ask, rather than move. A narrower interim fix: treat a gate result that is not `DONE` like a fault (keep the status, keep the round).

### F2. Minor, observation (w146): a `DONE` gate result with no questions also skips straight to apply

- **Where:** the same code as F1.
- **What happens:** the plan named this open case in §5, and the report names it too. In the r68 scenario itself, "every round ends" gives `DONE` with no questions, so apply and formulate follow the gate.
- **Reproduction:** researcher's `probe_zero` (notes §6 D1): `EXIT 3`, round directories `1-apply` and `2-formulate`, `p1` ending `status: formulated`.
- No line asks for a refusal here, and a gate that has nothing to decide may arguably pass. Whoever writes F1's line should settle this case too.

### F3. Minor, drop (w146): an empty-string question from a gate is written as an empty bullet `- ` under `## Questions`

- **Where:** `scripts/supervise_rounds.py:64` and `scripts/supervise.py:109-110`.
- That empty bullet then counts toward `due()`'s question count, so the proposal needs an answer to a question nobody asked. Found by reading; no client sends `""` today.

## Commands and probes

- `git log --format=%H -1 --grep="^work: w146 ready -> claimed$" work/w146`: fatal, the branch is gone. I used `git log --grep="^work: w146 "` on HEAD instead: claim `aa4ada2`, done `db142c6`.
- `git log --format='%h %s' aa4ada2..db142c6`, `git show bbca36c`, `git show --stat c71999a`, `git diff c71999a bbca36c --stat -- scripts tests`.
- `python3 -m pytest -q -k "drafted_capabilityproposal_is_given_to_a_gate_round or gate_round_work_run_started_for_a_capabilityproposal_ends" tests/scenarios/test_supervision.py`: 2 passed.
- `grep -n -i -E "recommended|readings" scripts/supervise*.py`: the words appear only in the new gate brief line. This verified the risk that the brief-ask Then would pass on the generic brief: it would not, so the Then tells the two apart.
- `grep -rn -E "\.move\(|question=" scripts/supervise*.py`, plus a read of `outcome()`. This verified the risk that the new `move()` loop would change one-question callers: it does not.
- `grep -n -i -E "status|BLOCKED|gate" agents/initiative-round.md`: the agent replies `BLOCKED` in named cases (for F1).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base aa4ada2df20e2140b41321b1bd954acb7009a197`:
  - **ruff:** one error, `tests/scenarios/test_work_queue.py:7:1 I001`. That file was last changed by w148's `fd180a0`, not w146's commit.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over 300 lines.
