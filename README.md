# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow with one spec of capability files per
bounded context, Gherkin feature files paired with them as the contract, one human gate on the spec's Behaviour
lines, and delivery by work-items that a script, `work run`, pulls through research, plan, implementation and review.

Skills: `integrating-a-proposal`, `formulating-features`, `delivering-an-initiative`, `bdd-red-green`,
`checking-spec-consistency`, `migrating-to-capabilities`, `analyzing-a-batch`.
Agents: `capability-writer`, `feature-formulator`, `initiative-round`, `spec-checker`, `code-scout`, `bdd-planner`,
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`, `architecture-reviewer`, `trial-runner`.
Format: `docs/capability-format.md`. The design model it keeps: `docs/design-model/` (version 3).
This repository's own spec: `spec/index.md`; check it with `python3 scripts/model check`.

## Requires

The plugin depends on no other plugin. It needs, in the consuming repository's Python:

- clingo, for `model check` (`python3 -m pip install clingo`);
- pytest and pytest-bdd, for the scenarios;
- pytest-xdist, optional, to run the tests in parallel (`pytest.ini`'s `addopts = -n auto`; `-n 0` runs them in one
  process). `work run` runs the tests with `-n auto` where it is installed.

`work run` also needs the `claude` CLI on the PATH (or `$SHOPSYSTEM_WORK_CLAUDE`).

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the working copy instead.

## The layout

A consuming repository keeps (design-decision/final-layout):

- `spec/`: `index.md` (the bounded context: purpose, constraints, composition, glossary), `capabilities/<name>.md`,
  and `decisions/`, one file a decision with its index `decisions/index.md`, written by `model decisions`;
- `features/<name>.feature`, one a capability, the file of its own name;
- `.shop/work/<initiative>/`: the initiative, its proposals and its work-items, and `runs/`, what `work run`'s
  workers left;
- `.shop/records/`: observations, measurements, review findings, decision arguments and the archive;
- `.shop/delivery.toml`, `work run`'s settings, optional;
- `.shop/scratch/` and `.shop/worktrees/`, drafts, notes and the implementers' worktrees, both git-ignored.

## The workflow

- **A proposal becomes lines.** `integrating-a-proposal` has the `capability-writer` (blind to the code) merge an
  approved note into `spec/` and stops at the one gate: the added, changed and removed Behaviour lines with their
  ids, glossary entries and decisions. Nothing is written to `spec/` before the person's yes.
- **Lines are EARS.** Every Behaviour line is one EARS requirement with "shall", in one of its patterns (`When`,
  `While`, `If … then`, `Where`, or none), one response, one sentence, with a stable id `[r<n>]`
  (design-decision/behaviour-lines-are-ears). `model check` reports a line that is not (`v_e1`, `v_e2`).
- **Lines become scenarios.** `formulating-features` has the `feature-formulator` (blind to the code) write one
  scenario a line, tagged `@r<n>`, with no second approval. A scenario that passes today and whose line changes is
  kept, tagged `@deprecated`, until the work-item that turns its replacement green retires it.
- **Scenarios are delivered.** `delivering-an-initiative` drafts the initiative's work-items from the spec alone
  (`work add`), commits them and starts `work run <initiative>`. `work run` takes each work-item through its stages,
  one fresh `claude -p` worker a stage: `code-scout` researches, `bdd-planner` plans (intent, never code),
  `bdd-implementer` implements red-green under `bdd-red-green` in its own worktree, and `bdd-task-reviewer`
  reviews. It writes every status itself, merges a branch only when the work-item's scenarios and the whole suite
  pass on it, and ends printing each work-item's status and each question for the person. Exit 0: every work-item
  green; 3: a question awaits the person; 1: it stopped, saying why.
- **The spec checks itself.** `checking-spec-consistency` and the `spec-checker` judge lines against scenarios and
  against the glossary; `model check` checks the whole repository against the design model.

## `work run`

Each worker runs with `--permission-mode acceptEdits`, the plugin's directory as `--plugin-dir`, and
`--allowedTools` set for its stage: no bare Write or Edit (a worker's writes stay in the worktree it starts in), and
Bash only for `python3 -m pytest`, the plugin's scripts by path and the git commands the stage needs. Nothing runs
with permissions bypassed.

The tests it runs load the plugin's own pytest plugin, `scripts/work_items.py` (`-p work_items`, the scripts
directory on `PYTHONPATH`): `--work-item <name>` for the work-item's scenarios, and `--whole-suite` for the suite
before a merge, where a failing scenario counts as expected while another work-item that is neither `green` nor
`withdrawn` accepts its requirement. Where pytest-xdist is installed, `-n auto` is added. A repository can name its
own commands in `.shop/delivery.toml` (`[tests]`, with `{work_item}` replaced by the name; its `suite` command needs
`--whole-suite` for expected red to work). `[allowed_tools]`, a list for a stage, replaces that stage's list
(`research`, `plan`, `implement`, `review`); a bare Write or Edit in it is still dropped. Git-ignore `.shop/scratch/`
and `.shop/worktrees/`.

Before you run it:

- The initiative branch needs a remote it can push to. `work run` checks the push before every worker starts and
  pushes after every commit it makes.
- Run `work run` with the same credentials as your `git push` (for example inside the credential wrapper you push
  with). Without them its push check fails and the work-item goes to `failed`.
- Commit `.shop/work/` first: `work run` refuses to start over uncommitted changes there.

A fault (a refused push, a git failure, a worker changing `.shop/work/`, a worker ending in an error or at its turn
limit, or with no readable result) moves the work-item to `failed` and the run exits with an error naming it. Fix the
cause, then `work retry <work-item>` brings it back to where its stage started. Workers write their result first, as
`PARTIAL`, and keep it current.

## Scripts

Python 3, in `scripts/`. `--help` is each one's contract; the plugin's own tests: `python3 -m pytest`.

- `scripts/model`: read a bounded context's spec, feature files, decisions, work and records as the facts of the
  design model's grammar (`facts`), check them with clingo (`check`), list the rules (`rules`), write the decisions
  index (`decisions`), and trace a requirement to why it exists (`why`).
- `scripts/features`: count, list, tag, move and verify-moved for feature files without the test runner;
  deprecate, retire and deprecated for scenarios kept while they still pass; bindings and rebind for the titles
  test modules bind.
- `scripts/work`: `add` drafts a work-item, `show` lists every work-item with its status (`--json`), `retry`
  returns a `failed` work-item, `withdraw` withdraws one, `run` delivers an initiative.
- `scripts/tools`: the project's analysis tools behind one interface: `probe`, `install`, `map`, `tests-of`,
  `untested`, `refs`, `check`, and `size`, the tracked Python files over a line limit.
- `scripts/migrate`: `migrate run --context <owner/product/context>` takes a repository from the old system to
  this layout in one run.
- `scripts/measure`: write an initiative's measurement from `work run`'s log, its sessions and git (`measure initiative`), print one as tables (`measure show`) and
  two side by side with their ratio (`measure compare`).

## Agents: rules enforced by tools

| agent | tools | model | for |
|---|---|---|---|
| `capability-writer` | Read, Glob, Grep, Write | opus | integrating a note into `spec/`, and a repository's first `spec/`, blind to the code; writes only drafts |
| `feature-formulator` | Read, Glob, Grep, Write | opus | writing feature files from the spec, blind to the code; writes only drafts |
| `initiative-round` | Read, Glob, Grep, Bash, Write, Edit, Agent | sonnet | one round of spec work for the session that keeps the gate; dispatches only the two agents above |
| `spec-checker` | Read, Glob, Grep, Write | sonnet | judging a spec against itself, blind to the code; writes only its findings file |
| `code-scout` | Read, Glob, Grep, Bash, Write | haiku | a work-item's research for `work run`: why its scenarios are red, its file set, the tests it may break |
| `bdd-planner` | Read, Glob, Grep, Write | opus | a work-item's plan for `work run`, from the research notes, intent and never code |
| `bdd-implementer` | Read, Edit, Write, Glob, Grep, Bash, Skill | sonnet | a work-item, red-green under `bdd-red-green`, in its worktree and branch |
| `bdd-task-reviewer` | Read, Glob, Grep, Bash, Write | opus | a done work-item's review for `work run`; changes nothing |
| `bdd-branch-reviewer` | Read, Glob, Grep, Write | opus | an initiative's branch review, from its base, over every work-item; changes nothing |
| `architecture-reviewer` | Read, Glob, Grep, Bash, Write | opus | an architecture review when the person asks for one |
| `trial-runner` | Read, Glob, Grep, Bash, Write | sonnet | one trial of a plugin tool or `work run` on a target; writes only one measurement record |

Only `initiative-round` has the Agent tool. A plugin agent's `hooks` and `permissionMode` are ignored, so a role's
limits are its tools; under `work run` they are also its `--allowedTools`.

## 0.28.3: a branch review that runs nothing

- **`work run` makes the branch review's runs before it starts** (supervision r154, r155): the whole suite, each
  work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and
  `features bindings`, at the branch's head, and gives the reviewer each one's command, how it exited and its output,
  naming the commit.
- **The reviewer is given what to read** (supervision r156, r157): the commits from the initiative's base, each with its
  work-item or none, the change less `.shop/`, and the capabilities, decisions, plans, reports and review findings.
- **The branch reviewer runs nothing and has no shell tool** (review r32-r34, role-boundaries r7): a behaviour only a
  run would show is a finding with the test that would show it, marked not run. review r9 is retired. In i42 a
  branch review took about 33 turns, 6 to 8 of them commands the sandbox refused, and re-ran every check itself.

Upgrading a consuming repository from 0.28.2: update the plugin and start a session. No file is rewritten.

## 0.28.2: answers a round cannot hold go back to integration

- **An apply round names the answers its drafts do not hold** (spec-integration r46): `initiative-round` gives them in
  its result.
- **`work run` starts a new integrate round for them** (supervision r150, r151): when an apply round gives an answer
  its drafts do not hold, the proposal goes back to integration, and no formulate round starts for it until the new
  integrate round has been applied. r140 is retired for r150.
- **A formulate round that formulates nothing because the answers change lines not in `spec/`** (supervision r149,
  r152, r153) starts a new integrate round, keeps the proposal's status and counts as the round's output, where before
  the proposal was set `formulated` with nothing formulated.

Upgrading a consuming repository from 0.28.1: update the plugin and start a session. No file is rewritten.

## 0.28.1: `work run` stops visibly on questions, and spends less agent time

- **`work run <initiative>` prints each capability-proposal with its status**, and one awaiting an answer with its open
  questions, exiting 3; before, an initiative with no work-item yet exited 0 printing nothing.
- **An initiative is not set `done` while a capability-proposal of it is neither formulated, withdrawn nor merged**, by
  `work run` or by `work withdraw`.
- **A researcher's empty file set** (no file to change) is its output, not a missing one.
- **Less agent time, quality kept** (from a measurement of 801 sessions): a branch review is started only when an
  unread commit touches the initiative's own files, not for another initiative's commits on a shared branch; a
  work-item's worker is refused `pytest --whole-suite` (`work run` runs the suite at the merge); a task reviewer's brief
  gives the merged `Commits:` and the `Suite record:`; the researcher locates the change (one run of the accepted
  scenarios, no probes); the branch reviewer runs the whole suite once.

Upgrading a consuming repository from 0.28.0: update the plugin and start a session. No file is rewritten.

## 0.28.0: one set of request commands, `work list` and `work show`, and answers that redraft

- **`work list` and `work show <id>`** (work-queue r34-r39, decision 0072): `work list` lists every initiative, request
  and work-item with its status; `work show <initiative>` gives where an initiative stands (what `work status
  <initiative>` gave), `work show <work-item>` a work-item's status and open questions, `work show <request>` a
  request. `work status` and the old `work show` are retired in the spec; `work status` still runs in this release
  and is removed in a later one.
- **Requests** (requests r25, r29-r34, r44, r45; q14 lines 1, 5-7, 10-12): one set of commands and one lifecycle for
  every request; `work request` refuses, changing nothing, a request from another asker raised with `--source` or with
  neither `--raised-for` nor `--thread`, and an asker that is not the context or product whose repository raises it;
  `--raised-for <request>` names the request it is raised for. The side that writes a part of a request is taken from
  the repository, and `work outcome`, `ask` and `resolve` refuse a side writing the other side's part. Requests between
  repositories (q14 lines 2-4, 13-16, 18, 20-22) are not in this release: they will travel as GitHub issues. Until then another
  context cannot raise a request into this repository with `work request`, which raises only as the repository it runs
  in; `work run`'s raise is the one way a request reaches an upstream.
- **An integrate round that needs an upstream** (spec-integration r44; supervision r135, r136; work-queue r39; q14 lines
  23-26): the round gives the lines of a request into the upstream named in `spec/index.md`; `work run` raises them,
  raised for the request the initiative fulfils and with its delegation, holds the proposal's work-items until that
  request is `delivered`, and `work list` shows the initiative waiting on it.
- **`model check`** (design-model-check r120, r121; q14 lines 8-9): no `v17` for a request that is part of a job-thread
  kept in another repository, and neither `v17` nor `v18` for a request raised for a request of another context.
- **Answers that ask for what the drafts do not hold are redrafted** (supervision r140-r148, spec-integration r45):
  an apply round that applies nothing because of its answers sends the proposal back to a new integrate round, given
  its questions, answers and the initiative's ledger; that round drafts the lines the answers ask for, and the ids it
  writes for another capability are added to that capability's proposal, never written over it. An apply round also
  gives in its result (`unheld_answers`, spec-integration r46) each answer its applied drafts do not hold.

Upgrading a consuming repository from 0.27.0: update the plugin and start a session. No file is rewritten. Use `work
list` and `work show <id>` in place of `work show` and `work status`.

## 0.27.0: transitions from how a session ended, and the turn of an accepted request

- **`work run` moves a node by how its session ended and what its result holds** (supervision r128-r134), never by
  the outcome word a result gives (r133). A session that ends in an error, at its turn limit or with no result
  `work run` can read is a fault, whatever its result says (r128): a work-item goes to `failed`; a round's or an
  answering session's fault is recorded under its node's `## Faults` and printed, the node keeping its status. A
  result that gives questions sends them where its stage's questions go (r129): a researcher's into the planner's
  brief, the work-item moving on to `researched`; every other stage's under the node's `## Questions`, the node
  `awaiting-answer`. A result with no question and its stage's output makes the next transition (r130); one with
  neither gets a question naming the missing output (r131). Each stage's output (r132): a researcher's file set, a
  planner's plan and file set, an implementer's commits on which the work-item's scenarios and the whole suite pass,
  a reviewer's findings, an answer, an integrate or apply round's change list, a formulate round's scenario for each
  requirement its proposal adds or changes (none for a requirement of a guarantees capability, none for a term), an
  intake round's line outcome or question on each line, a gate round's questions. So a formulate round's question
  waits for its answer whatever the round reports (q13). Supervision r3, r5, r16, r112 and r113 are removed; "fault",
  "outcome" and "stage" in the glossary now speak of every session.
