---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i57-migration-tools
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i57
status: awaiting-answer
argues: [migration-tools]
adds: [migration-tools#r35, migration-tools#r36]
changes: []
removes: []
date: 2026-10-28
---

# migration-tools

The drafts of this proposal are in .shop/work/i57/runs/i57/1-integrate/drafts/round-1/.

## Questions
- migration-tools r36 against r24 and r28. The lines in full: [r36] "When a session starts, the plugin's SessionStart hook shall give the session each rule of the log of temporary rules." (added). [r24] "When a session starts in a repository with `.shop/` for which no upgrade step is pending, whose plugin version is not above the plugin's and that has no initiative that is neither `done` nor `abandoned`, the plugin's SessionStart hook shall tell the session nothing." [r28] "When a session starts in a repository without `.shop/`, the plugin's SessionStart hook shall tell the session nothing." r36 contradicts r24 and r28 where the log holds a rule. Readings: (A, recommended) r36 wins: r24 is retired and replaced by a new line r37 that adds 'and whose log of temporary rules holds no rule' to its condition, and r28 is likewise retired and replaced. (B) r24 and r28 win: r36 is restricted to repositories with a pending step or an open initiative, so a rule of the log is not given in other repositories.
