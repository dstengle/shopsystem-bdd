# Review 10 of w211 (fix loop of review 7: the side per request, r34 on every part)

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now. The person's ruling of 2026-10-27 said to apply r34's side check to "every command that writes a part (ask, reply, resolve, outcome, turn)". The commits apply it to outcome, ask and resolve, but not to `reply`. So the upstream still writes the asker's answers on a request from another context.

Nothing is Critical: the commits touch only `scripts/workqueue_request.py`, with no change under `features/` and no test changed. `tools check` and `tools size` are clean.

## Commits reviewed

The branch `work/w211` is gone, so the commits were taken from HEAD. They are those between `085bb6e2 work: w211 ready -> claimed` (the last claim) and `fa667613 work: w211 claimed -> done`:

- `025433c3` requests: decide the side per request; apply r34's side check to ask and resolve, let an internal request be raised in a repository with upstreams
- `4618d2d7` requests: the side check of a part reads the repository's context only for a request to an upstream, …

The implementers' results list these commits under other ids:

| Result | Id it lists | Id on HEAD |
|---|---|---|
| 8-implement | `7b3f8f29` | `025433c3` |
| 9-implement | `cb1aaaef` | `4618d2d7` |

The branch commits were rebased when `work run` merged them, so the ids differ but the content is the same: `git diff 7a5f40f0 cb1aaaef --stat` and `git diff 085bb6e2 4618d2d7 --stat` each show `scripts/workqueue_request.py | 19 ++++++++++++++-----`, and `git diff 7b3f8f29 025433c3 -- scripts tests features` and `git diff cb1aaaef 4618d2d7 -- scripts tests features` are both empty. This is not a finding.

## Removed and weakened tests

None. What I searched for: any change under `tests/` or `features/`, deleted test or step functions, dropped parametrize cases, changed asserts, and skip or xfail added. `git diff 085bb6e2 4618d2d7 --stat` names only `scripts/workqueue_request.py`.

## Allowances

Both reports (8-implement, 9-implement) say "none", and the commits change no test, so there is nothing to verify.

## Cannot verify

