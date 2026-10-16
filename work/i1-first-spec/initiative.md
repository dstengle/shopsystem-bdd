---
id: i1
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

One capability-proposal per capability, `first-spec/<capability>` (decision/one-capability-per-proposal).
Decisions 0001-0021 record rules already released; 0022-0028 are new with this initiative.

## Questions for the person

1. **How do the workflow capabilities get scenarios?** spec-integration, formulation, spec-migration,
   slicing, code-research, red-green, review and batch-analysis describe what agents do. Their evidence
   today is fixture runs (`records/measurements/fixture-runs/`) and measured batches. Readings:
   (a) Gherkin scenarios run as fixture sessions with `claude -p` against a fixture repository, bound like
   decision/plugin-scenarios-run-as-unittest; (b) group them as guarantees, checked by `measure` against
   a bound, with no scenarios. Until this is answered, `model check` lists their requirements under v_s3,
   and their proposals cannot reach `formulated`.
2. **Behaviour seen only in the scripts' source** (obs/2026-10-15-script-behaviour-unpinned): add any of
   it as requirements, with tests, or leave it as implementation?
