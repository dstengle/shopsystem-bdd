---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-146/review-1
kind: review
batch: batch-146
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/169
head: bc8e79b055028c82eb988b94216620c861954ef0
range: 7aae176ef3090afe79a9c316f10508027a3dc610..bc8e79b055028c82eb988b94216620c861954ef0
result: clean
---

# batch-146 review 1

## Verdict

The batch builds all four lines: drafting#r88 (b759), checking#r147 (b744), and drafting#r89 and r90 (b760). Every run exits 0 at Head, the change is 632 lines against a limit of 1000, and the module map has a row for each new module. I found nothing to fix now; there are two hardening observations.

## Findings

### f1 Minor observation: reinstating an id that one of the item's own lines retires leaves that line's `retires:` pair behind
- item: b760
- where: scripts/backlog_reword.py:533
`_unretiring` takes the id out of `retired:` in every case. It drops a `retires:` pair only when the pair's line is not one of the item's lines (`p[1] != rid or p[0] in lines`). Take a block holding `- [r5] ...` with `retired: [r1, r2]` and `retires: [r5 r1]`. Running `work line <item> --remove work-queue#r1` leaves `retired: [r2]` but still writes `retires: [r5 r1]`, so the block pairs a line with an id it no longer retires. The parser does not check that a pair's id is in `retired:` (scripts/backlog_section.py:210-214), so nothing refuses this. If `retired:` ends up empty, the renderer drops the `retires:` line without saying so (scripts/backlog_section_render.py:37-38), and line r5 stays in the item with no record that it once replaced r1. drafting#r90 is still met: the item no longer retires the id. No scenario reaches this case, because r89 and r90 only use `--no-line` retirements. Hardening: either refuse an id that one of the item's lines retires and name that line, or drop the pair with the id.

### f2 Minor observation: imports resolved through a search path other than the importer's folder or the root are not read
- item: b744
- where: scripts/spec_coupling_imports.py:715
`imported` tries two places for a bare or dotted name: the importer's folder, then the repository root. In this repository, `tests/scenarios/*.py` and `tests/scripts/*.py` import modules of `scripts/` by bare name through `sys.path`. Two examples are `import spec_coupling_imports` in tests/scripts/test_spec_coupling.py and the `shop_*_world` modules. None of these resolve, so `spec coupling` reports no coupling between a test area and a scripts area, even when `.shop/modules.toml` places them in different areas. checking#r147 is still met for the case it names, a file importing another tracked file it can resolve. Hardening: an optional `paths` list in `.shop/modules.toml`, for example `["scripts"]`, searched after the importer's folder.
