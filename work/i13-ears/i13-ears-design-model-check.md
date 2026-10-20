---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ears-design-model-check
kind: capability-proposal
part_of: initiative/i13
status: merged
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r103-r105]
changes: [design-model-check#r1-r27, design-model-check#r29, design-model-check#r33-r37, design-model-check#r43, design-model-check#r46, design-model-check#r48-r49, design-model-check#r51-r55, design-model-check#r59, design-model-check#r61, design-model-check#r64-r66]
removes: [design-model-check#r28, design-model-check#r30-r32, design-model-check#r38-r41, design-model-check#r44, design-model-check#r47, design-model-check#r50, design-model-check#r56-r58, design-model-check#r60, design-model-check#r62-r63, design-model-check#r67]
---

# Design model check: Behaviour lines in EARS

What the gate approves (the person, 2026-10-19: "I approve"): added `design-model-check#r103-r105`; changed `design-model-check#r1-r27`, `design-model-check#r29`, `design-model-check#r33-r37`, `design-model-check#r43`, `design-model-check#r46`, `design-model-check#r48-r49`, `design-model-check#r51-r55`, `design-model-check#r59`, `design-model-check#r61`, `design-model-check#r64-r66`; removed `design-model-check#r28`, `design-model-check#r30-r32`, `design-model-check#r38-r41`, `design-model-check#r44`, `design-model-check#r47`, `design-model-check#r50`, `design-model-check#r56-r58`, `design-model-check#r60`, `design-model-check#r62-r63`, `design-model-check#r67` (now under `retired:`).

Each line is one EARS requirement, its pattern chosen by what starts the behaviour, with "shall", one response and one sentence; `If` lines only where design-decision/behaviour-lines-are-ears allows them. A line whose meaning is unchanged keeps its id; a retired line's meaning is in the line named below, or in "Implementation, may change".

Lines: original 65 → round 1 100 (98 + r103, r104) → now 50 (23 lines + 27 rows of the reports table).
Highest id ever published: r67. Round-1 ids r68–r102 are unused (never published). r103, r104 (i13's
EARS check) survive; r105 is new (the general line). `retired:` gains r28, r30, r31, r32, r38, r39, r40, r41,
r44, r47, r50, r56, r57, r58, r60, r62, r63, r67 (r42, r45 were already retired).

The reports (violations, unresolved references, file problems) are the capability's purpose: they stay, as rows
of one table (id | code | what is reported), conditions with one code joined in a row.

Where each line that is not kept as it was went: r28 → r27; r30 → r2; r31 → r2; r32 → r2; r38 → r14; r39 → r105; r40 → r16; r41 → r16, r17; r44 → r20; r47 → r24; r50 → r48; r56 → r55; r57 → r12; r58 → r36; r60 → r25; r62 → r26; r63 → r29; r67 → r22.

In `features/design-model-check.feature`, 14 scenarios take the tag of the line that now holds their line's meaning, one or more (design-decision/a-scenario-may-name-several-requirements); no scenario is added or removed.
