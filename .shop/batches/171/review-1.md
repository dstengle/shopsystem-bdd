---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-171/review-1
kind: review
batch: batch-171
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/193
head: a9fb5575a42a3f6a8e6aff0f796abc59fa2eaea6
range: 3770f1dd73a016ba11ea1b4909d089b5f0a7b043..a9fb5575a42a3f6a8e6aff0f796abc59fa2eaea6
result: fix-now
---

# batch-171 review 1

## Verdict

The batch builds b859's chore. CLAUDE.md is down to its working rules, the size limit and a pointer. The map now lives at `docs/reference/modules.md`. The two map tests read the new page with their assertions unchanged. The agents, the brief, the driver and the skill each name the page. Every run exits 0. One finding to fix: several rows of the new page were cut mid-clause and lost part of their module's concern.

## Findings

### f1 Important fix now: module map rows cut mid-clause, losing part of their module's concern
- item: b859
- where: docs/reference/modules.md:21
The item asks for each row to be "cut to the module's concern": item numbers, requirement ids and history out. Several rows were instead truncated where they stood, so each now ends in a dangling fragment and leaves out concerns the module still holds. Nothing else in the map names those concerns, and the map is binding on whoever places or reviews a module.
- Line 21, `grammar/`: ends at "`language.md`". It no longer names `packs/` (the plugin's term packs base, cli, time, spec), `corpus/`, `rules.md`, `constructs.md`, the step grammar `Steps4`/`Steps4Eng` or the time grammar `Time`/`TimeEng`. No other row of the page names `grammar/packs/` as a module of its own; only spec_packs' row mentions it as a path it reads.
- Line 18, `scripts/features_generate4.py`: ends `; a group of only "may"`. The rest of that rule is gone, and so is the `# entailed:` comment concern.
- Line 56, `scripts/spec_lf_member.py`: ends `and, on a response's object`.
- Line 80, `scripts/spec_entail.py`: ends `; each response`.
- Line 88, `scripts/spec_steps4_held.py`: ends `its K2s named by no step but`.
- Line 124, `scripts/contract_registry.py`: stops after `deposit(root, contract, version)`. It drops `retrieve`, `register`, `deregister` and `held`, and the adapter wiring through `$SHOPSYSTEM_CONTRACT_REGISTRY`.

The chore's check passes because it tests only length (rows under 700 characters), not whether a row reads to the end. Fix: go through the rows of `docs/reference/modules.md` against the rows removed from CLAUDE.md in 691b6164c. Rewrite each truncated row so it ends in a whole clause and keeps every concern the module holds, with item and requirement ids still left out.

### f2 Minor observation: the brief's Rules line names the module map only where the tree keeps the page
- item: -
- where: scripts/batch_brief.py:183
`_rules` now says "the repository's rules" and adds "its module map at …" only when `docs/reference/modules.md` exists. A consuming repository whose CLAUDE.md still holds its own module map gets a Rules line that no longer mentions a map. The pr-reviewer definition still tells the reviewer to check "module-map rows", so the map is still covered. This is wording, recorded for later.
