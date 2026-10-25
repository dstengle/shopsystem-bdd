/tmp/work-run-i30-o1gqd7vm/i30-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md
/tmp/work-run-i30-o1gqd7vm/i30-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/formulation.md

## Change list

| change | capability | id | line | note sentence |
|---|---|---|---|---|
| added | supervision | r109 | **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted. | "When a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions` one question asking for the approval of the proposal's lines as drafted." (q7 line 1) |
| added | supervision | r110 | **When** a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends. | "When a work-item drafted for a kept branch review's findings turns `green`, `work run` shall start the next branch review of the initiative before it ends." (q7 line 2) |
| changed | supervision | r19 | new: **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns. / old: **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 40 turns. | "When `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns." (q7 line 3) |
| added | formulation | r23 | **When** `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`. | "When `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`." (q7 line 4) |

No glossary term added, changed or removed. No decision file drafted.

Placement: r109 follows r85 (the gate's questions), r110 follows r74 (the findings' work-item), r19 stays where it is, formulation r23 follows r5 (old scenarios). Supervision's frontmatter is unchanged, since no id is retired. Formulation's frontmatter is unchanged: r23 is one above r22, the highest it uses or retires.

## Questions

1. supervision r19: q7 line 3 names only the turn limit, but r19 also gives the researcher the file set and accepted scenarios. I drafted r19 with only the limit changed (40 to 80), so nothing is lost: `[r19] **When** `work run` starts a researcher, `work run` shall give it the work-item's file set and accepted scenarios and a limit of 80 turns.` The other reading takes line 3's words alone and drops the file set and scenarios: `[r19] **When** `work run` starts a researcher, `work run` shall give the researcher a limit of 80 turns.` Recommended: the first.
2. supervision r110 against r27/r50 (you asked me to flag this): in my reading r110 mostly repeats r27. A fix work-item turning `green` makes a merge commit that no kept branch review has read. So r50 does not block a review, and r27 already starts the next branch review once every work-item is `green` or `withdrawn`. r110 adds something only when another work-item is still not `green` or `withdrawn`, or when the delivery would end first. It is drafted as worded. Readings: (a) keep r110 as an added line; (b) drop r110 as a duplicate of r27, adding nothing; (c) keep r110 and narrow it so that it does not clash with r27's guard: `[r110] **When** a work-item drafted for a kept branch review's findings turns `green` and every work-item of the initiative is `green` or `withdrawn`, `work run` shall start the next branch review of the initiative before it ends.`
3. supervision r110: "before it ends" can mean before the initiative ends (is done) or before `work run` ends. Readings: (a) the initiative, so the next review is started before `measure initiative` (r75); (b) the delivery, as written now: `... shall start the next branch review of the initiative before `work run` exits.`
4. Glossary, supervision r19 (and r86-r90's "turn limit"): "turn" is a glossary term for a side of a request. The unit `--max-turns` limits is the "round trip". Should r19 say `... and a limit of 80 round trips.`? Or should "80 turns" stay as written, with r19's earlier "40 turns" as precedent?
5. supervision r109: r85 and r109 both fire when a gate round ends, and r69 then makes the proposal `awaiting-answer`. I assumed r109 writes its question before r69's transition, so r70 does not find every question answered at once. The line does not say so. If an order is wanted: `[r109] **When** a round of the kind `gate` that `work run` started for a capability-proposal gives no question, `work run` shall write under the proposal's `## Questions`, before it transitions the proposal to `awaiting-answer`, one question asking for the approval of the proposal's lines as drafted.`

## Cut sentences

None. Each of q7's four lines landed as a Behaviour line. The title, "The loop's gates, reviews and limits as runs showed them", is a heading, not a sentence.
