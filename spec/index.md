---
id: missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
---

# shopsystem-bdd

**State.** Plugin 0.18.0. Every Behaviour line on `main` describes what 0.18.0 does, except
`design-model-check`, which arrives with initiative i2. What is approved and unbuilt lives on its
branch with its code, and under `Not yet`. Requirements carry ids from the start (design model v3).
Check with `python3 scripts/model check`; the decisions index is `python3 scripts/model decisions`.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files paired with them as the contract, thin
vertical slices, implementation red-green, review, and measurement of what a batch cost. One human gate,
on the spec's Behaviour lines. It is not a test runner, not a project manager, and holds no state of its
own outside the consuming repository's files.

## Constraints carried

- The design model, version 3 (`docs/design-model/`): standing artifacts, initiatives and parts, records;
  grammar.md's rules hold over this repository's files (decision/plugin-adopts-the-design-model).
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored (decision/rules-held-by-agent-tools).
- superpowers as a declared dependency (decision/superpowers-dependency).
- Scripts on the standard library (decision/scripts-stdlib-only), except the solver behind `model check`
  (decision/model-check-solves-with-clingo).

## Composition

The spec side, with the person:

| capability | narrator | group |
|---|---|---|
| `spec-integration` | the person at the gate | service |
| `formulation` | the person who approved the lines | service |
| `spec-migration` | the person migrating a repository onto spec/ | service |

The build side, dispatched:

| capability | narrator | group |
|---|---|---|
| `slicing` | the session that plans a batch | service |
| `code-research` | the session that plans a batch | service |
| `red-green` | the controller that dispatched the implementer | service |
| `review` | the controller closing a task or a batch | service |
| `role-boundaries` | the person running the workflow | guarantees |

Measurement:

| capability | narrator | group |
|---|---|---|
| `batch-measurement` | a session measuring a closed batch | service |
| `batch-analysis` | the person deciding a change to the workflow | operations |

Tools the skills and agents run:

| capability | narrator | group |
|---|---|---|
| `feature-file-tools` | an agent or session editing feature files | service |
| `slice-plan-tool` | an agent or session editing a living slice plan | service |
| `analysis-tools` | an agent researching or reviewing a project's code | service |
| `design-model-check` | a person or agent checking a repository against the design model | service |

## Testing

- Script capabilities: `python3 -m unittest discover -s tests/scripts`. A capability formulated in
  `features/` binds each scenario to the test whose docstring is its title
  (decision/plugin-scenarios-run-as-unittest); so far `design-model-check`.
- Workflow capabilities (agents and skills): fixture runs recorded under `records/measurements/fixture-runs/`,
  and batches measured with `scripts/measure`. How their requirements get acceptance-scenarios is open
  (initiative i1); until then `model check` reports them under v_s3.
- `role-boundaries` is guarantees: checked against `agents/*.md`, not by scenarios.

## Glossary

- **batch**: the slices one session plans and one controller executes, archived and measured together.
- **controller**: the session that dispatches implementers and reviewers for a batch.
- **hand-back**: an implementer's stop on an observed condition, logged with its evidence.
- **slice**: a unit of work with an observable done (scenarios or a check); to become a work-item (i4).
- **suite record**: a whole-suite result logged once and used while nothing it depends on has changed.

## Where things live

`spec/` (this index, capabilities, generated `decisions.md`), `decisions/`, `features/`, `work/`,
`records/` (observations, measurements, review-findings, archive), `docs/design-model/` (the model),
`docs/capability-format.md` (the format the plugin teaches consuming repositories).
