---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-93/review-1
kind: review
batch: batch-93
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/116
head: 8f21449e84ae30d0195c0aa430e98e6ffa0cae46
range: ceef9f54cdf0af2ec5173bbf082d9be6d6574393..8f21449e84ae30d0195c0aa430e98e6ffa0cae46
result: clean
---

# batch-93 review 1

## Verdict

The batch builds b540's four lines (checking#r84 to r87). The diff shows no tests removed or weakened and no hand-written scenarios, and every check exits 0. The change is within the size limit, and both new modules are rows in `CLAUDE.md`'s module map. There are two hardening observations and nothing to fix now.

## Findings

### f1 Minor observation: the adapter spec id's name is not checked against the folder that holds the spec
- item: b540
- where: scripts/model_adapter.py:197
`path` accepts any `<parent id>/adapter/<name>` id, whatever the folder is called. An adapter spec kept at `adapters/stock-inventory/` whose index says `id: <parent>/adapter/payments` passes as conforming to the adapter spec id form. The module docstring and the vocabulary entry both describe the spec as kept at `adapters/<name>/` with the id ending `/adapter/<name>`, which reads as one `<name>`. Decision 0123 names the folder `adapters/<port>-<provider>/`. No line names this case and no client writes such an id today, so it is recorded only. Hardening: match on `re.escape(root.name)` in place of `NAME` when a parent spec holds the root.

### f2 Minor observation: a provider's version is used as a glob pattern
- item: b540
- where: scripts/model_adapter.py:229
`uncontracted` puts the version from `providers:` (`\S+`) straight into a `root.glob` pattern. A version holding `*`, `?`, `[` or `..` matches other folders, or reaches outside `provider/`. For example, `...inventory@1.*` passes when only `1.1.0` is kept, so the check does not tell that version apart. No line names such a version; the version form `spec publish` enforces (r83) would exclude it. Hardening: when a version is given, check the version form and test `(root / kept / "contract.toml").is_file()`. Keep the glob only for a provider that names no version.
