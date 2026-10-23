---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/review
title: Review
narrator: the script `work run`, closing a work-item or an initiative
group: guarantees
rests_on: [design-decision/review-of-work-items, design-decision/the-v3-agents, design-decision/worker-results-are-files, design-decision/workflow-capabilities-are-guarantees]
retired: []
---

# Review

## Purpose
Finds defects in one work-item's commits or in an initiative branch as a whole, against the work-item's plan, the
spec and the repository's rules, and triages them. The reviewers are `bdd-task-reviewer` and `bdd-branch-reviewer`,
started by `work run`, and, when the person asks, `architecture-reviewer`. A reviewer changes nothing: what is to be
fixed now becomes a fix work-item, and the rest an observation.

## Behaviour
- [r1] **When** a review ends, the reviewer shall leave its findings in the findings file and the result its brief names, and the working tree, index, HEAD and branches as they were.
- [r13] The reviewer shall read, for a work-item review, the commits of one work-item and its plan, and for a branch review, the initiative branch from its base and every work-item of the initiative.
- [r2] The work-item and branch reviewers shall grade every finding Critical, Important or Minor.
- **When** a work-item or branch review finds one of the following in what it reads, the reviewer shall do what the row says:

  | id | found | the reviewer shall |
  |---|---|---|
  | [r10] | a change under `features/` other than removing a deprecated scenario the work-item lists under Retires | grade it Critical |
  | [r3] | a test removed or weakened | list it, graded Important where the work-item's plan did not list it |
  | [r4] | a setup-only change, or a rewrite of a test this initiative wrote, that the implementer named in its report | verify each against the commits |
  | [r5] | behaviour that contradicts a Behaviour line or a capability's Purpose, whether or not a scenario covers it | grade it Important |
  | [r6] | a check a work-item names that the reviewer cannot verify | in a branch review, fail the review; in a work-item review, list what it cannot verify from the commits separately |
  | [r11] | in a branch review, a deprecated scenario whose replacement's work-item is `green`, a scenario removed that was not deprecated, or a binding that names no scenario | write each in its findings |
  | [r29] | code whose observable behaviour, such as an output, a file written, a status or a refusal, no Behaviour line asks for | grade it Important |

- [r12] The reviewer shall triage each finding, naming the work-item whose commits contain it, as fix now for a wrong answer, a crash where a refusal belongs or lost data, as an observation, with its reproduction, for hardening, or as drop for polish that is not cheap.
- [r30] **When** a work-item or branch review, a re-review included, finds code whose observable behaviour no Behaviour line asks for, the reviewer shall triage it as fix now, the fix being its line written first or the code removed, whatever r8 and r12 would make it.
- [r8] **When** the re-review of a fix work-item finds something other than data left invalid, the system's own fault on input, or a write that lands where a refusal belongs, the reviewer shall triage it as an observation.
- [r7] **When** a branch review ends, the branch reviewer shall write in its findings the suite's wall time, the code's shape against `CLAUDE.md` and its coupling to the projects it depends on.
- [r9] **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall run the randomized test that they agree.
- [r14] **When** the architecture reviewer finds a refactor to call for, the architecture reviewer shall give it as an observation with a check that would show it complete, naming the work-item it would unblock, if any.
- [r28] **If** a reviewer cannot do what its input asks, then the reviewer shall stop, saying why, and change nothing.

## Implementation, may change
- Opus; `work run` starts one `bdd-task-reviewer` for a work-item, however many files its commits touch.
- Probes go in the scratch directory the brief names; another revision is read with `git show`, not checked out.
- `tools check` runs the lint, dead-code and import-contract tools.
- A finding gives its file and line, what is wrong, why it matters and the fix.

## Not yet
- None.