- **An accepted request stays in the upstream's turn** (requests r23, r24, r7 narrowed): the delivery an acceptance
  promises is the upstream's, so `work` keeps the turn there when it sets a request `accepted`, and passes it to the
  asker when the request is `delivered`.

Upgrading a consuming repository from 0.26.0: update the plugin and start a session. No file is rewritten. A request
already `accepted` in the asker's turn stays there until it is resolved, which passes the turn to the asker as before.
Workers are still asked for an outcome word; it is kept for reports.

## 0.26.0: requests and the context loop

- **Requests** (capability requests, decision 0067): the one way work enters a bounded context. `work request <title>
  --from <asker> --lines <file>` takes one in (strict EARS lines; `--source` or `--thread`; `--delegation <text>` for
  questions a session may answer in the person's place). The upstream writes each line's outcome with `work outcome`
  and its questions with `work ask`; the asker answers with `work reply`; `work turn` passes the turn; `work resolve`
  writes the requirement and version that hold each accepted line. `work start <request>` writes the initiative an
  accepted request begins. `work delegate <request> <delegation>` writes, replaces and commits a request's delegation
  (refused for a delivered, refused or withdrawn request); a UserPromptSubmit hook tells a session, in a repository
  that keeps an open request, to write a delegation the person gives with it, in the same reply. Requests are kept as
  `.shop/work/requests/q<n>.md`.
- **The context runs without a coordinator** (decision 0068): `work run` with no initiative takes every open request and
  initiative through every transition it can: the intake round of a request, the initiative of an accepted one, its
  integrate round (drafts kept on the branch, one capability-proposal a capability, ids above those other initiatives'
  drafts hold), the gate (its questions on the proposal, or one asking for approval), answers under the request's
  delegation, the apply round (the proposal's ids rewritten from what it applied), the formulate round (a question
  sends the proposal back to awaiting-answer), drafting (deprecated scenarios listed under `## Retires` by their
  `Deprecated for:`), delivery, the branch review again after its fixes, the measurement and analysis, committed, and
  the initiative set `done` once it has a green work-item and nothing open. A round that stops does not stop the
  other nodes.
- **A reviewer's question reaches implementation** (decision 0069, superseding 0063's row): `work answer <work-item>
  --change <answer>` returns the work-item to `ready` with the findings and the answer in the implementer's brief;
  `--accept` returns it to `done`. One of them is required on a reviewer's question.
