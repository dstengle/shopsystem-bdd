# w211 plan: requests r25, r28-r34, r39-r45

Planned from `.shop/work/i39/runs/w211/1-research/notes.md`, the earlier plan `2-plan/plan.md` (which stopped on two questions), the work-item's Answers (2026-10-27), `spec/capabilities/requests.md`, decisions 0055, 0067, 0071 and `features/requests.feature`. Outside the notes I read `scripts/supervise_raise.py:1-50` (what the raise passes to `workqueue_request.request`), `supervise_brief.upstreams` (upstreams are read from `spec/index.md`'s `## Upstreams`), and searched `tests/`, `features/` and `scripts/` for every run of `work request` and every caller of `workqueue_request.request`. This plan takes over 2-plan's D1-D8. The work-item's Answers now settle its two questions.

## 1. What goes green

The notes (§1) report that all 26 accepted scenarios in `tests/scenarios/test_requests.py` are red today. Each one stops at its first Given (`StepDefinitionNotFoundError`). The behaviour behind each, from notes §2 and §6:

- **requests#r28**: "the asker <doing> from its own repository, with no checkout of the upstream's repository" (raising, answering, passing the turn). Every command writes into the caller's own root, and nothing reaches the upstream (probe A).
- **requests#r44**: "request with <given> writes an open request in the upstream's turn with the lines and asker given<and where from>, and prints its id" (three rows). Red for the same reason as r28, and the two-repository steps are undefined.
- **requests#r29**: "request with --raised-for writes in the upstream's request the request it is raised for". `raised_for:` is written, but only into the asker's own copy (probe F).
- **requests#r45**: "a request the upstream raises for itself with neither --source nor --thread is refused, and nothing changes". The refusal is already right (probe D). Only the Given is missing.
- **requests#r30**: "a request from another asker raised with --source is refused, and nothing changes". `--source` with `--thread` is accepted, and the sources are silently dropped (probe B).
- **requests#r31**: "a request from another asker raised with neither --raised-for nor --thread is refused, and nothing changes". The message names only --source and --thread (probe C).
- **requests#r32**: "request raised from <role>'s repository giving the asker <given asker> is refused, naming the asker, and nothing changes" (two rows). `--from` is not checked (probe E).
- **requests#r33**: "a command writing <part> of <kind> in <where> writes it as the <side>'s part" (four rows). The side comes from the turn alone (probes L, M).
- **requests#r34**: "the asker writing a line outcome of a request from another context is refused, naming the upstream, and nothing changes". The only refusal is by turn, and it names the turn (probe G).
- **requests#r39**: "the upstream taking in what has been sent takes in every request and message sent before, when a listing of what has been sent shows <shown>" (two rows). There is no take-in and no carrier (probe I).
- **requests#r40**: "run in an upstream's repository takes in what has been sent to it before its intake rounds start". `supervise_intake.due` reads only local requests.
- **requests#r41**: "<sent> from a repository registered under an asker id the upstream does not allow for its asker is left untaken, and the upstream is told which and why" (two rows). There is no allow list and no take-in.
- **requests#r42**: "requests from repositories registered under different asker ids are taken in as different askers' requests". There is no registry of asker ids.
- **requests#r43**: "<sent> whose <field> is written as an instruction is taken in as that field, and nothing it says is done" (two rows). There is no take-in. Related defect: a title with a newline writes sections, and on its own sets the request to accepted (probe J).
- **requests#r25**: "requests from another context, from the product level and from the upstream itself are each taken through the same work commands and the same statuses". There is no take-in, and `work show <request>` is refused (probes H, I).

**Retired:** "request with <given> writes an open request in the upstream's turn with the lines, asker and <where from> given, and prints its id (deprecated)" and "request with neither --source nor --thread is refused, and nothing changes (deprecated)". These are the scenarios tagged `@r1 @deprecated` and `@r3 @deprecated` in `features/requests.feature`, and the capability lists r1 and r3 as `retired`. The researcher asked about the work-item's "(requests @r44)" and "(requests @r45)". These name the requirement each title is "Deprecated for", not a tag, so the titles settle it (D1). Both scenarios stay deselected.

## 2. Where the change lands

