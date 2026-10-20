---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-red-green
kind: capability-proposal
part_of: initiative/i10
status: approved
date: 2026-10-19
argues: [red-green]
adds: [red-green#r17-r18, red-green#r37]
changes: [red-green#r1-r3, red-green#r5-r7, red-green#r9-r11, red-green#r15-r16]
removes: []
---

# Red-green: the implementer stage

What the gate approves: added `red-green#r17-r19`, changed `#r1-r3` and `#r5-r16` (r4 stands), and the narrator
"the supervisor that started the implementer" (was "the controller that dispatched the implementer").

The implementer takes a ready work-item in its worktree in place of a task brief, reports through its result file in
place of the plan's log (HAND-BACK becomes a result status, the checkpoint a report section), claims a file outside
its set or stops (r17), and leaves branches and `.shop/work/` to `work run` (r18, r19). Steps go; the 15-file
budget and `PARTIAL` stay (r9). A test's allowance is measured from the initiative's base (r6). The Not yet entry is
done. Decisions: design-decision/plans-list-the-tests-they-break, design-decision/the-file-set-is-the-claim.

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): red-green#r17 -> r17, r37; red-green#r19 -> r2; red-green#r8 out (retired: output format, to "Implementation, may change"); red-green#r12 -> r3; red-green#r13 -> r5; red-green#r14 -> r5. The ids in the text above are the drafted ones.
