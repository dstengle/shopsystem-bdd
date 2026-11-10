---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
language: codified-2
imports: [cli, spec]
---

# shopsystem-bdd

**Where it stands.** Plugin 2.0.0: the workflow simplified
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified,
`.shop/records/2026-11-04-workflow-simplification/`). Work is items in a backlog, readied against the codified spec
and built in batches, each closed by one review at its pull request. The old workflow of plugin 1.x (`work run`, its
stages, initiatives, work-items, proposals and delegations) is retired
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired), its capabilities kept as the
record of their ids, and `.shop/work/` is frozen as history. Every capability file is codified (design model v5): the
glossary below is typed, `spec/universal.md` holds the universal conditions, and `spec/restated.json` freezes the
0.29 ids. This index says `codified-2` and imports the CLI pack (CNL 4) and the spec pack (b240): a capability that still says `codified-1`
keeps parsing in the old grammar over the glossary and its own terms, and the glossary's words the pack defines too
are marked `Redefines: cli`, and the spec pack's `Redefines: spec`. Verify with `python3 scripts/model check`; the decisions index, `spec/decisions/index.md`,
is written by `python3 scripts/model decisions`; `python3 scripts/model rules` lists every rule with its label.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files generated from them as the contract, a backlog of items,
items built in batches closed by one reviewed pull request, and measurement of what each batch cost. It is not a test
runner, not a project manager, and keeps nothing of its own outside the consuming repository's files.

## Constraints

- The design model, version 5 (design model v5, `docs/design-model/`): the graph of standing artifacts, initiatives
  and parts, records, checked by `model check`, and the requirement language (the grammar, this glossary as its
  lexicon, the logic check `model logic`); grammar.md's rules are kept by this repository's files, in the layout of
  design-decision/final-layout. Plugin 2.0 builds on design model v5 with items in place of initiatives.
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored, so a role's rules are enforced by its tools (design-decision/the-2-0-agents).
- The dependencies the plugin needs, named in its documentation: clingo, pytest, pytest-bdd
  (design-decision/plugin-takes-the-dependencies-it-needs; the solver: design-decision/model-check-solves-with-clingo).

## Composition

The capabilities of plugin 1.x's stages are retired
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired) and kept as records of their ids;
`batch-measurement`, `requests`, `design-model-check` and `migration-tools` keep the lines that 2.0 still holds.

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
| `migration-tools` | a person or session migrating a repository to the final layout or upgrading it between plugin releases | service |

The simplified workflow:

| capability | narrator | group |
|---|---|---|
| `backlog` | a person or session keeping the backlog | service |
| `readiness` | a person or session readying an item | service |
| `intake` | a session answering a peer bounded context's request | service |
| `batches` | a person or session building a batch | service |
| `pr-review` | the person who merges a batch's pull request | guarantees |
| `brainstorming` | the person shaping work in a conversation | guarantees |
| `decision-tiers` | a person or session keeping the decisions | service |
| `telemetry` | a session measuring a batch | service |
| `conversation` | the person reading why a piece of work was asked for | service |

### Retired in 2.0.0

