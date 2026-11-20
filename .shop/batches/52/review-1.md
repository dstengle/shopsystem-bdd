---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-52/review-1
kind: review
batch: batch-52
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/76
head: 84f9762d39c9f39a3db40b20052baff8b416ccbd
range: 231e5b6990c8d868ae639cd4e2845084d4805db1..84f9762d39c9f39a3db40b20052baff8b416ccbd
result: clean
---

# batch-52 review 1

## Verdict

The batch builds b416's one line, scenarios#r33. When a response gives out a thing by a trigger's or While part's thing ("return the items of the checklist"), `features generate` now brings that thing and its row in with Givens before the When. The regenerated features and the new r33 scenario show it, and every run exits 0, at the base too. Nothing needs fixing now; there are two observations. Moving `bring_response` out of spec_steps4_boxes into the new spec_steps4_bring matches the module map's new row and the edited rows. The test changes strengthen the checks rather than weaken them: feature-file-tools now handles its own "does not keep" Thens, which requests' "does not post" handler used to pass without checking anything.

## Findings

### f1 Minor observation: an owner that is an indexical ("this K") is not taken as an owner
- item: -
- where: scripts/spec_steps4_bring.py:89
`owner` takes a row `K1 | of | K2` only when K2's origin is `while` or `trigger`. In the logical form, a referent made by a kind's `This:` has the origin `indexical`. So a line such as "When the person lists this backlog, the backlog service shall return the items of the backlog" falls outside b416's case. Its item would still be mentioned by a Then that no Given introduces, which is what r33 forbids for any line that uses `of-relation` in its response. I have not seen such a line among this repository's capabilities, and the `features generate --check` run is clean, so nothing breaks today. Reproduction: add that line to a codified-2 capability whose `backlog` entry has `This:`, run `features generate`, and look for `the item i1` with no `Given an item i1`. Fix when it comes up: also accept `indexical` (and `where`, if Where referents carry their own origin) in the origin test.

### f2 Minor observation: the r33 test lines have no precondition at all
- item: b416
- where: tests/scenarios/feature_file_tools_collections.py:78
The "owned" lines that `check` reads back are both untriggered by any While part ("When the person runs `work status` on a stage, ..."). So the case where K2 comes from the While part, which `owner` also accepts and the module map's row names, is not exercised. The r33 line only asks that the precondition not use `of-relation`, so the test meets it. Hardening: add a line whose owner a While clause introduces, e.g. "While a stage is open, when the person runs `work status`, `work` shall print the lines of the stage."
