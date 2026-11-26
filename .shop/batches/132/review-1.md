---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-132/review-1
kind: review
batch: batch-132
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/155
head: 0f7b98a030bf2cf1af91c4a7fd669e5960da7eef
range: a177f280f511c23e61ee4042b6306e1a147ad993..0f7b98a030bf2cf1af91c4a7fd669e5960da7eef
result: clean
---

# batch-132 review 1

## Verdict

The batch builds all three items. b731 (items#r73 and batches#r169) adds v_m9 to the violations the readiness bar and `work batch start` count, and names the item's own requirement in each. b728 (scenarios#r46) takes a reply trigger's requester from the context's line that makes the request, else from the operation's `by` actor, and refuses naming the operation when there is neither. b733 (scenarios#r48) writes a code before its kind's noun only when the bare step reads more than one way. Every run exits 0 at `Head:`, as at the base, and the change is 732 lines against the 1000 limit. I found nothing to fix now; one observation follows.

Checks I made against risks I could name:
- **Test removed in `checking_handlers_reply.py`:** the `spec logic` branch and the `then_returns` handler are gone. No scenario in `features/checking.feature` says `spec logic` or `no findings`, so nothing reached that code. b728's title asks for the test file's branches to all run, so this is not a weakened test.
- **The r48 test could pass without testing anything:** `feature_file_tools_ambiguous.prepare` adds its row by replacing the text `| file | in | worktree |  |`. If that text were missing, the step would never be ambiguous and the test would pass anyway. The text is present in `grammar/corpus/constructs/spec/index.md:20`, so the step it builds really does read two ways.
- **v_m9's arguments:** `readiness_bound.transitions` unpacks four values (object, attribute, from, to). That matches `v_m9/4` in `scripts/model.lp:521-522`, and it joins the same `sets`/`sets_from_any`, `requester`, `op_area` and `obj_area` facts as those rules.
- **Hand-written feature lines:** the changed lines in `checking.feature`, `feature-reading.feature`, `upgrades.feature` and `batches.feature` come from b733's change to how a code is written. `features generate --check` exits 0, so they are generated, not written by hand.

## Findings

### f1 Minor observation: a code whose kind differs between lines is never named, so its step can still read two ways
- item: b733
- where: scripts/spec_steps4_code.py:25
`kinds` drops any code that refers to things of two different kinds across the group's forms. If a bare step with such a code reads more than one way, `one` has no kind to name it by and raises a TraceError. `features_generate4.lines` then writes no scenario for the group and lists it as skipped. No line in this repository has that shape today.

Reproduction: write a group of two lines that use the same backticked code for things of two kinds (say a stage and a worktree), each kind reachable through a row the bare code can also read. `features generate` reports "no scenario: the step ... reads more than one way".

A possible fix: key the kind by the referent the bare node stands for, not by the code's text.
