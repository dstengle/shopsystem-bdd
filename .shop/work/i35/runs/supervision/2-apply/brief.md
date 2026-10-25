# apply of supervision

Capability-proposal: .shop/work/i35/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: apply
Give the change list of what you applied in your result's `changes`: a list with one entry for each capability, each `{"capability": <name>, "adds": [...], "changes": [...], "removes": [...]}`, the ids as `<capability>#r<n>` or `term/<term>`.
Drafts path: .shop/work/i35/runs/i35/1-integrate/drafts/round-1/
Base: 3fbe46ea079ea23096e2dc093be6b24d1799fbd7
Worktree: /tmp/work-run-i35-geaeg_4d/supervision-2-apply
Branch: round/supervision-2-apply
Answers the person gave, each with the question it answers:
- Question: r73 (changed): is the old criterion replaced by `Deprecated for:`, or kept beside it? Was: "**When** `work run` drafts a work-item for a `formulated` capability-proposal, `work run` shall list under the work-item's `## Retires` each scenario tagged `@deprecated` whose `@r<n>` tag names a requirement the work-item accepts." Drafted: "**When** `work run` drafts a work-item, `work run` shall list under the work-item's `## Retires` each deprecated scenario whose `Deprecated for:` line names a scenario of a requirement the work-item accepts." Readings: (a) Replaced, r73 as drafted (recommended); (b) Kept beside it: r73 adds "or whose `@r<n>` tag names a requirement the work-item accepts".
  Answer: 2026-10-25: 1: (a), replaced; r73 as drafted (the coordinator under the person's delegation 2026-10-25)
- Question: r123 (added): "**When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft one work-item that retires each deprecated scenario whose replacement's work-item is `green`." When no deprecated scenario has such a replacement, is a work-item still drafted? Readings: (a) No (recommended): r123 gains "and a deprecated scenario's replacement's work-item is `green`" after its condition; (b) Yes: r123 as drafted.
  Answer: 2026-10-25: 2: (a), no work-item when no deprecated scenario has a green replacement (the coordinator under the person's delegation 2026-10-25)
- Question: r123 (added, same line as above): is "replacement's work-item" a work-item of that initiative, or of any? Readings: (a) That initiative (recommended): "... whose replacement's work-item is a `green` work-item of the initiative"; (b) Any: r123 as drafted.
  Answer: 2026-10-25: 3: (b), any initiative's work-item: the scenarios left by earlier initiatives (supervision @r75, @r102, @r105; work-queue @r9, @r23) are retired too (the coordinator under the person's delegation 2026-10-25)
- Question: r123 (added): under which capability-proposal is the retiring work-item drafted? Readings: (a) the capability-proposal of the last-drafted work-item whose replacement it retires; (b) the initiative's last `formulated` capability-proposal. No recommendation; the line as drafted names neither.
  Answer: 2026-10-25: 4: (a), under the capability-proposal of the last-drafted work-item whose replacement it retires (the coordinator under the person's delegation 2026-10-25)
- Question: r123 against r27 and r75: is the retiring work-item drafted before the branch review starts and `measure initiative` runs? Readings: (a) Yes (recommended): add a line "**When** every work-item of an initiative is `green` or `withdrawn`, `work run` shall draft the work-item r123 names before it starts a branch review or runs `measure initiative`."; (b) No: no line.
  Answer: 2026-10-25: 5: (a), yes: add the line; drafted before the branch review and measure initiative (the coordinator under the person's delegation 2026-10-25)
- Question: r73/r123: a scenario deprecated with `Deprecated for: removal` names no replacement; is it retired by a work-item? Readings: (a) No (recommended, as the note gives): no line; (b) Yes: a line listing it under the r123 work-item's `## Retires` when a capability-proposal of the initiative removes its requirement.
  Answer: 2026-10-25: 6: (a), no line (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i35/supervision.md
- .shop/work/i35/runs/supervision/1-gate
- .shop/work/i35/runs/i35/1-integrate/drafts/round-1/

Run directory: /tmp/work-run-i35-geaeg_4d/supervision-2-apply/.shop/scratch/2-apply
Result file: /tmp/work-run-i35-geaeg_4d/supervision-2-apply/.shop/scratch/2-apply/result.json

You start in your worktree, /tmp/work-run-i35-geaeg_4d/supervision-2-apply: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
