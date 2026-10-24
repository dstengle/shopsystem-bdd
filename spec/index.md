---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
---

# shopsystem-bdd

**Where it stands.** Plugin 0.22.0: the final layout (design-decision/final-layout), delivery by work-items and `work run`,
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
what an initiative's deliveries cost. One human gate,
on the spec's Behaviour lines and glossary entries. It is not a test runner, not a project manager, and keeps nothing of its
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

- **agent**: a definition under `agents/` (its name, model, tools and skills) that a worker or a dispatch is started as. Not: persona.
- **answer**: the answer to a question on a work-item, a capability-proposal or a request, written in it in its answerer's words. Not: ruling.
- **brief**: the input data `work run` writes for one worker in its stage directory, naming the work-item, the files to read, the worktree and where the result goes. Not: task file.
- **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
- **claim**: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
- **compaction**: Claude Code's replacement of a session's earlier messages by a summary, recorded in its transcript.
- **delegation**: the person's words, given with a request, naming the questions a session may answer in the person's place.
- **delivery**: one invocation of `work run` on an initiative, from its start until it exits.
- **deprecated scenario**: a scenario kept in its feature file, tagged `@deprecated`, after its line is changed or removed, until its replacement passes; it formulates no requirement. Not: held, holding, superseded.
- **dispatch**: a session another session starts with its Agent tool, and the transcript it leaves. Not: subagent.
- **failed**: a work-item's status when a fault stopped a stage from starting or finishing; its committed work is kept, and pushed when the remote takes it, and `work retry` returns it once the fault is remedied. Not: aborted.
- **fact**: one statement `model facts` gives clingo about the repository's files.
- **fault**: a failure outside a worker's work that stops a stage: a push or git command failing, a worker changing a file under `.shop/work/` outside its stage directory, or a worker's session ending in an error, at its turn limit or without a result `work run` can read.
- **file set**: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
- **gate**: the person's approval of Behaviour lines and glossary entries before they are committed to `spec/`, with the questions they raise. Not: sign-off.
- **guarantees capability**: a capability of the group guarantees, checked by `measure` on real batches and not by scenarios.
- **hand-back**: an implementer's stop with the outcome `HAND-BACK`, giving the condition and its evidence word for word. Not: handback.
- **initiative branch**: the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Not: integration branch.
- **input**: what a session is started with: input data, such as a brief, or an input prompt, the text filled from a template.
- **ledger**: the tracked file `.shop/work/<initiative>/ledger.md` of one initiative, one line an event, archived with the initiative.
- **line outcome**: the upstream's answer to one line of a request: accepted, rewritten, refused, question or withdrawn.
- **measurement**: a record under `.shop/records/measurements/` that `measure` writes for one initiative's deliveries, or that a trial writes. Not: facts file.
- **outcome**: the one word a worker's result gives: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION` or `NEEDS_CONTEXT`. Not: verdict.
- **plugin version**: the plugin release a repository on the final layout is on, recorded as one line in `.shop/plugin-version`.
- **record**: a file under `.shop/records/` whose frontmatter id has a record kind. Not: log entry.
- **remote**: the remote `work run` pushes the initiative branch to: the branch's upstream remote, else `origin`.
- **report**: the implementer's file in its stage directory, beside its result, naming the files it touched, the tests whose setup it changed and its open questions. Not: write-up.
- **request**: the one way work enters a bounded context: lines in strict EARS that its asker (another context, the product level, or the context itself) proposes to its upstream (the context asked), negotiated in turns until each is accepted, refused or withdrawn, and resolved by the requirement ids that hold the accepted ones.
- **requirement**: one Behaviour line of a capability, named `#r<n>`. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying.
- **result**: the file `result.json` a worker writes in its stage directory, giving its outcome, its summary and the files it names. Not: return.
- **review**: a reviewer's reading of commits against the plan, the spec and the repository's rules, written as graded findings: a work-item review, a branch review or an architecture review. Not: audit.
- **round**: one `initiative-round` session for one kind, numbered under its drafts path. Not: iteration.
- **round trip**: one assistant message of a session's transcript with its own request id, the unit `--max-turns` limits.
- **run**: to execute a command, script, test, scenario or probe until it exits.
- **scenario**: a Gherkin scenario in `features/<capability>.feature`, passing when the one test that binds it passes. Not: test case.
- **session**: one Claude Code conversation with its own id and transcript: the person's, a worker or a dispatch. Not: conversation, chat.
- **stage**: one of research, plan, implementation and review, done by one worker and started by `work run` from the work-item's status. Not: phase.
- **stage directory**: the directory `runs/<work-item>/<k>-<stage>/` that holds one stage's brief, result, report and session. Not: run directory.
- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter; a work-item's are `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-answer`, `failed` and `withdrawn`; a capability-proposal's are `drafted`, `awaiting-answer`, `approved`, `formulated`, `merged` and `withdrawn`; a request's are `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`, `refused` and `withdrawn`; an initiative's are `proposed`, `started`, `done` and `abandoned`. Not: state.
- **suite**: every test `python3 -m pytest` runs from the root by default. Not: fast suite.
- **template**: standing text in a skill or an agent definition that a session fills with input to start another session. Not: boilerplate.
- **tool use**: one call of a tool in a session's transcript, named by the tool.
- **transition**: one change of a node's status, written by `work`; a work-item's is logged in `log.jsonl`. Not: move.
- **trial**: one run by the `trial-runner` of a plugin tool or `work run` on a real target or a fixture repository, measuring what its input names.
- **turn**: the side of a request, its asker or its upstream, whose part of the request is to be written next, passed to the other side by `work turn`.
- **upgrade**: what `migrate upgrade` does to a repository on the final layout to take it from one plugin release to the next: it applies the pending upgrade steps.
- **upgrade step**: one change to a repository's files that the plugin holds with the version that introduced it and a one-line description, pending for a repository when its version is above the repository's plugin version and at or below the plugin's.
- **work-item**: the unit of delivery under a capability-proposal, named by its id `w<n>`, complete when the scenarios it accepts or its check pass, or, where every requirement it accepts is of a guarantees capability, when its review passes, taken through its stages by `work run`.
- **work-item branch**: the branch an implementer commits a work-item's work on, from the initiative branch's head, merged into the initiative branch and deleted when it is merged.
- **worker**: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent; the branch reviewer, owning no work-item, is not one.

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/work/`,
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(`work run`'s settings), `.shop/plugin-version` (the repository's plugin version), `.shop/scratch/` and
`.shop/worktrees/` (drafts, notes and the implementers' worktrees, ignored by git), `docs/design-model/` (the model),
`docs/capability-format.md` (the format the plugin teaches consuming repositories).