- **Sessions start from the repository's state**: `work status` prints where each open initiative stands; `work note`
  appends to the initiative's ledger, now tracked as `.shop/work/<initiative>/ledger.md` (decision 0066). The
  SessionStart hook gives a new session `work status`; a PreCompact hook logs the compaction and asks for a hand-off.
- **`measure initiative`** gives each session's round trips, tool uses, dispatches and compactions, and whether the
  request behind the initiative was internal or external.
- **`work run`** delivers a work-item whose requirements are all of guarantees capabilities; a researcher's limit is
  80 turns; `work start` commits the initiative; `work add` refuses a done initiative; `work answer
  <initiative>/<name>` names a node of one initiative.
- **`model check`** reads requests: a request's form, an initiative dated after 2026-10-23 that fulfils none, a request
  neither part of a job-thread nor citing an origin, a delivered request naming a requirement the spec lacks.
- **Skills**: `delivering-an-initiative` starts `work run` and shows what it printed; `integrating-a-proposal` and
  `formulating-features` have no small-change path: every change goes through rounds.

Upgrading a consuming repository from 0.25.0: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). There is no file to rewrite: initiatives dated before 2026-10-24 need no
request, and a ledger under `.shop/scratch/` stays where it is while new lines go to the initiative's `ledger.md`.

