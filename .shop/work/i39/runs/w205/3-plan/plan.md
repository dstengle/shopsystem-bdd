# Plan of w205: `work list` and `work show <target>` (work-queue r34-r39)

From the research notes `.shop/work/i39/runs/w205/1-research/notes.md` ("notes §n"). This plan takes over the plan of stage 2 (`.shop/work/i39/runs/w205/2-plan/plan.md`) and settles its one question, r39, with the answer of 2026-10-27 in w205's `## Answers` (reading A).

## 1. What goes green

- **work-queue#r34**, "list prints each initiative, each request and each work-item under .shop/work/ with its status". Red: the Given "an initiative i1 ... that is started, whose work-items w1 is drafted and w2 is ready" has no step, and `scripts/work` has no `list` subcommand (probe P-A: exit 2, "invalid choice: 'list'").
- **work-queue#r35**, "list with --json prints each initiative, request and work-item with its status as one JSON object". Red: the Given "a request q1 under .shop/work/ that is accepted" has no step, and `list --json` does not exist (P-A).
- **work-queue#r39**, "list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered". Red: the Given "a request q1 that i1 raised into the upstream ctx-up, which is accepted" has no step; nothing prints a waiting line; and this context keeps no record of a request it raised (notes §2, §3).
- **work-queue#r36**, "show of an initiative prints where it stands, for a session to start from". Red: the Given "... that is started, whose capability-proposal p1 is approved" and the Then "work prints i1's status as started" have no step, and `work show i1` is refused by argparse (P-A). `work status i1` prints this content today (P-C).
- **work-queue#r37**, "show of a work-item prints its status and its open questions". Red: the Given "i1's work-item w2 is awaiting-answer with the question ... not yet answered", standing alone, has no step, and `show` takes no target (P-A).
- **work-queue#r38**, "show of <target> with --json prints its result as one JSON object" (examples i1, w1). The Givens match. Red: `work show <target> --json` exits 2, and the Thens "it gives <gives>" with their question clause have no step (notes §1).
- **Deprecated scenarios retired:** none. w205 has no Retires section. The deprecated r3, r11, r16, r17 and r18 scenarios stay and keep passing (D1, D2).

## 2. Where the change lands

- `scripts/work`: a `list` subcommand with `--json`, and an optional positional target for `show`. Both go to the new module. `show` with no target keeps today's path (D1).
- `scripts/workqueue_list.py` (new): listing the whole queue, reading the record of raised requests (D5), and showing one target. It reuses `workqueue.items`, `workqueue.requests`, `workqueue.entry` and `workqueue.find`, and `workqueue_status`'s reading and rendering of an initiative. Nothing new goes in `scripts/workqueue.py`: it is at 294 lines (notes §7).
- `CLAUDE.md`: one module-map row for `scripts/workqueue_list.py` (a new concern gets a new module and a row).
- `tests/scenarios/work_queue_list_steps.py` (new): the missing Givens and Thens of r34-r39. That includes the r39 Given, which writes the record of D5 directly, since no command writes it yet.
- `tests/scenarios/test_work_queue.py`: one import line for the new step module (282 lines, room for it).
- `tests/scenarios/work_queue_status_steps.py`: changed only where widening an existing Given (the "started" or plural work-items forms, or the question form) is better than writing a second one. The implementer judges this (160 lines).

Files the research set had that this plan drops, and why:
- `scripts/workqueue.py`: no room; reused unchanged.
- `scripts/workqueue_status.py`: reused unchanged, because `status` stays (D2).
- `scripts/migrate_session.py`: the hook keeps `status`'s text (D2).
- `tests/scenarios/requests_show_steps.py`: requests r13 keeps the no-target `show` (D1).
- `features/work-queue.feature`: this work-item retires nothing.

D5 adds no file to the repository's code. The record is a data file the r39 step writes in the test's own `.shop/work/`.

## 3. Decisions

