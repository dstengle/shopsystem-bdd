---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-migration-tools
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [migration-tools]
adds: [migration-tools#r37, migration-tools#r38, migration-tools#r39, migration-tools#r40, migration-tools#r41, migration-tools#r42, migration-tools#r43, migration-tools#r44, migration-tools#r45]
changes: []
removes: [migration-tools#r7, migration-tools#r30]
date: 2026-10-29
---

# migration-tools

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- migration-tools r37-r45 (adds), r7 and r30 (removes): is the field `ok` named in the Behaviour lines? (a) Yes, as drafted (recommended): r38 "The JSON object that `migrate` gives shall hold the field `ok`."; r39 "**When** `migrate` does what it was asked, `migrate` shall give `ok` true in its JSON object."; r42, r43 and r45 name `ok` likewise. (b) The lines say "whether it did what it was asked" and `ok` is named only in Implementation, e.g. "The JSON object that `migrate` gives shall hold whether `migrate` did what it was asked."
- migration-tools r37 ("`migrate` shall give its output as one JSON object on stdout."): `--json` given after JSON is the default is (a) refused as an unknown option (Implementation: "`--json` is no longer an option; given, it is refused as bad usage"), or (b) accepted and ignored (Implementation: "`--json` is accepted and changes nothing"). Recommended: (b), since it breaks no caller that still passes it.
- migration-tools r44 ("**When** the plugin's SessionStart hook runs `migrate`, `migrate` shall give the text the hook tells the session inside a field of its JSON object."): (a) keep the line as drafted (recommended), since the note's A1 names the SessionStart hook as a command that prints text; or (b) retire it, so the hook's text is not a field of the JSON object.
