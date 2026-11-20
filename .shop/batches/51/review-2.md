---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-51/review-2
kind: review
batch: batch-51
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/75
head: c87c488b3efcd275c97ca0ca18a5500a75619e34
range: 3468f6c8c3a4f79fcc044c1466ce586aafbcdc07..c87c488b3efcd275c97ca0ca18a5500a75619e34
result: clean
---

# batch-51 review 2

## Verdict

Both earlier findings are fixed. f1: in an index that still has the old `| capability | narrator | group |` tables, a new capability is now written in the index form, with one area table and the Retired subsections kept. The unlay puts the index back byte for byte, and two new tests cover this, one shaped like this repository's index. f2: the batch brief and building-a-batch now point to step 6 of the plugin's own `docs/getting-started.md`. The fix raises three observations and nothing to fix now. Every run exits 0 at `Head:`, and the change is well under the size limit.

## Findings

### f9 Minor observation: the conversion lists a capability named in a Retired table as part of its area
- item: b391
- where: scripts/backlog_capability.py:46
- `_converted` collects every backticked first cell from every table in the section, the `### Retired in ...` tables included. It decides a capability's area from its file's `area:` alone, and then also keeps the Retired subsection word for word:

```
names = re.findall(r"(?m)^\|[ \t]*`([^`|]+)`[ \t]*\|", body) + [block.capability]
```

So a retired capability whose file says `area:` ends up both in its area's row and in the Retired list.

What I checked:
- In this repository, `spec/capabilities/parsing.md` says `area: specification`, but `spec/index.md` lists `parsing` only under "Retired in 0.31.0". Laying a new capability here would add `parsing` to the specification row and also keep it under Retired.
- `migrate_upgrade_domain.plan` gives `area: <context>` to every file under `spec/capabilities/`, retired ones included (scripts/migrate_upgrade_domain.py:104-105). In an upgraded consumer that keeps a Retired table, every retired capability would therefore be listed as part of the area.
- The reverse case: a capability in an area table whose file has no `area:` is left out of the new index. The code ignores its `### <area> (<kind>)` heading.

Neither test has a retired capability with `area:`. Hardening: read capability names only from the `### <area> (<kind>)` subsections, and fall back to that heading's area when the file has no `area:`.

### f10 Minor observation: every unlay of a new capability reads the whole git history of spec/index.md
- item: b391
- where: scripts/backlog_capability.py:110
- `_without` calls `_held` before it does anything else, even when the index was already in the index form and nothing was converted. `_held` runs one `git show` for every commit that touched `spec/index.md`, then runs `_converted` on each old-table version it finds; each run reads every capability file it names. Unlay runs on `work batch park`, on `work batch done`'s tested tree and on `work batch review`, so the cost grows with the history of the index. Hardening: call `_held` only when the old tables at the base, or in the lay's own commit, could have produced the current section, for example by checking only the most recent version of `index.md` that has old tables.

### f11 Minor observation: the module map's row for backlog_capability does not mention converting old tables
- item: b391
- where: CLAUDE.md:276
- The `scripts/backlog_capability.py` row still says only "the table made in an empty section". It does not say that old `| capability | narrator | group |` tables are rewritten in the index form, or that the unlay puts back the old section as git held it. The module docstring says both. The row should be brought in line with the docstring.

## Earlier findings
- f1: fixed
- f2: fixed
