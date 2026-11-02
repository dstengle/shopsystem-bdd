## Coverage

| Id | Line | Scenario |
|---|---|---|
| r221 | **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold for a glossary-proposal, `work run` shall start a new round of the kind `integrate` for the glossary-proposal. | an apply round that gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for the glossary-proposal |

## Questions

None. r221 has one reading. "for a glossary-proposal" might attach to the apply round or to the answer, but either way it is the apply round started for that glossary-proposal (r165), so the scenario is the same.

## Cases no line mentions

- An apply round for a glossary-proposal that applies some of its drafts and also gives an answer those drafts do not hold. r166 would set the glossary-proposal `approved` and r221 would start a new integrate round. No line says which one wins, or whether both happen. The scenario avoids this by having the apply round apply nothing, the same way @r150 does.
- What status the glossary-proposal has while the new integrate round runs and after it ends. No line says whether it stays `awaiting-answer`, goes back to `drafted`, or whether the new round's drafts go to a new glossary-proposal.
- Whether the new integrate round for a glossary-proposal is given the answers that sent it back. r221, like r150, says only that it is started.
- r150 has a follow-on line, r151, that holds formulate rounds back until the new drafts are applied. No line does the same for a glossary-proposal, for example holding back other apply rounds that use the terms being re-integrated. r55 withholds terms that are not approved, which may already cover this, but no line says so.

## Drafts

- /tmp/work-run-i64-fow6jpdp/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.feature
- /tmp/work-run-i64-fow6jpdp/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.reply.md