## 0.25.0: work-items side by side, answers, and guarantees

- **`work run` runs work-items side by side** (supervision r59-r63): research and plan stages of independent
  work-items start at the same time, up to `workers` in `.shop/delivery.toml` (4 where it gives none). Implementers'
  branches merge one at a time. A work-item whose `blocked_by` names one that is not `green`, in any initiative, gets
  no worker. Each stage's `session.json` records the path of its transcript.
- **Answers, not rulings** (decisions 0063, 0064): the status `awaiting-ruling` is `awaiting-answer`.
  `work answer <work-item> <answer>` (or `<initiative>/<name>`, naming the initiative) writes a one-line answer under the work-item's `## Answers` and returns it to the
  status the stage that asked started from, so `work run` takes it up again. On an awaiting-answer capability-proposal
  it writes the answer under the proposal's `## Answers` and commits the proposal's file alone.
- **Workflow capabilities are guarantees** (decision 0065, superseding 0030 and 0043): the ten workflow capabilities
  have no scenarios and are checked by `measure` on real batches.
  `--work-item` still refuses a work-item with no scenarios: deliver such a work-item outside `work run`.
- **`measure`** counts round trips, reads an empty `session.json`, Unicode line breaks in transcripts and times
  ending in `Z`. The analysis tools answer with `--json`.
