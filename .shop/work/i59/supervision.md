---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [supervision]
adds: [supervision#r188, supervision#r189, supervision#r190, supervision#r191, supervision#r192, supervision#r193, supervision#r194, supervision#r195, supervision#r196, supervision#r197, supervision#r198, supervision#r199, supervision#r200, supervision#r201, supervision#r202, supervision#r203, supervision#r204, supervision#r205, supervision#r206, supervision#r207, supervision#r208]
changes: []
removes: [supervision#r9, supervision#r101, supervision#r32, supervision#r52, supervision#r81, supervision#r82, supervision#r53, supervision#r10, supervision#r96, supervision#r107, supervision#r88, supervision#r115, supervision#r40, supervision#r46, supervision#r51]
date: 2026-10-29
---

# supervision

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- supervision r193, r194, r195, r196 (added; they replace removed r101, r32, r52, r81): when `work run` ends waiting on the person or on a fault, does its JSON object give `ok` true or false?
  Drafted lines: r193 "**When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall give `ok` false in its JSON object, with the request and its open questions."; r194 "**When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall give `ok` false in its JSON object, with each work-item's status and each open question."; r195 (same, a work-item `failed`, `ok` false, each fault); r196 (no initiative given, a node `awaiting-answer` or `failed`, `ok` false, the status of each initiative it took). The lines they replace said "exit with an error" for all of these.
  Readings: (a) `ok` false for waiting on an answer as for a fault, as drafted (RECOMMENDED: keeps the old exit-with-error behaviour, and one field says 'nothing more can be done without the person'); (b) `ok` true when a work-item is `awaiting-answer` or a request is in the asker's turn, the status in the JSON object saying it waits, and `ok` false only for `failed`; e.g. r194 would read "**When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall give `ok` true in its JSON object, with each work-item's status and each open question." (r193 and r196's awaiting part change the same way).
- supervision r189 (added): does the Behaviour line name the field `ok`?
  Drafted line: r189 "The JSON object that `work run` gives shall hold the field `ok`." (A1 puts each command's JSON shape in its contract); r192-r208 also say `ok` true or false.
  Readings: (a) name `ok` in the Behaviour lines, as drafted (RECOMMENDED: the lines are checkable, and r208 relies on the field by name); (b) the lines say "whether `work run` did what it was asked" and `ok` is named only in Implementation, e.g. r189: "The JSON object that `work run` gives shall hold whether `work run` did what it was asked." with r190-r208 worded to match.
