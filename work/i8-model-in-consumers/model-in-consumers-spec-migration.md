---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/model-in-consumers-spec-migration
kind: capability-proposal
part_of: initiative/i8
status: drafted
date: 2026-10-19
argues: [spec-migration]
adds: [spec-migration#r15-r23]
changes: [spec-migration#r4, spec-migration#r9, spec-migration#r11, spec-migration#r13, spec-migration#r14]
---

# Spec migration: to the final layout, in one pass

Migration ends on the final layout whatever the repository had of the old system
(design-decision/migration-in-one-pass), with one gate. The proposed file is `capabilities/spec-migration.md`.

- What the person sees: r16 (the gate adds glossary bullets out of form, the plan's open slices, the entries
  that would become observations), r23 (each file other than Markdown in which a moved path was rewritten: on kb, `tests/slices.py` reads the living plan by path, and its suite stops when the plan is not where it says).
- What it ends with: r15 (the layout; `migrate status` clean), r17 (work-items and observations,
  design-decision/living-plan-to-work-items), r18 (`@deprecated`, still bound), r19 (decision files, sources
  as ids), r20 (`model check` clean but the lines that had no scenario), r21 (the glossary in form), r22
  (the mechanical move in a commit of its own, reviewable before the gate).
- Changed: r11 and r13 say deprecated for held, and set aside r18's renaming; r14 names `spec/decisions/`
  and `.shop/` where it named "outside spec/" and drops ledger headings, which no longer survive a
  migration; r4 and r9 are plain words (holding → with, carry → have).

The mechanical half is a new script capability, capability/migration-tools
(capability-proposal/model-in-consumers-migration-tools); these lines are the person's view of it.
