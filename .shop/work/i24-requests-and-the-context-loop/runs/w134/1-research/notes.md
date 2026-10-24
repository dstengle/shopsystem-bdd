# w134 research notes

Brief: `.shop/work/i24-requests-and-the-context-loop/w134.md`. Accepts supervision#r66, r81, r82.
Scenarios: features/supervision.feature:957 (r66), :1003 (r81 outline, 3 rows), :1018 (r82).
Tools: `tools` ran (`--help`, `refs`, `tests-of`, `size`). No coverage map (`tools: no map`), so
`tests-of` and `untested` give nothing; test lists below are `by search`. `refs` misses `scripts/work`
(no .py suffix): `supervise.run` shows 0 refs, the real caller is scripts/work:82 (found by search).
Probes: `.shop/scratch/w134-1-research/probe_no_initiative.py`, `probe_refusals.py` (scratch repos only).
Scratch dir is git-ignored: `git status --porcelain` empty after the probes.

## 1. Why each scenario is red today

Each accepted scenario was run by node id (`python3 -m pytest -q "<node id>"`, `read`/`run` as marked).
All 5 collected cases fail at their first Given, a missing step definition (pytest-bdd stops there):

- r66 `takes every initiative ...` (run): `StepDefinitionNotFoundError` on Given line 960
  "i1's capability-proposal p1 is drafted and i1's work-item w1 is drafted". Read: the later steps are
  undefined too: line 961 "an initiative i2 ... whose capability-proposal p2 is drafted" (supervision_parallel_steps.py:37
  takes "whose work-item" only); line 962 "that is done ... that is abandoned"; line 963 "every round ends ...
  the gate rounds of p1 and p2 each ending"; Thens 965 "the gate rounds ... ran at the same time", 966, 967,
  and 968 "w1 is green, and p1 and p2 are awaiting-answer" (test_supervision.py:80 matches "{names} are green" only).
  Code: no gate, apply or formulate round exists in scripts/supervise*.py (`grep` for gate|capability-proposal|
  proposed|integrate|apply|formulate: 0 hits in supervise*.py). So the Thens could only pass after r68/r83/r85
  rounds exist, which w134 does not accept (see part 7, question A).
- r81 outline `ending with <node> <status>` (run, 3 rows, `[work-item w1-awaiting-answer]`, `[capability-proposal
  p1-awaiting-answer]`, `[work-item w1-failed]`): all 3 fail at line 1006 "i1 is started, and i1's <node> is <status>"
  (no step; supervision_given.py:128 needs "i1's work-item"). Read: line 1007 "an initiative i2 ..., started, none of
  whose nodes ..." undefined; Then 1009 "`work run` prints i1 with started and i2 with started" undefined
  (test_supervision.py:181 needs ", and " before the second name, not " and ").
  Code: scripts/work:100 makes `initiative` a required positional; scripts/supervise.py:41-44 `Run.__init__(root,
  initiative)` takes exactly one; supervise.py:196-204 prints work-item lines only (`name status`), never an
  initiative's status; supervise.py:205-207 counts work-items only.
- r82 `ending with no node awaiting-answer or failed` (run): `StepDefinitionNotFoundError` on Given line 1021
  "i1 is started, none of its nodes can make a transition and none of them is awaiting-answer or failed". Read:
  lines 1022 (i2 Given) and 1023 ("an initiative i3 ... that is done") undefined; Then 1025 "prints i1 with started
  and i2 with started, and does not print i3" undefined (regex at test_supervision.py:181 ends in "$" after the second
  status). "it exits successfully" (test_supervision.py:91) is defined. Real When outcome: see part 2, P1.

## 2. What the system answers today

Probe commands: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w134-1-research/probe_no_initiative.py`
and `... probe_refusals.py` (`-n 0`: the repo's addopts start xdist, which swallows prints). Each probe builds its own
git repo under the scratch dir with `.shop/delivery.toml` (tests `true`), commits it, and runs
`scripts/work --root <repo> run [args]`. No remote, no worker started (nothing movable), so every result is `run`.

- P1 `NO-ARG` (run): `work --root R run`, with i1 started and w1 drafted (the r82/r66 When without an initiative).
  Returns exit 2, stdout empty, stderr `usage: work run [-h] initiative` / `work run: error: the following arguments
  are required: initiative`. Nothing is read or changed. (Feeds r66, r81, r82.)
- P2 `I1-ONLY` (run): i1 has w1 awaiting-answer (`## Questions` "Which module owns the log?"); i2 has its own
  awaiting-answer w2 (question "Second initiative's question?"). `work run i1` returns exit 3, stdout
  `w1 awaiting-answer` / `  - Which module owns the log?`. i2 is not read or printed. (The nearest case of r81's
  "the other initiative stays put"; r66 takes all open ones only with no initiative.)
