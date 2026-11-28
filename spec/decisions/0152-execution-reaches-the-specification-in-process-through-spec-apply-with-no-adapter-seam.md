---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/execution-reaches-the-specification-in-process-through-spec-apply-with-no-adapter-seam
summary: "The batches service reaches the specification through the specification service's module spec_apply, in the same process, with no driven port and no adapter swapped in by the environment."
date: 2026-11-28
status: accepted
tier: judgement
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-laying-port-is-wired-to-the-in-process-adapter]
---

# 0152. Execution reaches the specification in process through spec_apply, with no adapter seam

## Context

b611 put execution's use of the specification behind the driven port laying, wired to its in-process adapter by decision 0150, with $SHOPSYSTEM_LAYING naming another adapter as a test seam. The laying area owned no data, only operations, so its operations became the specification service's (quote-117): b871 to b873 moved lay, prepare and check into spec_apply and spec_apply_check, b874 and b875 took lift out (nothing is lifted), and b861 retires the area.

## Decision

Execution (the batches service's modules) reaches the specification through the specification service's module spec_apply (with spec_apply_check), called in the same process; it imports no other module of the specification area for it, as the import contract in .importlinter says. There is no adapter seam: no port module, no adapter chosen by an environment variable and no stand-in. Scenarios that need a failure of the specification build it from a real failing world (a rule no catalogue entry has, an unresponsive feature generator under $SHOPSYSTEM_GENERATE_TIMEOUT). Which adapter is wired stays a technical architecture decision (0125): when the specification moves into its own shop's context, a port and a remote adapter are added then, by a decision superseding this one.

## Alternatives

Keeping the laying port with the in-process adapter (0150): a port of no data whose one adapter calls spec_apply, kept only for a test seam real failing worlds already give.
