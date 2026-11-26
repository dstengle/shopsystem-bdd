---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-119/review-1
kind: review
batch: batch-119
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/142
head: 9b975fdd2711fd34469194ce84c7d10794c66da3
range: 8c19eff44110f61575e3b4e326beb08829ea5042..9b975fdd2711fd34469194ce84c7d10794c66da3
result: clean
---

# batch-119 review 1

## Verdict

The batch builds all of b618: it imports `base` into spec/index.md, retires the `object version kind of text` model line, and takes the shared.md entries of bounded context, file, text and repository out, with version's entry going along with its element. The objects text, file, repository and bounded context stay in spec/model/specification.md, read as the base pack's nouns. The code changes are what the import needs for this repository's spec to keep reading. Every run exits 0 and the change is within the size limit. Two observations, nothing to fix now.

## Findings

### f1 Minor observation: v_t16 now tells a verb from a pack's noun, a rule change b618 has no line for
- item: b618
- where: scripts/spec_packs.py:583
`sense` changes what v_t16 counts as redefining a pack's word. A verb such as "file" beside the base pack's noun "file" now neither redefines it nor hides it; any other part of speech still does. `spec_rgl_vocab.lexicon` also keeps both entries. None of b618's lines (an import and five retirements) names this rule. It is still inside the item: without it, importing `base` would raise v_t16 on this repository's verb "file" and hide the pack's noun. b618's Notes give this as the reason, and `test_a_verb_spelled_as_a_packs_noun_neither_redefines_nor_hides_it` covers it. It is recorded because the rule change reaches every consuming context that imports a pack, with no requirement line saying so. It could be written as a checking line in a later item.

### f2 Minor observation: the domain model cache's check of spec/index.md has no test
- item: b618
- where: scripts/domain_model.py:558
`_load` now reuses a cached Model only if spec/index.md is unchanged too, but it checks this only when the model looked a parameter up among the imported packs' kinds (`asked`). The risk I checked: a context that adds or removes an import in the same process would keep a stale parameter type. The code does compare `_stamp(root, True)`, so the risk is handled. But no test changes the index's `imports:` between two `domain_model.load` calls and checks the parameter's type. Reproduction for a test: load the fixture of `test_a_parameter_naming_an_imported_packs_kind_the_model_refers_to_is_that_kind`, rewrite index.md to `imports: [request]`, load again, and expect `("text", ())` for `version`.
