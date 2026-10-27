# w211 research notes: requests (r25, r28-r34, r39-r45)

Method: work-item `.shop/work/i39/w211.md`, `spec/capabilities/requests.md`, 26 accepted scenarios in `features/requests.feature`, run as `tests/scenarios/test_requests.py` (node ids from `--collect-only`). No `fileset:` in the work-item or brief; started from the scenarios. Tools: `refs` and `tests-of` (map at 068650ac), `size`. Probes in `.shop/scratch/w211-1-research/probe_requests.py`.

**Mistake, disclosed:** I ran `tools map --json` once (not `tests-of`). Its output (`commit 068650ac, tests 154`) suggests it ran the suite under coverage, which the brief forbids. The map files are under the worktree's ignored `.shop/scratch/tools`. Nothing else was run beyond the 26 scenarios' file and my probes.

**Limit of `tests-of`:** every request function returns `none`. The scenario tests reach `scripts/work` by subprocess, which the map does not follow. Test columns below say `by search` or `none (map)`.

**Blocked:** `tests/scenarios/test_work_queue.py` cannot be collected here: the `--work-item w211` plugin refuses it ("w211 accepts none of the scenarios it collected"). Its claims are `read` only.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -n 0 --tb=line tests/scenarios/test_requests.py` (run; 26 failed). All 26 stop at their first Given (`StepDefinitionNotFoundError`), so no Then runs. Later steps: `read`.

| scenario (feature line) | first undefined step (run) | other gaps (read) | code behind it (read) |
|---|---|---|---|
| r28 raising, answering, passing turn (24) | Given "a file lines.md ... in the asker ctx-a's repository" (28) | "the asker ctx-a's repository has no checkout..." (29); "work made no checkout..." (32) | `workqueue_request.request` writes into the caller's own root (`workqueue_request.py:103-117`); asker's `reply`, `turn` likewise |
| r44 three rows (42) | Given "an upstream ctx-u that keeps no request" (44) | "the asker ctx-a keeps a request q7 ..." (45); "its lines are the two lines of lines.md" (49, only the `and its asker is ctx-a` form is defined); "its asker is ctx-u/ctx-a" (52); "the asker ctx-a runs" (47, only `the asker runs` is defined) | origin forms accepted (`workqueue_request.py:95-107`); asker's writes land in the asker's root (probe A) |
| r29 --raised-for (61) | Given "an upstream ctx-u" (63) | "it names q7 as the request it is raised for" (68) undefined | `raised_for:` written (`workqueue_request.py:107`); probe F |
| r45 upstream, neither flag (121) | Given "an upstream ctx-u" (123) | none: the When, Then, "keeps no request" are defined | refusal already right (probe D) |
| r30 asker with --source (131) | Given "an upstream ctx-u" (133) | "the asker ctx-a runs ..." (135); "refused because an origin belongs to an internal request" (136) | no such check (`workqueue_request.py:95-107`); probe B |
| r31 asker, neither flag (141) | Given "an upstream ctx-u" (143) | "the asker ctx-a runs" (145); "...neither a request it is raised for nor a job-thread" (146) | message names --source and --thread only (`workqueue_request.py:96`); probe C |
| r32 two rows (150) | Given "an upstream ctx-u" (153) | "the asker ctx-a / the product level p1 runs" (155); "refused, naming <given asker>" (156) (the only refusal step is hard-wired to "line 2") | no asker check against the repository (`workqueue_request.py:87`, `scripts/work:146`); probe E |
| r33 four rows (165) | Given "a request q1 to the upstream ctx-u from the asker ..." (168) | "<command> in <where>, giving no side" (170); "q1 holds <written> as the <side>'s part" (171) | `outcome`, `ask`, `reply` take no side from the repository (`workqueue_request.py:121-146`); probes L, M |
| r34 asker writes outcome (180) | Given "a request q1 to the upstream ctx-u ..." (183) | "the command is refused, naming the upstream as the side that writes line outcomes" (186) | refusal is by turn only (`workqueue_request.py:125`); probe G |
| r39 two rows (352) | Given "the upstream ctx-u keeps a request q2 ..." (355) | "the asker ctx-a has sent ctx-u a request q1 ..." (357); "a listing of what has been sent ... shows" (358); "the upstream takes in what has been sent to it" (359) | no take-in command (probe I); no sent-carrier in code (search: `sent`, `inbox`, `registered`, `asker id` in `scripts/`: none) |
| r40 intake before rounds (335) | Given "a request q1 that the asker ctx-a has sent ..." (338) | "ctx-u had taken in q1 when work run started its first round of the kind intake" (340); "that round is given q1" (341) | `supervise_intake.due` reads local requests only (`supervise_intake.py:18-20`); `supervise.run` not read |
| r42 two asker ids (343) | Given "a repository registered under the asker id id-a ..." (346) | "the upstream takes in ..." (348); "ctx-u keeps q1 from the asker ctx-a" (349) | none: no asker-id registry (decision 0071 accepted; search of `scripts/` and `spec/` finds no list) |
| r41 two rows (370) | Given "the upstream ctx-u keeps a request q2 ..." (372) | "a repository registered under the asker id id-x ..." (374); "work tells the upstream it left ..." (377); `<untaken>` steps (376) | none |
| r43 two rows (385) | Given "the upstream ctx-u keeps a request q2 ..." (387) | "the asker ctx-a has sent ctx-u <sent>, whose <field> reads ..." (389); "<kept>" (391); "q2's status is as it was" (393) | title written as heading with no newline check: a newline lands sections (probe J) |
| r25 (421) | Given "an upstream ctx-u" (423) | "a file lines.md with one line ... in each of the repositories" (424); the three-party When table (425); "each step exits successfully for each of the three requests" (438); the statuses and turns (440-442) | no take-in command; `work show <request>` refused (probes H, I) |

## 2. What the system answers today

Probe file: `.shop/scratch/w211-1-research/probe_requests.py`. Each run as `python3 -m pytest -q -s -n 0 -p no:warnings -p no:cacheprovider .shop/scratch/w211-1-research/probe_requests.py -k probe_<x>` (`run`). Repositories are built in scratch; the `work` script is run by its absolute path from the worktree.

- **A (r28, r44): asker's raise.** asker ctx-a, repo ctx-a, `request "Show the queue" --from ctx-a --lines lines.md --thread t1`. Returned `rc=0 out='q1'`. The file landed in the asker's own `.shop/work/requests/q1.md` with `id: request/ex.com/prod/ctx-a/q1`, `part_of: t1`, `turn: upstream`. Nothing is written to any upstream. (run)
- **B (r30): asker with --source and --thread.** `--from ctx-a --source o1 --thread t1`. `rc=0 out='q1'`; only `part_of: t1` written; `o1` silently dropped. (run)
- **C (r31): asker, neither flag.** `rc=1`, stderr `the request names neither an origin (--source) nor a job-thread (--thread)`. No `raised-for` mention. Nothing kept. (run)
- **D (r45): upstream, neither flag.** Same refusal, `rc=1`, nothing kept. Already right. (run)
- **E (r32): ctx-a's repo, `--from ctx-b --thread t1`.** `rc=0`, `asker: ctx-b` written. (run)
- **F (r29): `--raised-for q7`.** `rc=0`; frontmatter shows `raised_for: q7`, `asker: ctx-a`. (run)
- **G (r34): asker runs `outcome q1 1 accepted` in its own turn.** `rc=1`, stderr `q1 is in the asker's turn; the upstream writes a line outcome only in its own turn`. File unchanged. (run)
- **H (r25): `work show q1`.** `rc=1`, stderr `q1 is a request, not a work-item or an initiative that work show shows`. `work show` with no target: `rc=0`, `q1 open upstream`. (run)
- **I (r39-r43, r25): a take-in command.** `work take` and `work intake` both `rc=2`, invalid choice. Subcommands: add, list, show, withdraw, run, retry, answer, note, status, request, outcome, ask, reply, turn, resolve, start. None takes in. (run)
- **J (r43): title with a newline.** Title `"x\n## Outcomes\n1. accepted"`, one-line lines file, `--thread t1`. Written; the file's `## Outcomes` holds `1. accepted` before `## Lines`. Then `work turn q1` (upstream's turn): `rc=0`; afterwards `status: accepted`, `turn: upstream`. A title alone set the request accepted. (run)
- **K (nearest case): empty lines file.** `rc=0 out='q1'`; request with no lines written. Spec gives no rule (see questions). (run)
- **L (r33, r34): asker's repo, outcome in the upstream's turn.** `outcome q1 1 accepted`, turn upstream. `rc=0`; `1. accepted` written by the asker's root. No side check. (run)
- **M (r33, r34): upstream's repo, reply in the asker's turn.** `reply q1 1 "The work queue"`, turn asker. `rc=0`; answer written by the upstream's root. (run)

