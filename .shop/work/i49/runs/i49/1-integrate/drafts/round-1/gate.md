# Gate, integrate round 1 (i49, request q35)

## supervision

Removed:
- [r93] **When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` given the accepted lines of the request it fulfils. (id r93 retired)

Added:
- [r180] **When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils.
  (from q35 line 1: "...shall start a round of the kind `integrate` for it.")

## Glossary
No entry added, changed or removed.

## Decisions
None.

## Questions
1. r180: the request's line ends at "for it"; the clause "given the accepted lines of the request it fulfils" comes from retired r93 (and r79), not from the request.
   - Reading a (recommended, drafted): "... shall start a round of the kind `integrate` for it, given the accepted lines of the request it fulfils."
   - Reading b: "**When** a `started` initiative that fulfils a request has neither a capability-proposal, a glossary-proposal nor a work-item, `work run` shall start a round of the kind `integrate` for it."