- **`model check`**'s own gaps are fixed; a capability-proposal argues one capability.
- **`delivering-an-initiative`** lists a proposal's `## Retires`, and stops before drafting when the formulation
  added or reworded a scenario that no requirement of the initiative accepts.
- **`tools install` pins ruff**; `tools check` is clean.
- **Design model v4** is written in `docs/design-model/`: requests are the one way work enters a bounded context.
  `model check` still checks the v3 rules until a later release implements v4.

Upgrading a consuming repository from 0.24.0: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). Its step "answers, not rulings" renames `awaiting-ruling` to
`awaiting-answer` in work-items and `log.jsonl`, and `## Rulings` to `## Answers`.

## 0.24.0: work-items named by ids, and upgrades between plugin releases

- **Work-items are named by ids** (decision 0061): `work add <initiative> <title>` drafts `w<n>`, `<n>` one above the
  highest of any work-item in the bounded context, writes the title as its heading and prints the id. Every command
  that names a work-item takes the id (`work retry`, `work withdraw`, `--work-item`, `work run`'s branches and stage
  directories). `model check` prints a work-item whose file is not `w<n>.md`, and two with one id.
- **Upgrades between plugin releases** (decision 0062): a repository records its plugin version in
  `.shop/plugin-version` (none means 0.23.1). `migrate status` prints the repository's version, the plugin's and each
  pending upgrade step; `migrate upgrade` applies them, records the version and commits it all in one commit, and
  refuses on uncommitted changes. When a session starts, the plugin's SessionStart hook offers the person the upgrade
  when a step is pending, and asks for a plugin update when the repository is ahead of it.