| capability | narrator | group |
|---|---|---|
| `spec-integration` | the person at the gate | guarantees |
| `formulation` | the person who approved the lines | guarantees |
| `spec-migration` | the person migrating a repository onto spec/ | guarantees |
| `spec-consistency` | the person keeping a spec | guarantees |
| `delivery` | the person delivering an initiative | guarantees |
| `code-research` | the script `work run`, which started the researcher | guarantees |
| `planning` | the script `work run`, which started the planner | guarantees |
| `red-green` | the script `work run`, which started the implementer | guarantees |
| `review` | the script `work run`, closing a work-item or an initiative | guarantees |
| `role-boundaries` | the person using the workflow | guarantees |
| `supervision` | the person who started `work run` | service |
| `work-queue` | a person, session or script reading work-items or writing their transitions | service |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`.
- The guarantees capabilities left (`trials`, `pr-review`, `brainstorming`) are checked by script tests under
  `tests/scripts/`, not by scenarios (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired);
  `model check`'s v_s3 and design-model-check r27 leave guarantees capabilities out.

## Glossary

- **the person** (proper noun): the human who asks, answers and approves. Kind of: agent.
- **`work run`** (proper noun): the supervisor of plugin 1.x that ran an initiative's work-items through their stages, removed in 2.0.0 with its record frozen under `.shop/work/`. Kind of: tool.
- **`work`** (proper noun): the command that writes statuses, transitions and requests. Kind of: tool.
- **`features`** (proper noun): the tool that reads, edits and reports on feature files. Kind of: tool.
- **`tools`** (proper noun): the tool that installs and probes the project's interpreter and grammar toolchain, and maps code to tests. Kind of: tool.
- **`measure`** (proper noun): the tool that measures a merged batch, records a defect found after a merge, and shows and compares measurements. Kind of: tool.
- **`migrate`** (proper noun): the tool that migrates a repository to the final layout and upgrades it between plugin releases. Kind of: tool.
- **`model`** (proper noun): the tool that checks a repository against the design model and reads its requirements. Kind of: tool.
- **tool** (noun): any of the commands `work`, `features`, `tools`, `measure`, `migrate` and `model`. Kind of: agent. Redefines: cli.
- **worker** (noun): a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent. Kind of: stage.

- **bounded context** (noun): one repository's spec, with its index, capabilities, decisions and glossary. This: the bounded context whose repository the command runs in.
- **capability** (noun): one file under `spec/capabilities/`, with a group and a narrator. Plural: capabilities. Kind of: file.
- **requirement** (noun): one codified statement of a capability, named `<capability>#r<n>`, that parses to one tree in the requirement grammar. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying. Kind of: text. Redefines: spec.
- **requirement group** (noun): the requirements of a capability that together make one scenario, named `<capability>#g<n>`, with a title.
- **universal condition** (noun): a statement of `spec/universal.md`, named `U<n>`, true in every state of every trace and never restated in a requirement. Kind of: text.
- **term** (noun): one entry of this glossary or of a capability's `## Terms`, with a category.
- **design-decision** (noun): one file under `spec/decisions/`. Kind of: file.
- **feature** (noun): the generated file `features/<capability>.feature`, one scenario for each requirement group. Kind of: file.
- **scenario** (noun): a Gherkin scenario in `features/<capability>.feature`, generated from one requirement group, passing when the one test that binds it passes. Not: test case.
- **step** (noun): one Given, When or Then line of a scenario, the linearisation of one step function, bound to exactly one step definition.

- **request** (noun): the one way work enters a bounded context: lines that its asker (another context, the product level, or the context itself) proposes to its upstream (the context asked). Kind of: text.
- **request line** (noun): one proposed statement of a request, with its line outcome. Kind of: text.
- **initiative** (noun): the delivery of one request's accepted lines, named `i<n>`. Kind of: node.
- **proposal** (noun): a part of an initiative that proposes changes to the spec in its `adds`, `changes` and `removes`: a capability-proposal or a glossary-proposal. Kind of: node.
- **capability-proposal** (noun): the proposal of an initiative that adds, changes and removes the requirements of one capability. Kind of: proposal.
- **glossary-proposal** (noun): the part of an initiative, beside its capability-proposals, that proposes the terms the glossary of `spec/index.md` adds, changes and removes. Kind of: proposal.
- **work-item** (noun): the unit of delivery under a capability-proposal, named by its id `w<n>`, that `work run` runs through its stages. Kind of: node.
- **question** (noun): an open point on a node or a request line, with its readings and a recommended reading. Kind of: text.
- **answer** (noun): the answer to a question on a work-item, a capability-proposal, a glossary-proposal or a request, written in it in its answerer's words. Not: ruling. Kind of: text.
- **node** (noun): an initiative, a proposal or a work-item: anything with a status that `work run` runs through its transitions.
- **transition** (noun): one change of a node's status, written by `work`. Not: move. Kind of: text.
- **check** (noun): a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
- **ledger** (noun): the tracked file `.shop/work/<initiative>/ledger.md` of one initiative, one line an event, archived with the initiative.

