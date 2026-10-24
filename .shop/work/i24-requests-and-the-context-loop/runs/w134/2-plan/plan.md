# Plan of w134: `work run` with no initiative

Work-item: `.shop/work/i24-requests-and-the-context-loop/w134.md`, under supervision, accepts supervision#r66, #r81, #r82.
No `## Retires`, no `## Rulings`. From the research notes (`runs/w134/1-research/notes.md`).

Outcome: QUESTION. Parts 1-5 are planned as far as they go. Two questions (end of part 3) are not mine to take.

## 1. What goes green

- **supervision#r66**: "`work run` started with no initiative takes every initiative that is neither done nor
  abandoned through its transitions, the initiatives side by side and one session of an initiative at a time"
  (features/supervision.feature:957). Red today: its first Given has no step definition, and neither do the
  later steps (notes part 1). Below that, `work run` with no initiative is a usage error (notes P1: exit 2,
  "the following arguments are required: initiative"), and no code starts a gate round or reads a
  capability-proposal (0 hits in scripts/supervise*.py). Its Thens ("the gate rounds of p1 and p2 ran at the
  same time", "p1 and p2 are awaiting-answer") need supervision#r68 and #r69. Those are accepted by w146 and w136,
  not by w134 (question 1).
- **supervision#r81**: the outline "`work run` started with no initiative, ending with <node> <status>, exits with an
  error, printing the status of each initiative it took" (:1003). Rows: work-item w1 awaiting-answer,
  capability-proposal p1 awaiting-answer, work-item w1 failed. Red today: all three stop at the missing step
  "i1 is started, and i1's <node> is <status>". The i2 Given and the "prints i1 with started and i2 with started"
  Then are undefined, and the run itself is a usage error (P1). Row 2 also needs a proposal's status to be read,
  and nothing reads it (P3: a proposal awaiting-answer beside w1 changes nothing).
- **supervision#r82**: "`work run` started with no initiative, ending with no node awaiting-answer or failed, exits
  successfully, printing the status of each initiative it took" (:1018). Red today: its Givens and its print Then
  are undefined. "it exits successfully" exists. The run is a usage error (P1).
- Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/work`: the `run` parser's `initiative` becomes optional. `cmd_run` sends a run with no initiative
  to the all-initiatives path.
- `scripts/supervise.py`: `run` keeps the one-initiative path as it is. The end-of-run print and the exit rule
  get the no-initiative form (decisions 3, 4). `commit` keeps its `unlogged` lines per initiative (notes part 3:
  one initiative's commit would clear another's lines). Room 82 lines. Anything bigger goes to the new module.
- `scripts/supervise_all.py` (new): the no-initiative driver. It selects the open initiatives (reusing
  `workqueue_status.open_names`), runs the one-time checks (decision 2), pulls the initiatives side by side under
  one shared worker limit with one session of an initiative at a time, and prints each initiative's status.
- `scripts/supervise_pool.py`: `choose` and `pull` take the shared limit and the rule of one session of this
  initiative at a time (decision 5).
- `scripts/supervise_worker.py`: the checkout lock is shared by all initiatives of the run (notes part 3, :129-175).
- `scripts/workqueue.py`: a reader of a capability-proposal's status beside `items` (decision 6). Room 28
  lines. If the reader does not fit, it goes into `scripts/supervise_all.py` and `workqueue.py` drops out of the set.
- Read and reused unchanged: `scripts/workqueue_status.py` (`open_names`), `scripts/supervise_faults.py`,
  `scripts/supervise_merge.py`, `scripts/supervise_review.py`, `scripts/supervise_brief.py`. Each one runs per
  taken initiative through `self.initiative` and `self.dir`.
- `tests/scenarios/supervision_all_steps.py` (new): the Givens and Thens of part 1. supervision_given.py has
  50 lines of room, which is not enough.
- `tests/scenarios/test_supervision.py`: one import line for the new steps module.
- `tests/scenarios/supervision_world.py`: reused (`fields`, `write`, `item_text`). It is in the set only in case
  a helper for an initiative's status or a proposal file is needed there.
- `CLAUDE.md`: a module-map row for `scripts/supervise_all.py` ("a new concern gets a new module and a row").

## 3. Decisions

1. **Selection.** With no initiative, `work run` takes each initiative whose `initiative.md` status is
   neither `done` nor `abandoned`, by `workqueue_status.open_names`, and no other. An ended initiative
   gets no session and is not printed (supervision#r66; #r82 "does not print i3").
2. **Checks once, before anything moves.** These run once for the run: the r21 worker refusal, `read_delivery`
   (the limit), the branch, the refusal of uncommitted `.shop/work` and the r54 push of unpushed commits. The
   `agrees` check runs for each taken initiative. A refusal changes nothing (supervision#r10, #r46, #r54, #r60).
   With no open initiative, the run prints no initiative and exits successfully (supervision#r82: none is
   awaiting-answer or failed).
3. **Print.** For each taken initiative, a line naming it and its `initiative.md` status. Under that line come its
   nodes' statuses and each open question and fault, as supervision#r9, #r32 and #r52 already require of any run
   whose work-items stop. The one-initiative output is unchanged (notes part 4: prints_end, prints_statuses and
   prints_question stay sound).
4. **Exit.** With no initiative given, the run exits with an error when any taken initiative's node (work-item or
   capability-proposal) is `awaiting-answer` or `failed`, and successfully otherwise (supervision#r81, #r82). The
   error codes follow the rule the Implementation section gives for one initiative
   (design-decision/exits-are-successful-or-errors): 3 when a node is awaiting-answer and none is failed, 1 when
   a node is failed. The Implementation section is spec, so the implementer does not edit it.
5. **Side by side, one session of an initiative at a time.** The taken initiatives are pulled at the same time,
   within one worker limit for the whole run. An initiative has one session running at a time, except for the
   workers supervision#r20 and #r59 start together (supervision#r66, #r60).
6. **A capability-proposal is a node.** Its status is read from its `kind: capability-proposal` file under the
   initiative. `awaiting-answer` or `failed` counts for decision 4 (supervision#r81 row 2). Starting a proposal's
   rounds is not part of this work-item (question 1).

Questions (not taken; outcome QUESTION):

- Q1, the gate rounds in r66's scenario. Its Thens need `work run` to start a gate round for a drafted proposal
  (supervision#r68, w146) and to move the proposal to awaiting-answer when that round ends (supervision#r69, w136).
  w134 has no `blocked_by`. Reading A: w134 does the selection, the side-by-side pulling and the exit only, and
  gets `blocked_by: [w146, w136]`. The narrator sees no gate round from any `work run` until those land, and w134
  waits for them. Reading B: w134 also starts the gate round of a drafted proposal and moves the proposal to
  awaiting-answer. The narrator sees `work run` start gate rounds as soon as w134 is merged, and w146 and w136
  build on that.
- Q2, the branch when several initiatives run. One checkout has one branch, and today the checked-out branch is
  the initiative branch (supervise.py:74). Reading A: every taken initiative commits and pushes on the one
  checked-out branch, and the run has one branch review over it. The narrator sees the transitions of i1 and i2
  mixed on that branch and, under supervision#r50, one review that reads all of them, so the second initiative
  gets no review of its own. Reading B: each initiative has its own branch, which `work run` checks out or makes
  (no requirement says how). The narrator sees one branch and one branch review per initiative.

## 4. Tests the decisions break

None. Verified from the notes, part 4: no test pins the usage error of a `work run` with no initiative (searched
for "required", "the following arguments" and "usage: work"). Every test that runs `work run` names `i1` and
asserts on i1's output, which decision 3 leaves unchanged. The r63 scenario (:694), which has i2 present, runs
`work run i1` and asserts only that a worker was started for w1 (read). Nothing in `tests/scripts/` imports
`work` or `supervise` except test_work_items.py, which only loads the pytest plugin.

## 5. Open cases

- The layout of the no-initiative print: the words of the initiative line, and how its nodes are set under it.
- The order of the taken initiatives, in the print and in starting them.
- A drafted capability-proposal under reading A of Q1: whether it counts as a node that can still make a
  transition. r82's success depends on it.
- An initiative that is `proposed` (supervision#r79): the selection takes it, but nothing in w134 moves it.
- A fault in one initiative (a failed push, r53) while another initiative's sessions run: whether the others finish.
- The `log.jsonl` and lock names when two initiatives write at the same time.
