---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-7
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 7: Telemetry — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `telemetry` capability, so that all 4 of its requirements leave `unbuilt:`.
- `measure batch <batch>` writes one measurement of a batch. It gives the wall time, the session time, the tokens, and
  the cost by role (planning, implementing, review, fixing). It also gives the pull request's review findings by grade
  and the defects traced to their items, and the knobs the batch ran with.
- `measure defect <item>` records a fault found after the merge, against the delivered item and its batch.
- `measure show` and `measure compare` read batch measurements, and `compare` takes batch names.

The plan closes these items left open by earlier plans:
- Plan 6's "0060 is superseded when plan 7 builds `measure batch`".
- Plan 6's "knob changes are recorded as decisions, with their figures".
- Plan 5's "a real `pr-reviewer` run has not been measured".

**Architecture:**
- **No network, no session record of its own (D2-D4).** A batch keeps no session ids: `.shop/batches/<n>/` holds
  only its plan, its reviews and now its defects. `measure batch` finds its sessions the way `measure initiative
  --sessions` does today (`measure_read.read_transcripts`, `assistant_rows`, `request_key`): by reading Claude Code's
  transcripts on disk and keeping those active inside the batch's window. The default directory is this repository's
  own project directory in Claude Code's store: `measure_read.store_dir()` / `projects` / the resolved root with every
  character that is not a letter or a digit written `-`. `--sessions <dir>` names another directory.
  - The window comes from git: the commits of `.shop/batches/<n>/plan.md` on the base.
  - The tests write transcripts into a `CLAUDE_CONFIG_DIR` of their own and never read the person's store.
- **Cost is computed, not read (D5).** Transcripts carry tokens and the model, never dollars. `measure_cost.py` holds
  a price table per model, dated, which `.shop/delivery.toml` `[prices."<model>"]` overrides. A request of a model with
  no price is counted in tokens and named under `unpriced`, never guessed (0018).
- **Roles (D6).** A subagent's role comes from its `agent-<id>.meta.json` beside its transcript (`agentType`,
  `description`). Failing that, it comes from when the subagent started, against the first review. The main session
  is `planning`.
- **The record (D8).** The record is `.shop/records/measurements/<date>-batch-<n>.md`, the `measurement` kind of
  `measure_write`, with a `## Summary` of tables before the JSON block. The tables carry the words "wall time",
  "session time", "tokens" and "cost by role".
- **New modules** (each ≤ 300 lines): `scripts/measure_cost.py`, `measure_batch_read.py`, `measure_batch_sessions.py`,
  `measure_batch.py`, `measure_defect.py`, `measure_batch_show.py`; `tests/scenarios/telemetry_handlers.py`;
  `tests/scripts/measure_batch_testing.py` and five test modules.
- **How each line is met:**

  | id | line (short) | met by | checked by |
  |---|---|---|---|
  | r1 | `measure batch` on a `merged` batch writes its measurement with wall time, session time, tokens, cost by role | `measure_batch.figures_of`, `measure_batch_show.summary`, `measure_write` | scenario @r1; Task 2 tests |
  | r2 | a review finding on the batch's pull request → its grade is in the measurement | `measure_batch.findings_of` over `batch_findings.reviews` | scenario @r2; Task 2 tests |
  | r3 | `measure defect` on a delivered item in a batch writes a defect of the item for the batch | `measure_defect.record` | scenario @r3; Task 3 tests |
  | r4 | `measure compare batch-2 batch-3` prints both names | `measure_batch_show.resolve`, `compare` | scenario @r4; Task 4 tests |

  `telemetry` is a `service` capability with a generated feature. Each id leaves `unbuilt:` in the commit that makes
  its scenario pass. The strict xfail holds that rule (plan-1 ruling P6).

**Tech Stack:** Python 3.11, standard library only (`json`, `re`, `subprocess`, `tomllib`, `dataclasses`,
`datetime`), git, pytest with xdist and pytest-bdd.

**Spec:**
- Read first: `spec/capabilities/telemetry.md` (4 lines; relations `defect of item`, `defect for batch`, `measurement
  of batch`).
