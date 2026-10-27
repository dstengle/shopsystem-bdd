# w211 plan: requests r25, r28-r34, r39-r45

Planned from `.shop/work/i39/runs/w211/1-research/notes.md`, `spec/capabilities/requests.md`, decisions 0055, 0067, 0071 and `features/requests.feature`. I read some files outside the notes, only where a decision needed them: `scripts/supervise_raise.py` (what it passes to `workqueue_request.request`), `features/supervision.feature:1444-1452`, `features/work-queue.feature:303-311`, and the Givens in `tests/scenarios/requests_write_steps.py`, `work_queue_request_steps.py` and `conftest.py` (the test repository's context id is `bounded-context/<PATH>`, not `ctx-a`).

**Status: QUESTION.** The plan stops where it needs the carrier of what is sent (Q1) and an answer on whether r28 binds supervision's raise (Q2). Every part that does not depend on them is planned below. Where a part does depend on them, it says so.

## 1. What goes green

All 26 accepted scenarios are red today. Each stops at its first Given with `StepDefinitionNotFoundError` (notes §1). The behaviour behind each gap comes from notes §2 and §6:

- **requests#r28**: "the asker <doing> from its own repository, with no checkout of the upstream's repository" (three rows: raising, answering, passing the turn). Red because every command writes into the caller's own root. A request the asker raises is kept in the asker's repository, and nothing reaches the upstream (probe A).
- **requests#r44**: "request with <given> writes an open request in the upstream's turn with the lines and asker given<and where from>, and prints its id" (two --source, --thread, --raised-for). Red for the same reason as r28 (probe A). The steps for the two-repository setup are also undefined.
- **requests#r29**: "request with --raised-for writes in the upstream's request the request it is raised for". `raised_for:` is already written (probe F), but only in the asker's own copy. The steps are undefined.
- **requests#r45**: "a request the upstream raises for itself with neither --source nor --thread is refused, and nothing changes". The refusal is already right (probe D). Only the Given "an upstream ctx-u…" is missing.
- **requests#r30**: "a request from another asker raised with --source is refused, and nothing changes". Red because `--source` with `--thread` is accepted and the sources are silently dropped (probe B).
- **requests#r31**: "a request from another asker raised with neither --raised-for nor --thread is refused, and nothing changes". Red because the message names only --source and --thread (probe C).
- **requests#r32**: "request raised from <role>'s repository giving the asker <given asker> is refused, naming the asker, and nothing changes" (asker ctx-a / ctx-b; product level p1 / ctx-a). Red because `--from` is taken unchecked (probe E).
- **requests#r33**: "a command writing <part> of <kind> in <where> writes it as the <side>'s part" (four rows). Red because the side is decided by the turn alone, never by the repository (probes L, M).
- **requests#r34**: "the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes". Red because the refusal is by turn only and its wording names the turn (probe G).
- **requests#r39**: "the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown>" (two rows). Red because there is no take-in command (probe I) and no carrier for what is sent.
- **requests#r40**: "run in an upstream's repository takes in what has been sent to it before its intake rounds start". Red because `supervise_intake.due` reads local requests only.
- **requests#r41**: "<sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why" (two rows). Red because there is no allow list and no take-in.
- **requests#r42**: "requests from repositories registered under different asker ids are taken in as different askers' requests". Red because there is no registry of asker ids.
- **requests#r43**: "<sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done" (title, answer text). Red because there is no take-in. A related defect: a title with a newline writes sections, and on its own sets a request accepted (probe J).
- **requests#r25**: "requests from another context, from the product level and from the upstream itself are each taken through the same work commands and the same statuses". Red because there is no take-in, and `work show <request>` is refused (probes H, I).

**Retired.** The work-item's Retires gives two titles. They are the scenarios tagged `@r1 @deprecated` (line 5) and `@r3 @deprecated` (line 109) in `features/requests.feature`. The capability lists r1 and r3 as `retired`. The work-item's "(requests @r44)" and "(requests @r45)" name the requirements each title is "Deprecated for", not the tags. So this is settled by the titles, and the researcher's tag question needs no ruling. Both stay deselected; nothing in this work runs them.

## 2. Where the change lands

The researcher's set, minus `scripts/workqueue.py`, plus the files the decisions below add:

- `scripts/workqueue_request.py`: the origin rule (r30), the wording for neither flag (r31), the side checks in `outcome`, `ask` and `reply` with the side read from the repository and a refusal naming the side that writes that part (r33, r34), and the asker check (r32), placed as D4 says.
- `scripts/work`: a take-in subcommand (r25, r39), `show <request>` routed to the request (r25), and the repository's own identity passed to the request commands (r32, r33).
- `scripts/workqueue_list.py`: `show` of a request, printing its status and whose turn it is (r25, r13).
- `scripts/supervise_intake.py` and `scripts/supervise.py`: the take-in run before the first intake round (r40). `supervise.py` has room for a call only.
- New module `scripts/workqueue_sent.py`: what an asker sends, and the upstream's take-in of requests and messages. It covers the allow list of asker ids (r39, r41, r42, decision 0071) and the reading of what is sent as fields only (r43). Its carrier waits on Q1.
- `scripts/supervise_raise.py`: changes only under Q2's reading B.
- `CLAUDE.md`: a row for the new module (the module map's rule).
- `tests/scenarios/requests_steps.py`, `tests/scenarios/requests_write_steps.py`, `tests/scenarios/requests_show_steps.py`: the two-repository Givens and the "the asker ctx-a runs … in its own repository" Whens, the side-less commands and the refusals that name a side or an asker, plus the rebinding in D6.
- New `tests/scenarios/requests_send_steps.py`: steps for what is sent, the listing, take-in and registration (r39-r43, r40, r25).
- `tests/scenarios/test_requests.py`: import the new step module.

Removed from the researcher's set: `scripts/workqueue.py`, which has room for 6 lines and needs no change. The helpers it already has (`requests`, `context_path`, `committed`) are read, not changed.

## 3. Decisions

- **D1. Retires.** Retire the two titles as tagged `@r1`/`@r3 @deprecated`. Rests on the work-item's Retires titles and the capability's `retired: [r1, r3]`.
- **D2. A request's sides.** The side that runs a command is the repository's relation to the request. If the repository is the request's upstream, it writes the upstream's part. If it is the asker named in the request, it writes the asker's part. If the asker is the upstream itself (an internal request), the one repository writes both parts, and the command decides which part, exactly as today. Rests on requests#r33 and r34, with r33 rows 3-4 for the internal case. The refusal names the side that writes the part ("the upstream writes line outcomes"), per r34. The turn check (r16) is kept after the side check.
- **D3. The repository's identity.** The asker check (r32) and the side (r33) compare against the repository's own id, read where `work add` already reads it (`workqueue.context_path`, from `spec/index.md`). `--from` passes when it equals that id. Rests on requests#r32 ("the bounded-context or product level whose repository raises"). The test repositories give their `spec/index.md` the ids ctx-a, ctx-u and p1.
- **D4. Order of refusals in `work request`.** The order is: empty delegation (r22), missing lines file (work-queue r7), strict form (r2), then asker (r32), origin (r30), and finally neither-flag (r31/r45), as one gate before any write. Rests on work-queue#r7 and requests#r2/r22, which are already pinned with an asker that D6 makes the upstream itself. With D6, no live scenario depends on this order. It is fixed only so that each refusal "changes nothing" (r30-r32). Which checks the function that supervision calls also runs waits on Q2.
- **D5. `work show <request>`.** A target naming a request kept here prints that request with its status and whose turn it is, the same line `work show` with no target prints for it. Rests on requests#r25 (show in the one set of commands) and r13.
- **D6. Live scenarios stay single-repository as internal requests.** The shared Givens "an upstream that keeps no request" (`requests_write_steps.upstream_keeps_none`, which `work_queue_request_steps` reuses) and "a request q1 from the asker ctx-a …" give the repository the id ctx-a. That makes these requests internal, so r19, r22, r2, r4, r5, r7, r8, r9, r10, r11, r12, r15-r18, r20, r21, r23, r24 and work-queue r7 keep running in one repository unchanged. Rests on requests#r30 (an origin belongs to an internal request, which is what `--from ctx-a --source o1` then is) and r33 rows 3-4. The accepted scenarios that name a distinct upstream ctx-u (r28, r33 rows 1-2, r34) build two repositories through their own Givens.
- **D7. Take-in is a `work` subcommand that `work run` also calls.** The upstream runs it in its own repository. It takes in everything sent before it began. It reads the carrier itself, never a listing of it (r39), and the listing the r39 steps set up may lag. It checks each item's registered asker id against the upstream's allow list, which is a setting of the upstream's repository (capability Implementation, decision 0071). It leaves the items that fail and prints each one with the asker id and the asker it named (r41). It writes each item through the same functions and checks `request`, `reply` and `turn` use, with each field written as a value and never as markup (r43, and notes §5 on the skipped checks). `work run` calls it before the first intake round (r40). Rests on requests#r39-r43 and decision 0071. **The carrier waits on Q1.**
- **D8. A zero-line lines file (probe K).** Behaviour unchanged. No accepted requirement or scenario of this work-item touches it, so no decision is taken here. A future request can raise it.

## 4. Tests the decisions break

- `features/requests.feature` r19, r22, r2 (in `test_requests.py`) and work-queue r7 "request with a --lines file that does not exist…" (`test_work_queue.py`, steps `work_queue_request_steps.py`). These run `--from ctx-a --source o1` in a repository whose id is `bounded-context/<PATH>`, so under D3, r32 and r30 they would be refused naming ctx-a. **D6 rebinds** "an upstream that keeps no request" to a repository with the id ctx-a. The scenario text is unchanged, and each keeps asserting what it asserts today.
- The live single-repository scenarios that use "a request q1 from the asker ctx-a…" (r4, r5, r7, r8, r9, r10, r11, r12, r15-r18, r20, r21, r23, r24, r13, r14). They run every side in one repository whose id is not ctx-a, so under D2 every command there would be the upstream's. **D6 rebinds** the Given to an internal request, and their assertions stay as they are.
- `tests/scenarios/supervision_raise_steps.py` (`request_run`, `request_raised`) and `features/supervision.feature:1445-1452` (supervision r135). `supervise_raise.raise_requests` calls `workqueue_request.request` with the upstream's root and this context's id as the asker. If r32 sits inside that function, the raise is refused. **What becomes of it waits on Q2.** Under reading A it is untouched. Under reading B its Then cannot hold until the upstream takes in, and the scenario is supervision's to reformulate.
- `tests/scenarios/supervision_done_steps.py`, `work_queue_start_steps.py`, `batch_measurement_request_steps.py`, `design_model_check_requests.py` and `tests/scripts/test_workqueue_list.py`. Each writes its own local request file, so by the notes (§4) they keep passing as long as the upstream's file form is unchanged. Under Q1's reading B (the asker keeps its own copy), `workqueue_done`'s reading of "requests this context asked" may move. Checking that waits on Q1.
- The `@r1`/`@r3 @deprecated` scenarios are deselected and retired (D1), and stay as they are.

## 5. Open cases (for the implementer to name, not choose)

- Title, answer or question text with a newline, at `work request` and at take-in (probe J). r43 settles take-in (fields only). Whether `work request` refuses such a title or keeps it as one field is not covered by any scenario.
- How the product level p1's repository is identified (r32 row 2, r25). Its `spec/index.md` id is assumed to be p1.
- One Given text, "a request q1 from the asker ctx-a…", is used both by the single-repository live scenarios (D6) and by r28, where later Givens name a distinct asker repository. The binding must serve both.
- A take-in that finds the same item sent twice, or an item for a request the upstream does not keep.
- A take-in that leaves some items and takes others: which exit it gives (decision 0055 allows only success or error).
- `work show <request>` for an id that is no request, initiative or work-item: the refusal's wording.

## Questions

- **Q1. The carrier of what an asker sends, and what each side sees before a take-in.** r28, r44 and r29 say "the upstream keeps" the request right after the asker's `work request`, with no checkout of the upstream's repository. r39 and r41 say it is kept only once taken in. r28 rows 2-3 and r33 row 1 have the asker answer, in its own repository, a question only the upstream wrote. Decision 0071 needs a "registered asker id" that the carrier carries.
  - Reading A, a git transport: the asker pushes each request or message to a ref under the upstream's remote, in a namespace named by its asker id, and fetches the upstream's requests to read questions. The upstream's `work list` shows nothing until take-in. "The upstream keeps" in r28/r44 is bound as "has been sent to and is in the upstream's repository's refs". The asker configures the upstream's remote, and the registry is the namespace.
  - Reading B, a drop directory: a shared directory, set in each repository's settings, with one subdirectory per registered asker id, where the asker also keeps its own copy of each request it raised. The upstream sees nothing in `work list` until take-in. The asker sees the upstream's questions only through what the upstream writes back to the drop.
  - In both readings the narrator observes a different setup to raise at all, and a different way the asker learns of a question.

- **Q2. Does r28 bind supervision's raise (r135)?**
  - Reading A, it does not: `work run` keeps writing a raised request directly into the upstream's checkout. The r30-r32 checks run in the `work request` command, not in the function supervision calls. Supervision's narrator sees no change, and `features/supervision.feature:1445-1452` stays green.
  - Reading B, it does: `work run` sends the raised request through the Q1 carrier like any asker. The request is in the upstream only after the upstream's take-in, `waits`/`arrived` read it through the carrier, and supervision r135's scenario ("the request it wrote in catalogue") must be reformulated by a supervision proposal before this work can go green.
