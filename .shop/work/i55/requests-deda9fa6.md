---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i55-requests-deda9fa6
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i55
status: awaiting-answer
argues: [requests]
date: 2026-11-02
adds: [requests#r50, requests#r51, requests#r52, requests#r53, requests#r54, requests#r55, requests#r56, requests#r57, requests#r58]
changes: []
removes: [requests#r13, requests#r34, requests#r39, requests#r41, requests#r43]
---

# requests: the lines applied in deda9fa6

Hand repair by the person's session, 2026-11-02, from branch review 2 of i55 (.shop/work/i55/runs/branch-review/2/result.json): commit deda9fa6 applied requests r50-r58 (retiring r13, r34, r39, r41, r43) to spec/ with the person's approval of 2026-10-29, but no proposal of i55 named them, so they had no scenario and no work-item. This proposal names them, approved as they stand in spec/, for a formulate round and then a work-item. The person chose on 2026-11-02 to build them in i55.

## Questions
- requests r52: "While an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in." Reading 1: an answer sent alone, with the turn still the asker's, is enough, so show prints awaiting the upstream even in the asker's turn (clashes with r51). Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream; an answer sent alone leaves show printing the asker's turn under r51. Also: is 'awaiting the upstream' the status awaiting-upstream or only a description of who acts next?
