---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the supervisor closing a work-item or an initiative
group: service
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files]
formulated_as: features/review.feature
retired: []
---

# Review

## Purpose
Finds defects in one work-item's commits or in an initiative's whole branch, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Behaviour
- [r1] **When** a review ends, its findings are in the findings file and the result file the brief names, and the working tree, index, HEAD and branches are as they were.
- [r2] **When** a task or branch review ends, every finding is graded Critical, Important or Minor and gives its file and line, what is wrong, why it matters and the fix.
- [r3] **When** a test was removed or weakened in the commits reviewed, the review lists it, and one the work-item's plan did not list is Important.
- [r4] **When** the implementer reported a setup-only change or a rewrite of a test this initiative wrote, the review checks each against the commits.
- [r5] Behaviour that contradicts a Behaviour line or a capability's Purpose is Important, whether or not a scenario covers it.
- [r6] **If** the branch reviewer cannot verify a check a work-item states, the review fails; a task reviewer lists what it cannot verify from the commits separately.
- [r7] **When** a branch review ends, it reports the suite's wall time and checks the code's shape against `CLAUDE.md` and its coupling to the projects it depends on.
- [r8] **When** the re-review of a fix work-item finds something other than data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, it is triaged as an observation.
- [r9] **Where** the system has a dry run and a real run of one operation, the branch review runs the randomized test that they agree.
- [r10] **If** the commits reviewed change anything under `features/` other than removing a deprecated scenario the work-item lists under Retires, the review grades it Critical.
- [r11] **When** a branch review ends, it reports each deprecated scenario whose replacement's work-item is green, each scenario removed that was not deprecated, and each binding that names no scenario.
- [r12] Each finding names the work-item whose commits contain it and its triage: fix now for a wrong answer, a crash where a refusal belongs or lost data; observation for hardening, with its reproduction; or drop for polish that is not cheap.
- [r13] A task review reads the commits of one work-item and its plan; a branch review reads the initiative branch from its base and every work-item of the initiative.
- [r14] **When** the architecture reviewer finds a refactor to call for, it gives it as an observation with a check that would show it done, and names the work-item it would unblock, if any.

## Implementation, may change
- Opus; a work-item's commits over 8 production or 4 test files are reviewed by area, one reviewer each, in parallel.
- Probes go in the scratch directory the brief names; another revision is checked out as a worktree there.
- `tools check` runs the lint, dead-code and import-contract tools.

## Not yet
- None.
