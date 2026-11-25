---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-97/review-1
kind: review
batch: batch-97
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/120
head: f41bfc8ceb1f0618ea01f6135a56f64d03a0fcde
range: 8e1969a6779eaa3ff992bbf5f93daf100c8936ce..f41bfc8ceb1f0618ea01f6135a56f64d03a0fcde
result: clean
---

# batch-97 review 1

## Verdict

The batch builds all four items. b575's dispatcher meets its chore. b599 keeps the pinned version for r100. b606 writes the Composition in the index form on every lay and unlay, so r113 to r115 are met. b610's v_m9 fails the check and names the transition for r101. All runs exit 0, as they did at the base. The size is 959 changed lines, under the limit of 1000. No test was removed or weakened, and no `.feature` file was written by hand. I found nothing to fix now; there are three observations.

## Findings

### f1 Minor observation: a pin overrides an explicit `--version` without saying so
- item: b599
- where: scripts/contract_obtain.py:162
`wanted = pin or version` makes an adapter spec's pin win over the version the person asked for. Reproduction: an adapter spec has `providers: [<id>@1.2.0]` and the person runs `spec obtain <id> --version 1.3.0`. The run keeps `.../1.2.0/contract.toml` and prints only `obtained <path>`, with no word that the version asked for was not used. r100 only covers a run with no version, so this does not break the line. Hardening would be to name the pin in the output, or to refuse when the asked version and the pin differ.

### f2 Minor observation: one adapter spec's missing pinned version refuses the whole obtain
- item: b599
- where: scripts/contract_obtain.py:160
Every holder's contract is fetched before anything is written. When one adapter spec pins a version the upstream does not keep, `published` raises `_none`, and the other adapter specs of the same provider get nothing either. I read `published` (scripts/contract_obtain.py:87-113): a pinned version goes through the `if version:` path and is refused as "has no contract at the version". No line names this case, so it is an edge for later.

### f3 Minor observation: rows of the old capability tables are read as area rows
- item: b606
- where: scripts/spec_composition.py:618
`_given` treats every three-cell row as `| area | kind | capabilities |`. That includes the old `| capability | narrator | group |` tables and their rows. So `kinds` gets entries such as `capability` → `narrator`, and `order` picks up words such as `group`. In this repository it does no harm: the capability cells are backticked, and every `spec/model/<area>.md` has a `kind:` that takes precedence. It goes wrong in a consumer whose old table has an unbackticked capability named like its area, with no model file. There, a row `| upgrades | the person | service |` would make `the person` that area's kind. Fix by reading a row as an area row only under the index form's header.
