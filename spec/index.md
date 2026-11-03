---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
language: codified-1
---

# shopsystem-bdd

**Where it stands.** Plugin 0.22.0: the final layout (design-decision/final-layout), delivery by work-items and `work run`,
and `scripts/migrate`; slicing, `scripts/plan` and the superpowers dependency are removed
(design-decision/superpowers-not-a-dependency). Requirements have ids from the start (design model v3). The gate of
2026-10-21 (observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-release-gate) approved every capability's
Behaviour lines, i10's, i11's and i8's among them: every Behaviour line is approved, and one the plugin does not do yet
has a drafted work-item. `Not yet` holds what no gate has approved.
The conversion to design model v5 (`.shop/records/2026-11-03-gf-conversion/`) is under way: the glossary below is
typed, `spec/universal.md` holds the universal conditions U1-U10, and `spec/restated.json` freezes the 0.29 ids. A
capability file is codified when its own frontmatter says `language: codified-1`; until then it is read as 0.29 lines.
Verify with `python3 scripts/model check`; the decisions index, `spec/decisions/index.md`, is written by `python3 scripts/model decisions`;
`python3 scripts/model rules` lists every rule with its label.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files paired with them as the contract, work-items
taken through their stages by `work run`, implementation red-green, review, and measurement of
what an initiative's deliveries cost. One human gate,
on the spec's Behaviour lines and glossary entries. It is not a test runner, not a project manager, and keeps nothing of its
own outside the consuming repository's files.

## Constraints

- The design model, version 5 (design model v5, `docs/design-model/`): the graph of standing artifacts, initiatives
  and parts, records, checked by `model check`, and the requirement language (the grammar, this glossary as its
  lexicon, the logic check `model logic`); grammar.md's rules are kept by this repository's files, in the layout of
  design-decision/final-layout.
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored, so a role's rules are enforced by its tools (design-decision/the-v3-agents).
- The dependencies the plugin needs, named in its documentation: clingo, pytest, pytest-bdd
  (design-decision/plugin-takes-the-dependencies-it-needs; the solver: design-decision/model-check-solves-with-clingo).

## Composition

The spec side, with the person:

| capability | narrator | group |
|---|---|---|
| `spec-integration` | the person at the gate | guarantees |
| `formulation` | the person who approved the lines | guarantees |
| `spec-migration` | the person migrating a repository onto spec/ | guarantees |
| `spec-consistency` | the person keeping a spec | guarantees |

The build side, started by `work run`:

| capability | narrator | group |
|---|---|---|
| `delivery` | the person delivering an initiative | guarantees |
| `code-research` | the script `work run`, which started the researcher | guarantees |
| `planning` | the script `work run`, which started the planner | guarantees |
| `red-green` | the script `work run`, which started the implementer | guarantees |
| `review` | the script `work run`, closing a work-item or an initiative | guarantees |
| `role-boundaries` | the person using the workflow | guarantees |

Measurement:

| capability | narrator | group |
|---|---|---|
| `batch-measurement` | a session measuring an initiative's deliveries | service |
| `trials` | the session that started a trial | guarantees |

Tools the skills and agents run:

