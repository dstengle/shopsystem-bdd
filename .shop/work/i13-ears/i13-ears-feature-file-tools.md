---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/ears-feature-file-tools
kind: capability-proposal
part_of: initiative/i13
status: formulated
date: 2026-10-19
argues: [feature-file-tools]
adds: []
changes: [feature-file-tools#r1@0.29, feature-file-tools#r2@0.29, feature-file-tools#r4@0.29, feature-file-tools#r5@0.29, feature-file-tools#r7@0.29, feature-file-tools#r12@0.29, feature-file-tools#r13@0.29, feature-file-tools#r14@0.29, feature-file-tools#r16@0.29, feature-file-tools#r17@0.29, feature-file-tools#r19@0.29, feature-file-tools#r21@0.29, feature-file-tools#r23@0.29, feature-file-tools#r24@0.29, feature-file-tools#r25@0.29, feature-file-tools#r26@0.29, feature-file-tools#r28@0.29, feature-file-tools#r29@0.29, feature-file-tools#r35@0.29, feature-file-tools#r46@0.29, feature-file-tools#r51@0.29, feature-file-tools#r52@0.29, feature-file-tools#r56@0.29, feature-file-tools#r57@0.29, feature-file-tools#r58@0.29]
removes: [feature-file-tools#r3@0.29, feature-file-tools#r6@0.29, feature-file-tools#r10@0.29, feature-file-tools#r11@0.29, feature-file-tools#r15@0.29, feature-file-tools#r18@0.29, feature-file-tools#r20@0.29, feature-file-tools#r22@0.29, feature-file-tools#r27@0.29, feature-file-tools#r36@0.29, feature-file-tools#r37@0.29, feature-file-tools#r38@0.29, feature-file-tools#r39@0.29, feature-file-tools#r40@0.29, feature-file-tools#r41@0.29, feature-file-tools#r42@0.29, feature-file-tools#r53@0.29, feature-file-tools#r54@0.29, feature-file-tools#r55@0.29, feature-file-tools#r59@0.29]
---

# Feature file tools: Behaviour lines in EARS

What the gate approves (the person, 2026-10-19: "I approve"): changed `feature-file-tools#r1@0.29, feature-file-tools#r2@0.29`, `feature-file-tools#r4@0.29, feature-file-tools#r5@0.29`, `feature-file-tools#r7@0.29`, `feature-file-tools#r12@0.29, feature-file-tools#r13@0.29, feature-file-tools#r14@0.29`, `feature-file-tools#r16@0.29, feature-file-tools#r17@0.29`, `feature-file-tools#r19@0.29`, `feature-file-tools#r21@0.29`, `feature-file-tools#r23@0.29, feature-file-tools#r24@0.29, feature-file-tools#r25@0.29, feature-file-tools#r26@0.29`, `feature-file-tools#r28@0.29, feature-file-tools#r29@0.29`, `feature-file-tools#r35@0.29`, `feature-file-tools#r46@0.29`, `feature-file-tools#r51@0.29, feature-file-tools#r52@0.29`, `feature-file-tools#r56@0.29, feature-file-tools#r57@0.29, feature-file-tools#r58@0.29`; removed `feature-file-tools#r3@0.29`, `feature-file-tools#r6@0.29`, `feature-file-tools#r10@0.29, feature-file-tools#r11@0.29`, `feature-file-tools#r15@0.29`, `feature-file-tools#r18@0.29`, `feature-file-tools#r20@0.29`, `feature-file-tools#r22@0.29`, `feature-file-tools#r27@0.29`, `feature-file-tools#r36@0.29, feature-file-tools#r37@0.29, feature-file-tools#r38@0.29, feature-file-tools#r39@0.29, feature-file-tools#r40@0.29, feature-file-tools#r41@0.29, feature-file-tools#r42@0.29`, `feature-file-tools#r53@0.29, feature-file-tools#r54@0.29, feature-file-tools#r55@0.29`, `feature-file-tools#r59@0.29` (now under `retired:`).

Each line is one EARS requirement, its pattern chosen by what starts the behaviour, with "shall", one response and one sentence; `If` lines only where design-decision/behaviour-lines-are-ears allows them. A line whose meaning is unchanged keeps its id; a retired line's meaning is in the line named below, or in "Implementation, may change".

Lines: original 45 → round 1 64 → now 25. Highest id ever published: r59. Round-1 ids r60–r78 are unused
(never published); no new id. `retired:` gains r3, r6, r10, r11, r15, r18, r20, r22, r27, r36, r37, r38, r39,
r40, r41, r42, r53, r54, r55, r59.

`If` lines kept: the checks' findings (`verify-moved`, `bindings`, the purpose), and refusals that keep an edit
from damaging the wrong scenario, a file `features` cannot read, a scenario not deprecated, or test modules
(r2, r35, r24, r29). Every other refusal is under the general line r46.

Where each line that is not kept as it was went: r3 → r2; r6 → r5; r10 → r35; r11 → r46; r15 → r46; r18 → r17; r20 → r46; r22 → r21; r27 → r46; r36 → r46; r37 → r17; r38 → r5; r39 → r19; r40 → r21; r41 → r29; r42 → r29; r53 → r35; r54 → r35; r55 → r35; r59 → r58.

In `features/feature-file-tools.feature`, 19 scenarios take the tag of the line that now holds their line's meaning, one or more (design-decision/a-scenario-may-name-several-requirements); no scenario is added or removed.
