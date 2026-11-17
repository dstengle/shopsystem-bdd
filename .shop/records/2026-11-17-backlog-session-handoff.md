---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-17-backlog-session-handoff
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-17
---

# Backlog session handoff

Where the session that worked the backlog on 2026-11-16 and 17 left it, for the next session. The person's standing direction is directive-1 (merge, release, decide when away); directive-2 to -4 are shown at SessionStart.

## State

- No batch open: batch-45 merged (PR #68). Releases: 0.35.1 (PR #60), 0.36.0 (PR #65). Batches 41-45 delivered after 0.36.0 and are unreleased: b65, b77, b6, b286 shipped in 0.36.0; b175, b296, b305, b314 (batch-43), b20, b315, b316, b317 (batch-44), b301, b323, b232 (batch-45) are not.
- Ready: b289 (chore; its work is on branch batch-45-b289, commit 6a9c3ce1d, to cherry-pick), b346 (chore: the parallel shaping brief), b318, b309, b324, b334, b333.
- The triage: .shop/records/2026-11-16-backlog-triage.md. Every open item is rated.

## How the session worked

Shaping in waves of about six agents, one item each, in parallel, each given the brief in this record's folder (`shaping-brief-wave.md`) with "Your item is b<n>". b346 makes that brief part of the plugin. A batch is started with `work batch start` run in the background with no time limit (it took over 28 minutes once: b340), then one driver agent is given the brief's path. Drivers often stop while a task is still out or its reply came to the session instead: check `work batch status` and resume the driver with what it is missing. A release is a plan record, one implementer on a branch, one fresh reviewer, the review recorded, then merge and tag.

## Known traps

- An agent's note appended by hand to an item lands under `## Requirements` and `work batch start` refuses the item (b281).
- Every task's first `work batch done` fails on the corpus blocks and catalogues until b333 is built; drivers put one shared commit on each branch.
- `git stash` is shared by every worktree (b289).
- The live-repo timing test fails when task suites run at once; close tasks one at a time.
