# The sample written in each language, side by side

Phase 2 of b112's research (`.shop/backlog/b112.md`). The 27 sample lines of
`scratchpad/b112/sample.md`, each written in Attempto Controlled English (ACE), SBVR Structured English, FRETish and a
candidate form in the owner's direction, with the constructs each candidate needs, the coined adjective it removes and
the vocabulary it asks for. Sources for the three languages are phase 1's reports
(`2026-11-08-cnl-research-phase-1/logic-cnls.md` for ACE and SBVR, `requirement-cnls.md` for FRETish); no language's
own tool was run here (APE's web service was down in phase 1, FRET was not installed), so the ACE, SBVR and FRETish
renderings are hand-written by the construction rules those reports quote. Where I am unsure a rendering is
well-formed, the line says so.

Every candidate was put through `python3 scripts/model parse` on main (2026-11-08). The result is in each entry and in
§3.

## 1. Conventions

### 1.1 How each language is written here

**ACE** (ACE 6.7 construction rules, Fuchs, Kaljurand and Kuhn): actors are proper names (`Work`, `Migrate`,
`Features`, `Model`, `Measure`, `Trial-runner`); a backquoted command is an ACE string (`"work sync"`), which ACE
allows as a noun phrase but which carries no type; multi-word nouns are hyphenated (`request-line`, `pull-request`)
as ACE requires unless the lexicon lists the compound; `shall` is `must`; ACE has one conditional, `If ... then`, so
While, When and If all become conjuncts of one if-part; a participle ("naming X") becomes a relative clause ("that
names X"). A prepositional verb ("conforms to") is assumed to be a lexicon entry; I did not check it against APE.

**SBVR Structured English** (SBVR 1.5 annex; "SBVR Speaks", Business Rules Journal 2006): terms in lower case, names
as written, keywords `It is obligatory that`, `It is prohibited that`, `It is necessary that`, `each`, `that`, `if`,
`only`, `at most`. A behaviour (shall) is an operative rule, `It is obligatory that ...`; a shall-not is
`It is prohibited that ...`; an invariant of what counts as a valid state is `It is necessary that ...`. SBVR has no
While/When distinction either; both become an `if` clause, usually last. Fonts (term underlined, verb italic) are not
shown.

**FRETish** (Giannakopoulou et al. 2021; FRET manual): `[scope] [condition] component shall [timing] response`.
I map EARS onto it as: a While state is a FRET *scope* (a mode: `in <mode> mode`), a When or If trigger a FRET
*condition* with `upon` (the rising edge), the response `satisfy <boolean>`, timing `at the next timepoint` for a
command's effect (FRET's default `eventually` is wrong for these lines). FRETish is propositional: "a comment", "the
request line" become boolean variables, so every quantified noun phrase is lost. That loss is the same on every line
and is not repeated in each entry.

### 1.2 The candidate form

EARS clause order kept; no coined adjectives; a state in While, the behaviour in When (If for a refusal); the agent
explicit; relative clauses from verb frames and relations; "of"; conformance to a named artifact; a small modal set.
Responses keep today's fixed forms ("exit with an error naming X and change nothing", "exit successfully") so that a
candidate differs from today's line only where the adjective was; §4.3 weighs shortening the refusals to
"refuse the command" with U11 supplying the rest.

### 1.3 Constructs (the fixed list used below)

"Exists" means `model parse` accepts it on main today in some form; "partly" names the limit.

| Code | Construct | Example | Today |
|---|---|---|---|
| RC-SUBJ | relative clause, subject gap, from a verb or a relation | "a measurement that names the target" | partly: relation rows ("a commit that cites no item") and verbs whose frame's subject the noun fits; a verb whose frame takes an agent refuses a thing as subject |
| RC-OBJ | relative clause, object gap | "a comment that a session posts" | no |
| WHOSE-REL | "whose" over a relation noun, not only an attribute | "a branch whose upstream branch ...", "a docstring whose text ..." | no (attributes only: "whose status is") |
| OF | "the X of Y" as a noun phrase in any slot, including an attribute as the subject of "is" | "the release of a repository is `own`", "the text of an untracked file" | partly: per relation row whose word is "of", and "the status of X" as an object only |
| POSS | possessive pronoun | "its upstream", "its target" | partly: "its" for some kinds ("its worktree") |
| HAS | "has" / "holds" as a relation verb with any object | "a feature file has a docstring" | no |
| NEG-EXIST | "no X" in a subject or after "has"/"with" | "no commit holds ...", "has no frame", "with no origin option" | partly: "no X" as a relation's object ("cites no item") |
| CONFORMS | conformance to a named artifact | "does not conform to the comment schema" | no |
| COMPARE | order or difference between values | "after `1.0.0` and before `3.0.0`", "a different name" | no |
| COUNT | a numeral meaning exactly n | "with one `scenarios(...)` call" | no ("one" reads as "a") |
| NP-LIST | a coordinated list of objects inside a clause | "includes "wall time", "session time" ... and "cost by role"" | partly: after print only |
| VP-COORD-NEG | one subject, a positive and a negated verb phrase | "shall print the comment and not write the comment" | no (needs ", and `work` shall not ...") |
| ADJUNCT-PP | a verb frame's extra prepositional role | "remove X from Y", "refuses X for a reason", "binds X with Y", "record X in Y" | no (the frame's "to" recipient only) |
| REL-COPULA | a relation row whose word is a preposition, used as "X is <prep> Y" | "a repository is on a branch" | unverified: the row is missing, so not tried |
| WITH-ARG | a command's argument as a noun phrase after the trigger | "runs `work request` with no origin option", "runs `features list` with the tag" | no |
| SENSE | a second frame of a word already in the glossary | "a measurement names" beside "an agent names"; "record" for keep's second sense | no (one frame per verb) |
| TRIGGER-AS-ACTION | an action with an explicit agent in place of a command string | "When `work` makes a transition" | exists for glossary verbs |
| EXAMPLE-DATA-OUT | example data moved out of the line into the group's given block | `banana`, `i1`, `features/notes.feature` | (a writing rule) |
| STATE-MOVE | a state moved out of a trigger's noun phrase into While, or a property of the command moved into the trigger | r24, telemetry r1; r6 | (a writing rule) |
| ONLY | "only" on an object | "change only files in its worktree" | exists |
| NEVER / ALWAYS, MAY, ONLY-AFTER, HISTORY | invariant adverbs, permission, precedence, "has <verb>ed" | | no; none of the 27 candidates needs one (§4.1) |

## 2. The 27 lines

Each entry: the current line; ACE; SBVR; FRETish; the candidate; constructs, the adjective removed and the
vocabulary; example data; whether the candidate parses today.

