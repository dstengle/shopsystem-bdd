---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-first-disentangling-keeps-packs-measurement-batches-and-the-flat-spec-as-they-are
summary: "For now the plugin's packs are a published language every context may import, measurement stays in execution, a batch stays one commit, and a shop keeps a flat spec/."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-85]
---

# 0131. The first disentangling keeps packs, measurement, batches and the flat spec as they are

## Context

Open questions Q3, Q4, Q7 and Q9 of the disentangling worked example.

## Decision

Until a later decision says otherwise: the plugin's packs are available to every context to import (a published language, not a conformist relation); measurement is part of the execution context; opening a batch stays as it is, not a saga; a shop keeps one flat spec/, which is easily moved later.