- **stage** (noun): one session `work run` starts for a node from its status: research, plan, implement and review by a worker, a round, an answering session, a branch review or an analysis. Not: phase. Kind of: session.
- **round** (noun): a stage of the kind `integrate`, `gate`, `apply`, `formulate` or `intake`, numbered under its drafts path. Not: iteration. Kind of: stage.
- **session** (noun): one Claude Code conversation with its own id and transcript: the person's, a stage or a dispatch. Not: conversation, chat. Kind of: agent. This: the session that runs the command.
- **dispatch** (noun): a session another session starts with its Agent tool, and the transcript it leaves. Plural: dispatches. Not: subagent. Kind of: session.
- **agent** (noun): a session or a tool, as the one that does what a verb says. Kind of: thing.
- **result** (noun): the file `result.json` a stage writes, giving its outcome, its summary and the files it names. Not: return.
- **report** (noun): the implementer's file in its stage directory, beside its result, naming the files it touched, the tests whose setup it changed and its open questions. Not: write-up.
- **review** (noun): a reviewer's reading of commits against the spec and the repository's rules, written as graded findings: a pull request review or an architecture review. Not: audit. Kind of: text.
- **review finding** (noun): one graded finding of a review. Kind of: text.
- **compaction** (noun): Claude Code's replacement of a session's earlier messages by a summary, recorded in its transcript.
- **fact** (noun): one statement `model facts` gives clingo about the repository's files.

- **worktree** (noun): a working tree `work run` makes for one stage.
- **file** (noun): a file or a directory of the repository or of a worktree. Kind of: text.
- **text** (noun): what a session or a tool writes: a file, or a part of one it writes whole, such as an entry, a line, a row, a block or a comment. Kind of: thing.
- **thing** (noun): anything a requirement names, as what a verb such as keep, name, read or use takes.
- **command** (noun): one run of `work`, `work run` or another tool, with its arguments. Kind of: thing. This: the command the run runs. Redefines: cli.
- **reason** (noun): what an error names as the cause of a refused command. Kind of: text. Redefines: cli.
- **JSON object** (noun): the one object a tool prints on standard output when `--json` is given.
- **initiative branch** (noun): the branch `work run` commits each transition on and merges each work-item branch into, whose base is the commit it started from. Plural: initiative branches. Not: integration branch.
- **work-item branch** (noun): the branch an implementer commits a work-item's work on, from the initiative branch's head, merged into the initiative branch and deleted when it is merged. Plural: work-item branches.
- **commit** (noun): one git commit on a branch, with its message and its change. Kind of: thing.
- **commit** (verb, action): a session or a tool records changed files, or a text changed in one, as one git commit on the current branch. Forms: commits, committed. Frame: agent commits text.
- **push** (verb, action): a commit is pushed to a remote. Forms: pushes, pushed. Frame: agent pushes commit.
- **relocate** (verb, action): a file or directory is moved with git, keeping its history. Forms: relocates, relocated. Frame: `migrate` relocates file.
- **use** (verb, action): a session or a tool uses another tool, a model, an interpreter or a file. Forms: uses, used. Frame: agent uses thing. Redefines: spec.
- **test** (noun): one test of the repository's suite, a scenario's or a script's, by its pytest id. Kind of: thing.
- **violation** (noun): a row of a rule `model check` finds, printed under the rule's code and plain label.
- **remote** (noun): the remote `work run` pushes the initiative branch to: the branch's upstream remote, else `origin`.

- **record** (noun): a file under `.shop/records/` whose frontmatter id has a record kind. Not: log entry. Kind of: file.
- **measurement** (noun): a record under `.shop/records/measurements/` of the figures of one batch, of one earlier delivery or of a trial, written by `measure` or by the trial. Not: facts file. Kind of: record.
- **trial** (noun): one run by the `trial-runner` of a plugin tool or `work run` on a real target or a fixture repository, measuring what its input names. Kind of: thing.

- **status** (attribute of initiative): a node's, request's or design-decision's place in its kind's lifecycle, written in its frontmatter by `work`. Values: `proposed`, `started`, `done`, `abandoned`.
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

