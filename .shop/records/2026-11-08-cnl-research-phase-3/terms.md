# b112 phase 3, share `terms`: the vocabulary

One row per adjective (condition) entry is in `terms.tsv`: 170 rows, one for each (term, kind) pair in
`spec/index.md`'s glossary and every capability's `## Terms`. A term given for two kinds (`open` of initiative and
of work-item) is two rows.

## How the columns were filled

- **defined**: taken from the tool, not judged by hand. `spec_context.load(".")` parses every condition's definition
  in the generated Def grammar; a condition is `y` when it is in `vocab.def_lits` (its definition parsed and was read
  into facts). 25 rows are `y`, matching the 25 the brief expected. Every `y` row has the form "A <kind> is <term>
  when ..."; every `n` row is a noun-phrase gloss ("a repository whose ..."), so the form test and the tool agree.
- **used**: the number of requirement statements whose parse tree holds a fun of that condition (via
  `vocab.decode`), over all 265 statements of `spec/capabilities/*.md` and `spec/universal.md`; none is refused, so
  no line is missed. A condition used only inside another condition's definition counts 0 (noted in the row).
- **constructs**: the phase 2 list (sample-rewrites.md §1.3). Four new names were needed:
  - **EXISTS**: a thing's existence as a state ("while the file `.venv/bin/python` exists", "no review of the pull
    request exists").
  - **ABILITY**: can / cannot as ability, not permission ("an interpreter that cannot import clingo"). MAY is
    permission and does not fit.
  - **INDEXICAL**: "this bounded context", the context whose spec the line is in (received, sent, untaken).
  - **HYPOTHETICAL**: "would" ("a file onto which `migrate run` would relocate another file").

## Counts by verdict

| Verdict | Rows | Lines using them | Defined (y) |
|---|---|---|---|
| structure | 74 | 104 uses | 8 |
| dead | 66 | 0 | 11 |
| artifact | 17 | 19 uses | 0 |
| keep | 7 | 20 uses | 2 |
| value | 5 | 7 uses | 5 |
| merge | 1 | 1 use | 0 |

Read the counts this way:

- **66 of 170 (39%) are used by no line** (55 prose, 11 defined; phase 1 counted the 55). Six are used only inside
  another definition: `open` (initiative) in idle and busy, `closed` (three kinds) and `unfixed` in complete,
  `well-formed` in passing, `codified` (capability) in uncodified. All but busy belong to plugin 1.x kinds
  (initiative, work-item, proposals, result, session) or retired capabilities. Nothing reports them.
- **Of the 104 live rows, 91 go**: 74 become a sentence structure, 17 a conformance (format) test. Five more are
  synonyms of a release value (behind, outdated, queued, current, ahead of repository), and one (unmigrated of
  repository) merges into unmigrated of bounded context.
