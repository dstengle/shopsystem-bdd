/home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md
/home/vscode/shopsystem-bdd/.shop/worktrees/i43-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/review.md

## Change list

### supervision (adds supervision#r154, supervision#r155, supervision#r156, supervision#r157; changes none; removes none)

| op | capability | id | line | from |
|---|---|---|---|---|
| added | supervision | supervision#r154 | **When** `work run` starts a branch review, `work run` shall first run, at the initiative branch's head, the whole suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`. | q23 line 1: "**When** `work run` starts a branch review, `work run` shall first run, at the initiative branch's head, the whole suite, each work-item's scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`, and give the branch reviewer each one's command, exit code and output, naming the commit they ran at." |
| added | supervision | supervision#r155 | **When** `work run` starts a branch review, `work run` shall give the branch reviewer each run r154 names with its command, how it exited and its output, naming the commit they ran at. | q23 line 1 (as above). Line 1 has two responses, running and giving, so it is split into r154 and r155 (one response a line). "exit code" is written as "how it exited", and the exit code goes in Implementation ("r155: how a run exited is given as its exit code"). See question 1. |
| added | supervision | supervision#r156 | **When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less `.shop/`. | q23 line 2: "**When** `work run` starts a branch review, `work run` shall give the branch reviewer the commits from the initiative's base to the branch's head, each with the work-item it belongs to or none, and the change of that range less `.shop/`." ("the initiative's base" uses the glossary's term: the initiative branch's base) |
| added | supervision | supervision#r157 | **When** `work run` starts a branch review, `work run` shall give the branch reviewer the files to read: the capabilities the work-items are under, the design-decisions those capabilities rest on, and each work-item's plan, implementer's report and review findings. | q23 line 3: "**When** `work run` starts a branch review, `work run` shall give the branch reviewer the files to read: the capabilities the work-items are under, the design-decisions those capabilities rest on, and each work-item's plan, implementer's report and review findings." |

Placed directly after r27. Frontmatter unchanged. One Implementation line added (r155).

### review (adds review#r32, review#r33, review#r34; changes none; removes review#r9)

| op | capability | id | line | from |
|---|---|---|---|---|
| added | review | review#r32 | The branch reviewer shall run nothing: it reads what `work run` gives it and the repository's files, and writes its findings and its result. | q23 line 4: "The branch reviewer shall run nothing: it reads what `work run` gives it and the repository's files, and writes its findings and its result." |
| added | review | review#r33 | **When** a branch review finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction. | q23 line 5: "**Where** the branch reviewer finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction." (A finding is an event, not an option or configuration, so the line is event-driven and uses **When** where the request has **Where**. See question 2.) |
| added | review | review#r34 | **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall verify from the suite run `work run` gave it that the randomized test that they agree ran, and how many cases it tried. | q23 line 6: "**Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall verify from the suite run `work run` gave it that the randomized test that they agree ran, and how many cases it tried." |
| removed | review | review#r9 | **Where** the system reviewed has a dry-run mode and a real mode of one operation, the branch reviewer shall run the randomized test that they agree. | Replaced by q23 line 6 (a different rule, so the id is retired and r34 is added). |

Frontmatter: `retired: [r9]`.

### Glossary

No term added, changed or removed.

## Decision files

None.

## Questions

1. supervision#r155: the request says to give "each one's command, exit code and output", but the format puts an exit code in Implementation. Reading A, as drafted: the line says "how it exited", and Implementation says "r155: how a run exited is given as its exit code". Reading B: keep the request's words, "`work run` shall give the branch reviewer each run r154 names with its command, exit code and output, naming the commit they ran at." This is defensible because here the exit code is data handed to the reviewer, not `work run`'s own exit.
2. review#r33: the request writes line 5 with **Where**. Reading A, as drafted: "**When** a branch review finds a behaviour that only a run would show, the branch reviewer shall give it as a finding ...". Reading B: keep the request's **Where**: "**Where** the branch reviewer finds a behaviour that only a run would show, the branch reviewer shall give it as a finding with the test that would show it, marked not run, in place of a reproduction."
3. review#r12 against review#r32 and review#r33: r12 asks for every observation "with its reproduction". Reading A: r12 stands unchanged; a reproduction is written, not run, and r33 covers only what a run alone would show. Reading B: change r12 (new id, r12 retired): "[r35] The reviewer shall triage each finding, naming the work-item whose commits contain it, as fix now for a wrong answer, a crash where a refusal belongs or lost data, as an observation, with its reproduction or, in a branch review, the test r33 names, for hardening, or as drop for polish that is not cheap."
4. review#r7 against review#r32: r7 has the branch reviewer write "the suite's wall time", which it can no longer measure itself. Reading A: r7 stands; the reviewer reads the wall time from the suite run's output that supervision#r155 gives it. Reading B: add to supervision "[r158] **When** `work run` starts a branch review, `work run` shall give the branch reviewer the wall time of the whole suite's run r154 names." Then r7 stands as it is.
5. review#r6 against review#r32: a branch review fails on "a check a work-item names that the reviewer cannot verify". Reading A: r6 stands; the reviewer verifies each check from the run of it that supervision#r154 and r155 give. Reading B: change r6's branch-review cell (new id, r6 retired) to "in a branch review, fail the review where the run of it that `work run` gave shows it did not exit successfully, or `work run` gave no run of it".
6. review Implementation against review#r32: "Probes go in the scratch directory the brief names" implies a reviewer runs probes. Reading A: keep it as it is, since it now covers only the work-item reviewer. Reading B: reword it to "A work-item reviewer's probes go in the scratch directory the brief names; the branch reviewer makes none (r32)." This is not an accepted line, so it is left unedited pending the answer.
7. Agent tools against review#r32: design-decision/the-v3-agents gives `bdd-branch-reviewer` Bash. Can a tool list hold "run nothing" (role-boundaries)? Reading A: no change; r32 is held by the reviewer's brief. Reading B: a new decision superseding design-decision/the-v3-agents's row, and a role-boundaries line "[r<next>] The plugin's agent definitions shall give the branch reviewer no Bash tool." That would be raised as its own request, since q23 does not give it.

## Cut sentences

- Title: "A branch review that runs nothing: work run gives it every run and the change". This is a summary of lines 1 to 4, which already carry it.