- **The first upgrade step**, "work-items named by ids": every work-item becomes `w<n>`, numbered by initiative and
  then file name; its file and `runs/` directory are renamed, its old name kept as its heading, and its name rewritten
  in its initiative's `log.jsonl` and in every work-item's `blocked_by`, `depends_on` and `for`.
- **A researcher's limit is 40 turns** (supervision r19), up from 25: researchers that finished used 14 to 30.

Upgrading a consuming repository from 0.23.x: update the plugin and start a session; accept the offered upgrade (or
run `migrate upgrade` with a clean checkout). Scripts or skills that call `work add <initiative> <name>` now pass a
title and read the printed id.

## 0.23.1: `--work-item` keeps tests that are not scenarios

- **`--work-item` keeps tests that are not scenarios** (supervision r55, r56): the option `work run` gives every
  worker's pytest now keeps a probe file or a script's test it collects, deselects only the scenarios the work-item
  does not accept, and refuses only a run that collected scenarios and none the work-item accepts. A researcher's
  probes run again, the cause of research stages ending at their turn limit since 0.22.0
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`).
- **Still known**: work-item names repeat across initiatives, and `--work-item` takes the first initiative's
  work-item of a name; 0.24.0 gives work-items `w<n>` ids.

Upgrading a consuming repository from 0.23.0: a worker's `python3 -m pytest -q` under `--work-item` now also runs the
repository's tests that are not scenarios; nothing needs to change.

## 0.23.0: faults settled, query output as JSON, the session keeps the gate, measurement on v3

- **Faults settled** (the 0.22.0 review's deferred findings, decision 0057): a fault decides a work-item's status
  whatever its worker's outcome; a session that exits with an error or prints no JSON result is a fault;
  `work withdraw <work-item>`; `work retry` returns to the status `log.jsonl` gives before `failed`; the branch
  review's directory is kept under `.shop/work/<initiative>/runs/branch-review/<k>/`, committed, logged and pushed,
  and not run again while only its own commit is new; a run first pushes an initiative branch that is ahead of its
  remote; a run with a `failed` work-item exits with an error naming each fault. The glossary gains fault, remote and
  work-item branch.
- **Query commands answer in their output** (decision 0058, superseding 0055): `--json` prints a query's whole
  result as one JSON object for `features list`, `deprecated` and `bindings`, `model why` and `rules`, and
  `work show`; a query that finds nothing exits successfully (`features list`, `model why`). The `tools` query
  commands follow in a later release.
- **The session keeps the gate** (decision 0059): `initiative-round` gains a `gate` job and appends to the
  initiative's ledger; `delivering-an-initiative` sends fixes through `work run` and new scenario rows to the blind
  formulator; a new agent, `trial-runner`, runs one trial and writes a measurement record.
- **Measurement on v3** (decision 0060): `measure initiative <initiative>` measures an initiative's deliveries from
  `work run`'s log, the stages' sessions and git, with `--sessions` for the sessions around them; `measure show` and
  `measure compare` read the records. The old `measure batch` is removed; `analyzing-a-batch` follows.
- **Known**: a researcher under `work run` can end at its turn limit, because the `--work-item` option `work run`
  gives every worker's pytest refuses the researcher's probe files
  (`.shop/records/measurements/2026-10-22-research-at-the-limit.md`); work-item names repeat across initiatives.
  Both are next. Until then, deliver a work-item whose researcher fails by a direct `bdd-implementer`.

Upgrading a consuming repository from 0.22.0: scripts that read the exit of `features list` or `model why` on an
empty answer now see success (read the output, or use `--json`); records written by the old `measure batch` cannot be
read by `measure show` (measure an initiative instead); nothing else needs to change.

## 0.22.0: one requirement per scenario, faults, and the lessons of a blind formulation

- **One requirement per scenario** (decision 0054): a scenario names exactly one `@r<n>`; `model check` reports a
  scenario naming more (v_s2); `features tag` replaces the requirement tag. Steps are shared in code.
- **Exits in words** (decision 0055): a line and its scenario say a command exits successfully or with an error;
  exit codes live in a capability's Implementation section.
- **Faults** (decision 0056): `failed`, `work retry`, a push check before every worker and a push after every commit,
  worktrees removed on exit, a session ending in an error or at its turn limit is a fault, results start as
  `PARTIAL`, and expected red before a merge. `work add` and `work retry` commit what they change.
- **Small work-items**: `delivering-an-initiative` gives a work-item at most five requirements.
- **The spec's language**: a glossary in which each term has one meaning (run, delivery, stage directory, status,
  outcome, result, brief, input, template, transition, failed, ...), and five lessons in `docs/capability-format.md`
  that the spec-checker and the reviewers check (spec-consistency r22-r27, review r29-r30).
- **Records**: formulators' questions, reviews, run reports and gate verdicts kept under `.shop/records/`; bulky
  data (slim transcript exports) in a separate records repository, scanned by gitleaks before every push.

Upgrading a consuming repository from 0.21.0: give its initiative branches a pushable remote and run `work run` with
your push credentials; split any scenario that names two requirements (`model check` lists them under v_s2); reword
scenario steps that name exit codes as "exits successfully" or "exits with an error"; commit `.shop/work/` before each
`work run`.

## 0.21.0: the final layout and delivery by `work run`

What changes for a consuming repository:

- **The layout.** `spec/` (with `decisions/` one file a decision, where 0.20.0 had the ledger
  `spec/decisions.md`), `features/`, and `.shop/` for work, records, scratch and worktrees. `docs/superpowers/`
  and top-level `decisions/`, `work/` and `records/` are gone; `model` reads only the new layout.
- **Delivery is v3.** Slicing, slice plans, lanes and steps, `scripts/plan` and the `slicing-into-increments` skill
  are removed, and so is the dependency on superpowers (design-decision/superpowers-not-a-dependency).
  An initiative's work-items are drafted by `delivering-an-initiative` and delivered by `work run`.
- **EARS.** Behaviour lines are EARS requirements with "shall"; `model check` reports any that is not.
- **`migrate run`** makes every mechanical change of the move in one run, or none: moves, decision files from the
  ledger, ids, `@holding` scenarios to `@deprecated`, rewritten references.
- **pytest-bdd and xdist.** The plugin's scenarios run as pytest-bdd step definitions, every scenario bound
  exactly once (`features bindings --unbound`), in parallel under pytest-xdist.
- **`tools size`.** Tracked Python files stay at 300 lines or fewer; `tools size --limit 300` lists those over it,
  and the reviewers run it.

To upgrade: install 0.21.0, `python3 -m pip install clingo pytest pytest-bdd` (and pytest-xdist), and from a clean
checkout with nothing in progress ask Claude to migrate the repository: the `migrating-to-capabilities` skill runs
`migrate run`, re-pairs what needs judgment, and stops at its one gate. Then git-ignore `.shop/scratch/` and
`.shop/worktrees/`, and give pytest a `--work-item` option or set `[tests]` in `.shop/delivery.toml` before the first
`work run`. Earlier releases' notes are in git's history of this file.
