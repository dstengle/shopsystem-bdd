# w137 report

## Budget
scripts/supervise_rounds.py (new), scripts/supervise.py, scripts/workqueue.py, scripts/supervise_brief.py,
scripts/supervise_worker.py, CLAUDE.md, tests/scenarios/supervision_rounds_steps.py (new), tests/scenarios/test_supervision.py.
(8 files.) The plan's "supervision_proposal_steps.py (new)" already exists with other steps, so the new steps went in
`supervision_rounds_steps.py`. supervision_world.py, stub_claude.py, supervise_merge.py and supervise_faults.py were not changed.

## Outside the file set
None. (supervise_rounds.py and supervision_rounds_steps.py are new modules, the first with its CLAUDE.md row.)

## What changed
- `supervise_rounds.py`: `Rounds` mixin. An awaiting-answer proposal with as many answers as questions (none included) gets an
  apply round; an approved one a formulate round. A round is a worker of `initiative-round` on a branch `round/<p>-<k>-<kind>`;
  when it ends its branch is merged into the initiative branch and deleted, then the proposal is moved (approved/formulated)
  and committed through `Run.move`. A fault (cut short, no/invalid result, push check, git failure) keeps the proposal's
  status, commits the stage directory and log lines with no transition, and ends `work run` with a Refused error naming the
  round and fault (exit 1).
- `supervise.py`: `Run` includes `Rounds`; `run()` calls `self.rounds()` before drafting.
- `workqueue.py`: `move` accepts `approved` and `formulated` for a capability-proposal only.
- `supervise_worker.py`: `ROUNDS`, tools for apply/formulate, role name; a round's pytest gets no `--work-item`.
- `supervise_brief.py`: a round's brief says `Capability-proposal:` and `Job:`, no work-item branch; answers via `answer_lines`.
- Tests: new step module for the four scenarios.

## Red and green
- Suite at start (brief): 782 passed, 4 failed (the four w137 scenarios among those expected/failing).
- Red: `python3 -m pytest -q -n 0 --work-item w137` after writing the steps only: 4 failed, 142 passed. The failing Then
  was `position(...)`'s assertion on log.jsonl, e.g. "AssertionError: ([{... 'stage': 'branch-review' ...}], '')" — no round
  started, so no apply/approved lines. Expected: the code did not exist.
- Green: `python3 -m pytest -q --work-item w137`: 146 passed, 1 skipped, 56 subtests passed.
- Touched modules: `python3 -m pytest -q -p work_items --whole-suite --work-item w137 tests/scenarios/test_supervision.py
  tests/scenarios/test_work_queue.py tests/scripts`: 315 passed, 1 skipped, 20 xfailed, 23 xpassed, no failures.

## Tests changed under an allowance
none

## Open questions
- `work run`'s output and exit when the initiative holds only a proposal and no work-item (r9 speaks of work-items); today
  the branch review runs over the empty set of work-items, as the red run's log showed.
- A round result giving questions or an outcome other than DONE: the transition still happens (plan decision 4).
- A merge of a round's branch that conflicts: treated as a round fault (merge aborted, proposal unchanged); no line says so.
- A round branch left behind by a faulted round when the next run starts the same round again (new `<k>`, new branch).
- A round that changes files under .shop/work/ in its branch: not put back, unlike an implementer's (r6).
- Round turn limit: none set.
- D3 (work answer returns the proposal to drafted) is not touched.

## Plan contained code?
No code in the plan; nothing pasted.

## Completeness check
`python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing: no file over the limit.

## Now possible
`work run i1` takes an awaiting-answer proposal whose answers are given through apply (merged, approved) and formulate
(merged, formulated) in one run.

Surprise: the real `initiative-round` agent wants drafts in git-ignored scratch, which a round's worktree lacks (plan open case).

Commit: 6a37039 work run: apply then formulate rounds for an answered capability-proposal.

Files changed: the 8 above. Concerns: the open questions above.
