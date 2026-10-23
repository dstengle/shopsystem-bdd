---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i8
title: Migrate a consuming repository to design model v3
summary: Migration tools only, that take a consuming repository from the old system to the final layout of design model v3; the plugin keeps nothing of the old system beyond them.
kind: capability-change
owner-level: shopsystem-bdd
status: done
priority: 3
source: [review-finding/2026-10-13-kb-and-bdd-assessment]
date: 2026-10-15
---

Rewritten 2026-10-19 to the person's direction: there is no intermediate state in a consuming repository,
only the final one (the layout of initiative/i11) and the tools that move a repository there. shopsystem-kb
and shopsystem-knowledge move after the plugin itself is on the model.

Covers:
- adding ids to a repository already on capability files (shipped in 0.19.0, spec-migration);
- the decision ledger in `spec/decisions.md` to one decision file each, with a generated index;
- living slice plans to work-items;
- `@holding` scenarios to `@deprecated` (the person, 2026-10-19: deprecated in place of superseded);
- the repository layout: `spec/decisions/`, `.shop/work`, `.shop/records`;
- the glossary in its form.

## The final state

The layout and conventions are i11's (design-decision/final-layout, design-decision/light-decisions,
design-decision/references-are-ids); this initiative only moves a repository to them, in one pass with one
gate (design-decision/migration-in-one-pass).

**`scripts/migrate`** (capability/migration-tools) is the only code in the plugin that knows the old layout.
`migrate status` says what is left of it. `migrate run` makes every change that is transcription, in four
steps computed before any is written: ids (the numbering and id rewrites Adding Ids did by hand in 0.19.0),
layout (the moves, ids for the records among them, moved paths rewritten in tracked text files, `.gitignore`),
decisions (the ledger split into `spec/decisions/<nnnn>-<name>.md`, `source` to ids and `by`, the index), and
deprecated (`@holding` to `@deprecated`, `Held for:` to `Deprecated for:`, bindings rebound). `migrate plan`,
run once scenarios are tagged, turns the living plan's open slices into work-items under
`initiative/migrated-plan` and its backlog and open log entries into observations
(design-decision/living-plan-to-work-items). It refuses rather than guesses: a `formulated_as` naming
another file, a ledger property it does not know, a slice in progress, a scenario a slice names that has no
`@r<n>` tag.

**`migrating-to-capabilities`** has one process for a repository that has a `spec/` (the old Adding Ids
section folds into it) and keeps its first-spec process for one that has none, which ends by running the
same steps for what is left. In order: preconditions and the baseline under `.shop/scratch/migration/`; the
context path, asked of the person if `spec/index.md` lacks it; `migrate run`, verified (suite equal,
`verify-moved`, word-diff of Behaviour lines showing only ids) and committed alone as the mechanical move;
the scenario mapping by `feature-formulator`; one gate, showing the mapping's questions, glossary bullets
out of form, each open slice (keep or drop) and each entry that would become an observation (keep or leave
out); `features tag`, the glossary rewritten in the person's words, `migrate plan --drop … --leave …`; verify
(`migrate status` 0, `model check` clean but the `v_s3` of lines that had no scenario, the suite equal) and
commit. `capability-writer`'s migration brief writes decision files, not a ledger.

**What the plugin keeps of the old system**: `scripts/migrate` and the migration skill's text. Nothing else
reads a ledger, a slice plan, `@holding` or a top-level `work/`.

## How it is shown working

- Script: migration-tools' scenarios, as pytest-bdd step definitions (design-decision/plugin-scenarios-run-as-pytest-bdd),
  each against a small repository built in a temporary directory.
- Workflow: a fixture case, T-migrate-final, in the scratch harness (`/home/vscode/scratch/shopsystem-bdd/`):
  an old-layout shelf repository (capabilities without ids, `spec/index.md` without an id, a ledger with
  `decision/` headings and sources naming `docs/superpowers/specs/` and `adrs/`, an `@holding` scenario bound
  by title, a living plan with a planned capability slice, an enabling slice before it, a blocked slice and a
  green one, backlog and log entries, an archive, a glossary bullet out of form, pytest-bdd steps). The skill
  runs headless (`claude -p --plugin-dir` the working copy) three times, the gate answered by the harness;
  each run is scored on: `migrate status` exit 0, `model check` exit 0, the suite's summary and passing titles
  equal to the baseline's, `verify-moved` clean before tagging, the two commits, the work-items and
  observations expected, nothing under `docs/superpowers/`. Three of three, recorded in
  `.shop/records/measurements/fixture-runs/`.
- Trial: a fresh clone of shopsystem-kb (https://github.com/dstengle/shopsystem-kb) at its current head,
  outside any repository the plugin owns, with the gate answered by the controller from the session's
  recommendations, as the 2026-10-16 trials were. Scored like the fixture, except `model check` may report
  `v_s3` for kb's ten lines that have no scenario today; the suite equal at 1603 passed. Nothing is pushed:
  kb moves for real only when its own session runs the migration with the person at the gate.

## What is removed

The 0.19.0 "Adding Ids" section as a hand procedure (its numbering is `migrate run`); the ledger in the
first-spec process (`decisions.append.md`); the migration's `.superpowers/spec-drafts/` path (now
`.shop/scratch/drafts/`); slice-plan editing in the migration ("rewrite the feature half of `Scenarios:`
lines" goes: the plan becomes work-items).

## Parts

model-in-consumers-migration-tools (a new capability), model-in-consumers-spec-migration. Decisions 0049,
0050.

Since 2026-10-19 (walking skeleton, initiative/i13): migrate-status-and-ids → migrate-decisions → kb-trial, the
skeleton's proof (`migrate run` alone on a clone). The other work-items are withdrawn until the skeleton has run.

## Ideas to test once the skeleton runs

Cut from the drafted lines when they became walking skeletons (design-decision/behaviour-lines-are-ears, the
person, 2026-10-19): notes, not requirements, each to be tested once the skeleton has run and earning a line
from what that shows.

- migration-tools: Only files under `--root`.
- migration-tools: `migrate status`: what is left of the old system, exit 1 or 0.
- migration-tools: Refusals: not a git working tree, no or malformed `--context`, a context differing from `spec/index.md` (covered by the general line).
- migration-tools: `--dry-run` and the per-step printed changes.
- migration-tools: Nothing to migrate on a repository on the final layout.
- migration-tools: `retired: []` added; `formulated_as` removed when it names its own feature file, refused otherwise.
- migration-tools: A rewritten reference changes nothing else; record frontmatter kept.
- migration-tools: Moved paths in non-Markdown files listed with the line.
- migration-tools: `.gitignore`'s `.superpowers/` to `.shop/scratch/`.
- migration-tools: Ledger entries with unknown property lines or no `date:` refused.
- migration-tools: A decision's `source` split into record ids, node ids and `by`.
- migration-tools: Retitling `(held)` to `(deprecated)` and `Held for:` to `Deprecated for:`; unparsable modules or multi-line titles refused.
- migration-tools: `migrate plan`: the living plan's open slices to work-items under `migrated-plan`, enabling slices to checks, backlog and log entries to observations, `--plan`, `--drop`, `--leave`, refusals for in-progress slices, unknown titles, untagged scenarios, an existing `migrated-plan`.
- migration-tools: Bad usage exit 2.