- The glossary of `spec/index.md`:
  - `measurement` ("the figures of one batch, of one earlier delivery or of a trial", plan-1 P9);
  - `defect` ("a fault in the behaviour of the repository's code, with its reproduction, found by a review or after a
    merge", lifted by plan-1 P9). Both are already in the glossary; this plan adds no term.
  - `batch`, `batch plan`, `pull request`, `review finding`, `grade` (`Critical`, `Important`, `Minor`), `triage`
    (`fix now`, `observation`, `drop`), the item's and the batch's statuses;
  - `review finding on pull request`, `item in batch`.
- `design.md` goal 8, and § "The session's calls" ("Knob changes are recorded as decisions").
- `recon.md` § Cost and time: how the cost figures of i42-i64 were read (`session.json` totals per stage, transcripts
  for round trips). § Quotes: `measure_read.py` reads usage, timestamps, session and agent ids, tool-use names and
  compaction boundaries, never message text.
- Read beside them:
  - `plan-5-pr-review.md`: D7 (size is the batch-size knob), D13 (the review record), D21 (recurring findings are
    plan 7's to count), D23 (the third-review park, "revisit with plan 7's figures");
  - `plan-5-implementation.md` and `plan-6-implementation.md` § Open problems;
  - `spec/capabilities/batch-measurement.md` (`measure initiative`, kept unchanged until plan 9);
  - `spec/decisions/0018-*` (refuse unknown shapes) and `0060-measure-an-initiative.md`.

## Global Constraints

- **Branch:** `workflow-simplification`, from `9d765bb8` or later. Every plan is built on this one branch. No new
  branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command, since together they need the person's
  approval. Run them as separate commands, or leave scratch directories under
  `/home/vscode/.claude/jobs/7e9ba079/tmp`. Keep shell variables few.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/measure` (97) may grow to at most 150 (two subcommands and the contract's text).
  - `scripts/measure_show.py` (112) may grow to at most 135: it only hands a batch measurement to
    `measure_batch_show`.
  - `scripts/measure_write.py` (41) may grow to at most 50.
  - `scripts/measure_read.py` (213), `scripts/measure_build.py` and every `scripts/batch_*.py` are not changed.
  - `tests/scenarios/world_nodes.py`, `batch_measurement_handlers.py`, `batches_handlers*.py` and `batches_world.py`
    are not changed. Telemetry's steps that share a key with them go through `work_queue_world.local` (D13).
- **Module map:** each task that creates a module adds its `CLAUDE.md` row in the same commit (rows given per task).
  - Task 2 also rewrites the `scripts/measure` row to name `batch`.
  - Task 2 adds `telemetry` to the `tests/scenarios/<capability>_handlers*.py` row.
- **Spec:** no requirement line, group or relation row is edited or added anywhere. A line found wrong is reported, not
  changed. The only spec edits are these:
  - `telemetry.md`: `unbuilt:`, `rests_on:` (Task 5), and the new `## Implementation, may change` and `## Not yet`
    sections. Plan 1 wrote the file and it has never been merged to `main`, so it may be fixed in place (plan-1 ruling
    P10).
  - `spec/decisions/`: the frontmatter of 0060 only (`status`, with `tier` and `enforced_by` removed), the new files
    0078 and 0079, and `index.md` as `model decisions` writes it.
- **The glossary is not edited.** `measure` (actor) still reads "the tool that measures an initiative's deliveries",
  and plan 9 rewrites it with `measure initiative` (D17).
- **The strict xfail:** an id leaves `telemetry.md`'s `unbuilt:` in the same commit that makes its scenario pass,
  never before and never after.
- **No network, no claude in the suite.** No test reaches a network, starts a session, or reads the person's
  `~/.claude`: every test that runs `measure batch` sets `CLAUDE_CONFIG_DIR` to a directory of its own.
- **`measure` writes no prompt, reply or tool content** (batch-measurement's rule, kept). It writes only tokens,
  times, ids, models, agent types and the meta `description`'s role words. It writes no `description` text.
- **Names next to ids:** an item is printed with its label (`b1 "Abandon"`), a batch as `batch-<n>`, a defect as
  `batch-<n> d<k>` (design goal 10).
- **Old behaviour kept:** every test of plans 1-6 passes unchanged, except the two pinned totals named in Task 5. That
  includes batch-measurement's 22 scenarios: `measure initiative`, and `show` and `compare` on initiative records.
- **Baselines** (measured at `9d765bb8` on this machine). Each task's expected figures are given in the task, and any
  change from these is planned there:
  - `python3 -m pytest -q`: `1402 passed, 1 skipped, 8 xfailed, 135 subtests passed` (28 s wall). The ceiling report
    lists `test_e2e_codified` (11.7 s) and `test_supervision`'s flaky-scenario test (11.1 s), as before.
  - `python3 -m pytest -m timing -n 0 -q`: `2 passed, 1411 deselected` (5.5 s).
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 9, with no problems: brainstorming r3; conversation r1-r4; telemetry r1-r4.
    At the end there are 5, and `telemetry` is absent.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/model decisions --check | tail -1`: `4 check decisions: 4 hold, 0 failing`, exit 0 (3.1 s).
  - `python3 scripts/features generate --check`: exit 0.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
  - `python3 scripts/tools check <the branch's changed Python>`: ruff and vulture clean. import-linter states no
    contracts.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled for every plan. |
| D2 | **Where the sessions come from.** A batch records no session ids, and `work batch` runs no session of its own, so nothing like `session.json` exists. `measure batch` reads transcripts on disk, as `measure initiative --sessions` does:<br>- **Default:** `measure_batch_read.project_dir(root)` = `store_dir() / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(Path(root).resolve()))`. This is Claude Code's directory for sessions started in the base checkout, where building-a-batch runs every `work batch` command. The task subagents' transcripts are under it too (`<session>/subagents/agent-<id>.jsonl`), wherever their worktrees are.<br>- **`--sessions <dir>`:** any directory of transcripts, raw or the slim export.<br>- **A directory that is missing or holds no transcript** is not refused. The batch is measured without sessions, and the measurement gives `"sessions_from": "<dir>"` and `"sessions_found": 0`. `show` says "no transcripts at <dir>".<br>- Only that one directory is read, never another project's. |
| D3 | **The window, from git.** `git log --reverse --format=%H%x09%cI%x09%s -- .shop/batches/<n>/plan.md` on the current checkout gives these moments:<br>- `started`: the first commit;<br>- `first_review`: the first subject containing `-> in-review`;<br>- `built`: the last subject containing `-> awaiting-merge`;<br>- `closed`: the subject containing `-> merged` or `-> abandoned`. For a batch whose status is `merged` or `abandoned` with no such subject, it is the last commit.<br>Each is an ISO time or `null`. **Session window:** from `started` to `built`, else `closed`, else the time of measuring (`measure_batch.now()`, which tests monkeypatch). Both ends are inclusive, at second resolution: a request's time is truncated to the second. **Wall time** is `closed` (or now) − `started`. **Waiting for merge** is `closed` − `built` when both are given. Wall time is what the person sees. Session time leaves out the wait for the merge, so the review loop's cost is not charged for the person's delay. |
| D4 | **Which requests count.** Every distinct request (`measure_read.request_key`) of every `*.jsonl` under the directory, read through `measure_read.assistant_rows`, so an unknown shape is refused naming the file and line (0018).<br>- A request of a main session counts when its time is inside the window.<br>- A subagent counts whole when its first request is inside the window, even if it ends after the window.<br>- A subagent that started outside the window does not count.<br>- Claude Code writes one row per content block, with one `requestId` and the usage repeated. A request is counted once, each usage field the maximum over its rows and its time the earliest.<br>**Session time** of a session or subagent is the sum of the gaps between its consecutive counted requests that are at most `IDLE = 300` s. A role's session time is the sum over its sessions, so subagents running side by side add up. |
| D5 | **Prices.** `measure_cost.PRICES` maps a model id to `(input, output, cache_read)` in dollars per million tokens, `AS_OF = "2026-10-06"` (the claude-api skill's table, read 2026-11-05):<br>`claude-opus-5-5` 4, 20, 0.20; `claude-opus-5` 5, 25, 0.50; `claude-opus-4` 5, 25, 0.50; `claude-sonnet-5-5` 2, 10, 0.20; `claude-sonnet-5` 2, 10, 0.20; `claude-sonnet-4` 3, 15, 0.30; `claude-haiku-5-5` 0.10, 0.50, 0.01; `claude-haiku-4` 1, 5, 0.10; `claude-fable-5-1` 10, 50, 0.25; `claude-fable-5` 10, 50, 1.00.<br>Where the table states no cache-read price, the price is 0.1 × input.<br>- **Model match:** a model is priced by the longest key it starts with, so a dated id still matches.<br>- **Cache writes:** 1.25 × input for `usage.cache_creation.ephemeral_5m_input_tokens`, and 2 × input for `ephemeral_1h_input_tokens`. Claude Code writes 1 h caches, as the live transcripts show. Without that breakdown, `cache_creation_input_tokens` is priced as 5 min.<br>- **Overrides:** `.shop/delivery.toml` `[prices."<model id>"]` with `input`, `output` and `cache_read` (numbers ≥ 0, all three) overrides or adds one model. Anything else there is refused, naming the key.<br>- **Requests that are not priced:** one with every usage field 0 costs 0 whatever its model, such as Claude Code's `<synthetic>` rows. Any other request of a model with no price has cost `None`, and its model and request count go under `"unpriced"`. Totals are over priced requests, and `show` says what they leave out. |
| D6 | **Roles.** `ROLES = ("planning", "implementing", "review", "fixing")`. The first rule that applies gives the role:<br>1. A row with no agent id is in a main session → `planning`. That covers orchestration, the pick and `work batch` runs.<br>2. A subagent whose `agentType` ends in `pr-reviewer` → `review`.<br>3. A subagent whose meta `description` starts with `batch-<n> review` → `review`; with `batch-<n> fix` → `fixing`; with `batch-<n> t<k>` → `implementing`. building-a-batch gives these descriptions (Task 5).<br>4. Otherwise, by time: a subagent that started before `first_review` (or with no review at all) → `implementing`, else `fixing`.<br>`measure_batch_read.agent_types(dir)` reads each `agent-<id>.meta.json` as `{id: (agentType, description)}`. A meta file that is not a JSON object is refused, naming it. Only the role words of the description reach the measurement. |
| D7 | **What a review counts.** From `batch_findings.reviews(root, batch)`:<br>- `findings`: one entry per finding, with `finding`, `review`, `grade`, `triage` and `item`;<br>- `findings_by_grade`: all three grades, 0 included;<br>- `findings_by_triage`;<br>- `reviews`: one entry per review, with `review`, `result` and `findings`.<br>A **review defect** is a `fix now` finding: an observation is not a fault. `defects.review` counts them by item. |
| D8 | **The record.** It is `.shop/records/measurements/<date>-batch-<n>.md`, written by `measure_write` with `name = "batch-<n>"`, so the frontmatter id is `measurement/<context>/<date>-batch-<n>`. The body is `# Measurement of batch-<n>`, then `## Summary` (`measure_batch_show.summary(figures)`), then the JSON block. `--replace` writes over the day's record and is refused without it (`check_unwritten`). The record is written, not committed: the session commits it with its analysis (analyzing-a-batch), as `measure initiative`'s record is today. |
| D9 | **The figures' JSON** (`measure_batch.figures_of`), with keys in this order:<br>- `batch`, `status`, `pull_request`, and `items` (each with `item`, `title`, `status`);<br>- `window` (`started`, `first_review`, `built`, `closed`);<br>- `wall_time_seconds`, `wall_time`, `waiting_for_merge_seconds`;<br>- `session_time_seconds`, `session_time`;<br>- `tokens` (`output_tokens`, `new_input_tokens`, `cache_read_tokens`), where new input is input plus cache writes as in `measure_build.KINDS`;<br>- `cost`, `unpriced`, `prices_as_of`;<br>- `cost_by_role`: every role of D6, each with `sessions`, `session_time_seconds`, `session_time`, the three token kinds and `cost`;<br>- `sessions` (each with `session`, `agent`, `agent_type`, `role`, `started`, `requests`, `session_time_seconds`, the three token kinds, `cost`), then `sessions_from` and `sessions_found`;<br>- `reviews`, `findings`, `findings_by_grade`, `findings_by_triage`;<br>- `defects` (`review`: {item: count}, `after_merge`: {item: count}, `per_item`);<br>- `knobs` (D10);<br>- `goals` (`wall_time_seconds`, `cost`, `defects_per_item`).<br>Durations use `measure_build.duration`. |
| D10 | **The knobs** (design goal 8: batch size, review depth, the readiness bar), as the batch ran with them:<br>- `batch_size`: `batch_pick.batch_size(root)`;<br>- `items`: the plan's task count;<br>- `changed_lines`: the sum of `git diff --numstat <range> -- . ':(exclude).shop'` (a binary file counts 0) over the `range` of the last review record, or `null` with no review;<br>- `size_limit`: `[review] size`, default `batch_brief.SIZE`;<br>- `reviews`: the review count;<br>- `readiness_bar`: `"mechanical"`, the one bar there is (design § the session's calls).<br>Nothing here sets a knob. |
| D11 | **A defect after the merge.** The command is `measure defect <item> --says "<the fault and how to reproduce it>"`.<br>- **Refusals,** each changing nothing: an item that is not `delivered` (naming its label and status); an item in no batch; a batch (`batch_plan.of_item`) that is not `merged`; `--says` empty or only whitespace.<br>- **The file** is `.shop/batches/<n>/defect-<k>.md`, with k one more than the batch's highest. Its frontmatter is `id: defect/<context>/batch-<n>/d<k>`, `kind: defect`, `batch: batch-<n>`, `item: b<j>`, `date: <today>`. The body is `# batch-<n> d<k>`, then the text.<br>- **The commit:** it is committed on the current branch alone (`workqueue.committed`), as `measure defect: batch-<n> d<k> of b<j> "<title>"`. It prints the file's path. A defect is state traced to its item, like the batch's reviews.<br>- **Its place in the measurement:** `measure batch` counts it under `defects.after_merge` for its item. `measure_defect.parse(render(d), rel) == d`, and any other shape is refused as `<rel>: <field> …`. |
| D12 | **`measure compare` of batches.** An argument of the form `batch-<n>` resolves to the newest `.shop/records/measurements/*-batch-<n>.md` by name, which is by date. Any other argument is a path, as today. A batch with no measurement is refused: `no measurement of batch-2 in .shop/records/measurements/; run measure batch batch-2`.<br>- **Two batch measurements:** `measure_batch_show.compare` prints `total \| <name a> \| <name b> \| ratio`. The rows are wall time, session time, the three token kinds, cost, defects per item and each role's cost (`<role> cost`), then the findings by grade.<br>- **Two initiative measurements:** printed as today.<br>- **One of each:** refused, `measure compare: <a> is a batch's measurement and <b> is not`.<br>`measure show` on a batch measurement prints the summary and the sessions table. |
| D13 | **Scenario handlers** live in `tests/scenarios/telemetry_handlers.py`, binding with `bind_all`. They reuse what exists:<br>- the batches world builds the batch: `T.prepare`, `T.ensure_batch`, `make_batch`;<br>- the backlog Givens write the items: `GivenK_A item`, `GivenR in`, `GivenR of` → `OF_GIVENS["pull request"]`;<br>- batch-measurement's `include` and `prints` Thens read the run. The When sets `step.context["world"]` to an object with `code`, `out`, `err`, `record()`, `figures()` and `written()`, the attributes those handlers use.<br>New registry keys: `WhenRuns` `` `measure batch` ``, `` `measure defect` ``, `` `measure compare batch-2 batch-3` ``, and `GivenK review finding`.<br>Locals, each returning `False` unless `step.context.get("telemetry")` (set by the three Whens) or the kind is its own: `GivenR review finding` (`on`), `ThenDoes measurement` and `ThenR measurement`, `ThenDoes defect` and `ThenR defect` (`of`, `for`), and `ThenDoes review finding` (`include`). |
| D14 | **Where a batch's measurement comes from in the workflow.** building-a-batch gives each subagent a description: `batch-<n> t<k> b<j>` for a task, `batch-<n> review <k>` for the pr-reviewer, and `batch-<n> fix f<m>` for a fix. After `work batch merged`, the session runs `measure batch <batch>` and commits the record. shaping-items says that a bug in what a delivered item built is first recorded with `measure defect <item> --says …`, then shaped as an item. analyzing-a-batch reads `measure batch`'s record. `measure initiative` stays for `work run` until plan 9. |
| D15 | **0060 is superseded** by a new `0078-measure-a-batch.md`, which is `accepted`, `tier: requirement`, `enforced_by: [telemetry#r1, telemetry#r2, telemetry#r3, telemetry#r4]` and `supersedes: [design-decision/measure-an-initiative]`. In 0060's frontmatter `status` becomes `superseded`, and its `tier` and `enforced_by` are removed, since history carries no tier (plan-6 D3, pinned by `test_the_sort_holds_its_totals`). Its `## Decision` is not edited. telemetry's `rests_on` gains `design-decision/measure-a-batch`. batch-measurement keeps resting on 0060 until plan 9 retires it, which `model check` allows, since standing is by kind. |
| D16 | **Knob changes are decisions:** a new `0079-a-knob-is-changed-by-a-decision.md`, `accepted`, `tier: judgement`. Its `## Decision`: "A change to `batch_size`, to `[review] size` or `[review] checks` of `.shop/delivery.toml`, or to the readiness bar is made with a design-decision that gives the figures of `measure compare` for the batches before and after, and names the goal it trades (wall time, cost, defects per item)." It is a judgement decision, so it reaches the batch's subagents and the pull request's reviewer (plan-6 D15). No test can check that a decision was written. |
| D17 | **What this plan leaves for plan 9:** `measure initiative`, batch-measurement and `batch-analyst` (started by `work run`); the glossary's `measure` actor; the README's 0.23.0 history. The plugin's README gains one bullet for `measure batch`, `measure defect` and `compare` by batch name. |
| D18 | **A real `pr-reviewer` run is measured** in Task 6's smoke run (plan 5's open problem):<br>- a scratch batch, built with `work batch` and the stand-in gh;<br>- one real reviewer subagent dispatched on its brief, with the description `batch-1 review 1`;<br>- `measure batch batch-1 --sessions <the implementer's own project directory>`.<br>The installed plugin may lack `pr-reviewer`, since it is older than this branch. Then the reviewer is a general-purpose subagent given `agents/pr-reviewer.md`'s body and the brief's path, and its role still comes from the description (D6, rule 3). Its cost is the plan's only spend on a model, about a dollar. |
| D19 | **No `--json` for `measure batch`.** It writes a record whose JSON is the figures (0058). `show` reads it. |

## Review Focus

These are the input classes the spec implies but no line's check exercises, most likely to bite first. Each has its
test in the task named.

1. **Sessions that are not the batch's.** The person's store holds every project's sessions and sessions from before
   and after the batch. Only the root's own project directory may be read. Inside it, only requests inside the window
   count for a main session, and a subagent that started before `work batch start` does not count. A missing
   directory measures the batch without sessions and says so.
   Pinned in Task 2: `test_only_the_roots_project_directory_is_read`, `test_only_the_windows_requests_count`,
   `test_a_batch_with_no_transcripts_is_measured_without_sessions`.
2. **One request written in several rows, and requests that cannot be priced.** Claude Code repeats a request's usage
   on each content block's row. A `<synthetic>` row has zero usage, and a model may be missing from the table. The
   cost must not double, and must never be guessed.
   Pinned in Task 1: `test_a_request_in_several_rows_is_counted_once`, `test_zero_usage_costs_nothing`,
   `test_an_unpriced_model_is_named_not_guessed`, `test_one_hour_cache_writes_cost_twice_the_input`.
3. **The wrong role.** A pr-reviewer whose `agentType` is general-purpose, a fix subagent started after the first
   review, a subagent with no meta file, and the main session must each land in their role. A cost by role that puts
   the review under fixing would mislead the knob tuning.
   Pinned in Task 2: `test_each_session_has_its_role` (parametrised over D6's four rules).
4. **A defect against the wrong thing.** An item still `in-batch`, an item never in a batch, an item of an
   `abandoned` batch, and an empty `--says` are each refused and change nothing. A second defect is `d2`. A defect of
   batch-1 never counts in batch-2's measurement.
   Pinned in Task 3: `test_a_defect_needs_a_delivered_item_of_a_merged_batch` (parametrised),
   `test_the_next_defect_is_numbered_on`, `test_a_defect_counts_in_its_own_batch_only`.
5. **`compare` by name over records that do not line up.** A batch measured on two days gives the newest. A batch
   never measured is refused, naming `measure batch`. A batch's record set against an initiative's is refused. Old
   initiative records still compare as before.
   Pinned in Task 4: `test_a_batch_name_takes_its_newest_measurement`, `test_an_unmeasured_batch_is_refused`,
   `test_a_batch_and_an_initiative_do_not_compare`, and batch-measurement's r21 and r22 scenarios unchanged.

---

### Task 1: Prices and the transcripts' requests

**Files:**
- Create: `scripts/measure_cost.py`, `scripts/measure_batch_read.py`, `tests/scripts/measure_batch_testing.py`,
  `tests/scripts/test_measure_cost.py`, `tests/scripts/test_measure_batch_read.py`
- Modify: `CLAUDE.md`, with two rows after the `scripts/measure` row:
  - `scripts/measure_cost.py`: "the price of a request: the dated table of each model's input, output and cache-read
    price, `.shop/delivery.toml`'s `[prices]` over it, cache writes by their time to live, and an unpriced model
    named, never guessed (telemetry)";
  - `scripts/measure_batch_read.py`: "the transcripts of a batch's sessions: each distinct request with its model and
    tokens, each subagent's type and description from its meta file, and the root's project directory in Claude
    Code's store (telemetry)".

**Interfaces:**
- Consumes: `measure_read.assistant_rows`, `request_key`, `moment`, `store_dir`, `Refused`; `batch_git.delivery`.
- Produces, in `measure_cost.py`:
  - `AS_OF = "2026-10-06"`, `PRICES: dict[str, tuple[float, float, float]]` (D5), `WRITE_5M = 1.25`, `WRITE_1H = 2.0`.
  - `prices(root) -> dict[str, tuple[float, float, float]]`: PRICES with the overrides of D5.
  - `price_of(model: str | None, table) -> tuple | None`: by the longest key the model starts with.
  - `cost(request, table) -> float | None`: dollars, unrounded. The request has these attributes: `model`,
    `input_tokens`, `cache_write_5m_tokens`, `cache_write_1h_tokens`, `cache_read_tokens` and `output_tokens`.
- Produces, in `measure_batch_read.py`:
  - `@dataclass Request: key, session: str, agent: str | None, at: datetime, model: str | None, input_tokens: int,
    cache_write_5m_tokens: int, cache_write_1h_tokens: int, cache_read_tokens: int, output_tokens: int`, with the
    property `new_input_tokens` (input plus both writes).
  - `requests_of(directory) -> list[Request]`: D4's reading, sorted by `at`. A directory that is missing gives `[]`.
  - `agent_types(directory) -> dict[str, tuple[str | None, str | None]]`: D6's meta files.
  - `project_dir(root) -> Path`: D2.
- Produces, in `measure_batch_testing.py` (test helpers, not a test module):
  - `store_rows(session, times, agent=None, model="claude-opus-5-5", usage=None, rows_per_request=1) -> str`: Claude
    Code's raw rows, `requestId` `<session|agent>-q<n>`, at each of `times` (ISO strings).
  - `write_session(project, session, text)` writes `<project>/<session>.jsonl`.
  - `write_agent(project, session, agent, text, agent_type=None, description=None)` writes
    `<project>/<session>/subagents/agent-<agent>.jsonl` and, when either value is given, its `.meta.json`.

- [ ] **Step 1: Write the failing tests.**
  `test_measure_cost.py`:
  - `test_a_request_is_priced_by_its_model`: 1,000,000 output tokens of `claude-opus-5-5` cost 20.0, and 1,000,000
    input tokens cost 4.0.
  - `test_a_dated_model_takes_the_longest_key`: `claude-opus-5-5-20261001` prices as `claude-opus-5-5`, and
    `claude-opus-5-1` as `claude-opus-5`.
  - `test_one_hour_cache_writes_cost_twice_the_input` (Review Focus 2): 1,000,000 `cache_write_1h_tokens` cost 8.0,
    and 1,000,000 `cache_write_5m_tokens` cost 5.0.
  - `test_zero_usage_costs_nothing` (Review Focus 2): model `<synthetic>`, all zero → `0.0`.
  - `test_an_unpriced_model_is_named_not_guessed` (Review Focus 2): model `claude-new-9` with tokens → `None`.
  - `test_delivery_overrides_a_price`: `[prices."claude-opus-5-5"]` with input 1, output 2, cache_read 0.1 →
    1,000,000 output cost 2.0. With `input = "x"`, `prices` raises `Refused` naming `prices.claude-opus-5-5`.

  `test_measure_batch_read.py`, on `tmp_path`:
  - `test_a_request_in_several_rows_is_counted_once` (Review Focus 2): 3 rows of one `requestId`, output 5, 9 and 9,
    give one `Request` with output 9 and the earliest time.
  - `test_cache_writes_are_read_by_their_time_to_live`: `cache_creation` with `ephemeral_1h_input_tokens: 13` gives
    `cache_write_1h_tokens == 13`. With only `cache_creation_input_tokens: 7`, it gives `cache_write_5m_tokens == 7`.
  - `test_a_subagent_is_named_by_its_agent_id`: a row with `agentId: "a1"` under `<s>/subagents/` gives
    `session == s` and `agent == "a1"`.
  - `test_agent_types_are_read_from_meta`: `{"a1": ("shopsystem-bdd:pr-reviewer", "batch-1 review 1")}`. A meta file
    `[]` is refused, naming its path.
  - `test_an_unknown_row_is_refused_naming_it`: a line `not json` → `Refused` naming the file and `:1`.
  - `test_the_project_directory_of_a_root`: with `CLAUDE_CONFIG_DIR=/s`, the root `/home/x/re.po/.claude/w` gives
    `/s/projects/-home-x-re-po--claude-w`.
  - `test_a_missing_directory_has_no_requests`: `[]`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch_read.py -q | tail -3`
  Expected: FAIL with `ModuleNotFoundError: No module named 'measure_cost'`.

- [ ] **Step 3: Implement** `measure_cost.py` and `measure_batch_read.py` (D2, D4-D6). `requests_of` iterates
  `sorted(Path(directory).rglob("*.jsonl"))`, as `read_transcripts` does.

- [ ] **Step 4: Run them, and the measure tests.**
  Run: `python3 -m pytest tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch_read.py tests/scripts/test_measure_runs.py tests/scenarios/test_batch_measurement.py -q | tail -1`
  Expected: all pass. batch-measurement's 22 scenarios are unchanged.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - taking the sum, not the max, over a request's rows fails `test_a_request_in_several_rows_is_counted_once`;
  - pricing 1 h writes at 1.25 fails `test_one_hour_cache_writes_cost_twice_the_input`;
  - a shortest-key match fails `test_a_dated_model_takes_the_longest_key`.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/measure_cost.py scripts/measure_batch_read.py tests/scripts/measure_batch_testing.py tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch_read.py`
  Expected:
  - the suite: `8 xfailed`, no failures, passed = 1402 + the new tests;
  - `size` silent;
  - `check` clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/measure_cost.py scripts/measure_batch_read.py tests/scripts/measure_batch_testing.py \
    tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch_read.py CLAUDE.md
  git commit -m "measure: the price of a request and the requests of a store's transcripts, for a batch's measurement (telemetry)"
  ```

### Task 2: `measure batch` writes a batch's measurement (r1, r2)

**Files:**
- Create:
  - `scripts/measure_batch_sessions.py`, `scripts/measure_batch.py`, `scripts/measure_batch_show.py` (the summary
    only; Task 4 grows it);
  - `tests/scripts/test_measure_batch.py`, `tests/scenarios/telemetry_handlers.py`.
- Modify:
  - `scripts/measure`: the subcommand `batch <batch> [--sessions DIR] [--replace]` and the contract's paragraph.
  - `scripts/measure_write.py`: `path_of`, `check_unwritten` and `text_of` take any name; `text_of` gains
    `summary=""`, written after the heading and before the JSON block.
  - `tests/scenarios/test_telemetry.py`: binds with `bind_all`, like `test_decision_tiers.py`.
  - `spec/capabilities/telemetry.md`: `unbuilt: [r3, r4]`, and a new `## Implementation, may change` with bullets for
    D2, D3, D4, D5, D6 and D8, each one sentence.
  - `CLAUDE.md`:
    - the `scripts/measure` row now reads "the `measure` command: `batch` (`measure_batch*.py`), `defect`
      (`measure_defect.py`), `initiative` (reading `measure_read.py`, figures `measure_build.py`, the record
      `measure_write.py`) and `show`, `compare` (`measure_show.py`, a batch's `measure_batch_show.py`)";
    - a new row, `scripts/measure_batch.py` with `scripts/measure_batch_sessions.py`: "`measure batch`: a batch's
      window from git, its sessions in the window with their role and session time, its review findings, defects and
      knobs (telemetry)";
    - `telemetry` added to the handlers row.

**Interfaces:**
- Consumes: Task 1's `requests_of`, `agent_types`, `project_dir`, `prices`, `cost`; `batch_plan.find`; `batch_findings.reviews`;
  `backlog_items.find`, `label`; `batch_pick.batch_size`; `batch_brief.SIZE`; `batch_git.delivery`;
  `measure_build.duration`, `KINDS`; `measure_write`.
- Produces, in `measure_batch_sessions.py`:
  - `IDLE = 300`, `ROLES = ("planning", "implementing", "review", "fixing")`.
  - `role_of(agent: str | None, kind: tuple[str | None, str | None], started, first_review) -> str` (D6).
  - `sessions_of(requests, types, window: tuple, first_review, table) -> list[dict]`: D4's counting, one dict per main
    session and per subagent (D9's `sessions` entries), in order started.
  - `roles_of(sessions) -> dict[str, dict]`: every role, zeros included.
- Produces, in `measure_batch.py`:
  - `now() -> datetime` (aware, UTC).
  - `window_of(root, batch) -> dict[str, str | None]` (D3).
  - `findings_of(root, batch) -> dict`: the keys `reviews`, `findings`, `findings_by_grade`, `findings_by_triage`
    (D7).
  - `knobs_of(root, batch, reviews) -> dict` (D10).
  - `figures_of(root, name, sessions_dir=None) -> dict` (D9). In this task `defects.after_merge` is `{}`, and Task 3
    fills it. A `workqueue.Refused` from the batch's files is raised again as `measure_read.Refused`.
- Produces, in `measure_batch_show.py`: `summary(figures) -> str`. It gives a `totals` table (`wall time`, `session
  time`, `waiting for merge`, `output tokens`, `new input tokens`, `cache-read tokens`, `cost`) and a `cost by role`
  table (`role | sessions | session time | output tokens | new input tokens | cache-read tokens | cost`). Then come
  `review findings by grade`, `defects`, `knobs`, and a line for `unpriced` or "no transcripts at <dir>" when either
  applies. It uses `measure_show.table`.
- `measure batch batch-1` prints the record's path relative to the root and exits 0.
- Produces, in `telemetry_handlers.py`, D13's handlers for r1 and r2:
  - `Ran(step, done)`: the duck world: `code`, `out`, `err`, `record()` (the printed path under the repository),
    `figures()` (its JSON block), `written()`.
  - `run_measure(step, *args) -> Ran`: `step.run("measure", *args, env=…)` with
    `CLAUDE_CONFIG_DIR=<T.outside(step)>/store`. It sets `step.context["world"]` and `["telemetry"]`.
  - `WhenRuns` `` `measure batch` `` runs `T.prepare`, `T.ensure_batch`, writes a review record for each given review
    finding (below), commits, then `run_measure(step, "batch", T.batch_name(step, <the batch>))`.
  - `GivenK review finding` records it under `T.given(step, "review finding", name)`.
  - The local `GivenR review finding` (`on`) sets its pull request.
  - The review record is `batch_findings.render(Review(1, "batch-1", "review/ex.com/prod/ctx/batch-1/review-1", <the
    pull request's URL>, <head of batch-1>, "<forked_from>..<head>", "fix-now", "One finding.", [Finding("f1",
    "Important", "fix now", "a fault", <an in-batch item of the batch>, "src/x.txt:1", "")]))`, written at
    `.shop/batches/1/review-1.md` and committed on main.
  - The locals `ThenDoes measurement` (`write`: the printed path exists under `.shop/records/measurements/`),
    `ThenR measurement` (`of`: `figures()["batch"] == T.batch_name(step, b1)`) and `ThenDoes review finding`
    (`include`: `figures()["findings_by_grade"]["Important"] >= 1`, and the record's text holds `Important`).

- [ ] **Step 1: Write the failing script tests** (`test_measure_batch.py`).
  - The repository is the one `review_testing.published` builds: `batch_repo`, two items, the batch reviewed and
    published.
  - Records are added with `work batch reviewed` (FIX_NOW_B1, then FIXED_F1 after a fix, as `test_batch_fix_loop.py`
    does), and the merge with `test_batch_close.merge`.
  - `CLAUDE_CONFIG_DIR` is `tmp_path / "store"`, and the transcripts are written there by Task 1's helpers.
  - Each request's time is one of the commit times that `git log --format=%cI -- .shop/batches/1/plan.md` gives.

  The tests:
  - `test_a_merged_batch_is_measured`: `measure batch batch-1` exits 0, prints
    `.shop/records/measurements/<today>-batch-1.md`, and the record's text holds `wall time`, `session time`,
    `tokens` and `cost by role`. `figures["status"] == "merged"`, and `items` names b1 and b2. `window` has all four
    moments. `wall_time_seconds >= 0`.
  - `test_the_findings_are_counted_by_grade`: after FIX_NOW_B1, `findings_by_grade == {"Critical": 0, "Important": 1,
    "Minor": 1}`. `defects["review"] == {"b1": 1}`, since the observation is not a defect. `reviews[0]["result"] ==
    "fix-now"`.
  - `test_each_session_has_its_role` (Review Focus 3), parametrised and run on `sessions_of` with fixed datetimes:
    - a main session → `planning`;
    - `agentType` `shopsystem-bdd:pr-reviewer` → `review`;
    - general-purpose with description `batch-1 review 2` → `review`;
    - `batch-1 fix f1` → `fixing`;
    - `batch-1 t2 b2` → `implementing`;
    - no meta, started before `first_review` → `implementing`;
    - no meta, started after it → `fixing`;
    - no review at all → `implementing`.
  - `test_only_the_windows_requests_count` (Review Focus 1):
    - a main session with one request a day before `started`, two inside, and one a day after `built`: 2 requests,
      session time = their gap (≤ 300 s);
    - a subagent whose first request is inside and its last a day later: counted whole;
    - a subagent that started a day before: absent.
  - `test_session_time_leaves_out_idle_gaps`: requests at 0, 60, 120 and 1000 s give `session_time_seconds == 120`.
  - `test_only_the_roots_project_directory_is_read` (Review Focus 1): an in-window session written under another
    project directory of the same store is not counted. With `--sessions <that directory>` it is.
  - `test_a_batch_with_no_transcripts_is_measured_without_sessions` (Review Focus 1): no store → exit 0,
    `sessions_found == 0`, and the summary says `no transcripts at`.
  - `test_the_cost_by_role_sums_to_the_cost`: with one priced request per role, `sum(r["cost"] for r in
    cost_by_role.values()) == cost`, rounded to 6 places. A request of `claude-new-9` gives `unpriced ==
    {"claude-new-9": 1}`.
  - `test_the_knobs_are_given`: `batch_size == 4`, `items == 2`, `reviews` is the count of `review-<k>.md`,
    `size_limit == 1000`, and
    `changed_lines` equals the sum of `git diff --numstat` over the review's range less `.shop/`.
  - `test_an_open_batch_is_measured_so_far`: an `in-review` batch with `measure_batch.now` monkeypatched has
    `window["closed"] is None` and `wall_time_seconds` from `started` to that now.
  - `test_a_measurement_is_not_written_over`: a second run exits 1 naming the record and changes nothing. With
    `--replace` it exits 0.
  - `test_an_unknown_batch_is_refused`: `measure batch batch-9` exits 1 naming `batch-9` and writes nothing.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_measure_batch.py -q | tail -3`
  Expected: FAIL. `measure` has no subcommand `batch` (exit 2), and there is no `measure_batch_sessions`.

- [ ] **Step 3: Implement D3, D4, D6-D10** in the three modules, then `measure_write` and the `batch` subcommand.

- [ ] **Step 4: Run them, and the measure scenarios.**
  Run: `python3 -m pytest tests/scripts/test_measure_batch.py tests/scripts/test_measure_cost.py tests/scripts/test_measure_batch_read.py tests/scenarios/test_batch_measurement.py -q | tail -1`
  Expected: all pass. batch-measurement's records are unchanged by the `summary=""` default.

- [ ] **Step 5: The r1 and r2 handlers; take r1 and r2 out of `unbuilt:`.** Switch `test_telemetry.py` to
  `bind_all`.
  Run: `python3 -m pytest tests/scenarios/test_telemetry.py tests/scenarios/test_batches.py tests/scenarios/test_supervision.py tests/scenarios/test_batch_measurement.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected:
  - telemetry: `2 passed, 2 xfailed`;
  - batches, supervision and batch-measurement pass as before, since the locals return `False` for them
    (supervision's "commits the measurement m1" included);
  - `every step has one handler`.

- [ ] **Step 6: Mutations, each reverted.** Each must turn its test red:
  - counting an `observation` as a review defect fails `test_the_findings_are_counted_by_grade`;
  - dropping the window filter for main sessions fails `test_only_the_windows_requests_count`;
  - dropping rule 3 of D6 fails the `batch-1 review 2` case;
  - r2 left in `unbuilt:` fails the suite as `XPASS(strict)`.

- [ ] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/model check | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/measure scripts/measure_write.py scripts/measure_batch.py scripts/measure_batch_sessions.py scripts/measure_batch_show.py tests/scripts/test_measure_batch.py tests/scenarios/telemetry_handlers.py tests/scenarios/test_telemetry.py`
  Expected:
  - the suite: `6 xfailed`, no failures;
  - generate: exit 0;
  - `model check` at its baseline, 53/16/19/0;
  - `size` silent, with `scripts/measure` ≤ 150 and `measure_write.py` ≤ 50;
  - `check` clean.

- [ ] **Step 8: Commit.**
  ```bash
  git add scripts/measure scripts/measure_write.py scripts/measure_batch.py scripts/measure_batch_sessions.py \
    scripts/measure_batch_show.py tests/scripts/test_measure_batch.py tests/scenarios/telemetry_handlers.py \
    tests/scenarios/test_telemetry.py spec/capabilities/telemetry.md CLAUDE.md
  git commit -m "measure batch: a batch's wall time, session time, tokens and cost by role from git and its sessions' transcripts, its review findings by grade (telemetry r1, r2)"
  ```

### Task 3: `measure defect` traces a fault after the merge to its item and batch (r3)

**Files:**
- Create: `scripts/measure_defect.py`, `tests/scripts/test_measure_defect.py`
- Modify:
  - `scripts/measure`: `defect <item> --says TEXT`, and the contract's paragraph.
  - `scripts/measure_batch.py`: `figures_of` fills `defects.after_merge` and `per_item`, and `goals`.
  - `tests/scenarios/telemetry_handlers.py`: the r3 handlers.
  - `spec/capabilities/telemetry.md`: `unbuilt: [r4]`, and one Implementation bullet for D11.
  - `CLAUDE.md`: the row `scripts/measure_defect.py`: "`measure defect`: a fault found after the merge, written
    `.shop/batches/<n>/defect-<k>.md` against its delivered item and committed, and the defects of a batch read back
    (telemetry)".

**Interfaces:**
- Consumes: `backlog_items.find`, `label`; `batch_plan.of_item`, `BATCHES`, `number`; `workqueue.frontmatter`,
  `read`, `committed`, `context_path`; `measure_write.today`.
- Produces, in `measure_defect.py`:
  - `@dataclass Defect: name: str, ident: str, batch: str, item: str, date: str, says: str`.
  - `rel_of(batch_name, k) -> str`, `parse(text, rel) -> Defect`, `render(defect) -> str`.
  - `defects(root, batch_name) -> list[Defect]`: by k. A `defect-*.md` not named `defect-<k>.md` is refused.
  - `record(root, item_name, says) -> str`: D11's checks, file and commit. It returns the rel path.
- `measure defect b1 --says "…"` prints that path and exits 0. A refusal exits 1 and changes nothing.
- Produces, in `telemetry_handlers.py`:
  - `WhenRuns` `` `measure defect` ``: the item's batch is given `status: merged`, then `T.prepare`,
    `T.ensure_batch`, and `run_measure(step, "defect", B.ident(i1), "--says", "abandon leaves it started; run work
    abandon i1")`;
  - the locals `ThenDoes defect` (`write`: the printed path exists and `git log -1 --format=%s` names it) and
    `ThenR defect` (`of`: its frontmatter `item` is `B.ident(i1)`; `for`: its `batch` is `T.batch_name(step, b1)`).

- [ ] **Step 1: Write the failing tests** (`test_measure_defect.py`, on the merged batch of Task 2's fixture,
  imported from `test_measure_batch`):
  - `test_a_defect_is_written_and_committed`: exit 0, it prints `.shop/batches/1/defect-1.md`, and the file parses as
    `Defect("d1", "defect/ex.com/prod/ctx/batch-1/d1", "batch-1", "b1", <today>, "the fault")`. The last commit's
    subject is `measure defect: batch-1 d1 of b1 "Abandon"` and touches only that file. `git status --porcelain` is
    empty.
  - `test_a_defect_needs_a_delivered_item_of_a_merged_batch` (Review Focus 4), parametrised. Each case exits 1, names
    the words given, and leaves the tree and HEAD as they were:
    - b2 still `in-batch` (the batch not merged) → `in-batch`;
    - an item `ready` in no batch → `no batch`;
    - an item of an `abandoned` batch → `abandoned`;
    - `--says "  "` → `--says`.
  - `test_the_next_defect_is_numbered_on` (Review Focus 4): two defects → `defect-1.md` and `defect-2.md`, names `d1`
    and `d2`.
  - `test_a_defect_round_trips`: `parse(render(d), rel) == d`. A file with `kind: bug` is refused naming `kind`.
  - `test_a_defect_counts_in_its_own_batch_only` (Review Focus 4): after a defect of b1 in batch-1, `measure batch
    batch-1` gives `defects["after_merge"] == {"b1": 1}`, `per_item == 1.0` (the review's `fix now` plus this one,
    over 2 items) and `goals["defects_per_item"] == 1.0`. A second batch, batch-2, gives `after_merge == {}`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_measure_defect.py -q | tail -3`
  Expected: FAIL. There is no subcommand `defect`.

- [ ] **Step 3: Implement D11** and the counts in `figures_of`.

- [ ] **Step 4: The r3 handlers; take r3 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scripts/test_measure_defect.py tests/scripts/test_measure_batch.py tests/scenarios/test_telemetry.py tests/scenarios/test_backlog.py tests/scenarios/test_batches.py -q | tail -1; python3 scripts/features vocab --check | tail -1`
  Expected: all pass, telemetry `3 passed, 1 xfailed`; `every step has one handler`.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - accepting an `abandoned` batch fails the `abandoned` case;
  - numbering from the count of files rather than the highest k fails `test_the_next_defect_is_numbered_on` once
    `defect-1.md` is removed by hand. Remove it with `git rm` alone (the person's rule).

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/measure scripts/measure_defect.py scripts/measure_batch.py tests/scripts/test_measure_defect.py tests/scenarios/telemetry_handlers.py`
  Expected: `5 xfailed`, no failures; silent; clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/measure scripts/measure_defect.py scripts/measure_batch.py tests/scripts/test_measure_defect.py \
    tests/scenarios/telemetry_handlers.py spec/capabilities/telemetry.md CLAUDE.md
  git commit -m "measure defect: a fault after the merge recorded against its delivered item and batch, and counted in the batch's measurement (telemetry r3)"
  ```

### Task 4: `measure show` and `measure compare` read batches (r4)

**Files:**
- Create: `tests/scripts/test_measure_batch_show.py`
- Modify:
  - `scripts/measure_batch_show.py`: `show`, `compare` and `resolve`.
  - `scripts/measure_show.py`: `show` and `compare` hand a batch's figures to `measure_batch_show` (D12).
  - `scripts/measure`: `compare`'s arguments may be batch names (`compare <a> <b>`, where each is a record or
    `batch-<n>`), and the contract's paragraph.
  - `tests/scenarios/telemetry_handlers.py`: the r4 When.
  - `spec/capabilities/telemetry.md`: `unbuilt: []`, one Implementation bullet for D12, and `## Not yet` (Task 5
    writes its bullets; here `- None.`).

**Interfaces:**
- Consumes: Task 2's figures; `measure_show.figures_of`, `table`, `ratio`, `cell`.
- Produces, in `measure_batch_show.py`:
  - `resolve(root, word) -> Path` (D12);
  - `show(figures) -> str`: `summary` plus the `sessions` table (`session | agent type | role | started | requests |
    session time | output tokens | new input tokens | cache-read tokens | cost`);
  - `compare(a_name, a, b_name, b) -> str` (D12).
- `measure_show.show(path)` and `measure_show.compare(first, second)` are unchanged for an initiative's records.
- Produces, in `telemetry_handlers.py`: `WhenRuns` `` `measure compare batch-2 batch-3` ``. It writes
  `.shop/records/measurements/2026-11-01-batch-2.md` and `2026-11-02-batch-3.md` through `measure_write.text_of`,
  each with figures built from the test module's `FIGURES` constant (a complete D9 dict with every role). Then it runs
  `run_measure(step, "compare", "batch-2", "batch-3")`.

- [ ] **Step 1: Write the failing tests** (`test_measure_batch_show.py`, records written from a complete D9 dict):
  - `test_compare_by_batch_name`: exit 0, and the head line is `total | batch-2 | batch-3 | ratio`. The rows hold
    `wall time`, `cost`, `planning cost`, `review cost` and `defects per item`. The cost row's ratio is `b / a`,
    rounded as `measure_show.ratio` rounds.
  - `test_a_batch_name_takes_its_newest_measurement` (Review Focus 5): with `2026-11-01-batch-2.md` (cost 1) and
    `2026-11-03-batch-2.md` (cost 3), `resolve` gives the second and `compare` prints `3.00`.
  - `test_an_unmeasured_batch_is_refused` (Review Focus 5): `compare batch-2 batch-7` exits 1 naming `batch-7` and
    `measure batch batch-7`.
  - `test_a_batch_and_an_initiative_do_not_compare` (Review Focus 5): exit 1, `is a batch's measurement and`.
  - `test_show_prints_a_batch`: `measure show <record>` prints `cost by role`, `sessions`, `review findings by grade`
    and a session's role.
  - `test_an_initiatives_records_compare_as_before`: batch-measurement r21's two records give the same output as at
    `9d765bb8`. The test pins the head `total | a | b | ratio`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_measure_batch_show.py -q | tail -3`
  Expected: FAIL. `batch-2` is read as a path, giving `no measurement at batch-2`.

- [ ] **Step 3: Implement D12.**

- [ ] **Step 4: The r4 handler; take r4 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scripts/test_measure_batch_show.py tests/scenarios/test_telemetry.py tests/scenarios/test_batch_measurement.py -q | tail -1`
  Expected: all pass; telemetry `4 passed`; batch-measurement's `show` and `compare` scenarios (r18-r22) unchanged.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - resolving the oldest record fails `test_a_batch_name_takes_its_newest_measurement`;
  - letting a mixed pair through fails `test_a_batch_and_an_initiative_do_not_compare`.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features vocab --check | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/measure scripts/measure_show.py scripts/measure_batch_show.py tests/scripts/test_measure_batch_show.py tests/scenarios/telemetry_handlers.py`
  Expected:
  - the suite: `4 xfailed`, no failures;
  - `every step has one handler`;
  - silent, with `measure_show.py` ≤ 135;
  - clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add scripts/measure scripts/measure_show.py scripts/measure_batch_show.py tests/scripts/test_measure_batch_show.py \
    tests/scenarios/telemetry_handlers.py spec/capabilities/telemetry.md
  git commit -m "measure show and compare read batches: compare takes batch names, side by side with their ratio (telemetry r4)"
  ```

### Task 5: The decisions, the skills and the docs

**Files:**
- Create:
  - `spec/decisions/0078-measure-a-batch.md` (D15);
  - `spec/decisions/0079-a-knob-is-changed-by-a-decision.md` (D16);
  - `tests/scripts/test_skill_analyzing_a_batch.py`.
- Modify:
  - `spec/decisions/0060-measure-an-initiative.md`: frontmatter only (D15);
  - `spec/decisions/index.md`, regenerated;
  - `spec/capabilities/telemetry.md`: `rests_on:` and `## Not yet`;
  - `tests/scripts/test_decision_checks.py`: the two pinned totals;
  - `skills/analyzing-a-batch/SKILL.md`, `skills/building-a-batch/SKILL.md`, `skills/shaping-items/SKILL.md`;
  - `tests/scripts/test_skill_building_a_batch.py`, `tests/scripts/test_skill_shaping_items.py`;
  - `README.md`: one bullet (D17).

**Interfaces:**
- Consumes: `model_decisions.decisions`, `batch_brief.judgement` (plan 6).
- Each decision is written in 0077's form. The id is `design-decision/missingmass.io/shopsystem/shopsystem-bdd/<slug>`,
  with `summary`, `date: 2026-11-05`, `status: accepted`, `tier`, `enforced_by` (0078 only), `supersedes` (0078
  only), `source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]`, and
  `by: "workflow simplification plan 7, decided by the planner; revisit"`. Each has a one-paragraph `## Decision`:
  - 0078: "`measure batch <batch>` measures one batch from git and its sessions' transcripts on disk: wall time,
    session time, tokens and cost by role, the pull request's findings by grade, the defects traced to their items
    (`measure defect`) and the knobs it ran with, written as one measurement record. It replaces 0060's measurement
    of an initiative, which `work run` keeps until the old queue is retired."
  - 0079: D16's text.
- telemetry's `## Not yet`:
  - "Recurring findings across batches (plan-5 D21): counted by reading `measure compare`'s rows; a count over many
    batches waits for there being many.";
  - "The third-review park (plan-5 D23) is revisited with the figures of real batches.";
  - "A price table read from a source: the table is dated (`prices_as_of`) and `.shop/delivery.toml` overrides it."

- [ ] **Step 1: Write the failing tests.**
  - In `test_decision_checks.py`, change the pinned totals of `test_the_sort_holds_its_totals` to 78 decisions, status
    `{"accepted": 28, "superseded": 48, "rejected": 2}` and tiers `{"check": 4, "requirement": 15, "judgement": 9}`.
    Change `test_the_judgement_decisions_reach_the_brief` to 9 entries, with
    `spec/decisions/0079-a-knob-is-changed-by-a-decision.md` among them.
  - Add `test_0060_is_superseded_by_measure_a_batch`. 0060's status is `superseded` with no tier. 0078 is
    `requirement` with the four telemetry ids. telemetry's `rests_on` names `design-decision/measure-a-batch`.
  - `test_skill_analyzing_a_batch.py`:
    - `test_it_measures_a_batch`: the Process names `measure batch <batch>`, `measure show`, `measure compare <earlier
      batch> <batch>`, `cost by role` and `defect`;
    - `test_a_candidate_that_changes_a_knob_is_a_decision`: it names `a-knob-is-changed-by-a-decision`;
    - `test_an_initiative_is_still_measured_until_plan_9`: it names `measure initiative`.
  - In `test_skill_building_a_batch.py`:
    - `test_each_subagent_is_described_for_its_role`: the text holds `batch-<n> t<k> b<j>`, `batch-<n> review <k>` and
      `batch-<n> fix f<m>`;
    - `test_a_merged_batch_is_measured`: it names `measure batch <batch>` after `work batch merged`.
  - In `test_skill_shaping_items.py`, `test_a_bug_in_delivered_work_is_a_defect_first`: it names `measure defect`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_decision_checks.py tests/scripts/test_skill_analyzing_a_batch.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py -q | tail -3`
  Expected: FAIL. The totals are 76, 0060 is accepted, and no skill names `measure batch`.

- [ ] **Step 3: Write the decisions, 0060's frontmatter and telemetry's `rests_on` and `## Not yet`; then the skills.**
  - **analyzing-a-batch:**
    - step 1 becomes `measure batch <batch>` (it writes the record, reading git and the sessions' transcripts;
      `--sessions` for another directory);
    - step 2 compares with the batch before;
    - step 3 judges each `fix now` finding (its review record), each defect after the merge (its `defect-<k>.md`)
      and each parked item;
    - the report's `## The delivery` table is `measure show`'s;
    - a candidate that changes a knob says it is made as a decision (`a-knob-is-changed-by-a-decision`);
    - one line keeps `measure initiative <initiative>` for an initiative of the old queue until plan 9.

    The Common Mistakes table gains the row "Adding the roles' costs by hand | `cost by role` in the measurement".
  - **building-a-batch:**
    - step 4's dispatch gives each subagent the description `batch-<n> t<k> b<j>`;
    - step 7's reviewer `batch-<n> review <k>` and its fixes `batch-<n> fix f<m>`;
    - after `work batch merged`: "`python3 <scripts>/measure batch <batch>`, and commit its record".
  - **shaping-items:** one bullet: "A bug in what a delivered item built: `python3 <scripts>/measure defect <item>
    --says "<the fault and how to reproduce it>"` first, then shape its fix as an item."
  - **README:** under `scripts/measure`, one bullet for `measure batch`, `measure defect` and `compare` by batch name.

- [ ] **Step 4: Regenerate the index; run the checks.**
  Run: `python3 scripts/model decisions && python3 scripts/model decisions --check | tail -1; python3 scripts/model check | tail -1; python3 -m pytest tests/scripts/test_decision_checks.py tests/scripts/test_skill_analyzing_a_batch.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py tests/scripts/test_batch_brief.py -q | tail -1`
  Expected:
  - `spec/decisions/index.md is current`, and `4 check decisions: 4 hold, 0 failing`;
  - `53 violations, 16 warnings, 19 unresolved references, 0 file problems`: the telemetry ids resolve and 0060 has
    no tier;
  - all pass.

- [ ] **Step 5: Mutations, each reverted.** Each must turn its test red:
  - leaving 0060's `tier: requirement` fails `test_the_sort_holds_its_totals`;
  - 0078 with `enforced_by: [telemetry#r9]` gives an unresolved reference.

- [ ] **Step 6: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/features generate --check; echo $?; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check tests/scripts/test_decision_checks.py tests/scripts/test_skill_analyzing_a_batch.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py`
  Expected: `4 xfailed`, no failures; exit 0 (`rests_on` changes no step); `11 findings: 6 L5, 5 L6`; `401 terms, 0
  problems`; silent; clean.

- [ ] **Step 7: Commit.**
  ```bash
  git add spec/decisions spec/capabilities/telemetry.md tests/scripts/test_decision_checks.py \
    tests/scripts/test_skill_analyzing_a_batch.py tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py \
    skills/analyzing-a-batch/SKILL.md skills/building-a-batch/SKILL.md skills/shaping-items/SKILL.md README.md
  git commit -m "spec: measure-a-batch supersedes measure-an-initiative, a knob is changed by a decision; the skills measure each merged batch and record defects"
  ```

### Task 6: Whole-plan verification, a real review measured, and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-7-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement of the plan is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('telemetry' in d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False 5 []`.

- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/model decisions --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only 9d765bb8...HEAD -- '*.py' scripts/measure)`
  Expected:
  - the suite: `4 xfailed`, no failures. Passed = 1402 + 4 telemetry scenarios + the new script tests, and the
    subtests stay 135;
  - timing: `2 passed`;
  - `model check`: 53/16/19/0;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `decisions --check`: `4 check decisions: 4 hold, 0 failing`;
  - generate: exit 0;
  - `vocab --check`: `every step has one handler`;
  - bindings: `every binding names a scenario`;
  - `size`: silent;
  - `check`: clean.

- [ ] **Step 3: The smoke run with a real review** (D18), in a scratch repository under
  `/home/vscode/.claude/jobs/7e9ba079/tmp/smoke7/`. Each `cp` and each `rm` is its own command (the person's rule).
  1. **Build the scratch batch.** Follow plan 5's smoke loop (`plan-5-implementation.md`, "Figures after the fixes")
     and the recipe in `tests/scripts/review_testing.py::published`:
     - the fixture spec of `tests/scripts/fixtures/generate/repo` with its context `ex.com/prod/ctx`;
     - `.shop/delivery.toml` with `[batch] tests = "python3 -c pass"`;
     - a bare `origin`;
     - the stand-in gh (`SHOPSYSTEM_WORK_GH` running `tests/scripts/stub_gh.py`, `STUB_GH_CALLS`, `STUB_GH_STATE`);
     - two ready items, `work batch start`, `resume`;
     - each task's commit made by hand, with its ids out of `unbuilt:` and `Item: b<j>`;
     - `done` for both, then `work batch review` and `work batch brief`.
  2. **Dispatch one real reviewer** with the description `batch-1 review 1`. Use the agent `shopsystem-bdd:pr-reviewer`
     if the session lists it. Otherwise dispatch a general-purpose agent whose prompt is `agents/pr-reviewer.md`'s body
     followed by the brief's path. Then run `work batch reviewed batch-1`.
  3. **Close the batch.** If the review leaves a `fix now` finding, fix it by hand with its trailers, `review` and
     `brief` again, and review once more with a second real reviewer, `batch-1 review 2`. Once it is clean, merge
     `batch-1` into `main` with `--no-ff`, write gh's state `MERGED` at that commit, and run `work batch merged
     batch-1`.
  4. **Measure it.** Run `python3 <root>/scripts/measure batch batch-1 --sessions ~/.claude/projects/<this session's
     project directory>`, from the scratch repository. Take the project directory from `measure_batch_read.project_dir`
     of this session's working directory. Then run `measure show` on the record, `measure defect b1 --says "<a fault
     found by hand>"`, `measure batch batch-1 --replace`, and `measure compare batch-1 batch-1`.

  Expected:
  - the reviewer's subagent is in `sessions` with role `review`, its tokens above 0 and a cost above 0;
  - this session's requests inside the window are `planning`;
  - `cost_by_role.review.cost` is recorded in the report against the review's wall time;
  - the second measurement has `defects.after_merge == {"b1": 1}`;
  - `compare`'s ratios are all `1`;
  - `git status --porcelain` in the scratch repository shows only the untracked records under
    `.shop/records/measurements/`;
  - no prompt, reply or description text appears in the record: grep it for a phrase of the brief, which must be
    absent.

  If no subagent can be dispatched, record that in the report as not measured, with why, and run the rest with
  transcripts written by `measure_batch_testing`.

- [ ] **Step 4: Write the implementation report** at `plan-7-implementation.md`, in `plan-6-implementation.md`'s form
  (no frontmatter):
  - Final state: each Step 2 figure as measured.
  - The smoke run: the reviewer's tokens, cost, session time and wall time; the batch's cost by role; the record's
    path in the scratch directory (not committed).
  - The commits: a table of each task's commit, what was done and its verification, the mutations included.
  - Deviations, each with its reason.
  - D1-D19, each kept or changed.
  - Open problems for plans 8-9. Among them:
    - plan 9 retires `measure initiative`, batch-measurement and `batch-analyst`, and rewrites the glossary's `measure`
      (D17);
    - the price table is dated and kept by hand (D5);
    - other sessions in the same project directory inside a batch's window are counted as planning (D2, D4), and
      `--sessions` is the way round it;
    - plan-5 D21 and D23 wait for real batches' figures.
  - Files.

- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-7-telemetry.md`:
  `| \`2026-11-04-workflow-simplification/plan-7-implementation.md\` | plan 7 executed: telemetry (\`measure batch\` from git and the sessions' transcripts, cost by role, findings by grade, knobs; \`measure defect\`; \`compare\` by batch name), 0060 superseded by measure-a-batch, knob changes as decisions, a real review measured, 4 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.

- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-7-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-7-telemetry.md
  git commit -m "records: plan 7 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-7-review.md`. It reads `<this plan's
  commit>..HEAD` on `workflow-simplification` against this plan's Review Focus and D2-D6.
