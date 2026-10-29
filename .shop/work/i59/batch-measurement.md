---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i59-batch-measurement
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i59
status: awaiting-answer
argues: [batch-measurement]
adds: [batch-measurement#r68, batch-measurement#r69, batch-measurement#r70, batch-measurement#r71, batch-measurement#r72, batch-measurement#r73, batch-measurement#r74]
changes: []
removes: [batch-measurement#r50]
date: 2026-10-29
---

# batch-measurement

The drafts of this proposal are in .shop/work/i59/runs/i59/1-integrate/drafts/round-2/.

## Questions
- batch-measurement r69: how is the field `ok` named? (a, recommended) In the Behaviour line, as drafted: [r69] "The JSON object that `measure` gives shall hold the field `ok`." (b) The line says what `ok` means and names `ok` only in Implementation: "The JSON object that `measure` gives shall hold whether `measure` did what it was asked." The other lines drafted stand either way: [r68] "`measure` shall give its output as one JSON object on stdout." [r70] "**When** `measure` does what it was asked, `measure` shall give `ok` true in its JSON object." [r71] "**When** `measure` ends without crashing on an error it does not handle, `measure` shall exit successfully." [r72] "**If** `measure` crashes on an error it does not handle, **then** `measure` shall exit with an error." [r73] "**If** `measure` refuses, **then** `measure` shall give `ok` false in its JSON object, with the reason it refuses." Removed: [r50] "**If** `measure` refuses, **then** `measure` shall exit with an error." (replaced by r73).
- batch-measurement r74: [r74] "**When** `measure show` or `measure compare` is run, `measure` shall give the text of its tables inside a field of its JSON object." The note names three text commands (the SessionStart hook, features showing Gherkin, model rules), not `measure show` or `compare`. (a, recommended) Keep r74: the tables are read as text, so they go inside a field. (b) Drop r74: `measure show` and `compare` give their tables as JSON data only.