- `scripts/workqueue_request.py`: the side checks in `outcome`, `ask` and `reply`, with the refusal naming the side that writes that part (r33, r34; D2). The origin rule, the wording for neither flag and the asker check go in a gate the command runs before any write (r30-r32; D4). `request` itself keeps writing into the root it is given (D9).
- `scripts/work`: the `take-in` subcommand (D7). `request`, `reply` and `turn` in an asker's repository go through the carrier (D10). `show <request>` (D5). The repository's own id is given to the request commands (D3).
- `scripts/workqueue_list.py`: `show` of a request (D5).
- New `scripts/workqueue_sent.py`: the asker's side of the carrier. It reads the request settings, sends a request, an answer or a turn to the asker id's namespace on the upstream's remote, and reads the upstream's published requests (D10, D11).
- New `scripts/workqueue_takein.py`: the upstream's side. It covers the take-in, the allow list, a request's publication after each change, and reading what is sent as fields only (D7, D11, D12). It is split from `workqueue_sent.py` so that each module stays under 300 lines.
- `scripts/supervise.py` and `scripts/supervise_intake.py`: the take-in before the first intake round (r40; D13). `supervise.py` has room for one call only, so any further logic goes in `supervise_intake.py`.
- `CLAUDE.md`: one row each for `workqueue_sent.py` and `workqueue_takein.py` (the module map's rule).
- `tests/scenarios/requests_steps.py`, `requests_write_steps.py`, `requests_show_steps.py`: the two-repository Givens, the Whens that run a command "in its own repository" or with "giving no side", and the refusals that name a side or an asker. Also the rebinding of the shared single-repository Givens (D6).
- New `tests/scenarios/requests_send_steps.py`: the bare remote, the repositories registered under asker ids, the allow list, what is sent, the listing, the take-in and its report (r39-r43, r40, r25). More new step modules may be added if the 300 limit needs them.
- `tests/scenarios/test_requests.py`: import the new step modules.

Changes from the researcher's set:
- `scripts/workqueue.py` is removed. It has room for 6 lines, and what it already has is read, not changed.
- `scripts/supervise_raise.py` is removed. The Answer keeps the raise as it is (D9).
- Added: the two new production modules, the new step module and `CLAUDE.md`.

## 3. Decisions

- **D1. Retires.** The two retired titles are the `@r1` and `@r3 @deprecated` scenarios. Rests on the work-item's Retires titles and the capability's `retired: [r1, r3]`.
- **D2. Sides.** The side is the repository's relation to the request. Rests on requests#r33 and #r34 (r33 rows 3-4 for the internal case) and keeps r16 after the side check.
  - A repository that keeps a request whose asker is another context or the product level is that request's upstream. There, `reply` is refused, naming the asker as the side that writes answers.
  - A repository that reads the request from its upstream (D10) is the asker. There, `outcome`, `ask` and `resolve` are refused, naming the upstream as the side that writes that part.
  - For an internal request (its asker is the repository's own id, or `internal`), the one repository writes both parts, and the command decides which part, as today.
  - The turn check (r16) still runs, after the side check.
- **D3. The repository's id.** The repository's id is read from `spec/index.md`, where `work add` already reads it (`workqueue.context_path`). r32 refuses a `--from` that is not this id, naming the `--from` given. Rests on requests#r32. The test repositories' `spec/index.md` give the ids ctx-a, ctx-b, ctx-u and p1.
- **D4. The gate of `work request`, in this order:**
  1. empty delegation (r22)
  2. missing lines file (work-queue r7)
  3. strict form (r2)
  4. asker (r32)
  5. origin (r30: `--source` on a request to an upstream)
  6. neither flag (r31 wording for a request to an upstream, r45 wording for an internal one)

  All of these run before anything is written or sent. Rests on requests#r22, #r2, #r30-r32 and #r45, and on work-queue#r7 ("change nothing").
- **D5. `work show <request>`.** For a request kept here, it prints the request with its status and whose turn it is, the same line `work show` with no target prints for it. In an asker's repository, it prints the upstream's published request. Rests on requests#r25 and #r13.
- **D6. Live single-repository scenarios stay internal.** The shared Givens "an upstream that keeps no request" (also used by `work_queue_request_steps`) and "a request q1 from the asker ctx-a …" give their one repository the id ctx-a and no upstream setting. Their requests are then internal requests of ctx-a. Rests on requests#r33 rows 3-4 and #r30. r19, r22, r2, r4, r5, r7-r12, r15-r18, r20, r21, r23, r24 and work-queue r7 keep asserting what they assert today. This also settles the researcher's work-queue r7 conflict: the repository is ctx-a with no upstream, so `--from ctx-a --source o1` is internal, and the missing file is what refuses it.
- **D7. Take-in is `work take-in`.** The command is named for r25's "take in". The upstream runs it in its own repository. Rests on requests#r25, #r39, #r41-r43 and decision 0071.
  - At its start it fetches every asker-id namespace from its remote. It never relies on a listing it already has: the step "a listing of what has been sent … shows" is bound to the upstream's local copy of the remote's refs, which may lag (r39).
  - It takes in each item in the order it was sent: a request, then the answers and turns on it.
  - It checks each item against the allow list: is the asker the item names allowed for the namespace's asker id (r41, r42)? It leaves any item that fails, and prints one line for each, naming the item, the asker id and the asker (r41's wording).
  - It writes each item it takes through the same functions and gate that `request`, `reply` and `turn` use. So the strict form, the delegation, the turn and the side checks all hold at take-in (notes §5).
  - An item it has taken is not taken again. An item it left stays sent.
  - With no request settings, the take-in takes nothing and succeeds.
- **D8. A zero-line lines file (probe K).** Unchanged. No accepted requirement or scenario of this work-item touches it.
- **D9. Supervision's raise is unchanged.** `supervise_raise.raise_requests` keeps calling `workqueue_request.request` straight into the upstream's checkout. The gate of D4 and the carrier of D10 run only in the `work request` command, never in that function. `features/supervision.feature:1445-1452` stays green. This is the work-item's Answer (Reading A, "no"). Sending the raise through the carrier is a follow-up, as the ledger of 2026-10-27 records.
- **D10. The carrier is git, on the upstream's remote.** Rests on the work-item's Answer (carrier Reading A), requests#r28, #r42 and decision 0071.
  - An asker's repository has a request setting naming its upstream's remote and the asker id it is registered under.
  - There, `work request`, `reply` and `turn` push what they write to the namespace of that asker id on that remote. They make no clone and no worktree of the upstream (r28's "no checkout").
  - The asker reads the upstream's requests (their questions and turns) only by fetching them from that remote.
  - Before a take-in, the upstream's `work list` shows nothing that has been sent.
  - In r28, r44 and r29, "the upstream keeps" a request or an answer, and in r30-r32 "keeps no request": both are bound to what is on the upstream's remote in that namespace, together with what the upstream's repository keeps.
  - `work request` in an asker's repository numbers the request one above every request it can see on the remote (published and sent), and prints that id. It is the id the upstream keeps it under at take-in.
- **D11. Where the settings are kept.** Both sides' settings are in `.shop/requests.toml`. Rests on the capability's Implementation ("a setting of the upstream's repository") and decision 0071.
  - In an asker's repository: the upstream's remote and the asker id.
  - In an upstream's repository: its remote, and the allow list, which maps each asker id to the askers it is allowed for.
  - The namespace an asker pushes to is its registration.
  - A repository with neither setting behaves as today.
- **D12. Publishing.** After each command or take-in that changes a request whose asker is another context or the product level, the upstream pushes that request to its remote under a ref of its own, so that the asker can read it. Each push is one turn of the conversation. Internal requests are never pushed. Rests on the Answer ("fetches the upstream's requests to read its questions") and requests#r28 rows 2-3 and #r33 row 1.
- **D13. `work run` takes in first.** In an upstream's repository, `work run` runs the take-in of D7 before it chooses its first intake round. Rests on requests#r40.

## 4. Tests the decisions break

- **requests r19, r22, r2 (`test_requests.py`) and work-queue r7 "request with a --lines file that does not exist…" (`test_work_queue.py`, `work_queue_request_steps.py`).** These are the only live runs of `work request` outside the accepted scenarios. They run `--from ctx-a` in a repository whose id comes from conftest (`bounded-context/<PATH>`), so under D3 they would be refused. D6 rebinds "an upstream that keeps no request" to a repository with the id ctx-a. Each keeps its text and its assertions. If one of them asserts a request id that holds the context path, it now reads the ctx-a path.
- **The live scenarios that use "a request q1 from the asker ctx-a …" (r4, r5, r7-r12, r15-r18, r20, r21, r23, r24, r13, r14).** Under D2, every asker-side command run in a repository that keeps a request from another context would be refused. D6 makes these requests internal, so the assertions stay as they are.
- **`supervision_raise_steps.py` and `features/supervision.feature:1445-1452`.** Not broken. Under D9 the function the raise calls keeps its behaviour. The supervision intake steps (`supervision_intake_steps.py`, `supervision_then_faults_steps.py`) run `outcome`, `ask` and `turn` only as the upstream, on requests kept in their own repository, which D2 allows.
- **`supervision_done_steps.py`, `work_queue_start_steps.py`, `batch_measurement_request_steps.py`, `design_model_check_requests.py`, `tests/scripts/test_workqueue_list.py`.** Not broken. Each writes a local request file in the form the upstream keeps, and D10-D12 leave that form and its place unchanged. None runs `reply`.
- **`@r1` and `@r3 @deprecated`.** Deselected and retired (D1). They stay as they are.

## 5. Open cases (for the implementer to name, not choose)

- A title, question or answer text with a newline (probe J), at `work request` and at take-in. r43 settles that what is taken in is read only as fields. No scenario says whether such a text is refused or kept as one field.
- A repository with more than one upstream, or one that has an upstream setting and also raises an internal request. Under D10 every `--from <own id>` request there is sent.
- At take-in: a sent request whose id the upstream already keeps (two askers numbering at once), an answer or turn on a request the upstream does not keep, and an item whose named asker is not the request's asker.
- When a take-in leaves some items: its exit status. Decision 0055 allows only success or an error, and r41's scenario does not say which.
- A push or fetch that fails, at the asker's commands, at publishing (D12) and at take-in.
- An asker that answers or passes the turn again before the upstream has taken in its last message.
- The shared Given "a request q1 from the asker ctx-a …" serves both the internal scenarios (D6) and r28/r33/r34, where later Givens name a distinct upstream ctx-u. Its binding must serve both.
- `work show <id>` for an id that is no request, initiative or work-item: the refusal's wording.
