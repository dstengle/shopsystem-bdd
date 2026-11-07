---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-17/review-1
kind: review
batch: batch-17
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/30
head: 52ffc67a1bfe3dbe05c49e5448f4ad72f4ff7edb
range: bbaee40320819376ae182cee9af3fb05e24b002b..52ffc67a1bfe3dbe05c49e5448f4ad72f4ff7edb
result: fix-now
---

# batch-17 review 1

## Verdict

The batch builds design-model-check#r67. One finding to fix: the relabelling breaks every glossary still written in plugin 2.x's categories, and the brief's own `features generate --check` run shows it as a crash at `Head:`. Two observations go with it.

## Findings

### f1 Important fix now: a glossary in plugin 2.x's categories now crashes `features generate` instead of being refused
- item: b83
- where: scripts/spec_lexicon.py:84
The new `_category` gives every entry written `(kind)`, `(actor)`, `(event)`, `(condition of …)` or `(resource, …)` an empty category. It no longer reads them as before. Every consuming repository's glossary is written that way at base, and no upgrade step comes with the change. The commit message says `relabel` is "for the message and for an upgrade step", but no `migrate_upgrade*` module was added.

The brief's `## Runs` shows what that does to `features generate`: exit 1 at Head, 0 at base. That run used the base checkout's `spec_lexicon` on the batch's relabelled glossary, the same mismatch a consumer gets the other way round (new reader, old labels). With no term in a category, StepsTyped has no funs, and the output ends in a traceback rather than a refusal:

```
spec_grammar.GrammarError: gf could not compile StepsTyped:
StepsTyped.gf:4:2:
   Syntax error:
        Unexpected token '}'.
```

So a consumer that upgrades the plugin gets a GF traceback from `features generate`, and a v_t4 on every term from `model check`. At base, both worked. That is a crash where a refusal belongs, and a regression of behaviour that worked before this batch. I checked `features_vocab_gf.py:12,23`: StepsTyped is built only from `lex.of("attribute")` and `lex.of("kind")`, which are both empty for such a glossary.

Fix, on b83's branch: either
- have `features generate` (and the grammar load) refuse a lexicon with v_t4 problems, naming the terms and the fix, the way an uncodified capability is refused naming `migrate upgrade`; or
- add the upgrade step that `relabel` was written for, through a line that asks for it.

### f2 Minor observation: vulture flags two unused `kwargs` in test files the change touched
- item: -
- where: tests/scripts/test_spec_grammar.py:274
`tools check --base` exits 1 at Head and 0 at base. Its output names `tests/scripts/test_spec_grammar.py:274` and `tests/scripts/test_spec_parse_cache.py:40` (`unused variable 'kwargs'`). The change did not write those lines: the patch touches only the glossary strings of these files, at lines 25-30 and 230-245, and 18-25. They are reported because `--base` limits the check to files the range touched. Renaming them `_kwargs` would clear it.

### f3 Minor observation: the change is over the size limit
- item: b83
- where: -
`## Size` gives 58 files, +785 -731, against a limit of 1000 changed lines. Almost all of it is b83 relabelling every glossary entry in the 30 capability files, `spec/index.md`, the test fixtures and the inline test glossaries. It is mechanical, one-for-one, and no assertion changed.
