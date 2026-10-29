---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-feature-file-tools
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [feature-file-tools]
adds: [feature-file-tools#r63, feature-file-tools#r64, feature-file-tools#r65, feature-file-tools#r66, feature-file-tools#r67, feature-file-tools#r68, feature-file-tools#r69, feature-file-tools#r70, feature-file-tools#r71, feature-file-tools#r72, feature-file-tools#r73]
changes: []
removes: [feature-file-tools#r46, feature-file-tools#r7, feature-file-tools#r60, feature-file-tools#r61, feature-file-tools#r62, feature-file-tools#r17, feature-file-tools#r25, feature-file-tools#r58]
date: 2026-10-29
---

# feature-file-tools

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- feature-file-tools r64, r65, r68, r71, r72 (added): must the Behaviour lines name the field `ok`? (a) Yes, as drafted, since the note's A1 puts each command's JSON shape in its contract: r64 'The JSON object that `features` gives shall hold the field `ok`.' and r68 '**If** `features` cannot do what it was asked, **then** `features` shall give `ok` false in its JSON object, saying why, and change nothing.' (b) The lines say 'whether it did what it was asked' and `ok` is named only in Implementation, e.g. r64 'The JSON object that `features` gives shall hold whether `features` did what it was asked.' Recommended: (a).
- feature-file-tools r63-r73 (added) and r60-r62 (removed): after JSON becomes the default, what does `--json` do? r60-r62 are removed, so nothing in Behaviour covers it. (a) It is refused as an unknown option; Implementation says '`--json` is no longer an option; given, it is refused as bad usage'. (b) It is accepted and ignored; Implementation says '`--json` is accepted and changes nothing'. Recommended: (a), one way to ask for the output.
- feature-file-tools r16 and r26 (kept, not in this change; they still say `features` shall 'print how many scenarios match and exit successfully' and 'say so and exit successfully'), against the added r65 and r70-r72 and the removed r17, r25, r58, r46: (a) keep r16 and r26 as they are, read under the new JSON-object lines (as drafted). (b) retire each and redraft it: r16 as '**When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` shall give how many scenarios match in its JSON object, with `ok` true.' and r26 as '**When** `features bindings` finds every binding names a scenario, `features` shall give `ok` true in its JSON object.' Recommended: (b), since r16 and r26 are the success cases of the failing cases r70 and r71 that were redrafted, and an exit-code reading no longer holds.
- feature-file-tools r73 (added): '**When** `features` shows Gherkin text, `features` shall give the text inside a field of its JSON object.' No `features` command in spec/ shows Gherkin or a scenario, so the line has no command to bind to. Which does the note's A1 ('features showing Gherkin') mean? (a) Keep r73 general, as drafted. (b) Name a new command: '**When** `features show <title>` is run, `features` shall give the scenario's Gherkin inside a field of its JSON object.' (a new command, to be built). (c) Drop r73. Recommended: (b) if a command that shows a scenario is wanted; otherwise (c), since a general line with no command cannot get a scenario.
