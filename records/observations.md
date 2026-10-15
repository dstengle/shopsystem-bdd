# Observations

Dated, never edited. An observation is an origin: an initiative may cite it as its `source`.

## obs/2026-10-15-design-model-v3
about: shopsystem-bdd/formulation
by: the person
date: 2026-10-15

Design model version 3 gives every capability-requirement a stable id `[r<n>]`, referenced as `<capability>#r<n>`; scenarios, resolutions and proposals point by id; a capability-proposal lists `adds`, `changes`, `removes` by id and gains a `formulated` stage. The plugin's format (`docs/capability-format.md`), its writers and formulators, and `features rebind` all still work by text.

## obs/2026-10-15-grammar-eval-v1
about: shopsystem-bdd/design-model-check
by: the person
date: 2026-10-15

A separate evaluator, grammar-eval (clingo, lark, markdown-it-py), runs grammar.md against documents written as sentences, such as ecommerce-example.md. It is written against model version 1 (transaction, thread, proposal, request, item, `needed_by`). Its FIX notes found clauses of grammar.md that do not compile as written; three of those carry into v3: `standing_edge` (v7c) is undefined, `authored_depends_on` (v4) has no declaration, and `age` (w_stale_intake) has none.

## obs/2026-10-15-unmeasured-releases
about: shopsystem-bdd
by: the 13 October assessment
date: 2026-10-15

Releases 0.13.0 to 0.18.0 have fixture evidence only: no batch of a consuming repository has been measured on any of them. Every rule change proposed since rests on the 0.10.0/0.11.0 baseline of kb batches 32-35.

## obs/2026-10-15-proposal-argues-many
about: shopsystem-bdd/spec-migration
by: the session adopting the model
date: 2026-10-15

design-model.md v3 says a capability-proposal argues one capability, and grammar.md v3 rule v_k5 gives an initiative one first part. grammar.md's edge table allows `argues` 1..n. A repository's first spec (a migration) adds requirements to every capability at once; this repository's first spec is one proposal arguing fourteen capabilities. The model has no kind for that, or the one-capability rule needs a stated exception.

## obs/2026-10-15-closed-before-formulated
about: shopsystem-bdd/design-model-check
by: the session adopting the model
date: 2026-10-15

grammar.md v3's `closed(P)` counts a part closed at `merged`, but v3 adds `formulated` after `merged` for a capability-proposal. So v_d1 lets an initiative be `done` while a proposal's requirements have no scenarios.

## obs/2026-10-15-script-behaviour-unpinned
about: shopsystem-bdd/feature-file-tools
by: the session drafting the script capabilities
date: 2026-10-15

Behaviour seen in the scripts' source that neither `--help` nor a test establishes, left out of the first spec: `features verify-moved` reporting titles missing or added; `features move` refusing its own file as destination; `features hold` on a held scenario leaving the file unchanged; what `plan show --backlog` prints; `plan archive`'s refusals (contract only, untested); the plan file's discovery (exactly one `docs/superpowers/plans/*-slices.md`); `measure`'s refusals for an open batch with no plan and for no earlier archive without `--from`, its ambiguous-commit count and its note when tasks cannot be counted; `tools install`'s output for a non-virtualenv interpreter; `tools untested`'s exit status; `tools check`'s output with nothing to check.
