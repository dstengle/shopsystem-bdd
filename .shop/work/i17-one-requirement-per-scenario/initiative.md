---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i17
title: One requirement per scenario, and exits in words
summary: A scenario names exactly one requirement and Behaviour lines say a command exits successfully or with an error, never an exit code; work run exits with an error when a work-item awaits a ruling.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 1
source: [observation/2026-10-21-one-requirement-per-scenario]
date: 2026-10-21
---

For 0.21.1 (the person, 2026-10-21: one requirement per scenario, steps shared in code; lines say exits
successfully or with an error; awaiting a ruling is an error; do it as 0.21.1 now). Decisions
design-decision/a-scenario-names-one-requirement (0054, superseding 0052) and
design-decision/exits-are-successful-or-errors (0055).

Covers:
- the lines changed under 0052 back to one requirement per scenario (formulation r4, r11, r13; design-model-check
  r20 and the new row r107, v_s2; spec-migration r2, r11; feature-file-tools r51);
- every Behaviour line naming an exit code or "non-zero" reworded to exits successfully or with an error, codes
  kept in Implementation;
- supervision r9 split: r9 exits successfully when every work-item is `green` or `withdrawn`, the new r32 exits
  with an error when a work-item is `awaiting-ruling`;
- the teaching (docs/capability-format.md, feature-formulator, capability-writer, formulating-features);
- the scenarios that name several requirements, and the scenarios of the reworded lines, reformulated one
  requirement each (another pass); the code of v_s2 and of `features tag` (the drafted work-items).
