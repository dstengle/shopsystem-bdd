---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-17/review-2
kind: review
batch: batch-17
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/30
head: f9ea1885fad3533530f77b39ba67b541a9cb40ef
range: 52ffc67a1bfe3dbe05c49e5448f4ad72f4ff7edb..f9ea1885fad3533530f77b39ba67b541a9cb40ef
result: clean
---

# batch-17 review 2

## Verdict

The fix for f1 works: `features generate` and the grammar load now refuse a glossary in plugin 2.x's categories, naming each term and the label it should carry, and a test covers it. Three observations remain, none of them a fix.

## Findings

### f4 Minor observation: `work ready` and `work batch start` still crash on an old-labelled glossary, now with an uncaught `Unlabelled`
- item: b83
- where: scripts/readiness_bar.py:49
The risk was that `spec_grammar.sources` raising `Unlabelled` reaches a caller that does not catch it. I grepped the callers. `features` (scripts/features:110) catches it, and `model_spec.py:90,109`, `model_report.py:78`, `request_lines.py:29` and `spec_context.py:59` catch `GrammarError`, which `Unlabelled` subclasses. Two callers catch neither, and nothing in `scripts/work`, `backlog_*.py`, `batch_*.py` or `shop_files.py` catches them higher up:
- `readiness_bar._parses` calls `spec_grammar.parse` (line 49), and `_scenarios` catches only `GenerateError` (line 101).
- `batch_start.py:58-59` catches only `GenerateError`.

So in a consumer whose glossary still says `(kind)`/`(actor)`, `work ready` and `work batch start` end in a traceback, not a refusal. Before this fix they ended in GF's traceback, so the fix does not make this worse. Hardening: catch `spec_grammar.Unlabelled` (or `GrammarError`) where `_parses`/`_scenarios` are called and in `batch_start`, and give back its text as a reason or a `Refused`.

### f5 Minor observation: the `features generate --check` run's traceback comes from the base checkout's scripts, not from the fix
- item: -
- where: -
`## Runs` ran `/home/vscode/shopsystem-bdd/scripts/features`, the base's script, against the batch's relabelled spec. The traceback's `cmd_generate` frame is at line 107, where the base has the dict comprehension; at Head it is line 108, and the `except` at Head's line 110 catches `Unlabelled`. The test the fix adds (`test_a_glossary_in_plugin_2_categories_is_refused_naming_each_term_and_its_label`) checks the Head behaviour: exit 1, no traceback, each term named. Once the batch merges, the base's scripts and spec agree. This is not a fault in the change.

### f6 Minor observation: vulture names two unused `kwargs` in test files
- item: -
- where: tests/scripts/test_spec_grammar.py:274
`tools check` exits 1 at Head and 0 at the base. Vulture reports:

```
tests/scripts/test_spec_grammar.py:274: unused variable 'kwargs' (100% confidence)
tests/scripts/test_spec_parse_cache.py:40: unused variable 'kwargs' (100% confidence)
```

Neither file is in this re-review's range, so it is an observation here. Fix: rename the variables to `_kwargs`, or use them.

## Earlier findings
- f1: fixed
