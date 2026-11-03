---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ears-design-model-check
kind: capability-proposal
part_of: initiative/i13
status: formulated
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r103@0.29, design-model-check#r104@0.29, design-model-check#r105@0.29]
changes: [design-model-check#r1@0.29, design-model-check#r2@0.29, design-model-check#r3@0.29, design-model-check#r4@0.29, design-model-check#r5@0.29, design-model-check#r6@0.29, design-model-check#r7@0.29, design-model-check#r8@0.29, design-model-check#r9@0.29, design-model-check#r10@0.29, design-model-check#r11@0.29, design-model-check#r12@0.29, design-model-check#r13@0.29, design-model-check#r14@0.29, design-model-check#r15@0.29, design-model-check#r16@0.29, design-model-check#r17@0.29, design-model-check#r18@0.29, design-model-check#r19@0.29, design-model-check#r20@0.29, design-model-check#r21@0.29, design-model-check#r22@0.29, design-model-check#r23@0.29, design-model-check#r24@0.29, design-model-check#r25@0.29, design-model-check#r26@0.29, design-model-check#r27@0.29, design-model-check#r29@0.29, design-model-check#r33@0.29, design-model-check#r34@0.29, design-model-check#r35@0.29, design-model-check#r36@0.29, design-model-check#r37@0.29, design-model-check#r43@0.29, design-model-check#r46@0.29, design-model-check#r48@0.29, design-model-check#r49@0.29, design-model-check#r51@0.29, design-model-check#r52@0.29, design-model-check#r53@0.29, design-model-check#r54@0.29, design-model-check#r55@0.29, design-model-check#r59@0.29, design-model-check#r61@0.29, design-model-check#r64@0.29, design-model-check#r65@0.29, design-model-check#r66@0.29]
removes: [design-model-check#r28@0.29, design-model-check#r30@0.29, design-model-check#r31@0.29, design-model-check#r32@0.29, design-model-check#r38@0.29, design-model-check#r39@0.29, design-model-check#r40@0.29, design-model-check#r41@0.29, design-model-check#r44@0.29, design-model-check#r47@0.29, design-model-check#r50@0.29, design-model-check#r56@0.29, design-model-check#r57@0.29, design-model-check#r58@0.29, design-model-check#r60@0.29, design-model-check#r62@0.29, design-model-check#r63@0.29, design-model-check#r67@0.29]
---

# Design model check: Behaviour lines in EARS

What the gate approves (the person, 2026-10-19: "I approve"): added `design-model-check#r103@0.29, design-model-check#r104@0.29, design-model-check#r105@0.29`; changed `design-model-check#r1@0.29, design-model-check#r2@0.29, design-model-check#r3@0.29, design-model-check#r4@0.29, design-model-check#r5@0.29, design-model-check#r6@0.29, design-model-check#r7@0.29, design-model-check#r8@0.29, design-model-check#r9@0.29, design-model-check#r10@0.29, design-model-check#r11@0.29, design-model-check#r12@0.29, design-model-check#r13@0.29, design-model-check#r14@0.29, design-model-check#r15@0.29, design-model-check#r16@0.29, design-model-check#r17@0.29, design-model-check#r18@0.29, design-model-check#r19@0.29, design-model-check#r20@0.29, design-model-check#r21@0.29, design-model-check#r22@0.29, design-model-check#r23@0.29, design-model-check#r24@0.29, design-model-check#r25@0.29, design-model-check#r26@0.29, design-model-check#r27@0.29`, `design-model-check#r29@0.29`, `design-model-check#r33@0.29, design-model-check#r34@0.29, design-model-check#r35@0.29, design-model-check#r36@0.29, design-model-check#r37@0.29`, `design-model-check#r43@0.29`, `design-model-check#r46@0.29`, `design-model-check#r48@0.29, design-model-check#r49@0.29`, `design-model-check#r51@0.29, design-model-check#r52@0.29, design-model-check#r53@0.29, design-model-check#r54@0.29, design-model-check#r55@0.29`, `design-model-check#r59@0.29`, `design-model-check#r61@0.29`, `design-model-check#r64@0.29, design-model-check#r65@0.29, design-model-check#r66@0.29`; removed `design-model-check#r28@0.29`, `design-model-check#r30@0.29, design-model-check#r31@0.29, design-model-check#r32@0.29`, `design-model-check#r38@0.29, design-model-check#r39@0.29, design-model-check#r40@0.29, design-model-check#r41@0.29`, `design-model-check#r44@0.29`, `design-model-check#r47@0.29`, `design-model-check#r50@0.29`, `design-model-check#r56@0.29, design-model-check#r57@0.29, design-model-check#r58@0.29`, `design-model-check#r60@0.29`, `design-model-check#r62@0.29, design-model-check#r63@0.29`, `design-model-check#r67@0.29` (now under `retired:`).

Each line is one EARS requirement, its pattern chosen by what starts the behaviour, with "shall", one response and one sentence; `If` lines only where design-decision/behaviour-lines-are-ears allows them. A line whose meaning is unchanged keeps its id; a retired line's meaning is in the line named below, or in "Implementation, may change".

Lines: original 65 → round 1 100 (98 + r103, r104) → now 50 (23 lines + 27 rows of the reports table).
Highest id ever published: r67. Round-1 ids r68–r102 are unused (never published). r103, r104 (i13's
EARS check) survive; r105 is new (the general line). `retired:` gains r28, r30, r31, r32, r38, r39, r40, r41,
r44, r47, r50, r56, r57, r58, r60, r62, r63, r67 (r42, r45 were already retired).

The reports (violations, unresolved references, file problems) are the capability's purpose: they stay, as rows
of one table (id | code | what is reported), conditions with one code joined in a row.

Where each line that is not kept as it was went: r28 → r27; r30 → r2; r31 → r2; r32 → r2; r38 → r14; r39 → r105; r40 → r16; r41 → r16, r17; r44 → r20; r47 → r24; r50 → r48; r56 → r55; r57 → r12; r58 → r36; r60 → r25; r62 → r26; r63 → r29; r67 → r22.

In `features/design-model-check.feature`, 14 scenarios take the tag of the line that now holds their line's meaning, one or more (design-decision/a-scenario-may-name-several-requirements); no scenario is added or removed.