- P3 `P1-BESIDE` (run): as P2 plus `.shop/work/i1/p1.md`, a capability-proposal with status awaiting-answer and a
  `## Questions` line. `work run i1` output is identical: exit 3, only w1 printed. The proposal's status is never
  read (`workqueue.items` yields only `kind: work-item` files, workqueue.py:100-105). This is the r81 row 2 case.
- P4 `UNKNOWN` (run): `work run i9` with no i9 folder: exit 1, stderr `work: the initiative i9 does not exist (no
  .shop/work/i9)` (supervise.py:70-71). Refusal is per named initiative, so no no-initiative counterpart exists.
- P5 `WORKERS-0` (run): `.shop/delivery.toml` with `workers = 0`, i1 with w1 awaiting-answer: exit 1, stderr
  `work: workers in .shop/delivery.toml is 0, not a positive integer`. Refused in `read_delivery` (supervise_pool.py:33-44)
  from `check()` (supervise.py:69), before any move.
- P6 `UNCOMMITTED` (run): i1's w1.md changed and not committed: exit 1, stderr `work: .shop/work/i1/w1.md under
  .shop/work is not committed; commit it before work run starts` (supervise.py:77-81, r46).
- Not probed (read): a `work run` on i3 (done) or i4 (abandoned) explicitly: `check()` accepts any initiative that has
  a folder; nothing skips an ended one. Not run, because the no-initiative selection is the new behaviour.

## 3. Old assumptions

"One initiative per run" is the old form: a `Run` is built for one name, and its paths, items, log, lock, limit and
branch review follow it. Row set (`by search`, since no map exists; "tests" are the supervision scenarios that drive
`work run i1`, all in tests/scenarios/test_supervision.py and the supervision_*_steps.py modules):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work:100 `run` parser | `initiative` required positional | optional; no name = every open initiative (r66, r81, r82) | test_supervision.py: every `work run` scenario | read + search (scripts/work has no .py: refs misses it) |
| scripts/work:81-82 `cmd_run` | calls `supervise.run(root, initiative)` | dispatch with None to the all-initiatives path | test_supervision.py (every run) | search |
| scripts/supervise.py:41-55 `Run.__init__` | one `initiative`; `dir`, `lock`, `limit`, `finished`, `turns`, `own`, `unlogged`, `faults` per run | a run of many initiatives: the limit (r60) and the lock are shared; per-initiative serial (r66) | test_supervision.py; supervision_parallel_steps.py | search |
| scripts/supervise.py:60-61 `items()` | filters `workqueue.items` to `self.initiative` | per initiative, for each taken one | test_supervision.py | read |
| scripts/supervise.py:63-81 `check()` | refuses non-existent initiative, reads delivery (sets `self.limit`), `self.branch`, refuses loose .shop/work and worker env | must run once for the run and per taken initiative; sets `self.branch` and `self.limit` used later | test_supervision.py (refusal scenarios) | search |
| scripts/supervise.py:182-194 `run()` | `check`, `push_unpushed`, `pull(MOVABLE)` for one initiative; branch review when its items are all green | one pass per taken initiative, branch review per initiative (r27), r50 unchanged | test_supervision.py | read |
| scripts/supervise.py:196-207 print and exit | prints work-item lines; exit 0 if its items green/withdrawn, 3 if awaiting, else 1 | r81/r82 print each initiative's status and exit 1 for awaiting/failed, 0 otherwise; single-initiative output stays | test_supervision.py:172-185, 227 (prints_end, prints_statuses, prints_question) | search |
| scripts/supervise_pool.py:59-84 `choose()` | takes `self.items()` (one initiative) and `self.limit` | worker limit shared by all initiatives (r60, r66 "but for r20/r59 together") | supervision_parallel_steps.py (limit, same-time scenarios) | search |
| scripts/supervise_pool.py:86-126 `pull()` | starts workers for the one run's items until none can move | one initiative's sessions at a time (r66); other initiatives side by side | supervision_parallel_steps.py | read |
| scripts/supervise.py:96 `commit()` | `self.unlogged = []` clears the run's lines, whatever initiative they were for | per initiative: a commit of i2 would clear i1's unlogged lines | none (no scenario has two initiatives in one run) | read |
| scripts/supervise_faults.py:81-83 `fail()` | `workqueue.move(self.initiative, ...)` | per initiative (named by the taken initiative) | supervision_faults_steps.py | read |
| scripts/supervise_worker.py:124 tempfile prefix uses `self.initiative`; :129-175 `self.lock` and `self.turns` | per run lock | per run lock kept only if one Run handles all initiatives; two Runs in threads need one shared lock on the checkout | supervision_parallel_steps.py | read |
| scripts/supervise_review.py:35-77 `branch_review()` | runs for `self.initiative`, commit names it | run once per initiative whose items are green (r27), using the one branch | supervision_review_steps.py | search |
| scripts/supervise_merge.py:85-87 `agrees(root, self.initiative, name)` | one initiative's items | per initiative | supervision_parallel_steps.py | search |
| scripts/supervise_brief.py:15,21,27,67 | `self.dir`, initiative.md history | per taken initiative | supervision_then_workers.py | search |

Shared branch (read, not a row of code): `Run.check` sets `self.branch` to the checked-out branch (supervise.py:74),
and every commit and push goes to it. The requirements name "the initiative branch" per initiative (r27, r38, r54).
With several initiatives there is one checked-out branch (see part 7, question C).

## 4. Tests the requirements make impossible to keep

- Searched tests for a usage error of the `run` parser (`required`, `the following arguments`, `usage: work`): none
  (`by search`). No test pins that `work run` needs an initiative.
- Searched tests for `work run` callers: tests/scenarios/test_supervision.py, supervision_answers_steps.py,
  supervision_faults_steps.py, supervision_given.py, supervision_review_steps.py, supervision_tests_steps.py,
  supervision_then_workers.py, supervision_world.py, supervision_parallel_steps.py, test_work_queue.py (its word
  "work run" is in text only), tests/scripts/stub_claude.py, tests/scripts/test_work_items.py (`by search`).
  Every one passes `i1` (or none of `work run`'s argv beyond `run i1`) and asserts on i1's own files and lines.
- Read test_supervision.py whole: prints_end (172), prints_statuses (181), prints_question (227), exits_successfully
  (91), exits_with_error (96), the `{names} are green` helpers. They assert the single-initiative output. Changing
  the no-initiative output keeps them sound, since r81/r82 say the initiative lines are printed for no-initiative runs
  only. Verified sound (`read`).
- Not read (open): features/supervision.feature:697 "an initiative i2 under .shop/work/ whose work-item w2 is green"
  (a scenario that starts `work run i1` with i2 present). I did not read its Then; if it asserts that i2's status or
  lines are absent from output, a new per-run print could break it. Check before the plan.
- Nothing in `tests/scripts/` breaks by the change (`by search`, the `work` and `supervise` names are not imported
  there except test_work_items.py, which loads the pytest plugin only).

## 5. A step the work-item skips

The single-initiative `Run.run` does five things before anything moves; a no-initiative path that loops
initiatives around `pull` skips the ones that set state:

- `check()` (supervise.py:63-81): r21 worker refusal (P: `read`), initiative existence (P4 `run`), `workqueue.entry`,
  `agrees` per item (`read`), `self.branch` set (`read`: only check sets it; pull, commit and push use it, so a path
  that skips check gets an AttributeError), `read_delivery` sets `self.limit` (P5 `run`: refusal; a skipped read leaves
  4 workers instead of the file's number, so r60 breaks), and the loose .shop/work refusal (P6 `run`).
- `push_unpushed()` (run, supervise.py:186; supervise_faults.py:35-63, r54): pushes the branch once, refuses a diverged
  remote (`read`). A per-initiative loop would repeat it per initiative: `read`.
- `branch_review()` (run, supervise.py:189-190): r50 and r51 guards and the push verification before a review (`read`).

## 6. Defects

None found by the probes run (P1-P6). P2 shows the single-initiative run reads only the named initiative, as the code
says; P3 shows a capability-proposal's awaiting-answer is ignored, as the code says (there is no proposal reader).
Neither is a defect against today's spec; both are the gap the accepted requirements fill.

## 7. The file set

Production (to change):
- scripts/work (138 lines, room 162): `run` parser makes `initiative` optional (:100), `cmd_run` (:81-82) passes None for it.
- scripts/supervise.py (218, room 82): the no-initiative selection, the per-initiative `Run`s, the print of each
  initiative's status and the exit rule (:196-207). Or split into a new module: see below.
- scripts/supervise_pool.py (142, room 158): the worker limit and the one-session-per-initiative rule shared across
  initiatives (`choose`, `pull`) if one `Run` is built per initiative; `choose` already reads cross-initiative statuses
  for `blocked_by` (:62-63).
- A new module for the all-initiatives driver (e.g. `scripts/supervise_all.py`), with a row in CLAUDE.md's module map
  ("a new concern gets a new module and a row here"). The planner decides; `open_names` (below) gives the list.

Read or reused, on the path, not changed by the requirements (each named with the search that showed it):
- scripts/workqueue_status.py (170, room 130): `open_names(root)` (:129-134) lists initiatives whose initiative.md status is
  not done or abandoned (ENDED at :15). It is the r66 selection; reuse, do not copy.
- scripts/workqueue.py (272, room 28): `items(root)` (:100-105) yields (initiative, name, status) for work-items only,
  and `agrees` (:179). Reused as they are.
- scripts/supervise_worker.py (229, room 71), supervise_faults.py (160, room 140), supervise_merge.py (135, room 165),
  supervise_review.py (77, room 223), supervise_brief.py (110, room 190): each uses `self.initiative` or `self.dir`; run
  per taken initiative, so no edit is needed unless the lock or the log change (see part 3).

Tests (to change):
- tests/scenarios/test_supervision.py (246, room 54): `scenarios("supervision.feature")` binds r66/r81/r82 already;
  it must import the new steps module (lines 25-32), one import line.
- a new steps module, e.g. tests/scenarios/supervision_all_steps.py: the Givens "i1's capability-proposal p1 is
  drafted ...", "an initiative i2 ... whose capability-proposal p2 is drafted", "an initiative i3 ... that is done",
  "i1 is started, and i1's <node> is <status>", "every round ends", the Thens "`work run` prints i1 with started and i2
  with started", "... and does not print i3", "w1 is green, and p1 and p2 are awaiting-answer". supervision_given.py
  (250, room 50) has no room for them; keep them in a new module.
- tests/scenarios/supervision_world.py (173): `fields`, `write`, `item_text` reused as they are.
- tests/scripts/stub_claude.py: no change expected (`by search`).

Open conflicts (for the plan, both readings):
- A. r66's scenario (features/supervision.feature:957) needs `p1` and `p2` to get gate rounds ("the gate rounds of p1 and
  p2 ran at the same time", "p1 and p2 are awaiting-answer"). That is r68 and r85, which w134 does not accept, and no
  code of them exists (part 1). Reading 1: w134 makes only the selection and the exit, and r66's scenario stays red
  until the proposal-round work-item lands. Reading 2: w134 also takes the gate rounds (not accepted, so out of its scope).
- B. The print. r81/r82 require `prints i1 with started`, the initiative's own status. Today's run prints work-item lines
  (supervise.py:196-204). Reading 1: no-initiative runs print initiative lines only. Reading 2: they print each initiative's
  status and then its work-items (the scenarios assert only that the initiative lines appear).
- C. The branch. The one checked-out branch serves every initiative (supervise.py:74); r27's "the initiative branch" is
  read per initiative in the requirements. Reading 1: one shared branch; each initiative's branch review then reads the
  commits of all (r27/r50 bite across initiatives). Reading 2: each initiative has its own branch, which the code does not
  create. The plan must pick; the scenarios do not say.
- D. r81's second row takes `capability-proposal p1 awaiting-answer` as a stop. No code reads a proposal's status (P3). The
  scenario sets it by a Given, so a reader of `kind: capability-proposal` files is needed (`workqueue` reads work-items only).

Size: `python3 .../tools size --limit 300` printed nothing (no tracked Python file over 300), so every room above is
`300 - lines`. The module map is CLAUDE.md's; the `scripts/tools` and `tests/scenarios` lines are as read.
