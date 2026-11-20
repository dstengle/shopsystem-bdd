---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-56/review-1
kind: review
batch: batch-56
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/80
head: e555f4dc769ebe288a33ecff21b78f00bc1beacf
range: f37284ce0f219704a0b11fd2a8def022c8eb2a99..e555f4dc769ebe288a33ecff21b78f00bc1beacf
result: fix-now
---

# batch-56 review 1

## Verdict

The batch builds the lines of b420 and b418, and b429's chore. Three findings are `fix now`. b418 made the `tools check` run fail. b420 loosened a test's timing assertion. b420 also added a `spec check` behaviour that no line asks for. The change is over the size limit.

## Findings

### f1 Important fix now: `tools check` exits 1 at Head and 0 at the base
- item: b418
- where: scripts/spec_steps4_request.py:13
The `## Runs` block shows `python3 scripts/tools check --base f37284ce0` at `Exit code: 1 (base: 0)`:
```
scripts/spec_steps4_request.py:13:1: I001 [*] Import block is un-sorted or un-formatted
tests/scripts/docs_gherkin.py:28:12: BLE001 Do not catch blind exception: `Exception`
tests/scripts/docs_gherkin.py:53:12: PIE810 Call `startswith` once with a `tuple`
```
b418's commit 9b5536311 caused all three. It added `import spec_steps4_boxes` between `spec_rgl` and `spec_rgl_ops`, which leaves the import block unsorted. It also touched tests/scripts/docs_gherkin.py by adding `fresh`, and that put the file's two existing findings into the check's changed set.

This matters because the repository's own review check now fails on the batch. Fix: sort the imports (`ruff --fix` handles I001). In docs_gherkin.py, fix lines 28 and 53: catch the exceptions the step reader actually raises, and pass `startswith` a tuple.

### f2 Important fix now: the timing assertion of `features generate --check` on the live repo was loosened from 5 s to 10 s
- item: b420
- where: tests/scripts/test_features_generate.py:240
b420's commit 119621282 switched the measure from wall-clock time to the child process's CPU time, still under 5 s. Its commit 35f8d89ce then raised the limit from 5 s to 10 s:
```
-    assert took < 5, "features generate --check took %.1f s" % took
+    assert took < 10, "features generate --check took %.1f s" % took
```
That is a loosened assertion, which counts as a weakened test. The switch to CPU time was itself meant to keep parallel suite load out of the measurement, and the commit message says the command takes 2.8 s alone, the same as on the base. Doubling the limit on top of that lets a generation slowdown of up to 3.5x pass unnoticed.

Fix: put the 5 s limit back on CPU time. If 5 s of CPU time is really exceeded under load, find out why rather than raising the limit.

### f3 Minor fix now: `spec check` now resolves `quote-<n>` references, which no line asks for
- item: b420
- where: scripts/model_facts.py:273
Commit 119621282 makes a `quote-<n>` reference count as resolved when `.shop/quotes/<n>.md` exists. That changes `spec check`'s observable output: such a reference is no longer reported as unresolved.

No line of the batch asks for this. design-model-check's Implementation section (spec/capabilities/design-model-check.md:35-43) lists what `model` reads and how references resolve, and `.shop/quotes/` is not in it. The commit message says the change exists so that decisions 0110 and 0111, which cite quotes, name something.

Fix: take the change and its test (`test_a_decision_may_cite_a_kept_quote`) out of b420 and give it an item of its own (`work idea`), with a line, or a change to design-model-check's Implementation section, that says a decision's `source:` may cite a kept quote. If 0110 and 0111 need it before that item is built, say so on the item.

### f4 Minor observation: the change is over the size limit
- item: -
- where: -
`## Size` gives 72 files, +1782 -413 (2195 changed lines) against a limit of 1000. Most of it comes from b418 (param-of through grammar, logical form, check.lp, steps, worlds and docs) and b420 (spec_one_thing, the meaning path, the rewritten examples in language.md, and the frames world).

### f5 Minor observation: the "one logical form" Then now also accepts a parse without `--form`
- item: b420
- where: tests/scenarios/design_model_check_handlers.py:231
`model_prints` used to require exactly one `shall`/`may` form line. It now counts `forms or trees`, so output with no form lines but one tree line also passes. It also now requires exit 0, which is stricter.

For parsing#r2, where the When says "with the logical form", output that lost its form lines but still printed a tree would now pass this Then. Today no command prints a tree under `--form` without the form, so this is hardening only. Keying the tree branch on the When having no `--form` would close the gap.
