---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
---

# shopsystem-bdd

**State.** Plugin 0.21.0: the final layout (design-decision/final-layout), delivery by work-items and `work run`,
and `scripts/migrate`; slicing, `scripts/plan` and the superpowers dependency are removed
(design-decision/superpowers-not-a-dependency). Requirements have ids from the start (design model v3). The gate of
2026-10-21 (observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-release-gate) approved every capability's
Behaviour lines, i10's, i11's and i8's among them: every Behaviour line is approved, and one the plugin does not do yet
has a drafted work-item. `Not yet` holds what no gate has approved.
Verify with `python3 scripts/model check`; the decisions index, `spec/decisions/index.md`, is written by `python3 scripts/model decisions`;
`python3 scripts/model rules` lists every rule with its label.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files paired with them as the contract, work-items
taken through their stages by `work run`, implementation red-green, review, and measurement of
what a batch cost. One human gate,
on the spec's Behaviour lines and glossary entries. It is not a test runner, not a project manager, and keeps no state of its
own outside the consuming repository's files.

## Constraints

- The design model, version 3 (`docs/design-model/`): standing artifacts, initiatives and parts, records;
  grammar.md's rules are kept by this repository's files, in the layout of design-decision/final-layout.
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored, so a role's rules are enforced by its tools (design-decision/the-v3-agents).
- The dependencies the plugin needs, named in its documentation: clingo, pytest, pytest-bdd
  (design-decision/plugin-takes-the-dependencies-it-needs; the solver: design-decision/model-check-solves-with-clingo).

## Composition

The spec side, with the person:

| capability | narrator | group |
|---|---|---|
| `spec-integration` | the person at the gate | service |
| `formulation` | the person who approved the lines | service |
| `spec-migration` | the person migrating a repository onto spec/ | service |
| `spec-consistency` | the person keeping a spec | service |

The build side, started by `work run`:

| capability | narrator | group |
|---|---|---|
| `delivery` | the person delivering an initiative | service |
| `code-research` | the script `work run`, which started the researcher | service |
| `planning` | the script `work run`, which started the planner | service |
| `red-green` | the script `work run`, which started the implementer | service |
| `review` | the script `work run`, closing a work-item or an initiative | service |
| `role-boundaries` | the person using the workflow | guarantees |

Measurement:

| capability | narrator | group |
|---|---|---|
| `batch-measurement` | a session measuring a closed batch | service |

Tools the skills and agents run:

| capability | narrator | group |
|---|---|---|
| `feature-file-tools` | a session editing feature files | service |
| `analysis-tools` | a session researching or reviewing a project's code | service |
| `design-model-check` | a person or session verifying a repository against the design model | service |
| `work-queue` | a person, session or script reading work-items or writing their transitions | service |
| `supervision` | the person who started `work run` | service |
| `migration-tools` | a person or session migrating a repository to the final layout | service |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`. `batch-measurement` keeps its
  docstring binding until initiative i12.
- Workflow capabilities (agents and skills): their scenarios run as fixture sessions, `claude -p` against
  fixture repositories, under pytest-bdd with the `fixture` marker, outside the suite
  (design-decision/fixture-scenarios-under-pytest-bdd); fixture sessions are written under
  `.shop/records/measurements/fixture-runs/`, and batches measured with `scripts/measure`. Until a line's
  scenario is written, `model check` reports it under v_s3.
- `role-boundaries` is guarantees: verified against `agents/*.md`, not by scenarios.

## Glossary

- **agent**: a definition under `agents/` (its name, model, tools and skills) that a worker or a dispatch is started as. Not: persona.
- **batch**: (old system, until i12) the slices one session plans and one controller executes, archived and measured together.
- **brief**: the input data `work run` writes for one worker in its stage directory, naming the work-item, the files to read, the worktree and where the result goes. Not: task file.
- **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
- **claim**: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
- **controller**: (old system, until i12) the session that dispatches implementers and reviewers for a batch.
- **delivery**: one invocation of `work run` on an initiative, from its start until it exits.
- **deprecated scenario**: a scenario kept in its feature file, tagged `@deprecated`, after its line is changed or removed, until its replacement passes; it formulates no requirement. Not: held, holding, superseded.
- **dispatch**: a session another session starts with its Agent tool, and the transcript it leaves. Not: subagent.
- **fact**: one statement `model facts` gives clingo about the repository's files.
- **file set**: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
- **gate**: the person's approval of Behaviour lines and glossary entries before they are committed to `spec/`, with the questions they raise. Not: sign-off.
- **hand-back**: an implementer's stop with the outcome `HAND-BACK`, giving the condition and its evidence word for word. Not: handback.
- **initiative branch**: the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Not: integration branch.
- **input**: what a session is started with: input data, such as a brief, or an input prompt, the text filled from a template.
- **outcome**: the one word a worker's result gives: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION` or `NEEDS_CONTEXT`. Not: verdict.
- **record**: a file under `.shop/records/` whose frontmatter id has a record kind. Not: log entry.
- **report**: the implementer's file in its stage directory, beside its result, naming the files it touched, the tests whose setup it changed and its open questions. Not: write-up.
- **requirement**: one Behaviour line of a capability, named `#r<n>`. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying.
- **result**: the file `result.json` a worker writes in its stage directory, giving its outcome, its summary and the files it names. Not: return.
- **review**: a reviewer's reading of commits against the plan, the spec and the repository's rules, written as graded findings: a work-item review, a branch review or an architecture review. Not: audit.
- **round**: one dispatch of `initiative-round` for one job, numbered under its drafts path. Not: iteration.
- **ruling**: the person's answer to a work-item's question, written in the work-item in their words.
- **run**: to execute a command, script, test, scenario or probe until it exits.
- **scenario**: a Gherkin scenario in `features/<capability>.feature`, passing when the one test that binds it passes. Not: test case.
- **session**: one Claude Code conversation with its own id and transcript: the person's, a worker, a dispatch or a fixture session. Not: conversation, chat.
- **stage**: one of research, plan, implementation and review, done by one worker and started by `work run` from the work-item's status. Not: phase.
- **stage directory**: the directory `runs/<work-item>/<k>-<stage>/` that holds one stage's brief, result, report and session. Not: run directory.
- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter; a work-item's are `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-ruling` and `withdrawn`. Not: state.
- **suite**: every test `python3 -m pytest` runs from the root by default, fixture scenarios excluded. Not: fast suite.
- **suite record**: (old system, until i12) a whole-suite pass or failure logged once and used while nothing it depends on has changed.
- **template**: standing text in a skill or an agent definition that a session fills with input to start another session. Not: boilerplate.
- **transition**: one change of a work-item's status, written by `work` and logged in `log.jsonl`. Not: move.
- **work-item**: the unit of delivery under a capability-proposal, complete when the scenarios it accepts or its check pass, taken through its stages by `work run`.
- **worker**: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent. Not: job.

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/work/`,
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(`work run`'s settings), `.shop/scratch/` and `.shop/worktrees/` (drafts, notes and the implementers'
worktrees, ignored by git), `docs/design-model/` (the model), `docs/capability-format.md` (the format
the plugin teaches consuming repositories).
