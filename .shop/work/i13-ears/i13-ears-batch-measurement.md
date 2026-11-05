---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ears-batch-measurement
kind: capability-proposal
part_of: initiative/i13
status: formulated
date: 2026-10-19
argues: [batch-measurement]
adds: []
changes: [batch-measurement#r1@0.29, batch-measurement#r2@0.29, batch-measurement#r3@0.29, batch-measurement#r4@0.29, batch-measurement#r6@0.29, batch-measurement#r7@0.29, batch-measurement#r9@0.29, batch-measurement#r10@0.29, batch-measurement#r11@0.29, batch-measurement#r12@0.29, batch-measurement#r13@0.29, batch-measurement#r14@0.29, batch-measurement#r15@0.29, batch-measurement#r16@0.29, batch-measurement#r17@0.29, batch-measurement#r18@0.29, batch-measurement#r19@0.29, batch-measurement#r29@0.29, batch-measurement#r31@0.29, batch-measurement#r32@0.29, batch-measurement#r33@0.29, batch-measurement#r34@0.29, batch-measurement#r38@0.29]
removes: [batch-measurement#r5@0.29, batch-measurement#r8@0.29, batch-measurement#r20@0.29, batch-measurement#r21@0.29, batch-measurement#r22@0.29, batch-measurement#r23@0.29, batch-measurement#r24@0.29, batch-measurement#r25@0.29, batch-measurement#r26@0.29, batch-measurement#r27@0.29, batch-measurement#r28@0.29, batch-measurement#r30@0.29, batch-measurement#r35@0.29, batch-measurement#r36@0.29, batch-measurement#r37@0.29]
---

# Batch measurement: Behaviour lines in EARS

What the gate approves (the person, 2026-10-19: "I approve"): changed `batch-measurement#r1@0.29, batch-measurement#r2@0.29, batch-measurement#r3@0.29, batch-measurement#r4@0.29`, `batch-measurement#r6@0.29, batch-measurement#r7@0.29`, `batch-measurement#r9@0.29, batch-measurement#r10@0.29, batch-measurement#r11@0.29, batch-measurement#r12@0.29, batch-measurement#r13@0.29, batch-measurement#r14@0.29, batch-measurement#r15@0.29, batch-measurement#r16@0.29, batch-measurement#r17@0.29, batch-measurement#r18@0.29, batch-measurement#r19@0.29`, `batch-measurement#r29@0.29`, `batch-measurement#r31@0.29, batch-measurement#r32@0.29, batch-measurement#r33@0.29, batch-measurement#r34@0.29`, `batch-measurement#r38@0.29`; removed `batch-measurement#r5@0.29`, `batch-measurement#r8@0.29`, `batch-measurement#r20@0.29, batch-measurement#r21@0.29, batch-measurement#r22@0.29, batch-measurement#r23@0.29, batch-measurement#r24@0.29, batch-measurement#r25@0.29, batch-measurement#r26@0.29, batch-measurement#r27@0.29, batch-measurement#r28@0.29`, `batch-measurement#r30@0.29`, `batch-measurement#r35@0.29, batch-measurement#r36@0.29, batch-measurement#r37@0.29` (now under `retired:`).

Each line is one EARS requirement, its pattern chosen by what starts the behaviour, with "shall", one response and one sentence; `If` lines only where design-decision/behaviour-lines-are-ears allows them. A line whose meaning is unchanged keeps its id; a retired line's meaning is in the line named below, or in "Implementation, may change".

Lines: original 38 → round 1 62 → now 23. Highest id ever published: r38. Round-1 ids r39–r66 are unused (never
published); no new id. `retired:` gains r5, r8, r20, r21, r22, r23, r24, r25, r26, r27, r28, r30, r35, r36, r37.

`If` lines kept: an unknown transcript shape or no dispatch (r6, the purpose "refuses rather than guesses",
decision 0018), an existing facts file not written over (r7, protects a file the transcripts cannot rebuild),
tasks left uncounted rather than guessed (r29). Every other refusal is under the general line, r38, and listed
in Implementation. The facts' counting rules are the purpose and stay, joined where they share a subject.

Where each line that is not kept as it was went: r5 → r38; r8 → r6; r20 → r38; r21 → r38; r22 → r38; r23 → r38; r24 → r38; r25 → r2, r4; r26 → r2; r27 → r15; r28 → r14; r30 → r1; r35 → r18; r36 → r19; r37 → r38.

In `features/batch-measurement.feature`, 15 scenarios take the tag of the line that now holds their line's meaning, one or more (design-decision/a-scenario-may-name-several-requirements); no scenario is added or removed.
