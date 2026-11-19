---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-19-release-0-38-0-the-domain-contract
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-19
---

# Release 0.38.0: the domain contract

Released under directive-1 ("You can merge when you need to. Do releases when you need to.") and directive-8 ("get this refactoring done and released ...").

- Branch `domain-contract` (design `.shop/records/2026-11-19-domain-contract/design.md`, plans 1-7), check loop clean at 62f55805f, opened as PR #71 (https://github.com/dstengle/shopsystem-bdd/pull/71) and merged with a merge commit, 3ee553be0aa54339bae1160f6f1e66b0b76acdf9.
- On main after the merge: `.claude-plugin/plugin.json` and `.shop/plugin-version` say 0.38.0; CHANGELOG.md's newest section is `## 0.38.0: the domain contract`.
- Annotated tag `v0.38.0` ("Release 0.38.0") on the merge commit, pushed; GitHub release https://github.com/dstengle/shopsystem-bdd/releases/tag/v0.38.0 with the CHANGELOG section as its notes (the first release published on GitHub; earlier versions are tags only).
- Why 0.38.0 (design-decision 0092): every line in 0.37's words is refused, the `--json` shapes changed, `model` became `spec`; the upgrade step 0.38.0 "the domain contract" ships with it.
- Deferred: b356 (the old run/option reading deleted), b358 (handlers keyed on the operations through driver_cli). Ideas filed on the branch: b354, b355, b357, b359-b363.
- Known on release: `spec check` exits 1 with 0 violations, from 2 file problems in the variant files under `.shop/records/2026-11-18-cli-as-port/`.
