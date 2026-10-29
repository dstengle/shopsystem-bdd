---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r50, work-queue#r51, work-queue#r52, work-queue#r53, work-queue#r54, work-queue#r55, work-queue#r56, work-queue#r57, work-queue#r58]
changes: []
removes: [work-queue#r7, work-queue#r21, work-queue#r28, work-queue#r15, work-queue#r35, work-queue#r38]
date: 2026-10-29
---

# work-queue

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- work-queue r52: the field `ok` is named in the Behaviour lines. Drafted: r52 "The JSON object that `work` gives shall hold the field `ok`."; r53 "**When** `work` does what it was asked, `work` shall give `ok` true in its JSON object."; r50 "**If** `work` cannot do what it was asked, **then** `work` shall give `ok` false in its JSON object, saying why, and change nothing." Readings: (a) name `ok` in the lines, as drafted, since the note's A1 puts the shape in the contract [recommended]; (b) the lines say "whether `work` did what it was asked" and `ok` is named only in Implementation, e.g. r52: "The JSON object that `work` gives shall hold whether `work` did what it was asked."
- work-queue r35 and r38, removed: r35 "**Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object." and r38 the same for `work show`; r51 "`work` shall give its output as one JSON object on stdout." replaces them. Once JSON is the default, what does `--json` do? Readings: (a) refused as an unknown option, Implementation: "`--json` is no longer an option; given, it is refused as bad usage" [recommended]; (b) accepted and ignored, Implementation: "`--json` is accepted and changes nothing", which keeps callers that pass it working.
- work-queue r7, r21, r28, r15, removed (each said `work` shall "exit with an error"), replaced by r50, r56, r57, r58 (`ok` false) with r54 "**When** `work` ends without crashing on an error it does not handle, `work` shall exit successfully." and r55 "**If** `work` crashes on an error it does not handle, **then** `work` shall exit with an error." Approve retiring all four, so `work run` and the suite read `ok` in place of the exit code (the note's A2)? Readings: (a) approve all four [recommended]; (b) keep an error exit for some `work` refusals (name which), which A2 does not allow.
- work-queue r34, r36, r37 are kept unchanged but say `work` shall "print" each initiative, request, work-item and status; r51 now sits over them. Readings: (a) keep them, read under r51 so what is printed is the JSON object's fields [recommended, no change to approved lines]; (b) retire each and redraft it as "shall give ... in its JSON object", e.g. r37: "**When** `work show <work-item>` is run, `work` shall give the work-item's status and its open questions in its JSON object."
