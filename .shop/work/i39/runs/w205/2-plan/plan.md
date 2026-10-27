# Plan of w205: `work list` and `work show <target>` (work-queue r34-r39)

Based on the research notes `.shop/work/i39/runs/w205/1-research/notes.md` (cited below as "notes §n").

## 1. What goes green

- **work-queue#r34**, "list prints each initiative, each request and each work-item under .shop/work/ with its status". It is red because the Given "an initiative i1 ... that is started, whose work-items w1 is drafted and w2 is ready" has no step, and `scripts/work` has no `list` subcommand (probe P-A: exit 2, "invalid choice: 'list'").
- **work-queue#r35**, "list with --json prints each initiative, request and work-item with its status as one JSON object". It is red because the Given "a request q1 under .shop/work/ that is accepted" has no step, and `list --json` does not exist (P-A).
- **work-queue#r39**, "list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered". It is red because the Given "a request q1 that i1 raised into the upstream ctx-up, which is accepted" has no step, and nothing prints a waiting line. Also, no record of a request raised into an upstream exists in this context. A request is kept only in its upstream's repository (requests Implementation; decision 0067), and its file has no upstream field (notes §2, §3). See the question in §3.
- **work-queue#r36**, "show of an initiative prints where it stands, for a session to start from". It is red because two steps are missing: the Given "an initiative i1 ... that is started, whose capability-proposal p1 is approved" and the Then "work prints i1's status as started". Also, `work show i1` is refused by argparse (P-A: "unrecognized arguments"). `work status i1` already prints this content (P-C).
- **work-queue#r37**, "show of a work-item prints its status and its open questions". It is red because the Given "i1's work-item w2 is awaiting-answer with the question ... not yet answered", on its own, has no step, and `show` takes no target (P-A).
- **work-queue#r38**, "show of <target> with --json prints its result as one JSON object" (examples i1 and w1). The Givens match. It is red because `work show <target> --json` exits 2, and the Thens "it gives <gives>", with their question clause, have no step (notes §1).
- **Deprecated scenarios retired:** none. w205 has no Retires section. The deprecated r3, r11, r16, r17 and r18 scenarios stay, and they must keep passing (see §3, D1 and D2).

## 2. Where the change lands

- `scripts/work`: adds a `list` subcommand with `--json`, and gives `show` an optional positional target. Both route to the new module. The no-target `show` keeps today's path (D1).
- `scripts/workqueue_list.py` (new): the new concern of listing the whole queue and showing one target. It reuses `workqueue.items`, `workqueue.requests` and `workqueue.find` (`entry` too), and `workqueue_status`'s initiative reading and rendering for an initiative target. `scripts/workqueue.py` is at 294 lines (notes §7), so no new code goes there.
- `CLAUDE.md`: one module-map row for `scripts/workqueue_list.py`. Per CLAUDE.md, a new concern gets a new module and a row.
- `tests/scenarios/work_queue_list_steps.py` (new): the missing Givens and Thens of the r34-r39 scenarios.
- `tests/scenarios/test_work_queue.py`: one import line for the new step module (282 lines, so there is room for it).
- `tests/scenarios/work_queue_status_steps.py`: only where an existing Given there (the "started"/plural work-items forms, or the question form) is better widened than duplicated. The implementer judges this (160 lines, with room).
- Depending on the answer to Q1 (§3, D5): a file may be added for the record of a request raised into an upstream, or a reader of the upstream's requests. No file is named until the answer comes.

The researcher's set loses these files, and why:
- `scripts/workqueue.py`: no change, and no room.
- `scripts/workqueue_status.py`: reused, not changed, because `status` stays (D2).
- `scripts/migrate_session.py`: the hook keeps `status`'s text (D2).
- `tests/scenarios/requests_show_steps.py`: requests r13 keeps the no-target `show` (D1).
- `features/work-queue.feature`: nothing is retired by this work-item.

## 3. Decisions

