---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-terms-analysis
kind: review-finding
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-21
---

# Term analysis of spec/ and the glossary draft, release 0.21.0

The whole-context term analysis of spec/ (2026-10-21, release 0.21.0) by a dispatched agent, and the glossary draft
made from it for the person's release gate. The agent could not write findings.md (the harness refused a subagent's
report file), so the coordinator saved its findings; the prompt and the agent's summary are taken word for word from
its session transcript (session 172b8519).

The answers: the person, 2026-10-21, "input" covers what a session starts with (input data such as a brief, or an
input prompt filled from a template); the glossary draft became card 2 of the release gate, approved with every card
(2026-10-21). It led to eb1432a (the approved entries in spec/index.md), 507c23b (every capability's lines in the one
meanings), 9fd8e36 (scenarios and step definitions following), 283485e; then 8116471 (worker no longer avoids "job";
"findings mode" confirmed, the person). Coordinator's ledger:
initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-migration-release-ledger, lines 161-166.

Archived from git-ignored scratch; each file's text as it was.

## `/tmp/archive-tools/terms-analysis-exchange.md`

~~~~~~
### 2026-10-21T14:02:56, the coordinator to the agent

Whole-context term analysis of /home/vscode/shopsystem-bdd/spec/ (spec/index.md with its Glossary, spec/capabilities/*.md; read features/*.feature only to see how a term is used in scenarios; read no code, skills or agents). Write your findings to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-terms/findings.md. Change no other file.

Find the frequent terms (count occurrences across the Behaviour lines and Implementation sections) that are NOT glossary entries and are used in more than one sense, or are near-synonyms for one thing. For each: the term, its count, each sense with 2-3 quoted line ids (capability#rN), and a proposed resolution (one glossary entry with its definition and Not: words, and the replacement word for the other senses). Order by how much confusion the term can cause an implementing agent.

Must cover, in detail:
- "run": count every sense (e.g. `work run` the command; a run of work run; a worker's session; running tests or the suite; a run directory; `migrate run`; fixture runs; "re-runs"; "can run" = is able to execute). Propose one meaning for the bare word "run" and words for each other sense.
- "brief" vs the text a skill or session hands an agent: the person's view is that "brief" is the file `work run` writes for a worker's stage, a skill is standing, and what a skill hands an agent is ephemeral — the candidate words are "template" (the standing text in a skill) and "prompt" (the ephemeral text an agent starts with). Check these against every use.
- Also check: session, worker, agent, stage, result, report, check, suite, scenario vs test, file set vs fileset vs claim, initiative branch, move, status, gate, review/reviewer, round, record, and any others you find frequent and ambiguous.
- The glossary's stale entries (batch, controller, slice, suite record, hand-back): which are still used and where.
Reply in at most 10 lines: the top terms with their sense counts.

### 2026-10-21T14:11:56, the agent's reply (handback)

I could not write findings.md. The harness refused the Write call ("Subagents should return findings as text, not write report files"), so the full findings are below for you to save to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-terms/findings.md. No file was changed. I removed the empty directory I had made.

Summary (top terms, counted over Behaviour + Implementation lines):
1. run: 143 hits, 10 senses. Invoke a command 46, `work run` 38, `migrate run` 17, run tests 12, "can run" 9, run directory 8, a worker's session 5, a mode in operation 5, a time span 2, the label `run` 1. Proposal: bare "run" = execute a command or test; run directory → "stage directory".
2. status 27 / result 26 / done 25 / green 13: one tangled lifecycle cluster. The `done` status means "before review", `DONE` is a worker's outcome, the glossary's "done" means accepted, and `green` is an undeclared status. Proposal: status, outcome and result as three separate entries.
3. brief 17 / prompt 4 / template 0: your split holds for every `work run` use. It breaks in 3 spec-side places (formulation#impl2, spec-migration#impl3 → template; review#r28 → brief or prompt) and the role-boundaries Purpose. The features and supervision#impl3 also disagree on where brief.md lives.
4. check: 65 hits, 7 senses. A work-item's check vs `work run`'s pre-merge check vs `model check`. red-green#r1 and #r3 use two of them three lines apart.
5. session 16 / worker 19 / agent 19 / dispatch 26: one kind of thing under four words. Read literally, role-boundaries#r1 forbids `work run` starting workers.
6. file set / claim: the glossary contradicts supervision#r19, red-green#r17 and supervision#r20. Then report (27 hits, 6 senses), test/suite, stage (code-research#r6 uses it for another sense), move, review/task, record, round, gate.
7. Stale glossary entries: batch (44, measurement only), controller (1), slice (15), suite record (2, plus a live use at supervision.feature:28 that no spec line backs), hand-back (live; its "logged" wording is stale, and planning#r8 and review#r28 use it for a different stop).
~~~~~~

## `.shop/scratch/drafts/2026-10-21-terms/findings.md`

~~~~~~
# Term analysis of spec/, 2026-10-21

Scope: spec/index.md (Glossary, State, Purpose, Testing) and every spec/capabilities/*.md. Feature files were read only for how scenarios use a term. Counts are whole-word, case-insensitive, inflections as noted, over the Behaviour lines (table rows included) and the `Implementation, may change` bullets of all 17 capabilities. B = Behaviour, I = Implementation. Line ids are capability#rN; Implementation bullets are capability#impl<k> (the k-th bullet). Code spans are counted, since an implementing agent reads them too.

Two model-check consequences apply to every proposal below:
- v_t3: a word one term lists after `Not:` must not be another term. Where two proposed terms are near-synonyms (brief/prompt, worker/session), neither can list the other, so the definitions have to keep them apart.
- v_t1: an avoided word is flagged in requirements and scenarios outside code spans. features/supervision.feature writes `work run` bare 24 times (its Narrator line included), so no term can list "run" as `Not:` until those are code-spanned.

Order: how much confusion the term can cause an agent implementing a line.

## 1. run: 143 (B 110, I 33), ten senses
Counted: run, runs, running, ran, re-runs.
a. Invoke a command or script ("`X` is run", "shall run `model check`", "runs `pytest`"): 46. analysis-tools#r3, design-model-check#r13, spec-consistency#r1, delivery#impl1, spec-integration#impl3.
b. `work run`, the command's name: 38. supervision#r1, delivery#r4, red-green#r1.
c. `migrate run`, a subcommand's name (and a bare `run` for it): 17. migration-tools#r1, migration-tools#r6, spec-migration#impl2 ("asks the context path before `run`").
d. Execute tests, scenarios, the suite or a probe: 12. analysis-tools#r8 ("run the suite once"), code-research#r4 ("from a run of it"), code-research#r9, red-green#impl1 ("run one scenario red"), review#r9, spec-migration#r1 ("the suite does not run cleanly").
e. Be able to execute, or be alive as a process: 9. formulation#r13 ("Where `model check` can run"), spec-integration#r16, formulation#impl5 ("cannot run"), analysis-tools#impl10 ("re-runs itself"), design-model-check#r55 ("shall run again"), delivery#r5 ("While `work run` runs").
f. Run directory, a stage's directory under runs/: 8. supervision#r6, supervision#r15, supervision#impl3, code-research#impl1 (also `.shop/scratch/<run>/`), planning#impl1.
g. A worker's or dispatch's session, its execution: 5. red-green#r16 ("end every run with a result"), batch-measurement#r14 ("the implementer running when it was made", "while more than one ran"), batch-measurement#impl4.
h. A skill, mode or operation in operation: 5. spec-consistency#r4 ("the check runs in report mode"), spec-consistency#r11 ("shall run only when the person asks"), supervision#r20 ("shall run them [work-items] at the same time"), review#r9 ("a dry run and a real run of one operation").
i. A time span: 2. batch-measurement#r1 ("the batch running from the commit"), batch-measurement#impl10 ("the batch ran in").
j. An evidence label in notes: 1. code-research#impl3 ("marked `run`").

Outside the count:
- index Testing: "fixture runs", "outside the default run" (which means outside the suite), the directory .shop/records/measurements/fixture-runs/.
- Purposes: "run by the session" (delivery), "run in a `initiative-round`" (formulation), both sense h.
- role-boundaries narrator: "the person running the workflow".
- Features: "When the agent runs ..." (a), "a second run" (a), "the scenario never runs" (d), "each worker ran in a worktree" (g), "an implementer dispatch running from 10:00 to 10:30" (g), "the batch runs from commit A to commit B" (i).

Why it matters:
- In supervision, `work run` (b), the run directory (f) and "shall run them at the same time" (h) share lines.
- red-green#r16's "every run" (g) reads as one invocation of `work run` (b). That ends with an exit code, not a result.
- In spec-migration#r1, "does not run cleanly" (d) leaves open whether a failing suite or a crashing one stops migration.

Proposal: the bare word keeps senses a and d as one meaning, with no `Not:` list (because of v_t1 above).
- **run**: to execute a command, script, test, scenario or probe until it exits.
- b: always the code span `work run`, never bare "work run". Today it is bare 24 times in supervision.feature, in the supervision narrator and in index Composition. One invocation is "a delivery by `work run`", never "a run".
- c: always `migrate run`; the bare `run` in spec-migration#impl2 becomes `migrate run`. Rename candidate: `migrate apply`, beside `migrate status` and `migrate plan`.
- e:
  - formulation#r13, spec-integration#r16: "Where `model check` is available".
  - analysis-tools#impl8: "does not start".
  - analysis-tools#impl10: "re-executes itself under it".
  - design-model-check#r55: "shall try again, once".
  - delivery#r5: "Until `work run` exits".
- f: **stage directory** (its path already ends `<k>-<stage>/`). `.shop/scratch/<run>/` becomes `.shop/scratch/<stage directory>/`. The runs/ path segment may stay as code.
- g: "session" for a worker (red-green#r16: "end every session with a result"). In measurement, "dispatch ... active" (batch-measurement#r14: "the implementer dispatch active when it was made ... while more than one was active").
- h:
  - spec-consistency#r4: "Where the check is in report mode".
  - spec-consistency#r11: "shall start only when the person asks".
  - supervision#r20: "shall have both implemented at the same time".
  - review#r9: "a dry-run mode and a real mode".
- i: "spanning" or "the batch's window from ... to ..." (the feature already says "window").
- j: the label `probed`, beside `read`.
- index Testing: "fixture runs" → "fixture sessions" (formulation#impl1 already says that); "outside the default run" → "outside the suite".

## 2. The lifecycle cluster: status, result, done/DONE, green
status 27 (B 19, I 8); result 26 (B 19, I 7); done/DONE 25 (B 23, I 2); green 13 (B 8, I 5). None is a glossary entry, and the glossary's work-item says "done when the scenarios it accepts or its check pass".

status, six senses:
- A work-item's lifecycle status: work-queue#r4, work-queue#r6, supervision#r3, delivery#r6.
- The value of a worker's result: code-research#impl4 ("The result's status is `DONE`"), planning#r5, red-green#r16.
- A decision's or proposal's status: design-model-check#r14, design-model-check#r16, migration-tools#r2.
- A dispatch reply's closing word: batch-measurement#r31.
- Exit status: design-model-check#r11, design-model-check#r33, analysis-tools#impl14.
- Command names `migrate status` and `git status`: spec-migration#r15, spec-integration#impl2.

result, four senses:
- The file result.json: supervision#r2, code-research#r1, review#r1.
- Its value: red-green#r7 ("return the result `HAND-BACK`"), supervision#r5 ("gives any result but `DONE`"), planning#r6.
- A holder of fields ("the result's file set"): code-research#r10, supervision#r15.
- An edit's output: feature-file-tools#impl2 ("An edit's result is checked").

done, five senses:
- The work-item status `done`, which means implemented but not yet reviewed. supervision#r2 starts bdd-task-reviewer on a `done` work-item, and the features' lifecycle runs "... claimed, done and green" (supervision.feature:51 and :167).
- The outcome `DONE`: supervision#r3, supervision#r4, supervision#r16.
- "reports a work-item done", meaning it gives `DONE`: red-green#r1.
- Plain English for finished: spec-migration#r4 and #r22 ("When migration is done", in ten lines), spec-consistency#r9, design-model-check#r36 ("an initiative may be done").
- A work-item visibly complete: the glossary's work-item and slice entries, review#r14 ("a check that would show it done").

green, three senses:
- A passing scenario: red-green#r5, formulation#r4.
- A commit with every scenario passing: red-green#r9, red-green#r37.
- The work-item status after review, `green`: review#r11 ("whose replacement's work-item is green"), supervision#impl5 ("Exit 0 every work-item green"), supervision.feature:16 and :51. No capability line names `green` as a status.

Why it matters: an agent implementing `work run` has to tell four things apart: a work-item that is `done` (waiting for review), one whose worker gave `DONE`, the glossary's "done" (accepted), and `green`. And "status" names both the work-item's value and the result's value, which sit in neighbouring files of one stage directory.

Proposal:
- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter. Not: state.
- **outcome**: the one word a worker's result gives: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION` or `NEEDS_CONTEXT`. Not: verdict.
  - "result status", "the result `X`" and "gives any result but `DONE`" become "outcome": "stop with the outcome `NEEDS_CONTEXT`", "gives any outcome but `DONE`".
  - batch-measurement#r31: "the closing outcome its reply states".
- **result**: the file a worker writes in its stage directory, result.json, giving its outcome, its summary and the files it names. Not: result file (the term already means a file), return.
  - feature-file-tools#impl2: "An edit's output".
- Exit status becomes "exit code" everywhere: design-model-check#r11 and #r33, and the three "Exit status:" bullets.
- `done` and `green` appear only as code spans, for the statuses. Plain "done" becomes "complete" or "finished" (the ten spec-migration lines: "When migration is complete"). red-green#r1: "When the implementer's outcome is `DONE`".
- The glossary's work-item becomes "... accepted when its review finds nothing to fix now and its status is `green`" (or whatever the last status is), not "done when the scenarios ... pass".
- List the lifecycle's statuses in one place in spec/: drafted, researched, planned, ready, claimed, done, green, awaiting-ruling, withdrawn. Today they can only be pieced together from supervision#r2, supervision#impl4, design-model-check#impl7 and the features.

## 3. brief vs prompt vs template: 17 / 4 / 0
brief 17 (B 10, I 7); prompt 4 (B 3, I 1); template 0. The person's split: **brief** = the file `work run` writes for a worker's stage; **template** = the standing text in a skill; **prompt** = the ephemeral text an agent starts with.

Every use, checked against that split:

Fits:
- code-research#r1 (the result file its brief names), code-research#r12, red-green#r15 (cannot do what its brief asks), planning#r1, red-green#r18, red-green#impl5, review#impl2.
- supervision#r2 ("brief file", where "file" is redundant), supervision#r16, supervision#r17, supervision#impl3 (brief.md).
- supervision#impl2, `claude -p "<brief path>"`: the prompt is the brief's path. supervision.feature:25 agrees: "a prompt naming its brief file".
- review#r1 fits for bdd-task-reviewer. But review#r1 also covers architecture-reviewer, which the person starts and which gets no brief.

Does not fit:
- review#r28 ("If a reviewer cannot do what its brief asks") also covers architecture-reviewer → "its brief or prompt".
- formulation#impl2 ("with the brief in the skill") → template.
- spec-migration#impl3 ("drafts with the migration brief") → template (the text in migrating-to-capabilities).
- batch-measurement#impl3: "prompt" fits, but "a ledger's task brief" is the superpowers ledger's file, which `work run` does not write → "the ledger's task file".
- role-boundaries Purpose (not counted): "whatever a brief asks". initiative-round, capability-writer and feature-formulator get prompts, not briefs → "whatever its prompt or brief asks".

Prompt uses, all fitting: batch-measurement#r12, #r17, #r34 (each message is one prompt).

Gains a word: spec-integration#impl1 describes initiative-round's prompt (the job, the note path, the drafts path, the round number) without naming it → "dispatches `initiative-round` with a prompt giving the job ...".

So the split holds for every `work run` use; the cases that break it are spec-side dispatches. A location conflict needs settling alongside it: supervision#impl3 puts brief.md in the stage directory under .shop/work/.../runs/, but supervision.feature:26-27 says the brief and result file are under .shop/scratch/ in the worker's worktree.

Proposal (v_t3 forbids listing either term under the other):
- **brief**: the file brief.md that `work run` writes in a stage directory for one worker, naming its work-item, the files to read, its worktree and its result. Not: instructions, task file.
- **prompt**: the text an agent session starts with. A worker's is its brief's path; a dispatch's is the message its dispatcher sends. Not: message.
- **template**: standing text in a skill or agent definition from which a session fills a prompt. Not: boilerplate.
- supervision#r2: "brief file" → "brief".

## 4. check: 65 (B 46, I 19), seven senses
Counted: check, checks, checked, checking (including `checking-spec-consistency` 13 times).
- `model check`, about 26: design-model-check#r1, formulation#r13, migration-tools#r6.
- `tools check`, about 7: analysis-tools#r16, analysis-tools#r17, review#impl3.
- The `--check` flag of `model decisions`: design-model-check#r15, design-model-check#r37.
- One consistency check (one use of the skill): spec-consistency#r1, #r2, #r4.
- A work-item's check, the command whose pass shows its work complete: red-green#r3 ("the work-item's check passes before any work is done"), review#r6 ("a check a work-item states"), review#r14, the glossary's work-item and slice entries.
- `work run`'s check, the whole suite before a merge: red-green#r1 ("leaving the whole suite to `work run`'s check").
- To verify: review#r4 ("check each against the commits"), formulation#impl2, spec-integration#impl2, role-boundaries#impl1. Also "checked out" (review#impl2) and "a check failed" (feature-file-tools#impl11).

Why it matters: red-green#r1 and red-green#r3 sit three lines apart and use "check" for two different gates on the same work-item. "The work-item's check" is undefined: no line says where a work-item states it or how it is run.

Proposal:
- **check**: a command a work-item names in place of scenarios, whose exit 0 shows the work is complete (for guarantees and refactors). Not: criterion.
- red-green#r1 → "leaving the whole suite to `work run`, which runs it before it merges".
- spec-consistency: one use of the skill becomes "a consistency review" or "consistency pass".
- The verb becomes "verify" or "compare".
- `model check`, `tools check` and `--check` appear only in code spans.
- A line is needed (in work-queue or supervision) for where a work-item states its check. Today it appears only in work-queue's Not yet ("`--check` work-items").

## 5. session / worker / agent / dispatch: four words for one kind of thing
session 16 (B 7, I 9); worker 19 (B 17, I 2); agent 19 (B 11, I 8); dispatch 26 (B 15, I 11).

session, five senses:
- The person's own conversation: spec-integration#r10 ("the session that brainstormed the note", "a new session"), spec-integration#impl1, formulation#impl2, spec-migration#impl2.
- A worker's `claude -p` process: supervision#r2, supervision#r8 (the session id), supervision#impl3 (session.json).
- A transcript directory that measure reads: batch-measurement#impl1, batch-measurement#r11.
- A fixture test's `claude -p`: formulation#impl1 ("fixture sessions").
- Narrators: "a session measuring a closed batch", "an agent or session editing feature files".

worker has one sense, the `claude -p` session `work run` starts for one stage: supervision#r1, supervision#r11, supervision#impl2, delivery#r5.

agent, four senses:
- An agent definition: role-boundaries#r1-r6, planning#impl1, spec-consistency#impl1.
- The role a worker is started as: supervision#r2 ("that stage's agent"), supervision#r8, supervision#r12.
- A live, started instance: role-boundaries#r1 ("start another agent"), spec-integration#impl2 ("sends back an agent").
- A measure figure: batch-measurement#impl7 ("agent minutes").

dispatch: a subagent started by a session's Agent tool, as verb and noun (formulation#impl2, spec-consistency#r2, spec-consistency#r3); in measurement, one subagent transcript (batch-measurement#r9, batch-measurement#r34).

Role-name synonyms on top of these:
- researcher = code-scout = scout: code-research narrator, role-boundaries#r2, role-boundaries#r5, batch-measurement#r34.
- supervisor = `work run`: four narrators and index Purpose; it appears 0 times in Behaviour lines.
- "spec writers" (role-boundaries#r5) = capability-writer + feature-formulator.

Why it matters:
- A worker is not a dispatch (no Agent tool, a process of its own), so measure's dispatch counting misses every worker. batch-measurement's Not yet says as much; the words do not.
- role-boundaries#r1 ("only `initiative-round` start another agent") reads as forbidding `work run` from starting workers, unless "agent" means a dispatch.

Proposal:
- **session**: one Claude Code conversation with its own id and transcript: the person's session, a worker, a dispatch or a fixture session. Not: conversation, chat.
- **worker**: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent. Not: job.
- **dispatch**: a session another session starts with its Agent tool, and the transcript it leaves. Not: subagent.
- **agent**: a definition under agents/ (name, model, tools, skills) that a worker or a dispatch is started as. Not: persona.
- Line changes:
  - role-boundaries#r1 → "shall let only `initiative-round` dispatch".
  - spec-integration#impl2 → "sends back a dispatch".
  - Narrators: "the supervisor" → "`work run`".
  - Use "researcher" in prose: role-boundaries#r2, role-boundaries#r5 and batch-measurement#r34 change.

## 6. file set / claim / claimed: glossary entries that contradict their use
file set 6 (B 6), fileset 0, claim/claims/claimed 7 (B 6, I 1). Both are glossary entries. Claim: "the file set a claimed work-item has to itself". File set: "the paths a work-item's work changes, found by its researcher and made final by its planner".

Uses:
- The researcher's list: code-research#r1, code-research#r10.
- The planner's final list: planning#r5.
- A file set the work-item already has when drafted and that is given to the researcher: supervision#r19; supervision.feature:355 ("w1 is drafted, its file set scripts/thing.py ...").
- The overlap test between ready work-items: supervision#r20, which tests file sets, not claims.
- claim as the act of adding one file: red-green#r17 ("claim it with `work claim`"), red-green#r37.
- claim as the set held: red-green#r37 ("the work-item whose claim has it"). The feature also uses "claims" as a verb: "a glob or a directory in a file set claims each tracked file it holds" (supervision.feature:375).
- `claimed` as the status: red-green#r3, spec-migration#r1, supervision#impl4.

Contradictions:
- The glossary's file set is found by the researcher, but supervision#r19 hands the researcher one.
- The glossary's claim *is* the file set, but red-green#r17 grows the claim beyond the "final" file set.
- supervision#r20 tests overlap on file sets, so a file added by `work claim` falls outside the overlap test.
- File sets may hold globs or directories, but only the feature says so.

Proposal:
- **file set**: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
- **claim**: the tracked files a `claimed` work-item holds: those its file set covers plus any added with `work claim`. No other claimed work-item's claim shares a file. Not: lock, reservation.
- supervision#r20 → "two ready work-items whose claims would not share a file". The verb "claims" in the feature → "covers".

## 7. report: 27 (B 21, I 6), six senses
Counted: report, reports, reported.
- The implementer's report file: red-green#r6, red-green#r9, red-green#impl3, supervision#impl3.
- A script prints a finding: design-model-check#r12, feature-file-tools#r25, migration-tools#r6, analysis-tools#r16.
- A mode: spec-consistency#r4 ("report mode").
- Giving the outcome `DONE`: red-green#r1 ("reports a work-item done").
- A reviewer writing into its findings: review#r7, review#r11.
- Telling the person: spec-migration#r6, spec-consistency#r9.

Why it matters: red-green#r1 ("reports ... done") and red-green#r6, #r9 and #r10 ("in its report") are in one capability. The first is the result's outcome; the others are a separate file. Nothing says where the report lives: supervision#impl3 only lists "report" among the stage directory's files.

Proposal:
- **report**: the implementer's file in its stage directory, beside its result, naming the files it will touch, the tests whose setup it changed and its open questions. Not: write-up.
- Scripts "print". Reviewers "write in the findings". The person is "shown" or "told".
- red-green#r1 → "When the implementer's outcome is `DONE`".
- spec-consistency's "report mode" → "findings mode", beside "fix mode".

## 8. scenario / test / suite
scenario 134 (B 102, I 32); test(s) 64 (B 39, I 25); suite 14 (B 9, I 5).

test, five senses:
- A pytest test: analysis-tools#r9, red-green#r5, planning#r3.
- A test file as a class of path: code-research#r10, batch-measurement#r14, analysis-tools#impl12.
- The test binding a scenario: spec-migration#r18, feature-file-tools#impl10.
- "the tests" as the command `work run` runs: supervision#r5 ("its work fails the tests"), supervision#impl6.
- A legacy record, "test log": migration-tools#r9.

Near-synonym: "the work-item's tests" (supervision#impl1) and "the work-item's scenarios" (supervision#r4, red-green#impl1) name one command.

suite, four senses:
- Everything `python3 -m pytest` runs by default: supervision#r4, red-green#r1, review#r7.
- "the fast suite" (analysis-tools#impl7): the same thing under a second name.
- The set of feature-file scenarios: formulation#r4 ("keep the old scenario in the suite").
- "suite record", which is stale (§17).

Proposal:
- **suite**: every test `python3 -m pytest` runs from the root by default, fixture scenarios excluded. Not: fast suite, default run, test run. (Note: "default run" contains "run"; check this against v_t1 before adopting it.)
- Consider an entry for **scenario**: a Gherkin scenario in features/<capability>.feature, passing when the one test that binds it passes. Not: test case.
- supervision#impl1: "the work-item's tests" → "the work-item's scenarios".
- supervision#r5: "fails the tests" → "fails its scenarios or the suite".
- formulation#r4: "in the suite" → "in its feature file".

## 9. stage: 8 (B 5, I 3), two senses, and its overlap with status
- One worker's part of a work-item's delivery (research, plan, implementation, review): supervision#r2, supervision#r8, supervision#r14, planning#impl1.
- A step of the system under change: code-research#r6 ("a work-item adds a path that skips a stage ... every refusal and effect only that stage produces").

The stage names (supervision#r1: research, plan, implementation, review) and the statuses that start them (supervision#r2: drafted, researched, ready, done) are two vocabularies for one sequence. "plan" is a stage, while `planned` is a status that moves to `ready` with no worker (supervision#impl4).

Proposal:
- **stage**: one of research, plan, implementation and review, done by one worker and started by `work run` from the work-item's status (`drafted`, `researched`, `ready`, `done`). Not: phase.
- code-research#r6 → "a path that skips a step of today's processing ... every refusal and effect only that step produces".

## 10. move: 45 (B 32, I 13), four senses
- A work-item's status change: work-queue#r4, work-queue#r6, supervision#r3, supervision#r9.
- `features move`, a scenario moved between files: feature-file-tools#r12, feature-file-tools#r14, spec-migration#impl3.
- `git mv` by migrate: migration-tools#r1, migration-tools#r5, migration-tools#impl2.
- The mechanical migration commit: spec-migration#r22, spec-migration#r26, spec-migration#impl5.

Proposal: **move**: one change of a work-item's status, written by `work` and logged in log.jsonl. Not: transition. `features move` stays a code span. migrate's moves become "relocate with git". spec-migration's "mechanical move" becomes "mechanical commit".

## 11. review / reviewer / task: 15 / 20 / 15
review, five senses:
- Task review, of one work-item's commits: review#r13, review#r6.
- Branch review, of the initiative branch: review#r7, review#r11.
- Re-review of a fix work-item: review#r8.
- The stage: supervision#r1.
- The old controller's branch review: batch-measurement#r34.

reviewer means any of three agents in review#r1 and review#r28, but two of them in review#r2.

task, two senses: a work-item, in "task review" (review#r2, review#r13, bdd-task-reviewer); an entry in an old plan's ledger (batch-measurement#r16, #r29, #impl3).

Proposal:
- **review**: a reviewer's reading of commits against the plan, the spec and the repository's rules, written as graded findings: a work-item review, a branch review or an architecture review. Not: audit.
- In prose, "task review" → "work-item review"; the agent keeps its name.
- Measurement's "task" → "ledger task".

## 12. record: 25 (B 22, I 3), four senses
- A design-model record node: design-model-check#r29, migration-tools#r12, spec-integration#r21.
- The .shop/records/ path: design-model-check#r19, migration-tools#r8, spec-migration#r15.
- "suite record": batch-measurement#r16, batch-measurement#impl7 (stale, §17).
- To write down: batch-measurement#r32, spec-consistency#r10, the glossary's ruling ("recorded with `work rule`"), index Testing.

Proposal: **record**: a file under .shop/records/ whose frontmatter id has a record kind. Not: log entry. Verb uses become "write" or "give" (batch-measurement#r32: "shall give the plugin and harness versions").

## 13. round: 13 (B 4, I 9), four senses
- The agent initiative-round: role-boundaries#r1, role-boundaries#r5.
- One numbered dispatch of it for one job: spec-integration#impl1, spec-integration#r4 ("a further round"), formulation#impl5.
- The whole integration or formulation: spec-consistency#r11 ("never in an integration or formulation round").
- The directory round-<n>/: spec-integration#impl1, spec-integration#impl3.

Proposal: **round**: one dispatch of initiative-round for one job, numbered under its drafts path. Not: pass, iteration. spec-consistency#r11 → "never during an integration or a formulation".

## 14. gate: 15 (B 13, I 2), two senses
- The one human approval, of Behaviour lines: index Purpose, spec-integration#r19, formulation#r14, spec-consistency#r5.
- Migration's stop, where the person also answers retitles, slices, the context path and glossary bullets: spec-migration#r2, spec-migration#r10, spec-migration#r17.

The second contradicts index Purpose ("One human gate, on the spec's Behaviour lines").

Proposal: **gate**: the person's approval of Behaviour lines and glossary entries before they are committed to spec/, together with the questions they raise. Not: sign-off.

## 15. initiative branch / base / work-item branch
- initiative branch: 4 uses (review#r13, supervision#r4, supervision#r7, supervision#impl3).
- Its start appears as "its base" (review#r13), "the initiative's base" (red-green#r6) and "the initiative's base commit" (supervision.feature:28). `--base` in analysis-tools#r16 is any git ref.
- The work-item's branch: red-green#r7, supervision#r18, red-green#r18, and work/w1 in the features only.
- Nowhere is it defined which branch is checked out in the person's repository, or where the initiative branch comes from.

Proposal: **initiative branch**: the branch `work run` commits each move on and merges each work-item's branch into; its base is the commit it started from. Not: integration branch. Use "work-item branch" for work/<work-item>.

## 16. Lower-risk overloads
- **line**, 120 (B 79, I 41):
  - About 64 mean a Behaviour line: formulation#r1, spec-integration#r12, spec-migration#r9.
  - About 46 mean a text line: tag line, log line, `path:line`, "Lands line", "Then line".
  - The glossary's requirement is "one Behaviour line". design-model-check says "requirement"; formulation and spec-integration say "line".
  - Proposal: "Behaviour line" in full, "requirement" for the unit with an id, and bare "line" only for a text line.
- **plan**, 34:
  - Senses: the work-item's plan.md (planning#r1, red-green#r11); the stage "plan" (supervision#r1); the legacy living plan or batch plan (batch-measurement#r2, #r16, spec-migration#r17); `migrate plan` (spec-migration#impl2).
  - Proposal: plan = the planner's plan.md; the legacy ones are always qualified.
- **path**, 49:
  - Senses: a file path; a code path (code-research#r11, analysis-tools#impl7); a process path (formulation#r14 "small-change path", spec-consistency#r7 "question path"); a context path (design-model-check#r43).
  - migrate writes the context path as a bare `<path>` (migration-tools#r1, #r4, #r12).
  - Proposal: `<path>` → `<context path>`; a process path becomes a "route".
- **context**, 42:
  - Senses: bounded context; the model's context (red-green#impl5, batch-measurement#r34 "starting context", NEEDS_CONTEXT); a coverage context (analysis-tools#r8); a decision's Context section (spec-integration#impl4).
  - Proposal: "bounded context" in full; "context window" for the model's.
- **note/notes**, 29:
  - Senses: the researcher's notes.md (code-research); a brainstorming note (spec-integration#r1, #r2, #r10); a note in the facts (batch-measurement#r29); design notes (migration-tools#r9).
- **step**, 18:
  - Senses: a Gherkin step or step definition (feature-file-tools#r13, spec-migration#r7); a fix-mode step (spec-consistency#r9); the legacy 'step <k>' (batch-measurement#impl3); `work step` (supervision Not yet).

## 17. Stale glossary entries: batch, controller, slice, suite record, hand-back
batch ("the slices one session plans and one controller executes"):
- Spec: 44 uses, all in batch-measurement (`measure batch` and the concept, r1-r34, impl1-10), plus index Purpose ("what a batch cost"), Testing and the Composition narrator.
- Features: 148 in batch-measurement.feature; 11 in design-model-check.feature (example glossary data only).
- No capability makes a batch now; i12 replaces it with an initiative's delivery.

controller ("the session that dispatches implementers and reviewers for a batch"):
- Spec: 1, batch-measurement#r11. Also the decision name design-decision/controller-per-spec-round in the rests_on of formulation and spec-integration.
- Features: 3 in batch-measurement.feature (lines 103-108).
- No live meaning. What dispatches spec rounds is "the session"; what starts workers is `work run`.

slice ("a unit of work with an observable done; to become a work-item (i4)"):
- Spec: 15. batch-measurement#r12, #r15, #r19, #impl3, #impl6, #impl7, #impl8. Also spec-migration#r16 and #r17, where open slices of a living plan are legitimate old-system input.
- Features: 46 in batch-measurement.feature; 14 in design-model-check.feature (example data); 16 in feature-file-tools.feature (slice-1 tag names in fixtures, harmless).
- The i4 clause is done.

suite record ("a whole-suite result logged once ..."):
- Spec: 2, batch-measurement#r16 and batch-measurement#impl7, plus its Purpose.
- Features: 4 in batch-measurement.feature; 1 in design-model-check.feature (example data).
- Live: supervision.feature:28, "the implementer's brief also names ... the suite record work run made". No supervision line backs it, so either a line is missing or the scenario step is stale.

hand-back ("an implementer's stop on an observed condition, logged with its evidence"):
- Spec: 10. The live `HAND-BACK` outcome: red-green#r3, #r7, #r16, #impl4; formulation#r10 ("handed back").
- planning#r8 and review#r28 use "hand back" for a different stop (`NEEDS_CONTEXT`, or saying why).
- batch-measurement#r16 and #impl7: "the plan's hand-back entries", a legacy log.
- Features: 6 in batch-measurement.feature; 3 in design-model-check.feature (example data).
- The definition's "logged" is stale: a hand-back is now a result outcome, not a plan-log entry.

Proposals:
- Mark batch, controller, slice and suite record as legacy, reworded "(old system) ...". Keep them only while batch-measurement and spec-migration read the old layout, and drop them with i12.
- batch-measurement#r11: controller → "dispatching session".
- Decide supervision.feature:28: either add a supervision line or drop the clause from the scenario.
- **hand-back**: an implementer's stop with the outcome `HAND-BACK`, giving the stop condition and its evidence verbatim. Not: handback. planning#r8 → "shall stop with the outcome `NEEDS_CONTEXT`"; review#r28 → "shall stop, saying why".

Method: a script split each capability into Behaviour lines (table rows included, ### headings excluded) and Implementation bullets, then counted whole-word, case-insensitive regex matches. I sorted all 143 "run" hits into senses by hand; the other terms list representative ids. Feature-file counts are grep -ci per file.
~~~~~~

## `.shop/scratch/drafts/2026-10-21-terms/glossary-draft.md`

~~~~~~
# Proposed glossary (spec/index.md), for the person's gate, 2026-10-21

New or changed entries, in the glossary's form. From the term analysis (findings.md) and the person's
direction: "input" covers what an agent session starts with, structured input data or an input prompt;
a template is standing and needs input.

- **agent**: a definition under `agents/` (its name, model, tools and skills) that a worker or a dispatch is started as. Not: persona.
- **brief**: the input data `work run` writes for one worker in its stage directory, naming the work-item, the files to read, the worktree and where the result goes. Not: task file.
- **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.
- **claim**: the tracked files a `claimed` work-item holds: those its file set covers and any added with `work claim`; no two claims share a file. Not: lock, reservation.
- **delivery**: one invocation of `work run` on an initiative, from its start until it exits.
- **dispatch**: a session another session starts with its Agent tool, and the transcript it leaves. Not: subagent.
- **file set**: the paths, globs or directories a work-item says its work changes: drafted with it, revised by its researcher and fixed by its planner. Not: fileset, scope.
- **gate**: the person's approval of Behaviour lines and glossary entries before they are committed to `spec/`, with the questions they raise. Not: sign-off.
- **hand-back** (changed): an implementer's stop with the outcome `HAND-BACK`, giving the condition and its evidence word for word. Not: handback.
- **initiative branch**: the branch `work run` commits each transition on and merges each work-item branch into; its base is the commit it started from. Not: integration branch.
- **input**: what a session is started with: input data, such as a brief, or an input prompt, the text filled from a template.
- **outcome**: the one word a worker's result gives: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`, `QUESTION` or `NEEDS_CONTEXT`. Not: verdict.
- **record**: a file under `.shop/records/` whose frontmatter id has a record kind. Not: log entry.
- **report**: the implementer's file in its stage directory, beside its result, naming the files it touched, the tests whose setup it changed and its open questions. Not: write-up.
- **result**: the file `result.json` a worker writes in its stage directory, giving its outcome, its summary and the files it names. Not: return.
- **review**: a reviewer's reading of commits against the plan, the spec and the repository's rules, written as graded findings: a work-item review, a branch review or an architecture review. Not: audit.
- **round**: one dispatch of `initiative-round` for one job, numbered under its drafts path. Not: iteration.
- **run**: to execute a command, script, test, scenario or probe until it exits.
- **scenario**: a Gherkin scenario in `features/<capability>.feature`, passing when the one test that binds it passes. Not: test case.
- **session**: one Claude Code conversation with its own id and transcript: the person's, a worker, a dispatch or a fixture session. Not: conversation, chat.
- **stage**: one of research, plan, implementation and review, done by one worker and started by `work run` from the work-item's status. Not: phase.
- **stage directory**: the directory `runs/<work-item>/<k>-<stage>/` that holds one stage's brief, result, report and session. Not: run directory.
- **status**: a node's place in its kind's lifecycle (a work-item's, a capability-proposal's, a decision's), written in its frontmatter; a work-item's are `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`, `green`, `awaiting-ruling` and `withdrawn`. Not: state.
- **suite**: every test `python3 -m pytest` runs from the root by default, fixture scenarios excluded. Not: fast suite.
- **template**: standing text in a skill or an agent definition that a session fills with input to start another session. Not: boilerplate.
- **transition**: one change of a work-item's status, written by `work` and logged in `log.jsonl`. Not: move.
- **worker**: a session `work run` starts with `claude -p` for one stage of one work-item, as that stage's agent. Not: job.

Removed: **slice** (slicing is gone; the i4 clause is done). Marked "(old system, until i12)": **batch**, **controller**, **suite record**.

Rewording that follows (one meaning per word, EARS kept, scenarios' steps and their step definitions following):
`work run` always in code; "run directory" → stage directory; the outcome `DONE` against the status `done`;
plain "done" → "complete"; exit status → exit code; "the work-item's check" defined where a work-item states it;
"check" as a verb → "verify"; spec-side "brief" → template or input; role-boundaries r1 → "only `initiative-round`
dispatches"; review/branch/work-item review; "move" → transition for a work-item's status; migrate's moves → "relocate with git"; spec-migration's mechanical move → the mechanical commit; and the two inconsistencies:
where `brief.md` lives (supervision's Implementation against its feature), and supervision.feature's suite record
that no line backs.
~~~~~~
