# Plan of w163 (accepts supervision#r79, supervision#r84)

Finding: branch review 3's R3-F1 (`runs/branch-review/3/findings.md`). An integrate round that ends DONE leaves its stage directory `.shop/work/<init>/runs/<init>/<k>-integrate/` uncommitted, so the next `work run` is refused under r46.

## 1. What goes green

The four accepted scenarios all pass on base f890f2f today (notes §1: `4 passed`):
- r79 `features/supervision.feature:849` "a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils": green, stays green.
- r79 `:857` "a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind": green, stays green.
- r79 `:870` "a proposed initiative whose fulfils names a request the queue does not hold …": green, stays green.
- r84 `:1056` "when `work run` starts the integrate round of a proposed initiative, the initiative is started": green, stays green.

The failing case is the scenario the findings file gives as a keep-as-test, tagged @r84: "an integrate round that ends leaves nothing uncommitted and blocks no later `work run`". Its steps are: a Given of q1 with lines 1 and 3 accepted, every round ends, `work run i1`, then i1 is started, nothing under .shop/work/ is left uncommitted, a second `work run i1`, and the second `work run` was not refused. It is **not in `features/supervision.feature` yet**, and this plan cannot add it. See the question in the result. Once it is there, it is red today at "nothing under .shop/work/ is left uncommitted". Probe A (notes §2, §6 D1) shows `?? .shop/work/i1/runs/i1/`, and then the second run exits 1 with r46's refusal.

Retires: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: in `Rounds.round`, the DONE path of an integrate round, after the merge, commits the round's stage directory and its `log.jsonl` lines, the way `keep_round` does on the fault path and `move` does for the other kinds. It now has 102 lines, so there is room.
- `scripts/supervise.py`: read only. `commit` and `keep_round` are the helpers to call. Edit it only if the helper needs a different message parameter. It has 247 lines, with room for 53.
- `tests/scenarios/supervision_rounds_steps.py`: add a Then "i1 is started", the sibling of `i1_is_proposed`, because no step has that text today (searched). The other steps of the scenario exist: `work_committed`, `second_not_refused`, and the When of a second run in `test_supervision.py`. It has 242 lines, with room for 58.
- `features/supervision.feature`: the new @r84 scenario. It is a formulation, not the implementer's edit (see the question).

The notes' read-only and D2/D3-only files are dropped from the set: `supervise_brief.py`, `supervise_worker.py`, `workqueue_request.py`, and `supervision_world.py`. This plan takes neither D2 nor D3 (see §5).

## 3. Decisions

1. **On DONE, an integrate round commits its stage directory and `log.jsonl`.** It makes this commit as its own commit after the round's merge. `start_initiative`'s commit stays where it is, before the session. Rests on r84 and on the `:1056` scenario, which pins that the `started` transition comes before the round's start in the log. Moving that commit after the round would put this at risk. Also rests on r46: `work run` must not leave `.shop/work/` changes that refuse its own next run. The commit follows the shape r7 gives a transition (stage directories and `log.jsonl`, nothing else), and keep_round's for a round's stage directory. The commit is on the initiative branch, like the fault path's `keep_round`.
2. **The fault and non-DONE paths stay as they are** (`keep_round`, r86/r87/r88). This work-item does not reopen them. The work-item says to research narrowly, on the one finding.

## 4. Tests the decisions break

None. Decision 1 adds a commit after a DONE integrate round. No test asserts that the stage directory is left untracked. The notes' §4 searched `tests/` for `proposed`, `integrate` and `w_stale_intake`, and found no test that can no longer pass. `:1056` (`started_with_round`) reads the order of the log lines and the status in `initiative.md`. Decision 1 leaves `start_initiative` before the session, so both still hold. `:849` reads only the round's brief.

## 5. Open cases (for the implementer to name, not to choose)

- What the commit message of the DONE integrate commit says. Whether that commit pushes, as `start_initiative`'s does, or leaves the push to the next commit (notes §5).
- What the second `work run i1` does on a `started` initiative with no work-items (a second branch review, or nothing), as long as it exits 0 and prints no `work:` line on stderr.
- D2 (notes §6): a faulted integrate round leaves the initiative `started` (r84 timing against r86). Not taken here, because it is reading-dependent.
- D3 / review O9: a held request with no accepted line still gets an integrate round with an empty list of lines. Not taken here, because it is reading-dependent.
- An integrate round's `questions` are dropped (`supervise_rounds.py:82`). No requirement covers them.
