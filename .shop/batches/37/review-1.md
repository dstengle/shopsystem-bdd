---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-37/review-1
kind: review
batch: batch-37
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/57
head: 3676860aa87458b2844f9e5a1d50862abbefa682
range: 06cced53f26062e0f7f62c8e09ceed9fab00313d..3676860aa87458b2844f9e5a1d50862abbefa682
result: clean
---

# batch-37 review 1

## Verdict

The batch builds all three lines of b284: r81, r82 and r83 replace r77, r78 and r79, which are retired. Their scenarios now set the repository's release and `migrate`'s release apart, each with a value of its own. There is nothing to fix now. The failed `features generate --check` run comes from how the check was run, not from the batch.

## Findings

### f1 Minor observation: `features generate --check` ran the base checkout's scripts against the batch's tree
- item: b284
- where: features/migration-tools.feature:936
`## Runs` shows `python3 /home/vscode/shopsystem-bdd/scripts/features generate --check` exiting 1 at the head and 0 at the base, with this output:

```
differs: features/migration-tools.feature
```

The risk I checked was that the feature file had been written by hand. The command runs the main checkout's `scripts/features`, and that script puts its own folder first on `sys.path` (`sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))`, line 8). So it uses main's `spec_lf_compare` and `spec_lf_order`, without commit ad75c766b's `pool` and `own`.

Main's generator picks one shared value for both senses of `release`. That gives what commit 111ac5923 wrote: "the release of `migrate` is `0.23.1`" for g81 and `0.25.0` for g83. The batch's generator keeps each sense to its own entry's values. The tool's sense lists only `0.34.1`, so it writes `0.34.1` for g81 and g83, and `0.23.1` over `0.23.0` for g82, which is what the head's feature holds. ad75c766b's message says the same: `0.23.1` is a value of the repository's sense, so it is no code of the tool's, and that Given does not parse.

In the same brief, `model decisions --check` reports `tests/scripts/test_decision_checks.py::test_the_features_are_what_features_generate_writes` as holding. That test runs `features generate --check` from the tree. So the committed feature is what the batch's own generator writes, and this check should pass once the batch is merged. If `[review] checks` ran the tree's own `scripts/features`, this false difference would not show up.

### f2 Minor observation: the scenarios' Given of the repository's release now writes the file it used to check
- item: b284
- where: tests/scenarios/migration_tools_handlers.py:80
Before, "the release of this repository is `v`" asserted that the given block's `.shop/plugin-version` held `v`. Now `recorded` writes that file with `v`. This is no weaker for r81, r82 or r83, whose given blocks no longer hold that file. But a scenario whose given block says one release and whose Given says another now passes silently, with the Given's release overwriting the block's. Today g80's block and Given both say `0.33.0`, and the old assertion held for every other scenario, so nothing in the feature disagrees. This is hardening only.
