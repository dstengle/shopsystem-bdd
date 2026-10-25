# Plan of w147: answers under a request's delegation

Work-item `.shop/work/i24-requests-and-the-context-loop/w147.md`, under `supervision`, accepts r77 and r78. No `## Retires`, no `## Rulings`. Planned from `runs/w147/1-research/notes.md`, and a read of `supervise.py`, `supervise_rounds.py`, `supervise_brief.py`, `supervise_worker.py` (tools, ROLE, worker), `workqueue_answer.py`, `agents/initiative-round.md` and `tests/scripts/test_agents.py`. I read these to settle the brief, the agent and the answer form.

## 1. What goes green

- **supervision#r77**, outline "under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>", examples "answers it" and "leaves it for the person". Both are red today at the first Given (feature line 943, `StepDefinitionNotFoundError`). The Given at 946, the Thens at 948-949 and `<after>` at 950 have no steps either. No code in `scripts/` reads a delegation. `Run.run` has no answer pass, and `pull(MOVABLE)` skips `awaiting-answer`. The probe showed that `work run i1` with a delegation behaves exactly as it does without one: exit 3, the question printed, no session.
- **supervision#r78**, "an answer given by a session started under a delegation is written naming that delegation". Red at the Given on line 960. The Given at 962 and the Then at 964 have no steps. Nothing in `supervise*.py` writes an answer, and `work answer` writes `- <date>: <text>` with no `by`.
- Deprecated scenarios retired: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_answers.py` (new): the answer pass, a mixin of `Run` like `Rounds`. It does four things:
  - reads the delegation of the request the initiative fulfils;
  - collects the open questions of the initiative's `awaiting-answer` work-items and capability-proposals;
  - starts one session for each question;
  - writes and commits what each session gives back.
- `scripts/supervise.py`: `Run` takes the new mixin, and `run()` calls the pass (see D6). The file has room for 66 more lines.
- `scripts/supervise_brief.py`: `brief()` writes the answer session's own brief for the stage `answer` (D3). `answer_lines` is unchanged.
- `scripts/supervise_worker.py`: a `TOOLS` entry for the stage `answer` (reader tools only) and a `ROLE` entry for the new agent (D2).
- `agents/delegation-answerer.md` (new): the answering session's agent (D2).
- `CLAUDE.md`: a module-map row for `scripts/supervise_answers.py`. CLAUDE.md requires one for each new concern.
- `tests/scenarios/supervision_delegation_steps.py` (new): the Givens at 943, 946 and 962 and the Thens at 948-950 and 964.
- `tests/scenarios/test_supervision.py`: one more star import, for the new step module.

Removed from the researcher's set, and why:
- `scripts/workqueue_answer.py`: the person's `work answer` keeps its form (D4). The pass reuses `asked_from` as it is.
- `scripts/supervise_rounds.py`: `due()` already counts a written answer, so no change is needed (D5).
- `scripts/model_requests.py`, `scripts/workqueue_request.py`, `scripts/workqueue.py`: the delegation is a frontmatter key that the pass reads with `workqueue_request.field` (D1). No section, no command and no reader in `workqueue` changes.
- `tests/scenarios/supervision_given.py` and `supervision_then_workers.py`: both are near the size limit, so the new steps go into the new module. Any shared helper is imported from those files, not added to them.
- `tests/scripts/stub_claude.py`: its per-step `fields` already lets the stand-in give an `answer` field. Nothing is added.

## 3. Decisions

- **D1. Where a request gives its delegation.** The request's frontmatter key `delegation:`, a one-line quoted string. The pass reads it from the request named by `initiative.md`'s `fulfils`, through `workqueue_request.path_of` and `workqueue_request.field`, the same way `measure_read` reads `asker`.
  - An initiative with no `fulfils`, no request file or no `delegation:` gets no pass, so `work run` behaves as today.
  - A `##` section would be refused by `model`'s `request_form`. Frontmatter keys are not checked.
  - Rests on design-decision/requests-written-through-work: how `work` keeps a request is its own and may change.
  - No `work` command writes a delegation yet. The Givens write the key directly. The researcher found a gap here: no requests line yet says how a request gives a delegation. That is a later line, not this work-item's.
