---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-design-model-check
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [design-model-check]
adds: [design-model-check#r125, design-model-check#r126, design-model-check#r127, design-model-check#r128, design-model-check#r129, design-model-check#r130, design-model-check#r131, design-model-check#r132, design-model-check#r133, design-model-check#r134, design-model-check#r135, design-model-check#r136, design-model-check#r137, design-model-check#r138, design-model-check#r139]
changes: []
removes: [design-model-check#r2, design-model-check#r11, design-model-check#r33, design-model-check#r12, design-model-check#r15, design-model-check#r108, design-model-check#r65, design-model-check#r109, design-model-check#r105, design-model-check#r13]
date: 2026-10-29
---

# design-model-check

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- design-model-check, form of the `ok` field. r126 reads: "The JSON object that `model` gives shall hold the field `ok`." and r127, r130, r133, r134, r138 name `ok` true/false. Readings: (a) [recommended] name `ok` in the Behaviour lines as drafted, since request line 1 puts the shape in the contract; (b) the lines say "whether it did what it was asked" and `ok` is named only in Implementation, e.g. "The JSON object that `model` gives shall hold whether `model` did what it was asked."
- design-model-check, `--json` after JSON becomes the default (removes r33, r108, r109). Readings: (a) [recommended] `--json` is refused as an unknown option (Implementation: "`--json` is no longer an option; given, it is refused as bad usage"); (b) accepted and ignored (Implementation: "`--json` is accepted and changes nothing").
- design-model-check, text inside a field. Drafted: r139 "**When** `model facts` is run, `model facts` shall give inside a field of its JSON object the facts read, one a line in clingo's syntax, using only the standard library." (replaces r13) and r137 for `model rules` (replaces r65; the request names text for `model rules`). Readings: (a) [recommended] keep r139 and r137; (b) text only where the request names it: retire r139, keep r13 unretired. Also: do report commands keep a text form in a field? If yes, add "**When** `model check` is run, `model check` shall give inside a field of its JSON object the text of what it finds, one relation's code, label and count above its rows."; [recommended] no.
- design-model-check, lines still saying "print" or "say so and exit successfully": r1 ("shall say so and exit successfully"), r16 (`model why` "shall print the requirement's text..."), r17 ("shall say so and exit successfully"), r37 ("shall say the file is current and exit successfully"). Readings: (a) [recommended] keep them, read under the new JSON-object lines (r125, r127, r135) as drafted; (b) retire each and redraft as "shall give ... in its JSON object".
