# Plan of w130: `work start` and an initiative's `done` (work-queue#r22, work-queue#r23)

Status: one open question (part 3, D7), which decides where the done check sits and whether `scripts/supervise.py` changes. Everything else is decided below.

## 1. What goes green

- **work-queue#r22**: "start on an accepted request writes a proposed capability-change initiative that fulfils it, sourced from its origins, and prints its id" (features/work-queue.feature:34-44). Red today because no step matches the Given "a request q1 that is accepted, whose origins are o1 and o2" (StepDefinitionNotFoundError at line 38). Nothing in tests/ binds the Thens about a new initiative, `fulfils` and the printed id. `scripts/work` has no `start` subcommand: probe P1 exits 2 with "invalid choice: 'start'".
- **work-queue#r23**: the Scenario Outline "a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done" (features/work-queue.feature:46-62), four rows. Red today because no step matches the `<request>` Given in any of its four forms (line 51). The code has no done check either: probes P2 and P3 show that `work withdraw w2` leaves initiative.md `started`, with only w2.md and log.jsonl in the commit.
- This work-item retires no deprecated scenarios and has no Rulings.

## 2. Where the change lands

- `scripts/work`: a `start <request>` subparser and its dispatch entry.
- `scripts/workqueue_start.py` (new): r22. It reads the request kept under `.shop/work/requests/`, refuses when the request is missing or not `accepted`, and writes the new initiative directory and its initiative.md.
- `scripts/workqueue_done.py` (new): r23. It decides whether an initiative's work and requests are complete and rewrites the initiative's status to `done`. `scripts/workqueue.py` is close to its limit (262 lines), so this check lives in its own module.
- `scripts/workqueue.py`: calls the done check after a transition. `rels_of` (or the commit path of `withdraw`, `retry` and `answer`) adds initiative.md to the commit when the check wrote it. Only a small hook goes here, because only 38 lines are free.
- `scripts/workqueue_request.py`: read for its request-file reading (`_field` and the path helper). It is edited only if the new modules need a public reader instead of private helpers.
- `scripts/supervise.py`: changes **only under reading A of D7**. Its commit (89-99) would include initiative.md when work run's green move wrote `done`. Under reading B it stays as it is.
- `tests/scenarios/test_work_queue.py`: one import line for the new step module (14 lines free).
- `tests/scenarios/work_queue_start_steps.py` (new): the request Givens (r22's, and r23's four `<request>` forms), the Background-style Given "an initiative i1 … that is started, whose work-item w1 is green and whose work-item w2 is ready", and the r22 When and Thens.
- `tests/scenarios/work_queue_withdraw_steps.py`: may take the started-initiative Given instead, if it fits there better.
- `CLAUDE.md`: a module-map row for `workqueue_start.py` and one for `workqueue_done.py`, as the repository's rule requires.

## 3. Decisions

