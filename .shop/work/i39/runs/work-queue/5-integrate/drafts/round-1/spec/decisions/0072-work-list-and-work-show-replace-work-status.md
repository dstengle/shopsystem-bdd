---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/work-list-and-work-show-replace-work-status
summary: "`work status` and `work show` are consolidated into `work list`, which lists all work (initiatives, requests and work-items) with its status, and `work show <id>`, which shows the detail of one initiative, request or work-item; `work status` is retired."
date: 2026-10-27
status: proposed
source: [capability/work-queue#r3@0.29, capability/work-queue#r11@0.29, capability/work-queue#r16@0.29, capability/work-queue#r17@0.29, capability/work-queue#r18@0.29, capability/work-queue#r33@0.29, capability/requests#r13@0.29, capability/requests#r14@0.29, capability/work-queue#r34@0.29, capability/work-queue#r35@0.29, capability/work-queue#r36@0.29, capability/work-queue#r37@0.29, capability/work-queue#r38@0.29, capability/work-queue#r39@0.29, capability/requests#r46@0.29, capability/requests#r47@0.29, design-decision/the-context-runs-without-a-coordinator]
by: "the person's answers of 2026-10-27 to the question against spec/capabilities/work-queue.md (answers 1 and 2)"
---

# 0072. `work list` and `work show` replace `work status`

## Decision

`work status` and `work show` are consolidated into two actions. `work list` lists all work with its status:
initiatives, requests and work-items. `work show <id>` shows the detail of one initiative, request or work-item.
`work status` is retired: its lines are retired and replaced by lines naming `work list` or `work show`. This
replaces what design-decision/the-context-runs-without-a-coordinator says of `work status`: the person's surface
it names holds `work list` and `work show` where it held `work status`; the rest of that decision stands.
