/tmp/work-run-i55-k2ut5f4r/requests-deda9fa6-4-integrate/.shop/scratch/4-integrate/drafts/round-4/spec/capabilities/requests.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | requests | r52 | **While** an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in. | The person's answer (2026-11-02, under the delegation of The person, 2026-10-27): "Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream, so an answer sent alone leaves `work show` printing the asker's turn under r51; and 'awaiting the upstream' is only the description printed of who acts next, not a new status named awaiting-upstream." |
| added | requests | r73 | **While** a turn the asker has passed to the upstream, with any answers sent with it, has not been taken in by the upstream, `work show <request>` run on either side shall print the upstream as the side that acts next and that the turn is not yet taken in. | The same answer, quoted above. |

The drafted frontmatter puts r52 in `retired`: [r6, r1, r3, r13, r34, r39, r41, r43, r14, r69, r52]. r73 sits where r52 was in Behaviour. No other line changed. No glossary change and no decision file.

## Questions

None.

## Cut sentences

None. The clause "an answer sent alone leaves `work show` printing the asker's turn under r51" is already held by r51 and r73's condition (a passed turn only). The clause "'awaiting the upstream' is only the description printed of who acts next, not a new status named awaiting-upstream" is held by r73's response: it prints the upstream as the side that acts next, and r18 still sets the status by itself.
