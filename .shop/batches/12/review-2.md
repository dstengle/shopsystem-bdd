---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-12/review-2
kind: review
batch: batch-12
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/26
head: 7d8885c6bf0e13a30ddb8196564030a50378e0be
range: dcc53a599d7a50cb7cf3749971684edd825f46b0..7d8885c6bf0e13a30ddb8196564030a50378e0be
result: clean
---

# batch-12 review 2

## Verdict

The three fixes hold. f1's baseline now comes before the start check, and the new test fails without the fix. The Implementation bullets for f2 and f3 describe what the code does. One observation, which does not hold the merge.

## Findings

### f5 Minor observation: a baseline that fails, or one taken only after the start, leaves the same uncovered window f1 had
- item: b78
- where: scripts/request_forward.py:209
The fix takes the notifications' baseline once, before the start check, and only when `watched.polled` is non-empty after the first `arm()`. Two paths still make a later `Notifications.changed` call the first one, and that call discards everything it lists without any check covering it:
- The baseline call's `gh` fails, or its response carries no status or a status other than 200. `self.since` stays `None` (scripts/request_forward.py:120-134), so the first poll after the first wait is the baseline again. A readable comment that came between the start check and that poll is dropped. Every later poll answers 304.
- No repository is polled at the start: every repository is forwarded. Later a forward ends, or a request on a repository the account does not administer is raised, and `arm()` (lines 152-169) adds it to `polled`. The next `changed` (line 221) is then the first call. It returns False, and no check covers the time between the forward ending and that call.

Neither path is in any test, and no line names it. Hardening: run `check(root)` straight after any call that set `since` for the first time, or keep the baseline's listed repositories and count them as a change.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
