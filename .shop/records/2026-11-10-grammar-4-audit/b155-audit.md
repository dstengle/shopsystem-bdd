# Audit: can grammar 4 say spec/universal.md? (b155)

Sources: b155's reworded lines U12-U16 (which retire U11, U4, U5, U7, U8), spec/universal.md (codified-1, five live
lines, no other item adds grammar-4 lines to it), phase 3's candidates (c.tsv rows U11-U8, c.md). Each line was run
through `model parse --form` against main's codified-2 index (glossary as it stands, no item rows laid). Per-line
verdicts are in `audit.tsv` beside this file.

## Counts

5 lines: **fine 1, distortion 2, unsayable 0, coined 2.**

| id (old) | verdict | parses today |
|---|---|---|
| U12 (U11) | distortion | yes |
| U13 (U4) | coined | no, stops at "transition" (row commit\|of\|text missing) |
| U14 (U5) | coined | yes |
| U15 (U7) | distortion | no, stops at "its" (row worktree\|of\|session missing) |
| U16 (U8) | fine | no, stops at "of" (row command\|of\|tool missing) |

Three of five lines do not parse until b235 lets an item add a relation row. b155's notes say so, and the parser
confirms it.

## Missing constructs

| construct | lines | where |
|---|---|---|
| changing an attribute's value ("change/set the status of a node"), which `change` cannot take because its frame is `agent changes file` | 2 | U13, U14 (hidden in *transition*) |
| the reason of an event ("refuses a command for a reason", "the reason it refuses it") | 1 | U12 |
| "nothing" as an object of any kind, because `change`'s frame narrows it to files | 1 | U12 |
| the result of an earlier act ("the commit it made"), stood in for by a relation row | 1 | U13 |
| glossary only: rows worktree\|of\|session, command\|of\|tool, commit\|of\|text; a word for a batch's task subagent | 3 | U13, U15, U16 |

## The worst examples

**U14 "A session shall not write a transition."** It parses, but only because *transition* (noun, Kind of: text,
glossed "one change of a node's status, written by `work`") carries the structure. The original U5 said a session
never writes a status, meaning it never changes the status attribute of any node. The plain sentence "A session
shall not change the status of a node" is refused: `change` takes only a file, and the base grammar has no way to say
that an attribute's value is set. This is the anti-goal the design names: a noun whose gloss hides an attribute
change, with "write" applied to something that is not text. U13 rests on the same noun and adds a second stand-in:
"push the commit of the transition" needs an invented `commit | of | text` row to point at the commit that "commit
the transition" just made.

**U12 "... exit with an error naming a reason and change no file."** The form shows `response [x3: reason]`. Under
R1 this is a *new* reason, any reason at all, not the reason the tool refused the command. "If a tool refuses a
command for a reason" does not parse, so the line has no link from the reason to the refusal. That link survives
only in the gloss of *reason* ("what an error names as the cause of a refused command"). U11's "change nothing" also
became "change no file", because `change`'s frame refuses any object that is not a file. The line is now weaker:
changing a git ref, an issue or a remote no longer breaks it. U12 is also the line that b122 and goal 5 rely on to
make every "shall refuse the command and name X" line short. A weak U12 therefore weakens every refusal in the spec.

**U15 "A dispatch shall change only files in its worktree."** The language can say this: R5 handles "only" and R8
handles "its", and the reading-rule twin uses this exact shape with "session". But the meaning moved. *dispatch* is
any session another session starts with its Agent tool: reviewers, the batch driver and audit dispatches such as
this one. U7 meant only a batch's task subagent. *worktree* is still glossed as "a working tree `work run` makes for
one stage", from the retired workflow. As written, the line forbids what reviewers and audits rightly do.

## Which distortions a rewording alone could fix

- **U15**: yes, with glossary work and no new construct. Re-gloss *worktree* for a batch task. Add the row
  `worktree | of | session | one`, or better a row from a task to its worktree. Narrow the subject to the task's
  dispatch, for example "A dispatch that runs a task shall change only files in the worktree of the task", given a
  frame for "runs a task".
- **U16**: needs only the `command | of | tool | one` row (b235). Also drop the conditional clause from the gloss of
  *JSON object*: the line now says that condition.
- **U12**: only partly. "change no file" could be fixed by giving `change` a second frame (`agent changes thing`) in
  the glossary or the CLI pack. That is a glossary edit, not a construct. Tying the reason to the refusal needs a
  construct: a "for" adjunct on `refuse` (a frame `tool refuses command for reason`) would carry it as frame
  structure. That is again a glossary frame rather than base grammar, and it is legitimate, since frames are the
  sentence structure of 4.0. Without it, the line stays weaker than U11.
- **U13, U14**: no. Saying them honestly needs a base-grammar construct for an attribute's value being changed by an
  agent, such as "`work` shall commit every change of the status of a node", plus a way to name what an earlier act
  produced, or else a second frame of `change` over attributes. Until then *transition* is a coined noun hiding
  that structure.

## Also noted

- The "An If line takes precedence" section of spec/universal.md is now the language's R9 / call 12 reading rule. It
  is not a line and needs no rewording.
- universal.md's purpose and reading notes still cite `work run`, stages and U7's "Carried forward to R14". The
  reword should update them along with the gloss of *worktree*.
