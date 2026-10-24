# Plan of w128: a request accepted, refused or resolved to delivered, each change committed

Accepts requests#r8, r9, r10, r11, r12. No Retires section, no Rulings. Planned from `runs/w128/1-research/notes.md`; the sibling notes of w126 were read to keep names and forms the same.

## 1. What goes green

All five are red today for the same reasons. No `tests/scenarios/test_requests.py` binds `features/requests.feature`, and no step module defines its Givens, so each scenario fails `StepDefinitionNotFoundError` on its first Given. Also, `scripts/work` has no `turn`, `outcome` or `resolve` command: argparse refuses each as `invalid choice`.

- **requests#r8**, "the upstream ending its turn with every line accepted, refused or withdrawn and one accepted sets the status to accepted": the Given is undefined and `work turn` is missing.
- **requests#r9**, "the upstream ending its turn with every line refused or withdrawn sets the status to refused": the Given is undefined and `work turn` is missing.
- **requests#r10**, "resolve on an accepted request in the asker's turn writes each accepted line's requirement id and version as the resolution": the Given is undefined and `work resolve` is missing.
- **requests#r11**, "resolve writing a request's resolution sets the request's status to delivered": the Given is undefined and `work resolve` is missing.
- **requests#r12**, "a command that changes a request commits the request on the current branch": the Given is undefined and `work outcome` is missing. Its first Then matches the path step `new_commit_holds` (`tests/scenarios/work_queue_git_steps.py:47`) only with `q1` taken as a path, so `git show main:q1` fails. Its second Then matches no step.

No deprecated scenarios are retired.

## 2. Where the change lands

The changed files:

- `scripts/work`: add the subcommands `turn`, `outcome` and `resolve` to the subparsers and the dispatch, each calling the new module.
- `scripts/workqueue_request.py` (new):
  - finds a request by id under `.shop/work/requests/` and reads and writes the request's form;
  - `outcome` writes a line outcome;
  - `turn` passes the turn and applies the status rules of r8 and r9;
  - `resolve` writes the resolution and the status `delivered`, and refuses a request that is not `accepted`.
  - Every write goes through `workqueue.committed` (r12).
  - It uses the name w126's research gave the request library, so the sibling work-items meet in one module.
- `CLAUDE.md`: a module-map row for `scripts/workqueue_request.py`, "the requests of a context: `work request`, `outcome`, `turn`, `resolve`".
- `tests/scenarios/test_requests.py` (new): binds `requests.feature`, as `test_work_queue.py` does.
- `tests/scenarios/requests_steps.py` (new):
  - the Givens that write `q1` in the form of decision D2 (asker, status, turn, lines, line outcomes);
  - the Whens that run `work turn`, `work outcome` and `work resolve` as the upstream, setting `context["done"]` the way the existing Whens do;
  - the Thens of r8 to r11 (status, resolution per line, a line with nothing, the success exit, if no existing step already covers it).
  - It also gives a helper that maps a request id to the path where it is kept.
- `tests/scenarios/work_queue_git_steps.py`:
  - `new_commit_holds` takes either a path or a request id, mapping a request id to its kept path;
  - a new Then, "nothing work keeps for {request} differs from main's last commit", checks git status on that path.

Changed from the researcher's set:

- **Removed, read only:** `scripts/workqueue.py` (`committed`, `Refused` and the frontmatter helpers are reused).
- **Removed, no change:** `scripts/model_work.py` (D2 is not fixed, see section 3), `scripts/work_items.py`, `tests/scenarios/conftest.py` (only its `repo` and `context` fixtures are used), `tests/scenarios/test_work_queue.py`.
- **Added:** `scripts/workqueue_request.py`, `tests/scenarios/requests_steps.py`.

## 3. Decisions