| capability | narrator | group |
|---|---|---|
| `feature-file-tools` | a session editing feature files | service |
| `analysis-tools` | a session researching or reviewing a project's code | service |
| `design-model-check` | a person or session verifying a repository against the design model | service |
| `requests` | a context taking in or raising a request | service |
| `work-queue` | a person, session or script reading work-items or writing their transitions | service |
| `supervision` | the person who started `work run` | service |
| `migration-tools` | a person or session migrating a repository to the final layout or upgrading it between plugin releases | service |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`.
- The workflow capabilities (agents and skills: spec-integration, spec-migration, spec-consistency, review,
  delivery, formulation, red-green, code-research, planning, trials) are guarantees, checked by `measure` on real
  batches, not by scenarios (design-decision/workflow-capabilities-are-guarantees); `model check`'s v_s3 and
  design-model-check r27 leave guarantees capabilities out.
- `role-boundaries` is guarantees: verified against `agents/*.md`, not by scenarios.

## Glossary

- **the person** (actor): the human who asks, answers and approves.
- **`work run`** (actor): the supervisor that runs nodes through their transitions by starting stages, one session each.
- **`work`** (actor): the command that writes statuses, transitions and requests; the only writer of a status.
- **`features`** (actor): the tool that reads, edits and reports on feature files.
- **`tools`** (actor): the tool that installs and probes the project's interpreter and grammar toolchain, and maps code to tests.
- **`measure`** (actor): the tool that measures an initiative's deliveries and shows and compares measurements.
- **`migrate`** (actor): the tool that migrates a repository to the final layout and upgrades it between plugin releases.
- **`model`** (actor): the tool that checks a repository against the design model and reads its requirements.
- **tool** (actor): any of the commands `work`, `work run`, `features`, `tools`, `measure`, `migrate` and `model`.
- **worker** (actor): a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent; the branch reviewer, owning no work-item, is not one.

- **bounded context** (kind): one repository's spec, with its index, capabilities, decisions and glossary.
- **capability** (kind): one file under `spec/capabilities/`, with a group and a narrator. Plural: capabilities.
- **guarantees capability** (kind): a capability of the group `guarantees`, checked by `measure` on real batches and not by scenarios. Plural: guarantees capabilities.
- **requirement** (kind): one codified statement of a capability, named `<capability>#r<n>`, that parses to one tree in the requirement grammar. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying.
- **requirement group** (kind): the requirements of a capability that together make one scenario, named `<capability>#g<n>`, with a title; its statements share a pre-state and a trigger.
- **universal condition** (kind): a statement of `spec/universal.md`, named `U<n>`, true in every state of every trace and never restated in a requirement.
- **term** (kind): one entry of this glossary or of a capability's `## Terms`, with a category.
- **design-decision** (kind): one file under `spec/decisions/`.
- **feature** (kind): the generated file `features/<capability>.feature`, one scenario for each requirement group.
- **scenario** (kind): a Gherkin scenario in `features/<capability>.feature`, generated from one requirement group, passing when the one test that binds it passes. Not: test case.
- **deprecated scenario** (kind): a scenario kept in its feature file, tagged `@deprecated`, after its line is changed or removed, until its replacement passes; it formulates no requirement. Not: held, holding, superseded.
- **step** (kind): one Given, When or Then line of a scenario, the linearisation of one step function, bound to exactly one step definition.

- **request** (kind): the one way work enters a bounded context: lines that its asker (another context, the product level, or the context itself) proposes to its upstream (the context asked), negotiated in turns until each is accepted, refused or withdrawn, and resolved by the requirement ids that hold the accepted ones.
- **request line** (kind): one proposed statement of a request, with its line outcome.
- **initiative** (kind): the delivery of one request's accepted lines, named `i<n>`.
- **proposal** (kind): a part of an initiative that proposes changes to the spec in its `adds`, `changes` and `removes`: a capability-proposal or a glossary-proposal.
- **capability-proposal** (kind): the proposal of an initiative that adds, changes and removes the requirements of one capability.
- **glossary-proposal** (kind): the part of an initiative, beside its capability-proposals, that proposes the terms the glossary of `spec/index.md` adds, changes and removes, listing each `term/<term>` in its `adds`, `changes` or `removes`.
- **work-item** (kind): the unit of delivery under a capability-proposal, named by its id `w<n>`, complete when the scenarios it accepts or its check pass, or, where every requirement it accepts is of a guarantees capability, when its review passes, run through its stages by `work run`.
- **question** (kind): an open point on a node or a request line, with its readings and a recommended reading.
- **answer** (kind): the answer to a question on a work-item, a capability-proposal, a glossary-proposal or a request, written in it in its answerer's words. Not: ruling.
- **delegation** (kind): the person's words, given with a request, naming the questions a session may answer in the person's place.
- **node** (kind): an initiative, a proposal or a work-item: anything with a status that `work run` runs through its transitions.
- **transition** (kind): one change of a node's status, written by `work`; a work-item's is logged in `log.jsonl`. Not: move.
- **check** (kind): a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
- **gate** (kind): the person's approval of requirements and glossary entries before they are committed to `spec/`, with the questions they raise. Not: sign-off.
- **ledger** (kind): the tracked file `.shop/work/<initiative>/ledger.md` of one initiative, one line an event, archived with the initiative.

- **delivery** (kind): one invocation of `work run` on an initiative, from its start until it exits. Plural: deliveries.
- **stage** (kind): one session `work run` starts for a node from its status: research, plan, implement and review by a worker, a round, an answering session, a branch review or an analysis. Not: phase.
- **round** (kind): a stage of the kind `integrate`, `gate`, `apply`, `formulate` or `intake`, numbered under its drafts path. Not: iteration.
- **session** (kind): one Claude Code conversation with its own id and transcript: the person's, a stage or a dispatch. Not: conversation, chat.
- **dispatch** (kind): a session another session starts with its Agent tool, and the transcript it leaves. Plural: dispatches. Not: subagent.
- **agent** (kind): a definition under `agents/` (its name, model, tools and skills) that a worker or a dispatch is started as. Not: persona.
- **brief** (kind): the input data `work run` writes for one stage in its stage directory, naming the node, the files to read, the worktree and where the result goes. Not: task file.
- **input** (kind): what a session is started with: input data, such as a brief, or an input prompt, the text filled from a template.
- **template** (kind): standing text in a skill or an agent definition that a session fills with input to start another session. Not: boilerplate.
- **result** (kind): the file `result.json` a stage writes, giving its outcome, its summary and the files it names. Not: return.
- **report** (kind): the implementer's file in its stage directory, beside its result, naming the files it touched, the tests whose setup it changed and its open questions. Not: write-up.
- **hand-back** (kind): an implementer's stop with the outcome `HAND-BACK`, giving the condition and its evidence word for word. Not: handback.
- **review** (kind): a reviewer's reading of commits against the plan, the spec and the repository's rules, written as graded findings: a work-item review, a branch review or an architecture review. Not: audit.
- **review finding** (kind): one graded finding of a review.
- **stage directory** (kind): the directory `runs/<node>/<k>-<stage>/` that holds one stage's brief, result, report and session. Plural: stage directories. Not: run directory.
- **compaction** (kind): Claude Code's replacement of a session's earlier messages by a summary, recorded in its transcript.
- **round trip** (kind): one assistant message of a session's transcript with its own request id, the unit `--max-turns` limits.
- **tool use** (kind): one call of a tool in a session's transcript, named by the tool.
- **fault** (kind): a failure outside a session's work that stops it: a push or git command failing, a worker changing a file under `.shop/work/` outside its stage directory, or a session `work run` started ending in an error, at its turn limit or without a result `work run` can read; kept while 0.29 lines name it (U6 replaces it).
- **fact** (kind): one statement `model facts` gives clingo about the repository's files.

- **worktree** (kind): a working tree `work run` makes for one stage.
- **initiative branch** (kind): the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Plural: initiative branches. Not: integration branch.
- **work-item branch** (kind): the branch an implementer commits a work-item's work on, from the initiative branch's head, merged into the initiative branch and deleted when it is merged. Plural: work-item branches.
- **commit** (kind): one git commit on a branch.
- **remote** (kind): the remote `work run` pushes the initiative branch to: the branch's upstream remote, else `origin`.
- **file set** (kind): the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
- **suite** (kind): every test `python3 -m pytest` runs from the root by default. Not: fast suite.

- **record** (kind): a file under `.shop/records/` whose frontmatter id has a record kind. Not: log entry.
- **measurement** (kind): a record under `.shop/records/measurements/` that `measure` writes for one initiative's deliveries, or that a trial writes. Not: facts file.
- **trial** (kind): one run by the `trial-runner` of a plugin tool or `work run` on a real target or a fixture repository, measuring what its input names.
- **plugin version** (kind): the plugin release a repository on the final layout is on, recorded as one line in `.shop/plugin-version`.
- **upgrade** (kind): what `migrate upgrade` does to a repository on the final layout to take it from one plugin release to the next: it applies the pending upgrade steps.
- **upgrade step** (kind): one change to a repository's files that the plugin holds with the version that introduced it and a one-line description, pending for a repository when its version is above the repository's plugin version and at or below the plugin's.

- **status** (attribute of initiative): a node's, request's or design-decision's place in its kind's lifecycle, written in its frontmatter by `work`; this entry gives an initiative's, and the entries below give the other kinds'. Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`. Not: state.
- **status** (attribute of capability-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `formulated`, `withdrawn`.
  Transitions: `drafted` → `awaiting-answer`: ask; `awaiting-answer` → `drafted`: `work answer`; `drafted` → `approved`: approve; `approved` → `formulated`: a formulate round; `drafted` → `withdrawn`: `work withdraw`; `awaiting-answer` → `withdrawn`: `work withdraw`; `approved` → `withdrawn`: `work withdraw`.
- **status** (attribute of glossary-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `withdrawn`.
  Transitions: `drafted` → `awaiting-answer`: ask; `awaiting-answer` → `drafted`: `work answer`; `drafted` → `approved`: approve; `drafted` → `withdrawn`: `work withdraw`; `awaiting-answer` → `withdrawn`: `work withdraw`.
- **status** (attribute of work-item): Values: `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-answer`, `failed`, `withdrawn`.
  Transitions: `drafted` → `researched`: a research stage; `researched` → `planned`: a plan stage; `planned` → `ready`: `work`; `ready` → `claimed`: `work claim`; `claimed` → `done`: an implement stage; `done` → `green`: a review stage; `drafted` → `awaiting-answer`: ask; `researched` → `awaiting-answer`: ask; `planned` → `awaiting-answer`: ask; `claimed` → `awaiting-answer`: ask; `done` → `awaiting-answer`: ask; `awaiting-answer` → `drafted`: `work answer`; `awaiting-answer` → `researched`: `work answer`; `awaiting-answer` → `planned`: `work answer`; `awaiting-answer` → `ready`: `work answer`; `awaiting-answer` → `done`: `work answer`; `drafted` → `failed`: discard; `researched` → `failed`: discard; `planned` → `failed`: discard; `claimed` → `failed`: discard; `done` → `failed`: discard; `failed` → `drafted`: `work retry`; `failed` → `researched`: `work retry`; `failed` → `planned`: `work retry`; `failed` → `claimed`: `work retry`; `failed` → `done`: `work retry`; `drafted` → `withdrawn`: `work withdraw`; `researched` → `withdrawn`: `work withdraw`; `planned` → `withdrawn`: `work withdraw`; `ready` → `withdrawn`: `work withdraw`; `awaiting-answer` → `withdrawn`: `work withdraw`; `failed` → `withdrawn`: `work withdraw`.
- **status** (attribute of request): Values: `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused`, `withdrawn`.
- **status** (attribute of design-decision): Values: `proposed`, `accepted`, `rejected`, `superseded`.
- **outcome** (attribute of result): the one word a stage's result gives. Values: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION`, `NEEDS_CONTEXT`. Not: verdict.
- **line outcome** (attribute of request line): the upstream's answer to one line of a request. Values: `accepted`, `rewritten`, `refused`, `question`, `withdrawn`.
- **side** (attribute of request): the side whose part of the request is written next. Values: `asker`, `upstream`.
- **kind** (attribute of stage): Values: `research`, `plan`, `implement`, `review`, `integrate`, `gate`, `apply`, `formulate`, `intake`, `answer`, `branch review`, `analysis`.
- **group** (attribute of capability): Values: `service`, `guarantees`, `model`, `operations`.
- **grade** (attribute of review finding): Values: `Critical`, `Important`, `Minor`.

- **open** (condition of initiative): Means: its status is not `done` and not `abandoned`.
- **open** (condition of work-item): Means: its status is not `green` and not `withdrawn`.
- **complete** (condition of initiative): Means: a work-item of it is `green`, every work-item of it is `green` or `withdrawn`, every capability-proposal of it is `formulated` or `withdrawn`, and its branch review lists no finding to fix now.
- **settled** (condition of request line): Means: its line outcome is `accepted`, `refused` or `withdrawn`.
- **closed** (condition of capability-proposal): Means: its status is `formulated` or `withdrawn`.
- **closed** (condition of glossary-proposal): Means: its status is `approved` or `withdrawn`.
- **closed** (condition of work-item): Means: its status is `green` or `withdrawn`.
- **failed** (condition of work-item): a work-item whose stage was discarded; its committed work is kept, and pushed when the remote takes it, and `work retry` returns it once the fault is remedied. Means: its status is `failed`. Not: aborted.
- **green check** (condition of work-item branch): Means: the scenarios of its work-item and the suite pass on it, a failing scenario counted after its one rerun alone.

- **fulfils** (relation initiative → request): an initiative fulfils exactly one request.
- **part of** (relation proposal → initiative): each proposal is part of exactly one initiative.
- **argues** (relation capability-proposal → capability): each capability-proposal argues exactly one capability.
- **adds** (relation capability-proposal → requirement): a requirement the proposal adds.
- **removes** (relation capability-proposal → requirement): a requirement the proposal retires.
- **changes** (relation capability-proposal → requirement group): a group whose title or membership the proposal changes.
- **adds** (relation glossary-proposal → term): a term the glossary-proposal adds.
- **changes** (relation glossary-proposal → term): a term the glossary-proposal changes.
- **removes** (relation glossary-proposal → term): a term the glossary-proposal removes.
- **under** (relation work-item → capability-proposal): a work-item delivers part of exactly one capability-proposal.
- **accepts** (relation work-item → requirement): a requirement a work-item delivers; a group named there means its members.
- **blocked by** (relation work-item → work-item): a work-item waits for another; the relation has no cycle.
- **member of** (relation requirement → requirement group): each requirement is a member of exactly one group.
- **generates** (relation requirement group → scenario): each group that is not logic-only generates exactly one scenario.
- **in** (relation requirement group → capability): each group is in exactly one capability.
- **in** (relation capability → bounded context): each capability is in exactly one bounded context.
- **rests on** (relation capability → design-decision): a decision a capability rests on.
- **supersedes** (relation design-decision → design-decision): a decision that replaces another.
- **asker** (relation request → bounded context): the context that proposes a request's lines.
- **upstream** (relation request → bounded context): the context a request asks.
- **raised for** (relation request → request): the request an integrate round raised this one for.
- **on** (relation question → node): the node a question is asked on.
- **for** (relation stage → node): the node a stage is started for.
- **belongs to** (relation commit → work-item): the work-item a commit is made for.
- **merges into** (relation work-item branch → initiative branch): the branch a work-item branch is merged into.

- **start** (event): a stage begins to run, holding its resources.
- **end** (event): a stage's session stops, with a result or without one.
- **ask** (event): a stage raises a question, and its node becomes `awaiting-answer`.
- **approve** (event): the person approves a proposal at the gate.
- **discard** (event): `work run` drops a stage that ended without a readable result.
- **merge** (event): `work run` merges a work-item branch into the initiative branch. Forms: merges, merged.
- **rerun** (event): `work run` runs a failing scenario once more, alone. Forms: reruns, rerun.
- **raise** (event): an initiative raises a request into an upstream. Forms: raises, raised.

- **spec lock** (resource, exclusive): one for each bounded context, held by every integrate, apply and formulate round.
- **initiative lock** (resource, exclusive): one for each initiative, held by every stage of the initiative that is not a worker's.
- **node lock** (resource, exclusive): one for each node, held by every stage for that node.
- **claim** (resource, exclusive): the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
- **worker slot** (resource, counted by `workers`): one of the `workers` of `.shop/delivery.toml` (default 4), held by every worker's stage.
- **merge lock** (resource, exclusive): one for each initiative branch, held by a merge.
- **initiative directory** (resource, exclusive): `.shop/work/<initiative>/`, held by the delivery that runs the initiative. Plural: initiative directories.
- **turn** (resource, exclusive): one for each request, held by the side whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered.
- **checkout** (resource, exclusive): the repository's main working tree, held by one delivery of `work run`.

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/work/`,
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(`work run`'s settings), `.shop/plugin-version` (the repository's plugin version), `.shop/scratch/` and
`.shop/worktrees/` (drafts, notes and the implementers' worktrees, ignored by git), `docs/design-model/` (the model),
`docs/capability-format.md` (the format the plugin teaches consuming repositories), `spec/universal.md` (the universal
conditions), `spec/restated.json` (the 0.29 ids, frozen), `grammar/` (the plugin's core grammars and their corpus).
