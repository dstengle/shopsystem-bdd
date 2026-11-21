---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-21-the-new-user-flow-missing-commands-and-time-outside-agent-time
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-21
---

# The new-user flow, missing commands and time outside agent time

Sources are four reports that skeptics re-checked. Their scratch work is under `/tmp/claude-1000/-home-vscode-shopsystem-bdd/d0999860-a5ec-42eb-b649-f0728fe0f332/scratchpad/wf-next/`, in `new-user-flow/`, `commands-skeptic/`, `skeptic-time/` and `contracts/`. All of it was measured on main at d23776a14 and 4599fe2af; no commit in between changes `scripts/`. I checked overlaps against the backlog with `python3 scripts/work names | grep -iE 'venv|pytest|gitignore|purpose|split|retitle|amend|parallel|brief|bindings|forms|contract|…'`, which found no item for any of the new items below.

## 1. The new-user flow

**Speed is fine for a small context.** A fresh context with one capability and five lines ran 59 commands in 11.14 s (`awk '{s+=$NF}' times.log`).
- `work ready b1` takes 0.49 s cold and 0.16 s warm, and leaves a 46 K cache.
- `spec check` and `spec logic` take 0.08 s warm.
- This says nothing about large repositories. There, b430 (in batch-58), b351 and b340 apply.

**What failed or misleads, ranked:**

1. **The tests run with a different Python than the docs set up.** This is a risk read from the code; I did not see it fail.
   - `TESTS = "python3 -m pytest -q -p work_items"` is at `scripts/batch_tasks.py:39`, and `migrate init` writes the same line, commented out, into `.shop/delivery.toml`.
   - The docs install pytest only in `.venv` (`docs/getting-started.md:61`, `skills/shaping-items/SKILL.md:27`).
   - `python3 -s -m pytest --version` prints `No module named pytest`. It only works on this machine because pytest is in the user site.
   - No item covers this; b406 is about the order of `tools install`.
2. **A second item on a capability still in a batch is sent the wrong way.**
   - With b1 in batch-1, `work line b2 --into notes "…"` exits 1 and suggests `--capability notes`.
   - Following the hint succeeds and commits 0b44d51, creating a second block for the same capability.
   - `work line b2 --remove notes` is then refused: `--remove takes <capability>#r<n>, not notes`.
   - b341 covers refusing the second block. New: the refusal should name b1 and batch-1, and `--remove <cap>` should take a block back out.
3. **`spec parse` cannot read an item's words.** It has no `--item` option (`usage: spec parse [-h] [--file FILE] [--form] [--json] [line]`). Not covered; b351 and b352 are about speed and output.
4. **`--term` takes one entry per call** (`work line --help`: `[--term TERM]`). Not covered.
5. **`spec forms` is out of date.** It says "b354 (no command yet)", but b354 is delivered; and it names b13, which is still an idea. Not covered; b342 is a different check.
6. **Files the user still edits by hand:**
   - `migrate init` writes an empty `## Purpose` (`migrate_init.py:30,46`) and no `.gitignore`. Not covered.
   - `cli.toml` is covered by b355, and `delivery.toml` by b44.
7. **Low priority:**
   - Plain `pytest` from a plugin checkout cannot find `work_items` (only without `CLAUDE_PLUGIN_ROOT`).
   - The doubled prefix in `work: work line: --remove takes …` is a cosmetic bug.

**Fixes, in order:** the tests interpreter, then `--remove <cap>` with the refusal that names the in-batch item, then `spec parse --item`, then repeatable `--term`, then `spec forms`, then `.gitignore` and `## Purpose`.

## 2. Missing commands

**Defects first:**

| # | Gap | Evidence | Proposed fix | Covered by |
|---|---|---|---|---|
| 0 | `work line --remove` of a new capability's last line drops the whole `### notes` block, including its narrator, group and purpose | `backlog_reword.py:61` never checks `block.new`; reproduced in `commands-skeptic/ctx/` | Add `block.new` to the test, or refuse and say how to drop the capability | none |
| 1 | `spec forms` gives stale writers, leaves forms out, `--check` exits 0, and the JSON has no `kind` | 37 `Form(` rows, no constructs, packs, corpus or `CLAUDE.md` (`model_forms.py:44,56-57`) | Point the two writers at b398, add the missing forms, put `kind` in the JSON | b342 is related, not the same |
| 1b | Docs gaps | `commands.md:116` has no `--model`; the dot required in the domain is not documented (`migrate_init.py:17`); `how-it-works.md:334` shows `bounded-context/ex/notes/notes-cli`, which `migrate init` would refuse | Fix the docs and say it in the refusal | none |

