## Coverage

| Line | Scenario |
|---|---|
| r180 | a started initiative fulfilling a request, with neither a capability-proposal, a glossary-proposal nor a work-item, is given to an integrate round with the accepted lines of the request |

The scenario reuses the wording of the retired @r93 scenario. The only change is "neither a capability-proposal, a glossary-proposal nor a work-item" in the Given step and the title. Its new Given step needs a step binding.

## Questions

None. r180 has only one reading.

## Cases no line mentions

- A started initiative with a glossary-proposal but no capability-proposal and no work-item. One example is the glossary-only initiative in the existing scenario at features/supervision.feature:1812. r180 does not apply to it, and no line says that `work run` starts no integrate round for it. If that should be pinned, it needs a line of its own.
- A started initiative whose request has no accepted line, for example every line refused. r180 would start an integrate round given no lines, and no line says whether it should.

## Drafts

- /tmp/work-run-i49-k6h3iltt/supervision-3-formulate/.shop/scratch/3-formulate/drafts/round-1/supervision.draft.feature
