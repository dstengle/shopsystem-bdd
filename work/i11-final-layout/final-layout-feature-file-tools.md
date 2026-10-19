---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-feature-file-tools
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [feature-file-tools]
adds: [feature-file-tools#r57-r59, term/deprecated-scenario]
changes: [feature-file-tools#r2-r5, feature-file-tools#r10, feature-file-tools#r18-r24, feature-file-tools#r35, feature-file-tools#r39-r41, feature-file-tools#r51, feature-file-tools#r53, feature-file-tools#r54, term/requirement]
---

# Feature file tools: deprecate, and every scenario bound once

"Deprecated" in place of held, holding and superseded (the person, 2026-10-19), and `features bindings`
able to show that every scenario has exactly one test, which is how this repository's scenarios stay
covered under pytest-bdd (design-decision/plugin-scenarios-run-as-pytest-bdd). The proposed file is
`capabilities/feature-file-tools.md`.

- Deprecate: `features hold` becomes `features deprecate` (r19, r20, r35, r39), `features holding` becomes
  `features deprecated` (r21, r22, r40), `retire` acts on `@deprecated` (r23, r24). The title suffix is
  " (deprecated)" and the description line `Deprecated for:`. `deprecated` names the replacement's file and
  `@r<n>` tag where `holding` named its slice tag (r21, r40); a missing `Deprecated for:` line is said, not
  printed as `for: None` (observation/2026-10-16-release-0-19-0-defects).
- Bindings: r57 (`scenarios(...)` binds every scenario of the files it names), r58 (`--unbound` reports a
  scenario bound by no test), r59 (and one bound twice).
- Plain words: "hold"/"holds" → "has", "contains", "include"; "carrying" → "with" (r2-r5, r10, r18, r41,
  r51, r53, r54; r8 and r45 are retired by i10).
- Glossary (spec/index.md, proposed in `spec-index.md` beside this file): adds **deprecated scenario**
  (Not: held, holding, superseded); changes **requirement**, whose Not: list gains carry, carries, carried,
  carrying (the matcher allows only a plural "s", so each form is listed).

The slice lines (r8-r11, r30-r34, r43-r50) are left to initiative i10, which removes slicing; where i10
retires r8 or r10, their rewording here is dropped.

Formulation follows: the deprecate scenarios are rewritten from the changed lines, and every scenario whose
title or steps say held, holding or superseded is reworded, since v_t1 reads titles and steps.
