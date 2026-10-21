---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
---

# shopsystem-bdd

**State.** Plugin 0.21.0: the final layout (design-decision/final-layout), delivery by work-items and `work run`,
and `scripts/migrate`; slicing, `scripts/plan` and the superpowers dependency are removed
(design-decision/superpowers-not-a-dependency). Every approved Behaviour line describes what the plugin does; requirements have
ids from the start (design model v3). Drafted and not yet approved, all awaiting the gate: i1's ten open
proposals (three withdrawn 2026-10-19 with the slicing, slice-plan-tool and batch-analysis capabilities), i2's, i3's five, i9's (the ubiquitous language), the migration release's i10, i11 and i8 (drafted
2026-10-19, whose lines the capability files already show). What is approved and unbuilt lives under `Not yet`.
Check with `python3 scripts/model check`; the decisions index, `spec/decisions/index.md`, is written by `python3 scripts/model decisions`;
`python3 scripts/model rules` lists every rule with its label.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files paired with them as the contract, work-items
pulled through their stages by a script supervisor, implementation red-green, review, and measurement of
what a batch cost. One human gate,
on the spec's Behaviour lines. It is not a test runner, not a project manager, and keeps no state of its
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

The build side, started by the supervisor:

| capability | narrator | group |
|---|---|---|
| `delivery` | the person delivering an initiative | service |
| `code-research` | the supervisor that started the researcher | service |
| `planning` | the supervisor that started the planner | service |
| `red-green` | the supervisor that started the implementer | service |
| `review` | the supervisor closing a work-item or an initiative | service |
| `role-boundaries` | the person running the workflow | guarantees |

Measurement:

| capability | narrator | group |
|---|---|---|
| `batch-measurement` | a session measuring a closed batch | service |

Tools the skills and agents run:

| capability | narrator | group |
|---|---|---|
| `feature-file-tools` | an agent or session editing feature files | service |
| `analysis-tools` | an agent researching or reviewing a project's code | service |
| `design-model-check` | a person or agent checking a repository against the design model | service |
| `work-queue` | a person, agent or script reading or moving work-items | service |
| `supervision` | the person who started work run | service |
| `migration-tools` | a person or session migrating a repository to the final layout | service |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`. `batch-measurement` keeps its
  docstring binding until initiative i12.
- Workflow capabilities (agents and skills): their scenarios run as fixture sessions, `claude -p` against
  fixture repositories, under pytest-bdd with the `fixture` marker, outside the default run
  (design-decision/fixture-scenarios-under-pytest-bdd); runs are recorded under
  `.shop/records/measurements/fixture-runs/`, and batches measured with `scripts/measure`. Until a line's
  scenario is written, `model check` reports it under v_s3.
- `role-boundaries` is guarantees: checked against `agents/*.md`, not by scenarios.

## Glossary

- **batch**: the slices one session plans and one controller executes, archived and measured together.
- **claim**: the file set a claimed work-item has to itself: no other claimed work-item's file set shares a path with it.
- **controller**: the session that dispatches implementers and reviewers for a batch.
- **deprecated scenario**: a scenario kept in the suite, tagged `@deprecated`, after its line is changed or removed, until its replacement is green; it formulates no requirement. Not: held, holding, superseded.
- **fact**: one statement `model facts` gives clingo about the repository's files.
- **file set**: the paths a work-item's work changes, found by its researcher and made final by its planner.
- **hand-back**: an implementer's stop on an observed condition, logged with its evidence.
- **requirement**: one Behaviour line of a capability, named `#r<n>`. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying.
- **ruling**: the person's answer to a work-item's question, recorded in the work-item in their words.
- **slice**: a unit of work with an observable done (scenarios or a check); to become a work-item (i4).
- **suite record**: a whole-suite result logged once and used while nothing it depends on has changed.
- **work-item**: the unit of delivery under a capability-proposal, done when the scenarios it accepts or its check pass, moved through its stages by `work run`.

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/work/`,
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(the supervisor's settings), `.shop/scratch/` and `.shop/worktrees/` (drafts, notes and the implementers'
worktrees, ignored by git), `docs/design-model/` (the model), `docs/capability-format.md` (the format
the plugin teaches consuming repositories).
