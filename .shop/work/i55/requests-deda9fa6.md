---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i55-requests-deda9fa6
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i55
status: drafted
argues: [requests]
date: 2026-11-02
adds: [requests#r73]
changes: []
removes: [requests#r52]
---

# requests: the lines applied in deda9fa6

Hand repair by the person's session, 2026-11-02, from branch review 2 of i55 (.shop/work/i55/runs/branch-review/2/result.json): commit deda9fa6 applied requests r50-r58 (retiring r13, r34, r39, r41, r43) to spec/ with the person's approval of 2026-10-29, but no proposal of i55 named them, so they had no scenario and no work-item. This proposal names them, approved as they stand in spec/, for a formulate round and then a work-item. The person chose on 2026-11-02 to build them in i55.

## Questions
- requests r52: "While an answer or a turn the asker has sent has not been taken in by the upstream, `work show <request>` shall print the request on either side as awaiting the upstream and not yet taken in." Reading 1: an answer sent alone, with the turn still the asker's, is enough, so show prints awaiting the upstream even in the asker's turn (clashes with r51). Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream; an answer sent alone leaves show printing the asker's turn under r51. Also: is 'awaiting the upstream' the status awaiting-upstream or only a description of who acts next?

## Answers
- 2026-11-02: Reading 2: only a sent turn (with any answers sent with it) makes the request await the upstream, so an answer sent alone leaves `work show` printing the asker's turn under r51; and 'awaiting the upstream' is only the description printed of who acts next, not a new status named awaiting-upstream. (Under the delegation of The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me.")
  by: work run, under the delegation "The person, 2026-10-27: "I'm delegating this to you. Please get the new version delivered without involving me." Lines 1-9 are i39's requests gate answers a formulate round could not draft (q14 lines 13-16 among them): line 1 replaces requests r13 (r14, an observation listing under work status, is retired with work status); lines 2-5 are q14 lines 13-16 naming work show; line 6 replaces r34; lines 7-9 replace r39, r41 and r43, a 'message' being an answer or a turn. Requirement lines are retired and replaced, never edited. Lines 10-13 fix the bugs i39 met. Answer every question with its recommended reading; where none is recommended, choose the one a test can check."

The drafts of this proposal are in .shop/work/i55/runs/requests-deda9fa6/4-integrate/drafts/round-4/.