- **open** (adjective of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.
- **open** (adjective of work-item): A work-item is open when the work-item is not `green` and the work-item is not `withdrawn`.
- **unfixed** (adjective of initiative): an initiative whose kept branch review lists a review finding to fix now.
- **settled** (adjective of request line): A request line is settled when the request line is `accepted` or the request line is `refused` or the request line is `withdrawn`.
- **closed** (adjective of capability-proposal): A capability-proposal is closed when the capability-proposal is `formulated` or the capability-proposal is `withdrawn`.
- **closed** (adjective of glossary-proposal): A glossary-proposal is closed when the glossary-proposal is `approved` or the glossary-proposal is `withdrawn`.
- **closed** (adjective of work-item): A work-item is closed when the work-item is `green` or the work-item is `withdrawn`.

- **start** (verb, action): a session begins a thing it runs, such as a stage or a trial. Frame: session starts thing.
- **end** (verb, action): a session or a tool stops a thing it runs, such as a stage or a trial, with a result or without one. Frame: agent ends thing.
- **ask** (verb, action): a session or a tool raises a question that waits for an answer. Frame: agent asks question.
- **discard** (verb, action): `work run` drops a stage that ended without a readable result. Frame: `work run` discards stage.
- **merge** (verb, action): `work run` merges a work-item branch into the initiative branch. Forms: merges, merged. Frame: the person merges pull request.
- **raise** (verb, action): an initiative raises a request into an upstream. Forms: raises, raised. Frame: initiative raises request.
- **refuse** (verb, action): a tool declines a command. Frame: tool refuses command. Redefines: cli.
- **write** (verb, action): a session or a tool writes a file or a field. Forms: writes, written. Frame: agent writes text.
- **change** (verb, action): a session or a tool changes a file or a field. Frame: agent changes file. Redefines: cli.
- **give** (verb, action): a session or a tool gives a text a thing it lacks, such as a grade to a review finding. Forms: gives, given. Frame: agent gives thing to text.

- **turn** (noun, exclusive): one for each request, held by the side whose part of the request is to be written next.

- **item** (noun): one file of the backlog, `.shop/backlog/b<n>.md`: work this bounded context may do, with its requirement lines, its provenance and its ratings, named by its id `b<n>` and its title. Kind of: file.
- **backlog** (noun): every item of a bounded context, kept in `.shop/backlog/`.
- **batch** (noun): ready items built together on one branch and closed by its pull request, named `batch-<n>`, kept as the directory `.shop/batches/<n>/`. Plural: batches. Kind of: file.
- **batch plan** (noun): the file `.shop/batches/<n>/plan.md`, with a batch's tasks and their statuses. Kind of: file.
- **task** (noun): one unit of a batch plan, built in its own worktree.
- **pull request** (noun): the GitHub pull request of a batch's branch. Kind of: thing.
- **quote** (noun): a file under `.shop/quotes/` of the person's words cited by another file, with its session, its message and the messages around it. Kind of: file.
- **message** (noun): one turn of the person or of a session in a transcript, without its tool uses.
- **status** (attribute of item): Values: `idea`, `shaped`, `ready`, `in-batch`, `delivered`, `needs-input`, `refused`, `withdrawn`.
  Transitions: `idea` → `shaped`: `work shape`; `shaped` → `ready`: `work ready`; `ready` → `shaped`: pick; `ready` → `in-batch`: pick; `in-batch` → `delivered`: merge; `in-batch` → `needs-input`: park; `in-batch` → `ready`: `work batch abandon`; `needs-input` → `shaped`: `work answer`; `idea` → `refused`: `work refuse`; `shaped` → `refused`: `work refuse`; `idea` → `withdrawn`: `work withdraw`; `shaped` → `withdrawn`: `work withdraw`; `ready` → `withdrawn`: `work withdraw`; `needs-input` → `withdrawn`: `work withdraw`.
- **provenance** (attribute of item): where an item came from: this bounded context, a peer bounded context or the product. Values: `own`, `peer`, `product`.
- **value** (attribute of item): Values: `low-value`, `medium-value`, `high-value`.
- **urgency** (attribute of item): Values: `low-urgency`, `medium-urgency`, `high-urgency`.
- **size** (attribute of item): Values: `small`, `medium`, `large`.
- **status** (attribute of batch): Values: `building`, `in-review`, `awaiting-merge`, `merged`, `abandoned`.
  Transitions: `building` → `in-review`: `work batch review`; `in-review` → `building`: a fix-now finding; `in-review` → `awaiting-merge`: a clean review; `awaiting-merge` → `merged`: merge; `in-review` → `merged`: merge; `building` → `abandoned`: `work batch abandon`; `in-review` → `abandoned`: `work batch abandon`.
- **status** (attribute of task): Values: `pending`, `running`, `done`, `failed`.
- **tier** (attribute of design-decision): Values: `check`, `requirement`, `judgement`.
- **dependency** (noun): one item's need of another item, written in the item that needs it. Plural: dependencies. Kind of: text.
- **blocked** (adjective of item): an item with a dependency on an item that is not `delivered` and is not in the same batch.
- **well-formed** (adjective of item): an item whose every requirement parses, has no L0 or L1 finding of `model logic` with the item's lines laid over `spec/`, and has its scenarios written by `features generate`, and whose capabilities' `check` design-decisions pass their tests.
- **passing** (adjective of item): An item is passing when the item is well-formed and every request line of the item is settled.
- **clean** (adjective of pull request): A pull request is clean when no review finding on the pull request is `fix now`.
- **pick** (verb, action): `work batch start` takes a ready item into a batch, or returns it to `shaped` when it is no longer passing. Forms: picks, picked. Frame: `work` picks item.
- **park** (verb, action): a batch sets an item it cannot finish without an answer to `needs-input`. Forms: parks, parked. Frame: batch parks item.
- **publish** (verb, action): `work` puts a thing on GitHub: a batch's branch as a pull request, with its commits. Forms: publishes, published. Frame: `work` publishes thing.
- **triage** (attribute of review finding): what a review asks of its finding: fixed on the branch before the merge, kept as an observation, or dropped. Values: `fix now`, `observation`, `drop`.
- **defect** (noun): a file of a batch that records a fault in the behaviour of the repository's code, with its reproduction, found by a review or after a merge. Kind of: file.
- **failing** (adjective of test): the test fails when it runs.
- **use** (verb, state): a text holds a word or a thing, as a requirement uses a term. Forms: uses, used. Frame: text uses thing. Redefines: spec.
- **list** (verb, state): a text holds each of some things, as a glossary lists a term. Forms: lists, listed. Frame: text lists thing.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| proposal | part of | initiative | one |
| design-decision | supersedes | design-decision |  |
| request | raised for | request |  |
| file | in | worktree | one |
| initiative | fulfils | request | one |
| work-item | blocked by | work-item |  |
| question | on | node | one |
| stage | for | node | one |
| stage | with | result | one |
| request line | proposed in | request | one |
| dependency | of | item | one |
| dependency | on | item | one |
| request line | of | item | one |
| question | on | item | one |
| item | proposes | requirement |  |
| item | in | batch | one |
| task | of | batch | one |
| pull request | of | batch | one |
| review finding | on | pull request | one |
| quote | from | session | one |
| quote | cites | message |  |
| design-decision | enforced by | test |  |

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/backlog/` (the
items), `.shop/batches/` (the batches), `.shop/requests/` (the requests), `.shop/quotes/` (the person's words kept),
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(the batch settings and prices), `.shop/plugin-version` (the repository's plugin version), `.shop/work/` (plugin
1.x's queue, frozen), `.shop/scratch/` and `.shop/worktrees/` (drafts, notes and the batches' worktrees, ignored by
git), `docs/design-model/` (the model), `docs/capability-format.md` (the format the plugin teaches consuming
repositories), `spec/universal.md` (the universal conditions), `spec/restated.json` (the 0.29 ids, frozen), `grammar/`
(the plugin's core grammars and their corpus).
