---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i35-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i35
status: approved
argues: [supervision]
date: 2026-10-25
adds: [supervision#r123, supervision#r124]
changes: [supervision#r73]
removes: []
---

# supervision

The drafts of this proposal are in .shop/work/i35/runs/i35/1-integrate/drafts/round-1/.

## Questions
- r73 (changed): is the old criterion replaced by `Deprecated for:`, or kept beside it? Was: "**When** `work run` drafts a work-item for a `formulated` capability-proposal, `work run` shall list under the work-item's `## Retires` each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts." Drafted: "**When** `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts." Readings: (a) Replaced, r73 as drafted (recommended); (b) Kept beside it: r73 adds "or whose `@r<n>` tag names a requirement the work-item accepts".
- r123 (added): "**When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each deprecated scenario whose replacement's work-item is `green`." When no deprecated scenario has such a replacement, is a work-item still drafted? Readings: (a) No (recommended): r123 gains "and a deprecated scenario's replacement's work-item is `green`" after its condition; (b) Yes: r123 as drafted.
- r123 (added, same line as above): is "replacement's work-item" a work-item of that initiative, or of any? Readings: (a) That initiative (recommended): "... whose replacement's work-item is a `green` work-item of the initiative"; (b) Any: r123 as drafted.
- r123 (added): under which capability-proposal is the retiring work-item drafted? Readings: (a) the capability-proposal of the last-drafted work-item whose replacement it retires; (b) the initiative's last `formulated` capability-proposal. No recommendation; the line as drafted names neither.
- r123 against r27 and r75: is the retiring work-item drafted before the branch review starts and `measure initiative` runs? Readings: (a) Yes (recommended): add a line "**When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`."; (b) No: no line.
- r73/r123: a scenario deprecated with `Deprecated for: removal` names no replacement; is it retired by a work-item? Readings: (a) No (recommended, as the note gives): no line; (b) Yes: a line listing it under the r123 work-item's `## Retires` when a capability-proposal of the initiative removes its requirement.

## Answers
- 2026-10-25: 1: (a), replaced; r73 as drafted (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 2: (a), no work-item when no deprecated scenario has a green replacement (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 3: (b), any initiative's work-item: the scenarios left by earlier initiatives (supervision @r75, @r102, @r105; work-queue @r9, @r23) are retired too (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 4: (a), under the capability-proposal of the last-drafted work-item whose replacement it retires (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 5: (a), yes: add the line; drafted before the branch review and measure initiative (the coordinator under the person's delegation 2026-10-25)
- 2026-10-25: 6: (a), no line (the coordinator under the person's delegation 2026-10-25)
