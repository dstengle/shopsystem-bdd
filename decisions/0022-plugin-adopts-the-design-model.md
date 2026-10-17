---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-adopts-the-design-model
summary: "This repository is a bounded context in design-model v3's layout: spec/, decisions/, features/, work/ and records/."
date: 2026-10-15
status: proposed
source: "docs/design-model/ (v3); records/review-findings/2026-10-13-kb-and-bdd-assessment.md section 4"
---

# 0022. Plugin adopts the design model

## Decision

The plugin's own design lives in `spec/` (capabilities with requirement ids), `decisions/` (one file each, `spec/decisions.md` generated), `work/` (initiatives and parts) and `records/` (observations, measurements, review-findings, archive). `docs/design-model/` holds the model it follows. History that was under `docs/superpowers/` is under `records/`.

## Context

The plugin ran on a different system from the repositories it runs on, so migrating its own functionality had no shared form, and its rules had no spec, no revisit triggers and no removals.

## Alternatives

Keep the design notes and changelog; give the plugin a spec only when it is rewritten.

## Consequences

The plugin's rules become decisions that can be retired when their signals fire. Formulating the plugin's own requirements needs a way to run its scenarios (question in i1).
