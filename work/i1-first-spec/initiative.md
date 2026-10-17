---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i1
title: The plugin's first spec
summary: Give the plugin its own spec, decisions, work and records in the design model's layout, describing what 0.18.0 does.
kind: capability-change
owner-level: shopsystem-bdd
status: started
priority: 0
source: [review-finding/2026-10-13-kb-and-bdd-assessment]
date: 2026-10-15
---

The assessment's section 4: the plugin has become the product-ops system in the "how" layer, with
1,348 lines of instruction and no spec of its own. This initiative migrates it onto the model it
teaches, without changing what any skill, agent or script does.

One capability-proposal per capability, `capability-proposal/first-spec-<capability>` (design-decision/one-capability-per-proposal).
Decisions 0001-0021 record rules already released; 0022-0028 are new with this initiative.

## Questions for the person

1. **Answered 2026-10-16: how the workflow capabilities get scenarios.** As fixture sessions, several
   runs each (design-decision/workflow-scenarios-run-as-fixture-sessions). They are written against the
   behaviour i4 brings, not 0.18.0's (the person, 2026-10-16): the eight workflow proposals here stay
   short of `formulated`, and their requirements under v_s3, until i4 changes them. Still open: how many
   runs a scenario takes and how many must pass; the command that runs them apart from the unittest suite.
2. **Answered 2026-10-16: behaviour seen only in the scripts' source.** Every script is to be described by
   its requirements. A sweep of all five scripts added feature-file-tools#r35-r50, slice-plan-tool#r26-r38,
   batch-measurement#r21-r38, analysis-tools#r18-r35 and design-model-check#r19-r41, each stating what
   0.18.0 does today; their tests come with formulation.
