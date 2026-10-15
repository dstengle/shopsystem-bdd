---
id: i2
title: Check a repository against the design model
summary: A script that reads a bounded context's files as the grammar's facts and reports what grammar.md v3 refuses.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 0
source: [review-finding/2026-10-13-kb-and-bdd-assessment, obs/2026-10-15-grammar-eval-v1, obs/2026-10-15-design-model-v3]
date: 2026-10-15
---

Stage 1 of the migration: the layout is only worth adopting if something holds it. grammar.md section 7
asks for the constraints to run over facts exported from frontmatter, in CI and at every transition.
