# Plan of w207: fix the findings of branch review 3 of i39

w207 accepts work-queue#r34-r39. Its title and its `findings:` field name `.shop/work/i39/runs/branch-review/3/findings.md`. `work run` drafts a work-item like this from a branch review's fix-now findings (`supervise_draft.py`). The scope is therefore those fix-now findings, 1 and 2, kept green against r34-r39. w207 has no `Retires` section and no `## Rulings`.

## 1. What goes green

All seven accepted scenarios pass today: the researcher ran each by node id, `1 passed` each (notes §1). None is red, and none goes red from this plan.
- r34: "list prints each initiative, each request and each work-item under .shop/work with its status"
- r35: "list with --json prints each initiative, request and work-item with its status as one JSON object"
- r39: "list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered"
- r36: "show of an initiative prints where it stands, for a session to start from"
- r37: "show of a work-item prints its status and its open questions"
- r38: "show of <target> with --json prints its result as one JSON object" (outline rows i1 and w1)

Deprecated scenarios retired: none. w207 has no `Retires` section. The deprecated work-queue r3, r11, r16, r17 and r18 scenarios stay as they are.

What this work makes true, with no scenario for it (unit tests only):
- **Branch review finding 2:** a round merging into another held capability-proposal no longer repoints that proposal's drafts.
- **D1:** `work show <initiative>` refuses a ledger it cannot decode, giving a reason and no traceback.
- **D3:** a work-item file with no `kind` is refused with a reason that says what is missing.

## 2. Where the change lands

- `scripts/supervise_change.py` (added to the researcher's set, for finding 2): in `write_proposals`, the replacement or appending of "The drafts of this proposal are in …" runs only on the own-proposal path (`held.stem == own`). On the merge path, the held proposal's drafts sentence is left as it was.
- `tests/scripts/test_supervise_change.py` (added, for finding 2): one new test, the one branch review 3 asks to keep. A held proposal p2 with drafts `old/`, then `write_proposals` started for p1 with an entry for p2's capability: p2 still says its drafts are in `old/`.
- `scripts/workqueue_status.py` (D1): `ledger` reads the ledger under a refusal (`Refused`, as `workqueue.read` does) that names the file when it is not UTF-8.
- `scripts/workqueue_list.py` (D3): `work_item`'s refusal of a file whose `kind` is missing says that the file has no kind, not "is a None".
- `tests/scripts/test_workqueue_list.py` (D1, D3): one test for each refusal: exit status 1, the reason, and no traceback.

Removed from the researcher's set: `tests/scenarios/work_queue_list_steps.py`. Its only reason to be in the set was D2 (`gives_pairs` checking every key), and D2 is not taken here (§5).

Not touched:
- `scripts/work`, `scripts/workqueue.py` (6 lines of room), `scripts/migrate_session.py`
- the retired `work status` path and the no-target `work show`
- `features/`

## 3. Decisions

1. **Branch review finding 1: keep the merge as it is, with no code change.** This is already ruled: the ledger of 2026-10-27 reads "w206 branch review finding 1: reading B (union of the round's ids into another capability's proposal); a supervision line for it goes into the follow-up request". The finding's own fix offers this: "confirm that i39 closes with this line carried by q20". Observations F3 (an id in both `adds` and `removes`) and F4 (a first integrate round also merges) depend on that line, so they stay unfixed.
2. **Branch review finding 2: on the merge path, the other proposal's drafts sentence is left unchanged.** This rests on supervision#r108: a gate or apply round gets the kept drafts of the integrate round "that wrote the proposal". A round started for p1 wrote p1. Into p2 it only merged ids, and it was briefed without p2's earlier drafts, so its drafts are not p2's.
   - It also rests on supervision#r142: a proposal drafted anew keeps its earlier drafts "in their round's directory".
   - The own-proposal path is unchanged (r142, r148): it rewrites the lists and repoints the drafts.
   - The other fix the reviewer offers is a second drafts sentence that `supervise_brief.py` would read. It is not taken: the reviewer says it "needs a line in q20".
3. **D1: an undecodable ledger is refused.** This rests on work-queue#r7: a command that cannot do what it was asked exits with an error and says why. Here that is `work show <initiative>`, on the path of the accepted r36. The refusal names the ledger file, as the r7 refusal of a non-UTF-8 work-item file already does.
4. **D3: a work-item file with no `kind` is refused, saying it has no kind.** This rests on work-queue#r7 ("say why"), on the path of the accepted r37. The command is refused today too; only the wording changes, so no outcome changes.

## 4. Tests the decisions break

None. What I verified:
- **Decision 2:** `tests/scripts/test_supervise_change.py::test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal` asserts only p1's `adds`, p2's `adds`, `removes` and `status`. It never asserts p2's drafts sentence (read), so it stays valid. The other test there, `test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids`, writes no held proposal, so the merge path is not reached.
- **Decisions 3 and 4:** by the notes (§4), no test asserts the traceback of a non-UTF-8 ledger or the text "is a None". The r7 scenario at `features/work-queue.feature:268` uses work-item files, not a ledger, and stays as it is.
- **Decision 1:** changes no code.

## 5. Open cases

- **Finding 2:** the round's drafts of p2's capability hold the merged ids, but p2's apply round still reads p2's own drafts. Its `rewrite_lists` (r145) can then drop those ids on apply. That is for the q20 line, which this plan does not choose. The implementer names it in the report.
- **D1:** whether `show <initiative> --json` refuses in the same way as the text form. The implementer names what comes back.
- **D3:** the wording when `kind` is present but empty, as opposed to missing.
- **Not taken here:**
  - **D2** (O3): whether `work list --json` carries r39's waiting. r35 and r39 do not settle it, and it changes what the narrator observes. It is not a fix-now finding, so it is left for the follow-up request that carries r40 and r48.
  - **Retirement:** the retirement of `work status` and the no-target `work show` (decision 0072). This would mean replacing requests r13 and r14 and migration-tools r32, and rewriting the r7 scenario at `features/work-queue.feature:268`. No accepted requirement or `Retires` section of w207 asks for it.