- **The new refusals have no scenario.** No scenario covers the refusals of `ask` and `resolve`, nor an internal request with `--source` in a repository that lists upstreams. The 8-implement report says so and says no red run was possible. The behaviour rests on the ruling and r34 alone, and only the probe below exercises any of it. A scenario row needs a formulation (features/ is not the implementer's).
- **The whole suite after 4618d2d7.** The 9-implement report gives `test_requests.py` in whole-suite mode as 43 passed and 11 xfailed, and `--work-item w211` as 165 passed and 1 skipped. I did not re-run the whole suite: `work run` ran it before the merge.

## Findings

### 1. Important, fix now: `reply` has no side check, so the upstream still writes the asker's answers (r34; the ruling of 2026-10-27)
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:172-178` (`reply`). `turn` (`:181-`) has no side check either.
- **What is wrong:**
  - The ruling says: "apply r34's side check to every command that writes a part (ask, reply, resolve, outcome, turn), not outcome alone". The commits add `_refuse_upstream_part` to `outcome`, `ask` and `resolve` only.
  - Take a repository that keeps a request whose asker is another context, i.e. the upstream. There, `work reply` writes the answer, which is the asker's part (r4), instead of refusing and naming the asker (r34).
  - The 8-implement report leaves this open: "with no transport there is no other path for an answer".
- **Why it matters:**
  - r34 binds whether or not a scenario covers it, and the person's ruling names `reply` explicitly.
  - There is a real conflict behind it. The capability's Implementation (requests.md:61-62) says "the asker writes and reads it there through the upstream's `work`". This repository keeps two such requests, q13 (asker `bounded-context/…/subscriptions-viewer/web`) and q14 (asker `product/…/subscriptions-viewer`). Refusing `reply` there leaves those askers no way to answer until w212 delivers a transport.
  - So the fix needs the person to choose: follow the ruling and refuse, or narrow r34 or the ruling until w212.
- **Verified by** a probe (commands below). In repository ctx-u, with no `## Upstreams`, on a request whose asker is ctx-a, in the asker's turn: `workqueue_request.reply(root, "q1", 1, "The work queue")` gave `reply: written: True`.
- **Fix:**
  - In `reply`, refuse, naming the asker as the side that writes answers, when the request's asker is neither this repository's own id nor `internal`.
  - `turn` writes no part (r7 lets either side pass the turn, and r16 already guards turns), so leaving it without a side check is defensible. Say so explicitly to the person, since the ruling lists it.
  - Add an r34 scenario row for each refusal.

### 2. Important, observation: an internal request on a job-thread in a repository that lists upstreams is taken as a request to the upstream
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:102-105` (`gate`) and `:108-114` (`_refuse_upstream_part`).
- **What is wrong:**
  - `_refuse_upstream_part` treats a request as one to the upstream when three things hold: its asker is this repository's id, the repository lists upstreams, and the request has no `source:`.
  - r44 and r45 also allow an internal request (asker the upstream itself) that has only `--thread`. In a repository with upstreams, `gate` accepts `--from <own id> --thread t1`, but every `outcome`, `ask` and `resolve` on that request is then refused, naming the upstream. With no transport, nobody can ever settle it, which contradicts r15 and r25 for that request.
  - The capability gives no way to tell an internal thread request from a thread request to an upstream: a request does not name its upstream. So the implementer's choice ("an origin means internal") is a reading, not something a line states.
- **Why "observation":** no client sends this today. This repository lists no `## Upstreams`. Its internal requests have asker `internal` and `source:`, and `supervise_raise` writes into the upstream's checkout. Grep of scripts/, features/ and tests/ found no client raising `--from <own id> --thread` in a repository with upstreams.
- **Reproduction** (probe below), in repository ctx-a with `## Upstreams` naming ctx-u, on a request with `asker: ctx-a`, `part_of: t1` and the turn the upstream's:
  - `wr.gate(root, "ctx-a", [], "t1", None)` gave `gate --thread t1: passes`.
  - `wr.outcome(root, "q1", 1, "accepted")` gave `outcome: refused: q1 is a request to the upstream ctx-u; the upstream writes the line outcomes`.
- **Fix:** a request to an upstream should name its upstream (for example an `upstream:` field written at raise), and the side should be read from that. This needs a line first: put it to the person with w212's transport design.

(Review 7's Minor findings 3-7 still stand. They were deferred by the ruling and are not repeated here.)

## Checks
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools check --base 085bb6e2`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools size --limit 300`: nothing printed, so no file is over the limit. `scripts/workqueue_request.py` is 220 lines.

## Commands run
- `git log --format='%h %s' -1 --grep="^work: w211 ready -> claimed$" work/w211`: the branch is gone.
- `git log --format='%h %s' --grep=w211 HEAD`, `git log --format='%h %s' -20 HEAD`, `git log --format='%h %s' 085bb6e2..fa667613`
- `git cat-file -t 7b3f8f29`, `git cat-file -t cb1aaaef`, `git log --format='%h %p %s' -1 7b3f8f29`, `… cb1aaaef`, `… -4 fa667613`
- `git diff 7a5f40f0 cb1aaaef --stat`, `git diff 085bb6e2 4618d2d7 --stat`, `git diff 7b3f8f29 025433c3 -- scripts tests features`, `git diff cb1aaaef 4618d2d7 -- scripts tests features`
- `git show 025433c3 -- scripts`, `git show 4618d2d7 -- scripts`
- Reads of `scripts/workqueue_request.py:85-184` and `scripts/supervise_raise.py:25-50`, plus a grep of `context_path` and `committed` in `scripts/workqueue.py`.
- Grep of the callers of `workqueue_request.*` and of `--thread` in scripts/; grep of `work request … --from` outside .shop/; grep of the asker and origin fields of `.shop/work/requests/*.md`; grep of `## Upstreams` and `id:` in `spec/index.md`; grep of the @r30, @r31, @r33 and @r34 scenarios in `features/requests.feature`.
- Probe `.shop/scratch/w211-10-review/test_probe_side.py`, run with `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w211-10-review/test_probe_side.py`. It loaded `…/w211-10-review/scripts/workqueue_request.py` and gave:
  - `outcome: refused: q1 is a request to the upstream ctx-u; the upstream writes the line outcomes`
  - `gate --thread t1: passes`
  - `reply: written: True`
  - 3 passed.
- `tools check --base 085bb6e2` and `tools size --limit 300`, as above.
- `git status --short`: clean.
