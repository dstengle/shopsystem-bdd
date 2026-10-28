I wrote one new scenario for supervision r173. It is in a draft file only. I did not edit `features/` or `spec/`.

## Coverage

| Line | Scenario |
|---|---|
| r173 | @r173 "when the gate round `work run` started for a glossary-proposal ends with no question, one question asking the person to approve the terms it adds, changes and removes is written" |

The scenario uses one proposal that adds, changes and removes a term ("ledger", "shelf" and "loan"), so the check covers all three. Most steps reuse existing wording:
- **Givens:** the first Given is copied from @r164. The second Given ("the gate round's result gives no question, and every round ends") is copied from @r117.
- **When and first Then:** both are copied from @r117 ("When the person runs `work run i1`", "Then a round of the kind gate was started for g1").

The last Then is the only new step wording: "And one question was written for g1, asking the person to approve the terms "ledger", "shelf" and "loan"". It does not say where the question is written, because r173 does not say. It does not check that g1 becomes awaiting-answer either, because r169 covers that.

## Questions

None. Your answer settled where the question is written: r173 as drafted, so the scenario only says the question is written for the proposal.

## Cases no line mentions

- r117 writes its question under the proposal's `## Questions`, and r173 names no place. Once this question exists, r165 and r172 count it among the gate's questions. Neither line says whether a question written by `work run` itself counts as one "that a round of the kind `gate` gave".
- No line says what happens when the gate round gives no question for a glossary-proposal that adds, changes and removes nothing.

## Drafts

- /tmp/work-run-i50-dmmrs8mf/supervision-3-formulate/.shop/scratch/3-formulate/drafts/supervision.fragment.feature
