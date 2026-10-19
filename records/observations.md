# Observations

Dated, never edited. An observation is an origin: an initiative may cite it as its `source`.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-design-model-v3
about: capability/formulation
by: the person
date: 2026-10-15

Design model version 3 gives every capability-requirement a stable id `[r<n>]`, referenced as `<capability>#r<n>`; scenarios, resolutions and proposals point by id; a capability-proposal lists `adds`, `changes`, `removes` by id and gains a `formulated` stage. The plugin's format (`docs/capability-format.md`), its writers and formulators, and `features rebind` all still work by text.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-grammar-eval-v1
about: capability/design-model-check
by: the person
date: 2026-10-15

A separate evaluator, grammar-eval (clingo, lark, markdown-it-py), runs grammar.md against documents written as sentences, such as ecommerce-example.md. It is written against model version 1 (transaction, thread, proposal, request, item, `needed_by`). Its FIX notes found clauses of grammar.md that do not compile as written; three of those carry into v3: `standing_edge` (v7c) is undefined, `authored_depends_on` (v4) has no declaration, and `age` (w_stale_intake) has none.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-unmeasured-releases
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the 13 October assessment
date: 2026-10-15

Releases 0.13.0 to 0.18.0 have fixture evidence only: no batch of a consuming repository has been measured on any of them. Every rule change proposed since rests on the 0.10.0/0.11.0 baseline of kb batches 32-35.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-proposal-argues-many
about: capability/spec-migration
by: the session adopting the model
date: 2026-10-15

design-model.md v3 says a capability-proposal argues one capability, and grammar.md v3 rule v_k5 gives an initiative one first part. grammar.md's edge table allows `argues` 1..n. A repository's first spec (a migration) adds requirements to every capability at once; this repository's first spec is one proposal arguing fourteen capabilities. The model has no kind for that, or the one-capability rule needs a stated exception.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-closed-before-formulated
about: capability/design-model-check
by: the session adopting the model
date: 2026-10-15

grammar.md v3's `closed(P)` counts a part closed at `merged` and not at `formulated`, though v3 makes `formulated` a capability-proposal's last stage. Read as written, v_d1 lets an initiative be `done` while a proposal's requirements have no scenarios, and refuses `done` once the proposal is `formulated`. `scripts/model.lp` carries a FIX: a capability-proposal is closed at `formulated` only.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-script-behaviour-unpinned
about: capability/feature-file-tools
by: the session drafting the script capabilities
date: 2026-10-15

Behaviour seen in the scripts' source that neither `--help` nor a test establishes, left out of the first spec: `features verify-moved` reporting titles missing or added; `features move` refusing its own file as destination; what `plan show --backlog` prints; the plan file's discovery (exactly one `docs/superpowers/plans/*-slices.md`); `measure`'s refusals for an open batch with no plan and for no earlier archive without `--from`, its ambiguous-commit count and its note when tasks cannot be counted; `tools install`'s output for a non-virtualenv interpreter; `tools untested`'s exit status; `tools check`'s output with nothing to check.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-model-owned-by-knowledge
about: capability/design-model-check
by: the person
date: 2026-10-16

The design model's grammar, its executable form (`scripts/model.lp`) and the check over it belong with shopsystem-knowledge, which owns the shop's artifact types (capability, decision, feature, work-item among them), their IRIs and `check-the-knowledge-base`. Building them here first gets them into use, but leaves the model owned by one of its consumers. 0027 meets the same line: the plugin's ids must follow the IRI decisions shopsystem-knowledge holds (decision/an-artifacts-iri-is-its-types-then-its-owners-path).

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-defects-seen-in-sweep
about: capability/feature-file-tools
about: capability/analysis-tools
about: capability/batch-measurement
by: the session describing the scripts
date: 2026-10-16

Seen while stating what the scripts do, and left as they are: `features tag` accepts `slice-1.2.3`, though feature-file-tools#r11 allows only `slice-<n>` or `slice-<n>.<m>` (confirmed in the pattern `slice-\d+(\.\d+)*`); analysis-tools#r2 says every subcommand needs a Python project, but only `probe`, `install` and `check` test for one; `tools untested` on a missing file, and `tests-of` or `untested` with coverage data but no `.at` file beside it, end in a traceback, not a refusal; `tools check --base` ignores any paths also given, without saying so; `measure batch` ends in a traceback when `--plan` or the archive file is missing from disk; the pytest plugin, with an ini `slice_plan` naming a missing file, expects nothing to fail without saying no plan was read.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-release-0-19-0-defects
about: capability/feature-file-tools
about: capability/analysis-tools
about: capability/batch-measurement
about: capability/spec-integration
by: the session building 0.19.0
date: 2026-10-16

Found while binding the script capabilities' scenarios to tests and in the reviews of 0.19.0. Fixed in the release: `features tag` accepted `slice-1.2.3` (feature-file-tools#r11 allows `slice-<n>` or `slice-<n>.<m>`); `scripts/plan` (about lines 171-172) said "has Scenarios, not Check" for a slice that has a Check, the two kinds reversed.

Still open, left as they are:
- `features holding` prints `for: None` for a held scenario with no `Held for:` line (`scripts/features:413`).
- `tools untested` on a missing file ends in a traceback, not a refusal (`scripts/tools:252-262`, `executed` and `functions` read the file unguarded).
- `tools tests-of` and `tools untested` end in a traceback when the coverage data has no `.at` file beside it (`read_map`, `scripts/tools:193`).
- `tools check --base` ignores any paths also given, without saying so (`scripts/tools:313-315`).
- `measure batch` ends in a traceback when `--plan` or the archive file is missing on disk (`scripts/measure:374`, the `open` of `plan_file` after the commit-based checks at 350-366).
- `tools map` has more than one way of removing the old map: the loop deleting every `coverage*` file (`scripts/tools:168-170`) beside the map file's own replacement through COVERAGE_FILE; one would do.
- A risk for spec-round, not a script defect: a harness that blocks subagents from writing files (one feature-formulator's `.reply.md` write was refused with "subagents may not write report files") stalls a round, because spec-round waits on reply files.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-final-state-only
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-19

There are no intermediate states, only the final state, the plugin fully on design model v3, and the tools that migrate a repository to it. Nothing more is invested in the old system (slices, slice plans, lanes, the old rules) beyond those tools. The plugin moves to the model first; shopsystem-kb and shopsystem-knowledge move afterwards. Decision 0017 is retired; 0028 and 0032 are rejected.
