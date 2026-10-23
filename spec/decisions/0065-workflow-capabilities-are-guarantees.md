---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/workflow-capabilities-are-guarantees
summary: "The ten workflow capabilities are guarantees, checked by `measure` on real batches as role-boundaries is, and their scenarios do not run as fixture sessions."
date: 2026-10-23
status: proposed
supersedes: [design-decision/workflow-scenarios-run-as-fixture-sessions, design-decision/fixture-scenarios-under-pytest-bdd]
source: [design-decision/workflow-scenarios-run-as-fixture-sessions, design-decision/fixture-scenarios-under-pytest-bdd]
by: "the person, 2026-10-23 (\"go with B\"), on the design note 2026-10-23-faster-batches-clean-model-check (i23), part 6; drafted under the delegation of the drafting decisions to the coordinator"
---

# 0065. Workflow capabilities are guarantees

## Context

Decision 0030 gives the ten workflow capabilities (spec-integration, spec-migration, spec-consistency, review,
delivery, formulation, red-green, code-research, planning, trials) Gherkin scenarios run as headless `claude -p`
fixture sessions; decision 0043 puts them under pytest-bdd with `@fixture`. The harness was never built, so their 150
lines are v_s3, nine closed initiatives are v_d1, and five green i10 work-items are file problems.

## Alternatives

A, keep 0030: bring the harness into the repository (tests/workflow/, the `fixture` marker), write the ten feature
files, and reopen the nine initiatives or move their backlog here.

## Decision

The ten workflow capabilities (spec-integration, spec-migration, spec-consistency, review, delivery, formulation,
red-green, code-research, planning, trials) are guarantees, checked by `measure` on real batches, as role-boundaries
is. `model check`'s v_s3 and design-model-check r27 leave guarantees capabilities out, and `spec/index.md`'s Testing
section says so. The capability-proposals of the nine closed initiatives left at `merged` become `formulated`, so
their closings stand. The fixture harness in /home/vscode/scratch/shopsystem-bdd is not brought into the repository.
