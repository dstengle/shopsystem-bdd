---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-113/review-2
kind: review
batch: batch-113
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/136
head: 2226b3c37981a8526541ac776437a5b31fe283b2
range: ce7866d87ae28aa619e4241a75e45fd0ed9677ab..2226b3c37981a8526541ac776437a5b31fe283b2
result: clean
---

# batch-113 review 2

## Verdict

The fix for f1 is right. `write` no longer refuses a pack that spec/index.md already imports. The test now checks that such a pack is kept in the item and laid into spec/index.md only once. One new observation: the module map row for `scripts/backlog_import.py` still describes the old refusal.

## Findings

### f6 Minor observation: the module map row of backlog_import still says an index import is refused
- item: b672
- where: CLAUDE.md:-
The fix (8118894e5) took out the check in `write` that refused a pack spec/index.md already imports. It also rewrote the module's docstring to say such a pack "is kept too". The `scripts/backlog_import.py` row of CLAUDE.md's module map did not change and still reads:

```
(a pack of the plugin's `grammar/packs/`, else refused naming the pack; one spec/index.md or the item imports already refused: `write`, `cmd`)
```

CLAUDE.md says the module map is binding, so the row now contradicts the code. Behaviour is correct: drafting#r73 is met and the lay does not list the pack twice (`backlog_pack._index` leaves `imports:` unchanged when the pack is already there). Fix: reword the row to "one the item imports already refused; one spec/index.md imports kept".

## Earlier findings
- f1: fixed
