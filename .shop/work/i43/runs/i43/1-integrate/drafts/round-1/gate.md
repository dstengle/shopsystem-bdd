# Gate, i43 round 1 (request q23)

Drafts: `.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/{supervision,review}.md`. No glossary entry and no decision is drafted.

## supervision (placed after r27)

Added:
- [r154] **When** `work run` starts a branch review, `work run` shall first run, at the initiative branch's head, the whole suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`.
- [r155] **When** `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at.
- [r156] **When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less `.shop/`.
- [r157] **When** `work run` starts a branch review, `work run` shall give the branch reviewer the files to read: the capabilities the work-items are under, the design-decisions those capabilities rest on, and each work-item's plan, implementer's report and review findings.

(Implementation line added: "r155: how a run exited is given as its exit code.")

## review

Added:
- [r32] The branch reviewer shall run nothing: it reads what `work run` gives it and the repository's files, and writes its findings and its result.
- [r33] **When** a branch review finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction.
- [r34] **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall verify from the suite run `work run` gave it that the randomized test that they agree ran, and how many cases it tried.

Removed (id retired, replaced by r34):
- [r9] **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall run the randomized test that they agree.

## Questions

1. supervision#r155, exit code. Reading A (recommended, drafted): "how it exited", with the exit code in Implementation. Reading B: "each run r154 names with its command, exit code and output, naming the commit they ran at."
2. review#r33, the request's **Where**. Reading A (recommended, drafted): **When** a branch review finds a behaviour that only a run would show, ... Reading B: keep **Where** the branch reviewer finds ...
3. review#r12 ("an observation, with its reproduction") against r32/r33. Reading A (recommended): r12 stands; a reproduction is written, not run. Reading B: retire r12, add [r35] "...as an observation, with its reproduction or, in a branch review, the test r33 names, for hardening, ...".
4. review#r7 (the suite's wall time) against r32. Reading A (recommended): r7 stands; the reviewer reads the wall time from the suite run output r155 gives. Reading B: add supervision [r158] "**When** `work run` starts a branch review, `work run` shall give the branch reviewer the wall time of the whole suite's run r154 names."
5. review#r6 (a check the reviewer cannot verify fails a branch review) against r32. Reading A (recommended): r6 stands; the reviewer verifies each check from the run r154/r155 give. Reading B: retire r6, change its branch-review cell to "fail the review where the run of it that `work run` gave shows it did not exit successfully, or `work run` gave no run of it".
6. review Implementation ("Probes go in the scratch directory the brief names"). Reading A (recommended): keep, it covers only the work-item reviewer now. Reading B: reword to "A work-item reviewer's probes go in the scratch directory the brief names; the branch reviewer makes none (r32)."
7. Agent tools: design-decision/the-v3-agents gives `bdd-branch-reviewer` Bash. Reading A (recommended): no change; r32 is held by the brief. Reading B: a new decision superseding the-v3-agents' row and a role-boundaries line giving the branch reviewer no Bash tool, raised as its own request.

## Cut sentences

1: the request's title, a summary of lines 1 to 4.