- **D2. The answering session's agent.** A new agent, `delegation-answerer`:
  - tools: Read, Glob, Grep, Write;
  - a `model:` line;
  - no Agent tool, no Bash;
  - text that says to answer the one question from the delegation and the named files only, to write `answer` in the result when the delegation covers the question, and to give no answer otherwise.

  The session runs as `work run`'s stage `answer`, through `Workers.worker`. That gives it the push verification (r35), the log lines (r8), the session record (r62), the check that the main checkout was not changed (r28) and the faults of r45. It runs in a detached worktree of the initiative branch, like a researcher's.
  - `initiative-round` does not fit. It reads the spec, the ledger and the drafts, which r77's "nothing else" forbids.
  - Rests on design-decision/the-v3-agents (each role is an agent whose tool list is exactly its role's) and supervision#r13 and r14.
  - `test_agents.py` r1 and r5 still pass: no Agent tool, and the agent names its model.
- **D3. What the session is given.** The answer brief holds:
  - the question;
  - the delegation in the person's words;
  - under "Read", only the files the question names;
  - the lines r17, r25 and r44 require of every brief: worktree, never change directory, scripts directory, base, branch "none", result file first with `PARTIAL`.

  It holds no work-item or proposal file, no capability, no run directories, no other question and no answers.
  - "The files a question names" means each token of the question text, with surrounding punctuation, quotes and backticks stripped, that is a relative path with a `/` and a file suffix. They are given in order of appearance, each once, whether or not the file exists.
  - The Thens at 948-949 read "given ... and nothing else" as this content: the Read list is exactly those files, and the brief names no other question, no `.shop/work/` file and no `spec/` file.
  - Rests on supervision#r77 together with r17, r25 and r44, which hold for every brief `work run` writes. Only this reading keeps all four. It is not a choice between readings of r77, because what the narrator observes (answer or none) is the same.
- **D4. How an answer names its delegation.** It is a bullet of `## Answers` in the person's form, `- <date>: <text>`, followed by one indented continuation line: `by: work run, under the delegation "<delegation>"`. It is written with `Run.section`.
  - `held()` keeps the continuation inside the bullet, so the n-th answer still answers the n-th question (r32, the Implementation note).
  - `answer_lines` joins the continuation into the brief line, so later workers and the `apply` round see the answer with its `by` (r57). The `apply` round needs that `by` for spec-integration r21.
  - The person's `work answer` line is unchanged.
  - The Then at 964 reads the bullet's text and its `by` line apart.
  - Rests on supervision#r78 and its Implementation note ("the answer names the delegation in its `by`").
- **D5. What an answer moves.**
  - On a work-item: the answer is written, and `work run` moves the item from `awaiting-answer` to the status `workqueue_answer.asked_from` gives. It commits through `Run.move`, so the log line, commit and push follow r7 and r38. Rests on design-decision/a-ruling-returns-to-the-asking-stage.
  - On a capability-proposal: the answer is written and committed with its run directory and log, with no transition, as `work answer` does. Once every question has an answer, `due()` starts the `apply` round (r70).
  - When a session gives no answer: nothing is written to the node. Its stage directory and log lines are still committed and pushed, as `keep_round` does, so the next `work run` finds nothing uncommitted (r46). The node stays `awaiting-answer`, and r32's exit 3 prints the question.
- **D6. When the pass runs and what it gives.**
  - It runs first in `run()`, before `rounds()`, so an answered proposal's `apply` round runs in the same `work run`. It runs again after each `pull` that leaves an open question not yet given in this run, followed by `rounds`, `draft` and `pull`, until no new question is open.
  - Each open question goes to a session once per `work run`. Sessions run one at a time, like rounds.
  - Every open question of a node is given (r77, "each question"). Answers are written only up to the node's first question left for the person. A later answer would land in the left question's position, which the n-th-answers-n-th rule forbids.
  - Rests on supervision#r77, r1 and the Implementation note on `## Answers`.
- **D7. What the session gives back.** Its result `status: DONE` with a non-empty one-line string `answer` is an answer. Any other result means the question is left for the person: `DONE` without an answer, any other outcome, or an `answer` holding a line break. Rests on supervision#r77 and design-decision/worker-results-are-files.

## 4. Tests the decisions break

None. What I checked:
- `tests/scenarios/work_queue_answer_steps.py:35-41` asserts the person's `- <date>: <text>` line. D4 leaves that form alone.
- `tests/scenarios/supervision_answers_steps.py` and the `sections` step at `test_supervision.py:220-229` assert answers that fixtures write. No code path they drive changes.
- `supervision_rounds_steps.py:55` asserts that `"Answer: <answer>"` appears in a brief. D4's continuation line is appended after the text, so it still matches. `due()` is unchanged.
- `tests/scripts/test_agents.py` iterates over every agent. The new agent has no Agent tool and names its model (D2), so r1 and r5 still pass. The stage-agent result check covers only the stage agents it names.
- In every existing scenario, the pass runs only where a request gives a delegation. No existing fixture writes `delegation:` (the researcher's search found none), so every other `work run` scenario sees no change.

## 5. Open cases

- An answer session that faults (push verification, uncommitted checkout change, cut-short session): the scenarios do not say whether the node goes `failed` or stays `awaiting-answer`.
- A request whose `fulfils` or request file cannot be read, or whose `delegation:` is not a one-line string (a block scalar, a list).
- A delegation holding a line break or a double quote, for D4's `by` line.
- A question that names no file. The session gets the question and the delegation only.
- A question asked by a worker during this run, after the first pass (D6 covers it). The scenarios have only questions that exist before the run.
- `work run` started with no initiative (r66): the pass runs for each initiative it takes. That is untested here.
