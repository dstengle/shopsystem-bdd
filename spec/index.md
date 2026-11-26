---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
language: codified-2
imports: [request, spec, base]
---

# shopsystem-bdd

**Where it stands.** Plugin 0.31.0: the workflow simplified
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified,
`.shop/records/2026-11-04-workflow-simplification/`). Work is items in a backlog, readied against the codified spec
and built in batches, each closed by one review at its pull request. The old workflow of plugin 0.30 (`work run`, its
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
  design-decision/final-layout. Plugin 0.31 builds on design model v5 with items in place of initiatives.
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored, so a role's rules are enforced by its tools (design-decision/the-2-0-agents).
- The dependencies the plugin needs, named in its documentation: clingo, pytest, pytest-bdd
  (design-decision/plugin-takes-the-dependencies-it-needs; the solver: design-decision/model-check-solves-with-clingo).

## Composition

Plugin 0.38.0: the domain contract (`.shop/records/2026-11-19-domain-contract/`). The specification is the domain
model (`spec/model/<area>.md`), the vocabulary naming its elements (`spec/vocabulary/`), the requirements of the
capabilities below, grouped by area, and the decisions (`spec/decisions/`); the CLI is an adapter, specified by
`spec/adapters/cli.toml`. The capabilities of 0.37.0 and before are retired and kept as records of their ids, each
with a `## Moved` table naming each id's new one (`spec/moves.json`).

| area | kind | capabilities |
|---|---|---|
| specification | core | decisions, checking, consistency, records, scenarios, parsing, product |
| tracking | supporting | items, drafting, context-requests, request-watch, quotes, directives, shaping-guarantees |
| execution | supporting | batches, reviews, review-guarantees, shop |
| measurement | generic | measurement, trials |
| analysis | generic | toolchain, code-analysis, feature-reading |
| upgrades | generic | upgrades |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`.
- The guarantees capabilities left (`trials`, `pr-review`, `brainstorming`) are checked by script tests under
  `tests/scripts/`, not by scenarios (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired);
  `model check`'s v_s3 and design-model-check r27 leave guarantees capabilities out.

## Glossary

Moved to `spec/vocabulary/`, each term naming an element of the domain model `spec/model/` (0.38.0).

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/backlog/` (the
items), `.shop/batches/` (the batches), `.shop/requests/` (the requests), `.shop/quotes/` (the person's words kept),
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/delivery.toml`
(the batch settings and prices), `.shop/plugin-version` (the repository's plugin version), `.shop/work/` (plugin
0.30's queue, frozen), `.shop/scratch/` and `.shop/worktrees/` (drafts, notes and the batches' worktrees, ignored by
git), `docs/design-model/` (the model), `docs/capability-format.md` (the format the plugin teaches consuming
repositories), `spec/universal.md` (the universal conditions), `spec/restated.json` (the 0.29 ids, frozen), `grammar/`
(the plugin's core grammars and their corpus).