- **D1. `show` with no target keeps today's output.** It prints each work-item of every initiative and each request with its status and turn, and `--json` behaves as today. A target is optional. This rests on **requests#r13** ("When `work show` is run, `work` shall print each request with its status and whose turn it is"), which is not retired, and on w205 retiring nothing. As a result, the deprecated r3/r11 scenarios, the work-queue r7 UTF-8 scenario and requests r13 all keep passing.
- **D2. `work status` stays as it is.** Decision 0072 retires it, but w205 accepts only r34-r39 and has no Retires section. r16-r18 (deprecated), requests#r14 and migration-tools#r32 (the hook text) still rest on it. Removing it is later work.
- **D3. `show <initiative>` prints what `work status <initiative>` prints today.** That covers the status, proposals, work-items with their open questions, the checkout's branch and whether it is pushed, uncommitted and untracked files, the last ten ledger lines and the last `next:` line. The text output is the same render. It rests on **work-queue#r36** (its content is the deprecated r16's, word for word), and on r16's scenario steps for the branch Given, which r36 shares. With `--json`, the output is one JSON object for that initiative (**work-queue#r38**, decision 0058; its keys are Implementation).
- **D4. A target is resolved as follows.** A name that is an initiative under `.shop/work/` (checked by `workqueue.entry`, with `initiative.md` present) is shown as an initiative. Otherwise the name is resolved as a work-item id by `workqueue.find`, which refuses when there is no match or more than one. A target that is neither is refused, naming it, and nothing changes. This rests on **work-queue#r7**, **work-queue#r12** and design-decision/work-items-named-by-ids (a work-item id is unique across the queue). `show <work-item>` prints the work-item's status and each open question, open meaning past the answers, as `workqueue_status.parts` counts them (**work-queue#r37**). With `--json`, it prints one object of the work-item, its status and its questions (**r38**).
- **D5. r39's source of knowledge: not taken, put as Q1.** `work list` must know, for an initiative, each request it raised into an upstream and whether that request is `delivered`. Today this context keeps no record of it. The request is kept in the upstream's repository (requests Implementation, 0067), and `--raised-for`/supervision r135 are not built (notes §3; a search of `scripts/` finds no `raised`). How the record is kept changes what the narrator sees from `work list` once the upstream moves on. No requirement, design-decision or ruling settles it.
- **D6. `list` prints one line per initiative, request and work-item, each with its status.** Ended initiatives are included (**work-queue#r34**). With `--json`, it prints one object holding all three kinds (**work-queue#r35**, decision 0058). Requests are read from `.shop/work/requests/`, as `workqueue.requests` reads them.

## 4. Tests the decisions break

None. I checked the following from the notes (§3, §4):
- The no-target `show` tests stay valid under D1: the deprecated r3/r11 scenarios, the work-queue r7 "show refuses a file ... not UTF-8" scenario, requests r13 (`requests_show_steps.py:44`) and `work_queue_withdraw_steps.py:39`.
- The `status` tests stay valid under D2: deprecated r16-r18, requests r14 and migration-tools r32 (`migration_session_steps.py:85`).
- D3 and D4 add new paths only, and change no existing function's behaviour.

## 5. Open cases (for the implementer to name, not to choose)

- A request with no `turn` printing as `None` (D1, notes §6), and a work-item with no status printing as `None` (D2 of the notes), in `list` and `show`.
- `list` on an empty `.shop/work/`. Under decision 0058, an empty result exits successfully.
- `show q1`, a request as target. Decision 0072 names it, but no accepted requirement here does.
- A name that is both an initiative directory and a work-item id.
- `show <initiative>` on a detached HEAD (P-D: branch `None`). Also: r36 says "the initiative branch", while today's render gives the checkout's current branch. The r36 scenario's Given is r16's, so the scenario does not tell the two apart.
- A non-UTF-8 file under `.shop/work/` met by `list` or `show <target>` (P-F's refusal today, by the no-target `show`).
- The order of lines in `list`, and how the waiting line of r39 sits beside the initiative's own line.
