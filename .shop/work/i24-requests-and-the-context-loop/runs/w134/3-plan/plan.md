# Plan of w134: `work run` with no initiative

Work-item: `.shop/work/i24-requests-and-the-context-loop/w134.md`, under supervision, accepts supervision#r66, #r81
and #r82. It is `blocked_by` w146, w151 and w152, and all three are now green. No `## Retires`. Its `## Answers`
(2026-10-24) answers the two questions of the plan before this one (`runs/w134/2-plan/plan.md`). Those two questions
were written as one `## Questions` bullet, and that bullet gets one answer: "Reading A". This plan reads that answer
as taking Reading A of both questions (decisions 1 and 7).

The research notes (`runs/w134/1-research/notes.md`) are from before w146, w151 and w152. Since then the gate,
apply, formulate and integrate rounds exist in `scripts/supervise_rounds.py`, and so does a reader of a
capability-proposal's status (`Rounds.proposals`). `Run.run` now calls `answers`, `rounds`, `draft` and `pull` in
that order. I read `supervise.py`, `supervise_rounds.py`, `supervise_pool.py` and `supervise_faults.py` again only
to see where the decisions land. The feature's line numbers have moved too: r66 is now at :984, r81 at :1030 and
r82 at :1045.

## 1. What goes green

- **supervision#r66**: "`work run` started with no initiative takes every initiative that is neither done nor
  abandoned through its transitions, the initiatives side by side and one session of an initiative at a time"
  (:984). Red today: its first Given, "i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted",
  has no step. The steps after it have none either: the i2-with-a-proposal Given, the i3-done and i4-abandoned
  Given, the Given in which the gate rounds of p1 and p2 each end once both have started, and the Thens on the
  same-time gate rounds, on no two sessions of i1 at once, on no session for i3 or i4, and on "w1 is green, and p1
  and p2 are awaiting-answer". Beneath that, `work run` with no initiative is a usage error (notes P1: exit 2), and
  `Run` takes exactly one initiative. The gate rounds and the move to awaiting-answer now exist (w146, w152).
- **supervision#r81**: the outline "`work run` started with no initiative, ending with <node> <status>, exits with
  an error, printing the status of each initiative it took" (:1030). Its rows are work-item w1 awaiting-answer,
  capability-proposal p1 awaiting-answer, and work-item w1 failed. Red today: every row stops at the missing step
  "i1 is started, and i1's <node> is <status>". The i2 Given and the Then "`work run` prints i1 with started and i2
  with started" are undefined too: `prints_statuses` needs ", and " before the second name. The run itself is a
  usage error, and today's output prints work-item lines only, never an initiative's status.
- **supervision#r82**: "`work run` started with no initiative, ending with no node awaiting-answer or failed, exits
  successfully, printing the status of each initiative it took" (:1045). Red today: its three Givens and its print
  Then ("... and does not print i3") are undefined. "it exits successfully" exists. The run is a usage error (P1).
- Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/work`: the `run` parser's `initiative` becomes optional, and its help text names both forms. `cmd_run`
  sends a run with no initiative to the new driver. The one-initiative path stays as it is.
- `scripts/supervise_all.py` (new): the driver of a no-initiative run. It selects the initiatives (decision 2),
  runs the run-wide checks once (decision 3), and builds one `Run` per taken initiative, sharing what decision 4
  names. It pulls the initiatives side by side (decision 4), then prints (decision 5) and gives the exit
  (decision 6). It is a new module because `supervise.py` has 62 lines of room left (238 lines today).
- `scripts/supervise.py`: `Run.run` is split into two parts. The run-wide checks and the push of unpushed commits
  stay in the one-initiative entry. The per-initiative body (`answers`, `rounds`, `draft`, `pull`, the branch
  review, the analysis, removing the worktrees) becomes callable by the driver. `Run.__init__` takes the shared
  lock, limit and registry from the driver when it is given them (decision 4). The one-initiative print and exit
  are unchanged.
- `scripts/supervise_pool.py`: `choose` counts the workers of every taken initiative against the one limit, not
  only those of its own `pull` (decision 4, r60).
- `scripts/supervise_worker.py`: a round's or stage's session takes a place under the shared limit before it
  starts (decision 4). The lock that guards changes to the main checkout is the run's one lock.
- `scripts/supervise_faults.py`: `checkout_changes` (r28) does not count as loose what any taken initiative's `Run`
  wrote and has not yet committed, meaning its `own` run directories and its `unlogged` log lines (decision 4).
  Without this, i1's worker ending would put back i2's uncommitted lines.
- `tests/scenarios/supervision_all_steps.py` (new): the Givens and Thens of part 1. The modules nearby have no room
  left for them.
- `tests/scenarios/test_supervision.py`: one import line for the new steps module.
- `tests/scenarios/supervision_world.py`: only if a helper is needed to write another initiative with a given
  status or a capability-proposal file. Its `fields`, `write` and `item_text` are reused as they are.
- `CLAUDE.md`: a module-map row for `scripts/supervise_all.py` ("a new concern gets a new module and a row").

Dropped from the researcher's set, because no decision changes them:
- `scripts/workqueue.py`: the reader of a proposal's status now exists as `Rounds.proposals`.
- `scripts/workqueue_status.py`: `open_names` is reused, not changed.
- `scripts/supervise_merge.py`, `scripts/supervise_review.py`, `scripts/supervise_brief.py`: each already runs per
  initiative through `self.initiative` and `self.dir`. Under decision 7 the branch review is not changed.

Added to the set: `scripts/supervise_all.py` and `tests/scenarios/supervision_all_steps.py`, both new.

## 3. Decisions

1. **The gate rounds are not w134's.** w134 builds the selection, the side-by-side pulling and the exit. The gate
   round of a drafted proposal and its move to awaiting-answer are the green w146 (r68, r85) and w152 (r69), which
   the driver reuses through `Run`'s per-initiative body. This rests on the answer of 2026-10-24 (Reading A of the
   first question).
2. **Selection.** With no initiative, `work run` takes each initiative whose `initiative.md` status is neither
   `done` nor `abandoned`, as `workqueue_status.open_names` gives them, and no other. An ended initiative gets no
   session and is not printed (supervision#r66; #r82 "does not print i3"). A `proposed` initiative is taken: its
   integrate round is one of the transitions its nodes can make (r66, r79, r84).
3. **Checks once, before anything moves.** These run once for the whole run: the refusal when started by a worker
   (r21), reading `.shop/delivery.toml` and its limit (r60, r10), the refusal on a detached HEAD, the refusal of
   uncommitted `.shop/work` (r46), and the push of unpushed commits (r54). The `agrees` check runs for each taken
   initiative before any of them moves. A refusal changes nothing (supervision#r10). With no open initiative, the
   run prints nothing and exits successfully, since no node is awaiting-answer or failed (supervision#r82).
4. **Side by side, sharing one checkout.** Each taken initiative is pulled in a thread of its own by its own `Run`,
   all of them at the same time (supervision#r66). They share four things:
   - one lock over every change to the main checkout, its commits and pushes included, because there is one
     checkout and one index;
   - one worker limit for the whole run, so at most `.shop/delivery.toml`'s number of `claude -p` sessions run at
     the same time, round sessions included (supervision#r60);
   - one registry of what any of them wrote and has not committed, which r28's check leaves alone (supervision#r28
     and #r6 are about a worker's changes, not `work run`'s own);
   - the run's worktrees, all removed when the run exits (supervision#r33).

   Within one initiative, the order stays as `Run.run` has it: delegated answers, then rounds one at a time, then
   drafting, then the pool. So one session of an initiative runs at a time, but for the workers that r20 and r59
   start together (supervision#r66).
5. **Print.** For each taken initiative, in `open_names` order, a line names the initiative and its
   `initiative.md` status as it stands when the run ends. Under that line come its work-items' statuses, with each
   open question and each fault, as r9, r32 and r52 already require. A proposal that is awaiting-answer gets its
   open questions printed as well. The one-initiative output is unchanged (notes part 4: `prints_end`,
   `prints_statuses` and `prints_question` stay sound). This rests on supervision#r81 and #r82 ("printing the
   status of each initiative it took").
6. **Exit.** With no initiative given, the run exits with an error when a node of a taken initiative (a work-item
   or a capability-proposal) is `awaiting-answer` or `failed`, or when any initiative's run raised a refusal, such
   as a faulted round (r88) or a failed push (r53). Otherwise it exits successfully (supervision#r81, #r82). The
   codes follow the Implementation rule (design-decision/exits-are-successful-or-errors): 1 when a node is failed
   or a refusal ended an initiative's run, 3 when a node is awaiting-answer and nothing is failed, and 0 otherwise.
   A refusal is said on stderr with its initiative's name, after the other initiatives have ended. One initiative's
   fault or refusal does not stop the others: their nodes can still make transitions, and r66 takes them through
   every transition they can make.
7. **One branch.** Every taken initiative commits and pushes on the one checked-out branch, which is the
   initiative branch of each of them. r27 and r50 are kept as they are, per initiative. So the first initiative
   whose work-items are all green starts the branch review over that branch, and a later one finds no unread
   commit and starts none. This rests on the answer of 2026-10-24 (Reading A).

## 4. Tests the decisions break

None. What I checked:
- From the notes, part 4: no test pins the usage error of a `work run` with no initiative (searched for
  "required", "the following arguments" and "usage: work").
- Every scenario that runs `work run` names an initiative (`run i1`, through the When at test_supervision.py:53),
  and decision 5 leaves that output unchanged.
- No test under `tests/` builds a `Run` or imports `supervise` (searched for "supervise" and "Run(" in
  `tests/**/*.py`: only test_supervision.py's docstring). So the changed `Run.__init__` and `Run.run` break none.
- With one initiative there is one `Run`, so decision 4 changes nothing for today's scenarios. The shared lock,
  limit and registry are the run's own, as before. This covers the parallel scenarios
  (supervision_parallel_steps.py), the r28 scenarios that put files back, and the r63 scenario with i2 present
  (now near :694), which asserts only that a worker was started for w1.

## 5. Open cases

- The layout of the no-initiative print: the words of the initiative line, and how its nodes are set under it.
- What the step definitions make the gate rounds of r66 give. Under r70, a proposal whose questions are all
  answered, none included, gets an apply round. So p1 and p2 stay awaiting-answer, as the last Then needs, only if
  each gate round gives a question.
- What makes the nodes of r82's i1 and i2 unable to move without being awaiting-answer or failed. All-green
  work-items would start a branch review (r27) and then `measure initiative` (r75). A blocked work-item, or a
  withdrawn one alone, would not.
- Under decision 7, an initiative that is all green but got no branch review of its own: whether its measurement
  and analysis (r75) start, given that r75 asks for its kept branch review.
- The order in which the threads start the initiatives. Decision 5 fixes only the order of the print.
- How the shared limit is shared: one counter that both the pool and the round sessions take from, or a
  semaphore.
- The name of each initiative's temporary worktree directory when the repository is inside the plugin (r23), now
  that several `Run`s may each make one.
