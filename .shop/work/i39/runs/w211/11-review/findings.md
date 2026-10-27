# Review 11 of w211 (after the answer that defers the reply and turn side check to w212)

**Verdict: DONE.** No finding is Critical and none is triaged fix now.

Review 10 had one fix-now finding: `reply` has no r34 side check. The answer of 2026-10-27 accepts this as it is and defers the side check on `reply` and `turn` to w212 (commit `9d0c875d` records it on w212), so the finding no longer applies. Review 10's finding 2 is still an observation; it is reproduced again below. The commits are unchanged since review 10.

## Commits reviewed

The branch `work/w211` is gone, so the commits were taken from HEAD. They are those between `085bb6e2 work: w211 ready -> claimed` (the last claim) and `fa667613 work: w211 claimed -> done`, leaving out `work run`'s `work:` commits:

- `025433c3` requests: decide the side per request; apply r34's side check to ask and resolve, let an internal request be raised in a repository with upstreams
- `4618d2d7` requests: the side check of a part reads the repository's context only for a request to an upstream, so a repository without spec/index.md is not refused

The implementers' results list `7b3f8f29` (8-implement) and `cb1aaaef` (9-implement). These are the same commits before the merge rebased them: `git diff --stat 7b3f8f29 025433c3 -- scripts tests features` and `git diff --stat cb1aaaef 4618d2d7 -- scripts tests features` are both empty. This is not a finding. Since `4618d2d7`, HEAD has no change under scripts/, tests/ or features/.

The two commits change only `scripts/workqueue_request.py`: 15 lines added and 5 removed, then 1 added and 2 removed.

## Removed and weakened tests

None. I looked for any change under `tests/` or `features/`, a deleted test or step function, a dropped parametrize case, a changed assert, and an added skip or xfail. The diff `085bb6e2..4618d2d7` names only `scripts/workqueue_request.py`.

## Allowances

Both reports (8-implement and 9-implement) say "none", and no test changed, so there is nothing to verify.

## Cannot verify

- **No scenario covers the new refusals.** Nothing exercises the r34 refusals of `ask` and `resolve`, or an internal request raised with only `--source` in a repository that lists upstreams. Only the probe below does. A scenario row needs a formulation first.
- **The whole suite after `4618d2d7`.** The 9-implement report gives `test_requests.py` in whole-suite mode as 43 passed and 11 xfailed, and `--work-item w211` as 165 passed and 1 skipped. I did not re-run the whole suite: `work run` ran it before the merge.

## Findings

### 1. Important, observation: an internal request on a job-thread in a repository that lists upstreams is taken as a request to the upstream
- **Work-item:** w211 (commit `025433c3`).
- **Where:** `scripts/workqueue_request.py:102-105` (`gate`) and `:108-114` (`_refuse_upstream_part`).
- **What is wrong:** `_refuse_upstream_part` treats a request as one to the upstream when three things hold: its asker is this repository's own id, the repository lists upstreams, and the request has no `source:`. r44 and r45 also allow an internal request that has only `--thread`. In a repository with upstreams, `gate` lets such a request be raised, but every `outcome`, `ask` and `resolve` on it is then refused, naming the upstream. With no transport, nobody can settle it, which goes against r15 and r25 for that request.
- **Why it matters:** the capability has no way to tell an internal thread request from a thread request to an upstream, because a request does not name its upstream. The rule "an origin means internal" is a reading of the ruling, not something a line states.
- **Why observation:** no client sends this today. This repository lists no `## Upstreams`, its internal requests have asker `internal` and a `source:`, and `supervise_raise` writes straight into the upstream's checkout.
- **Reproduction:** probe `.shop/scratch/w211-11-review/test_probe_side.py`. In repository ctx-a, whose `## Upstreams` names ctx-u, on a request with `asker: ctx-a` and `part_of: t1` in the upstream's turn:
  - `gate(root, "ctx-a", [], "t1", None)` gave `gate --thread t1: passes`.
  - `outcome(root, "q1", 1, "accepted")` gave `refused: q1 is a request to the upstream ctx-u; the upstream writes the line outcomes`.
- **Fix:** have a request to an upstream name its upstream (for example an `upstream:` field written when it is raised), and read the side from that. This needs a line first, so it belongs with w212's transport design.

(Not a finding: `reply` and `turn` still have no side check. The probe gave `reply on another context's request: written`, which is what the answer of 2026-10-27 accepts until w212. Review 7's Minor findings stay deferred by the ruling.)

### Checked and sound
- **The side comes from the repository** (r33): `_refuse_upstream_part` reads `spec/index.md` and the request's `asker`/`source`, never an argument.
- **Refusals change nothing** (r34): in `resolve`, `edit` runs before `write`, and in `outcome` and `ask` it runs inside `_change`. In both, the side check comes before the turn check (r16), as plan D2 says.
- **Internal requests still work:** a request with a `source` in a repository with upstreams passes the gate, and `ask` writes on it (probe: `gate --source only: passes`, `ask on internal (source) request: written`). This matches the ruling's r44, r15 and r25.
- **Code no line asks for:** none. Each changed behaviour serves r30, r31, r34 or r44 as the ruling reads them.

## Checks
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools check --base 085bb6e2`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools size --limit 300`: nothing printed, so no file is over the limit.

## Commands run
- `git log --format=%H -1 --grep="^work: w211 ready -> claimed$" work/w211`: the branch is gone.
- `git log --format='%H %s' --grep="^work: w211 "`, `git log --oneline -40`
- `git log --stat 085bb6e2..fa667613`, `git diff 085bb6e2 4618d2d7`, `git diff 4618d2d7 HEAD --stat -- scripts tests features` (empty)
- `git diff --stat 7b3f8f29 025433c3 -- scripts tests features` and `git diff --stat cb1aaaef 4618d2d7 -- scripts tests features` (both empty)
- Read `scripts/workqueue_request.py:85-215`, the plan's D2 and its "Tests the decisions break", and decisions 0067, 0055 and 0071.
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w211-11-review/test_probe_side.py`: 3 passed, with the output quoted above.
- `tools check --base 085bb6e2` and `tools size --limit 300`, as above.
- `git status --short`: clean.
