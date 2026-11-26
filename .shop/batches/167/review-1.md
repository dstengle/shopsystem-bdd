---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-167/review-1
kind: review
batch: batch-167
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/190
head: 549fa8e00001027b849ad92cb81354361c0cc1ec
range: d5396bebd3e389925a61443e320ab6d90677fbf6..549fa8e00001027b849ad92cb81354361c0cc1ec
result: fix-now
---

# batch-167 review 1

## Verdict

The batch builds b846: each fix its notes list is on the page, every changed path is one the chore names, and the runs at `Head:` all exit 0. The design-model.md row was already right on the base, so the batch did not need to touch that file. One finding to fix: a pasted output has the wrong capital letter.

## Findings

### f1 Minor fix now: step 3's probe line is not what the tool prints
- item: b846
- where: docs/getting-started.md:76
The item asks that the docs say what the commands print. The page's header says the outputs of step 3 are from runs of plugin 0.44.0. The new line is pasted as:

```text
No Python file: the analysis tools are not probed or installed; agents search by text, and say so
```

But `scripts/tools_env.py:54` (`NONE_OF_ITS_OWN`), which both `cmd_probe` (line 107) and `install_analysis` (line 127) print, starts with a lower-case "no":

```text
no Python file: the analysis tools are not probed or installed; agents search by text, and say so
```

The docs test checks no `text` block against the tool, so nothing catches this. A reader matching the output word for word sees a difference. Fix: write the line with "no".

### f2 Minor observation: the recipe's parsed form comes from a copy no test reads
- item: b846
- where: docs/recipes.md:136
The `markdown` entry and the `text` logical form under "A word a pack already has" rest on an operation `notes.return`. `docs/examples/notes-cli` does not declare that operation; the page's header comment says the output came from a copy that was given it. The docs tests read the block in `docs/examples/notes-cli` and cannot check the parse it shows. If grammar 4's reading of `Redefines: request` verbs changes, the shown form can go stale without any test failing. Hardening: keep the copy as a sketch context under `tests/scripts/fixtures/` (as `docs-labels/` is) and point the `<!-- docs: context -->` comment at it.
