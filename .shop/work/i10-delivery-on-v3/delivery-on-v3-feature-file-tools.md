---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-feature-file-tools
kind: capability-proposal
part_of: initiative/i10
status: formulated
date: 2026-10-19
argues: [feature-file-tools]
adds: []
changes: [feature-file-tools#r21@0.29, feature-file-tools#r46@0.29]
removes: [feature-file-tools#r8@0.29, feature-file-tools#r9@0.29, feature-file-tools#r30@0.29, feature-file-tools#r31@0.29, feature-file-tools#r32@0.29, feature-file-tools#r33@0.29, feature-file-tools#r34@0.29, feature-file-tools#r43@0.29, feature-file-tools#r44@0.29, feature-file-tools#r45@0.29, feature-file-tools#r47@0.29, feature-file-tools#r48@0.29, feature-file-tools#r49@0.29, feature-file-tools#r50@0.29]
---

# Feature file tools: no slices

What the gate approves: changed `feature-file-tools#r11@0.29`, `#r21`, `#r40`; removed `#r8`, `#r9`, `#r30-r34`,
`#r43-r45`, `#r47-r50`.

Slice tags and `slice_expectations.py` go with slicing: `features tag` sets only `@r<n>` (r11), `features holding`
no longer reports a replacement's slice tag (r21, r40), and `features plugin` with the plugin's lines goes, replaced
by `work plugin` and `work_expectations.py` (work-queue#r19@0.29, work-queue#r20@0.29, work-queue#r21@0.29, work-queue#r22@0.29, work-queue#r23@0.29, work-queue#r24@0.29). The words held and holding in r21 and r40 are
left for initiative i11's rename to deprecated.

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): feature-file-tools#r11@0.29 -> r46; feature-file-tools#r40@0.29 -> r21. The ids in the text above are the drafted ones.
