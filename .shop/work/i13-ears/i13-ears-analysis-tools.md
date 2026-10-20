---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ears-analysis-tools
kind: capability-proposal
part_of: initiative/i13
status: merged
date: 2026-10-19
argues: [analysis-tools]
adds: [analysis-tools#r49]
changes: [analysis-tools#r1, analysis-tools#r3-r11, analysis-tools#r13-r14, analysis-tools#r16-r17]
removes: [analysis-tools#r2, analysis-tools#r12, analysis-tools#r15, analysis-tools#r18-r35]
---

# Analysis tools: Behaviour lines in EARS

What the gate approves (the person, 2026-10-19: "I approve"): added `analysis-tools#r49`; changed `analysis-tools#r1`, `analysis-tools#r3-r11`, `analysis-tools#r13-r14`, `analysis-tools#r16-r17`; removed `analysis-tools#r2`, `analysis-tools#r12`, `analysis-tools#r15`, `analysis-tools#r18-r35` (now under `retired:`).

Each line is one EARS requirement, its pattern chosen by what starts the behaviour, with "shall", one response and one sentence; `If` lines only where design-decision/behaviour-lines-are-ears allows them. A line whose meaning is unchanged keeps its id; a retired line's meaning is in the line named below, or in "Implementation, may change".

Lines: original 35 → round 1 45 → now 15. Highest id ever published: r35. Round-1 ids r36–r48 are unused (never
published); r49 is new, the general line. `retired:` gains r2, r12, r15 and r18 to r35.

`If` lines kept: a missing tool named rather than skipped (r17, r7, the purpose), the refusal to install outside
a virtualenv (r6, protects the person's interpreter), and `tests-of` finding nothing executed (r11, its answer).
Every other refusal is under the general line r49 and listed in Implementation.

Where each line that is not kept as it was went: r2 → r49; r12 → r49; r15 → r49; r18 → r6; r19 → r5; r20 → r5; r21 → r49; r22 → r4; r23 → r8; r24 → r49; r25 → r13; r26 → r49; r27 → r17; r28 → r17; r29 → r49; r30 → r14; r31 → r16; r32 → r49; r33 → r16; r34 → r16; r35 → r16.

In `features/analysis-tools.feature`, 22 scenarios take the tag of the line that now holds their line's meaning, one or more (design-decision/a-scenario-may-name-several-requirements); no scenario is added or removed.
