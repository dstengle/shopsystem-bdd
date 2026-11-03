---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-supervision
kind: capability-proposal
part_of: initiative/i10
status: formulated
date: 2026-10-19
argues: [supervision]
adds: [supervision#r1@0.29, supervision#r2@0.29, supervision#r3@0.29, supervision#r4@0.29, supervision#r5@0.29, supervision#r6@0.29, supervision#r7@0.29, supervision#r8@0.29, supervision#r9@0.29, supervision#r10@0.29]
changes: []
removes: []
---

# Supervision: a new capability

What the gate approves: `supervision#r1@0.29, supervision#r2@0.29, supervision#r3@0.29, supervision#r4@0.29, supervision#r5@0.29, supervision#r6@0.29, supervision#r7@0.29, supervision#r8@0.29, supervision#r9@0.29, supervision#r10@0.29, supervision#r11@0.29, supervision#r12@0.29, supervision#r13@0.29, supervision#r14@0.29, supervision#r15@0.29, supervision#r16@0.29, supervision#r17@0.29, supervision#r18@0.29, supervision#r19@0.29, supervision#r20@0.29, supervision#r21@0.29, supervision#r22@0.29, supervision#r23@0.29, supervision#r24@0.29, supervision#r25@0.29, supervision#r26@0.29, supervision#r27@0.29, supervision#r28@0.29, supervision#r29@0.29, supervision#r30@0.29, supervision#r31@0.29, supervision#r32@0.29, supervision#r33@0.29, supervision#r34@0.29, supervision#r35@0.29`, a new capability, as written in `capabilities/supervision.md`.

`work run` is the supervisor the design model names ("workers; a script supervises"). It replaces the controller
session of subagent-driven-development and the plan's execution rules: fresh agents, paths in and results out,
review by risk, fresh fix rounds, further rounds only for the severe, and one session per batch become what a
script does rather than what a controller is asked. Lanes go: implementers with disjoint file sets work at once,
each in its own worktree. What it records (`log.jsonl`, run directories, review-finding records) is what
initiative i12's `measure` reads.

Decisions: design-decision/a-script-supervises-delivery (supersedes design-decision/one-batch-one-session),
design-decision/worker-results-are-files (supersedes design-decision/fresh-agents-short-replies),
design-decision/work-item-lifecycle-as-run (supersedes design-decision/suite-record-holds),
design-decision/review-of-work-items (supersedes design-decision/review-by-risk),
design-decision/the-file-set-is-the-claim (supersedes design-decision/slice-budget-refused-by-plan).

Glossary, added:
- **supervisor**: `work run`, the script that starts the workers and alone writes a work-item's status.
- **worker**: a new `claude -p` session of one agent, started by the supervisor for one stage of one work-item.

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): `capabilities/supervision.md` is now a walking skeleton (design-decision/behaviour-lines-are-ears), numbered from r1, which replaces the drafted lines wholesale; the drafted ids in the text above were never published. What the drafted lines said beyond the skeleton is in the initiative's "Ideas to test once the skeleton runs".