### requests#r33

- **Current:** While a comment is unreadable, when a session runs `work sync`, `work` shall print the comment, and
  `work` shall not write the comment. (unreadable: a comment whose block of fields does not parse.)
- **ACE:** If a comment does not conform to the comment-schema and a session runs "work sync" then Work must print the
  comment and Work must not write the comment.
- **SBVR:** It is obligatory that work prints each comment that does not conform to the comment schema if a session
  runs work sync. It is prohibited that work writes a comment that does not conform to the comment schema. (Two
  rules: SBVR keeps an obligation and a prohibition apart.)
- **FRETish:** in comment_nonconforming mode, upon sync_run, work shall at the next timepoint satisfy comment_printed &
  !comment_written.
- **Candidate:** While a request comment does not conform to the comment schema, when a session runs `work sync`,
  `work` shall print the comment and not write the comment. (The owner's own rewrite.)
- **Constructs:** CONFORMS, VP-COORD-NEG. **Removes:** unreadable. **Vocabulary:** artifact *comment schema* (the
  block of fields, kept as an external file the line names); *request comment* as a compound noun, or "a comment of a
  request" (OF over the existing comment-request link).
- **Example data:** none.
- **Parses today:** no (stops at "request comment"; no CONFORMS).

### requests#r38

- **Current:** While a request line is unparsed, if a session runs `work outcome accepted` on the request line, then
  `work` shall exit with an error naming the request line and change nothing. (unparsed: does not parse in its
  upstream's requirement grammar.)
- **ACE:** If a request-line does not conform to a requirement-grammar of an upstream of the request-line and a session
  runs "work outcome accepted" on the request-line then Work must exit with an error that names the request-line and
  must change nothing. (ACE would need "the upstream of the request-line" to be introduced first, or "a ... of";
  "its" works in ACE but resolves to the most recent noun phrase, here the grammar's owner is ambiguous.)
- **SBVR:** It is obligatory that work exits with an error that names the request line and changes nothing if a
  session runs work outcome accepted on a request line that does not conform to the requirement grammar of the
  upstream of the request line.
- **FRETish:** in line_unparsed mode, upon outcome_accepted_run, work shall at the next timepoint satisfy error_exit &
  names_line & !changed.
- **Candidate:** While a request line does not conform to the requirement grammar of its upstream, if a session runs
  `work outcome accepted` on the request line, then `work` shall exit with an error naming the request line and change
  nothing.
- **Constructs:** CONFORMS, OF, POSS. **Removes:** unparsed (both senses: the requirement one in design-model-check
  becomes "does not conform to the requirement grammar of its bounded context"). **Vocabulary:** artifact
  *requirement grammar* (one per bounded context: a relation bounded context | has | requirement grammar | one);
  the path request line -> request -> upstream, or a direct row request line | upstream | bounded context.
- **Example data:** `accepted` in the command is the line outcome, not example data; TRIGGER-AS-ACTION is possible
  ("if a session accepts the request line") but not needed.
- **Parses today:** no (no CONFORMS).

### requests#r6

- **Current:** While a command is originless, if the person runs `work request`, then `work` shall exit with an error
  naming an origin and change nothing. (originless: a command that gives none of `--source`, `--thread` and
  `--raised-for`.)
- **ACE:** If the person runs "work request" with no origin-option then Work must exit with an error that names an
  origin and must change nothing. (ACE's "no" in a prepositional phrase on the verb: allowed; the PP attaches to
  "runs".)
- **SBVR:** It is obligatory that work exits with an error that names an origin and changes nothing if the person runs
  work request with no origin option.
- **FRETish:** upon request_run & !source_given & !thread_given & !raised_for_given, work shall at the next timepoint
  satisfy error_exit & names_origin & !changed. (FRET is good here: the three options are three booleans and the
  condition says it directly.)
- **Candidate:** If the person runs `work request` with no origin option, then `work` shall exit with an error naming an
  origin and change nothing.
- **Constructs:** WITH-ARG, NEG-EXIST, STATE-MOVE (the While goes: "originless" was a property of the trigger, not a
  state of the system). **Removes:** originless. **Vocabulary:** kind *origin option* with instances `--source`,
  `--thread`, `--raised-for` (or attribute values), and the command | gives | option relation behind "with".
- **Example data:** none.
- **Parses today:** no (stops at "with").

### requests#r24

- **Current:** If the person runs `work resolve` on a request that is not `accepted`, then `work` shall exit with an
  error naming the status of the request and change nothing.
- **ACE:** If the person runs "work resolve" on a request and the status of the request is not accepted then Work must
  exit with an error that names the status of the request and must change nothing. (`accepted` as an ACE adjective
  or a proper name; ACE has no enumerated values.)
- **SBVR:** It is obligatory that work exits with an error that names the status of the request and changes nothing if
  the person runs work resolve on a request whose status is not accepted.
- **FRETish:** in request_not_accepted mode, upon resolve_run, work shall at the next timepoint satisfy error_exit &
  names_status & !changed.
- **Candidate:** While a request is not `accepted`, if the person runs `work resolve` on the request, then `work` shall
  exit with an error naming the status of the request and change nothing.
- **Constructs:** STATE-MOVE (the state moves out of the trigger's object into While). **Removes:** none.
  **Survives:** `accepted`, a status value. **Vocabulary:** none new.
- **Example data:** none.
- **Parses today:** yes.

### batches#r8

- **Current = Candidate:** While a batch is `building` and every task of the batch is `done`, when the person runs
  `work batch review` on the batch, `work` shall publish a pull request of the batch and set the status of the batch
  to `in-review`.
- **ACE:** If a batch is building and every task of the batch is done and the person runs "work batch review" on the
  batch then Work must publish a pull-request of the batch and must set the status of the batch to in-review. ("every"
  inside an if-part: ACE allows it and scopes it to its clause.)
- **SBVR:** It is obligatory that work publishes a pull request of the batch and sets the status of the batch to
  in-review if the person runs work batch review on a batch that is building and each task of that batch is done.
- **FRETish:** in batch_building & all_tasks_done mode, upon review_run, work shall at the next timepoint satisfy
  pr_published & status_in_review. ("every task" becomes one variable; FRET cannot say it.)
- **Constructs:** none new. **Survives:** `building`, `done`, `in-review` (status values). **Vocabulary:** none.
- **Parses today:** yes.

### batches#r13

- **Current:** While a commit of an item in a batch is uncited, if the person runs `work batch review` on the batch,
  then `work` shall exit with an error naming the commit and change nothing. (uncited: the commit cites no item.)
- **ACE:** If a commit is on a branch of a task of a batch and the commit cites no item and the person runs "work batch
  review" on the batch then Work must exit with an error that names the commit and must change nothing.
- **SBVR:** It is obligatory that work exits with an error that names the commit and changes nothing if the person runs
  work batch review on a batch and a commit on the branch of a task of that batch cites no item.
- **FRETish:** in uncited_commit_in_batch mode, upon review_run, work shall at the next timepoint satisfy error_exit &
  names_commit & !changed.
- **Candidate:** While a commit on the branch of a task of a batch cites no item, if the person runs `work batch review`
  on the batch, then `work` shall exit with an error naming the commit and change nothing.
- **Constructs:** OF (a new relation row), NEG-EXIST (as today). **Removes:** uncited. **Vocabulary:** relation commit
  | on | branch, branch | of | task (a task's branch is in the batch design already).
- **Example data:** none.
- **Parses today:** no as written (no commit-on-branch row). But **"While a commit of an item in a batch cites no item,
  if ..." parses today**: the adjective was never needed, the grammar already had the relation clause. That reading
  says "a commit of an item cites no item", which sounds self-contradictory; the branch version says what is meant.

### batches#r17

- **Current:** While an item that is `in-batch` proposes a requirement, when a batch parks the item, `work` shall remove
  the requirement.
- **ACE:** If an item is in-batch and the item proposes a requirement and a batch parks the item then Work must remove
  the requirement from the branch of the batch.
- **SBVR:** It is obligatory that work removes each requirement that an item proposes from the branch of the batch if
  the batch parks that item and the item is in-batch.
- **FRETish:** in item_in_batch & item_proposes mode, upon item_parked, work shall at the next timepoint satisfy
  !requirement_on_branch. (Here FRET states the effect as a state, which is clearer than "remove".)
- **Candidate:** While an item that is `in-batch` proposes a requirement, when a batch parks the item, `work` shall
  remove the requirement from the branch of the batch.
- **Constructs:** ADJUNCT-PP ("from"). **Removes:** none. **Survives:** `in-batch` (status value). **Vocabulary:**
  remove's frame given an optional "from" place.
- **Note:** I first wrote "when a session parks the item"; the grammar refused it ("the verb park takes as its subject
  batch"). The frame is right to insist: the agent is explicit, it is the batch.
- **Parses today:** without "from the branch of the batch", yes (that is today's line).

### batches#r16

- **Current = Candidate:** When the person merges the pull request of a batch, `work` shall remove every review folder
  of the batch.
- **ACE:** If the person merges the pull-request of a batch then Work must remove every review-folder of the batch.
  (Under ACE's interpretation rules "the pull-request" with no antecedent introduces a new entity: fine here.)
- **SBVR:** It is obligatory that work removes each review folder of a batch if the person merges the pull request of
  that batch.
- **FRETish:** upon pr_merged, work shall at the next timepoint satisfy !review_folders_exist.
- **Constructs:** none new. **Parses today:** yes.

### backlog#r20

- **Current:** While a repository is tasked, if the person runs `work idea`, then `work` shall exit with an error naming
  the task and change nothing. (tasked: its branch checked out is the branch of a task.)
- **ACE:** If a repository is on a branch of a task and the person runs "work idea" then Work must exit with an error
  that names the task and must change nothing. ("is on" as a copula with a PP is ACE-valid.)
- **SBVR:** It is obligatory that work exits with an error that names the task and changes nothing if the person runs
  work idea in a repository that is on the branch of a task.
- **FRETish:** in on_task_branch mode, upon idea_run, work shall at the next timepoint satisfy error_exit & names_task
  & !changed.
- **Candidate:** While a repository is on the branch of a task, if the person runs `work idea`, then `work` shall exit
  with an error naming the task and change nothing.
- **Constructs:** REL-COPULA, OF. **Removes:** tasked. **Vocabulary:** relation repository | on | branch | one (the
  branch checked out; "on" is git's own word, "on branch main"); branch | of | task.
- **Parses today:** no (no repository-on-branch row).

### backlog#r21

- **Current:** While a repository is tracking, when the person runs `work idea`, `work` shall write an item that is
  `idea`, commit the item and keep the upstream branch. (tracking: its branch checked out has an upstream branch of
  another name.)
- **ACE:** If a repository is on a branch and the branch has an upstream-branch and the name of the upstream-branch is
  not the name of the branch and the person runs "work idea" then Work must write an item that is idea and must commit
  the item and must keep the upstream-branch. (ACE can say "is not the name of the branch" with the copula; "a
  different name" has no ACE reading.)
- **SBVR:** It is obligatory that work writes an item that is idea, commits the item and keeps the upstream branch if
  the person runs work idea in a repository that is on a branch whose upstream branch has a name that is not the name
  of the branch.
- **FRETish:** in upstream_renamed mode, upon idea_run, work shall at the next timepoint satisfy item_written &
  committed & upstream_kept.
- **Candidate:** While a repository is on a branch whose upstream branch has a different name, when the person runs
  `work idea`, `work` shall write an item that is `idea`, commit the item and keep the upstream branch.
- **Constructs:** REL-COPULA, WHOSE-REL, COMPARE. **Removes:** tracking. **Survives:** `idea` (status value).
  **Vocabulary:** relation branch | has | upstream branch | one (or "upstream branch of"), attribute *name* of branch,
  and "different" (COMPARE between two values of one attribute: the subject's and the antecedent's).
- **Parses today:** no.

### migration-tools#r19

- **Current:** While a repository is idle, when the SessionStart hook runs `migrate status --hook`, `migrate` shall exit
  successfully, and `migrate` shall not print "migrate upgrade" or print "i1". (idle: the repository is `own` and no
  initiative is open.)
- **ACE:** If the release of a repository is own and no initiative of the repository is open and the SessionStart-hook
  runs "migrate status --hook" then Migrate must exit successfully and Migrate must not print "migrate upgrade" and
  must not print an id of an initiative. ("no ... is open" inside an if-part: ACE reads it as a negated existential in
  a sub-DRS, the right reading.)
- **SBVR:** It is obligatory that migrate exits successfully if the SessionStart hook runs migrate status --hook in a
  repository whose release is own and that has no initiative that is open. It is prohibited that migrate prints
  migrate upgrade or the id of an initiative if ... (repeated condition).
- **FRETish:** in release_own & !initiative_open mode, upon status_hook_run, migrate shall at the next timepoint
  satisfy success_exit & !upgrade_printed & !initiative_id_printed.
- **Candidate:** While the release of a repository is `own` and no initiative of the repository is open, when the
  SessionStart hook runs `migrate status --hook`, `migrate` shall exit successfully and not print "migrate upgrade" or
  the id of an initiative.
- **Constructs:** OF (attribute as subject), NEG-EXIST (subject), VP-COORD-NEG, EXAMPLE-DATA-OUT. **Removes:** idle.
  **Survives:** `own` (a value of release), and *open* (of initiative): its definition ("not `done` and not
  `abandoned`") already parses in the Def grammar, it is ordinary English and is derived from status values, so it is
  a defined condition rather than a coined one. Writing "every initiative of the repository is `done` or `abandoned`"
  removes it at a cost of four words.
- **Example data:** "i1" is an initiative id from the scenario's given block; the line means "the id of an initiative".
- **Parses today:** no (stops at "is" after "the release of a repository").

### migration-tools#r14

- **Current:** While the repository is current, when the person runs `migrate upgrade`, `migrate` shall print "no
  upgrade step is pending" and change nothing. (current: the repository is `own`.)
- **ACE:** If the release of a repository is own and the person runs "migrate upgrade" then Migrate must print "no
  upgrade step is pending" and must change nothing.
- **SBVR:** It is obligatory that migrate prints no upgrade step is pending and changes nothing if the person runs
  migrate upgrade in a repository whose release is own.
- **FRETish:** in release_own mode, upon upgrade_run, migrate shall at the next timepoint satisfy pending_none_printed
  & !changed.
- **Candidate:** While the release of a repository is `own`, when the person runs `migrate upgrade`, `migrate` shall
  print "no upgrade step is pending" and change nothing.
- **Constructs:** OF (attribute as subject). **Removes:** current (whose definition is one attribute value: a pure
  synonym). **Survives:** `own`.
- **Parses today:** no as written; **"While a repository is `own`, ..." parses today**, so "current" was never needed.
  It reads worse ("a repository is `own`" does not say own what); the OF form names the attribute.

### migration-tools#r25

- **Current:** While the repository is unframed, when the person runs `migrate upgrade`, `migrate` shall rewrite
  `spec/index.md` and print "verb frames" and "v_t11". (unframed: `.shop/plugin-version` names a release after 1.0.0
  and before 3.0.0.)
- **ACE:** If the plugin-version of a repository is after "1.0.0" and is before "3.0.0" and the person runs "migrate
  upgrade" then Migrate must rewrite "spec/index.md" and must print "verb frames" and must print "v_t11". (ACE has
  comparison of numbers, not of version strings; "after"/"before" here would be ordinary relations needing axioms.)
- **SBVR:** It is obligatory that migrate rewrites spec/index.md and prints verb frames and v_t11 if the person runs
  migrate upgrade in a repository whose plugin version is after 1.0.0 and before 3.0.0.
- **FRETish:** in version_gt_1 & version_lt_3 mode, upon upgrade_run, migrate shall at the next timepoint satisfy
  index_rewritten & frames_printed & v_t11_printed. (FRET handles numeric comparison natively if the version is a
  number; a version string is not.)
- **Candidate:** While the plugin version of a repository is after `1.0.0` and before `3.0.0`, when the person runs
  `migrate upgrade`, `migrate` shall rewrite `spec/index.md` and print "verb frames" and "v_t11".
- **Constructs:** OF, COMPARE (an order on release values). **Removes:** unframed. **Vocabulary:** an order on the
  values of release (the glossary already lists them in order: `0.23.1` ... `own`).
- **Alternative:** the domain notion is "the upgrade step "verb frames" is pending": "While the upgrade step "verb
  frames" is pending for a repository" (HISTORY in effect: a step the repository has not applied). That would need
  *upgrade step* as a kind with a status, and is the better long-term model; the version range is how it is computed.
- **Example data:** `1.0.0`, `3.0.0` are release boundaries of the spec, not example data; "verb frames" and "v_t11"
  are what is printed (a step name and a finding code), specified content.
- **Parses today:** no.

### migration-tools#r8

- **Current:** While an untracked file is uncommitted, if the person runs `migrate run --context
  example.org/acme/shop`, then `migrate` shall exit with an error naming the untracked file and change nothing.
  (uncommitted: an untracked file whose text no commit holds.)
- **ACE:** If no commit holds the text of an untracked-file and the person runs "migrate run" on a bounded-context then
  Migrate must exit with an error that names the untracked-file and must change nothing. (**Scope:** in ACE, "no
  commit" takes scope over "an untracked-file", giving "there is no commit that holds the text of any untracked file",
  which is wrong. ACE's way out is to put the file first: "If an untracked-file has a text and no commit holds the
  text then ...".)
- **SBVR:** It is obligatory that migrate exits with an error that names the untracked file and changes nothing if the
  person runs migrate run on a bounded context and the text of an untracked file is held by no commit.
- **FRETish:** in uncommitted_untracked mode, upon migrate_run, migrate shall at the next timepoint satisfy error_exit
  & names_file & !changed.
- **Candidate:** While no commit holds the text of an untracked file, if the person runs `migrate run` on a bounded
  context, then `migrate` shall exit with an error naming the untracked file and change nothing.
- **Constructs:** NEG-EXIST (subject), OF, EXAMPLE-DATA-OUT. **Removes:** uncommitted (and its clash with
  design-model-check's other "uncommitted"). **Vocabulary:** relation commit | holds | text, text | of | file.
- **Reading rule needed:** the same scope problem as ACE. The candidate needs a written rule that an indefinite
  inside a While clause takes wide scope (it is read "for any untracked file"), or the line must be ordered
  "While the text of an untracked file is in no commit". This is phase 1's hypothesis 2 showing up in a real line.
- **Example data:** `--context example.org/acme/shop` is example data: the given block supplies the context.
- **Parses today:** no.

### migration-tools#r21

- **Current:** While a repository is misversioned, when the SessionStart hook runs `migrate status --hook`, `migrate`
  shall print "holds no version" and "banana". (misversioned: `.shop/plugin-version` holds no version.)
- **ACE:** If the plugin-version-file of a repository holds no version and the SessionStart-hook runs "migrate status
  --hook" then Migrate must print "holds no version" and must print the text of the plugin-version-file.
- **SBVR:** It is obligatory that migrate prints holds no version and the text of the plugin version file if the
  SessionStart hook runs migrate status --hook in a repository whose plugin version file holds no version.
- **FRETish:** in version_unreadable mode, upon status_hook_run, migrate shall at the next timepoint satisfy
  message_printed & file_text_printed.
- **Candidate:** While the plugin version file of a repository holds no version, when the SessionStart hook runs
  `migrate status --hook`, `migrate` shall print "holds no version" and the text of the plugin version file.
- **Constructs:** NEG-EXIST, OF, EXAMPLE-DATA-OUT. **Removes:** misversioned. **Vocabulary:** kind *plugin version
  file* (`.shop/plugin-version`; today *plugin version* is the value and the file at once), relation file | holds |
  version, or CONFORMS: "does not conform to the version format".
- **Example data:** "banana" is the test's file content. The line's meaning is "prints what the file holds", which the
  candidate says; "banana" goes in the given block.
- **Parses today:** no.

### feature-file-tools#r3

- **Current:** While the feature file `features/notes.feature` is nested, when the person runs `features list --tag
  slice-9`, `features` shall exit successfully, and `features` shall not print the feature file
  `features/notes.feature`. (nested: a feature file with a docstring whose text has a tag and a `Scenario:` line.)
- **ACE:** If a feature-file has a docstring and the text of the docstring has a tag and has a scenario-line and the
  person runs "features list" with the tag then Features must exit successfully and Features must not print the
  feature-file. ("`Scenario:` line" becomes scenario-line; ACE has no backquoted literal inside a noun.)
- **SBVR:** It is obligatory that features exits successfully if the person runs features list with a tag. It is
  prohibited that features prints a feature file that has a docstring whose text has the tag and a Scenario: line if
  the person runs features list with that tag.
- **FRETish:** in tag_only_in_docstring mode, upon list_run_with_tag, features shall at the next timepoint satisfy
  success_exit & !file_printed. (The tie between "the tag" in the condition and in the command is lost.)
- **Candidate:** While a feature file has a docstring whose text has a tag and a `Scenario:` line, when the person runs
  `features list` with the tag, `features` shall exit successfully and not print the feature file.
- **Constructs:** HAS, WHOSE-REL, NP-LIST (two objects of "has"), WITH-ARG, VP-COORD-NEG, EXAMPLE-DATA-OUT.
  **Removes:** nested. **Vocabulary:** kinds *docstring*, *tag*, *`Scenario:` line*; relations feature file | has |
  docstring, docstring | text, text | has | tag / line; the `--tag` option as "with <tag>".
- **Note:** the candidate is clearer than the original: "the tag" refers back to the tag inside the docstring, which is
  the point of the requirement (a tag only in a docstring does not count). The original hid that in "nested" and in
  example data (`slice-9`).
- **Example data:** `features/notes.feature` and `slice-9`, both to the given block.
- **Parses today:** no.

### feature-file-tools#r14

- **Current:** While the test module `tests/test_cart.py` is sweeping, when the person runs `features bindings
  --unbound`, `features` shall exit successfully. (sweeping: binds every scenario of a feature file with one
  `scenarios(...)` call.)
- **ACE:** If a test-module binds every scenario of a feature-file with exactly 1 scenarios-call and the person runs
  "features bindings --unbound" then Features must exit successfully. (ACE needs "exactly 1" for a count; "one" alone
  is "a". "with ..." attaches to "binds", right here.)
- **SBVR:** It is obligatory that features exits successfully if the person runs features bindings --unbound and a test
  module binds each scenario of a feature file with exactly one scenarios(...) call.
- **FRETish:** in module_binds_all mode, upon unbound_run, features shall at the next timepoint satisfy success_exit.
- **Candidate:** While a test module binds every scenario of a feature file with one `scenarios(...)` call, when the
  person runs `features bindings --unbound`, `features` shall exit successfully.
- **Constructs:** OF, COUNT ("one" as exactly one, or simply "a"), ADJUNCT-PP ("with"), EVERY (exists),
  EXAMPLE-DATA-OUT. **Removes:** sweeping. **Vocabulary:** verb *bind* (frame: test module binds scenario, with
  call); kind *`scenarios(...)` call*.
- **Weakness of the line itself:** "exit successfully" says little; what the person cares about is "and not print a
  scenario of the feature file". Every rewrite inherits that. Worth a separate look (not part of b112's question).
- **Example data:** `tests/test_cart.py` to the given block.
- **Parses today:** no.

### trials#r1

- **Current = Candidate:** When a session runs `trial-runner` on a trial, `trial-runner` shall start the trial.
- **ACE:** If a session runs Trial-runner on a trial then Trial-runner must start the trial.
- **SBVR:** It is obligatory that trial-runner starts each trial that a session runs trial-runner on. (SBVR's
  relative-clause style reads badly here; "if a session runs trial-runner on the trial" is better.)
- **FRETish:** upon runner_invoked, trial_runner shall at the next timepoint satisfy trial_started.
- **Constructs:** none. **Parses today:** yes.

### trials#r2

- **Current:** `trial-runner` shall read only a target.
- **ACE:** Trial-runner reads nothing but files of a target. / It is necessary that Trial-runner does not read a file
  that is not in a target. (ACE's "nothing but" is its "only".)
- **SBVR:** It is obligatory that trial-runner reads only files of the target of the trial. (Operative: it is a
  behaviour trial-runner could break, so obligation, not necessity.)
- **FRETish:** trial_runner shall always satisfy !read_outside_target. (FRET's natural form for an invariant.)
- **Candidate:** `trial-runner` shall read only files of its target.
- **Constructs:** ONLY (exists), OF, POSS. **Removes:** none. **Vocabulary:** relation file | of | target (or "in").
  The line is an invariant (Dwyer universality): its route is a check or judgement, not a scenario.
- **Note:** the agent definition says trial-runner reads "the target and the plugin's scripts"; the glossary's
  *target* includes the plugin's scripts, so the line is right, but only through the definition of target.
- **Parses today:** no ("its target" refused; "only a target", today's line, parses).

### trials#r4

- **Current:** When `trial-runner` ends a trial, `trial-runner` shall write a measurement and name the target.
- **ACE:** If Trial-runner ends a trial then Trial-runner must write a measurement of the trial that names the target of
  the trial. (ACE attaches the relative clause to the nearest noun, "the trial", which is wrong; it would need
  "a measurement that is of the trial and that names ...".)
- **SBVR:** It is obligatory that trial-runner writes a measurement of the trial that names the target of the trial if
  trial-runner ends the trial. (Same attachment ambiguity, and SBVR has no rule to settle it.)
- **FRETish:** upon trial_ended, trial_runner shall at the next timepoint satisfy measurement_written &
  target_named.
- **Candidate:** When `trial-runner` ends a trial, `trial-runner` shall write a measurement of the trial that names the
  target of the trial.
- **Constructs:** RC-SUBJ with a thing as subject, SENSE ("a measurement names", beside the frame "agent names
  thing"), OF. **Removes:** none; it fixes a vagueness (the current "name the target" does not say where).
- **Attachment:** the relative clause follows "of the trial" and could attach to it. A typed grammar settles it by the
  frame (a trial does not name a target, if the relation row is measurement | names | target), which ACE and SBVR
  cannot do. Shorter: "write a measurement that names the target of the trial".
- **Parses today:** no ("a measurement that names" is refused: "the verb name takes as its subject agent").

### design-model-check#r60

- **Current:** If the person runs `model check` on a term that is frameless, then `model` shall exit with an error
  naming the term. (frameless: a verb whose glossary entry does not name the kinds of its subject and object, nor say
  that it takes no object.)
- **ACE:** If the person runs "model check" on a verb and the glossary-entry of the verb has no frame then Model must
  exit with an error that names the verb.
- **SBVR:** It is obligatory that model exits with an error that names the verb if the person runs model check on a
  verb whose glossary entry has no frame.
- **FRETish:** upon check_run & frameless_verb_present, model shall at the next timepoint satisfy error_exit &
  names_verb.
- **Candidate:** If the person runs `model check` on a verb whose glossary entry has no frame, then `model` shall exit
  with an error naming the verb.
- **Constructs:** WHOSE-REL, HAS, NEG-EXIST. **Removes:** frameless. **Vocabulary:** kind *verb* (a term whose part of
  speech is verb), *glossary entry*, *frame* (the `Frame:` field: a real domain noun, so it stays a term).
- **Note:** the 22-word definition hides a second clause ("nor say that it takes no object"); in the candidate that is
  in the definition of *frame*, where it belongs (a frame either names an object kind or says there is none).
- **Parses today:** no ("verb" is not a kind).

### design-model-check#r69

- **Current:** When the person runs `model parse` on a requirement that is prepositioned, `model` shall exit
  successfully. (prepositioned: a requirement with a prepositional verb followed by its preposition and its object, as
  in `a viewer subscribes to a channel`.)
- **ACE:** If the person runs "model parse" on a requirement that uses a prepositional-verb then Model must exit
  successfully.
- **SBVR:** It is obligatory that model exits successfully if the person runs model parse on a requirement that uses a
  prepositional verb.
- **FRETish:** upon parse_run & line_has_prep_verb, model shall at the next timepoint satisfy success_exit.
- **Candidate:** When the person runs `model parse` on a requirement that uses a prepositional verb, `model` shall exit
  successfully.
- **Constructs:** RC-SUBJ with a thing as subject, SENSE or a relation row (requirement | uses | term),
  EXAMPLE-DATA-OUT. **Removes:** prepositioned. **Vocabulary:** kind *prepositional verb* (a verb whose frame names a
  preposition: a real notion of the frame model, kept), relation requirement | uses | term.
- **Example data:** "a viewer subscribes to a channel" is the example; it goes in the given block as the requirement's
  text.
- **Parses today:** no ("a requirement that uses" is refused: "the verb use takes as its subject agent").

### conversation#r2

- **Current:** When the UserPromptSubmit hook runs `work quote --hook`, `work` shall keep the session.
- **ACE:** If the UserPromptSubmit-hook runs "work quote --hook" then Work must record the session in the git-directory.
- **SBVR:** It is obligatory that work records the session in the git directory if the UserPromptSubmit hook runs work
  quote --hook.
- **FRETish:** upon quote_hook_run, work shall at the next timepoint satisfy session_recorded.
- **Candidate:** When the UserPromptSubmit hook runs `work quote --hook`, `work` shall record the session in the git
  directory.
- **Constructs:** ADJUNCT-PP ("in"), SENSE. **Removes:** none. **Vocabulary:** verb *record* (frame: agent records
  thing, in place); kind *git directory*.
- **Finding:** the line uses *keep* in a sense its own glossary entry does not have. role-boundaries defines keep as
  "a session leaves a thing as it was"; here it means "stores". One word, two meanings: the vocabulary weakness phase
  1 named (7). The candidate uses a different verb rather than a second frame.
- **Parses today:** no ("record" is not a verb).

### telemetry#r1

- **Current:** When the person runs `measure batch` on a batch that is `merged`, `measure` shall write a measurement
  of the batch, include "wall time", include "session time", include "tokens" and include "cost by role".
- **ACE:** If a batch is merged and the person runs "measure batch" on the batch then Measure must write a measurement
  of the batch that includes "wall time" and that includes "session time" and that includes "tokens" and that
  includes "cost by role". (ACE coordinates relative clauses by repeating "that"; a coordinated object list of
  strings is not ACE.)
- **SBVR:** It is obligatory that measure writes a measurement of the batch that includes wall time, session time,
  tokens and cost by role if the person runs measure batch on a batch that is merged.
- **FRETish:** in batch_merged mode, upon measure_run, measure shall at the next timepoint satisfy measurement_written
  & has_wall_time & has_session_time & has_tokens & has_cost_by_role.
- **Candidate:** While a batch is `merged`, when the person runs `measure batch` on the batch, `measure` shall write a
  measurement of the batch that includes "wall time", "session time", "tokens" and "cost by role".
- **Constructs:** STATE-MOVE, RC-SUBJ with a thing as subject, NP-LIST, SENSE. **Removes:** none. **Survives:**
  `merged`.
- **Finding:** the current line makes `measure` the subject of "include", and the glossary's frame for include says
  so (`measure` includes measurement): the verb was framed to fit a line whose agent is wrong. The measurement
  includes the figures; `measure` writes it. The candidate needs include's frame to be text | includes | text (a
  relation row), which the grammar refused today: "the verb include takes as its subject `measure`".
- **Parses today:** no.

### universal#U4

- **Current:** `work` shall commit every transition and push the commit.
- **ACE:** If Work makes a transition then Work must commit the transition and must push the commit. ("the commit" with
  no antecedent: ACE introduces a new entity, which loses the link to the transition; ACE would want "must commit the
  transition in a commit and must push the commit".)
- **SBVR:** It is obligatory that work commits each transition that work makes and pushes the commit of that
  transition.
- **FRETish:** upon transition_made, work shall at the next timepoint satisfy committed & pushed. (Or, as an invariant
  checked after each scenario, `work shall always satisfy !uncommitted_transition`.)
- **Candidate:** When `work` makes a transition, `work` shall commit the transition and push the commit.
- **Constructs:** TRIGGER-AS-ACTION (an action of `work` itself as trigger). **Removes:** none. **Vocabulary:** verb
  *make* (frame: agent makes transition), or "writes a transition", since the glossary defines a transition as
  "written by `work`" (write exists: "When `work` writes a transition" may parse with today's verbs).
- **Note:** the current ubiquitous form is a hidden response rule (each transition, then a commit). Saying it as When
  makes the pattern visible and with it the route: a check after each scenario, as U4 is checked today. "the commit"
  has the same missing-antecedent problem in every form; "push the commit of the transition" (OF) fixes it.
- **Parses today:** no ("makes").

### universal#U7

- **Current = Candidate:** A worker shall change only files in its worktree.
- **ACE:** Every worker changes nothing but files that are in the worktree of the worker. / It is obligatory that ... is
  not ACE; "must": Every worker must change nothing but files that are in a worktree of the worker.
- **SBVR:** It is obligatory that each worker changes only files that are in the worktree of the worker.
- **FRETish:** worker shall always satisfy !changes_outside_worktree.
- **Constructs:** ONLY, POSS (both exist). An invariant: route is a check or judgement.
- **Parses today:** yes.

### universal#U11

- **Current:** If a tool refuses a command, then the tool shall exit with an error naming the reason and change
  nothing.
- **ACE:** If a tool refuses a command for a reason then the tool must exit with an error that names the reason and must
  change nothing. (Without "for a reason", ACE reads "the reason" as a new entity: no antecedent.)
- **SBVR:** It is obligatory that a tool exits with an error that names the reason of the refusal and changes nothing
  if the tool refuses a command.
- **FRETish:** upon command_refused, tool shall at the next timepoint satisfy error_exit & reason_named & !changed.
- **Candidate:** If a tool refuses a command for a reason, then the tool shall exit with an error naming the reason and
  change nothing.
- **Constructs:** ADJUNCT-PP ("for"). **Removes:** none. **Vocabulary:** refuse's frame with a "for" reason; kind
  *reason*.
- **Note:** today's "the reason" is a definite with no antecedent, which the check reads as "the only reason"
  (phase 1, weakness 2). The candidate gives it one.
- **Parses today:** no ("for").

## 3. Results

### 3.1 Which candidates parse today

5 of 27 parse as written: requests#r24, batches#r8, batches#r16, trials#r1, universal#U7 (four of them unchanged lines).
Three more have a variant that parses today and removes the adjective with no grammar change: batches#r13 ("a commit
of an item in a batch cites no item"), migration-tools#r14 ("a repository is `own`"), batches#r17 (today's line).
So **2 of the 15 coined adjectives in the sample (uncited, current) were never needed by the grammar**: the relation
clause and the attribute value were there.

The refusals are informative in themselves: "a measurement that names", "a requirement that uses" and "a measurement
that includes" parse up to the verb and are then refused by the verb's frame, whose subject is an agent. The grammar
has subject relative clauses from verbs; what it lacks is the second sense of verbs whose subject is a document
(names, uses, includes).

### 3.2 Construct counts (the 27 candidates)

| Construct | Lines | Which |
|---|---|---|
| OF (new rows, attribute as subject, any slot) | 11 | r38, b13, bl20, m19, m14, m25, m8, m21, f14, t2, t4 |
| EXAMPLE-DATA-OUT | 6 | m19, m8, m21, f3, f14, d69 |
| NEG-EXIST (subject, after has/with) | 5 | r6, m19, m8, m21, d60 |
| ADJUNCT-PP | 4 | b17, f14, c2, U11 |
| SENSE (second frame of a word) | 4 | t4, d69, tel1, c2 |
| RC-SUBJ (thing as subject) | 3 | t4, d69, tel1 |
| WHOSE-REL | 3 | bl21, f3, d60 |
| VP-COORD-NEG | 3 | r33, m19, f3 |
| STATE-MOVE | 3 | r6, r24, tel1 |
| CONFORMS | 2 | r33, r38 |
| HAS | 2 | f3, d60 |
| COMPARE | 2 | bl21, m25 |
| REL-COPULA | 2 | bl20, bl21 |
| WITH-ARG | 2 | r6, f3 |
| NP-LIST | 2 | f3, tel1 |
| POSS (new kinds) | 2 | r38, t2 |
| COUNT | 1 | f14 |
| TRIGGER-AS-ACTION | 1 | U4 |
| RC-OBJ, NEVER/ALWAYS, MAY, ONLY-AFTER, HISTORY | 0 | (m25's alternative would use HISTORY) |

(r = requests, b = batches, bl = backlog, m = migration-tools, f = feature-file-tools, t = trials, d =
design-model-check, c = conversation, tel = telemetry.)

Read with care: the sample is 27 lines, picked for their adjectives. Most of the gain comes from three constructs, OF,
NEG-EXIST in more positions and WHOSE over relations, and from vocabulary (relation rows) more than grammar. CONFORMS
is the owner's construct and fits two lines here; it would fit more of the 145 prose conditions (every "malformed",
"unreadable", "does not parse").

### 3.3 Adjectives: removed and surviving

All 15 coined adjectives in the sample go: unreadable, unparsed, originless, uncited, tasked, tracking, idle, current,
unframed, uncommitted, misversioned, nested, sweeping, frameless, prepositioned. Three of them (unparsed, uncommitted,
uncited) have a second, different sense elsewhere in the spec; the rewrite removes the clash.

Surviving, and why:

| Word | What it is | Why it stays |
|---|---|---|
| `accepted`, `building`, `done`, `in-review`, `in-batch`, `idea`, `merged` | status values | an enumerated attribute with transitions; the logic reads them as fluents and Gherkin sets them directly; they are the domain's own states |
| `own` | a value of release | the same; better written with its attribute ("the release of a repository is `own`") |
| open (of initiative) | a defined condition | its definition parses in the Def grammar and derives from status values; ordinary English; removable with "every initiative ... is `done` or `abandoned`" |
| frame, prepositional verb, comment schema, requirement grammar | nouns | real domain things (a field, a kind of verb, artifacts), not adjectives; the owner's rule is about adjectives that pack a structure, not about nouns that name things |

### 3.4 Verbosity

| | Current | Candidate |
|---|---|---|
| Words, 27 lines | 592 | 710 |
| Mean words per line | 21.9 | 26.3 (+20%) |
| The 15 lines with a coined adjective | 366 (24.4 mean) | 456 (30.4 mean, +25%) |
| Their 15 definitions | 189 words | 0 |
| Line + definition, 15 lines | 555 | 456 (-18%) |

The candidate lines are longer by about six words each, but the reader no longer has to look up a definition, and the
definitions themselves (189 words) disappear. A definition shared by many lines is paid once today; I did not count
how often each of the 15 is used. The longest growth is where a definition had two parts (idle +12, misversioned +12
with the example data replaced by what it stands for).

Per-line counts:

| Line | Current | Cand. | Line | Current | Cand. |
|---|---|---|---|---|---|
| requests#r33 | 23 | 27 | migration-tools#r8 | 28 | 34 |
| requests#r38 | 31 | 39 | migration-tools#r21 | 21 | 33 |
| requests#r6 | 24 | 23 | feature-file-tools#r3 | 28 | 35 |
| requests#r24 | 29 | 31 | feature-file-tools#r14 | 18 | 26 |
| batches#r8 | 41 | 41 | trials#r1 | 13 | 13 |
| batches#r13 | 34 | 38 | trials#r2 | 6 | 8 |
| batches#r17 | 20 | 26 | trials#r4 | 14 | 20 |
| batches#r16 | 19 | 19 | design-model-check#r60 | 22 | 25 |
| backlog#r20 | 24 | 29 | design-model-check#r69 | 16 | 18 |
| backlog#r21 | 27 | 36 | conversation#r2 | 13 | 17 |
| migration-tools#r19 | 27 | 39 | telemetry#r1 | 33 | 33 |
| migration-tools#r14 | 22 | 25 | universal#U4 | 9 | 14 |
| migration-tools#r25 | 21 | 29 | universal#U7 | 9 | 9 |
| | | | universal#U11 | 20 | 23 |

## 4. The three languages on these lines

### 4.1 What the sample needs, and does not

All 27 lines are next-step effect rules (When/If -> shall) or invariants (trials#r2, U7, and U4 as a hidden response).
None needs "may", "always/never" as a new construct, "only after" or a timing bound. The sample was chosen for its
adjectives, not its time structure, so this says nothing about the rest of the spec; it does say the adjective problem
is a noun-phrase problem, not a time or modality problem.

### 4.2 Each language

**ACE does better** on noun phrases: relative clauses, "of", "no", "every", "exactly 1" are all standard, and its
interpretation rules settle scope and definites. It caught two real problems the candidate also has: "no commit holds
the text of an untracked file" takes the wrong scope (m8), and "the reason" / "the commit" with no antecedent (U11, U4)
introduce new entities. **ACE does worse** on everything EARS gives: no While/When/If distinction (one if-part, state
and event mixed), so the state-versus-behaviour split the owner wants is lost; commands are untyped strings;
hyphenated compounds (request-line, pull-request, plugin-version-file) read worse; relative clauses attach to the
nearest noun, which misreads t4; a list of strings as objects needs "that includes ... and that includes ..." (tel1).
Length is about the same as the candidate.

**SBVR does better** on modality: an obligation and a prohibition are separate rules, so r33 and m19 split into two
rules each, which is honest about what each tests; trials#r2 and U7 are cleanly operative ("obligatory"), and SBVR
would call a structural truth "necessary". **SBVR does worse** on order and form: the response comes first and the
condition last, the reverse of EARS and of Given/When/Then; there is no formal grammar, so the attachment in t4 and the
scope in m8 are left to the reader; "It is obligatory that" adds four words to every line; repeated conditions when a
rule splits.

**FRETish does better** on the frame of a line: While maps to a scope (mode) and When to an `upon` condition, which is
exactly the state/event split the owner wants, and timing is explicit (`at the next timepoint`). It states effects as
resulting states (`!requirement_on_branch`), which suits Gherkin's Then. It handles r6 (three booleans) and m25
(numeric comparison) directly. **FRETish does worse** on everything else: it is propositional, so "a comment", "every
task of the batch", "the tag" of f3 and all relative clauses collapse into boolean variable names. Every coined
adjective becomes an opaque variable (`comment_nonconforming`, `upstream_renamed`): FRET has the coined-adjective
problem by design, since its vocabulary is a list of variables. It fits every line here as a pattern; it fits none as
a description of the domain.

### 4.3 The candidate's remaining weak spots

1. **Scope of "no" before an indefinite** (m8). Needs a written reading rule (an indefinite in a While clause is read
   "any") or word order that avoids it. This is a reading-rules question for the DRS-like layer phase 1 proposed.
2. **Definites with no antecedent** ("the commit" in U4, "the reason" in U11, "the upstream" if written without
   "its"): the candidate fixes them one by one; a rule is better ("the X of Y", or refuse a "the" with no antecedent
   unless the kind has one instance).
3. **Attachment of a relative clause after an of-phrase** (t4). Typed frames settle it when the relation row exists;
   the grammar should refuse the line when both attachments type-check.
4. **Verbs with a thing as subject** (names, uses, includes, holds, cites, binds). Today one frame per verb, mostly
   with an agent subject. Either relation rows (thing | names | thing) or a second frame per verb. Four of 27 lines
   hit it.
5. **One word, two meanings** (keep in c2; include in tel1 framed to fit a wrong agent). A rewrite exposes these;
   the vocabulary check should too.
6. **Refusal responses** are long and identical. With U11, "then `work` shall refuse the command and name the request
   line" would say the same and save 3-4 words on 7 sample lines (about 200 lines spec-wide, phase 1's count of fixed
   responses), but it makes "exit with an error and change nothing" an entailed Then rather than a stated one, which
   needs the entailment check phase 1 found missing. I kept today's responses for that reason.
7. **"different" and "after/before"** (bl21, m25) compare values; both need an order or identity on attribute values
   that the glossary does not carry.
8. **Thin responses** ("exit successfully" in f14, d69): the rewrite cannot add what the line never said.
9. **Object relative clauses** ("a comment that a session posts") were not needed in the sample but are the natural
   form for many relation lines; RC-OBJ is still missing.

## Sources

- Fuchs, N. E., Kaljurand, K., Kuhn, T. ACE 6.7 Construction Rules and Interpretation Rules,
  attempto.ifi.uzh.ch/site/docs/ (as quoted in phase 1's `logic-cnls.md` §2.3-2.4).
- OMG, Semantics of Business Vocabulary and Business Rules 1.5 (formal/19-10-02), 2019, Annex (SBVR Structured
  English); "SBVR Speaks" series, Business Rules Journal 7, 2006 (as quoted in `logic-cnls.md` §3).
- Giannakopoulou, D., Pressburger, T., Mavridou, A., Schumann, J. Automated formalization of structured natural
  language requirements. Information and Software Technology 137, 2021; FRET user manual, github.com/NASA-SW-VnV/fret
  (as quoted in `requirement-cnls.md` §2).
- Dwyer, M. B., Avrunin, G. S., Corbett, J. C. Patterns in property specifications for finite-state verification.
  ICSE 1999 (`requirement-cnls.md` §4).
- This repository: `python3 scripts/model parse` on main, 2026-11-08; `spec/index.md`, `spec/capabilities/*.md`.