- **D1. Where the new initiative lives and how it is named.** The id is `i<n>`, with `<n>` one above the highest `i<n>` of any initiative under `.shop/work/`. The directory is `.shop/work/i<n>/` and the frontmatter id is `initiative/<context path>/i<n>`. `work start` prints `i<n>` and nothing else, the same way `work add` prints `w<n>`. Rests on design-decision/work-items-named-by-ids (ids are the context's, numbered one above the highest, never repeated) and design-decision/work-file-forms. The scenario pins only "one new initiative" and "prints that initiative's id", and `.shop/work/i1/` staying as it was.
- **D2. The initiative's fields.** `kind: capability-change`, `status: proposed`, `fulfils:` the request's frontmatter id, `source:` the request's `source` list as written, a `title` (the request's `# ` heading) and a `date` (the day of the run). Rests on work-queue#r22, design-decision/work-file-forms (field set) and docs/design-model/design-model.md's initiative table (`fulfils`: exactly one request, `accepted`).
- **D3. What start refuses.** start exits with an error, saying why and writing nothing, when there is no request file for the id given or its status is not `accepted`. Rests on work-queue#r7. r22 applies only to an `accepted` request.
- **D4. start does not commit.** r9 names the commands that commit (`add`, `retry`, `withdraw`, `answer`), and `start` is not among them. Committing would be behaviour that no line asks for. Rests on work-queue#r9. Its consequence is in part 5.
- **D5. The done condition.** An initiative qualifies when:
  - it has at least one work-item;
  - every one of its work-items is `green` or `withdrawn`;
  - every request file under `.shop/work/requests/` whose asker is this context, and which names the initiative, has status `delivered`.

  A request names the initiative when its `part_of` or its `source` holds the initiative's frontmatter id (work-queue Implementation; design-decision/references-are-ids). The asker is this context when it is `internal` or this context's own context id (requests capability, Implementation: an asker is a context id, `internal` or the product level). The check runs only after a change that was made, and sets `done` only when the condition was false before that change and is true after it ("makes it true", work-queue#r23). Only initiative.md's `status` line is rewritten. No log.jsonl line is written for it, because r5 logs work-item transitions only.
- **D6. The done write is in the same commit as the work-item.** When `withdraw`, `retry` or `answer` sets the initiative to `done`, initiative.md joins that command's commit. Rests on work-queue#r9 and its withdraw row (features/work-queue.feature:236): that row's initiative has only w1, so withdrawing w1 makes it done. That row's Then "nothing under .shop/work/ differs from main's last commit" holds only if initiative.md is committed. The done write also counts as part of the command's change under r7: when the commit fails, initiative.md is restored along with the work-item.
- **D7. OPEN (the question): does `work run` count as "a `work` command" for r23?** If the done check sits in `workqueue.move`, it also runs when `work run` moves the last work-item to green. That changes what the person sees in `.shop/work/i1/initiative.md` after `work run i1`, which accepted supervision scenarios pin today. Supervision's requirements, those scenarios and this work-item's Rulings (it has none) do not settle it. See the result's `questions`. Under reading A the check sits in `move` and `scripts/supervise.py` commits initiative.md. Under reading B the check sits only in the `committed()` paths of `withdraw`, `retry` and `answer`, and `supervise.py` does not change.

## 4. Tests the decisions break

- **D6:**
  - The r9 withdraw row at features/work-queue.feature:236 is kept. The step `new_commit_holds_both` in work_queue_withdraw_steps.py compares only the work-item file and log.jsonl, and the step "nothing under .shop/work/ differs" holds because initiative.md is committed.
  - The r10 scenario at :198 also makes its i1 done. Its Thens do not look at initiative.md, so it is kept.
  - tests/scripts/test_work_withdraw.py only refuses, makes no move and has no initiative.md, so it is kept.
- **D1–D5:** none. I verified from the notes and by search that no test writes `.shop/work/requests/` for work-queue, calls `work start`, or sets an initiative to `done` (the notes' grep of `status: done` found nothing).
- **D7, reading A:** breaks features/supervision.feature:142-148 ("a worker's change to a file under .shop/work/ outside its stage directory is put back"). In that scenario w1 goes from drafted to green, the only work-item of i1, so initiative.md becomes `done`. Then `.shop/work/i1/initiative.md is as it was` (test_supervision.py:130-132) fails. Reading A also breaks :159-164 ("… are as that session committed them"). These are feature files and may not be rewritten in red-green (design-decision 0006), so reading A needs a formulation change to those scenarios before an implementer can make both green. **Reading B** breaks no test.

## 5. Open cases (for the implementer to name, not to choose)

- An initiative directory with no initiative.md (for example, a Given that writes only work-items). The done check then has no file to write.
- The done condition already holding before a command: for example, an initiative that is already `done`, or `proposed` with every work-item green.
- A request named by start whose origins are a job-thread (`part_of`) rather than `source`. r22 speaks only of origins.
- `work start` run twice on the same request. The design model allows at most one initiative per request, and no line here refuses a second.
- start run outside a git repository, and the uncommitted initiative.md start leaves: `work run`'s check (supervise.py:77-81) refuses uncommitted changes under `.shop/work/`.
- `model check` v_d1 (scripts/model.lp:240) flags a done initiative whose capability-proposal is not closed, and r23 can set done while a proposal is only `formulated`.
- A done initiative drops out of `work status` with no initiative (r17) and out of PreCompact compaction (migrate_session.py via `open_names`).
