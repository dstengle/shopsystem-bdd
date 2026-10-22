---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-migration-tools-formulation
kind: review-finding
about: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
date: 2026-10-20
---

# Formulation questions: migration-tools, release 0.21.0 (i8)

The blind feature-formulator's questions on spec/capabilities/migration-tools.md during release 0.21.0 (initiative i8),
2026-10-20 to 2026-10-21, with the coordinator's answers and the lines they led to. Three rounds: the first draft
(reply.md, 8 then 4 questions), review-2 of rows the code-writing session had added (Q1-Q8), and review-3 after the
kb trial (Q9-Q17). The exchanges are taken from the formulator's session transcript (session 172b8519, its prompts and
hand-backs, word for word); the coordinator's ledger for them is
initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-migration-release-ledger (lines 121-153). The
whole drafts are initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-migration-tools-formulation-drafts.

What the questions led to (commits on release-0.21.0):

| questions | answer | line or row it led to |
|---|---|---|
| round 1, Q1-Q8 (decisions dir vs ledger, records' landing, entry to file, @holding rebinding, id forms, numbering, reference forms, --context) | the coordinator's readings of decisions 0045, 0047, 0049, 0027 | the person moved the readings into the lines: fd5dfe7 (r1-r5 rewritten, r8-r10 new) |
| round 1b, Q1-Q4 (ledger gone, old id form, test logs, Behaviour order) | from lines and decisions | 25d2098 (r9, r10 refined, r11 added "from its questions") |
| review-2 Q3, Q5 (whole text in Decision; title and notes lost) | the person | 3e2fd74 (r2, r11) |
| review-2 Q1 (about for other moved records), F4 | the person | 71b0683 (r12) |
| review-2 Q2, Q4, Q6, Q7 | from r7, no new line | rows in e963f03 |
| review-3 (kb trial) | the person | 5f380db (r2, r6, r8, r9 changed; r13, r14) |
| review-3 Q9-Q12 | the person | b3a85b3 (r15-r17) |
| Q13-Q16 | the coordinator | rows in 95851ff; r17's by form put in Implementation |
| Q17 (by form not in r17's words) | left in Implementation | 95851ff |
| later rows (r5 with r13; README; by paths; two supersedes) | coordinator, from lines and 0047 | 8e03410, ada7d4f, 238237a |
| Q1, Q8 | left open for the kb trial | none |

Archived from git-ignored scratch; each file's text as it was.

## `/tmp/archive-tools/migration-tools-round1-exchange.md`

~~~~~~
### 2026-10-20T03:57:47, the coordinator to the agent

Formulate one feature file for the capability /home/vscode/shopsystem-bdd/spec/capabilities/migration-tools.md (7 Behaviour lines, a walking skeleton; approved). Write the draft to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature and your reply file beside it (reply.md). Format and rules: docs/capability-format.md in the plugin and the formulating-features skill (/home/vscode/shopsystem-bdd/skills/formulating-features/SKILL.md): one scenario per Behaviour line (a scenario may name several lines, decision 0052, only if they share one setup), tagged @r<n>, from the narrator's side, steps observable. Read features/work-queue.feature in the same repository for this context's step style. A line with two readings is returned as a question in your reply, never decided in a scenario.

### 2026-10-20T03:59:30, the agent's reply (handback)

I drafted one scenario per Behaviour line (7 scenarios, tagged @r1 to @r7), but only three lines are fully covered. Each of the other four has a clause with two readings or no stated form, and I held those clauses as questions rather than decide them.

Files:
- Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature
- Reply: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/reply.md (same content as this report)

**Not read:** I did not open docs/capability-format.md or skills/formulating-features/SKILL.md. My standing rules let me read only spec/ and existing features/ files, and they name docs/ as off limits. I copied the shape from features/work-queue.feature instead: the `# formulated from` header, Feature, Narrator, `@r<n>` tags, and a `Pins ...` line under each scenario. If either document asks for something that file doesn't show, the draft won't have it.

## Coverage

| Line | Scenario | Covered |
|---|---|---|
| r1 | run moves work/ to .shop/work/, and records/ and docs/superpowers/ under .shop/records/, with git | Partly. The decisions clause is held (Q1). The records destination is written only as "under .shop/records/" (Q2). |
| r2 | run replaces the ledger spec/decisions.md with one decision file for each of its entries | Yes. What a decision file holds is not pinned (Q3). |
| r3 | run makes a @holding scenario a @deprecated one | Partly. "Rebinding the tests that name it by title" is held (Q4). |
| r4 | run gives spec/index.md the context's id and each unnumbered Behaviour line an [r<n>] | Partly. Ids for capabilities, decision files and moved records are held (Q5). Numbering is pinned only where no line is numbered yet (Q6). |
| r5 | run rewrites a tracked text file's reference to a file it moved | Partly. Only a plain path to a moved file is pinned; changed ids and other reference forms are held (Q7). |
| r6 | after run, model check reports no violation, unresolved reference or file problem | Yes. |
| r7 | run that cannot make two of its moves names both, exits non-zero and changes no file | Yes. The failure example, a move onto a file that already exists, comes from the Implementation section, not Behaviour. |

No scenarios share a setup, so none names more than one line.

## Questions

1. **r1, "the decisions to spec/decisions/":** where are the decisions in the old layout? Is it a directory of decision files, or the ledger spec/decisions.md that r2 replaces?
2. **r1, "records/ and docs/superpowers/ to .shop/records/":** does records/r1.md land at .shop/records/r1.md, in a subdirectory, or in a destination for its kind? The same goes for docs/superpowers/. What happens when both hold a file with the same name?
3. **r2:** what does a decision file hold from its ledger entry, and how is the file named?
4. **r3, "rebinding the tests that name it by title":** two readings.
   - (a) Only the tag changes; the title stays and the tests are left as they are.
   - (b) The title changes too, and each test naming the old title is rewritten.

   Which is meant, and what counts as "a test that names it by title"?
5. **r4, "its id on the final layout":** the line gives no id form for a capability, a decision file or a moved record. Should the scenario take each form from design-decision/final-layout? Also, is the `--context <id>` value written into spec/index.md as given, or with a prefix such as bounded-context/?
6. **r4, numbering when some lines are already numbered:** say [r1] and [r3] exist with an unnumbered line between them. Does that line get the next number after the highest, the lowest unused one, or something else?
7. **r5, what counts as a reference?** Possible forms:
   - a repository-relative path
   - a path relative to the referring file
   - a markdown link
   - an id in frontmatter
   - a match inside a path that already starts with .shop/

   And for "changes an id": what old id do references name, when r4 says some files only now get an id?
8. **--context:** r1 names `migrate run --context <id>`, while r2 to r7 say only `migrate run`. Is --context required on every run?

## Cases no line mentions

- `migrate run` with no --context.
- A repository already on the final layout or partly migrated, including running migrate twice.
- A directory that is not a git repository, or uncommitted or untracked files under work/ or records/.
- spec/index.md missing, or already giving a different id.
- A ledger entry whose decision file already exists under spec/decisions/.
- A @holding scenario that no test names, or a title that two scenarios share.
- References in untracked files or in tracked files that are not text: are these left as they were?
- An old directory that is missing, for example no docs/superpowers/.
- A tracked text file that is not UTF-8.

### 2026-10-20T04:00:09, the coordinator to the agent

The coordinator sent a message while you were working:
Answers to your 8 questions (the coordinator's readings, from the approved decisions; the person sees them at the gate). Formulate the held clauses with them and update the draft and reply:
1. Both forms exist in the old layout: a top-level decisions/ directory of decision files moves to spec/decisions/ (r1); the ledger spec/decisions.md is split by r2 (design-decision/migration-in-one-pass lists both).
2. records/<x> lands at .shop/records/<x>, keeping its path; docs/superpowers/plans/* → .shop/records/archive/plans/, docs/superpowers/specs/* → .shop/records/archive/design-notes/ (design-decision/final-layout's records layout). Two files landing on one path: r7's refusal.
3. A ledger entry `## design-decision/<slug>` becomes spec/decisions/<nnnn>-<slug>.md, numbered in ledger order from one above any existing file, holding frontmatter id/summary/status (and source/by), `# <nnnn>. <title>` and `## Decision` with the entry's text.
4. Reading (b), as `features deprecate` does: the tag becomes @deprecated, the title gains " (deprecated)", a `Held for:` line becomes `Deprecated for:`, and each test that names the old title (a docstring, a `scenario(...)` call) names the new one.
5. Id forms are design-decision/capability-ids-are-context-scoped's and references-are-ids': capability/<context path>/<name>, design-decision/<context path>/<slug>, records by kind (decision-argument, initiative-archive, measurement). `--context <id>` takes the context path (owner/product/context) and spec/index.md gets `id: bounded-context/<that path>`.
6. One above the highest id the capability has ever used (its Behaviour ids and `retired:`).
7. In the skeleton, a reference is a repository-relative path, or a Markdown link path relative to the referring file, naming a moved file; and a frontmatter id naming a changed id. Nothing else.
8. `--context` is required on every `migrate run`.
The unmentioned cases fall under r7 (refuse, name it, change nothing); don't add scenarios for them.

Address this before completing your current task.

### 2026-10-20T04:01:18, the agent's reply (handback)

I've revised the draft and reply with your eight readings. All seven lines now have scenarios: 9 in all, with two each for r4 and r7. Three points are still open, and record ids under r4 are not pinned.

Files:
- Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature
- Reply: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/reply.md

**Not read:** docs/capability-format.md and skills/formulating-features/SKILL.md. My standing rules allow only spec/ and existing features/ files, and they name docs/ as off limits. The draft follows the shape of features/work-queue.feature.

**For the person at the gate:** the reply says that much of what is new in the r1 to r5 scenarios (paths, numbering, title text, id forms, reference kinds) comes from your readings of the decisions, not from the Behaviour lines. It suggests putting those readings into the lines, or into a decision they rest on, before approving.

## Coverage

| Line | Scenario | Covered | Rests on reading |
|---|---|---|---|
| r1 | run moves the old directories to the final layout with git | yes | 1, 2 |
| r2 | run replaces the ledger spec/decisions.md with one numbered decision file for each of its entries, in ledger order | yes, except the open points in question 1 | 3 |
| r3 | run makes a @holding scenario a deprecated one, and the tests that name it by title name its new title | yes | 4 |
| r4 | run gives spec/index.md, each capability and each decision file its id scoped to the context | partly: record ids are not pinned (question 2) | 5 |
| r4 | run numbers each unnumbered Behaviour line from one above the highest id the capability has ever used | yes | 6 |
| r5 | run rewrites a repository-relative path, a relative Markdown link and a frontmatter id to what it moved or renamed | yes | 7 |
| r6 | after run, model check reports no violation, unresolved reference or file problem | yes | none needed |
| r7 | run that cannot make two of its moves names both, exits non-zero and changes no file | yes | example from the Implementation section |
| r7 | run that would move two files onto one path names both, exits non-zero and changes no file | yes | 2 |

## Remaining questions

1. **r2 (reading 3):**
   - Where do a decision file's title, summary and status come from? The ledger heading is `## design-decision/<slug>`, which has no title. The scenario only says they are there.
   - Does "one above any existing file" count the files r1 moves from decisions/ in the same run? The scenario uses a repository with no decision files, so it only pins numbering from 0001.
   - When are source and by written?
2. **r4 (reading 5):** what is the full id form of a moved record (decision-argument, initiative-archive, measurement)? And which kind does each moved directory's files take? For example, do records/<x> or .shop/records/archive/plans/ files get initiative-archive ids? Record ids stay out of the scenario until this is answered.
3. **r5 (reading 7), "nothing else":** should a scenario pin the negative case, such as an id in body prose or a path in an untracked file being left as it was? I added none.

## Cases no line mentions

As you said, these fall under r7 and have no scenarios:
- `migrate run` without --context
- a repository already migrated, partly migrated, or run through migrate twice
- a directory that is not a git repository, or uncommitted or untracked files in the old directories
- spec/index.md missing, or already giving a different id
- a ledger entry whose decision file already exists
- a @holding scenario no test names, or a title two scenarios share
- references in tracked files that are not text or not UTF-8
- an old directory that is missing

### 2026-10-20T18:09:00, the coordinator to the agent

The coordinator sent a message while you were working:
The person approved your point: the readings are now in migration-tools' lines (commit fd5dfe7). Re-read /home/vscode/shopsystem-bdd/spec/capabilities/migration-tools.md: r1-r5 are rewritten and r8-r10 are new (r6, r7 unchanged). Revise your draft in the same place (/home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/) so every scenario rests on a line's own words, one scenario per line (several lines only if they share one setup), and update reply.md: coverage table and any question still open. Your remaining questions 1-3 are answered by the new r2 (title, summary, status, date and by from the entry; numbering as in the entry's heading), r9 (record id kinds), and r5 (only the three reference forms; no negative scenario needed).

Address this before completing your current task.

### 2026-10-20T18:10:12, the agent's reply (handback)

I've redrafted against the lines in commit fd5dfe7. There are now ten scenarios, one per line from r1 to r10, and each uses only the words of its own line. Seven lines are fully covered; r2, r5, r9 and r10 each leave one point open, and only r9 has a gap in coverage. The four questions are below.

Files:
- Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature
- Reply: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/reply.md

I still did not read docs/capability-format.md or skills/formulating-features/SKILL.md, because my rules allow only spec/ and existing features/ files. The shape follows features/work-queue.feature.

## Coverage
| Line | Scenario | Covered |
|---|---|---|
| r1 | run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git | yes |
| r2 | run replaces a ledger entry with a decision file named by its heading, holding its first paragraph, accepted, with its date and source | yes, except whether spec/decisions.md itself is removed (Q1) |
| r3 | run deprecates a @holding scenario as `features deprecate` does | yes, by comparing with a copy that `features deprecate` was run on |
| r4 | run gives spec/index.md the id bounded-context/<path> | yes |
| r5 | run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed | yes; the changed id used is a ledger entry's (Q2) |
| r6 | after run, model check reports no violation, unresolved reference or file problem | yes |
| r7 | run that cannot make two of its changes names both, exits non-zero and changes no file | yes; one setup has a move onto an existing file and two files moving to one path |
| r8 | run moves docs/superpowers/plans/ and docs/superpowers/specs/ under .shop/records/archive/, with git | yes |
| r9 | run gives a capability, a decision file, a plan and a design note the type-first id of its kind | partly; test logs and the full record id form are held (Q3) |
| r10 | run numbers each Behaviour line with no id from one above the highest id its capability has ever used | yes, with a single unnumbered line; the order of several is not pinned (Q4) |

The decision file's title is no longer pinned, because r2 doesn't mention it.

## Open questions
1. **r2, "replace it":** once every entry is replaced, is spec/decisions.md removed, or left holding whatever isn't an entry? The scenario only pins that the entry is gone.
2. **r5 with r9, "changes an id":** the scenario assumes the ledger entry's id decision/0007-a becomes design-decision/example.org/acme/shop/a, so a rests_on naming decision/0007-a is rewritten. Is decision/<nnnn>-<slug> the old id the lines mean? Does run change any other old id forms, such as an old capability id?
3. **r9, test logs and record ids:** where is a test log in the old layout? Neither r1 nor r8 says which moved files are test logs, so no scenario can name one. And what is the rest of a record's id after its kind? The scenario pins only the kind.
4. **r10, several unnumbered lines:** are they numbered in Behaviour order (r5, then r6)? The line says only "from one above".

## Cases no line mentions
As you said, these fall under r7 and have no scenarios:
- `migrate run` without --context
- a repository already migrated, or partly migrated
- a directory that is not a git repository
- spec/index.md missing, or already giving an id
- a ledger entry with no date, no source or no first paragraph
- a @holding scenario that `features deprecate` would refuse
- tracked files that are not text or not UTF-8
- an old directory that is missing

### 2026-10-20T18:10:26, the coordinator to the agent

The coordinator sent a message while you were working:
Answers (from lines and accepted decisions, no new readings): Q1: spec/decisions.md is gone after the run — r6 requires model check to report no file problem, and the old ledger's path is one (design-model-check's table); pin it in r2's scenario as "and spec/decisions.md is gone" only if the repository's ledger held nothing but entries. Q2: yes, decision/<nnnn>-<slug> is the old id in the skeleton; other old forms aren't pinned. Q3: the id form after the kind is design-decision/capability-ids-are-context-scoped's general `<kind>/<context path>/<name>`, the name being the file's stem; a test log is a file under records/ whose name ends `-test-log.md` — add one to r9's scenario. Q4: in Behaviour order. Finish the draft and reply.

Address this before completing your current task.

### 2026-10-20T18:11:11, the agent's reply (handback)

The draft is finished: ten scenarios, one per Behaviour line, every line covered and no questions left open. Three of them, r2, r9 and r10, pin things their own line does not say, so they do not yet rest wholly on their line's words.

Files:
- Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature
- Reply: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/reply.md

I still have not read docs/capability-format.md or skills/formulating-features/SKILL.md, because my rules allow only spec/ and existing features/ files. The shape follows features/work-queue.feature.

**For the gate:** in the three scenarios below, part of what is pinned comes from your answers and accepted decisions, not from the line. The reply flags this for the person. The fix is to add these points to r2, r9 and r10.
- **r2:** "spec/decisions.md is gone" rests on r6 and design-model-check's table. It is pinned only for a ledger that holds nothing but entries.
- **r9:** the id form `<kind>/<context path>/<name>` (name is the file's stem) comes from design-decision/capability-ids-are-context-scoped. "A test log is a file under records/ ending `-test-log.md`" comes from you.
- **r10:** numbering the new lines in Behaviour order comes from your answer.

## Coverage

| Line | Scenario | Covered |
|---|---|---|
| r1 | run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git | yes |
| r2 | run replaces a ledger that holds only entries with a decision file for each, named by its heading, holding its first paragraph, accepted, with its date and source | yes ("is gone" rests on r6 and a decision) |
| r3 | run deprecates a @holding scenario as `features deprecate` does | yes, by comparing against a copy of the repository that `features deprecate` was run on |
| r4 | run gives spec/index.md the id bounded-context/<path> | yes |
| r5 | run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed | yes; the old id used is decision/<nnnn>-<slug>, and no other old forms are pinned |
| r6 | after run, model check reports no violation, unresolved reference or file problem | yes |
| r7 | run that cannot make two of its changes names both, exits non-zero and changes no file | yes |
| r8 | run moves docs/superpowers/plans/ and docs/superpowers/specs/ under .shop/records/archive/, with git | yes |
| r9 | run gives a capability, a decision file, a plan, a design note and a test log the type-first id of its kind | yes (the id form and what a test log is rest on a decision and your answer) |
| r10 | run numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used | yes (the order rests on your answer) |

## Cases no line mentions

These fall under r7, and as you asked none has a scenario:
- `migrate run` without --context
- a repository already migrated, or partly migrated
- a directory that is not a git repository
- spec/index.md missing, or already giving an id
- a ledger entry with no date, source or first paragraph
- a ledger that holds more than entries
- a @holding scenario that `features deprecate` would refuse
- tracked files that are not text, or not UTF-8
- an old directory that is missing
~~~~~~

## `.shop/scratch/drafts/2026-10-20-migration-tools/reply.md`

~~~~~~
# Reply: migration-tools formulation (final, against commit fd5dfe7's lines)

Draft: /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature

Not read: docs/capability-format.md and skills/formulating-features/SKILL.md. My standing rules allow only spec/ and existing features/ files. The draft follows the shape of features/work-queue.feature.

There are ten scenarios, one per line. Three of them pin things their own line does not say. The coordinator answered these points from other lines and from accepted decisions, so the person should see them at the gate:

- **r2, "spec/decisions.md is gone":** this follows from r6 and design-model-check's table. It is pinned only for a ledger that holds nothing but entries.
- **r9, the id form:** r9 does not give the form after the kind, or say what a test log is. Both come from design-decision/capability-ids-are-context-scoped (`<kind>/<context path>/<name>`, where name is the file's stem) and from the coordinator: a test log is a file under records/ whose name ends `-test-log.md`.
- **r10, Behaviour order:** r10 does not say that new numbers follow the lines' order. The order comes from the coordinator's answer.

To make each scenario rest on its line's own words, add these to r2, r9 and r10.

## Coverage

| Line | Scenario | Covered |
|------|----------|---------|
| r1 | run moves decisions/ to spec/decisions/, work/ to .shop/work/ and each records/<x> to .shop/records/<x>, with git | yes |
| r2 | run replaces a ledger that holds only entries with a decision file for each, named by its heading, holding its first paragraph, accepted, with its date and source | yes ("is gone" rests on r6 and a decision) |
| r3 | run deprecates a @holding scenario as `features deprecate` does | yes, by comparison with a copy that `features deprecate` was run on |
| r4 | run gives spec/index.md the id bounded-context/<path> | yes |
| r5 | run rewrites a repository-relative path, a relative Markdown link and a frontmatter id that name what it moved or renamed | yes. The old id used is decision/<nnnn>-<slug>, and no other old id forms are pinned |
| r6 | after run, model check reports no violation, unresolved reference or file problem | yes |
| r7 | run that cannot make two of its changes names both, exits non-zero and changes no file | yes |
| r8 | run moves docs/superpowers/plans/ and docs/superpowers/specs/ under .shop/records/archive/, with git | yes |
| r9 | run gives a capability, a decision file, a plan, a design note and a test log the type-first id of its kind | yes (the id form and test log rest on a decision and the coordinator) |
| r10 | run numbers each Behaviour line with no id, in Behaviour order, from one above the highest id its capability has ever used | yes (the order rests on the coordinator) |

## Questions still open

None.

## Cases no line mentions

These fall under r7. None has a scenario.

- `migrate run` without --context
- a repository already migrated, or partly migrated
- a directory that is not a git repository
- spec/index.md missing, or already giving an id
- a ledger entry with no date, no source or no first paragraph
- a ledger that holds more than entries
- a @holding scenario that `features deprecate` would refuse
- tracked files that are not text, or not UTF-8
- an old directory that is missing
~~~~~~

## `/tmp/archive-tools/migration-tools-review-2-3-exchange.md`

~~~~~~
### 2026-10-20T19:46:26, the coordinator to the agent

You formulated /home/vscode/shopsystem-bdd/features/migration-tools.feature earlier (your drafts are under /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/). Since then the session that wrote scripts/migrate added and changed scenario rows in it (fix commits 115e50c and 5eaf500): new rows under r1, r2, r7, r11, r12 and a reworded r8 Then; and line r12 was added to spec/capabilities/migration-tools.md (read it). A reviewer rightly says formulation must stay blind to the code. Read the current feature file against the capability's lines only (you may diff it against your last draft in the drafts folder) and write to the same drafts folder `review-2.md`: for each added or changed scenario or row, "confirmed" (it says what its line says, from the narrator's side) or your reworded text, or "remove" with why; and whether r12 has a scenario that pins its line. Also write the corrected whole feature file as `migration-tools.feature` there. A line with two readings is a question, not a decision.

### 2026-10-20T19:49:22, the agent's reply (handback)

I read the capability's Behaviour lines (r1 to r12) and the current features/migration-tools.feature, and diffed it against my last draft; I read no code, tests or commits. Of the added and changed scenarios and rows, I confirm 7, reword 5 and remove 7 (the 7 removals include 4 rows dropped from two outlines). r12 does have a scenario that pins its line, once part of that scenario is removed.

Files:
- /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/review-2.md (a verdict for each item, plus the questions)
- /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature (the corrected whole file)

## Coverage, added or changed items

| Line | Item | Verdict |
|---|---|---|
| r1 | main scenario ("has the content X had") | reworded. My own earlier draft got this wrong too. decisions/0001-d0.md gets an id from r9, and records/logs/r1.md may get an id and an about, so their Thens now say "apart from the id..." |
| r1 | file under records/ that is not text | confirmed. Pins line reworded to the narrator's side, and a "records/img/a.png is gone" step added |
| r2/r11 | main scenario (holds/holding became has/with) | confirmed |
| r2 | date and source on the lines straight after the first paragraph | remove: r2 can be read two ways here (Q2) |
| r2 | outline on punctuation in the paragraph and source | confirmed |
| r2 | every paragraph kept in the Decision | remove: contradicts r2, which says the Decision is the first paragraph (Q3) |
| r2/r5 | supersedes and revisit_when kept | remove: no line says it |
| r2/r11 | ledger title before the first entry | reworded. It follows from r11 as written. The Given lacked the "We do a." paragraph its Then checks for, and the title no longer says "drops the title" |
| r7/r11 | outline row `## decision/b` | remove (Q4) |
| r7/r11 | outline row "Notes on the ledger." | remove: contradicts r11 as written (Q5) |
| r7 | outline row: an entry there twice | confirmed, now a scenario of its own |
| r7 | decision file lands where decisions/0007-a.md moves | confirmed, now a scenario of its own |
| r7 | decision file onto an existing file, tracked or untracked (2 rows) | remove (Q6) |
| r7 | move onto an untracked file | confirmed. Pins line reworded. It rests on the Implementation section, as my original r7 scenario does (Q7) |
| r3 | Pins line garbled to "a with scenario" | reworded back to "a @holding scenario" |
| r8 | reworded Then (apart from the r9 id and the r12 about) | confirmed |
| r12 | new scenario | reworded. The "keeps an about that is there" half is removed (no line says it), and the test log is added. It pins r12 |

## Questions
- Q1 (r9, r12): r9 gives a kind only for a moved plan, design note or test log. Does any other moved record, such as records/logs/r1.md, get an id, and so an about under r12?
- Q2 (r2): where does an entry's first paragraph end when a date or source line follows it with no blank line between them?
- Q3 (r2, for the person): r2 drops every paragraph of an entry after the first. Is that meant, or should the Decision be the entry's whole text?
- Q4 (r2, r7, r11): is a `## decision/` heading that is not of the `<nnnn>-<slug>` form an entry migrate cannot replace, so the run is refused, or is it ledger text outside any entry?
- Q5 (r11, for the person): as written, r11 removes the ledger once every entry is replaced, so any title or notes outside the entries are lost. Is that meant?
- Q6 (r2, r7): is writing a decision file where a file already is a change migrate cannot make, or does it replace that file?
- Q7 (r7): the rule that a move onto an existing file cannot be made is only in the Implementation section. Should it be a Behaviour line?

## Cases no line mentions
- An entry's supersedes, revisit_when or other fields.
- A moved record that already has an about.
- The earlier list still stands:
  - run without --context
  - a repository already or partly migrated
  - a directory that is not a git repository
  - spec/index.md missing or already giving an id
  - an entry with no date, source or first paragraph
  - a @holding scenario `features deprecate` would refuse
  - tracked files that are not UTF-8
  - an old directory that is missing

### 2026-10-20T20:43:53, the coordinator to the agent

The coordinator sent a message while you were working:
The person approved two line changes (spec/capabilities/migration-tools.md, now committed): r2 — the Decision is the entry's whole text and `date`, `by`, `supersedes`, `revisit_when` are the entry's; r11 — the ledger is removed when it holds nothing but its entries and a title. Answers to your other questions, from the lines: Q2 an entry's first paragraph ends at the first blank line or the first `date:` or `source:` line; Q4 a `## decision/` heading not of the `<nnnn>-<slug>` form, and Q6 a decision file landing where a file already is, are changes migrate cannot make — r7 (refuse, name it, change nothing); Q7 r7's general line covers it, no new line; Q1 left for the kb trial (no row). Revise your corrected file in the drafts folder accordingly: restore the rows you removed for Q3 and supersedes/revisit_when as r2 now says, the ledger-notes row as an r7 refusal under r11, the Q4 and Q6 rows as r7 refusals; then update review-2.md. Reply in at most 6 lines.

Address this before completing your current task.

### 2026-10-20T20:45:12, the agent's reply (handback)

I put back every row you named, as the new r2 and r11 and your answers say, and updated `migration-tools.feature` and `review-2.md` in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/ to match.
1. Restored: the whole-text Decision, supersedes/revisit_when, and the Q2 first-paragraph scenarios. Also restored: three refusal rows (`## decision/b`, the ledger notes, an entry there twice) and three decision-file collision rows (a file moving there, a tracked file, an untracked file).
2. I changed the Decision checks in the main and title scenarios. Since the new r2 makes the Decision the whole text, they now say "its Decision has 'We do a.'" instead of "is exactly 'We do a.'".
3. New question Q8: does "the entry's whole text" include its `date:`, `source:`, `supersedes:` and `revisit_when:` lines? The draft doesn't decide.
4. The ledger-notes refusal rests on your reading of r7, not on r11's words. Read alone, r11 would leave a ledger with notes in place rather than refuse the run. The person may want a line to say this.
5. Q1 is left for the kb trial and has no row. r12 is still pinned by its own scenario.

### 2026-10-20T21:36:30, the coordinator to the agent

The coordinator sent a message while you were working:
New formulation round for features/migration-tools.feature, from the kb trial (the person approved the line changes; read the current spec/capabilities/migration-tools.md and the trial's test log under .shop/records/measurements/fixture-runs/2026-10-20-kb-migrate-trial-test-log.md for what kb looks like — a narrator's view, no code). Changed: r2 (status superseded when another entry supersedes it), r6 (narrowed to unresolved references and file problems), r8 (requests), r9 (ADRs and requests); new: r13 (unnumbered entries numbered in ledger order from one above the highest), r14 (adrs/). Also rows for what existing lines require but kb showed broken: r7, a dirty working tree refused before any change; r9, a capability id already in the short form `capability/<name>` given the full form; r6, a `formulated_as` key gone, the new decision files tracked by git and spec/decisions/index.md written; r2, a `supersedes` value with a parenthetical qualifier like "(for artifacts)" keeps only the id, the qualifier going to `by`. Revise the whole file in your drafts folder (scenarios that the changed lines no longer support go or change), add rows as Examples where a scenario fits, and write review-3.md (coverage per line, questions). Reply in at most 6 lines.

Address this before completing your current task.

### 2026-10-20T21:38:53, the agent's reply (handback)

I revised the whole file and wrote `review-3.md` in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/; every line r1 to r14 now has a scenario. I did not read the kb test log: my rules allow only spec/ and features/, and a run's log would bring its behaviour into the formulation.
1. Changed lines: r2 now pins the superseded status; r6's Then is narrowed to unresolved references and file problems; requests and ADRs are added under r8, r9 and r12; new scenarios cover r13 and r14. The `## decision/b` refusal row is gone because r13 now numbers that entry.
2. Rows added from the trial, each backed by a model check table row: `formulated_as` (r25), a short-form capability id (r25/r46, also an r9 scenario), and a supersedes with "(for artifacts)" keeping only the id (r24) as an r6 Example.
3. Not added, returned as Q9 to Q12: a dirty working tree refused, new decision files tracked by git, `spec/decisions/index.md` written, and the qualifier going into `by`. No line requires them.
4. Decision 0023 allows one @r tag per scenario, so the earlier drafts' double tags are split; r11 now has its own outline.
5. Also open: Q1, Q8, Q13 (does a numbered ADR keep its number in its id) and Q14 (r13 with no numbered entry, and whether files in decisions/ count).

### 2026-10-20T22:42:32, the coordinator to the agent

The coordinator sent a message while you were working:
The person approved three new lines (now in spec/capabilities/migration-tools.md): r15 a dirty tree refused, r16 every written or moved file added to git and spec/decisions/index.md written, r17 a supersedes qualifier to `by`. Add their scenarios (your Q9-Q12). Answers: decision 0023 is superseded by 0052 (a scenario may name several requirements), so double tags are allowed — keep your split if it reads better; Q13 a numbered ADR keeps its number in its id (r9 drops it only for a decision file); Q14 with no numbered entry, numbering starts at 1, and r13 counts the ledger's entries only (a collision with a moved file is r7's refusal); Q1 and Q8 stay open for the trial. Write the final whole file in the drafts folder and update review-3.md. Reply in at most 4 lines.

Address this before completing your current task.

### 2026-10-20T22:43:57, the agent's reply (handback)

The final feature file and an updated `review-3.md` are in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/, and every line r1 to r17 now has a scenario.
r15, r16 and r17 have new scenarios. Per Q13 the ADR is now numbered and keeps its number in its id. Per Q14 the r13 outline has a no-numbered-entry row (numbering from 1), and the r7 collision outline has a row where a numbered entry lands on a moved decision file.
I kept one @r tag per scenario. Q1 and Q8 stay open. New: Q15 (r15: do untracked files count, and is a refusal a non-zero exit?) and Q16 (r17: does the qualifier replace the source in `by` or sit beside it, and in what form?).

### 2026-10-20T22:44:05, the coordinator to the agent

The coordinator sent a message while you were working:
Q15: untracked files count as uncommitted changes (a move could overwrite or strand them), and the refusal exits non-zero as r7's does. Q16: beside the source, `by: <the entry's source>; supersedes <id> <qualifier>`. Pin both in the rows and finish the file; reply in 2 lines.

Address this before completing your current task.

### 2026-10-20T22:45:14, the agent's reply (handback)

The file is finished and `review-3.md` is updated, both in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/. r15 now has two rows, a tracked change and an untracked file, each refused with a non-zero exit, and r17 pins `by: alice; supersedes design-decision/example.org/acme/shop/b (for artifacts)`.
Q1 and Q8 stay open for the trial. New Q17: the `by` form came from your answer, not from r17's own words, so r17 should spell it out if the line is to hold it.

### 2026-10-20T23:06:54, the coordinator to the agent

The coordinator sent a message while you were working:
One more row, from migrate-kb's review: r5 with r13 — a ledger entry `## decision/b` with no number is numbered (r13) and so changes its id; a frontmatter id `decision/b` elsewhere (e.g. a capability's rests_on) and another entry's `supersedes: decision/b` must name the new id afterwards, and the superseded entry's status is superseded (r2). Add it as an Examples row or a scenario under r5 (or r2) in your final file in the drafts folder, from the lines only. Reply in 2 lines.

Address this before completing your current task.

### 2026-10-20T23:07:55, the agent's reply (handback)

I added an @r5 scenario to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature: once r13 numbers `## decision/b` as 0008-b.md, a capability's rests_on and 0007-a's supersedes both name design-decision/example.org/acme/shop/b, and 0008-b.md's status is superseded (r2).
Every step rests on r2, r5, r9 and r13 as written, so it raises no new question; I have not updated review-3.md for this row.

### 2026-10-20T23:41:25, the coordinator to the agent

The coordinator sent a message while you were working:
From the second kb trial, three rows for features/migration-tools.feature, each from existing lines and decisions (no new line): (1) a moved README.md gets no id, no kind and no about — design-decision/references-are-ids gives frontmatter to every Markdown file under .shop/records/ but observations.md and a README.md (read spec/decisions/0047-references-are-ids.md); attach it to r9 or r12 as a row; (2) r5: a decision file's `by` naming a path that migrate moved (e.g. an ADR's old `adrs/0001-x.md` or `docs/superpowers/specs/y.md`) names the new path afterwards; (3) r2/r17: an entry whose `supersedes` names two decisions keeps both ids in `supersedes`. Write the final whole file in your drafts folder and reply in 3 lines.

Address this before completing your current task.

### 2026-10-20T23:42:38, the agent's reply (handback)

I added all three rows to /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature. Rows (2) and (3) rest on the lines; row (1), the README, rests on a decision, not a line:
(1) @r9: a moved README.md gets no id, kind or about. No line says so: r9 only says how to write an id once one is given. The rule comes from 0047, whose status is proposed, not accepted. 0047 also says every other Markdown file under records/ gets an id, which bears on open Q1. (2) @r5 outline: a `by` that names adrs/0001-use-x.md or docs/superpowers/specs/s1.md names the new path afterwards. (3) @r2: a `supersedes` naming 0003-b and 0004-c keeps both, by their new ids, and both are marked superseded.
review-3.md is not updated for these rows.

### 2026-10-21T00:14:45, the coordinator to the agent

The coordinator sent a message while you were working:
Two more rows for features/migration-tools.feature (the current file in features/ is the base; write the whole file to your drafts folder): (1) the README row should hold wherever a README.md lands under .shop/records/ — add an Examples row (or a second Given) for a README.md moved from adrs/ (r14) to .shop/records/decision-arguments/README.md: no id, kind or about; (2) a `by` built from an entry's source and a supersedes qualifier (r17's Implementation form `<source>; supersedes <id> <qualifier>`) has no stray punctuation such as `,;` — pin the exact `by` for an entry whose supersedes names two decisions, one with a qualifier. Reply in 2 lines.

Address this before completing your current task.

### 2026-10-21T00:15:55, the agent's reply (handback)

Both rows are in /home/vscode/shopsystem-bdd/.shop/scratch/drafts/2026-10-20-migration-tools/migration-tools.feature, written whole from the features/ file. The README scenario is now an @r9 outline with a second row for adrs/README.md moving to .shop/records/decision-arguments/README.md, with no id, kind or about. r17 is now an outline: for both "0003-b (for artifacts)" alone and "0003-b (for artifacts), 0004-c", `by` is exactly "alice; supersedes design-decision/example.org/acme/shop/b (for artifacts)" and `supersedes` names only the new ids.
That exact `by` form comes from r17's Implementation note, not its Behaviour line, so it is still my open Q17. A qualifier on the second decision (0004-c), or on both, has no row; I didn't touch review-3.md.
~~~~~~

## `.shop/scratch/drafts/2026-10-20-migration-tools/review-2.md`

~~~~~~
# Review 2: features/migration-tools.feature against spec/capabilities/migration-tools.md (r1 to r12)

Revised after the person's changes to r2 and r11 and the coordinator's answers to Q2, Q4, Q6 and Q7. Every verdict below rests on the lines as they are now committed. I read no code, tests or commits. The corrected whole file is migration-tools.feature in this folder.

## Added or changed scenarios and rows

### r1, main scenario (changed: "holds what X held" became "has the content X had")
Reworded. A moved file does not keep its content unchanged when r9 or r12 changes it: decisions/0001-d0.md gets an id from r9, and records/logs/r1.md may get an id and an about (Q1). New Thens:
- `Then spec/decisions/0001-d0.md has the content decisions/0001-d0.md had, apart from the id r9 gives it`
- `And .shop/records/logs/r1.md has the content records/logs/r1.md had, apart from any id r9 and about r12 give it`

### r1, file under records/ that is not text (added)
Confirmed. The Pins line is reworded to the narrator's side ("a file that is not text, such as an image, moves like any other."), and `And records/img/a.png is gone` is added.

### r2 @r11, main scenario (changed wording)
Reworded. r2 now makes the Decision the entry's whole text, so the Then no longer says the Decision is exactly "We do a.". It now reads `its Decision has "We do a."` (see Q8).

### r2, first paragraph ends at the date or source line (added)
Confirmed, on the answer to Q2: a first paragraph ends at the first blank line or the first `date:` or `source:` line. The title and Pins line now say that, and the Then checks the summary, date and by, not the Decision.

### r2, outline on punctuation in the paragraph and source (added)
Confirmed.

### r2, every paragraph kept in the Decision (added)
Confirmed under the new r2 ("whose Decision is the entry's whole text"). Its Then is `its Decision has "We do a." and then "Because b."`.

### r2 @r5, supersedes and revisit_when (added)
Confirmed under the new r2: `supersedes` and `revisit_when` are the entry's. r5 rewrites the superseded id to its new form.

### r2 @r11, ledger with a title (added)
Confirmed under the new r11, which removes a ledger that holds nothing but its entries and a title. The Given now gives the entry its first paragraph. Title: `run replaces a ledger that holds a title and its entries`.

### r7 @r11, outline "run that finds <found> in spec/decisions.md ..." (added)
All three rows are kept. The Pins line now reads "a ledger heading migrate cannot replace, or ledger text that is neither an entry nor its title, stops the run."
- `## decision/b`: confirmed, on the answer to Q4.
- "Notes on the ledger." before the entry: kept as the coordinator directed. Note that r11's words only say when the ledger is removed. Read alone, r11 would leave a ledger with notes in place rather than refuse the run. The refusal rests on the coordinator's reading of r7. The person may want r11 or r7 to say so.
- entry there twice: confirmed under r7.

### r7, outline "decision file would land on <there>" (added)
All three rows are kept. The moved-file row is confirmed under r7. The tracked and untracked rows are confirmed on the answer to Q6.

### r7, move onto an untracked file (added)
Confirmed: per Q7, r7's general line covers it. Pins line: "a file already there stops a move onto it whether or not git tracks it."

### r3 (Pins line garbled to "a with scenario")
Reworded back to "a @holding scenario".

### r8 (reworded Then)
Confirmed.

### r12 (added)
Reworded. "Keeps an about that is there" is removed because no line says it, and the test log is added. The scenario is now `run gives a moved plan, design note and test log with no about the context as their about`.

## Does r12 have a scenario that pins its line?
Yes, the r12 scenario above.

## Questions
- Q1 (r9, r12): left open for the kb trial, with no row. Does a moved record that is not a plan, design note or test log get an id, and so an about?
- Q8 (r2, new): does "the entry's whole text" in the Decision include the entry's `date:`, `source:`, `supersedes:` and `revisit_when:` lines, or only its prose? The draft checks only that the Decision has the prose, so it does not decide this.

## Cases no line mentions
- a moved record that already has an about
- run without --context
- a repository already or partly migrated
- a directory that is not a git repository
- spec/index.md missing or already giving an id
- an entry with no date, source or first paragraph
- a @holding scenario `features deprecate` would refuse
- tracked files that are not UTF-8
- an old directory that is missing
~~~~~~

## `.shop/scratch/drafts/2026-10-20-migration-tools/review-3.md`

~~~~~~
# Review 3 (final): migration-tools formulation after the kb trial

Formulated from spec/capabilities/migration-tools.md, lines r1 to r17, as committed. To see what r6 asks for, I also read design-model-check's table of unresolved references and file problems (rows r22, r24, r25, r46 and r61). I did not read the kb trial's test log: my rules allow only spec/ and features/, and a run's log would bring its behaviour into the formulation.

The final whole file is migration-tools.feature in this folder.

## This round
- **r15 (Q9 and Q15 answered):** now an outline with two rows, a tracked README.md changed since the last commit and an untracked notes/n2.md. In each, migrate refuses, naming the file, exits non-zero and changes no file.
- **r16 (Q11 and Q12 answered):**
  - git status shows the moved file, the new decision file and spec/decisions/index.md as staged, with nothing untracked or changed but not staged
  - `model decisions --check` says the index is current.
- **r17 (Q10 and Q16 answered):** supersedes is design-decision/example.org/acme/shop/b alone. by is "alice; supersedes design-decision/example.org/acme/shop/b (for artifacts)".
  - The id in by is written in its new form, as r5 rewrites ids in frontmatter.
  - The qualifier keeps its parentheses, as given.
- **Q13 answered:** the ADR is adrs/0001-use-x.md. Its id keeps its number: decision-argument/example.org/acme/shop/0001-use-x.
- **Q14 answered:**
  - the r13 outline has a row for a ledger with no numbered entry, where numbering starts at 1
  - the r7 collision outline has a row where entry b, numbered 0008, collides with decisions/0008-b.md as it moves.
- **Decision 0052 replaces 0023:** I kept the split into one @r tag per scenario, because each scenario then reads against one line.

## Coverage
| Line | Scenarios | Covered |
|---|---|---|
| r1 | moves decisions/, work/, records/<x>; a file that is not text | yes (Q1 open for records/logs/r1.md) |
| r2 | entry to file with its fields; first paragraph ends at date/source; punctuation outline; whole text in Decision; supersedes, revisit_when and the superseded status | yes (Q8 open) |
| r3 | as `features deprecate` does | yes |
| r4 | spec/index.md id | yes |
| r5 | path, link and frontmatter id rewritten | yes |
| r6 | outline: a full repository; formulated_as; short-form capability id; qualified supersedes | yes |
| r7 | ledger text it cannot replace (2 rows); decision-file collisions (4 rows); two failed changes; move onto an untracked file | yes |
| r8 | plans, specs, requests | yes |
| r9 | id of each kind (7 kinds, numbered ADR); short-form capability id | yes |
| r10 | Behaviour lines numbered | yes |
| r11 | outline: entries only; a title and entries | yes |
| r12 | about for each moved-record kind | yes |
| r13 | outline: among numbered entries; with no numbered entry | yes |
| r14 | adrs/ moved | yes |
| r15 | outline: a tracked change; an untracked file | yes |
| r16 | files added to git, index written | yes |
| r17 | qualifier to by, beside the source | yes |

## Questions
- **Q1 (r9, r12):** open for the trial. Does a moved record that is none of the listed kinds get an id and an about?
- **Q8 (r2):** open for the trial. Does the Decision's "whole text" include the entry's field lines?
- **Q17 (r17), new:** r17 itself does not give the form `<source>; supersedes <id> <qualifier>`, which came from your answer. If the form is to be held to the line, r17 should spell it out.

## Cases no line mentions
- the same unnumbered heading twice
- an entry superseded by, or superseding, a decision not in the ledger
- a moved record that already has an about
- run without --context
- a repository already or partly migrated
- a directory that is not a git repository
- spec/index.md missing or already giving an id
- an entry with no date, source or first paragraph
- a @holding scenario `features deprecate` would refuse
- tracked files that are not UTF-8
- an old directory that is missing
~~~~~~
