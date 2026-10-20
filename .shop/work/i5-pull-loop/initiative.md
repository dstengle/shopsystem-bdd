---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i5
title: A pull loop in place of the LLM controller
summary: Workers started by a shell loop with claude -p pull one work-item at one stage each; a script alone writes status, checking each transition's guard.
kind: capability-change
owner-level: shopsystem-bdd
status: abandoned
priority: 4
source: [review-finding/2026-10-13-kb-and-bdd-assessment, measurement/kb-batches-32-35]
date: 2026-10-15
---

Watch: the controller's share of cache reads (to zero), span minus agent-minutes, starting context per
worker, stops on file-set claims. Needs the baseline batch first.

Abandoned 2026-10-19 (the person): replaced by initiative/i10, whose script supervisor pulls work-items through stages with `claude -p` workers.
