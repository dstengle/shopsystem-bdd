---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-161/review-1
kind: review
batch: batch-161
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/184
head: ab7b3d847460c53819e595cedc687ef444502238
range: 66e01bb39c09df371d13a5de62ed304e09b11238..ab7b3d847460c53819e595cedc687ef444502238
result: fix-now
---

# batch-161 review 1

## Verdict

The batch builds b828, b825 and most of b829. One finding is to fix: drafting#r107 as written says more than its group title and the code mean. As the line reads, it overrides drafting#r106 for every reword of a requirement an item holds. Three minor observations and one drop follow.

## Findings

### f1 Important fix now: drafting#r107 says any reword of a held requirement changes nothing, not only a reword to the same text
- item: b829
- where: spec/capabilities/drafting.md:334
The line says "While an item holds a requirement, if the person rewords the requirement in the item, then the drafting service shall change nothing and name the requirement."

1. **It conflicts with r106.** The While part is met whenever the item holds the requirement. r106 needs exactly that state too: it reads `in(x2, x3)` as its trigger's condition in grammar/corpus/spec/drafting.md, the r106 block. So r107's precondition and trigger cover every case r106 covers.
2. **The If form makes r107 win.** An If line takes precedence over a line of another form on its own trigger (grammar/check.lp's If tag). So `spec logic` raises no L1 between them. It reads r107 as overriding r106: no reword of an item's own line is ever kept.
3. **The code does something else.** `scripts/backlog_reword.py:573` changes nothing only when `dict(group.requirements)[rid] == text`. Otherwise it rewrites and commits. Measured against the line, the code breaks r107 whenever the text differs.
4. **The tests cannot catch it.** The scenarios of g106 and g107 are word for word the same up to the When. Only the test world `tests/scenarios/drafting_handlers_result.py` tells them apart, by giving R.PASSING to r107 and R.LINE to r106. Nothing in the spec does.

The group title says the intent: "Rewording a requirement to the text the item holds changes nothing". The line has to say it too.

Fix: reword r107 on b829 with `work line --reword` and `work batch amend` so that its condition is a reword to the text the item already holds. Check it with `spec parse --item b829` and `spec logic` so it no longer covers r106's trigger.

### f2 Minor observation: a reword of a term to its own text skips the lexicon-rule refusal
- item: b825
- where: scripts/backlog_model_edit.py:534
`reword_term` returns "unchanged" at `if new == bullet:`. That is before `backlog_term_rules.refuse` runs. Take an item that already holds a term breaking v_t22, written before this batch added the rule. A `--reword-term <t> -- <same bullet>` then exits 0 and prints `term <t> unchanged: ...`. drafting#r109 says that request is refused, naming the term. No client produces such an item today, because `--term` now refuses it. Running the rule check before the early return would close the gap.

### f3 Minor observation: the gloss of `fit` disagrees with FITS
- item: b825
- where: spec/vocabulary/specification.md:348
The gloss says "a proper noun a service or an actor". `scripts/spec_vocabulary.py:706`'s `FITS` also lets a proper noun name an object, and the module map row says so too ("a constant of its kind"). The gloss also leaves out a verb of no aspect, which FITS lets name an operation or a relation. The gloss is the definition the person reads, so it should say what the check does.

### f4 Minor observation: `work line --term` prints the bullet as given, not as kept
- item: b829
- where: scripts/backlog_cli.py:262
`backlog_said.terms` prints `args.term`, each passed through `one_line`. In a modelled context, `backlog_model.add` keeps the entry it normalised, so what was printed may differ from what the item holds. drafting#r103 says the service returns "the term". Today's inputs are already in normal form, so the tests do not show a difference. Printing the entries `backlog_model.add` kept would make it exact.

### f5 Minor drop: `__import__("backlog_said")` inline in two modules
- item: -
- where: scripts/backlog_cli.py:502
`backlog_cli.py:502` and `:511`, and `backlog_model_edit.py:551`, import the new module with `__import__` in the middle of an expression. A plain import does the same and is easier to read. This is polish, and no rule asks for it.
