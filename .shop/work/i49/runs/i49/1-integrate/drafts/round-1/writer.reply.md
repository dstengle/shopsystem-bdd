/tmp/work-run-i49-356hhium/i49-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md

## Change list

| change | capability | id | line | from the note |
|---|---|---|---|---|
| removed | supervision | r93 | **When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils. | "A started initiative with only a glossary-proposal is not integrated again (supervision r93 retired)" |
| added | supervision | r180 | **When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils. | "1. **When** a started initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it." |

No glossary term added, changed or removed.

## Decisions

None.

## Questions

1. supervision r180: the request's line ends at "for it"; the clause "given the accepted lines of the request it fulfils" comes from retired r93 (and r79), not from the request. Kept (as drafted): "... shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils." Dropped: "**When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it."

## Cut sentences

None.
