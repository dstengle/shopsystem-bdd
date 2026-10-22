---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i12
title: Batch measurement on design model v3
summary: scripts/measure measures one initiative's delivery (its work-items, their commits and the dispatches that built them) and writes a measurement record under .shop/records/measurements/, with no superpowers paths.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 4
source: [observation/2026-10-19-final-state-only]
date: 2026-10-19
---

The release after i10 and i11 (the person, 2026-10-19: lower priority, held for the release after the
migration release).

Covers:
- batch-measurement rewritten for an initiative's work-items in place of a superpowers batch's plan,
  archive file and ledger, with "facts file" renamed "measurement file" (the person agreed) and the
  glossary entry **measurement**;
- analyzing-a-batch following it.

The migration release's sessions are measured afterwards, from their transcripts, so they are kept until
i12 measures them (Claude Code deletes transcripts after `cleanupPeriodDays`, 30 by default).
