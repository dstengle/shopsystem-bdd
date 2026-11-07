---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-19/review-1
kind: review
batch: batch-19
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/32
head: b0cb312fccfe2ca989ac8a9518d4e6c649ca9552
range: 53a6c4377a7c0f8e3021e7368db2cc2c3ae5cd22..b0cb312fccfe2ca989ac8a9518d4e6c649ca9552
result: clean
---

# batch-19 review 1

## Verdict

The batch builds b103's one line, feature-file-tools#r20. I found nothing to fix now and one minor observation.

## Findings

### f1 Minor observation: feature-file-tools' `withholding` condition is checked in design-model-check's handler file
- item: b103
- where: tests/scenarios/design_model_check_handlers_conditions.py:296
The CLAUDE.md module map says `tests/scenarios/<capability>_handlers*.py` holds the handlers of that capability's feature. `withholding` is a term of feature-file-tools, added by b103's term bullet. Its check (`WITHHOLDING` and `withholding()`) is in design-model-check's conditions module. The code lands there because the shared `GivenK_C "requirement"` handler lives in that file. A later change to feature-file-tools would not look for this check there. The fix: move `withholding()` into `tests/scenarios/feature_file_tools_handlers.py`, or a `feature_file_tools_handlers_*.py` file, and call it from the `requirement` handler, or register it there. It does not hold the merge.

I also checked a risk that turned out fine. The new `@handler("WhenRuns", "`features generate`")` at tests/scenarios/feature_file_tools_handlers.py:123 goes into the global registry. It therefore now runs g17 and g18 (feature-file-tools.feature:250 and :283) as well as g20. For a step with no names it calls `features generate` with the flags only. That is the same call world_run's fallback made, so those scenarios do not change.

The new code does build the line:
- `spec_steps.py:153-154` now words a negated recipient pair as `SDoesToNot`.
- `spec_typed_verbs.py:143-145` generates `e__SDoesToNot` with the line "s does not <verb> x to y".
- `features_vocab*.py` maps `SDoesToNot` to `ThenDoesToNot`.
- The `holds` check at `work_queue_handlers.py:356-358` makes "`features` writes `features/shelf.feature`" assert that the written feature has a "does not lend the book … to the reader" Then. That is what the item's notes ask for.

The changed migration-tools given blocks hold example data (the plugin version), not requirement lines. The size is within the limit, and every run exited 0 at both Head and base.
