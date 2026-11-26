---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-168/review-1
kind: review
batch: batch-168
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/191
head: 659374fe0b06719ad4af0548a1d1f43dd1544d07
range: e81fa1ca63498c8510c49dcf6b0836e31946326f..659374fe0b06719ad4af0548a1d1f43dd1544d07
result: clean
---

# batch-168 review 1

## Verdict

The batch builds both items. b853's step now reports each requirement of a codified-2 capability that grammar 4 refuses on the upgraded tree, by id with the refusal, and g48's scenario checks both desk#r3 and notebook#r2. b854's `word()` now names a term by its entry's own word, so `follow-up` keeps its hyphen; its commit touches only the two chore files and its check is the hyphen test. Every run exits 0. There is nothing to fix now; three observations follow.

## Findings

### f1 Minor observation: one parse error anywhere hides every requirement's report and blames the grammar build
- item: b853
- where: scripts/upgrades/migrate_upgrade_stricter.py:188
`refused` parses every line inside a single `try`, and its `except Exception` catches any error from any line. If `spec_language.parse` raises on one line (a bug in a reading rule, a construct with no translation), the step drops the refusals of every other line too. Its one note then says "grammar 4 could not be built of this spec", which is not what happened. I read `spec_language._parse`: after the GF parse it calls `spec_lf_read.refusal` and `spec_catalogued.refusal` for each line, so an error there is a per-line error, not a build error. Fix: build or load the grammar once before the loop and catch only that failure. Catch each line's error inside the loop and report it under the line's id.

### f2 Minor observation: `word()` reads the lexicon and the model again for every note
- item: b854
- where: scripts/upgrades/migrate_upgrade_stricter.py:151
For every v_t13 or v_t22 note, `word` builds a new `Model(root)` and calls `spec_lexicon.read(root)`. On an upgrade of a large context with many such notes, that means many full reads of the lexicon. When two terms make the same id (`follow up` and `follow-up` both give `follow-up` in `Model.term_id`), it returns the first in lexicon order, which may not be the term the node came from. It also returns `t.term` as it stands, while `term_word` strips backticks before making the id, so a backticked term is printed with its backticks. Fix: build a map from node to word once in `plan` and pass it to `line`.

### f3 Minor observation: the new test's docstring cites the retired upgrades r47
- item: b854
- where: tests/scripts/test_migrate_upgrade_stricter.py:1
The docstring says "(b851, upgrades r47)". This batch retires r47 in favour of r48, and the step module's own docstring now cites r48. Fix: cite upgrades r48.
