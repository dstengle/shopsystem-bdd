---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-161/review-2
kind: review
batch: batch-161
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/184
head: 312ebb1aa44947ba51961bdea5e0c7734bab7455
range: ab7b3d847460c53819e595cedc687ef444502238..312ebb1aa44947ba51961bdea5e0c7734bab7455
result: clean
---

# batch-161 review 2

## Verdict

The fix rewords drafting#r107 on b829 to "rewords the requirement in the item with the same text". Its logical form now holds `param(e1, text, x2)`, so the line no longer covers every reword r106 covers. It now matches `scripts/backlog_reword.py`, which changes nothing only when the text is the one the item holds. The model gives `reword` its `text` parameter. The CLI table adds `text = { positional = 2 }`. The r107 scenario's When says the text. The handler (`tests/scenarios/drafting_handlers_returned.py`) now tells r106 from r107 by the step's `text` parameter, not by its tag. r107 is out of `unbuilt:` again. Every run exits 0. f1 is fixed. Two observations remain, and neither holds the merge.

## Findings

### f6 Minor observation: r106 still covers a reword to the same text, and `spec logic` cannot see the clash with r107
- item: b829
- where: spec/capabilities/drafting.md:349
- r106's trigger, "When the person rewords a requirement in an item", names no `text` parameter. A request with fewer parameters covers one with more, so r106 still obliges "keep a different requirement" on a reword to the same text. r107 obliges "change nothing" on that same reword.
- `spec logic` reads the two lines as two triggers, because a parameter given in one line and absent from the other makes two triggers (spec_lf_facts_request). It therefore raises no L1, and r107's If precedence does not apply across them.
- The code and the tests do what r107 says, so nothing is wrong in behaviour. Only the spec is still loose.
- Hardening: on a later item, r106 could be worded with a text different from the one the item holds.

### f7 Minor observation: the amend's catalogue rewrite dropped v_t22's entry, and the relay moved g108 and g109
- item: -
- where: grammar/rules.md:1338
- 1c58241e5, the `work batch amend` commit, deleted the v_t22 entry from `grammar/rules.md`. 553af41a7 put it back by hand, so the net change has no difference in `grammar/rules.md`. The cause is the amend writing the catalogues without the batch's scripts, and idea b836 is already filed for it.
- The same relay moved `[g108]` and `[g109]` above `[g107]` in `spec/capabilities/drafting.md`. Their text is the same, the feature file's order is the same, and `features generate --check` exits 0. The move only adds lines to the diff.

## Earlier findings
- f1: fixed
