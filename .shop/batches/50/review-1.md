---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-50/review-1
kind: review
batch: batch-50
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/74
head: 632de961b04e74d2e340b04bb4aa58201292409f
range: 9b94281ab9900aef95f2428b91f70a69612b0425..632de961b04e74d2e340b04bb4aa58201292409f
result: fix-now
---

# batch-50 review 1

## Verdict

The batch builds b370's seven lines and b371's chore. One check that passed at the base now fails at Head and has to be fixed. The rest are hardening observations, plus the size.

## Findings

### f1 Minor fix now: `tools check` fails at Head and passed at the base
- item: b370
- where: tests/scripts/test_model_catalogue.py:10
`python3 scripts/tools check --base 9b94281ab` exits 1 at Head and exited 0 at the base. Both lines it prints come from b370's change:

```
tests/scripts/test_model_catalogue.py:10:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
scripts/model_rules.py:130: unused variable 'check' (100% confidence)
```

The `noqa` is in the new test file. The vulture line is about the `check=False` parameter of `catalogue(root, write=False, check=False)`. That parameter is older than the batch, but b370 edited `scripts/model_rules.py`, so the check now covers the file. Fix: remove the `# noqa: E402`. For `check`, either drop the parameter (`--check` is already the "not write" path) and update its callers, or use it. Then `tools check --base` exits 0.

### f2 Minor observation: `spec check` on this repository fails v_c4 until b370 is delivered
- item: b370
- where: grammar/catalogue-entries.toml:336
The `[rules.v_c1]` to `[rules.v_c4]` tables say `since = "b370"`, and `grammar/rules.md` writes that as `- Since: b370` on those four entries. On the batch branch, `.shop/backlog/b370.md` says `status: ready`, and on main it is `in-batch` until `work batch merged` runs. While b370 is not `delivered`, v_c4 fires on all four entries. So `spec check` fails on this branch, and on main between the merge and `work batch merged`. Every later batch that adds a rule or adds its item to `Changed:` will fail its own branch's `spec check` the same way. This is what checking#r57 says should happen, and no run in `## Runs` executes `spec check` on the repository, so this does not hold the merge. It is worth a decision on whether a branch's own in-batch item should count, for example by treating `in-batch` as passing on the batch's own branch.

### f3 Minor observation: v_c1 checks nothing in a context with no `grammar/rules.md`
- item: b370
- where: scripts/model_catalogue.py:227
`read_catalogues` returns early when the context's root keeps neither catalogue. `cites_rule` and `rule_catalogue` are only written when `grammar/rules.md` is under the context's own root, not the plugin's. So a consumer that imports the spec pack and writes "While a file violates `v_zz9`, ..." gets no v_c1, although its rule `v_zz9` has no catalogue entry (checking#r54). The module's docstring states this choice ("A context that keeps no catalogue has no fact of it"). Reproduction: the r54 world in `tests/scenarios/design_model_check_worlds_catalogue.py`, without the `H.write(... "grammar/rules.md", ...)`, passes the check.

### f4 Minor observation: an entry naming an item the backlog does not have passes v_c3 and v_c4
- item: b370
- where: scripts/model.lp:4149
`v_c4(E, I) :- entry_item(E, I), item_status(I, S), S != "delivered".` needs an `item_status` fact. An entry whose `Since:` names `b99999`, which has no `.shop/backlog/` file, gets `entry_item`, so v_c3 passes, and gets no `item_status`, so v_c4 passes too. A mistyped item number is never caught. Hardening: also fail an `entry_item` whose owner is this context and that has no `item_status`.

### f5 Minor observation: the change is over the size limit
- item: -
- where: -
40 files, +2259 −814, against a limit of 1000 changed lines. Most of it is b370:
- generated or data files: `grammar/catalogue-entries.toml` (about 840 lines), `grammar/rules.md` (about 1100), `grammar/constructs.md` (about 670) and the corpus blocks;
- the 22 retired checking scenarios.

b371's docs are about 590 lines.
