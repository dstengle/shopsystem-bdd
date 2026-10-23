# Plan of w97: work-item ids, the review's open findings

Accepts design-model-check#r110 and work-queue#r12. The work-item names four findings: N9 F6 (held id checked on the stem only), N9 F10 (`work add` beside a `w<n>.md` that is no work-item), N7 (an unreachable branch of `entry`), N2 (the named-problem step drops r110's problems for every fixture). No `## Rulings`; no Retires section, so no deprecated scenario is retired.

## 1. What goes green

- **design-model-check#r110**, "a work-item not named w<n>.md, or two work-items with one id, is a file problem" (outline, 4 examples). Not red today (notes §1, run): every fixture gives each work-item an id equal to its stem, so the stem-keyed check and an id-keyed check agree. The defect it misses (notes D3, run): `model check` prints no problem for two work-items with one id under different stems, nor for `w3.md` holding id `w9`.
- **work-queue#r12**, "add numbers the new work-item one above the highest work-item under .shop/work/, in any initiative and any status". Not red today (notes §1, run): fixtures again have id = stem and no stray `w<n>.md`. Defects it misses (notes D1, D4, run): a plain note `w2.md` beside `w1.md` makes `add` refuse, naming a work-item w2 that does not exist; a work-item `fix-login.md` holding id `w2` (or `w7`) is not counted, so `add` writes a second `w2`.

Both scenarios stay green throughout; the work is the defects behind them. No scenario goes red first; the implementer shows each changed behaviour by a probe or a script test before the change (see §5).

## 2. Where the change lands

- `scripts/model_work.py` (211 lines): `check_work_item_name` keys `held` by the work-item's frontmatter id, not its stem, and reports a work-item whose id's `w<n>` is not its file's stem (F6, D3).
- `scripts/workqueue.py` (255 lines): `highest` counts the `<n>` of every work-item's id as well as of its file name (D4), and whatever the answer to the question below makes of a `w<n>.md` that is no work-item (F10, D1); `add`'s refusal on an existing file is touched only under reading B of the question; `entry` loses its unreachable branch (N7).
- `tests/scenarios/design_model_check_problems.py` (288 lines, 12 to spare): the step "it prints a file problem naming …" drops r110's problems only for a fixture whose problem path is not a `w<n>.md` (N2). The change must not take the file past 300.

Removed from the researcher's set as read-only, no change planned: `scripts/model_parse.py`, `tests/scenarios/work_queue_add_steps.py`, `tests/scenarios/test_design_model_check.py`, `tests/scenarios/design_model_check_then.py`, `tests/scenarios/test_work_queue.py`. A script test the implementer adds for D3/D4 (§5) goes in `tests/scripts/` as a new file. It is part of the claim only if added; it is not in the file set below.

## 3. Decisions

1. **r110 reads the id, not only the stem.** A work-item breaks r110 when its file name is not `w<n>.md`, or when its id's last segment is not its file's stem, or when another work-item already holds its frontmatter id. Rests on design-model-check#r110 and design-decision/work-items-named-by-ids: the file is `w<n>.md` and the id is `work-item/<context path>/w<n>`, the same `w<n>`, never repeated. `held` maps the qualified id to the first file holding it. Each work-item still gets at most one r110 problem. The id/stem mismatch problem stays worded so that the N2 filter (decision 4) recognises it as r110's: either it uses the existing "a work-item's file is named w<n>.md" wording, or the filter learns its words.
2. **`work add` counts ids.** `highest` takes the greatest `<n>` over every work-item under `.shop/work/` (`kind: work-item`, any initiative, any status), counting both its id's `w<n>` and its stem's `w<n>`, where each is of that form. With `fix-login.md` holding w7 beside `w1.md`, `add` prints w8, and it never writes an id a work-item already holds. Rests on work-queue#r12 ("the highest `<n>` of any work-item": a work-item's `<n>` is its id's, by design-decision/work-items-named-by-ids) and that decision's "never repeated". This settles the researcher's first question.
3. **N7.** `entry` is called only with "initiative" (by `add` and `supervise.py`), so its "file name" branch is unreachable. It drops the `what == "name"` alternative, and its message for an initiative is unchanged. No observable change.
4. **N2.** In "it prints a file problem naming …", r110's lines are filtered out only when the named path is not a `w<n>.md` file. The finding says to drop them only for fixtures not named `w<n>.md`. A fixture whose work-item is a `w<n>.md` then has any r110 problem counted, so a stray held-id or mismatch problem fails the step instead of hiding.
5. **Non-UTF-8 notes (D2) are left as they are.** `work add` still refuses on a non-UTF-8 `.md` under `.shop/work/<initiative>/`, under work-queue#r7: it cannot read whether the file is a work-item. None of the work-item's findings names this case, and changing it changes what the narrator sees, so it stays outside this work. This settles the researcher's second question for D2. D1 is the open question below.

## 4. Tests the decisions break

- `tests/scenarios/test_work_queue.py`, the r12 scenario: kept. Its fixtures have id = stem, so decision 2 still gives w5 (notes §4).
- `tests/scenarios/test_design_model_check.py`, the r110 outline, 4 examples: kept. Ids equal stems, so the id-keyed `held` (decision 1) gives the same answers. Example 1 (`fix-login.md` holding w3) still prints the file-name problem.
- `design_model_check_problems.py`, "it prints a file problem naming …": rewritten by decision 4. Every scenario that uses this step must still pass. The risk is a fixture that writes a work-item as `w<n>.md` with an id whose last segment is not that stem: decision 1 would add a problem, and decision 4 would count it. The implementer runs every scenario using the step after decisions 1 and 4. Any that fails is a fixture fault, mended in the fixture so that its id is its stem, not by widening the filter. Not verified here: the researcher found the step's users by search only (no coverage map).
- No other test asserts `highest`, `check_work_item_name` or `entry` (notes §3–4, by search).

## 5. Open cases (for the implementer to name, not choose)

- No accepted scenario gives a work-item whose id differs from its stem, two stems holding one id, or a non-`w<n>` work-item whose id is counted by `add`. Decisions 1 and 2 are shown red by the researcher's probes (notes §2) or by a new script test in `tests/scripts/`. Proposing scenarios for them is the specifier's work, not this item's.
- A work-item whose frontmatter has no `id`, or an id that is not of the form `work-item/<context path>/w<n>`: what r110 says about it, and whether `highest` counts its stem.
- An id held twice in which one holder is not named `w<n>.md`: whether it gets one problem or two. Decision 1 says at most one r110 problem per work-item; the implementer names which.
- A `w<n>.md` that is no work-item: what `add` does with it depends on the question.

## Question

D1 / F10: beside work-item `w1.md`, `.shop/work/i1/w2.md` is a plain note, not a work-item, and `work add i1 …` is run.
- Reading A (r12 and r7 as written): the highest work-item is w1, so the new id is w2. Its file exists, so `add` refuses and changes nothing. The refusal names `.shop/work/i1/w2.md` as a file that is not a work-item, not as "the work-item w2 already exists".
- Reading B (the work-item's "number it past every `w<n>.md`"): `add` prints w3 and writes `w3.md`, one above the highest `w<n>.md` file, not one above the highest work-item.
