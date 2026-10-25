# formulate of supervision

Capability-proposal: .shop/work/i30/supervision.md
Agent: initiative-round
Scripts: /home/vscode/shopsystem-bdd/scripts
Kind: formulate
Base: 4fbc25cd32843edb441abb8b04189f38edde1105
Worktree: /tmp/work-run-i30-chbawhjx/supervision-3-formulate
Branch: round/supervision-3-formulate
Answers the person gave, each with the question it answers:
- Question: Scope of r19's change. r19 (supervision, changed): **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns. Was: ... and a limit of 40 turns. Readings: (a) keep the file set and scenarios, changing only the limit (as drafted, recommended); (b) take q7 line 3's words alone: `**When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.` (drops the file set and scenarios).
  Answer: 2026-10-25: 1: (a), keep the file set and scenarios, change only the limit (the coordinator under the person's delegation 2026-10-25)
- Question: r110 against r27/r50. r110 (supervision, added): **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends. A fix work-item turning `green` leaves an unread commit, so r27 already starts the next review once every work-item is `green` or `withdrawn`. Readings: (a) keep r110 as drafted (recommended: the person accepted it; it also covers other work-items still open); (b) drop r110 as a duplicate of r27; (c) narrow it: `... turns `green` and every work-item of the initiative is `green` or `withdrawn`, ...`.
  Answer: 2026-10-25: 2: (a), keep r110 as drafted (the coordinator under the person's delegation 2026-10-25)
- Question: r110 'before it ends'. r110 (supervision, added): **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends. Readings: (a) before the initiative is done, so the review comes before `measure initiative` (r75); (b) before `work run` exits: `... before `work run` exits.` Recommended: (b), as the request's own delegation text reads 'before it ends' of `work run`.
  Answer: 2026-10-25: 3: (b), before work run exits (the coordinator under the person's delegation 2026-10-25)
- Question: r19 '80 turns'. r19 (supervision, changed): **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns. Was: ... a limit of 40 turns. 'turn' is a glossary term for a side of a request; the unit limited is a round trip. Readings: (a) keep '80 turns' as written (recommended, precedent '40 turns'); (b) say '80 round trips'.
  Answer: 2026-10-25: 4: (a), keep '80 turns' (the coordinator under the person's delegation 2026-10-25)
- Question: r109 order. r109 (supervision, added): **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted. It fires with r85 when the gate round ends, and r69 then makes the proposal `awaiting-answer`. Readings: (a) keep as drafted (recommended, the order is the script's); (b) state the order: `... shall write under the proposal's `## Questions`, before it transitions the proposal to `awaiting-answer`, one question ...`.
  Answer: 2026-10-25: 5: (a), keep as drafted. Its id: spec now holds supervision r109 (i29's line, 3bfdba68, applied after this round's integrate), so this proposal's r109 is numbered r117 (r116 is drafted by i31) (the coordinator under the person's delegation 2026-10-25)

Read (paths in your worktree):
- .shop/work/i30/supervision.md
- .shop/work/i30/runs/supervision/1-gate
- .shop/work/i30/runs/supervision/2-apply

Run directory: /tmp/work-run-i30-chbawhjx/supervision-3-formulate/.shop/scratch/3-formulate
Result file: /tmp/work-run-i30-chbawhjx/supervision-3-formulate/.shop/scratch/3-formulate/result.json

You start in your worktree, /tmp/work-run-i30-chbawhjx/supervision-3-formulate: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
