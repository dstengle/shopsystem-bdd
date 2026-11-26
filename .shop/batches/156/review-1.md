---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-156/review-1
kind: review
batch: batch-156
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/179
head: 690d98937a693b5c09bc77104d646be025ea6a68
range: b74663f8975db4b0d577412974a44d7f643d4791..690d98937a693b5c09bc77104d646be025ea6a68
result: clean
---

# batch-156 review 1

## Verdict

The batch builds all three items. b797's `--item` on `spec check` and `spec trace` meets checking#r152 and product#r58, and b800's `--reword-term` meets drafting#r95: it now takes a `- ` bullet with no `--` before it, and it takes `--into`. b792's chore stays inside its files. Every run exits 0, as it did at the base. The change is 822 lines, under the 1000-line limit. Nothing needs fixing before the merge. There are two observations: `spec check --item` probably reports false errors for an item's new groups, and `--remove-term` now takes `--into` too, which no line asks for.

## Findings

### f1 Important observation: `spec check --item` reports false errors for the item's own new groups
- item: b797
- where: scripts/spec_preview.py:42
The risk: `spec check --item` exits 1 with errors that are not real whenever the item adds a group. I did not run it. What I read shows this:
- `_beside` links `features/` instead of copying it, and nothing generates scenarios on the copy.
- `spec annotate` does not run on the copy either.
- model.lp's `v_s3` ("a group has no scenario", severity `error` in grammar/rules.md:689) fires for any group with no `@g<n>` scenario. The item's new groups have none in the linked features.
- `v_a5` (a governing requirement missing from the adapter contract) likely fires as well. The copied `spec/adapters/cli.toml` is never annotated with the item's new lines.

The readiness bar avoids both by generating features and by leaving out v_a5 (decision 0112). `spec check --item` does neither.

tests/scenarios/checking_handlers_item.py lays a new notebook group g10 with a line that lists the notes. Its Then reads only the rows under `w_unserved_job` and never the exit code, so these errors would go unseen there. The docs' own examples only add `serves:` pairs to live groups, so they do not hit this. But skills/shaping-items/SKILL.md step 5 tells the session to run `shop spec check --item <b>` on items that hold lines, and it would see errors the item did not cause.

checking#r152 is met as written, so this does not hold the merge. Fix: generate the laid capabilities' features on the copy (copy `features/` rather than link it) and annotate the copied contract. Or leave out the rules the bar leaves out, and say so in the docs.

### f2 Minor observation: `--remove-term` now takes `--into`, which no line asks for
- item: b800
- where: scripts/backlog_model_edit.py:598
`cmd` no longer refuses `--into` with any of the term flags. Before this change, `work line b1 --remove-term folder --into notebook` was refused with "--into only of a model line". Now it narrows the search to notebook's area or its block. drafting#r95 and b800's title ask only for the reword. The change is harmless and consistent with how `--term` behaves, but it changes a refusal that no line names. Either add a line for remove-term with a capability, or keep refusing `--into` with `--remove-term`.
