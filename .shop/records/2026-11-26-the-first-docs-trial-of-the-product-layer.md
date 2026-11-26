---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-26-the-first-docs-trial-of-the-product-layer
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-26
---

# The first docs trial of the product layer

A fresh agent played a new user testing whether the documentation works, on a clean clone of main at 57af90f77 (plugin 0.44.0), right after b838 made the notes example a product and added "Your product and its jobs" to talking-with-claude.md. It read the docs in a new user's order, reproduced the product conversation of talking-with-claude.md on copies of `docs/examples/notes-cli/`, then followed getting-started.md and the shaping-items skill on a fresh "tool library" app (members borrow and return tools) through to `shop work batch start`, with no GitHub, reading only the README, docs, skills, `--help` and command output. It is the first docs iteration the person asked for (quote-106).

## Summary

- The notes example reproduces exactly: every product command, the 10-warning check, the five `--serves` pairs, the r5 line, the refusal when `--serves` comes before the line's text, and the traces with and without `--item` matched; the product file built was byte-identical to the example's. The only output difference is one extra `batch brief:` line after `shop work batch start`.
- The talking-with-claude walk-through goes from `shop work idea` to `shop work ready b1`, which is refused: the item must be shaped with a note first. It never says the example folder is the end state.
- The fresh project got stuck on the person's own word "return": a word of the request pack, `v_t6` blocks it even with `Redefines: request`; the docs describe `v_t6` wrongly, and `shop spec check --item` passes while `shop work ready` refuses. Got past only by renaming the verb ("brings back").
- The product's actor mapping is easy to lose: getting-started's product step never mentions `shop spec plays`, which is refused in a new context until the first batch merges, and nothing warns that a mapping is missing (`shop spec check --item b1`: 0 warnings, actor unmapped).
- Small: a broken anchor, a test module the page says the example holds, a wrong "first row", a wrong `specifies:` written by the batch, stale version notes.

## Reading

- README.md: clear; says you never run the tools yourself, and no page before commands.md says how you would.
- getting-started.md: its header says "The spec, feature and test module on this page are docs/examples/notes-cli/'s" but the example has no `tests/` and no `test_notes.py`; step 3 shows only the `grammar:` block, while `shop tools probe` in an empty folder also prints `no Python file: the analysis tools are not probed or installed; ...`; step 4 links "the vocabulary" to `concepts.md` with no anchor; step 8 does not mention `shop spec plays`, the shop id given to `--shop`, or that the mapping waits for the first merge; step 8 comes after the merge while the skill and talking-with-claude declare the product when the person says it; output notes dated 0.38.0.
- talking-with-claude.md: line 22 "Take the first row" means the third (`shop work show`); lines 72-76 call the example folder "the capability these steps end with" without saying how to replay from its start; lines 174-234 have no `shop work shape --note` between `idea` and `ready`; line 237's batch start output lacks the `batch brief:` line; `--shop example.org/notes/shop` never explained.
- tour.md and concepts.md "Product, job and trace": consistent.
- reference/commands.md: the `shop work line` synopsis lacks `--relied-on-by` and shows `--serves CAP#gN JOB` where `--help` says `--serves CAP#gN JOB [CAP#gN JOB ...]` (why a `--serves` before the text swallows it); no order warning there; header says 0.33.0 outputs.
- reference/design-model.md line 171: `v_t6` "two terms are written the same | Rename one of them"; the real message is "the grammar spells `return` itself".
- recipes.md 116-119: says `Redefines: request` gives a pack word your meaning; for "return" it does not.
- writing-requirements.md line 156: broken anchor `../grammar/language.md#r11-this-k-and-an-unbound-the-k-whose-entry-has-this-are-the-runs-own-k` (the heading now says "the request's own K").
- skills/shaping-items: followable; does not say `spec plays` waits for the first batch, nor what to do about a pack word such as "return".
- Every relative link and anchor of the README, docs/ (not history) and the skills checked: only the R11 anchor broken.

## Example reproduced

Two copies: `notes-copy` (literal) and `notes-start` (the start state the page implies: no `.shop/`, no `serves:` lines, no g5).

