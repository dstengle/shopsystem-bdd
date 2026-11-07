---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-12/review-1
kind: review
batch: batch-12
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/26
head: dcc53a599d7a50cb7cf3749971684edd825f46b0
range: 9fbfaf01c2d7888879b966e4b0553d31bda313fc..dcc53a599d7a50cb7cf3749971684edd825f46b0
result: fix-now
---

# batch-12 review 1

## Verdict

The batch builds all five lines: r54-r56 through `work watch --hook` and `request_hook watch`, and r57-r58 through `work watch --forward`. Three findings need fixing first. On a polled repository, the watch can miss a comment that arrives during its first wait. And on both items, observable behaviour beyond the lines is not given in the capability's Implementation section, which says nothing of `--forward` or `--hook`. One observation is recorded. The size (+591 -23) is under the limit, every run exits 0, and no test was removed or weakened.

## Findings

### f1 Important fix now: a comment on a polled repository during the first wait never wakes `--forward`
- item: b78
- where: scripts/request_forward.py:358
`forward` runs its first check, then waits up to `--every` seconds (default 60). Only after that wait does it make the first `Notifications.changed` call. That first call is the baseline, and it always returns False:
```
return not first and any(...)
```
It also sets `since` to the response's `Last-Modified`. Suppose a readable comment lands on a polled repository (an upstream's, the common case for a sent request) after the start check and before that first call. The baseline response already lists it and discards it, and every later `If-Modified-Since` call answers 304. The watch then sleeps until some other notification comes, or until the Monitor times out. That breaks r57: the comment is unrecorded and readable, and `work watch --forward` does not print it. Nothing in the batch tests this window. The stand-in only brings pending comments back on an `If-Modified-Since` call, which is why `test_a_repository_not_administered_is_polled_through_notifications` passes.

Fix: take the notifications baseline before the start check. Call `notes.changed(watched.polled)` once right after `watched.arm()` in `forward`, so the start check covers everything up to the baseline. Add a test where the stand-in holds the comment for the baseline call.

### f2 Important fix now: `--forward` installs a gh extension and polls notifications, and no line or Implementation bullet gives this
- item: b78
- where: scripts/request_forward.py:211
r57 and r58 only ask `work watch --forward` to print and exit. Several things the change does are observable but given neither by a line nor by the Implementation section of `spec/capabilities/requests.md`, which describes only `work watch [--every] [--polls]` (lines 282-292):
- it runs `gh extension install cli/gh-webhook` on the person's machine;
- it runs `gh webhook forward` only on repositories with `viewerPermission` ADMIN;
- it falls back to GitHub's notifications and says so on stderr (`polling GitHub's notifications for …`);
- it changes the meaning of `--every` and `--polls`, and ends with `nothing new after <n> waits`, exit 1.

These are in b78's Notes and the module map, but neither is a line or an Implementation bullet. Fix: add an Implementation bullet for `work watch --forward` to `spec/capabilities/requests.md`, saying what this code does.

### f3 Minor fix now: what `work watch --hook` prints beyond the request is in no Implementation bullet
- item: b79
- where: scripts/request_watch_hook.py:479
r54 and r55 ask the hook to print the request; r56 asks it to be silent. The hook also prints:
- the `START` line, telling the session to start `work watch --forward` with the Monitor tool;
- each request's line form, `<name> <status>: <title> (<issue>)`.

It also exits 0 on any error, and `request_hook` exists as a separate entry point because `work` imports clingo. The requests capability's Implementation section gives none of this. Fix: add an Implementation bullet for `work watch --hook` and `request_hook watch` to `spec/capabilities/requests.md`.

### f4 Minor observation: a forwarded repository's event can fall between the start check and the webhook's registration
- item: -
- where: scripts/request_forward.py:347
`Watched.arm` starts `gh webhook forward` with `Popen` and does not wait. `check(root)` runs right after. The extension needs a moment to create the repository webhook. A comment posted between the check and the webhook going live sends no event, so it waits for the next one or a Monitor restart. What I read: the `forward` and `arm` sequence in the diff; the stand-in's `forward` cannot show this gap, because it waits for an `issue list` call before posting. The window is seconds, against the full wait in the finding above. Hardening: run the check a second time after the forwards report ready, or after a short delay.
