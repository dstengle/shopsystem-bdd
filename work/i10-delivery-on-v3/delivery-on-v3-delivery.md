---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-delivery
kind: capability-proposal
part_of: initiative/i10
status: approved
date: 2026-10-19
argues: [delivery]
adds: [delivery#r1-r7]
changes: []
removes: []
---

# Delivery: a new capability

What the gate approves: `delivery#r1-r17`, a new capability, as written in `capabilities/delivery.md`.

`delivering-an-initiative` is the session's part of delivery: formulated capability-proposals become drafted
work-items, `work run` is started, and the person is asked only the questions it ends with. It replaces
`slicing-into-increments` and its hand-off to `superpowers:writing-plans`; what slicing kept that still holds (one
unknown, thin, observable, refusals routed to the spec, deprecated scenarios retired by the work that replaces
them) is in its lines, and the rest (Lands, Steps, lanes, batch plans, the living plan and its archive) goes with it.

Decision: design-decision/superpowers-not-a-dependency (supersedes design-decision/superpowers-dependency).

Glossary, added:
- **ruling**: the person's answer to a work-item's question, recorded with `work rule` in their words.

With this proposal `spec/index.md` changes: the Purpose says work-items for thin vertical slices; the
superpowers constraint goes; the build side of Composition lists delivery, code-research, planning, red-green,
review and role-boundaries with their new narrators, and the tools work-queue and supervision; Testing says the
workflow capabilities run as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd).

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): `capabilities/delivery.md` is now a walking skeleton (design-decision/behaviour-lines-are-ears), numbered from r1, which replaces the drafted lines wholesale; the drafted ids in the text above were never published. What the drafted lines said beyond the skeleton is in the initiative's "Ideas to test once the skeleton runs".