- **D1. `show` with no target keeps today's output** (each work-item of every initiative and each request with its status and turn; `--json` as today). The target is optional. Rests on **requests#r13**, which is not retired and runs `work show` with no target, and on w205 retiring nothing. The deprecated r3/r11 scenarios, the work-queue r7 UTF-8 scenario and requests r13 all keep passing.
- **D2. `work status` stays as it is.** Decision 0072 retires it, but w205 accepts only r34-r39 and has no Retires section. The deprecated r16-r18 scenarios, requests#r14 and migration-tools#r32 (the hook text) still rest on it. Removing it is later work.
- **D3. `show <initiative>` prints what `work status <initiative>` prints today**, through the same reading and rendering. Rests on **work-queue#r36**, whose content is the deprecated r16's word for word, and its scenario shares r16's Givens. With `--json`, the output is one JSON object for that initiative (**work-queue#r38**, decision 0058). Its keys are Implementation.
- **D4. Resolving a target.** A name that `workqueue.entry` accepts and that is an initiative directory with `initiative.md` is shown as an initiative. Any other name is resolved as a work-item id by `workqueue.find`, which refuses when nothing matches or more than one does. A name that is neither is refused, naming it, and nothing changes. Rests on **work-queue#r7**, **work-queue#r12** and design-decision/work-items-named-by-ids. `show <work-item>` prints the work-item's status and each open question, open meaning past the answers, counted as `workqueue_status` counts them (**work-queue#r37**). With `--json`, one object of the work-item, its status and its questions (**r38**).
- **D5. r39 reads this context's own record of the requests it raised, and only that.** This follows w205's answer of 2026-10-27 (reading A), taken as a ruling. Each entry gives the upstream, the request's id there (its local `q<n>`), the initiative it was raised for, and its last known status. `work list` never reaches the upstream and never fails because the upstream cannot be reached. The rest is Implementation:
  - The record is `.shop/work/<initiative>/raised.jsonl`, one JSON object a line, beside `log.jsonl`.
  - Where the same upstream request appears on more than one line, the last line gives its status.
  - The file is not Markdown, so `model` (which reads an initiative's `*.md` files as parts, `scripts/model_work.py`) and `workqueue.items` both pass over it, as they pass over `log.jsonl`. A directory of its own under `.shop/work/` would be read by `model` as an initiative with no `initiative.md`, so it is not used.
  - An entry names the upstream by its name and the request by its `q<n>`, not by a full id with the upstream's context path. This keeps it clear of design-model-check r121 (v18), which is still open.
- **D6. The raised request is not one of `list`'s requests.** Under D5 it appears only on its initiative's waiting line, never as a request line of r34/r35. Rests on the ruling (reading C, a copy in `.shop/work/requests/`, was set aside as contradicting decision 0067) and on **work-queue#r34**, which lists the requests kept in this context. For the same reason, r23's done is not affected by the record.
- **D7. `list` prints one line for each initiative, each request in `.shop/work/requests/` and each work-item, each with its status**, ended initiatives included (**work-queue#r34**). For each initiative it also prints a waiting line for each entry in its record whose last status is not `delivered` (**work-queue#r39**). With `--json`, the output is one object holding the three kinds (**work-queue#r35**, decision 0058).

## 4. Tests the decisions break

None. What was checked, from the notes (§3, §4) and the files above:
- Under D1, the no-target `show` tests stay valid: deprecated r3/r11, work-queue r7 "show refuses a file ... not UTF-8", requests r13 (`requests_show_steps.py:44`) and `work_queue_withdraw_steps.py:39`.
- Under D2, the `status` tests stay valid: deprecated r16-r18, requests r14, and migration-tools r32 (`migration_session_steps.py:85`).
- D5 adds a file kind that `model` and `workqueue.items` do not read, so no model-check or show test sees it. Only the r39 step writes the file.
- D3, D4 and D7 add new paths and change no existing function's behaviour.

## 5. Open cases (for the implementer to name, not to choose)

- No command writes `raised.jsonl` yet: requests#r29 `--raised-for` and supervision#r135 are not built. Nor does any command update the last known status. Until one does, the record is written by hand or by tests.
- `raised.jsonl` with a line that is not JSON, or that lacks a field. Under r7 a refusal is the nearest case.
- Whether the waiting line names the upstream (ctx-up) and the request's status beside q1. The scenario checks only "i1 as waiting on q1".
- Whether, and how, `list --json` carries the waiting of r39. r39's scenario runs text only.
- A request with no `turn` printing as `None` (notes D1), and a work-item with no status printing as `None` (notes D2), in `list` and `show`.
- `list` on an empty `.shop/work/`. Under decision 0058, an empty result exits successfully.
- `show q1`, a request as the target. Decision 0072 names it; no requirement accepted here does.
- A name that is both an initiative directory and a work-item id.
- `show <initiative>` on a detached HEAD (P-D: branch `None`). r36 says "the initiative branch" while today's render gives the checkout's current branch, and the scenario's Given does not tell the two apart.
- A non-UTF-8 file under `.shop/work/` met by `list` or `show <target>` (P-F).
- The order of lines in `list`, and where the waiting line sits beside its initiative's line.