- **D1. w128 builds the `work turn` and `work outcome` it needs.** The r8 and r9 scenarios run `work turn` and the r12 scenario runs `work outcome`, so they cannot go green without these commands. The parts that are w127's are left to w127:
  - the refusal out of turn (r16);
  - the statuses awaiting-asker and awaiting-upstream (r17, r18).

  Built here:
  - `work outcome <request> <n> <outcome>` writes the line outcome;
  - `work turn` passes the turn to the other side (the least that r8 and r9 need, which is r7's effect);
  - when the turn passes from the upstream with every line settled, `work turn` sets `accepted` (r8) or `refused` (r9);
  - in any other case `work turn` leaves the status as it was.

  Rests on requests#r8, r9 and r12. The names are the ones w126 used, so whichever work-item merges second reuses what the first one built rather than adding a second copy.
- **D2. How a request is kept.** It is the file form of the capability's Implementation section, at `.shop/work/requests/<id>.md`.
  - "Line n" is the nth entry of `## Lines`, counting from 1.
  - `## Outcomes` holds one entry per line, numbered as in `## Lines`, with the outcome word, or no entry when the line has no outcome.
  - `## Resolution` holds one entry per accepted line: its line number, the requirement id exactly as given (such as `thing#r3`) and the version.
  - Lines that were not accepted get no entry in the resolution.

  Rests on design-decision/requests-written-through-work: how `work` keeps a request is its own business. The id is kept verbatim because design-model-check r116 reads the requirement a resolution names.
- **D3. How `work resolve` takes its input.** It is `work resolve <request>` with one `--line <n> <requirement> <version>` per accepted line. The scenario's When maps onto it directly ("thing#r3 for line 1 … found in the version 0.26.0"), and r10 gives each line "the version that holds it". `resolve` does not check whose turn it is. Rests on requests#r10 ("whichever side's turn it is"). What the narrator gets back (the resolution stored, the status `delivered`) does not depend on this argument form, so it is not a question.
- **D4. `resolve` on a request that is not `accepted`** is refused with an error exit and changes nothing. Rests on the capability's Implementation (work-queue r7) and design-decision/exits-are-successful-or-errors.
- **D5. Each of `outcome`, `turn` and `resolve` commits only the request file, through `workqueue.committed`.** That function refuses outside a git work tree, restores the file when the commit fails, and leaves other staged files alone. Rests on requests#r12. The research notes' section 5 lists the effects this step gives.
- **D6. The defects are not fixed here.**
  - Notes D1: `work withdraw` takes a request for a work-item.
  - Notes D2: `model check` reports `.shop/work/requests` as having no initiative.md.

  No accepted scenario needs either fix. D2 belongs to design-model-check (its r19 and r112 scenarios). Both should be reported as findings.

## 4. Tests the decisions break

None. The decisions only add commands, a module, steps and one new Then. The generalised `new_commit_holds` still resolves a plain path as it does now, so the work-queue scenarios that use it (work add and retry, r9) keep their meaning. What was verified, from the notes and by reading `work_queue_git_steps.py`:

- no test lists `work`'s subcommands or its usage;
- no test withdraws a request;
- no existing test runs `workqueue_request`, which is new.

These lists come from searching the code; no coverage map was available.

## 5. Open cases (for the implementer to name, not to choose)

- `resolve` given a line that is not accepted, or not given every accepted line.
- `resolve` given a line number twice.
- `outcome` given a line number that is out of range, or an outcome word other than accepted, refused, withdrawn or question.
- A request id that does not exist for `turn`, `outcome` or `resolve`.
- A version that is not well formed, or a requirement id not in the form `<capability>#r<n>`.
- The commit message of each request command.
- Whether request changes also go into a log, as work-item changes go into `log.jsonl`.
- `turn` from the upstream when every line is withdrawn and none is refused. r9 reads "refused or withdrawn", so this case is refused; there is no scenario for it.
- The merge with w126 and w127, which share `scripts/workqueue_request.py`, `tests/scenarios/requests_steps.py` and `tests/scenarios/test_requests.py`: steps that would be defined twice with the same text.
