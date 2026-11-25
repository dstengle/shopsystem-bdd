---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-100/review-1
kind: review
batch: batch-100
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/123
head: 6162a9e28ee8f09abfe2fa33c2d5ce226db94c68
range: 03553be17d9979cd9d8c66bf75b78b4135136d77..6162a9e28ee8f09abfe2fa33c2d5ce226db94c68
result: clean
---

# batch-100 review 1

## Verdict

The batch builds all three of b609's lines. `checking#r104` is met because `domain_model_check` now counts the imported packs' kinds as declared. `checking#r105` is met by the new `grammar/packs/base.md`, which `spec lexicon` shows under `[pack base]`. `upgrades#r45` is met because `migrate init` now writes `imports: [base, request]`. Every run exits 0 at the head and at the base, the features are as `features generate` writes them, no test is removed or weakened, and the change of 21 files, +328 -21, is within the 1000-line limit. The new modules have their rows in CLAUDE.md's module map, and the change goes against none of the judgement decisions. Two minor observations, nothing to fix now.

## Findings

### f1 Minor observation: spec_packs.kinds' docstring names a reader that does not exist
- item: b609
- where: scripts/spec_packs.py:54
The docstring says the kinds are what "domain_model reads as `pack_kinds`". Nothing in the tree is called `pack_kinds`; a grep of every `*.py` file finds it only in this docstring. The kinds are read by model_domain (`read_domain`, which passes them to `domain_model_check.problems`) and by `spec_vocabulary_terms.lexicon`. A reader who follows the docstring looks for a name that is not there. Fix: name the two real readers.

### f2 Minor observation: a relation to an imported pack's kind as a lexicon row is tested by nothing
- item: b609
- where: scripts/spec_vocabulary_terms.py:192
`lexicon` now adds each imported pack's kind to the kinds that `rows` reads. With it, a `has → file` or `holds → file` relation to a pack's kind becomes a row (`K | of | O`, `K | in | O`), which gives grammar 4 new noun phrases such as "the file of the note". The g104 scenario builds the relation `refers to → binder`. That is a state verb's phrase, which `rows` skips. So no scenario and no script test runs this path. I searched the tree for `spec_packs.kinds` and found only the two callers in `scripts/`. A regression here would go unnoticed. The item's notes ask for this change, so it is not code that no line asks for. Fix: a script test where a fixture model `has →` a base kind and `rows` gives the row.
