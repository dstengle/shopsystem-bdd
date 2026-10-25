# Gate, integrate round 1 (q7)

No glossary entries, no decisions, no removals. Drafts: `.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/{supervision,formulation}.md`.

## supervision
- ADDED [r109] **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted.
- ADDED [r110] **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends.
- CHANGED [r19] **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns.
  Was: ... and a limit of 40 turns.

## formulation
- ADDED [r23] **When** `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`.

## Questions
1. r19: keep the file set and scenarios, changing only the limit (as drafted, recommended), or take q7 line 3's words alone: `**When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.` (drops the file set and scenarios).
2. r110 against r27/r50: a fix work-item turning `green` leaves an unread commit, so r27 already starts the next review once every work-item is `green` or `withdrawn`. Readings: (a) keep r110 as drafted (recommended: the person accepted it; it also covers other work-items still open); (b) drop r110 as a duplicate of r27; (c) narrow it: `... turns `green` and every work-item of the initiative is `green` or `withdrawn`, ...`.
3. r110 "before it ends": (a) before the initiative is done, so the review comes before `measure initiative` (r75); (b) before `work run` exits: `... before `work run` exits.` Recommended: (b) as the request's own delegation text reads "before it ends" of `work run`.
4. r19 "80 turns": "turn" is a glossary term for a side of a request; the unit limited is a round trip. Keep "80 turns" as written (recommended, precedent "40 turns") or say "80 round trips".
5. r109 order: it fires with r85 when the gate round ends, and r69 then makes the proposal `awaiting-answer`. Keep as drafted (recommended, the order is the script's) or state it: `... shall write under the proposal's `## Questions`, before it transitions the proposal to `awaiting-answer`, one question ...`.

Cut sentences: none.
