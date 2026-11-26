---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-162/review-1
kind: review
batch: batch-162
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/185
head: 0ae0db6ba70879b6edcae3f6e3202c567a512f55
range: f154d7f8955165c5ab15f3b70ebf4fa47a174634..0ae0db6ba70879b6edcae3f6e3202c567a512f55
result: clean
---

# batch-162 review 1

## Verdict

The batch builds both items, and I found nothing to fix.

b830 (laying#r48): `backlog_port.lay` now handles every area the item makes, not only driven ports. Each made area imports the areas whose words its lines say. Its model file is made only when it needs an import. Each other area of the item whose lines say its words imports it in turn. I checked the order the item's blocks come in (`plots` before `watering`, and the other way round). In both, `watering`'s model file is made and imports `plots`, so the `keep the area that imports the plots area` response holds.

`unlay` undoes this. The item's model lines and words come out first, so a made area's layer no longer has any words to match. The new third loop covers that case: it takes a removed area out of the imports of the areas left, and an import the base held is still kept (`_unimport`'s `before`). `tests/scripts/test_backlog_port.py` covers the lay and the unlay. The generated g48 scenario's handler (`tests/scenarios/laying_handlers_areas.py`) checks the changed paths of the lay's reply and the imports in `watering`'s model file. The module-map rows for `scripts/backlog_port.py` and the new handler are in `CLAUDE.md`.

b831 (chore): only the three files the chore names change. `spec --help` no longer says "design model v5" or "v_t4-v_t10". The new range, v_t4-v_t17, matches what `cmd_lexicon --check` reports (spec_lexicon's problems and spec_packs' v_t16 and v_t17). `spec job`'s options now show `<actor>`, `<text>` and `<job>`, as `docs/reference/commands.md` writes them. The item's note asked for `<statement>`, but the docs use `<text>` and the code follows the docs.

All runs exit 0 at `Head:` and at the base. No test was removed or weakened. `features/laying.feature` changed only as `features generate --check` confirms. The change is 312 lines, under the limit of 1000. No file goes over 300 lines, and no judgement decision is contradicted.

## Findings

None.
