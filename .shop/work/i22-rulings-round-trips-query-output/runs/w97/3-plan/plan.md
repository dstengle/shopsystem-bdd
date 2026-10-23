# Plan of w97: work-item ids, the review's open findings

Accepts design-model-check#r110 and work-queue#r12. The work-item names four findings: N9 F6 (held id checked on the stem only), N9 F10 (`work add` beside a `w<n>.md` that is no work-item), N7 (an unreachable branch of `entry`), N2 (the named-problem step drops r110's problems for every fixture). No Retires section, so no deprecated scenario is retired. The work-item's `## Answers` holds the person's answer of 2026-10-23 to the earlier plan's question (F10/D1): reading A, r12 and r7 as written. This plan takes it as a ruling (decision 3). It replaces the plan of `runs/w97/2-plan`. Apart from decision 3 and the test file, it keeps that plan's decisions.

## 1. What goes green

- **design-model-check#r110**, "a work-item not named w<n>.md, or two work-items with one id, is a file problem" (outline, 4 examples). Not red today (notes §1, run). Every fixture gives each work-item an id equal to its stem, so a check keyed by stem and one keyed by id agree. The defect it misses (notes D3, run): `model check` prints no problem for two work-items with one id under different stems, nor for `w3.md` holding id `w9`.
- **work-queue#r12**, "add numbers the new work-item one above the highest work-item under .shop/work/, in any initiative and any status". Not red today (notes §1, run). Here too ids equal stems, and no stray `w<n>.md` sits in the fixtures. The defects it misses (notes D1, D4, run):
  - A plain note `w2.md` beside `w1.md` makes `add` refuse, naming "the work-item w2", which does not exist.
  - A work-item `fix-login.md` holding id `w2` (or `w7`) is not counted, so `add` writes a second `w2`.

Both accepted scenarios stay green throughout. The work is the defects behind them. No accepted scenario goes red, so the implementer shows each changed behaviour red first in a new script test (§2). The researcher's probes (notes §2) give the fixtures.

## 2. Where the change lands

- `scripts/model_work.py` (211 lines): `check_work_item_name` keys `held` by the work-item's frontmatter id, not by its stem. It also reports a work-item whose id's `w<n>` is not its file's stem (F6, D3; decision 1).
- `scripts/workqueue.py` (255 lines):
  - `highest` counts the `<n>` of every work-item's id as well as of its stem, and only work-items (D1, D4; decision 2).
  - `add`'s refusal when the new id's file exists names that file as one that is not a work-item (F10; decision 3).
  - `entry` loses its unreachable branch (N7; decision 4).
- `tests/scenarios/design_model_check_problems.py` (288 lines, 12 to spare): the step "it prints a file problem naming …" drops r110's problems only for a fixture whose named path is not a `w<n>.md` (N2; decision 5). It must not go past 300 lines.
- `tests/scripts/test_work_item_ids.py` (new): script tests that show each changed behaviour red, then green. They cover:
  - D3: two stems holding one id, and `w3.md` holding `w9`, are each a file problem.
  - D4: `fix-login.md` holding `w7` beside `w1.md` makes `add` print `w8`.
  - F10: the plain note `w2.md` beside `w1.md` makes `add` refuse, naming `.shop/work/i1/w2.md` as not a work-item, and write nothing.

  CLAUDE.md's module map puts tests that no scenario drives in `tests/scripts/`. This test file was added to the researcher's set because no accepted scenario is red.

Removed from the researcher's set as read-only, with no change planned: `scripts/model_parse.py`, `tests/scenarios/work_queue_add_steps.py`, `tests/scenarios/test_design_model_check.py`, `tests/scenarios/design_model_check_then.py`, `tests/scenarios/test_work_queue.py`.

## 3. Decisions

1. **r110 reads the id, not only the stem.** A work-item breaks r110 when any of these holds:
   - its file name is not `w<n>.md`;
   - its id's last segment is not its file's stem;
   - another work-item already holds its frontmatter id.

   This rests on design-model-check#r110 and design-decision/work-items-named-by-ids (0061): the file is `w<n>.md` and the id is `work-item/<context path>/w<n>`, the same `w<n>`, never repeated. `held` maps the qualified id to the first file that holds it. Each work-item still gets at most one r110 problem. The new id/stem problem must be worded so that decision 5's filter recognises it as r110's: it either reuses the wording "a work-item's file is named w<n>.md", or the filter learns its words.
