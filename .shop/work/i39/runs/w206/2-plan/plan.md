# Plan of w206: fix the findings of branch review 2 of i39

The work-item accepts work-queue r34-r39. It has no Retires section and no Rulings. Its `findings:` field is `.shop/work/i39/runs/branch-review/2/findings.md`, which triages two findings as fix now: finding 1 (`scripts/supervise_change.py`, from w204 of i41) and finding 2 (`turn` in `work list --json`, from w205).

## 1. What goes green

None of the accepted scenarios is red today. At fb9cc6d3 the researcher ran all 7 by node id and all 7 passed (notes §1):

- work-queue#r34, "list prints each initiative, each request and each work-item under .shop/work/ with its status": passes.
- work-queue#r35, "list with --json prints each initiative, request and work-item with its status as one JSON object": passes. Its step `gives_pairs` checks only the name and status pairs. It does not check the scenario's "and nothing besides", so the extra request key `turn` (finding 2, probe p6) goes unseen.
- work-queue#r39, "list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered": passes. A malformed `raised.jsonl` line makes `work list` crash with a traceback (D1 and D2, finding 3). No scenario covers that.
- work-queue#r36, "show of an initiative prints where it stands, for a session to start from": passes.
- work-queue#r37, "show of a work-item prints its status and its open questions": passes.
- work-queue#r38, "show of <target> with --json prints its result as one JSON object" (i1 and w1): passes.

The new unit tests in part 2 are what start red: one for `turn` being absent, and one for the refusal of a malformed record. The implementer sees them red first.

Deprecated scenarios retired: none. The work-item has no Retires section. Work-queue r3, r11, r16, r17 and r18 stay deprecated, still pass, and stay in place.

## 2. Where the change lands

- `scripts/workqueue_list.py`: `listing` stops giving the request's `turn` in the JSON. The reader of `raised.jsonl` in `waiting` refuses a line it cannot read under r7, naming the file and the line number. It catches what fails today: a line that is not JSON, and a line without `request` or `status`. Today these give a traceback (lines 31-32).
- `tests/scripts/test_workqueue_list.py` (new): runs `scripts/work` on a temporary repository.
  - `list --json` with a request: each request object gives the request and its status, and no `turn`.
  - `list` with a `raised.jsonl` line that is not JSON, and with a line that lacks `status`: the exit is an error, the message names `raised.jsonl` and line 1, and no traceback is printed. The findings file sets out this test at line 203.
- Only if the question below is answered B or C: `scripts/supervise_change.py` (`write_proposals`, lines 91-99), and a test in `tests/scripts/test_supervise_change.py`. In that test, a redraft round for p1 whose change list also names p2's capability leaves p2's lists as the answer says.

Removed from the researcher's set, and why:
- `tests/scenarios/work_queue_list_steps.py`: its only item is RUF015, which finding 5 triages as drop. No step changes, because the `turn` check sits in the unit test.
- `scripts/work`, `scripts/workqueue_status.py`, `scripts/migrate_session.py`, `scripts/migrate`, `CLAUDE.md`: these change only when `work status` and the bare `show` are retired (decision 0072). w206 retires nothing (no Retires section), so they stay as they are.
- `scripts/workqueue.py`: it is on the path, but nothing in it changes.

## 3. Decisions

- **D-a: `work list --json` drops `turn` from each request.** This rests on work-queue#r35 ("each initiative, request and work-item with its status"), whose scenario pins "and nothing besides". The text form already omits the turn. No line asks `work list` for the turn (requests#r13 asks it of `work show`). Design-decision/query-commands-answer-in-their-output makes the JSON keys Implementation, so the keys of the request objects stay as they are apart from `turn`. This is finding 2, fix now.
- **D-b: a `raised.jsonl` line `work list` cannot read is refused under work-queue#r7.** The exit is an error, the message names the file and the line, and the command changes nothing, with no traceback. It rests on r7, on the r39 path. The review triaged this as an observation (finding 3) and gave this fix. It goes in because r7 already asks for it, and it is on an accepted line's path.
- **D-c: the branch r36 prints stays the checkout's branch, as it is now** (Q-5 of the notes). The r36 scenario passes as it is, and nothing in w206 changes it.
- **D-d: the old forms stay.** Bare `work show`, `work status` and the SessionStart hook text stay, along with requests r13 and r14 and migration-tools r32 (Q-2 and Q-3 of the notes). w206 has no Retires section, so their retirement belongs to the work-item that retires r3, r11 and r16-r18 under design-decision/work-list-and-work-show-replace-work-status.
- **Finding 1 (`write_proposals`): not taken. See the question.** No accepted requirement of w206 covers it. Supervision#r142 and #r148 are about the proposal being redrafted, and say nothing of what happens to a proposal held for another capability that the change list names. What supervision's narrator sees stored in that proposal's `adds`, `changes` and `removes` depends on the answer.

## 4. Tests the decisions break

None.
- D-a: by search, as the notes report, no step in `tests/scenarios/work_queue_list_steps.py` reads `turn`. The `turn` that `tests/scenarios/test_requests.py` r13 checks comes from bare `work show`, which D-d leaves as it is, not from `work list`.
- D-b: no existing test writes a malformed `raised.jsonl`. The r39 scenario's Given writes a well-formed line, and its result does not change.
- Answer B or C would change `tests/scripts/test_supervise_change.py` or the supervision steps. Whether any of them asserts the in-place rewrite of another proposal has to be checked once the answer is given. That check is not yet done.

## 5. Open cases

- The exact wording of the refusal for a malformed record, beyond naming `raised.jsonl` and the line number.
- Whether a well-formed JSON line missing `upstream` or `initiative` is also refused, or is read with what it has.
- Whether a blank line in `raised.jsonl` is skipped or refused.
- `list --json` does not carry r39's waiting (O3). The lines leave this open, and w206 leaves it as it is.
- A work-item with no `kind` gives the refusal "is a None" (O2). This is not in scope. It is left for the implementer to name, not fix.
