---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-4/review-1
kind: review
batch: batch-4
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/19
head: 307e9663bdbd8994f79b177c06447a47b3aed84c
range: 26cbc9b0e078b92c68803a91fff5eaaeec0f82f8..307e9663bdbd8994f79b177c06447a47b3aed84c
result: clean
---

# batch-4 review 1

## Verdict

The batch builds all seven of b43's lines (readiness#r5-r11). The `--relation`, `--universal`, `--upstream` and `--given` flags each write their piece and commit the item. A malformed relation row, upstream entry or given block is refused before anything is written, and the error names the piece. All runs exit 0 at the head and at the base, no test is removed or weakened, the size is under the limit, and the module map has a row for each new module. I found nothing to fix now; five observations follow.

## Findings

### f1 Minor observation: refusals and a bar reason that no line or Implementation section names
- item: b43
- where: scripts/backlog_forms.py:354
No line or Implementation section asks for several things the change does:
- `work line --upstream` refuses an upstream already in `spec/index.md` or already on the item (line 354).
- `--given` refuses a group that is not one of the item's own groups, and a group that already has a given block (lines 298-302).
- `--universal` refuses a statement that starts with `#` (line 325).
- `work ready` now parses the item's universal conditions and gives `universal.md` problems as reasons (`scripts/readiness_bar.py:103`, `_parses`).

The item's Notes explain each of these. But readiness's `## Implementation, may change` still describes only "term bullets first, then groups", so the spec does not show this behaviour. Fix, cheap: add a bullet to that section covering the `### universal` and `### index` blocks, the relation rows and given blocks, and these refusals.

### f2 Minor observation: unlay leaves behind a `spec/universal.md` that lay created
- item: b43
- where: scripts/backlog_forms.py:399
When `spec/universal.md` does not exist, `_universal_file` writes a scaffold of it, and `lay_spec` lays the item's conditions into it. `unlay_spec` (line 421) only removes the condition lines, so the scaffold file stays. It is also added to `files`, so `unlay_lines` in `work batch review` commits it when a parked item's lines are taken out. The base then gets an empty universal file it never had. `test_lay_and_unlay_carry_every_piece` only checks that `conditions == []`, not that the file is gone. Reproduction: run that test against a spec with no `universal.md` and look at `into/spec/universal.md` after `unlay`.

### f3 Minor observation: two items of one batch can lay the same upstream entry twice
- item: b43
- where: scripts/backlog_forms.py:352
The duplicate check in `add_upstream` only reads `spec/index.md` and the item's own entries. `renumber` and `batch_pick`'s `others` never compare upstream ids across picked items. If two ready items both name `bounded-context/x/y`, `lay_lines` writes the bullet twice under `## Upstreams` and the bar does not object. No client does this today.

### f4 Minor observation: blank lines in a given block's text are dropped
- item: b43
- where: scripts/backlog_forms.py:241
`given_block` drops every blank line (`if x.strip()`), and so does the item reader inside the fence (`scripts/backlog_section.py:749`). A docstring given block with a blank line between paragraphs loses that line without any warning. This is data the person wrote, but it is an edge case that no line names.

### f5 Minor observation: `--group` and `--in` are ignored without a word for the four new flags
- item: b43
- where: scripts/backlog_cli.py:140
`cmd_line` accepts `--group`/`--in` together with `--relation`, `--given`, `--universal` or `--upstream`, and discards them. A person who writes `--in g4 --given ...` expecting the group to come from `--in` gets no error. Fix, cheap: refuse `--group` or `--in` unless a requirement line is given.
