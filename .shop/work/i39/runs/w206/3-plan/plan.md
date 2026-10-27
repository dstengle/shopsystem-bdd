# Plan of w206: fix the findings of branch review 2 of i39

The work-item accepts work-queue r34-r39. It has no Retires section and no Rulings. Its `findings:` field is `.shop/work/i39/runs/branch-review/2/findings.md`, which marks two findings as fix now: finding 1 (`write_proposals` in `scripts/supervise_change.py`) and finding 2 (`turn` in `work list --json`). The question from plan stage 2 about finding 1 has an answer (work-item `## Answers`, 2026-10-27): **reading B**. The round's ids are merged (as a union) into the other proposal's adds, changes and removes. This plan is the plan from stage 2 with that answer added.

## 1. What goes green

None of the accepted scenarios is red today. At fb9cc6d3 the researcher ran all 7 by node id, and all 7 passed (notes §1):

- work-queue#r34, "list prints each initiative, each request and each work-item under .shop/work/ with its status": passes.
- work-queue#r35, "list with --json prints each initiative, request and work-item with its status as one JSON object": passes. Its step `gives_pairs` checks only the name/status pairs. It does not check "and nothing besides", so the extra request key `turn` goes unseen (finding 2, probe p6).
- work-queue#r39, "list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered": passes. A malformed `raised.jsonl` line still crashes `work list` with a traceback (notes D1 and D2, finding 3), and no scenario covers that.
- work-queue#r36, "show of an initiative prints where it stands, for a session to start from": passes.
- work-queue#r37, "show of a work-item prints its status and its open questions": passes.
- work-queue#r38, "show of <target> with --json prints its result as one JSON object" (i1 and w1): passes.

The tests that start red are the new or added unit tests in part 2:
- one for `turn` being absent from `list --json`;
- one for the refusal of a malformed `raised.jsonl` record;
- one for a redraft round leaving another proposal's applied ids in its lists. This one is red today: `rewrite_lists` replaces those lists, as observation 2026-10-27-redraft-overwrites-other-proposal and commit 2862e7bf show.

The implementer sees each of them red first.

Deprecated scenarios retired: none. Work-queue r3, r11, r16, r17 and r18 stay deprecated, still pass, and stay in place.

## 2. Where the change lands

- `scripts/workqueue_list.py` (78 lines):
  - `listing` stops putting the request's `turn` in the JSON.
  - The reader of `raised.jsonl` in `waiting` refuses a line it cannot read, under r7, naming the file and the line number. This covers a line that is not JSON and a line without `request` or `status`. Both give a traceback today (lines 31-32).
- `tests/scripts/test_workqueue_list.py` (new): runs `scripts/work` on a temporary repository.
  - `list --json` with a request: each request object gives the request and its status, and no `turn`.
  - `list` with a `raised.jsonl` line that is not JSON, and `list` with a line that lacks `status`: each exits with an error, with a message naming `raised.jsonl` and line 1, and no traceback. The findings file sets this test out at line 203.
- `scripts/supervise_change.py` (107 lines), added by the answer to finding 1:
  - `write_proposals` is told which proposal the round was started for.
  - A held proposal for a capability the change list names is handled as follows:
    - If it is that round's own proposal, it is rewritten in place as now: its lists are replaced, and so is its drafts path.
    - If it is any other held proposal, the round's ids for its capability are merged into its `adds`, `changes` and `removes`. Its own ids stay, in their order, and each id of the round that it lacks is appended after them. Its drafts sentence and status are handled as in D-f.
  - `rewrite_lists` (also used by the apply round, `supervise_rounds.py:168`, under r114) keeps its replacing behaviour. The merge is a separate path, or an option of it.
- `scripts/supervise_rounds.py` (229 lines), added because the caller at line 195 must pass the round's proposal name (`name`) to `write_proposals`. `write_proposals` cannot tell that name from the change list itself. Only that call changes.
- `tests/scripts/test_supervise_change.py` (27 lines), added by the answer to finding 1:
  - New test: an initiative holds proposal p2 for capability `other`, with applied adds and removes. A round started for p1 (a proposal for `thing`) gives a change list that adds ids on `thing` and on `other`. After it, p2's lists hold its earlier ids and the round's `other` ids, and p1's lists are exactly the round's `thing` ids.
  - The existing test's helper `write` calls `write_proposals` with no proposal name. It is adjusted only as far as the new parameter needs (part 4).

Removed from the researcher's set, and why:
- `tests/scenarios/work_queue_list_steps.py`: its only item is RUF015, which finding 5 marks as drop. The `turn` check sits in the unit test.
- `scripts/work`, `scripts/workqueue_status.py`, `scripts/migrate_session.py`, `scripts/migrate`, `CLAUDE.md`: these change only when `work status` and the bare `show` are retired (decision work-list-and-work-show-replace-work-status). w206 has no Retires section, so it retires none of them. The module-map row of `scripts/supervise_change.py` still fits the change.
- `scripts/workqueue.py`: it is on the path, but nothing in it changes.

