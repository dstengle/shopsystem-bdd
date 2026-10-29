# Plan: w237 (supervision r214, r215, r216)

This plan replaces 3-plan. The question 3-plan left open is answered (work-item, ## Answers, 2026-10-29): reading A. r218 governs i2's own sessions, and the code stays as it is. The scenarios are made independent of timing in their Given.

## 1. What goes green

The researcher ran `python3 -m pytest -q --work-item w237`: 3 failed, 180 passed, 1 skipped. All three scenarios stop at the same undefined Given (`StepDefinitionNotFoundError`, notes part 1), "every round ends and every worker gives DONE, and while i1's researcher works a session of i2 changes .shop/work/i2/initiative.md in the repository's own checkout without committing it". Their Thens have no step definitions either.

- supervision#r214, "what changed in the repository's own checkout while a session of one initiative worked is checked without the paths of another initiative run side by side". Red on the Given and on the missing Then "w1 is green, nothing recorded of w1 naming .shop/work/i2/initiative.md". The rule has been in `Faults.checkout_changes` since d8f57cc8: it leaves out each other initiative's `.shop/work/<X>/`.
- supervision#r215, "a change to another initiative's path under .shop/work/, made by that initiative's session while a session of one initiative worked, is not put back". Red on the Given and on the missing Then ".shop/work/i2/initiative.md is as i2's session changed it".
- supervision#r216, "... faults no session". Red on the Given and on the missing Thens "no session of i1 or of i2 was taken as a fault" and "w1 is not failed and p2 is not failed".

Deprecated scenarios retired: none. The work-item has no Retires section.

## 2. Where the change lands

The file set is the one the coordinator's answer gives (2026-10-29), and nothing else changes:

- tests/scenarios/supervision_faults_steps.py (207 lines, 93 to spare): the new Given (D1) and the four new Thens (D2).
- scripts/supervise_faults.py (194 lines): in the set by the coordinator's answer. Under reading A, `checkout_changes` is unchanged (answer: "Keep the code as it is"). Its docstring already names r214 and r218. At most it gains r215 and r216 among the requirements it names, if the implementer finds that wanting.

On the path and unchanged (notes part 4): scripts/supervise_worker.py, whose stale `Run.worker` docstring (169-177) is outside the set (see part 5); scripts/supervise.py (5 lines to spare); scripts/supervise_all.py; and tests/scripts/stub_claude.py, whose `elsewhere` step is used as it is, with its `commit` form and its `meet`/`linger` options.

## 3. Decisions

- D1. The Given. The change is made by a session of i2, not by i1's researcher (unlike `two_sessions_change`). It is made while i1's researcher works, and that same i2 session's own end takes it in, as the answer requires. No later i2 round then finds it uncommitted, and the scenarios hold on every run, alone and under `-n auto`.
  - Every worker and every round gives DONE.
  - One of p2's sessions that can run beside i1's researcher is bound to the change through the stub's plan, keyed by the round and p2 rather than by agent. That is p2's gate round: gate is not among the rounds r95 runs one at a time (notes part 3).
  - That session waits until i1's researcher has started (the stub's meeting options). It then writes `.shop/work/i2/initiative.md` in the repository's own checkout, as its committed text plus one added line. Before it ends, it commits that file itself through the `elsewhere` step's commit form, as "another session's commit" (the same way the r156 scenario's other session commits notes.txt).
  - The Given stores the written text in the scenario's `context` for r215's Then.
  - Rests on: the answer (reading A, gate question 2 (a)); r215 and r216 ("by a session of that initiative, while a session of one initiative worked"); r218 still holding for i2's own check.
- D2. The Thens. Each is a regex or parse Then in the faults steps module, reusing that module's and supervision_world's helpers:
  - r214: w1's status is `green`, read as `is_green` reads it. Neither w1's file nor any line of i1's log.jsonl about w1 names the path, the same check `nothing_names` makes. The Then is worded "naming", so it is a step of its own, not `nothing_names`. Rests on supervision#r214.
  - r215: at the end of `work run`, the file's text equals the text the Given stored. Rests on supervision#r215.
  - r216, first Then: no node file of i1 or of i2 (work-items, capability-proposals, initiative.md) has a `## Faults` section that holds an entry. No commit on the initiative branch is a round's "faulted" keep (`keep_round`'s message). Rests on supervision#r216, with r128/r86/r88 for what being taken as a fault records.
  - r216, second Then: w1's frontmatter status and p2's are each not `failed`. Rests on supervision#r216.
- D3. Production code. None changes in behaviour. This was settled by the answer (reading A: r215/r216 cover a change made by another initiative's session; r6, r34 and r218 still apply to a session's own initiative).

## 4. Tests the decisions break

None. The notes' part 3 searched tests/ for "put back", "checkout_changes", "i2/initiative" and "another initiative" and checked each of these:
- `another_session_changes` (i1's own path) is untouched.
- `two_sessions_change` with `is_failed` and `nothing_names` (r218) is untouched. Its i2 write stays bound to i1's researcher, and `is_failed` keeps leaving `.shop/work/i2` out of what must be clean.
- The committed-i2-file scenario (test_supervision.py:158-164) is untouched.

D1 adds a new Given and changes no existing step. D3 changes no code.

## 5. Open cases

The implementer names each of these and does not choose:

- Ordering within the Given. For r214's leaving-out to be exercised, the i2 path should still be uncommitted when i1's researcher ends, with i2's session committing after that. If the stub's options cannot hold i2's commit until after the researcher's end without a change to stub_claude.py (outside the set, 18 lines to spare), the implementer names what the scenario then exercises of r214.
- Whether p2's gate is the right i2 session: whether it starts while i1's researcher can still be met. If not, which p2 round is.
- Whether a later write by `work run` of i2's initiative.md (a transition of i2 through `workqueue_done.mark`) keeps the added line that r215's Then compares.
- That i2's session commits on the initiative branch while i1's run merges w1: whether `work run` takes that commit in as it does r156's notes.txt.
- The stale docstring of `Run.worker` (supervise_worker.py 169-177) says every uncommitted `.shop/work/` change is put back. It is outside the file set.