2. **`work add` counts work-items by their ids.** `highest` takes the greatest `<n>` over every work-item under `.shop/work/` (`kind: work-item`, any initiative, any status). For each work-item it counts the id's `w<n>` and the stem's `w<n>`, where each has that form. A `.md` that is not a work-item counts for nothing. So with `fix-login.md` holding `w7` beside `w1.md`, `add` prints `w8`, and it never writes an id a work-item already holds. This rests on work-queue#r12 ("the highest `<n>` of any work-item"; by 0061 a work-item's `<n>` is its id's) and on 0061's "never repeated". It settles the researcher's first question.
3. **A `w<n>.md` that is no work-item: reading A (the person's answer, 2026-10-23, in the work-item's `## Answers`).** Beside work-item `.shop/work/i1/w1.md` sits a plain note `.shop/work/i1/w2.md`. Then:
   - by decision 2 the new id is `w2`;
   - its file exists, so `work add i1 …` exits with an error and writes and commits nothing (work-queue#r7);
   - the refusal names `.shop/work/i1/w2.md` as a file that is not a work-item, in place of today's "the work-item w2 already exists".

   `add` does not number past the note (the finding's reading B is not taken). The refusal still says that `work add` leaves the file as it was. A file at the new id's path can only be a non-work-item, because decision 2 counts every work-item's stem. So the old "work-item … already exists" wording has no case left, and the refusal's words are the new ones only.
4. **N7.** `entry` is called only with "initiative" (by `add` and `supervise.py`), so its "file name" branch cannot be reached. The `what == "name"` alternative goes, and the message for an initiative stays as it is. Nothing the narrator sees changes.
5. **N2.** In "it prints a file problem naming …", r110's lines are filtered out only when the named path is not a `w<n>.md` file, as the finding asks. A fixture whose work-item is a `w<n>.md` then has any r110 problem counted, so a stray held-id or id/stem problem fails the step instead of hiding.
6. **Non-UTF-8 notes (D2) are left as they are.** `work add` still refuses on a non-UTF-8 `.md` under `.shop/work/<initiative>/`, under work-queue#r7: it cannot read whether the file is a work-item. The person's answer takes "r12 and r7 as written", and no finding of the work-item names this case. This settles the researcher's second question for D2. Decision 3 settles it for D1.

## 4. Tests the decisions break

- `tests/scenarios/test_work_queue.py`, the r12 scenario: kept. Its fixtures have ids equal to stems and no stray note, so decision 2 still gives `w5` (notes §4).
- `tests/scenarios/test_design_model_check.py`, the r110 outline, 4 examples: kept. Ids equal stems, so the `held` keyed by id (decision 1) gives the same answers. Example 1 (`fix-login.md` holding `w3`) still prints the file-name problem.
- `design_model_check_problems.py`, "it prints a file problem naming …": rewritten by decision 5, as above. Every scenario that uses this step must still pass. The risk is a fixture that writes a work-item as `w<n>.md` with an id whose last segment is not that stem: decision 1 adds a problem for it, and decision 5 counts it.
  - The implementer runs every scenario that uses the step once decisions 1 and 5 are in.
  - A scenario that then fails has a faulty fixture. The fix goes in the fixture, so that its id is its stem, and the filter is not widened.

  Not verified here: the researcher found the step's users by search only (no coverage map).
- Decision 3 changes the words of `add`'s refusal on an existing file. A search of `tests/` and `scripts/` for "already exists" finds no test of `work add` that asserts them; the one match is a migrate step about `migrate run`. Nothing breaks.
- No other test asserts `highest`, `check_work_item_name` or `entry` (notes §3–4, by search).

## 5. Open cases (for the implementer to name, not choose)

- A work-item whose frontmatter has no `id`, or an id not of the form `work-item/<context path>/w<n>`: what r110 says about it, and whether `highest` counts its stem.
- An id held twice where one holder is not named `w<n>.md`: one problem or two. Decision 1 allows at most one r110 problem per work-item; the implementer names which.
- A plain note `w2.md` in another initiative `i2` while adding to `i1`: by decisions 2 and 3, `i1/w2.md` is free and is written. The implementer names this case in the script test or leaves it out; no scenario gives it.
- Scenarios for decisions 1–3 (a new example of the r110 outline, or a new r12 scenario) are the specifier's work, not this item's.
