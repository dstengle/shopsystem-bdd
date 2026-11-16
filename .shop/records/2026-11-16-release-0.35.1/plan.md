# Release 0.35.1: holds-exactly, holds nothing, holds no K and orders on any response's object

The person, 2026-11-16, on the feed product's feedback that 0.35.0's collection lines parse but are not checked or generated on a returned object: "Go ahead." (quote-34), approving b297, b298, b299 and b307 as a fix batch and its release to unblock feed. The release ships batch-38 (PR #59):

- b297: holds-exactly with any restriction its every half reads, not only one value, and holds nothing, on a response's object, read by `model logic` and written by `features generate` (batch-34 defects 1 and 2);
- b298: the scenario of `order-by` on the object of a verb whose frame names the collection's kind, not `thing` (batch-35 defect 3);
- b299: the Then of "y holds no K" on a response's object, with a counter-example K the object does not hold;
- b307: `work ready` refuses an item a requirement of which `model logic` names `unread`.

It is carried out on one branch `plan-release-0.35.1` by one fresh agent, then one fresh reviewer of the whole branch, then a pull request that the session merges, and the tag `v0.35.1` on its merge commit.

## Why 0.35.1

Design-decision 0092 and docs/upgrading.md's Versions section: z for a fix with no upgrade step and no line reworded. These lines were refused by `model logic` or `features generate` in 0.35.0, so a consuming repository had no scenario of them to break. Task 1 checks that: if any scenario `features generate` wrote at v0.35.0 for a line that still reads the same changes, stop and say so in the reply, since that makes it 0.36.0.

## Tasks

1. **Check the bump.** `git diff v0.35.0 main -- features/` and read each changed scenario: only the new ids' scenarios (design-model-check r314, r315; feature-file-tools r125-r128; readiness r41) may be new or changed. Name any other.
2. **Version.** `.claude-plugin/plugin.json` `version` and `.shop/plugin-version` set to `0.35.1`; every place that names the current release as 0.35.0 updated (README.md, docs/getting-started.md, docs/upgrading.md: `grep -rn "0\.35\.0"` outside CHANGELOG.md, docs/history/, .shop/, spec/ and tests/). Do not edit spec/ unless a test fails without it; say so if you do.
3. **CHANGELOG.md.** A section `## 0.35.1: collections on any response's object`, newest first, its link in the 0.35 row of the Line table. In the voice of the existing sections, one bullet per item with its PR (#59). Say plainly that 0.35.0's holds-exactly on a response's object read only a value restriction, and that holds nothing and holds no K on a response's object, and an order on a verb whose frame names its kind, had no translation or scenario. An **Upgrading** bullet: no upgrade step; `features generate`, then handlers for the new scenarios; `work ready` may now refuse an item `model logic` cannot read.
4. **docs/upgrading.md.** A section "From 0.35.0 to 0.35.1" saying the same, short.
5. **docs/writing-requirements.md** section 3: where it shows these forms only after `print`, or says an order is a property of what a response prints, make it say any act's object. Every line and Gherkin block you add or change must pass the docs tests (tests/scripts/test_docs_lines.py).
6. **Checks.** The whole suite passes (`python3 -m pytest -q -n auto`; a test known flaky under load, test_work_watch_forward_wakes_on_a_new_ask or test_measure_defect.py, rerun alone and named in the reply), `python3 scripts/tools check --base main`, `python3 scripts/tools size --limit 300`, `python3 scripts/features generate --check`, `python3 scripts/model rules --check`, `python3 scripts/model constructs --check` exit 0. Commit messages end with `Release: 0.35.1`.

## Not in this release

b300 (order-by-every after a verb whose frame names its kind; b312), b301, b302 (language.md's print-only wording, unless task 5 fixes the same words there), b303-b305, b306, b308, b309, b310, b311, b313.