## 3. Decisions

- **D-a: `work list --json` drops `turn` from each request.**
  - Rests on work-queue#r35 ("each initiative, request and work-item with its status"), whose scenario pins "and nothing besides".
  - The text form already leaves the turn out. No line asks `work list` for the turn; requests#r13 asks it only of `work show`.
  - Under design-decision/query-commands-answer-in-their-output, the other keys stay as they are.
  - This is finding 2.
- **D-b: a `raised.jsonl` line that `work list` cannot read is refused under work-queue#r7.**
  - The command exits with an error, its message names the file and the line, it changes nothing, and it prints no traceback.
  - Rests on r7, on r39's path. This is finding 3.
- **D-c: the branch that r36 prints stays the checkout's branch** (notes Q-5). The r36 scenario passes as it is.
- **D-d: the old forms stay.** Bare `work show`, `work status`, the SessionStart hook text, requests r13/r14 and migration-tools r32 all stay as they are (notes Q-2, Q-3). w206 has no Retires section. Their retirement belongs to the work-item that retires r3, r11 and r16-r18 under design-decision/work-list-and-work-show-replace-work-status.
- **D-e: a redraft integrate round merges its ids into another held proposal's lists, as a union** (finding 1).
  - Rests on the answer of 2026-10-27 in the work-item: reading B, "as the coordinator restored i39-requests by hand". It is bounded by supervision#r142 and #r148, which rewrite in place only the proposal being drafted anew.
  - "Another" means any held proposal other than the one the round was started for. When the round is the initiative's own first integrate round (`name` is the initiative), every held proposal is another, so it is merged into and never replaced.
  - The round's own proposal keeps today's in-place rewrite (r148). No second proposal is written for a capability that already has one, so supervision#r92's scenarios keep their meaning for a capability with no held proposal.
- **D-f: the other proposal's drafts sentence and status.**
  - Its status is left as it is: only the round's own proposal moves (r142, `supervise_rounds.py:196-197`).
  - Its drafts sentence ("The drafts of this proposal are in …") is replaced by the round's kept drafts path, as today.
  - Rests on the answer's "as the coordinator restored": the restored `.shop/work/i39/requests.md` holds the union of the lists and the new round's drafts path (`.shop/work/i39/runs/work-queue/5-integrate/drafts/round-1/`). That round's drafts hold the capability's file with the round's ids. This is not a new behaviour for the narrator to observe: the lists are the only thing D-e changes.

## 4. Tests the decisions break

None is broken in what it asserts.
- D-a: no step in `tests/scenarios/work_queue_list_steps.py` reads `turn` (notes §4, by search). The `turn` that `test_requests.py` r13 checks comes from bare `work show`, which D-d leaves as it is.
- D-b: no existing test writes a malformed `raised.jsonl`. The r39 scenario's Given writes a well-formed line.
- D-e and D-f:
  - `tests/scripts/test_supervise_change.py::test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids` holds no earlier proposal, so its assertions stand. Only its helper's call to `write_proposals` gains the round's proposal name if the new parameter is required. It is the initiative's name, as in a first integrate round. What it asserts is unchanged.
  - The supervision scenarios @r92 (two), @r142 and @r148 (read in `features/supervision.feature`) each hold at most one proposal, the round's own, or none. None asserts that another proposal's lists are replaced, so each keeps its result.
  - The researcher did not cover `tests/scenarios/supervision_reintegrate_steps.py` and `supervision_integrate_steps.py`. Their asserts are reached only by those scenarios. The implementer confirms them by running the supervision scenarios after the change.

## 5. Open cases

- The exact wording of the refusal for a malformed record, beyond naming `raised.jsonl` and the line number.
- A well-formed JSON line in `raised.jsonl` that lacks `upstream` or `initiative`: refused, or read with what it has.
- A blank line in `raised.jsonl`: skipped or refused.
- `list --json` does not carry r39's waiting (finding O3). The lines leave this open, and w206 leaves it as it is.
- A work-item with no `kind` gives the refusal "is a None" (O2). This is outside scope.
- Under D-e, an id the round lists in one field that the other proposal holds in another field: for example, a round that removes `x#r3` where the proposal adds `x#r3`. Should both lists keep it, or should one win?
- Under D-e, an apply round of the other proposal applies its earlier ids from its earlier drafts. Its drafts path now names the new round's directory (D-f). Whether that round's draft of the capability holds every earlier id is a matter for the drafting round, not for `write_proposals`.
- The ruff B023 at `scripts/supervise_change.py:96` (a lambda in the loop) sits in the code D-e touches. Whether to clear it while there is left to the implementer.
