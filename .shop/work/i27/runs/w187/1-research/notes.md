# Research of w187 (fix the findings of branch review 8; accepts supervision r91-r97, r66)

Search: no map (`tools tests-of` says "no map"); counts by `tools refs` where it resolves a name, else by search (grep). `refs` does not follow `self.method` calls, so `write_proposals`, `show`, `round` are by search.
Probe scratch: `.shop/scratch/w187-1-research/` (probe_changes.py, probe_show.py). Git status at start: clean (HEAD 4df0a60b).

## 1. Why each scenario is red today

None is red. Command, run: `python3 -m pytest -q -p no:cacheprovider --tb=short -rfE <10 node ids of tests/scenarios/test_supervision.py>` → `10 passed in 9.94s`. Ids: the nine accepted scenarios, the outline giving two (`[gives DONE with a change list naming thing]`, `[ends at its turn limit]`), plus the branch-review scenario (`test_an_initiative_with_no_workitem_gets_no_branch_review_...`).

- r66 (no initiative, side by side): `test_work_run_started_with_no_initiative_takes_every_...` passes. Code: supervise_all.py:63-72 (threads), :44-46 (shared `rounds` Lock).
- r95 (rounds one at a time): `test_..._runs_the_integrate_apply_and_formulate_rounds_..._one_at_a_time` passes. Code: supervise_rounds.py:15, :55-61 (`round` takes `round_lock` for SERIAL kinds). Flaky at review 8 (findings F11: failed once in a loaded full run, passed alone and in a second run). Not reproduced here; I ran it once only.
- r97 (no measure without work-item): `test_an_initiative_with_no_workitem_is_not_measured` passes. Code: supervise.py:207 (`if self.items() and all(...)`).
- r94 (no branch review without work-item): `test_an_initiative_with_no_workitem_gets_no_branch_review_...` passes. Code: supervise.py:207 gate; supervise_review.py:39 (`unread()`).
- r93 (started, neither proposal nor item → integrate): `test_a_started_initiative_with_neither_...` passes. Code: supervise_rounds.py:35-41 (`due`).
- r96 (integrate DONE without change list → error): `test_an_integrate_round_that_ends_done_without_a_change_list_...` passes. Code: supervise_rounds.py:96-102, :115-116 (`refuse_integrate`).
- r91 (drafts kept, both endings): both outline examples pass. Code: supervise_rounds.py:90-94 (non-DONE → `keep_round`), :106-109 (commit of `runs/<name>/<label>` with the proposals).
- r92 (one proposal per capability): `test_an_integrate_rounds_change_list_...` and `test_the_change_lists_of_two_initiatives_..._different_ids` pass. Code: supervise_change.py:13-32 (`entries`), :38-52 (`write_proposals`).

## 2. What the system answers today

Scenario Givens and Whens: run as in part 1, all pass.

Probe A. Command: `python3 -m pytest -q -s -n0 .shop/scratch/w187-1-research/probe_changes.py -p no:cacheprovider`. Calls `supervise_change.entries` and `Changes.write_proposals` directly on a scratch initiative (not through `work run`). Run.
- Two entries for one capability, `[{capability: thing, adds:[thing#r4]}, {capability: thing, changes:[thing#r2]}]`: `entries` gives both; `write_proposals` returns two paths, both `thing.md`; the file holds only `changes: [thing#r2]`, `adds: []`. thing#r4 is lost.
- Capability `sub/x`: `FileNotFoundError: .../slash/sub/x.md`. A traceback, not r107's error.
- Capability `../escaped`: written as `<scratch>/escaped.md`, outside the initiative directory (`inside initiative dir: [False]`).
- Change-list forms: `changes` None or `[]` or missing → `[]` (r96 path); `changes` a dict → BadChanges; entry with no capability or blank capability → BadChanges; `adds` a string, or `[""]` → BadChanges; `[{capability: thing}]` alone → one entry with all three lists empty (accepted as a change list; see D3 note in part 6).

Probe B. Command: `python3 -m pytest -q -s -n0 .shop/scratch/w187-1-research/probe_show.py -p no:cacheprovider`. Calls `supervise.Run.show` on a scratch initiative `started`, with no work-item and one proposal p1. Run.
- proposal `awaiting-answer` with a question: `items: []`, `proposals: [('p1','awaiting-answer')]`, `show() returns: 0`.
- proposal `drafted`: `show() returns: 0`.
- The no-initiative path (supervise_all.py:77-82) counts proposals in `nodes`, so its exit is 3 for the same state (read, not run).

Nearest cases not run (read): integrate round with `started` status and an unreadable request → `due()` swallows the Refused and gives no round, no error (supervise_rounds.py:37-41); r93 only covers the `proposed` form in the scenarios.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise.py:231 `Run.show` | exit 0 when `all(...)` over the work-item list, which is true for an empty list | r97/r94: no work-item is not done; with a proposal awaiting-answer and no work-item, `work run i1` exits 0 (probe B) | `test_an_initiative_with_no_workitem_is_not_measured` (runs `work run i1`, by search) | by search (`show` is a method) |
| supervise_all.py:77-82 vs supervise.py:231 | the no-initiative path counts proposals in its exit code; the single-initiative path counts work-items only | the same initiative gives exit 3 under `work run` and 0 under `work run i1` | none | by search |
| supervise_change.py:44-52 `write_proposals` | one file per entry, path `dir/<capability>.md`, no merge of entries with one capability | r92: one drafted proposal per capability, with what it adds, changes and removes | none (no test has two entries for one capability) | by search |
| supervise_change.py:45 | capability name used as a file name, no check | r92/r107 (r107 not accepted): name becomes a path | none | by search |
| supervise_rounds.py:104-109 (integrate branch) | writes proposals and commits without `move` (supervise.py:111-118), so no lifecycle check and no log line for the new files | r91/r92: proposals written from the change list | `test_an_integrate_rounds_change_list_...`, `test_the_drafts_of_an_integrate_round_...` (both pass) | by search (`move` has 4 refs, `tools refs`) |
| supervise_rounds.py:35-36 `due` | `started` with no proposal and no work-item gives an integrate round | r93: the new form; `proposed` is the old | `test_a_started_initiative_with_neither_...` | by search |

