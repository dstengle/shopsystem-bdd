---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-94/review-1
kind: review
batch: batch-94
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/117
head: 97ea2329b7246e0cb2d6fb02ddfe05c084ace0bf
range: 01644aea1c69ea4e7d2145af439acbf59fecbab2..97ea2329b7246e0cb2d6fb02ddfe05c084ace0bf
result: fix-now
---

# batch-94 review 1

## Verdict

The batch builds the three lines of b591 (checking#r88, r89, r90) and the chores of b592, b586 and b594. Every run in `## Runs` exits 0, as it does at the base. The size is 22 files and 540 changed lines, under the limit of 1000. One finding must be fixed: a commit cited to b591 changes `work batch brief` in a way no line of the batch asks for, and that narrows review-guarantees#r2.

## Findings

### f1 Important fix now: work batch brief leaves out superseded judgement decisions, which no line of the batch asks for
- item: b591
- where: scripts/batch_brief.py:54
Commit 0d40a84eb, cited to b591, makes `judgement` keep only the decisions whose `status` is `accepted`:

```
if data.get("tier") == "judgement" and data.get("status") == "accepted":
```

b591's lines (checking#r88-r90) are all about `spec obtain`. None of them says anything about which decisions reach the reviewer's brief. The commit adds a test for the new behaviour, `test_a_superseded_judgement_decision_is_left_out_of_the_brief`, so this is a deliberate change to what `work batch brief` prints, not a repair.

The change also reads against review-guarantees#r2: "While the tier of a design-decision is `judgement`, when `pr-reviewer` reviews a proposed change, `pr-reviewer` shall review the design-decision". That line does not limit itself to decisions in force. After this change a superseded judgement decision silently stops reaching the reviewer.

The commit message gives the reason: the base fails `test_the_judgement_decisions_reach_the_brief` since 0135 superseded 0123. That reason holds, but a requirement is never edited in place (decision 0085), and a change of observable behaviour needs a line behind it.

I checked whether the filter could also drop a live decision: every file under `spec/decisions/` has a `status:` line (134 of 134), so no accepted judgement decision is lost today.

Fix, either way:
- give b591, or an item of its own, a line that retires review-guarantees#r2 and limits it to judgement decisions in force, laid with `work batch amend`;
- or take the batch_brief change out of b591 and repair the base test's failure in its own item.

### f2 Minor observation: the module map's rows of batch_warm and batch_brief do not say what the batch changed
- item: -
- where: CLAUDE.md:230
CLAUDE.md says the module map is binding.
- **batch_warm (line 230):** the row still says `work batch merged` always starts the warming. It does not mention that nothing starts while `$SHOPSYSTEM_NO_WARM` is set (b592, scripts/batch_warm.py:208).
- **batch_brief:** its row still describes the brief as listing "the `tier: judgement` decisions", with no mention of the new in-force filter.

The module's own docstring does mention the switch.

Fix: add the switch to the batch_warm row, and update the batch_brief row once the finding above is settled.

### f3 Minor observation: a gh failure other than a 404 on the contents is now reported as the bounded context unreachable
- item: -
- where: scripts/contract_obtain.py:289
`_api` now turns any gh failure that is not a 404, such as a 403 rate limit or a 5xx, into `bounded context unreachable`. Before, it was refused as a plain gh failure.

`_reach` has already confirmed that GitHub serves the repository by the time `_api` runs. So a failure part-way through reading a repository that was just reached is named as unreachable, and the person cannot tell a transient error from a missing repository. r89 asks for this reason only when the availability is `unreachable`.

To reproduce: make the stand-in gh fail with a 403 on `repos/ex/inventory/contents/.shop/contracts` while `repos/ex/inventory` answers. `spec obtain` then names `bounded context unreachable`.

This hardens an input no client sends today. It does not hold the merge.
