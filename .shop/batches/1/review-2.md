---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-1/review-2
kind: review
batch: batch-1
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/17
head: de270d102626e91c0108a5e25c5c2e45713c12e3
range: 584d5eca37c29139c77ea063ecc7b12a1d3e77f4..de270d102626e91c0108a5e25c5c2e45713c12e3
result: fix-now
---

# batch-1 review 2

## Verdict

The four fixes close f1-f4. The f1 fix leaves one thing stale: the `request_sync.py` row of CLAUDE.md's module map still says sync prints only live requests. That is one new Minor finding to fix.

## Findings

### f10 Minor fix now: the module map's `request_sync.py` row still says "every live request printed"
- item: b26
- where: CLAUDE.md:83
- The f1 fix (2d6066ec) changed what `work sync` prints. It now prints every request with its status, and adds "whose move it waits on" only for a request that is not closed. The fix updated the module docstring (scripts/request_sync.py:2) and the requests Implementation section to match. It did not update the module map, and the module map is binding. Its row for `scripts/request_sync.py` still reads:
```
| `scripts/request_sync.py` | `work sync`: ... an unreadable one printed and never recorded, every live request printed with whose move it waits on |
```
So the map now contradicts the code, in the same way f4 was about the `request_view.py` row. The f4 fix updated that row in the same batch. Fix: reword the row to say "every request printed with its status and, unless it is closed, whose move it waits on".

### f11 Minor observation: a comment on a closed request's issue can set its status back
- item: b26
- where: scripts/request_sync.py:42
- Since the f1 fix, `caught_up` reads the issues of `delivered`, `refused` and `withdrawn` records too. `applied` writes any `status:` or `turn:` field a comment carries, with no check on the record's current status. So a comment on a closed issue that carries `status: open` would reopen a delivered record on this side. The other side's own moves never post that today; the new test posts only `step: turn` with a question, and the record stays `delivered`. What I read: `applied` at scripts/request_sync.py:42-44 sets the fields without any condition, and `CLOSED` is now used only in `waiting`. Hardening: ignore `status` and `turn` in a comment on a closed record, or refuse such a comment as unreadable.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
- f4: fixed