- **7 are worth keeping as terms**: settled (request line), closed (request), blocked (item), downstream (bounded
  context), received and sent (request), prepositional (term). Each is a domain notion with an ordinary English
  reading (or, for prepositional, the linguist's own meaning) that several lines use or that the tool prints. Even
  these should have definitions that parse: blocked, downstream, received and sent are prose today, and received
  and sent need INDEXICAL to be defined at all.
- **Defined does not mean worth keeping.** 8 of the 14 live defined conditions are still `structure` or `value`:
  uncited ("cites no item"), untested and unrequired of design-decision ("is enforced by no test" and "...no
  requirement") already parse as relative clauses today, so the adjective never saved a construct. clean, passing,
  idle and uncodified pack two or more facts into one word. The five release synonyms are one attribute value each.

Constructs the 91 replacements need (live rows only; a row can need several):

| Construct | Rows | Construct | Rows |
|---|---|---|---|
| NEG-EXIST | 31 | COMPARE | 9 |
| WHOSE-REL | 28 | COUNT | 7 |
| HAS | 27 | NP-LIST | 6 |
| OF | 24 | WITH-ARG, STATE-MOVE | 4 each |
| SENSE | 22 | EXISTS, INDEXICAL | 3 each |
| RC-SUBJ | 18 | REL-COPULA, ABILITY | 2 each |
| CONFORMS | 14 | EXAMPLE-DATA-OUT, HISTORY, HYPOTHETICAL | 1 each |
| RC-OBJ | 12 | | |
| ADJUNCT-PP, POSS | 10, 9 | | |

The phase 2 finding holds over the whole vocabulary: four constructs (NEG-EXIST in every position, WHOSE over a
relation, HAS, and OF) do most of the work. SENSE comes next, at 22: the replacements keep needing a document as the
subject of name, use, hold or list, or a remote or git as the subject of refuse. CONFORMS fits 14 live rows and,
counting the dead ones, 18.

## Words with several meanings

| Word | Meanings |
|---|---|
| open | initiative (not done/abandoned), work-item (not green/withdrawn), the request status value `open`, GitHub's open issue (untaken's definition) |
| closed | four conditions (capability-proposal, glossary-proposal, work-item, request), each a different set of values, plus the participle of the verb close (`work` closes issue): "a closed request" and "a closed issue" are not the same thing |
| present | a Python interpreter whose file exists; a coverage map `tools map` has written (history); a measurement already written for its day |
| passing | an item that meets the readiness bar; a scenario whose test passes alone |
| malformed | four different forms: term entry, relation row, upstream entry, given block |
| uncommitted | a work-item that accepts nothing (committed *to* nothing); an untracked file in no git commit |
| uncited | a commit that cites no item; an observation no `source` names |
| untested | a design-decision enforced by no test; a requirement no scenario names |
| unparsed / unparsing | a request line in its upstream's grammar; a requirement in its own grammar; a result whose drafts do not parse |
| dangling | a capability-proposal with ids its capability lacks; a test module with bindings to no scenario |
| ahead | a repository on a newer plugin release; an initiative branch with commits its remote lacks (git's meaning) |
| codified / uncodified | of capability, change list and repository, three different tests |
| unreadable, lost, unheld, empty, large | each a condition and also an attribute value elsewhere (availability of transcript, standing of fulfilled request, content of session file, size of item) |
| kept, naming, received, sent, closed | participles of verbs (keep, name, close; receive and send have no entry), coined into conditions |
| foreign | a command whose `--from` names another context; the kind foreign entry |
| renumbered | duplicated ids, while renumber in the code (`backlog_lines.renumber`) is the fix for clashing ids |

## Common English words given a domain meaning

About 30 live rows take an everyday word and give it a narrow meaning a reader cannot guess: idle, busy, silent,
sound, stale, clean, present, current, behind, ahead, outdated, queued, compound, nested, partial, qualified,
conflicting, tracking, absent, foreign, sourced, unreadable, failing, passing, plus the dead ones (listless, free,
dirty, bare, strange, crowded, plural, large, flaky, lost, kept). Some clash with a technical meaning: sound (logic),
clean and dirty (a git working tree), tracking (git: has any upstream), bare, ahead (git's ahead of the remote). Misnomers: avoiding means the
requirement fails to avoid a word; renumbered means not yet renumbered; unformulated (dead) is said of a
`formulated` proposal.

## Nouns (kinds)

- **94 of 166 kinds are used by no line**, mostly 1.x (stage, worker, node, ledger, delivery) and the nouns of
  retired capabilities (spec-migration, spec-consistency, spec-integration, planning, review, code-research).
- **The kind tree confuses a thing with where it is stored.** item, batch, batch plan, record, quote, defect,
  capability, feature, design-decision, review folder and decisions index are all `Kind of: file`; request,
  comment, issue, question and answer are `Kind of: text`. Because of that, every file subkind inherits 1.x rows
  (`file | of | initiative`, `file | changed by | work-item`, `file | outside | file set`), so the grammar accepts
  "a batch of an initiative" and "an item in a worktree". A batch is a unit of work kept *as* a directory. It is not
  a file.
- **Several kinds are artifacts (formats or schemas) under another name**: given block, relation row, upstream
  entry, term entry, the comment's block of fields, feature (a path pattern), decisions index (a generated output),
  JSON object, plugin version (a file holding a version string). These are what CONFORMS should name. Today their
  forms live in prose definitions ("in the form `spec_read_given` reads", "not of the form `work request` writes"),
  which define the format by pointing at the code.
- Adjective-plus-noun kinds stand in for structure too: deprecated scenario, fulfilled request, logged stage,
  untracked file, unscoped requirement, misplaced scenario.

## Verbs and their frames

- **Gloss and frame disagree.** merge: the gloss says `work run` merges a work-item branch into the initiative
  branch, the frame says the person merges a pull request. name: the gloss says "a message or a file names a thing",
  the frame has an agent as subject, which is why phase 2's "a measurement that names" is refused. list: the gloss
  says "a session or a file lists things", the frame is "session lists file".
- **Frames bent to fit a line.** include: the gloss puts a figure *into* a measurement, the frame makes the
  measurement the object ("`measure` includes measurement"). note and log: the gloss appends a line to a ledger,
  the frame makes the ledger the object. keep: the gloss says "leaves a thing as it was", while conversation#r2 and
  the backlog lines need "keep X in Y" (record). Frames tied to one actor (relocate, rewrite, rename and append to
  `migrate`; install and replace to `tools`; publish, post and close to `work`; park to batch) hold today but fail
  as soon as a second actor does the same act.
- **Agentless glosses**, the passive the owner calls a fault: push ("a commit is pushed"), relocate, delete,
  retire, tag and note have no agent in their gloss, though their frames have one.
- **Catch-all verbs**: write (50 uses, "a file or a field") and change (6) take any text, so "write" covers
  creating, appending and recording, and the check cannot tell them apart.
- **Missing senses**, the SENSE construct: use, name, hold, list, include and find each need a document or a tool
  run as subject (a requirement uses a word; `model check` finds a violation); refuse needs a remote or git as
  subject (unpushable, uncommittable). fail and pass need intransitive entries.
- 18 of 43 verbs are used by no line (approve, discard, rerun, raise, pick, note, append, find, show, list, delete,
  retire, apply, tag, draft, take, log, restore). All 9 resources are unused (a 1.x mechanism).

## Relation rows

- 98 relation ids (per kind pair, after `Kind of:` is expanded), 32 used by a line.
- **Rows that are really verbs, or transitive acts**: cites, proposes, supersedes, fulfils, generates, quotes,
  weakens, contradicts, accepts, rests on and argues are fine as timeless relations. But adds, changes, removes and
  deletes (proposal and commit rows) are the same words as the verbs change, remove and delete, with no agent: one
  word in two categories, read differently by the check.
- **Rows whose word is a noun**: `request | asker | bounded context` and `request | upstream | bounded context`
  cannot be read as a sentence ("a request asker a bounded context"). They are OF relations ("the asker of a
  request") and need the OF construct to be usable. Neither is used by any line, though received, sent and unhosted
  are defined through them in prose.
- **Missing rows the replacements need**: repository | on | branch, branch | of | task, branch | has | upstream
  branch, commit | on | branch, bounded context | has | requirement grammar, request | holds | comment (unrecorded),
  test module | binds | scenario. Phase 2 found that most adjectives go with vocabulary (rows) rather than grammar;
  the whole vocabulary confirms it.
- **Inherited 1.x rows** (file | of | initiative, changed by work-item, outside file set, stage | needs | resource)
  make up about half of the 98 ids, and none of them is used.

## What the candidate form cannot say yet

Ability ("cannot import clingo"), the indexical "this bounded context", hypotheticals ("would relocate"), sameness
across two statements (repeating), and history ("has written", "already written") have no construct among the 1.3
list's live ones. The grammar findings of design-model-check (objectless, recipientless, mistyped, addressed,
verbal, negating, withholding, agentless, prepositioned: 9 rows) describe the requirement language's own sentence
forms. They are better as named grammar findings (codes) that a line cites than as adjectives of "requirement".
