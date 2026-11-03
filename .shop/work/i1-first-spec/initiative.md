---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i1
title: The plugin's first spec
summary: Give the plugin its own spec, decisions, work and records in the design model's layout, describing what 0.18.0 does.
kind: capability-change
owner-level: shopsystem-bdd
status: done
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
   its requirements. A sweep of all five scripts added feature-file-tools#r35@0.29, feature-file-tools#r36@0.29, feature-file-tools#r37@0.29, feature-file-tools#r38@0.29, feature-file-tools#r39@0.29, feature-file-tools#r40@0.29, feature-file-tools#r41@0.29, feature-file-tools#r42@0.29, feature-file-tools#r43@0.29, feature-file-tools#r44@0.29, feature-file-tools#r45@0.29, feature-file-tools#r46@0.29, feature-file-tools#r47@0.29, feature-file-tools#r48@0.29, feature-file-tools#r49@0.29, feature-file-tools#r50@0.29, slice-plan-tool#r26-r38,
   batch-measurement#r21@0.29, batch-measurement#r22@0.29, batch-measurement#r23@0.29, batch-measurement#r24@0.29, batch-measurement#r25@0.29, batch-measurement#r26@0.29, batch-measurement#r27@0.29, batch-measurement#r28@0.29, batch-measurement#r29@0.29, batch-measurement#r30@0.29, batch-measurement#r31@0.29, batch-measurement#r32@0.29, batch-measurement#r33@0.29, batch-measurement#r34@0.29, batch-measurement#r35@0.29, batch-measurement#r36@0.29, batch-measurement#r37@0.29, batch-measurement#r38@0.29, analysis-tools#r18@0.29, analysis-tools#r19@0.29, analysis-tools#r20@0.29, analysis-tools#r21@0.29, analysis-tools#r22@0.29, analysis-tools#r23@0.29, analysis-tools#r24@0.29, analysis-tools#r25@0.29, analysis-tools#r26@0.29, analysis-tools#r27@0.29, analysis-tools#r28@0.29, analysis-tools#r29@0.29, analysis-tools#r30@0.29, analysis-tools#r31@0.29, analysis-tools#r32@0.29, analysis-tools#r33@0.29, analysis-tools#r34@0.29, analysis-tools#r35@0.29 and design-model-check#r19@0.29, design-model-check#r20@0.29, design-model-check#r21@0.29, design-model-check#r22@0.29, design-model-check#r23@0.29, design-model-check#r24@0.29, design-model-check#r25@0.29, design-model-check#r26@0.29, design-model-check#r27@0.29, design-model-check#r28@0.29, design-model-check#r29@0.29, design-model-check#r30@0.29, design-model-check#r31@0.29, design-model-check#r32@0.29, design-model-check#r33@0.29, design-model-check#r34@0.29, design-model-check#r35@0.29, design-model-check#r36@0.29, design-model-check#r37@0.29, design-model-check#r38@0.29, design-model-check#r39@0.29, design-model-check#r40@0.29, design-model-check#r41@0.29, each stating what
   0.18.0 does today; their tests come with formulation.

On 2026-10-19 (the person) the proposals for slicing, slice-plan-tool and batch-analysis were withdrawn and
their capabilities removed: delivery moves to work-items in initiative/i10.
