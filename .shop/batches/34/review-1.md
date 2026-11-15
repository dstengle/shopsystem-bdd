---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-34/review-1
kind: review
batch: batch-34
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/54
head: 37ea867598a7cacca05bffd12f8e41e291c22c26
range: a02d28f54e19e003dbb359fba50e559a62f30fb2..37ea867598a7cacca05bffd12f8e41e291c22c26
result: fix-now
---

# batch-34 review 1

## Verdict

The batch builds the lines of b268, b272, b273 and b274. Three findings must be fixed now: two new `tools check` (ruff) failures, in b272's and b273's code, and a spec-corpus check that b268 loosened. Several of b273's counter-example Thens in this repository's own features are checked by nothing.

## Findings

### f1 Important fix now: `tools check` fails on b272's `unread` in spec_solve.py
- item: b272
- where: scripts/spec_solve.py:157
The `[review] checks` run of `tools check` exits 1 at Head and exited 0 at the base. Its output names this file:
```
scripts/spec_solve.py:157:47: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
scripts/spec_solve.py:159:66: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
scripts/spec_solve.py:161:36: RUF100 [*] Unused `noqa` directive (non-enabled: `E731`)
scripts/spec_solve.py:162:16: FURB188 [*] Prefer `str.removeprefix()` over conditionally replacing with slice.
```
Commit 7559980dc added these lines in `unread`. Fix: drop the three `# noqa: E731` comments (or write `keep` as one small `def`), and write `why.removeprefix("refused: ")`.

### f2 Important fix now: `tools check` fails on b273's feature_file_tools_collections.py
- item: b273
- where: tests/scenarios/feature_file_tools_collections.py:35
The same run reports seven `ISC004 Unparenthesized implicit string concatenation in collection` errors, at lines 35, 39, 41, 43, 45, 47 and 49. They are the two-part line strings inside the tuples of `LINES` (the "satisfy" and "boundary" entries), added by 98cc9cffc. Fix: put each concatenated string in parentheses.

### f3 Important fix now: test_corpus_spec's check 3 no longer needs a block for any `unbuilt:` id
- item: b268
- where: tests/scripts/test_corpus_spec.py:115
Commit 7be4b21c6 changes `faults` to `set(lines) - set(blocks) - unbuilt.get(stem, set())`, with no condition. Before, every live line of a codified-2 file needed a spec-corpus block. Now a capability can keep an id in `unbuilt:` with no block for as long as it likes, and check 3 still passes. That is a loosened assertion, and nothing at Head needs it: I read every capability's `unbuilt:` in the Tree and each is `[]`, and `grammar/corpus/spec/` has blocks for r111-r121 and r288-r295. The case it serves (a task's worktree holding the other items' unbuilt lines) is a `work batch done` situation. Fix: exempt unbuilt ids only in the tree that `$SHOPSYSTEM_UNBUILT_NONSTRICT` names, as `spec_unbuilt` already does for the xfail mark, and keep check 3 strict otherwise. Adjust `test_an_unbuilt_line_needs_no_block_yet_and_its_block_is_checked` to match.

### f4 Important observation: several of b273's counter-example Thens in this repository's features check nothing
- item: b273
- where: tests/scenarios/batch_measurement_handlers.py:150
The new counter-example steps that features generate writes into this repository's own features get handlers that cannot fail:
- `prints_not` does `continue` for "the stage row ..." and "the dispatch ...". This covers features/batch-measurement.feature:30, 53 and 83.
- migration_tools_handlers_thens.py:210 `continue`s for "the term t3". The new `rewrites_not` (line 213) only checks the exit.
- design_model_check_handlers.py:212 `unsaid` returns the placeholder `"<kind> <word>, none printed"` for a number past `PRINTED`. A `ThenPrintsNot` of it, such as features/design-model-check.feature:249 "`model` does not print the fact f3", is therefore always true.
- readiness_handlers_givens.py:58 names the bar check "a bar check no bar has". readiness_handlers_thens.py:113 then asserts that this made-up string is absent.

b273's purpose is scenarios that can fail. In these places the counter-example is written but never tested, so a command that prints the extra row would still pass. No line of the batch names these handlers, so this is not a fix-now finding. Each handler should make the counter-example's thing exist (a fifth row, an applied step, a term the given block holds) and assert that the output leaves it out.

### f5 Minor observation: a count's counter-example keeps only the first Then of its scope
- item: b273
- where: scripts/spec_steps4_counter.py:136
`upper` returns `[(True, tree) for _, tree in r.acts(box.scope.body)][:1]`. A response count whose scope says two acts ("print and write at most three files") would have its second act's Then silently dropped. Every line of the batch has one act there, so no feature is wrong today. Raising a TraceError when the scope has more than one act would be safer than cutting the list.

### f6 Minor observation: every Then is now order-independent, and the reorder changes consumers' features with no note
- item: b268
- where: tests/scenarios/vocab.py:271
`_deferring` catches every `Exception` from a Then and tries it again after each later Then and at the scenario's end. This applies to all scenarios, not only r111's. A Then can now pass only because a later Then's handler changed `step.context`.

The new Then order also breaks handlers that bound a name at a description. docs/getting-started.md had to rewrite `prints_title` and `has_title` because of it. A consumer whose handlers do the same will break after `features generate`. CHANGELOG.md is not in the change, and docs/upgrading.md only shows a reordered excerpt. A sentence in the changelog and in upgrading.md would cover it.

### f7 Minor observation: the `features generate --check` run used the base checkout's generator
- item: -
- where: -
The run is `python3 /home/vscode/shopsystem-bdd/scripts/features generate --check`, which uses the main checkout's scripts, not the Tree's. I checked: /home/vscode/shopsystem-bdd/scripts has `spec_steps4_boxes.py` and no `spec_steps4_counter.py` or `spec_steps4_held.py`. So the 13 `differs:` lines are the old generator compared with the batch's regenerated features, and they are no sign of a hand-written scenario. Every feature hunk I read is the reorder (r111) or a counter-example (b273). The check of record is `test_the_features_are_what_features_generate_writes`, which runs in the Tree. `[review] checks` should run each tool from the Tree's `scripts/`; the same applies to the `tools check` run, though its ruff findings are real.

### f8 Minor observation: the change is over the size limit
- item: -
- where: -
The change is 72 files, +2266 -257, against a limit of 1000 changed lines. Most of it is b273 (98cc9cffc: spec_steps4_counter.py, the collections tests, counter-examples written into 13 features with their handlers) and b268 (134456710: the Then reorder across every feature and the docs). b274's spec_lf_member.py and its worlds come next.
