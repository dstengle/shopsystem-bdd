# Plan of w130: `work start` and an initiative's `done` (work-queue#r22, work-queue#r23)

This plan replaces 2-plan/plan.md. The question that plan left open (whether `work run` counts as a `work` command for r23) was answered on 2026-10-24 with reading B, in the work-item's `## Answers`. The answer is taken here as decision D7.

## 1. What goes green

- **work-queue#r22**: "start on an accepted request writes a proposed capability-change initiative that fulfils it, sourced from its origins, and prints its id" (features/work-queue.feature:34-44).
  - Why it is red (notes §1): no step matches the Given "a request q1 that is accepted, whose origins are o1 and o2" (StepDefinitionNotFoundError at line 38).
  - No step binds the Thens about one new initiative, `fulfils` with its source, and the printed id.
  - `scripts/work` has no `start`: probe P1 exits 2 with "invalid choice: 'start'".
- **work-queue#r23**: the Scenario Outline "a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done" (features/work-queue.feature:46-62), with four Examples rows.
  - Why it is red: no step matches the `<request>` Given in any of its four forms (line 51).
  - The code has no done check: probes P2 and P3 show that after `work withdraw w2`, initiative.md is still `started` and the commit holds only w2.md and log.jsonl.
- No deprecated scenarios are retired. The work-item has no Rulings. It has one Answer (D7).

## 2. Where the change lands

- `scripts/work`: a `start <request>` subparser and its dispatch entry.
- `scripts/workqueue_start.py` (new), for r22:
  - reads the request kept at `.shop/work/requests/<request>.md`;
  - refuses a request that is missing or not `accepted`;
  - numbers the new initiative and writes its directory and initiative.md.
- `scripts/workqueue_done.py` (new), for r23:
  - the done condition over an initiative's work-items and the request files under `.shop/work/requests/`;
  - the rewrite of initiative.md's `status` line to `done`;
  - whether a write was made, so that the caller can add initiative.md to its commit.
  - `scripts/workqueue.py` has only 38 lines free, which is why this is a new module.
- `scripts/workqueue.py`: `withdraw`, `retry` and `answer`'s commit path (`committed` with `rels_of`) run the done check inside the committed change. initiative.md joins the commit when the check rewrote it.
  - The hook goes in the `committed()` paths only, not in `move`, because `work run` calls `move` (D7).
  - Only the hook lines go in this file.
- `scripts/workqueue_answer.py`: answer's `committed(rels_of …)` call takes the same hook, if the hook is not reached through `rels_of`/`committed` in workqueue.py itself.
- `scripts/workqueue_request.py` (114 lines):
  - `resolve` sets a request to `delivered`, which can make the condition true, so it runs the done check for the initiatives the request names. initiative.md then joins resolve's commit.
  - Added by D7's answer ("and the request commands, when they make the condition true"); this file was not in the researcher's set as an edited file.
  - `request`, `outcome` and `turn` cannot make the condition true: a new request is `open`, and turn sets only `accepted` or `refused`. They are left as they are.
- `tests/scenarios/test_work_queue.py`: one import line for the new step module (14 lines free).
- `tests/scenarios/work_queue_start_steps.py` (new):
  - r22's request Given;
  - r23's four `<request>` Givens;
  - the Given "an initiative i1 under .shop/work/ that is started, whose work-item w1 is green and whose work-item w2 is ready";
  - r22's When and its Thens: one new initiative, fulfils and source, the printed id, and `.shop/work/i1/` as it was.
- `tests/scenarios/work_queue_withdraw_steps.py` (64 lines): may take the started-initiative Given instead, if it fits there better.
- `CLAUDE.md`: a module-map row for `scripts/workqueue_start.py` and one for `scripts/workqueue_done.py`, as the repository's rule requires.
- **Removed** from the researcher's set: `scripts/supervise.py`. The notes needed it only if `work run` counted (their Q4), and D7 settles that it does not.

## 3. Decisions