**Command gaps, ranked by the hand commits behind them.** There are 274 hand commits to `.shop/backlog/` since 2026-11-07. Ten of them are titled with a literal "b%d: the triage's evidence", from a hand script with a broken format string.

| Rank | Gap | Hits | Proposed command | Covered by |
|---|---|---|---|---|
| 1 | A note on an open item (59 on ideas, 63 shaped, 33 ready) | 148 | none needed | b281, b383 |
| 2 | A rating's reason | 73 | none needed (drop `work rate --why`) | b281, b383 |
| 3 | Lines on a ready or in-batch item | 38–59 | `work amend <item>` laid on `batch-<n>` | b431 covers ready; in-batch is not covered |
| 4 | A status corrected | 14 | none needed | b386 |
| 5 | An item merged, split or retitled | 22 | `work split`, `work retitle`; merge folds into b281 | merge: b281; split and retitle: none |
| 6 | A decision's `enforced_by` or `rests_on` amended | 10 of 12 hand decision commits | `work decision <id> --amend --enforced-by/--rests-on`, and `--retires` names the decisions that cite the retired id | none |
| 7 | Bulk retire | 19 (not re-run) | `--retires-all --from <file>` | none |
| 8 | Model or vocabulary taken out of an item | rare | none needed | b367 |
| 9 | `delivery.toml` settings | 4 | `spec settings set` | b44 (which has no lines) |
| 10 | Catalogue entries | 2–3 | `spec catalogue entry` | none |
| 11 | `--remove` and `--reword` of a universal condition, given block or upstream entry | 0 | low | b48 (which has no lines) |
| 12 | Rename across the spec | not counted | `work rename` | none |

Also: b44, b48 and b355 are `shaped` but hold no `[r` lines (`grep -c` gives 0). They need lines, or a move back to `idea`.

## 3. Time outside agent time

I left out `work ready`, which took 165 min over 7 days and is what b430 fixes. Totals come from `tooltimes2.py 7`; they are approximate, because it matches the pattern anywhere in a command, compound commands included.

| Rank | Cost | Evidence | Fix | Covered by |
|---|---|---|---|---|
| 1 | Cold grammar after a vocabulary change: `spec check` 31.2 s, `features generate --check` 9.2 s | `features generate`: 84 min over 472 calls in 7 days | Reuse compiled modules (b439); a narrow parse key (b447); `--optimize-pgf` (b438) | b439 (in batch-58), b447, b438. b351 duplicates b447: merge them. |
| 2 | The suite at `work batch done` (about 38 s a task) and at `review` (34 s) | 74 + 25 min | Run only the touched capabilities' `tests/scenarios/test_<cap>.py` and the `tests/scripts/` tests of changed modules. Not `tools tests-of`: its coverage map is stale (1 context, 10 files, 88d66baed). Split `test_bound` (7.5 s). | none (b73 only measures; b265 withdrawn) |
| 3 | `work batch brief`: five checks run one after another (`batch_brief.py:136`) | 19 min | Run the checks in parallel. `features bindings` parses each module once: 978 `ast.parse` calls and 3 `test_modules` calls (4.2 s), estimated down to about 2 s. The `spec decisions --check` fix is struck: it already runs 4 at a time (`model_decisions.py:20,153`). | none (b75 is something else) |
| 4 | Warm overhead of 1–2 s per `spec` or `features` command | `_context` and `_state` called 2056 times, 397k stats; `spec_language.parse` called 823 times for 413 lines | Probably b430 steps A–D in `spec_grammar4`, which every command shares; re-measure `spec check` after batch-58 merges | b430 (to be confirmed) |
| 5 | Cache growth: 501 grammar folders (1.3 GB), 107,650 parse files (432 MB) | 139 grammars in 24 h | Evict by age and size | b350 and b446 duplicate each other: withdraw one |

Negligible: hooks, backlog commands, `measure`, clingo (`model_check.solve` 0.09 s).

On main, `test_decision_checks.py` fails twice (`111 == 110`, `28 == 27`). Commit 3381bfa3f in batch-58 fixes it, so no item is needed.

**Order of work:**
1. Merge batch-58 (b430, b439) and re-measure warm `spec check`.
2. b447, after merging b351 into it.
3. Test selection at `work batch done` and `review`.
4. Parallel checks in the brief, and one parse per module in bindings.
5. b438.
6. Cache eviction (b350 or b446).

## Items to file