Read, not run:
- The Given of each r39-r43 row says the upstream "has not taken in" what was sent. No command or file exists for "sent" (see §1), so no nearest case of that is runnable.
- `resolve` with a request not accepted is refused (`workqueue_request.py:171-172`). Not run.

## 3. Old assumptions

The code keeps every request in the caller's own `root`. The asker and upstream are the same repository, and a request's turn decides the side, not the repository.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `workqueue_request.py:request` (87-118) | writes `q<n>` into `root`'s requests dir and commits there | asker writes from its own repo; upstream keeps it (r28, r44) | none (map); by search: `requests_steps`, `requests_write_steps` (red) | read; probe A |
| `workqueue_request.py:outcome`, `ask`, `reply`, `turn`, `resolve` (121-187) | act on `root`'s copy; side decided by turn only | side must come from the repository the command runs in (r33, r34) | none (map); by search: `requests_write_steps` (red) | read; probes G, L, M |
| `workqueue_request.py:path_of` (20-24) | reads `root`'s `requests/<id>.md` only | a request sent to an upstream is not in the asker's root | none (map) | `refs`: 5 refs (`measure_write.py`, `workqueue_request.py`, `workqueue_start.py` read) |
| `workqueue_request.py:asked_here` (40-54) | lists requests of this context awaiting the asker | no refs; unused | none | `refs`: 0 references |
| `workqueue_request.py:accepted_lines` (32-37) | line numbers accepted | no refs; unused | none | `refs`: 0 references |
| `workqueue.py:requests` (117-124) | lists `root`'s requests | sent but untaken requests are not listed; take-in must precede | none (map); by search: `tests/scripts/test_workqueue_list.py:25` (in-process, not in map) | read; `scripts/work:41,46`, `workqueue_list.py:42`, `supervise_intake.py:20`, `supervise_all.py:24`, `workqueue_request.py:48` |
| `workqueue_done.py:33-36`, `naming` (65-71) | `done` reads this root's requests, asker `internal` or this context | the asker's request is not in its own root after r28 | none (map); by search: `tests/scenarios/supervision_done_steps.py:46` | read |
| `workqueue_start.py:26` | `start` reads `root`'s request file | an accepted request sent to the upstream is in the upstream's root | none (map); by search: `tests/scenarios/work_queue_start_steps.py:12` | read |
| `measure_read.py:65` | a request of `root` read for measurement | same | none (map); by search: `tests/scenarios/batch_measurement_request_steps.py` | read |
| `model_requests.py` (`read_requests`, `model_facts.py:118`) | model reads `root`'s request files; v17/v18 | a sent request is in another root; the model reads only its own | none (map); by search: `design_model_check_requests.py` | read |
| `supervise_raise.py:37-45` | writes the lines into the upstream's checkout via `upstream_root` (18-20) | r28 says the asker never needs the upstream's checkout | none (map); by search: `tests/scenarios/supervision_raise_steps.py:44-54`, `features/supervision.feature:1445-1452` | read |
| `supervise_raise.py:63` | reads the upstream's request through `upstream_root` | same | none (map); by search: `supervision_raise_steps.py` | read |
| `workqueue_request.py:95-96` | one message for any neither-flag request | r31 needs its own wording; r45 keeps this one | none (map); by search: `requests_write_steps.py:94-97` (r45) | read; probe C |
| `workqueue_request.py:106-107` | `part_of` if `--thread`, else `source` (sources dropped when thread given) | r30: asker's `--source` refused | none (map); no test asserts it | read; probe B |
| `scripts/work:146`, `workqueue_request.py:87` | `--from` taken as the asker, unchecked | r32: asker must be this repository's context or product level; r33: side from repo | none (map); by search: r32 scenario (red) | read; probe E |
| `scripts/work` `cmd_show` (35-47) and `workqueue_list.py:show` (79-84) | a target that is no initiative goes to `work_item`, which refuses a request | r25 lists show for requests | none (map); by search: `work_queue_list_steps.py` (work-items only) | read; probe H |
| `supervise_intake.py:due` (18-20) | intake rounds for local requests `open` or `awaiting-upstream` | r40: take in before the intake rounds | none (map); by search: `supervision_intake_steps.py` | read |