Checked and sound (no old assumption left): workqueue_done.py:31 (`if not statuses or any(...)`), supervise.py:207 (`self.items() and all(...)`).

## 4. Tests the requirements make impossible to keep

None. No map, so by search: the accepted requirements add behaviour; the nine accepted tests pass (part 1). Searched tests/scenarios for `write_proposals`, `supervise_change`, `BadChanges`, `.show(` and "two entries" / "same capability" on `supervis*` files: no match. The weakened test `supervision_rounds_steps.py second_not_refused` (findings, w164) is not on an accepted requirement's path; not run here.

## 5. A step the work-item skips

The step the integrate path leaves out is `workqueue.move` (workqueue.py:142-166), which the existing transitions go through. The integrate round's own start, `start_initiative` (supervise_rounds.py:118-123), calls `workqueue_done.mark` (workqueue_done.py:51-56) and a log line, not `move`.
Effects `move` alone produces (read of workqueue.py:142-166): it refuses a status that is no lifecycle status (`STATUSES`, `PROPOSAL_STATUSES`); it refuses a file with no status; it writes the file, then appends the log line, and puts the file back when the append fails (r7).
Effects `mark` alone produces (read of workqueue_done.py:51-56): none checked; it rewrites the `status:` line with no check of the transition.
Consequence (read): the integrate branch's proposal files (supervise_change.py:44-52) are written with no `move`, so none of `move`'s checks, and no log line for each new proposal. Not probed.

## 6. Defects

Each reproduced by probe A or B, on today's code; not fixed; no judgement of the plan.

D1 Two entries for one capability lose one. Repro: probe A, first test. Came back: `written: ['thing.md', 'thing.md']`; thing.md holds `adds: []` and `changes: [thing#r2]` only.
D2 A capability name with `/` crashes the round. Repro: probe A, second test. Came back: `FileNotFoundError ... sub/x.md`.
D3 A capability name with `..` writes outside the initiative directory. Repro: probe A, third test. Came back: written to `<scratch>/escaped.md`, `inside initiative dir: [False]`. In the checkout the same path is `.shop/work/escaped.md`. Related, read: a change-list entry with only `capability` gives an empty proposal, not the r96 error.
D4 Exit 0 for an initiative with no work-item and an open question on its proposal. Repro: probe B, first test. Came back: `items: []`, `show() returns: 0`, with p1 `awaiting-answer` and "Is it kept?" open. The no-initiative run gives 3 for the same state (read).
D5 (read, F11 of the findings) r95 scenario flaky under load. Not reproduced: one run alone passed. The lock (supervise_all.py:44, supervise_rounds.py:60) covers every SERIAL round (only call site: supervise_rounds.py:59-61), so the lock reading does not explain an overlap; the stand-in's `linger: 1` (supervision_all_steps.py:104) is the likelier cause. Read.

## 7. The file set

Must change for the accepted scenarios: none; they pass today (part 1).

Must change for the findings this work fixes (the plan decides which; from D1-D4 and F11):
- scripts/supervise_change.py (52 lines, room 248): merge entries of one capability (D1), refuse a bad capability name (D2, D3). Found by probe A.
- scripts/supervise.py (260 lines, room 40): `show` exit for no work-item (D4). Found by probe B. Room is small: a change here may need a split.
- scripts/supervise_all.py (83, room 217): only if F11 proves the lock is incomplete (read: not shown). Found by read.
- scripts/supervise_rounds.py (134, room 166): only if the integrate path changes for D1-D3 or the move gap (part 5). Found by read.
- tests/scenarios/supervision_all_steps.py (177, room 123): `linger` margin for F11, and F2's ruff lines `:111`, `:127` (findings F2). Found by read of findings file.
- tests/scenarios/supervision_integrate_steps.py (190, room 110): steps for D1-D3 scenarios, if added. Found by read.
- features/supervision.feature: new scenarios for D1-D4, if the plan adds them (not Python; no size limit).
- CLAUDE.md (44 lines, not Python, no limit): module-map row `scripts/supervise*.py` is stale (findings "Shape"). Found by read of findings file.
- scripts/supervise_rounds.py:1-3 docstring is stale (findings). Found by read of findings file.

Modules on the change path, edited or not (wc -l; room under 300):
- scripts/supervise.py 260 (room 40)
- scripts/supervise_rounds.py 134 (room 166)
- scripts/supervise_change.py 52 (room 248)
- scripts/supervise_all.py 83 (room 217)
- scripts/supervise_review.py 82 (room 218)
- scripts/supervise_analysis.py 74 (room 226)
- scripts/supervise_worker.py 251 (room 49), read for SCRIPTS and session only
- tests/scenarios/test_supervision.py 259 (room 41)
- `tools size --limit 300` printed nothing: no tracked Python file is over the limit.