- work line --remove keeps a new capability's declaration | `backlog_reword.py:61` deletes the block when it has no groups, terms, relations, retired ids or language, but never checks `block.new` (narrator, group, purpose). Removing the last line of a capability new on the item drops the whole `### <cap>` block, and the next `--into` is refused (reproduced in `commands-skeptic/ctx/`). Count `block.new` as content, or refuse and name the command that drops the capability. | 4/4/XS
- The tests command runs the context's .venv interpreter | `TESTS = "python3 -m pytest …"` (`batch_tasks.py:39`), and the line `migrate init` writes, ignore the `.venv` the docs install pytest into. `python3 -s -m pytest` prints "No module named pytest", so `work batch done` and `review` fail on a clean machine. Use `.venv/bin/python` when `.venv` exists, and have `migrate init` write it. | 4/3/S
- work line --remove <cap> takes a capability block out, and the --into refusal names the in-batch item holding it | Extends b341 and b414. With b1 in batch-1, `work line b2 --into notes` suggests `--capability notes`, which makes a second block (0b44d51) that no command can remove. The refusal should name b1 and batch-1, and `--remove <cap>` should take out a block and its model block. | 3/3/S
- spec forms tells the truth: current writers, every form, kind in JSON | `model_forms.py:56-57` says b354 "(no command yet)" though b354 is delivered, and names b13 for vocabulary terms; b398 is the right item. The constructs catalogue, packs, corpus, catalogue-entries and `CLAUDE.md` are missing, `--check` exits 0, and `_asdict()` drops `kind`. Fix all four, with a test against the delivered statuses. | 3/3/S
- spec parse --item b<n> reads lines with an item's words laid | `spec parse`, `--form` and `spec explain` cannot read an item's new terms or model lines, so a session has to run `work ready` to find out why a line is refused. Lay the item on a copy, as the readiness bar does. | 3/2/S
- work line --term repeatable | `--term` takes one entry per call, so N entries cost N commits and N lays. Accept it more than once, or a block, in one commit. | 2/2/XS
- migrate init writes .gitignore and fills ## Purpose | `migrate_init.py:30,46` leave `## Purpose` empty and write no `.gitignore` (`.venv/`, caches). Add `--purpose "<text>"` and a `.gitignore`. | 2/2/XS
- Docs: the bounded context id's domain needs a dot, and work line shows --model | `migrate init --id bounded-context/example/notes` is refused (`FORM`, `migrate_init.py:17`), but `commands.md:1162` does not say so and `how-it-works.md:334` shows an id `migrate init` would refuse. `commands.md:116` lacks `--model`. Also fix the doubled `work: work line:` prefix. | 2/2/XS
- work batch done and review run only the tests a change reaches | 74 + 25 min of suite runs in 7 days, about 38 s a task at `-n auto`. Select each touched capability's `tests/scenarios/test_<cap>.py` and the `tests/scripts/` tests of changed modules, and keep the full suite at review (or nightly). Not via `tools tests-of`, whose coverage map is stale. Also split `test_bound` (7.5 s). b73 only measures this. | 4/3/M
- work batch brief runs its checks in parallel, and features bindings parses each test module once | `batch_brief._runs` runs five checks serially (`:136`); 19 min in 7 days. `features bindings --unbound` makes 978 `ast.parse` calls through 3 `test_modules` calls (4.2 s). Use one cached parse per module and a thread pool for the checks. | 3/2/S
- work decision <id> --amend adds enforced_by and rests_on | 10 of 12 hand commits to `spec/decisions/` add `enforced_by` or `rests_on` lines (26 lines, e.g. 58aec415d, 73f23e6e4). Amend an accepted decision in one commit, and have `work line --retires` name the decisions that cite the retired id. | 3/2/S
- work split and work retitle | Part of 22 hand commits that merge, split or retitle items. Merging folds into b281: add "with its reason and the item it went into" there rather than filing it. Split copies the selected lines to a new item with provenance; retitle keeps the id. | 2/2/S
- Lines amended on an in-batch item | b383 stops "before it is in a batch" and b431 covers ready items only. 38–59 hand commits changed lines of ready or in-batch items. `work amend <item>` relays the item on `batch-<n>` and its task branch. | 2/2/M
- Bulk retire from a file | 19 hand commits retired or renumbered lines in bulk (not re-run). `work line --retires-all --from <file>`. | 1/1/S
- spec catalogue entry and spec settings set | `grammar/catalogue-entries.toml` (305ae777e, b0c30b462) and `delivery.toml` (4 commits, one of which moved `batch_size` to the wrong table) are edited by hand. The settings part folds into b44 once b44 has lines. | 1/1/S

(The contracts plan and its items are kept in their own record, for the person's review.)