- **D1. The new initiative's id and directory.**
  - The id is `i<n>`, with `<n>` one above the highest `<n>` of any initiative under `.shop/work/`. That `<n>` is read from the frontmatter id `initiative/<context path>/i<n>` or from the directory name's leading `i<n>`. Existing directories carry a slug (`i24-requests-and-the-context-loop`, whose id is `i24`).
  - The directory is `.shop/work/i<n>/`. `work` takes an initiative by its directory name (`work add <initiative>`, r1; `work status <initiative>`, r16), so the id that r22 prints has to name that directory.
  - `work start` prints the id alone, as `work add` prints `w<n>` (r1).
  - Rests on: design-decision/work-items-named-by-ids (ids are the context's, one above the highest, never repeated; by analogy), work-queue#r22 ("print its id") and r1/r16.
- **D2. The initiative's fields.**
  - `id`, `kind: capability-change`, `status: proposed`, `fulfils:` the request's frontmatter id, `source:` the request's `source` list as written, `title` (the request's `# ` heading) and `date` (the day of the run).
  - Rests on: work-queue#r22, and design-decision/work-file-forms (the initiative's field set; `fulfils` is r22's addition).
- **D3. What start refuses.** start exits with an error, saying why and writing nothing, when there is no request file for the id given or the request's status is not `accepted`.
  - Rests on: work-queue#r7 (r22 applies only to an `accepted` request).
- **D4. start does not commit.** r9 lists the committing commands, and `start` is not one of them.
  - Rests on: work-queue#r9.
  - Its consequence is in part 5.
- **D5. The done condition.** An initiative qualifies when all three hold:
  - it has at least one work-item;
  - every one of its work-items is `green` or `withdrawn`;
  - every request file under `.shop/work/requests/` whose `asker` is this context, and which names the initiative, is `delivered`.

  How the condition is read:
  - A request names the initiative when its `part_of` or its `source` holds the initiative's frontmatter id (work-queue Implementation, r23 line).
  - "This context" is an `asker` of `internal` or this context's own id.
  - The check sets `done` only when the command's change makes the condition true: false before the change, true after it.
  - Only initiative.md's `status` line is rewritten. No log.jsonl line is written for it, because r5 logs work-item transitions only.
  - Rests on: work-queue#r23.
- **D6. The done write is in the same commit as the change.**
  - When `withdraw`, `retry`, `answer` or `resolve` sets the initiative to `done`, initiative.md joins that command's commit.
  - When the commit fails, initiative.md is restored with the rest of the command's change.
  - Rests on: work-queue#r9 and its withdraw row (features/work-queue.feature:236), whose initiative has only w1. Withdrawing w1 makes it done, and "nothing under .shop/work/ differs from main's last commit" then holds only if initiative.md is committed. Also rests on work-queue#r7 (change nothing on failure).
- **D7. Which commands run the done check.**
  - These do: `work withdraw`, `work retry` and `work answer`, and the request command `work resolve`, when its change makes the condition true.
  - `work run` (supervision) does not. Its green move leaves initiative.md as it is, and `scripts/supervise.py` does not change.
  - Rests on: the work-item's Answer of 2026-10-24 (reading B). The gap this leaves, an initiative whose last work-item `work run` greens staying `started`, is recorded there as an observation for a later line and is not this work's.

## 4. Tests the decisions break

- **D6:**
  - The r9 withdraw row at features/work-queue.feature:236 is kept. Its "new commit holds both" step compares the work-item file and log.jsonl only, and "nothing under .shop/work/ differs" holds because initiative.md is committed.
  - The r10 scenario at :198 also makes its i1 done. Its Thens do not look at initiative.md, so it is kept.
  - tests/scripts/test_work_withdraw.py only refuses, has no initiative.md and makes no move, so it is kept.
- **D7:**
  - features/supervision.feature:142-148 and :159-164 are kept, with test_supervision.py:130-132, because `work run`'s move does not run the check.
  - The request scenarios that run `work resolve` (requests capability) are kept if their Givens make no initiative that the resolved request names. In that case the check finds nothing to set and resolve's commit is unchanged.
  - This last point comes from the notes' grep (no test writes `status: done` or sets an initiative done), not from a run. The implementer runs the requests scenarios to confirm it.
- **D1-D5:** none. Verified from the notes' searches:
  - no test calls `work start`;
  - no work-queue test writes `.shop/work/requests/`;
  - no test expects an initiative to stay `started` after withdraw, retry or answer.

## 5. Open cases (for the implementer to name, not to choose)

- An initiative directory with no initiative.md, for example a Given that writes only work-items: the check has no file to write.
- The condition already holding before the command, for example an initiative already `done`, or a `proposed` one with every work-item green.
- A request whose origin is a job-thread (`part_of`) rather than `source`, given to start. r22 speaks only of "origins".
- `work start` run twice on the same request. The design model allows one initiative per request, and no line here refuses a second.
- The uncommitted initiative.md that start leaves (D4): `work run`'s check (supervise.py:77-81) refuses uncommitted changes under `.shop/work/`.
- `model check` v_d1 (scripts/model.lp:240) flags a done initiative whose capability-proposal is not closed, and r23 can set done while a proposal is only `formulated`.
- A done initiative leaves `work status` with no initiative (r17) and PreCompact compaction (migrate_session.py via `open_names`).
- `resolve` on a request that names several initiatives, or an initiative that is not under `.shop/work/`.
