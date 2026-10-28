/tmp/work-run-i47-ee1m2t30/requests-3-integrate/.shop/scratch/3-integrate/drafts/round-1/spec/capabilities/requests.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | requests | r59 | **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn and at least one line the line outcome refused, `work` shall set the request's status to `refused`. | q33 line 3: "When `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`." with Answer Q1 reading A, "it holds for either side" (refused is no longer the status of an all-withdrawn request; replaces r9) |
| added | requests | r60 | **When** `work turn` passes the turn of a request that is not `delivered` with every line's line outcome withdrawn, `work` shall set the request's status to `withdrawn`. | q33 line 3: "When `work turn` passes a request's turn with every line's outcome `withdrawn`, `work` shall set the request's status to `withdrawn`." with Answer Q1 reading A, "it holds for either side", and Answer Q2 reading A, "it holds only for a request that is not `delivered`" |
| added | requests | r61 | **When** `work turn` passes a request's turn to its upstream with a line whose line outcome is not withdrawn, `work` shall set the request's status to `awaiting-upstream`. | Answer Q1 reading A: "r18 changes to name a line whose outcome is not withdrawn" (replaces r18) |
| removed | requests | r9 | **When** the upstream ends its turn on a request that is not `delivered` whose every line has the line outcome refused or withdrawn, `work` shall set the request's status to `refused`. | replaced by r59 (q33 line 3, Answer Q1 reading A) |
| removed | requests | r18 | **When** `work turn` passes a request's turn to its upstream, `work` shall set the request's status to `awaiting-upstream`. | replaced by r61 (Answer Q1 reading A: "r18 changes to name a line whose outcome is not withdrawn") |

Frontmatter: `retired` is now [r6, r1, r3, r9, r18]. r7 is unchanged (Answer Q3 reading B: "nothing else changes (r7 stays)"). The file's form has no place for notes, so the answers are quoted here only.

No glossary terms were added, changed or removed.

## Questions

None.

## Cut sentences

None.