## 4. Tests the requirements make impossible to keep

`tests-of` gives `none` for each function above (map blind to subprocess). Searched by name and text instead.

- **`tests/scenarios/test_work_queue.py`, "request with a --lines file that does not exist..." (`features/work-queue.feature:304`, steps `work_queue_request_steps.py`).** Runs `work request ... --from ctx-a --lines lines.md --source o1` in the upstream's repo. Today the origin check (`workqueue_request.py:95`) runs before the file check (`:97`), but the origin check passes. Under r30 (asker ctx-a is not the upstream and gives `--source`) the origin refusal would come first and the file refusal would not appear. Verified only by reading; not run (plugin refuses, see Blocked). **Conflict; two readings:** (i) r30 is checked after the file check, so the test stays; (ii) the scenario must change. Not decided here.
- **`tests/scenarios/supervision_raise_steps.py` (`request_run` 44-48, `request_raised` 51-54), `features/supervision.feature:1445-1452`.** Reads the request in the upstream's checkout `catalogue-ctx`. Under r28 read as a rule for every writer, it cannot pass. Under r28 read as the asker's own commands only (its raise is supervision's, r135), it stays. **Two readings.** Not run.
- **Deprecated scenarios `features/requests.feature` `@r1 @deprecated` (two --source, asker ctx-a, "upstream keeps") and `@r3 @deprecated` (neither flag).** Deselected by the collection (31 deselected), so not run. Both assert the old asker-writes-own-repo behaviour and would fail under r28/r30. Their deprecation covers them. **Mismatch:** the work-item's Retires cites them as `requests @r44` and `requests @r45`, while the feature tags them `@r1` and `@r3`; the live `@r44` and `@r45` are the new scenarios. Question for the plan.
- **`tests/scenarios/supervision_done_steps.py` (68 lines).** Writes `q2` in the context's own repo to make `done` see a delivered request. Under r28 the asker's request is not there. Read only to line 46; the rest not read. Not run.
- **Verified sound (none impossible):** `tests/scripts/test_workqueue_list.py` (in-process list of requests); `work_queue_start`, `batch_measurement_request`, `design_model_check_requests` (write their own local requests, so they keep passing if the layout is unchanged); `requests_show_steps` (r13, r14 scenarios not accepted).

## 5. A step the work-item skips

- **Take-in path (new, r39-r43) vs `request`.** `request` runs these checks before any write: empty delegation (`workqueue_request.py:93-94`, r22); no origin or thread (`:95-96`, r31/r45); missing lines file (`:97-98`); strict form per line via `model_parse.ears` (`:99-102`, r2). It writes `q<n>` one above the highest local number (`:103-105`) and commits the file (`:117`, through `workqueue.committed`, which refuses a repo git cannot commit in: `workqueue.py:272`). A take-in path that writes the sent request without these skips them: an empty delegation, a non-EARS line or an unnumbered id would land. Refusals: read. The strict-form and empty-delegation refusals are not run in this session.
- **Side checks (r33, r34) vs `outcome`, `ask`, `reply`.** These check only the turn (`workqueue_request.py:124-125`, `:133-134`, `:143-144`). The side the writing repository is never compared. Probes L and M show the consequence (run). No other effect is skipped.
- **Asker check (r32) vs `request`.** The asker comes from `--from` unchecked. `workqueue.context_path` (`workqueue.py:38`, read by `add`) already reads the repository's context id, so the check has its source.

## 6. Defects

Each reproduces by the probe named in §2, run today.

1. **Title alone accepts a request (r43).** Probe J: `request "x\n## Outcomes\n1. accepted" --from ctx-a --lines lines.md --thread t1` (one line in `lines.md`), then `work turn q1`: `status: accepted`, `turn: upstream`. No outcome was written by an upstream.
2. **A side writes the other side's part (r33, r34).** Probe L: asker's repo `outcome q1 1 accepted` in the upstream's turn, `rc=0`, `1. accepted` written. Probe M: upstream's repo `reply q1 1 "The work queue"` in the asker's turn, `rc=0`, answer written.
3. **Asker's --source with --thread accepted, sources dropped (r30).** Probe B: `rc=0`, `part_of: t1` only.
4. **Asker id from another context accepted (r32).** Probe E: in ctx-a's repo, `--from ctx-b` gives `asker: ctx-b`, `rc=0`.
5. **`work show <request>` refused (r25).** Probe H: `rc=1`, "q1 is a request, not a work-item or an initiative that work show shows".
6. **Neither-flag refusal omits raised-for (r31).** Probe C: message names `--source` and `--thread` only; the requirement names a request it is raised for.
7. **Asker's request kept in asker's repo (r28, r44).** Probe A: `q1.md` lands in the asker's `.shop/work/requests/`, nothing upstream. Read as a gap rather than a crash: the spec says the upstream keeps it.

Question, not a defect (no rule in the spec): **K**, an empty lines file gives a request with no lines (`rc=0`).

## 7. The file set

Production (must change):
- `scripts/workqueue_request.py` (187 lines; room 113): origin rules (r30), neither-flag wording (r31), asker check (r32), side checks in `outcome`, `ask`, `reply` (r33, r34), title check (r43), request location (r28).
- `scripts/work` (183; room 117): a take-in subcommand (r39, r40), `show <request>` route (r25), asker's repo identity (r32, r33).
- `scripts/workqueue_list.py` (84; room 216): `show` of a request (r25).
- `scripts/workqueue.py` (294; room 6): only `requests`, `context_path`, `committed` are read; any change pushes it near the limit, so new helpers go to new modules.
- `scripts/supervise_intake.py` (118; room 182): take-in before intake rounds (r40).
- `scripts/supervise.py` (284; room 16): `run` calls the take-in before rounds (r40); too little room for more than a call.
- New module (proposed): take-in of sent requests and messages, the allow list of asker ids (r39, r41-r43; decision 0071). Name not chosen.
- Possibly `scripts/supervise_raise.py` (84; room 216), only if r28 binds supervision's raise (question).

Production read, expected to keep passing (no change unless requests move): `workqueue_done.py` (73), `workqueue_start.py` (53), `supervise_all.py` (83), `measure_read.py` (213), `model_requests.py` (69), `workqueue_status.py` (170), `supervise_rounds.py` (243), `model_parse.py` (271, room 29).

Tests (must change or add):
- `tests/scenarios/requests_steps.py` (112; room 188): Givens/Whens for "the asker X runs", "to the upstream ctx-u", side-less commands, "q1 holds ... as the side's part".
- `tests/scenarios/requests_write_steps.py` (178; room 122): undefined "an upstream ctx-u", "its lines are ...", refusal naming steps.
- `tests/scenarios/requests_show_steps.py` (72; room 228): "the asker's repository" setups, `work show <request>` runs.
- New module, e.g. `tests/scenarios/requests_send_steps.py`: sent-request steps (r39-r43, r40). New file keeps the 300 limit.
- `tests/scenarios/test_requests.py` (10): import the new step module.
- Keep passing: `tests/scenarios/work_queue_request_steps.py` (r7 file-missing scenario, §4); `tests/scenarios/supervision_raise_steps.py` (101) if untouched.

Size: `tools size --limit 300` (run) prints nothing; no tracked Python file is over 300.

## Questions for the plan

- **Carrier of "sent" (r39-r43):** the spec says "sent", "message" and "registered asker id", decision 0071 says the upstream's allow list holds asker ids, but no mechanism or list location is in the spec or code. Two readings: a git transport of `.shop/work/requests` files, or a drop directory. Not chosen here.
- **Retire tags:** Retires cites `requests @r44` and `@r45` for the deprecated titles; the feature tags them `@r1` and `@r3`.
- **work-queue r7 (lines file missing, `--source`, asker ctx-a):** conflicts with r30 if the origin check runs first.
- **supervision raise into the upstream's checkout** vs r28: one reading breaks the supervision scenario.
- **Zero-line request (K):** refuse or accept.
