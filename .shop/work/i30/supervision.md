---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i30-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i30
status: awaiting-answer
argues: [supervision]
adds: [supervision#r109, supervision#r110]
changes: [supervision#r19]
removes: []
date: 2026-10-25
---

# supervision

The drafts of this proposal are in .shop/work/i30/runs/i30/1-integrate.

## Questions
- Scope of r19's change. r19 (supervision, changed): **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns. Was: ... and a limit of 40 turns. Readings: (a) keep the file set and scenarios, changing only the limit (as drafted, recommended); (b) take q7 line 3's words alone: `**When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.` (drops the file set and scenarios).
- r110 against r27/r50. r110 (supervision, added): **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends. A fix work-item turning `green` leaves an unread commit, so r27 already starts the next review once every work-item is `green` or `withdrawn`. Readings: (a) keep r110 as drafted (recommended: the person accepted it; it also covers other work-items still open); (b) drop r110 as a duplicate of r27; (c) narrow it: `... turns `green` and every work-item of the initiative is `green` or `withdrawn`, ...`.
- r110 'before it ends'. r110 (supervision, added): **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends. Readings: (a) before the initiative is done, so the review comes before `measure initiative` (r75); (b) before `work run` exits: `... before `work run` exits.` Recommended: (b), as the request's own delegation text reads 'before it ends' of `work run`.
- r19 '80 turns'. r19 (supervision, changed): **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns. Was: ... a limit of 40 turns. 'turn' is a glossary term for a side of a request; the unit limited is a round trip. Readings: (a) keep '80 turns' as written (recommended, precedent '40 turns'); (b) say '80 round trips'.
- r109 order. r109 (supervision, added): **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted. It fires with r85 when the gate round ends, and r69 then makes the proposal `awaiting-answer`. Readings: (a) keep as drafted (recommended, the order is the script's); (b) state the order: `... shall write under the proposal's `## Questions`, before it transitions the proposal to `awaiting-answer`, one question ...`.
