# Plan: w237 (supervision r214, r215, r216)

Outcome: QUESTION. The plan goes as far as the step module; one decision that changes what the person who started `work run` observes (whether i2's own session is faulted and the change put back) is left by the requirements, which conflict on it (part 3, decision D3).

## 1. What goes green

All three are red today at the same undefined Given (`StepDefinitionNotFoundError`, run by the researcher: 3 failed, 180 passed, 1 skipped), before any Then runs. The Thens are undefined too (notes part 1).

- supervision#r214, "what changed in the repository's own checkout while a session of one initiative worked is checked without the paths of another initiative run side by side": red on the missing Given and the missing Then "w1 is green, nothing recorded of w1 naming .shop/work/i2/initiative.md". The rule itself is in code since d8f57cc8 (r218): `Faults.checkout_changes` leaves out each other initiative's `.shop/work/<X>/`.
- supervision#r215, "a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, is not put back": red on the Given and the missing Then ".shop/work/i2/initiative.md is as i2's session changed it".
- supervision#r216, "a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, faults no session": red on the Given and the missing Thens "no session of i1 or of i2 was taken as a fault" and "w1 is not failed and p2 is not failed".

Deprecated scenarios retired: none (the work-item has no Retires section).

## 2. Where the change lands

- tests/scenarios/supervision_faults_steps.py (207 lines, room 93): the new Given and the four new Thens.
- scripts/supervise_faults.py (194 lines, room 106): named by the coordinator's answer (2026-10-29). `checkout_changes` already leaves out the other initiatives' parts. It changes only under reading B of the question (D3): there, i2's own check must leave out a change that a session of i2 made while a session of i1 worked. Under reading A it is unchanged but for its docstring, if the implementer finds it stale.

Unchanged, on the path (notes part 4): scripts/supervise_worker.py (`Run.worker` raises the Fault from what `checkout_changes` returns; its docstring at 169-177 is stale about other initiatives' paths, but the file is not in the set, so the implementer leaves it and names it), scripts/supervise.py (room 5: add nothing), scripts/supervise_all.py, tests/scripts/stub_claude.py (the `elsewhere` write is used as it is).

## 3. Decisions

- D1. The Given sets every worker to DONE as `two_sessions_change` does. The researcher (`code-scout`) of w1 writes, through the stub's `elsewhere` step, only `.shop/work/i2/initiative.md` in the repository's own checkout, holding its committed text plus one added line. The Given stores that text in the scenario's `context` for r215's Then. Rests on r214-r216 (the change is to another initiative's part, made while i1's session worked). The `elsewhere` step is bound to w1's researcher by the stub's default (the work-item of the session).
- D2. The Thens:
  - r214: w1's status is `green` (as `is_green` checks), and neither w1's file nor any line of i1's log.jsonl about w1 names the path. This is the check `nothing_names` makes, under the wording "naming". The step is one regex Then for this sentence, using the same helpers as `is_green` and `nothing_names`. supervision#r214.
  - r215: the file's text at the end of `work run` equals the text the Given stored. supervision#r215.
  - r216 (first Then): no `## Faults` section holds a fault in any node file of i1 or i2 (work-items, capability-proposals, initiative.md), and `work run`'s output names no failed node. supervision#r216, with r128 for what "taken as a fault" means (a fault is recorded under `## Faults`, r86/r88).
  - r216 (second Then): w1's status is not `failed` and p2's status is not `failed`, read from their frontmatter. supervision#r216.
- D3 (not taken: the question). i2's run is in the same `work run`. p2 drafted goes through gate (not serial, so it can run beside i1's researcher), then apply and formulate (supervise_rounds.py AFTER, SERIAL). Each of these ends in `Run.worker`, which calls i2's own `checkout_changes`. That check does not leave out i2's own part, so under r218 it puts back the uncommitted `.shop/work/i2/initiative.md` and faults the round ("while its ... worked, ... changed ... work run put it back"). r215 ("put back no change of that path") and r216 ("fault no session for that change") say the opposite for a change "by a session of that initiative". Any i2 round that ends after i1's researcher writes falls under both. The narrator sees the difference: the file put back or kept, and a fault recorded on p2's round or not. The existing `is_failed` Then already leaves `.shop/work/i2` out of its check for this reason ("depends on when its sessions ended"). This decision is the question in the result.

## 4. Tests the decisions break

None. Verified from the notes (part 3), by search of tests/ for "put back", "checkout_changes", "i2/initiative" and "another initiative": no test asserts that another initiative's uncommitted path is put back.
- `another_session_changes` (i1's own path) still holds.
- `two_sessions_change` with `is_failed` and `nothing_names` (r218) still holds. Under reading B of D3, the implementer re-runs the r218 scenario, because i2's check then changes. Its Thens are on i1 only and the i2 path is excluded from `is_failed`, so it should still hold.
- The committed-i2-file scenario (test_supervision.py:158-164) is untouched.

## 5. Open cases

- Under reading A, the scenarios r215/r216 depend on timing (whether every i2 round ends before i1's researcher writes). The implementer names whether the stub's `meet`/`linger` steps can order the write after i2's last round. Such ordering is a test arrangement and must not stand in for the answer to D3.
- Whether a later commit by `work run` of i2's initiative.md (a transition of i2 that rewrites initiative.md) would commit or overwrite the change. The scenarios are silent; the implementer names it if seen.
- The stale docstring of `Run.worker` (supervise_worker.py 169-177), outside the file set.
