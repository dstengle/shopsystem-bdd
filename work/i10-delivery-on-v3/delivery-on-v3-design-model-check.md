---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-design-model-check
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r67]
changes: [design-model-check#r6, design-model-check#r22, design-model-check#r23, design-model-check#r24, design-model-check#r43]
removes: [design-model-check#r42]
---

# Design model check: one requirement form, and fix work-items

What the gate approves: added `design-model-check#r67`, changed `#r6`, `#r22`, `#r23`, `#r24`, `#r43`, removed `#r42`.

`model check` accepts a requirement only as `capability/<name>#r<n>` and its short forms
(design-decision/one-requirement-form): `#behaviour/r<n>` is unresolved (r22, r67), and the line that read it as the
same requirement goes (r42). A fix work-item's `fixes` and `findings` are checked like `blocked_by` (r24, r43). A proposal that has been merged keeps naming the ids it added, changed or removed after a later
proposal retires them, without a report (r6, r23): retiring r42 here would otherwise leave i3's merged proposal under
v15e, and every removal unresolved once merged. The
Not yet entry for a work-queue view is done by `work show` and `work next` (work-queue).