| command | result |
|---|---|
| `shop spec trace keep-notes` on the copy | matches |
| `spec product`, `actor`, `job` on the literal copy | print `declared ...`, no commit (held already) |
| the 11 declarations on the start state | every line matches; 11 commits; product file identical |
| `shop spec check` | matches: 10 warnings |
| `shop work idea ...`, `--serves notes#g1 keep-notes` ... `g4` | match |
| `--serves clear-notes` before the text | matches: `--serves: 'clear-notes' is not a requirement group <capability>#g<n>` |
| the line with `--serves` after its text; an unknown job | match |
| `shop spec trace keep-notes` before the batch; `spec check --item b1`; `spec trace clear-notes --item b1` | match |
| `shop work ready b1` | **differs**: page `b1 "..." ready`; got `work ready: b1 "..." is idea; work ready takes an item that is shaped or ready`; plain `work shape b1` refuses `has no shaping note; give it one with the --note option`; after `work shape b1 --note`, matches |
| an item of only `--serves` pairs readied | matches: `it has no requirement line` |
| `shop work batch start` | differs: adds `batch brief: .../brief.md` (as commands.md shows) |
| the batch's capability file; `spec --root docs/examples/notes-cli trace`/`check`/`lexicon --check`/`features generate --check`/`annotate --check` | match |

## Fresh project

1-3. Repository, venv, `tools install`/`probe`, `migrate init --id bounded-context/example.org/toollib/tool-library`: worked (`## Purpose` empty: getting-started never mentions `--purpose`). 4. `idea`, `shape --note` worked; `work quote` refused `no session is known ...` outside a live session. 5. `--capability lending --narrator "the member"` and `--model` worked. 6. the `--term` set warned `v_t6: spec/vocabulary/lending.md: the grammar spells `return` itself`; following recipes.md, `Redefines: request.` added with `--reword-term`, which printed no warning. 7. `spec parse --item b1 --form` read all three lines, the "return" line included; "a tool that is `lent`" refused, "whose status is `lent`" worked. 8. product, actor, two jobs (return-tools needs borrow-tools), subdomain, context, two assigns worked; `spec plays` refused as documented (`it holds no actor`). 9. lines with `--serves <job>` after the text worked. 10. `spec check` 4 warnings; `spec check --item b1` 0 warnings, no reminder of the unmapped actor; `spec trace return-tools` refused pointing at the item; with `--item b1` right, needed job included. 11. **`shop work ready b1` refused** `the lexicon: v_t6 return: spec/vocabulary/lending.md: the grammar spells `return` itself`; nothing documents the grammar's own words; renamed the verb to "bring" (`Frame: <actor> brings back <tool>.`), r3 reworded, ready passed, against the skill's rule to keep the person's word. 12. `shop work batch start` worked; the capability says `specifies: service lending` but the service is `library` (`spec check` passes); `work batch next batch-1` says `prepare task`.

## Findings

1. **major** talking-with-claude.md "What Claude does" (174) and "The outcome" (233-235): `work idea` then `work ready b1`, refused for an idea; plain `work shape b1` refused without `--note`. Fix: show `shop work shape b1 --note "..."` between them.
2. **major** "return" as an operation verb (recipes.md 116-119, design-model.md 171): `v_t6 "the grammar spells `return` itself"` survives `Redefines: request`; design-model.md describes `v_t6` as "two terms are written the same". Fix: document the grammar's own words and how to name such an operation, or make `Redefines:` work for it, and correct the row.
3. **major** `shop spec check --item b1` passed with the `v_t6` entry on the item while `shop work ready b1` refused it; talking-with-claude says `--item` "checks it the same way". Fix: `check --item` reports the item's vocabulary problems, or the docs say it doesn't.
4. **major** getting-started step 8 and the product check: `spec plays` refused in a new context until the first merge, not mentioned there, and no warning reports an unmapped product actor (0 warnings). Fix: a warning for a product actor of a held job with no mapping, and getting-started and the skill saying to run `plays` after the merge.
5. **minor** talking-with-claude 72-76: the example folder is the end state; a literal copy gives 0 warnings, not 10, and `spec product`/`actor`/`job` print `declared` committing nothing.
6. **minor** talking-with-claude 237: batch start output lacks `batch brief: .../brief.md`.
7. **minor** getting-started header claims the example's test module, which does not exist.
8. **minor** writing-requirements.md 156: broken R11 anchor.
9. **minor** `work batch start` wrote `specifies: service lending` for a capability whose service is `library`.
10. **minor** talking-with-claude 22: "first row" means the third.
11. **minor** commands.md `shop work line`: synopsis lacks `--relied-on-by`, shows `--serves` as one pair, no order note.
12. **minor** the `v_t6` warning shows on `--term` but not on `--reword-term`.
13. **info** getting-started step 8's `--shop <shop id>` never says what a shop id is.
14. **info** getting-started step 3's output omits probe's "no Python file" line.
15. **info** stale output notes: getting-started 0.38.0, commands.md and tour.md 0.33.0, plugin 0.44.0; the re-run outputs still matched otherwise.
16. **info** getting-started step 4's "the vocabulary" link has no anchor; `#vocabulary-and-packs` exists.
17. **info** `work quote` refused outside a live session; getting-started does not say it may fail.
