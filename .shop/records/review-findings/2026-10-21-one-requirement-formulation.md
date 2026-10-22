---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-one-requirement-formulation
kind: review-finding
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/supervision, capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue, capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check, capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools, capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement, capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools]
date: 2026-10-22
---

# Formulation questions: one requirement per scenario, exits in words, a failed work-item (release 0.22.0)

The blind feature-formulator's questions in the formulation round for decisions 0054 (a scenario names one
requirement), 0055 (exits are successful or errors) and 0056 (a failed work-item), release 0.22.0 (begun as 0.21.1),
2026-10-21 to 2026-10-22: round 1 (Q1-Q14), round 2 (A-E), round 3 (one question). The exchange below is taken word
for word from the formulator's session transcript (session 172b8519): the coordinator's brief and answers, every
version of reply.md the formulator wrote (the file was overwritten each round), and its hand-backs; the last section is
reply.md as it is now. The seven whole feature drafts are the folder
initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-one-requirement-formulation-drafts. The
coordinator's ledger is initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-release-ledger-snapshot.

| questions | answer | lines it led to |
|---|---|---|
| Q1 (r14 vs delivery.toml) | a delivery.toml list replaces r14's limit (r30) | rows in the drafts |
| Q2 (r22 and the whole suite), Q3 (every worker's branch) | every pytest run; every worker has a worktree and branch | rows in the drafts |
| Q4, Q5 (git failure after claim; .shop/work commit) | the person's fault design, 2026-10-22 | cd42cd6: supervision r33-r41 (r34 worker changes .shop/work -> failed, r40, r41 git failure -> failed), work-queue r8 `work retry`, glossary `failed`, decision 0056 |
| Q6-Q8 | open = no ruling yet; nested run under r10; `work add` existing under r7 | rows in the drafts |
| Q9-Q11, Q14 | a scenario shows only its own line's response (0054); strip the rest | steps stripped in the drafts |
| Q12, Q13 | drop "bad usage"; keep contradicted scenarios @deprecated | the drafts |
| A (`work retry` from claimed) | to ready | row in work-queue r8's outline |
| B, C, E | observe through other commands; r6 and r34 both hold; strip Implementation text | the drafts |
| D (r28 vs 0056) | r28 goes to failed | 6bff977: supervision r28 -> failed (decision 0056) |
| round 3 ("in one line") | strip it from supervision r10, r21 too | the drafts |

The person also made, from this round, five lessons for the capability format and the spec-checker (ledger
2026-10-22).

Archived from git-ignored scratch; each file's text as it was.

## `/tmp/archive-tools/one-requirement-exchange.md`

~~~~~~
### 2026-10-21T22:08:39, the coordinator to the agent

Formulation round for 0.21.1 of /home/vscode/shopsystem-bdd (branch release-0.21.1). Two rules now hold (read spec/decisions/0054-a-scenario-names-one-requirement.md and spec/decisions/0055-exits-are-successful-or-errors.md): a scenario names exactly ONE requirement by one @r<n> tag and shows that requirement's own response; a scenario says a command "exits successfully" or "exits with an error", never an exit code. Formulate only from the capability files' Behaviour lines under spec/capabilities/ (and the glossary in spec/index.md); keep each existing scenario's title and steps where they already fit their one line.

Write whole revised feature files to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/ (same file names as features/), and reply.md there with, per file, what you changed and every question:
1. supervision.feature and work-queue.feature: formulate both afresh from their capability files, one scenario (or Scenario Outline) per requirement — they were written by their implementers, not formulated, so don't trust their current text; reuse their step wording where it fits a line.
2. Every other features/*.feature: split each scenario that carries more than one @r<n> tag into one scenario per requirement, each showing its own line's response; and change every step that names an exit code (e.g. "it exits 0", "exits 1", "exit status 2") to "it exits successfully" or "it exits with an error" as its line says.
A line with two readings is a question in reply.md, never decided in a scenario.

### 2026-10-21T22:20:26, the agent writes reply.md

# Formulation round 2026-10-21: one requirement per scenario (0054), exits in words (0055)

Whole revised feature files are in this directory, with the same names as features/. Wherever a step, title,
description or Examples cell named an exit code ("exits 0/1/2/3", "non-zero", "exit status 1", "the exit code"),
it now says "exits successfully" or "exits with an error". Titles that changed are listed below as old -> new, because
their bindings must follow (`features rebind`).

## Coverage

| file | lines | each line has a scenario | multi-tag scenarios left |
|---|---|---|---|
| supervision | r1-r32 | yes, all 32 (r21-r31 are new) | none |
| work-queue | r1-r7 | yes | none |
| design-model-check | 47 lines | yes; r106 and r107 had none and have one now | none (the old @r20 several-tags scenario is now `@r20 @deprecated`) |
| migration-tools | r1-r17 | yes | none |
| batch-measurement | 23 lines | yes | none |
| analysis-tools | 17 lines | yes | none |
| feature-file-tools | 25 lines | yes | none |

Supervision, line by line: r1 1, r2 2, r3 1, r4 3, r5 3, r6 4, r7 1, r8 1, r9 1, r32 2, r10 2, r11 1, r12 1, r13 1,
r14 1, r15 1, r16 1, r17 1, r18 1, r19 1, r20 3, r21 1, r22 1, r23 1, r24 1, r25 1, r26 1, r27 1, r28 1, r29 1,
r30 1, r31 1.
Work-queue: r1 1, r2 1, r3 1, r4 1, r5 1, r6 1, r7 7.

## supervision.feature (formulated again from the capability)
- Split `@r1 @r9`. r1 keeps the title and drops "exits 0". r9 is covered by its own scenario.
- r2: the first scenario keeps only the session and brief steps. The worktree step (Implementation) and the implementer-brief step (now r24 and r25) are gone. New outline: which agent each status starts.
- Old r2 tools outline removed. Its no-tools row is now a row of the r14 outline (researcher's `git commit` refused). Its delivery.toml row becomes the r30 outline (see Q1). The step pinning the exact default `--allowedTools` list is dropped, because no line gives that list.
- Split `@r4 @r5` tests-fail outline:
  - r4: "an implementer's DONE whose <tests> fail is not merged"
  - r5: "an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-ruling with the failure as its question"
- The r4 uncommitted-file scenario keeps only "not merged" (now "does not have feature.txt").
- Steps dropped because they show another line's response:
  - "no worker was started for w1 after ..." (no line says so; see Cases)
  - incidental "w1 is green" in the r5, r6 and r16 scenarios
  - the print step of the Questions-section scenario (now its own r32 scenario)
- r6 implementer-commit outline. Title "... is put back on its branch, the branch is not merged, and the work-item goes to awaiting-ruling naming the file" -> "an implementer's commit <change> under .shop/work/ is put back on its branch". It keeps only the put-back step (Q5).
- r9 title "... `work run` exits 0, ..." -> "... `work run` exits successfully, ...".
- Old r9 "when no work-item can make a transition, `work run` exits, printing ..." -> r32 "when no work-item can make a transition and one is awaiting-ruling, `work run` exits with an error, printing each work-item's status and each open question". New r32: "`work run` prints a work-item's open question and not what follows its Questions section".
- r10 outline: "exits non-zero" -> "exits with an error" in the title and step. Row 2's reason said "last move", a word the glossary avoids (v_t1); it now says "last transition". The program's message must follow.
- r10 git scenario title "... and a non-zero exit code" -> "..., exiting with an error".
- Removed with no replacement:
  - "a delivery's worktrees are removed when `work run` exits, whatever the implementer's work came to: <end>" (`@r4 @r5 @r10`; no line says worktrees are removed)
  - "a failure of git after the work-item was claimed makes its transition to awaiting-ruling with the failure as its question" (`@r5 @r10`; Q4)
- Old second r11 scenario -> @r23: "when the repository is inside the plugin's own directory, the workers' worktrees are outside it". Its green and worktree-removal steps are dropped.
- New: r21, r22, r24, r25, r26, r27, r28, r29, r30, r31.

## work-queue.feature (formulated again from the capability)
- Split `@r2 @r7`. "add when the work-item's file already exists leaves the file as it was and fails" -> "add when the work-item's file already exists leaves the file as it was" (r2 only). The error exit is not formulated (Q9).
- r7 outline title "... exits non-zero ..." -> "... exits with an error ...". Every "exits non-zero" step -> "exits with an error". The other scenarios are unchanged.

## design-model-check.feature
- Titles:
  - "violations are printed by their grammar name and make `model check` exit 1" -> "... exit with an error"
  - "warnings are counted and do not change the exit code" -> "warnings are counted and do not change whether `model check` exits successfully"
  - "file problems are each printed and make `model check` exit 1" -> "... exit with an error"
- r33 outline: the `code` column 0/1 becomes `exit`, successfully / with an error.
- Split `@r16 @r17` "why lists every proposal naming the requirement by date, and fails when none adds or changes it" into:
  - r16: "why lists every proposal naming the requirement by date, each with its status and date" (4 rows, no exit)
  - r17: "why fails when the only proposals naming the requirement remove it" (the 2 error rows; Q11)
- Split `@r5 @r23`. r23 keeps "a merged capability-proposal may add or remove an id its capability lists as retired" (not unresolved). New r5: "a merged capability-proposal adding an id its capability lists as retired is not v15c".
- "a scenario tagged with several requirements names each of them" contradicts r20 and r107 now. It is kept as `@r20 @deprecated`, retitled "... (deprecated)", with `Deprecated for:` the new r107 outline "a scenario with more than one requirement tag, its own and its feature's together, is v_s2" (Q10).
- New r106 outline: "a work-item with no accepts and no check is v_w4, unless it is withdrawn". These r106 and r107 additions go beyond the two operations the brief asked for. Drop them if they are not wanted.

## migration-tools.feature
- "exits non-zero" -> "exits with an error" in steps and titles:
  - "`migrate run` that finds <found> in spec/decisions.md names it, exits non-zero and changes no file, the ledger included"
  - "`migrate run` whose ledger entry's decision file would land on <there> names it, exits non-zero and changes no file"
  - "`migrate run` that cannot make two of its changes names both, exits non-zero and changes no file"
  - "`migrate run` that would relocate a file onto an untracked file names the relocation, exits non-zero and changes no file"
  - "`migrate run` on a repository with <change> refuses, naming it, exits non-zero and changes no file"
  - "`migrate run` that would <what> names it, exits non-zero and changes no file"
  - "`migrate run` outside a git repository says so, exits non-zero and changes no file"
- Split `@r4 @r5` "... the id bounded-context/<path>, and rewrites what names the old id" into:
  - r4: "`migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>"
  - r5: "`migrate run` rewrites a frontmatter id that names the context id it changed"
- Split `@r9 @r5` "... the type-first id, and rewrites what names the old id" into:
  - r9: "`migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id"
  - r5: "`migrate run` rewrites a frontmatter id that names a decision file's old id"

## batch-measurement.feature
- Split `@r2 @r4` "the open batch is named by --name, default open". r2 keeps the title, with the name step only. New r4 outline: "without --out the open batch's facts go under measurements in its name".
- "a refusal says why on stderr and exits 1" -> "a refusal says why on stderr and exits with an error" (its description and step changed too).

## analysis-tools.feature
- Split `@r1 @r3` outline. r1 keeps "the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one" with the path step only. New r3 outline: "probe says whether its interpreter came from --python, the project's virtualenv or neither".
- `@r1 @r17` ".venv whose python links ..." -> @r1. The title is kept. It drops "it says to run `tools install`", which is r17's response and already shown by "without jedi refs says to install it".
- Exit steps changed in words, including "neither ruff nor vulture makes it exit with an error". The `# [r51]` comment now quotes the current line ("exit with an error").

## feature-file-tools.feature
- `@r19 @r46` "deprecating for a new title written over two lines is refused" -> @r46 only. Its response is the refusal; r19 has its own scenarios.
- r51's line now makes `@r<n>` the scenario's one requirement tag, in place of any `@r<m>`. The old scenario (it adds @r7 beside @r1 @r4) contradicts it. It is kept as `@r51 @deprecated`, "tagging with a requirement id adds it to the scenario's requirement tags (deprecated)". The new outline is "tagging with a requirement id makes it the scenario's one requirement tag" (Q14).
- Exit steps changed in words. No titles changed apart from these.

## Questions
1. supervision r14 / r30: does r14's Bash limit still hold when `.shop/delivery.toml` gives a stage's `[allowed_tools]`? The old scenario let a researcher's `Bash(git commit *)` run. The r30 outline uses lists (Read and Grep; Read, Write and Edit) that do not decide this.
2. supervision r22: "every pytest command it starts, and every worker's" gets `--work-item <name>`. Does that include the whole-suite run? `--work-item` would narrow the suite, and Implementation's suite command has no such option. How is a worker's own pytest given it? Only the work-item's-scenarios command is formulated.
3. supervision r25: "a worker's brief" names the initiative branch's base, the worktree and "its work-item branch". Do the researcher, planner and reviewer have a work-item branch? Only the implementer's brief is formulated.
4. supervision r10 / r5: does r10 cover a git failure part-way through a delivery, after a work-item was claimed and transitions were committed, so that "change nothing" cannot hold? Does that work-item go to awaiting-ruling? r5 names only an outcome, a missing result, or failing scenarios or suite. The r10 git scenario is kept without "changes nothing". The awaiting-ruling scenario is removed.
5. supervision r6: an implementer's commit under `.shop/work/` is put back on its branch. The old scenario also said the branch is not merged and the work-item goes to awaiting-ruling naming the file. r28 covers only the main checkout. Which line holds those two, if any?
6. supervision r32: is a question that has a ruling still an "open question"? The scenario shows only that the Rulings section's text is not printed.
7. supervision r21: does a refused nested `work run` exit with an error (r10's reading) or only say so? Not decided.
8. work-queue r2 / r7: does `work add` on an existing work-item exit with an error (r7: it cannot do what it was asked), or succeed and leave the file (r2 alone)? The old scenario said it fails, saying the work-item already exists. Only r2 is formulated.
9. design-model-check r20 / r107: for a scenario with two `@r<n>` tags (a v_s2), does r20 read it as naming one of them, both, or neither, and is thing#r1 then printed under v_s3? The r107 outline checks only v_s2.
10. design-model-check r16 / r17: no line says `model why` exits successfully when a proposal adds or changes the requirement. The old outline pinned exit 0 for those rows. Those rows no longer check the exit.
11. Reading of 0054: many single-tag scenarios end with an exit that belongs to another line:
    - "exits with an error" in the table-row scenarios r9, r49, r52, r53, r54, r61, r103 and r104 is r2's response
    - in feature-file-tools, r57's "exits successfully" is r26's
    - in analysis-tools, r5's and r14's "exits successfully" come from Implementation

    Keep these steps (as drafted) or strip them?
12. feature-file-tools r46: "rejected as bad usage" names the Implementation's exit-2 class. Keep the words?
13. feature-file-tools r51 and design-model-check r20: the replaced scenarios are kept as `@deprecated` with `Deprecated for:`, as the glossary says. Their tests assert the old behaviour and will fail once the new behaviour lands. Should they be deprecated or removed outright?
14. migration-tools r15: the line says refuse and change no file, but not how it exits. The scenario keeps "exits with an error" (r7's reading).

## Cases no line mentions
- supervision: worktrees are removed when `work run` exits. r15 presupposes it, and the old `@r4 @r5 @r10` outline pinned it.
- supervision: no worker is started for an `awaiting-ruling` work-item. r2 lists the statuses that start workers but says nothing of the others.
- supervision: a question is written into the work-item's Questions section. This is kept under r5, but no line names the section.
- supervision: the default `--allowedTools` list of each stage.
- supervision: what `work run` does with the branch reviewer's outcome, and whether r9's exit waits on it. Whether a branch review starts when the delivery ends with a work-item awaiting a ruling.
- work-queue: a transition the lifecycle does not allow is refused (Implementation, under r7). No scenario covers it.
- design-model-check: `model why` succeeding.

### 2026-10-21T22:20:46, the agent's reply (handback)

All seven feature files are revised in full under /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/, with the same names as features/. reply.md beside them has the per-file changes, every old -> new title, the questions and the uncovered cases. No scenario in the drafts carries more than one `@r<n>` tag.

Every exit code is now in words: "exits successfully" or "exits with an error". I also changed "non-zero" and codes in titles, descriptions and Examples cells, and every changed title is listed old -> new in reply.md so the bindings can be rebound. My standing rules say an existing feature file should get only its new and changed scenarios; I followed your brief and wrote whole files.

## Coverage
| file | every line has a scenario | multi-tag scenarios left |
|---|---|---|
| supervision | yes, r1–r32; r21–r31 had none and are new | none |
| work-queue | yes, r1–r7 | none |
| design-model-check | yes; r106 and r107 had none and now have one each | none |
| migration-tools | yes, r1–r17 | none |
| batch-measurement | yes | none |
| analysis-tools | yes | none |
| feature-file-tools | yes | none |

## Things to check
- **Additions beyond the brief:** I added scenarios for r106 (v_w4) and r107 (v_s2) in design-model-check. Drop them if you don't want them.
- **Contradicted scenarios:** two old scenarios now contradict their lines:
  - design-model-check: "a scenario tagged with several requirements names each of them" (against r20 and r107).
  - feature-file-tools: r51 "tagging with a requirement id adds it…" (the line now makes `@r<n>` the scenario's one requirement tag).

  I kept both as `@deprecated` with a `Deprecated for:` line, as the glossary says, and wrote their replacements.
- **Removed from supervision:** two scenarios are gone with no replacement:
  - The worktrees-removed outline: no line says worktrees are removed.
  - The git-failure-to-awaiting-ruling scenario: see question 4.

  I also dropped steps that showed another line's response, such as "no worker was started after…" and incidental "w1 is green".
- **Error text changed:** one supervision reason said "move", a word the glossary avoids, so it would be flagged as v_t1. It now says "transition", so the message `work run` prints must change to match.

## Questions
1. supervision r14 vs r30: does r14's Bash limit still hold when delivery.toml gives a stage's `[allowed_tools]`? The old scenario let a researcher run `git commit`. My r30 outline uses lists that don't decide this.
2. supervision r22: does "every pytest command … and every worker's" include the whole-suite run? The suite command in Implementation has no `--work-item`. And how does a worker's own pytest get the option? I formulated only the work-item's-scenarios command.
3. supervision r25: do the researcher, planner and reviewer have a work-item branch? I formulated only the implementer's brief.
4. supervision r10/r5: does r10 cover a git failure after a work-item was claimed, when "change nothing" can no longer hold? Does that work-item go to awaiting-ruling, which r5 doesn't name?
5. supervision r6: an implementer's commit under `.shop/work/` is put back. Which line, if any, says the branch is then not merged and the work-item goes to awaiting-ruling naming the file? I formulated only the put-back.
6. supervision r32: is a question that already has a ruling still "open"?
7. supervision r21: does a refused nested `work run` exit with an error, or only say so?
8. work-queue r2/r7: does `work add` on an existing work-item exit with an error, or succeed and leave the file? I formulated r2 only.
9. design-model-check r20/r107: does a scenario with two tags name one requirement, both or neither? In other words, is thing#r1 then printed under v_s3?
10. design-model-check r16/r17: no line says `model why` exits successfully when a proposal adds or changes the requirement. Those rows no longer check the exit.
11. Reading of decision 0054: many single-tag scenarios end with an exit that belongs to another line or to Implementation. Examples are the table-row scenarios ending "exits with an error" (that is r2's), feature-file r57's "exits successfully" (r26's), and analysis r5 and r14. Keep these steps, as drafted, or strip them?
12. feature-file-tools r46: "rejected as bad usage" names Implementation's exit-2 case. Keep those words?
13. The deprecated scenarios assert the old behaviour, so their tests will fail once the new behaviour lands. Deprecate them, or remove them outright?
14. migration-tools r15 doesn't say how a refusal exits. The scenario keeps "exits with an error".

## Cases no line mentions
- supervision:
  - Worktrees are removed when `work run` exits (r15 presupposes it).
  - No worker starts for an awaiting-ruling work-item.
  - A question is written into the work-item's Questions section (kept under r5).
  - Each stage's default `--allowedTools` list.
  - What happens with the branch reviewer's outcome.
  - Whether a branch review starts when a work-item is still awaiting a ruling.
- work-queue: a transition the lifecycle forbids is refused. Implementation puts it under r7, but no scenario covers it.
- design-model-check: `model why` succeeding.

Files are in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/:
- reply.md
- supervision.feature
- work-queue.feature
- design-model-check.feature
- migration-tools.feature
- batch-measurement.feature
- analysis-tools.feature
- feature-file-tools.feature

### 2026-10-22T14:33:49, the coordinator to the agent

The coordinator sent a message while you were working:
Answers to your 14 questions and new lines (commit cd42cd6; re-read spec/capabilities/supervision.md, work-queue.md, spec/index.md's glossary and spec/decisions/0056-a-failed-work-item.md). Answers: Q1 a delivery.toml list replaces r14's limit for its stage (r30); Q2 r22 covers every pytest run work run starts, the whole suite included, and a worker's own pytest; Q3 every worker has a worktree and a work-item branch, so r25 holds for every worker's brief; Q4, Q5 now have lines: r34 (worker changes .shop/work/ → failed), r41 (git failure during a stage → failed), r40 (exit with an error on failed); Q6 open = no ruling yet; Q7 a refused nested run falls under r10 (exits with an error); Q8 `work add` on an existing work-item falls under r7 (refused, with an error); Q9 and Q10: don't assert what another line says; Q11 decision 0054: a scenario shows only its own line's response — strip steps that show another line's (the trailing exits included); Q12 drop "bad usage"; Q13 keep the two contradicted scenarios @deprecated (the work-item that greens their replacements retires them); Q14 strip, per Q11. Your r106 and r107 scenarios stay. New lines to formulate in your drafts: supervision r33 (worktrees removed on exit), r34, r35 (verify push before a worker starts), r36 (questions under ## Questions), r37 (no worker while awaiting-ruling or failed), r38 (push after every commit), r39, r40, r41; work-queue r8 (`work retry`). Update the whole files in your drafts folder and reply.md; reply in at most 5 lines.

Address this before completing your current task.

### 2026-10-22T14:43:35, the agent writes reply.md

# Formulation round 2026-10-21/22: one requirement per scenario (0054), exits in words (0055), a failed work-item (0056)

Every revised feature file is here in full, with the same names as features/. Round 2 takes in the coordinator's answers to
round 1's Q1-Q14 and the new lines (commit cd42cd6). Any title that changed is listed as old -> new, because its binding
must follow it (`features rebind`). Under Q11, a scenario now shows only its own line's response. Steps that showed another
line's response are gone, trailing exits included.

## Coverage

| file | every line has a scenario | multi-tag scenarios left |
|---|---|---|
| supervision | yes, r1-r41 (41 lines) | none |
| work-queue | yes, r1-r8 | none |
| design-model-check | yes, r106 and r107 included | none (`@r20 @deprecated` kept) |
| migration-tools | yes, r1-r17 | none |
| batch-measurement | yes | none |
| analysis-tools | yes | none |
| feature-file-tools | yes | none (`@r51 @deprecated` kept) |

Supervision scenarios per line:

| line | scenarios | line | scenarios | line | scenarios | line | scenarios |
|---|---|---|---|---|---|---|---|
| r1 | 1 | r10 | 1 | r19 | 1 | r28 | 1 |
| r2 | 2 | r11 | 1 | r20 | 3 | r29 | 1 |
| r3 | 1 | r12 | 1 | r21 | 1 | r30 | 1 |
| r4 | 3 | r13 | 1 | r22 | 2 | r31 | 1 |
| r5 | 2 | r14 | 1 | r23 | 1 | r33 | 1 |
| r6 | 4 | r15 | 1 | r24 | 1 | r34 | 1 |
| r7 | 1 | r16 | 1 | r25 | 1 | r35 | 1 |
| r8 | 1 | r17 | 1 | r26 | 1 | r36 | 1 |
| r9 | 1 | r18 | 1 | r27 | 1 | r37 | 2 |
| r32 | 2 | | | | | r38-r41 | 1 each |

Work-queue: r1 to r6 have 1 each, r7 has 8 and r8 has 1.

## supervision.feature

### Background
The Background now also gives "a remote the initiative branch can be pushed to", which r35 and r38 need.

### Removed or replaced
- Split `@r1 @r9`.
- Old r2 tools outline is removed. Its rows went to r14 (the researcher's `git commit` refused, with no tools in delivery.toml) and to r30.
- Old r10 git-failure scenario is removed. Its case is now the r41 row "the merge".
- Old `@r5 @r10` scenario (awaiting-ruling on a git failure) is removed. r41 replaces it.

### Split `@r4 @r5` (tests fail)
- r4: "an implementer's DONE whose <tests> fail is not merged"
- r5: "an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-ruling with the failure as its question"

### r6 implementer-commit outline
- Old title: "... is put back on its branch, the branch is not merged, and the work-item goes to awaiting-ruling naming the file".
- New title: "an implementer's commit <change> under .shop/work/ is put back on its branch".
- The failed half is now r34.
- The first r6 scenario no longer sets w1's status or checks log.jsonl, because r34 now makes that work-item failed.

### Retagged or retitled
- Questions-section scenario: was @r5, is now @r36. Title: "a question goes into the work-item's ## Questions, before a section that follows it".
- r9 title: "exits 0" -> "exits successfully".
- Old r9 (open question) is now r32: "when no work-item can make a transition and one is awaiting-ruling, `work run` exits with an error, printing each work-item's status and each open question".
- New r32 scenario: "`work run` prints a question that has no ruling yet, and not one that has a ruling" (Q6).
- r10 outline title: "exits non-zero" -> "exits with an error". New row: started by a worker of another `work run` (Q7). Row 2's reason now says "last transition", not "last move".
- r21 now shows only that `work run` refuses and says so.
- Old second r11 scenario is now @r23: "when the repository is inside the plugin's own directory, the workers' worktrees are outside it".
- r30 outline gains the row "Read and Bash(git commit *)" (Q1).
- r25 now names every worker's brief (Q3).
- r22 is two scenarios (Q2): every pytest command `work run` starts, the whole suite's included, and a worker's own pytest.

### Steps stripped (another line's response)
- "w1 is green" from r16 and the r20 scenarios
- the worktree-gone step from r15
- "has the implementer's commit" from r18
- "w1 is awaiting-ruling" from r26

### New scenarios
- r33: the worktrees outline. Its old title was "a delivery's worktrees are removed when `work run` exits, ...". New title: "every worktree `work run` made is removed when it exits, whatever the implementer's work came to: <end>".
- r34, r35, r37 (two scenarios), r38, r39, r40 and r41.

## work-queue.feature
- r2 keeps "add when the work-item's file already exists leaves the file as it was".
- New r7: "add when the work-item's file already exists is refused, saying so, with an error" (Q8).
- New r8 outline: `work retry` returns a failed work-item to drafted, researched or done (Q-A below).
- "exits non-zero" -> "exits with an error".

## design-model-check.feature
These changes are from round 1:
- "violations are printed by their grammar name and make `model check` exit 1" -> "... exit with an error"
- "warnings are counted and do not change the exit code" -> "warnings are counted and do not change whether `model check` exits successfully"
- "file problems are each printed and make `model check` exit 1" -> "... exit with an error"
- The r33 outline's exit column is now in words.
- Split `@r16 @r17`:
  - r16: "why lists every proposal naming the requirement by date, each with its status and date"
  - r17: "why fails when the only proposals naming the requirement remove it"
- Split `@r5 @r23`:
  - new r5: "a merged capability-proposal adding an id its capability lists as retired is not v15c"
  - r23 keeps its title
- `@r20 @deprecated` "a scenario tagged with several requirements names each of them (deprecated)".
- New r107 and r106 outlines.

These changes are from round 2 (Q11):
- Trailing exits stripped from r9, r49, r52, r53, r54, r55 (both scenarios), r61, r103 and r104.
- "prints no file problem" stripped from r36's withdrawn scenario.
- r3's table-row scenario is down to "it prints no v15a". Its file-problem and v_s3 steps are gone.
- "v_e2 does not name r2" moved from r103 to r104, as a new line r6 in r104's table.

## migration-tools.feature
These changes are from round 1:
- "exits non-zero" -> "exits with an error" in the steps and in these titles:
  - "`migrate run` that finds <found> in spec/decisions.md names it, ... and changes no file, the ledger included"
  - "`migrate run` whose ledger entry's decision file would land on <there> names it, ..."
  - "`migrate run` that cannot make two of its changes names both, ..."
  - "`migrate run` that would relocate a file onto an untracked file names the relocation, ..."
  - "`migrate run` that would <what> names it, ..."
  - "`migrate run` outside a git repository says so, ..."
- Split `@r4 @r5`:
  - r4: "`migrate run` gives spec/index.md whose id is bounded-context/shop the id bounded-context/<path>"
  - r5: "`migrate run` rewrites a frontmatter id that names the context id it changed"
- Split `@r9 @r5`:
  - r9: "`migrate run` gives a decision file whose id is decision/<nnnn>-<name> the type-first id"
  - r5: "`migrate run` rewrites a frontmatter id that names a decision file's old id"

These changes are from round 2:
- r15 title: "... refuses, naming it, exits non-zero and changes no file" -> "`migrate run` on a repository with <change> refuses, naming it, and changes no file". Its exit step is gone (Q14).
- Steps stripped:
  - the summary step from r11
  - the id step from r13
  - the id and status steps from the r5 numbered-entry scenario
  - the relocation step from the r5 symbolic-link scenario
- r16: "`model decisions --check` says ... is current" -> "spec/decisions/index.md is what `model decisions` would write".

## batch-measurement.feature
- Split `@r2 @r4`:
  - r2 keeps "the open batch is named by --name, default open"
  - new r4: "without --out the open batch's facts go under measurements in its name"
- "a refusal says why on stderr and exits 1" -> "a refusal says why on stderr and exits with an error".

## analysis-tools.feature
- Split `@r1 @r3`:
  - r1 keeps its title
  - new r3: "probe says whether its interpreter came from --python, the project's virtualenv or neither"
- `@r1 @r17` .venv scenario is now @r1 only.
- "install with every tool present says so and succeeds" -> "install with every tool present says so". Its exit step is gone.
- r14's refs outline: the exit step is gone.
- Every other exit is now in words.

## feature-file-tools.feature
- "retagging with a tag that is not a requirement tag is bad usage" -> "... is refused". The step no longer says "as bad usage" (Q12).
- `@r19 @r46` is now @r46 only.
- r51's old scenario is kept as `@deprecated`. The new outline is "tagging with a requirement id makes it the scenario's one requirement tag".
- r57 now shows only that neither scenario is printed as bound by no test. Its r26 response and exit are stripped.
- The r58 "looks only at the feature files it names" scenario now shows that neither "Old rule" nor "Older rule" is printed.

## Questions
- A. work-queue r8: "the status it had before the failed stage". Take an implementation stage that started at `ready` and failed after the work-item's transition to `claimed`. Does `work retry` return it to `ready` or to `claimed`? The outline has only drafted, researched and done, where the answer is clear.
- B. Reading lines (design-model-check r19, r20, r21, r43; analysis-tools r1): their response can only be seen through another command's output, such as v_s3, unresolved, facts, or a refusal. I kept those observation steps. If they also count as another line's response, these lines have no scenario that can see them.
- C. supervision r34 and r6 have the same condition. So a researcher that changes `.shop/work/` is put back (r6) and also makes the work-item failed (r34). Is that the intent for a change the worker did not commit, as with the researcher's?
- D. supervision r28 (main checkout differs -> awaiting-ruling) vs decision 0056 ("a fault outside the work-item's work -> failed, never awaiting-ruling"). Does r28 still send the work-item to awaiting-ruling?
- E. batch-measurement r1 "a written batch is reported in one line", r29's "writes the note on stderr", and analysis-tools r5 "install says each tool it installed" pin Implementation text, not their own line's. Keep them?

## Cases no line mentions
- A `work retry` on a work-item that is not failed.
- `model why` succeeding.
- What `work run` does with the branch reviewer's outcome.

### 2026-10-22T14:43:41, the agent's reply (handback)

Drafts redone with your answers and the new lines: supervision r33–r41, work-queue r8; 0054 applied to all files (another line's steps, exits included, stripped); r106, r107 and the two @deprecated scenarios kept.
Every line has a scenario and none has two `@r` tags; I added a row r6 to r104's lines table so the check moved from r103 ("v_e2 does not name r2") still has a line to check. Title changes for rebinding are in reply.md.
New questions (reply.md A–E): `work retry` after a failure from `claimed` — `ready` or `claimed`? Do r19/r20/r21/r43 and analysis r1 keep observing through other commands' output? A researcher's `.shop/work/` change is put back and fails the work-item (r6 and r34 together) — intended? Does r28 still go to awaiting-ruling, given 0056? Keep steps that pin Implementation text (batch r1, r29; analysis r5)?
Untouched: batch-measurement keeps its round-1 draft; it had no exits that belonged to another line.
Files in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/: reply.md and the seven feature files.

### 2026-10-22T14:44:00, the coordinator to the agent

The coordinator sent a message while you were working:
Answers to A–E: A) `work retry` returns a work-item failed from `claimed` to `ready`, the status before that stage started (work-queue r8's "before the failed stage"). B) yes, keep observing through other commands' output where that is what the narrator sees. C) yes, intended: r6 puts the file back and r34 fails the work-item; each scenario shows its own line's response only. D) r28 now transitions to `failed` (commit 32 lines up: re-read supervision r28; decision 0056). E) strip steps that pin Implementation text. Update the drafts and reply.md; reply in 2 lines.

Address this before completing your current task.

### 2026-10-22T14:51:52, the agent writes reply.md

# Formulation round 2026-10-21/22: one requirement per scenario (0054), exits in words (0055), a failed work-item (0056)

Every feature file here is the whole revised file, under the same name as in features/. This is round 3: it takes in the coordinator's answers A–E. The answers to round 1's Q1–Q14 and the new lines (cd42cd6, then r28 -> failed) were already taken in.

Two rules hold in every file:
- A scenario shows only its own line's response. Steps that show another line's response are gone, exits included.
- A scenario pins no Implementation text (E). Where a line can only be seen through another command's output, the scenario still observes it that way (B).

Every title that changed is listed below as old -> new, so its binding can follow (`features rebind`).

## Coverage

| file | every line has a scenario | multi-tag scenarios left |
|---|---|---|
| supervision | yes, r1-r41 | none |
| work-queue | yes, r1-r8 | none |
| design-model-check | yes, r106 and r107 included | none; `@r20 @deprecated` is kept |
| migration-tools | yes, r1-r17 | none |
| batch-measurement | yes | none |
| analysis-tools | yes | none |
| feature-file-tools | yes | none; `@r51 @deprecated` is kept |

## Round 3 changes

### supervision.feature
- **r28 (D):** "... and the work-item goes to awaiting-ruling naming the file" -> "a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file". The step is now "w1 is failed, naming .shop/work/i1/initiative.md".
- **Implementation text stripped (E):**
  - r7: the commit messages.
  - r31: the commit message. The step now reads "the commit of w1's transition to planned".
  - r29: "it ran no `python3 -m pytest`".
  - r15: the stage-directory path. The step now reads "w1's implementation stage directory".
  - r5: the row "its questions the string "Why so?"".
  - r2: the brief's directory. The step now reads "where the worker's result goes".
  - r19: `--max-turns 25`. The step now reads "a limit of 25 turns".
  - r33: `.shop/worktrees/w1`.

### work-queue.feature
- **r8 (A):** the outline gains the row "failed from claimed -> ready". It is now titled "retry returns a failed work-item to the status it had before the failed stage: failed from <from>".
- **r7:** "says why in one line" -> "says why". This changes the title "a command that cannot be done exits with an error, says why in one line and changes nothing" -> "... says why and changes nothing", and the steps.

### design-model-check.feature
- **Removed (Implementation only):**
  - "`model check` ends with the four counts"
  - "rows of a violated relation are limited, saying how many more there are"
- **r1:** the step is now "it says it found no violation, unresolved reference or file problem". It no longer pins the counts.
- **r14 titles and steps:**
  - "writing the decisions index names the file and leaves out decisions with no id" -> "writing the decisions index leaves out decisions with no id". It no longer says which file was written.
  - The no-decision scenario's step is now "spec/decisions/index.md is written with its header and no row".

### migration-tools.feature
- **r17:** "... the qualifier going to by after the source, <case>" -> "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, <case>". The step is now "its by has the qualifier "(for artifacts)"". It no longer pins the exact `by` format.

### batch-measurement.feature
- **Removed:**
  - "a written batch is reported in one line" (r1)
  - "show prints the header, the tables, the exceptions, the hand-backs and the notes" (r18)
- **r19:** "compare prints both files' figures with the ratio of the second to the first" now shows only each figure, in total and per slice, with the ratio.
- **r29:** the step "writes the note on stderr" is gone.
- **r38:** the steps "says to name the living plan with --plan" and "says to give the batch's start with --from" are gone.

### analysis-tools.feature
- **Removed:**
  - "install with every tool present says so"
  - "install says each tool it installed"
  - "a tool that prints nothing is shown clean"
- **Retitled:**
  - "tests-of without a map says to make one" -> "tests-of without a map is refused"
  - "untested without a map says to make one" -> "untested without a map is refused"
  - "without coverage tests-of and untested say to install it" -> "without coverage tests-of and untested name it as missing"
  - "without jedi refs says to install it" -> "without jedi refs names it as missing"
  - "`tools check` names a missing tool under its heading" -> "`tools check` names a missing tool". The r17 scenarios now end "it exits with an error", which is r17's own response.
  - "install outside a virtualenv explains each missing tool and installs nothing" -> "install outside a virtualenv says so for each missing tool and installs nothing"
  - "untested prints each function with its place, the count and the commit" -> "untested prints each function, the count and the commit"
  - "`tools check` with no file to examine says so under ruff and vulture and does not fail for them" -> "`tools check` with no file to examine does not fail for ruff and vulture"
- **Other steps:**
  - r8's map outline drops the line pytest printed, where the map is, and the commit.
  - The import-linter scenario keeps only "import-linter is not run".
  - r49 drops "in one line".
  - r3's probe steps are worded as the line words them.
  - The r1 .venv scenario now observes "tools names jedi as missing" (B).

### feature-file-tools.feature
- **Removed:**
  - "deprecating a scenario prints its file and new title"
  - "a tag is found with or without its leading @"
- **r28:** "rebinding rewrites each binding of the old title and counts them" -> "rebinding rewrites each binding of the old title". The count step is gone.
- **r29:** the multi-line scenario no longer names the module and line.
- **r2:** "an edit is refused only when it would leave a Rule: block outside a docstring" -> "an edit is refused when it would leave a Rule: block outside a docstring". The row with two same-titled scenarios is gone.
- **r58:** the no-call scenario no longer pins "no test binds it".

## Rounds 1 and 2 (still in the drafts)
- **Exits:** every exit is in words. "exits non-zero" and the exit codes are gone from steps, titles and Examples.
- **Multi-tag splits:**
  - supervision `@r1 @r9` and `@r4 @r5`
  - work-queue `@r2 @r7`
  - design-model-check `@r16 @r17` and `@r5 @r23`
  - migration-tools `@r4 @r5` and `@r9 @r5`
  - batch-measurement `@r2 @r4`
  - analysis-tools `@r1 @r3` and `@r1 @r17`
  - feature-file-tools `@r19 @r46`
- **Deprecated, with replacements:** design-model-check r20 (several tags) -> r107. feature-file-tools r51 -> its new outline.
- **New:**
  - supervision r21-r41
  - work-queue r7 (existing file refused) and r8
  - design-model-check r106 and r107
- **Stripped:** the exits and steps that belong to another line (Q11).

## Questions
1. "in one line": no line says it. work-queue and analysis-tools no longer say it, but supervision r10 and r21 still do ("says in one line"). Strip it there too?

## Cases no line mentions
- A `work retry` on a work-item that is not failed.
- `model why` succeeding.
- What `work run` does with the branch reviewer's outcome.

### 2026-10-22T14:51:56, the agent's reply (handback)

All seven feature files and reply.md are updated in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/ with A–E: r28 now goes to `failed`, retry from `claimed` returns to `ready`, and steps pinning Implementation text are stripped; nine Implementation-only scenarios were removed and their lines keep other scenarios.
One question: no line says "in one line" and I stripped it from work-queue and analysis, but supervision r10 and r21 still say it — strip there too? Retitled scenarios are listed old -> new in reply.md for rebinding.

### 2026-10-22T14:52:05, the coordinator to the agent

The coordinator sent a message while you were working:
Yes, strip "in one line" from supervision r10 and r21 too (no line says it). Finish and reply in one line.

Address this before completing your current task.

### 2026-10-22T14:53:46, the agent writes reply.md

# Formulation round 2026-10-21/22: one requirement per scenario (0054), exits in words (0055), a failed work-item (0056)

Every feature file here is the whole revised file, under the same name as in features/. This is round 3: it takes in the coordinator's answers A–E, and the answer that "in one line" goes everywhere. The answers to round 1's Q1–Q14 and the new lines (cd42cd6, then r28 -> failed) were already taken in.

Two rules hold in every file:
- A scenario shows only its own line's response. Steps that show another line's response are gone, exits included.
- A scenario pins no Implementation text (E). Where a line can only be seen through another command's output, the scenario still observes it that way (B).

Every title that changed is listed below as old -> new, so its binding can follow (`features rebind`).

## Coverage

| file | every line has a scenario | multi-tag scenarios left |
|---|---|---|
| supervision | yes, r1-r41 | none |
| work-queue | yes, r1-r8 | none |
| design-model-check | yes, r106 and r107 included | none; `@r20 @deprecated` is kept |
| migration-tools | yes, r1-r17 | none |
| batch-measurement | yes | none |
| analysis-tools | yes | none |
| feature-file-tools | yes | none; `@r51 @deprecated` is kept |

## Round 3 changes

### supervision.feature
- **r28 (D):** "... and the work-item goes to awaiting-ruling naming the file" -> "a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file". The step is now "w1 is failed, naming .shop/work/i1/initiative.md".
- **r10 and r21: "in one line" stripped.**
  - r10's title: "`work run` that cannot do what it was asked exits with an error, says why in one line, and changes nothing" -> "`work run` that cannot do what it was asked exits with an error, says why, and changes nothing". Its step is now "work says that <reason>".
  - r21's step is now "`work run` refuses, saying that it was started by a worker of another `work run`".
- **Implementation text stripped (E):**
  - r7: the commit messages.
  - r31: the commit message. The step now reads "the commit of w1's transition to planned".
  - r29: "it ran no `python3 -m pytest`".
  - r15: the stage-directory path. The step now reads "w1's implementation stage directory".
  - r5: the row "its questions the string "Why so?"".
  - r2: the brief's directory. The step now reads "where the worker's result goes".
  - r19: `--max-turns 25`. The step now reads "a limit of 25 turns".
  - r33: `.shop/worktrees/w1`.

### work-queue.feature
- **r8 (A):** the outline gains the row "failed from claimed -> ready". It is now titled "retry returns a failed work-item to the status it had before the failed stage: failed from <from>".
- **r7:** "says why in one line" -> "says why". This changes the title "a command that cannot be done exits with an error, says why in one line and changes nothing" -> "... says why and changes nothing", and the steps.

### design-model-check.feature
- **Removed (Implementation only):**
  - "`model check` ends with the four counts"
  - "rows of a violated relation are limited, saying how many more there are"
- **r1:** the step is now "it says it found no violation, unresolved reference or file problem". It no longer pins the counts.
- **r14 titles and steps:**
  - "writing the decisions index names the file and leaves out decisions with no id" -> "writing the decisions index leaves out decisions with no id". It no longer says which file was written.
  - The no-decision scenario's step is now "spec/decisions/index.md is written with its header and no row".

### migration-tools.feature
- **r17:** "... the qualifier going to by after the source, <case>" -> "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, <case>". The step is now "its by has the qualifier "(for artifacts)"". It no longer pins the exact `by` format.

### batch-measurement.feature
- **Removed:**
  - "a written batch is reported in one line" (r1)
  - "show prints the header, the tables, the exceptions, the hand-backs and the notes" (r18)
- **r19:** "compare prints both files' figures with the ratio of the second to the first" now shows only each figure, in total and per slice, with the ratio.
- **r29:** the step "writes the note on stderr" is gone.
- **r38:** the steps "says to name the living plan with --plan" and "says to give the batch's start with --from" are gone.

### analysis-tools.feature
- **Removed:**
  - "install with every tool present says so"
  - "install says each tool it installed"
  - "a tool that prints nothing is shown clean"
- **Retitled:**
  - "tests-of without a map says to make one" -> "tests-of without a map is refused"
  - "untested without a map says to make one" -> "untested without a map is refused"
  - "without coverage tests-of and untested say to install it" -> "without coverage tests-of and untested name it as missing"
  - "without jedi refs says to install it" -> "without jedi refs names it as missing"
  - "`tools check` names a missing tool under its heading" -> "`tools check` names a missing tool". The r17 scenarios now end "it exits with an error", which is r17's own response.
  - "install outside a virtualenv explains each missing tool and installs nothing" -> "install outside a virtualenv says so for each missing tool and installs nothing"
  - "untested prints each function with its place, the count and the commit" -> "untested prints each function, the count and the commit"
  - "`tools check` with no file to examine says so under ruff and vulture and does not fail for them" -> "`tools check` with no file to examine does not fail for ruff and vulture"
- **Other steps:**
  - r8's map outline drops the line pytest printed, where the map is, and the commit.
  - The import-linter scenario keeps only "import-linter is not run".
  - r49 drops "in one line".
  - r3's probe steps are worded as the line words them.
  - The r1 .venv scenario now observes "tools names jedi as missing" (B).

### feature-file-tools.feature
- **Removed:**
  - "deprecating a scenario prints its file and new title"
  - "a tag is found with or without its leading @"
- **r28:** "rebinding rewrites each binding of the old title and counts them" -> "rebinding rewrites each binding of the old title". The count step is gone.
- **r29:** the multi-line scenario no longer names the module and line.
- **r2:** "an edit is refused only when it would leave a Rule: block outside a docstring" -> "an edit is refused when it would leave a Rule: block outside a docstring". The row with two same-titled scenarios is gone.
- **r58:** the no-call scenario no longer pins "no test binds it".

## Rounds 1 and 2 (still in the drafts)
- **Exits:** every exit is in words. "exits non-zero" and the exit codes are gone from steps, titles and Examples.
- **Multi-tag splits:**
  - supervision `@r1 @r9` and `@r4 @r5`
  - work-queue `@r2 @r7`
  - design-model-check `@r16 @r17` and `@r5 @r23`
  - migration-tools `@r4 @r5` and `@r9 @r5`
  - batch-measurement `@r2 @r4`
  - analysis-tools `@r1 @r3` and `@r1 @r17`
  - feature-file-tools `@r19 @r46`
- **Deprecated, with replacements:** design-model-check r20 (several tags) -> r107. feature-file-tools r51 -> its new outline.
- **New:**
  - supervision r21-r41
  - work-queue r7 (existing file refused) and r8
  - design-model-check r106 and r107
- **Stripped:** the exits and steps that belong to another line (Q11).

## Questions
None open.

## Cases no line mentions
- A `work retry` on a work-item that is not failed.
- `model why` succeeding.
- What `work run` does with the branch reviewer's outcome.

### 2026-10-22T14:53:48, the agent's reply (handback)

Done: "in one line" is stripped from supervision r10 (title retitled) and r21, reply.md is updated with no questions open, and all seven drafts plus reply.md are in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-21-one-requirement/.
~~~~~~

## `.shop/scratch/drafts/2026-10-21-one-requirement/reply.md`

~~~~~~
# Formulation round 2026-10-21/22: one requirement per scenario (0054), exits in words (0055), a failed work-item (0056)

Every feature file here is the whole revised file, under the same name as in features/. This is round 3: it takes in the coordinator's answers A–E, and the answer that "in one line" goes everywhere. The answers to round 1's Q1–Q14 and the new lines (cd42cd6, then r28 -> failed) were already taken in.

Two rules hold in every file:
- A scenario shows only its own line's response. Steps that show another line's response are gone, exits included.
- A scenario pins no Implementation text (E). Where a line can only be seen through another command's output, the scenario still observes it that way (B).

Every title that changed is listed below as old -> new, so its binding can follow (`features rebind`).

## Coverage

| file | every line has a scenario | multi-tag scenarios left |
|---|---|---|
| supervision | yes, r1-r41 | none |
| work-queue | yes, r1-r8 | none |
| design-model-check | yes, r106 and r107 included | none; `@r20 @deprecated` is kept |
| migration-tools | yes, r1-r17 | none |
| batch-measurement | yes | none |
| analysis-tools | yes | none |
| feature-file-tools | yes | none; `@r51 @deprecated` is kept |

## Round 3 changes

### supervision.feature
- **r28 (D):** "... and the work-item goes to awaiting-ruling naming the file" -> "a change to .shop/work/ in the repository's own checkout that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file". The step is now "w1 is failed, naming .shop/work/i1/initiative.md".
- **r10 and r21: "in one line" stripped.**
  - r10's title: "`work run` that cannot do what it was asked exits with an error, says why in one line, and changes nothing" -> "`work run` that cannot do what it was asked exits with an error, says why, and changes nothing". Its step is now "work says that <reason>".
  - r21's step is now "`work run` refuses, saying that it was started by a worker of another `work run`".
- **Implementation text stripped (E):**
  - r7: the commit messages.
  - r31: the commit message. The step now reads "the commit of w1's transition to planned".
  - r29: "it ran no `python3 -m pytest`".
  - r15: the stage-directory path. The step now reads "w1's implementation stage directory".
  - r5: the row "its questions the string "Why so?"".
  - r2: the brief's directory. The step now reads "where the worker's result goes".
  - r19: `--max-turns 25`. The step now reads "a limit of 25 turns".
  - r33: `.shop/worktrees/w1`.

### work-queue.feature
- **r8 (A):** the outline gains the row "failed from claimed -> ready". It is now titled "retry returns a failed work-item to the status it had before the failed stage: failed from <from>".
- **r7:** "says why in one line" -> "says why". This changes the title "a command that cannot be done exits with an error, says why in one line and changes nothing" -> "... says why and changes nothing", and the steps.

### design-model-check.feature
- **Removed (Implementation only):**
  - "`model check` ends with the four counts"
  - "rows of a violated relation are limited, saying how many more there are"
- **r1:** the step is now "it says it found no violation, unresolved reference or file problem". It no longer pins the counts.
- **r14 titles and steps:**
  - "writing the decisions index names the file and leaves out decisions with no id" -> "writing the decisions index leaves out decisions with no id". It no longer says which file was written.
  - The no-decision scenario's step is now "spec/decisions/index.md is written with its header and no row".

### migration-tools.feature
- **r17:** "... the qualifier going to by after the source, <case>" -> "`migrate run` writes a qualified supersedes as the decisions' ids alone, the qualifier going to by, <case>". The step is now "its by has the qualifier "(for artifacts)"". It no longer pins the exact `by` format.

### batch-measurement.feature
- **Removed:**
  - "a written batch is reported in one line" (r1)
  - "show prints the header, the tables, the exceptions, the hand-backs and the notes" (r18)
- **r19:** "compare prints both files' figures with the ratio of the second to the first" now shows only each figure, in total and per slice, with the ratio.
- **r29:** the step "writes the note on stderr" is gone.
- **r38:** the steps "says to name the living plan with --plan" and "says to give the batch's start with --from" are gone.

### analysis-tools.feature
- **Removed:**
  - "install with every tool present says so"
  - "install says each tool it installed"
  - "a tool that prints nothing is shown clean"
- **Retitled:**
  - "tests-of without a map says to make one" -> "tests-of without a map is refused"
  - "untested without a map says to make one" -> "untested without a map is refused"
  - "without coverage tests-of and untested say to install it" -> "without coverage tests-of and untested name it as missing"
  - "without jedi refs says to install it" -> "without jedi refs names it as missing"
  - "`tools check` names a missing tool under its heading" -> "`tools check` names a missing tool". The r17 scenarios now end "it exits with an error", which is r17's own response.
  - "install outside a virtualenv explains each missing tool and installs nothing" -> "install outside a virtualenv says so for each missing tool and installs nothing"
  - "untested prints each function with its place, the count and the commit" -> "untested prints each function, the count and the commit"
  - "`tools check` with no file to examine says so under ruff and vulture and does not fail for them" -> "`tools check` with no file to examine does not fail for ruff and vulture"
- **Other steps:**
  - r8's map outline drops the line pytest printed, where the map is, and the commit.
  - The import-linter scenario keeps only "import-linter is not run".
  - r49 drops "in one line".
  - r3's probe steps are worded as the line words them.
  - The r1 .venv scenario now observes "tools names jedi as missing" (B).

### feature-file-tools.feature
- **Removed:**
  - "deprecating a scenario prints its file and new title"
  - "a tag is found with or without its leading @"
- **r28:** "rebinding rewrites each binding of the old title and counts them" -> "rebinding rewrites each binding of the old title". The count step is gone.
- **r29:** the multi-line scenario no longer names the module and line.
- **r2:** "an edit is refused only when it would leave a Rule: block outside a docstring" -> "an edit is refused when it would leave a Rule: block outside a docstring". The row with two same-titled scenarios is gone.
- **r58:** the no-call scenario no longer pins "no test binds it".

## Rounds 1 and 2 (still in the drafts)
- **Exits:** every exit is in words. "exits non-zero" and the exit codes are gone from steps, titles and Examples.
- **Multi-tag splits:**
  - supervision `@r1 @r9` and `@r4 @r5`
  - work-queue `@r2 @r7`
  - design-model-check `@r16 @r17` and `@r5 @r23`
  - migration-tools `@r4 @r5` and `@r9 @r5`
  - batch-measurement `@r2 @r4`
  - analysis-tools `@r1 @r3` and `@r1 @r17`
  - feature-file-tools `@r19 @r46`
- **Deprecated, with replacements:** design-model-check r20 (several tags) -> r107. feature-file-tools r51 -> its new outline.
- **New:**
  - supervision r21-r41
  - work-queue r7 (existing file refused) and r8
  - design-model-check r106 and r107
- **Stripped:** the exits and steps that belong to another line (Q11).

## Questions
None open.

## Cases no line mentions
- A `work retry` on a work-item that is not failed.
- `model why` succeeding.
- What `work run` does with the branch reviewer's outcome.
~~~~~~
