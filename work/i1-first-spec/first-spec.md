---
id: first-spec
kind: capability-proposal
part_of: i1
status: drafted
date: 2026-10-15
argues: [spec-integration, formulation, spec-migration, slicing, code-research, red-green, review, role-boundaries, batch-measurement, batch-analysis, feature-file-tools, slice-plan-tool, analysis-tools]
adds:
  - spec-integration#r1-r11
  - formulation#r1-r10
  - spec-migration#r1-r8
  - slicing#r1-r13
  - code-research#r1-r9
  - red-green#r1-r11
  - review#r1-r9
  - role-boundaries#r1-r5
  - batch-measurement#r1-r20
  - batch-analysis#r1-r8
  - feature-file-tools#r1-r34
  - slice-plan-tool#r1-r25
  - analysis-tools#r1-r17
---

# The plugin's first spec

What the gate approves: the ids above, as written in `spec/capabilities/`. Each line describes what
0.18.0 does today, taken from its skills, agents, `--help` contracts and tests; none adds behaviour.
Decisions 0001-0021 record rules already released; 0022-0028 are new with this proposal.

## Questions for the person

1. **How do the workflow capabilities get scenarios?** spec-integration, formulation, spec-migration,
   slicing, code-research, red-green, review and batch-analysis describe what agents do. Their evidence
   today is fixture runs (`records/measurements/fixture-runs/`) and measured batches. Readings:
   (a) Gherkin scenarios run as fixture sessions with `claude -p` against a fixture repository, bound like
   decision/plugin-scenarios-run-as-unittest; (b) group them as guarantees, checked by `measure` against
   a bound, with no scenarios. Until this is answered, `model check` lists their requirements under v_s3,
   and this proposal cannot reach `formulated`.
2. **One proposal for fourteen capabilities.** v3 says a capability-proposal argues one capability
   (obs/2026-10-15-proposal-argues-many). Accept one migration proposal, or split into one initiative
   per capability?
3. **Behaviour seen only in the scripts' source** (obs/2026-10-15-script-behaviour-unpinned): add any of
   it as requirements, with tests, or leave it as implementation?
