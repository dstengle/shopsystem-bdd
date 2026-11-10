# The language of grammar 4: its reading rules

What each construct of a grammar 4 requirement means, as the reading rules R1-R12 of the CNL 4 design (call 5,
section 7.3; I11b). A line's meaning is its logical form (`scripts/spec_lf.py`), which `model parse --form` prints:
its modality and the referents no part introduces (actors and codes as constants, a code that is no word of the
context as a parameter, the run's own things as indexicals), then its Where, While, trigger and response, each a box
of referents, atoms and boxes. `scripts/spec_lf_read.py` holds the rules that resolve a word or refuse a line;
`model parse` refuses a line one of them refuses, naming the words, with its tree.

Each rule names the real lines it was tested on. Those lines are still codified-1, in grammar 3, until this
repository's glossary and rewords (I20-I27); each rule's construct is shown here on a twin in the words of the
smallest codified-2 context (`tests/scripts/fixtures/codified-2/`: the CLI pack, sessions, stages, files and
worktrees). Each block below is a line and what grammar 4 reads it as: its logical form, or its refusal.
`tests/scripts/test_spec_lf_read.py` reads every block and fails when grammar 4 reads its line otherwise.

## R1. "a K": any K in a condition or a trigger, a new K in a response

"a K" in a While clause, a Where clause or a trigger is a referent of that part, any K: the line holds for each K
that meets it, and the response may name it again with "the K". In a response, "a K" is a new K the response brings
about. A bare plural in a response reads as "every" (R6).

Tested on requests r33 ("While a comment is unreadable, when a session runs `work sync`, `work` shall print the
comment ...": each unreadable comment is printed) and batches r13 ("While a commit of an item in a batch is uncited
...": any such commit refuses the review).

```reading
While a stage is `open`, when a session ends the stage, `work` shall print the stage.
shall [x3: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
  when [x2: session]
    end(e1, subject: x2, object: x1)
  response
    print(e2, subject: x3, object: x1)
```

```reading
When a session ends a stage, `work` shall write a file.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: file]
    write(e2, subject: x3, object: x4)
```

The subject of a response with no trigger ("A session shall ...", U7) is a response referent here too; how the
check reads an actor kind's line is I12a's.

So "a K" in a response never names a K the line gave before: where the line means one it gave, it says "the K"
(R2). The audit found two lines that say "a K" where an earlier one is meant: requests r63 ("`work` shall assign the
line outcome of a request line proposed in the request", one line of the request, not a new one) and
design-model-check r199 ("`model` shall use an interpreter that imports `clingo`", the interpreter it has, not a new
one). Their twins, each read as it is said and as it is meant:

```reading
When a session ends a stage, `work` shall print the status of a stage.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: stage, x5: status]
    status(x4) = x5
    print(e2, subject: x3, object: x5)
```

```reading
When a session ends a stage, `work` shall print the status of the stage.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: status]
    status(x2) = x4
    print(e2, subject: x3, object: x4)
```

```reading
While a session follows a stage, when the person runs `work start`, `work` shall end a stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response [x6: stage]
    end(e2, subject: x5, object: x6)
```

```reading
While a session follows a stage, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x2)
```

## R2. "the K" binds to something the line gave, else it is refused

"the K" binds to the latest earlier referent of kind K (or of a kind under K) in the line: one a part introduced, an
actor, a code or an indexical. Else to the image of a relation row `K | of | S` of the one earlier referent of kind S
("the worktree" after "a session" is the worktree of the session). Else, when K's entry has `This:`, to the run's own
K (R11). Else the line is refused, naming the noun: "the" never means the only K in the world. "Earlier" is said
before it in the line: a "the K" that only a later noun phrase gives is refused too. A referent whose noun phrase
holds the "the K" gives it nothing: in "a stage that precedes the stage" the stage is an earlier one, never the stage
the relative clause restricts, and with no earlier stage the line is refused (design-model-check r162,
feature-file-tools r24).

A referent made inside a "no", "not", "every" or "only" box, a count's box or one case of an "or" gives nothing to
a "the K" outside that box (DRS accessibility): "the K" binds to the latest earlier referent of kind K not inside
such a box that does not hold it, and when every earlier K is inside one the line is refused, naming the noun and the
box (design-model-check r166, r167, feature-file-tools r31; the boxes of a count and of "or" under Constructs).
A K of a pair "two Ks" gave is no antecedent of "the K", which names neither of them; "another K" and "the same K"
bind by this rule too (identity and distinctness, under Constructs).

"the K of X" (a row `K | of | S`) is the image of X by the row, a referent of its own: X is read first, wherever it
is said, and never an earlier K nor the K whose relative clause holds it. In "a review that lists the review of the
pull request" the review listed is the pull request's, not the review written; in "the worktree of every session" it
is inside the box of every session, one worktree of each (design-model-check r164, r165; feature-file-tools r29,
r30, b221).

Tested on design-model-check r58-r61 ("... `model` shall exit with an error naming the term": no term is given
before, so each is refused and is to be reworded) and migration-tools r13-r16 ("While the repository is behind
...": the repository is the run's own, an indexical once this repository's glossary gives `repository` a `This:`).

```reading
When a session ends a stage, `work` shall print the worktree.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: worktree]
    of(x4, x1)
    print(e2, subject: x3, object: x4)
```

```reading
When a session writes a file, `work` shall print the worktree of every session.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: file]
    write(e1, subject: x1, object: x2)
  response
    every [x4: session]
      scope [x5: worktree]
        of(x5, x4)
        print(e2, subject: x3, object: x5)
```

```reading
When the person runs `work start`, `work` shall print the command.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    print(e2, subject: x3, object: x2)
```

```reading
If `work` refuses a command, then `work` shall exit with an error naming the reason.
refused: "the reason" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a reason
```

```reading
When a session ends a stage that sessions follow, `work` shall print the worktree.
refused: "the worktree" has no antecedent: 2 earlier noun phrases may give it: say "the worktree of" one of them
```

```reading
While a session does not follow the stage, when a session ends a stage, `work` shall exit successfully.
refused: "the stage" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a stage
```

```reading
While a session follows a stage and no session follows a stage whose status is `done`, when the person runs `work start`, `work` shall print the stage.
shall [x5: agent the person (constant), x6: command `work start` (parameter), x7: tool `work` (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
    not [x3: session, x4: stage]
      status(x4) = `done`
      follow(subject: x3, object: x4)
  when
    run(e1, subject: x5, object: x6)
  response
    print(e2, subject: x7, object: x2)
```

```reading
While no session follows a stage, when the person runs `work start`, `work` shall print the stage.
refused: "the stage" has no antecedent: a stage is made inside "no session ...", which gives nothing outside it
```

## R3. "no K": there is no K, within its own clause

"no K" (and "nothing") is a `not` box over its referent and the rest of its own clause, and over nothing outside it.

Tested on migration-tools r8 ("... `migrate` shall exit with an error naming the untracked file and change
nothing": the error is said, and no thing is changed).

```reading
If `work` refuses a command, then `work` shall exit with an error naming the command and change nothing.
shall [x1: tool `work` (constant)]
  if [x2: command]
    refuse(e1, subject: x1, object: x2)
  response
    exit(e2, subject: x1, with an error naming: x2)
    not [x3: thing]
      change(e3, subject: x1, object: x3)
```

```reading
While a session has no worktree, when the person runs `work start`, `work` shall exit with an error naming the session.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: session]
    not [x2: worktree]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, with an error naming: x1)
```

## R4. "does not V a K" in a condition is refused; under "shall not", "a K" is any K

In a While or Where clause, "X does not V a K" (or a bare plural) reads two ways: "X Vs no K", and "there is a K that
X does not V". The line is refused, naming the words, and the writer says one of the two. In a response, "shall not
V a K" is a `not` box over the K: no K at all.

Tested on requests r53, which needs "some comment the request does not hold" (a comment that is unrecorded) and which
ACE's reading ("holds no comment") would break, and on U5 ("A session shall not write a status": no status at all).

```reading
While a session does not follow a stage, when the person runs `work start`, `work` shall exit successfully.
refused: the While clause says "does not follow a stage", which reads two ways: say "follows no stage" or "a stage that the session does not follow"
```

```reading
While a session follows no stage, when the person runs `work start`, `work` shall exit successfully.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: session]
    not [x2: stage]
      follow(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

```reading
While a stage that a session does not follow is `open`, when the person runs `work start`, `work` shall exit successfully.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage, x2: session]
    not
      follow(subject: x2, object: x1)
    status(x1) = `open`
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

```reading
When a session ends a stage, `work` shall not write a file.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response
    not [x4: file]
      write(e2, subject: x3, object: x4)
```

## R5. "X shall V only Ks that P": every K that X Vs meets P

"only" is an `only` box: its restrictor (the Ks and what restricts them) and its scope (the act). Every K the agent
Vs meets the restrictor; the line obliges no V. `model logic` reads it so (I12a): it clashes only with a line in
which the agent Vs a K known not to meet the restrictor (an attribute of another value), never with a V of a K that
may meet it.

Tested on U7 ("A worker shall change only files in its worktree") and trials r2 ("`trial-runner` shall read only a
target").

```reading
A session shall change only files in its worktree.
shall []
  response [x1: session]
    only [x2: file, x3: worktree]
      of(x3, x1)
      in(x2, x3)
      scope
        change(e1, subject: x1, object: x2)
```

## R6. "every K that P" in a response: for each such K

"every K" is an `every` box: its restrictor and its scope, the act done for each K. The scenario the generator writes
of such a line gives two Ks, so it is not met vacuously (the generator's part is I14a's). `model logic` reads it so
(I12a): the act is obliged of each K the restrictor allows, so it clashes with a line that forbids the act of a K of
that kind under the same trigger and state, though that line says more of its K ("a stage whose status is `done`").

Tested on batches r8 ("... and every task of the batch is `done` ...") and requests r37 ("... and every request line
proposed in the request is `refused` ...").

```reading
Where a stage is `open`, when a session writes a file, `work` shall print every file.
shall [x4: tool `work` (constant)]
  where [x1: stage]
    status(x1) = `open`
  when [x2: session, x3: file]
    write(e1, subject: x2, object: x3)
  response
    every [x5: file]
      scope
        print(e2, subject: x4, object: x5)
```

## R7. "one K" is exactly one; "a K" at least one

"a K" is at least one K (R1). A count before a number (one to ten) and a noun, "at least", "at most", "exactly",
"more than" or "fewer than", is a `count` box over its noun (call 4, I15): its bound and number, its restrictor and its
scope, the clause said of each K counted. "one K" alone is exactly one. A count that admits no K ("at most", "fewer
than") obliges no act, as "only" does not. `model logic` reads two counts of one act on one trigger and state: when no
number of Ks meets both, the pair is an L1 (I15).

Tested on U8 ("... a tool shall print one JSON object": exactly one).

```reading
When the person runs `work start`, `work` shall print one stage.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    count exactly 1 [x4: stage]
      scope
        print(e2, subject: x3, object: x4)
```

```reading
When the person runs `work start`, `work` shall print more than one stage whose status is `done`.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    count more than 1 [x4: stage]
      status(x4) = `done`
      scope
        print(e2, subject: x3, object: x4)
```

## R8. "its" binds to the subject of its clause, or the line is refused

"its K" (a row `K | of | S`) and "its T" (an attribute) are the image of the subject of the clause they are in. The
line is refused when that subject is of no kind the relation needs, or when another referent of such a kind was
given before it: the writer says "the K of" the one meant.

Tested on trials r2 and U7 ("A worker shall change only files in its worktree": the worker's own worktree).

```reading
When a session ends a stage, `work` shall print its status.
refused: "its status" binds to `work`, the subject of its clause, which has no status
```

```reading
When a session ends a stage that sessions follow, a session shall write a file in its worktree.
refused: "its worktree" binds to the session, the subject of its clause, and a session was given before it: say "the worktree of" one of them
```

## R9. When is an edge, While a level, If an unwanted event first

When names an event: the response follows at the next step. While names a state that holds when the event happens.
If names an unwanted event whose response takes precedence over a When line's at the same step (call 12). Every
state the response does not change keeps its value (inertia). The form keeps each part as its own box (`when`,
`while`, `where`, `if`); the check reads them so (I12a, I12b).

`model logic` reads the precedence as stated, never as a clash: an If line and a line of another form on one trigger
are no pair, since where the If line's state holds its response replaces the other's, and where it does not hold the
If line does not fire. Two If lines on one trigger are still checked against each other. A universal condition holds
in every trace, so it takes no precedence and none is taken over it: it is paired with each line it bears on, If or
not, and a line whose response it forbids under that line's trigger is an L1 naming it (b117). A pair of two
codified-1 lines keeps the reading of plugin 2.x (an If line never paired with a line of another form) until its
files are reworded.

Tested on backlog r20 and r21 (in a tasked repository `work idea` refuses, If; in a tracking one it writes, When).

```reading
Where a stage is `open`, while sessions follow the stage, if a session ends the stage, then `work` shall exit with an error naming the stage.
shall [x4: tool `work` (constant)]
  where [x1: stage]
    status(x1) = `open`
  while [x2: session]
    follow(subject: x2, object: x1)
  if [x3: session]
    end(e1, subject: x3, object: x1)
  response
    exit(e2, subject: x4, with an error naming: x1)
```

## R10. A literal that names no declared constant is a parameter

A code that is no word of the context is a parameter: the scenario's given block binds it (call 7). One that is a
word of the context is a constant.

Tested on migration-tools r21 ("... `migrate` shall print "holds no version" and "banana"": example data, not
words of the context).

```reading
When the person runs `work start`, `work` shall exit successfully.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    exit(e2, subject: x3, successfully)
```

## R11. "this K", and an unbound "the K" whose entry has `This:`, are the run's own K

"this K" of a kind whose entry has `This:` is an indexical: the run's own K, as the entry glosses it (call 6). An
unbound "the K" of such a kind is the same (R2).

Tested on requests r6 ("While a command is originless, if the person runs `work request` ...": the command is the
one the run runs) and r33 (the comment is one `work sync` reads).

```reading
When the person runs this command, `work` shall print this command.
shall [x1: agent the person (constant), x2: command "the command the run runs" (indexical), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    print(e2, subject: x3, object: x2)
```

## R12. A line that obliges with no trigger, and neither "always" nor "never", is refused

A line with no When or If, and neither "always" nor "never", would oblige its response in every state; it is
refused. A line whose response obliges nothing, "shall not" or "only", forbids or restricts in every state, which is
what it means, and stands.

Tested on phase 2 fault 2 of the design's research (lines that read as "in every state").

```reading
`work` shall write a file.
refused: the line has no trigger and neither "always" nor "never": it would oblige its response in every state
```

```reading
While a stage is `open`, `work` shall exit successfully.
refused: the line has no trigger and neither "always" nor "never": it would oblige its response in every state
```

```reading
`work` shall not change `spec/index.md`.
shall [x1: tool `work` (constant), x2: thing `spec/index.md` (parameter)]
  response
    not
      change(e1, subject: x1, object: x2)
```

## Modality: "shall", "may", "always" and "never"

A line's modality is the form's first word (I17; the design's section 4.5). "shall" obliges (scenarios). "may"
permits: it obliges nothing, so a "may" line with no trigger stands (R12 refuses only an obligation), and `model
logic` reports a "shall not" line that forbids what it permits, on one trigger or none, in a state both allow (L7).
"may not" reads two ways and is refused; so is a line that says both "shall" and "may". "always" and "never" say a
necessity: a line of no trigger over one state clause, its referents any K, as a While clause's are; a While clause
may come before it. `model logic` does not read a necessity yet: it is no premise of a pair and hides no finding,
and the check neither refuses it nor reports it.

```reading
A session may write a file.
may []
  response [x1: session, x2: file]
    write(e1, subject: x1, object: x2)
```

```reading
A session may not write a file.
refused: the line says "may not", which reads as "is not allowed to" and as "is allowed not to": say "shall not", or say what it may do
```

```reading
When a session ends a stage, the session may write a file, and `work` shall print the stage.
refused: the line says both "may" and "shall": say each in a line of its own
```

```reading
A session never follows a stage.
never []
  holds [x1: session, x2: stage]
    follow(subject: x1, object: x2)
```

## Time: moments compared, the clock, history

The time constructs of the CNL 4 design (section 4.4, call 9; I16), read with the rules above. The words of time are
the time pack's (`grammar/packs/time.md`: moment, duration, the units, a schedule a moment, the clock an agent whose
entry has `This:`, and reach); the constructs are the base grammar's (`grammar/Time.gf`, generated over a context's
kinds by `scripts/spec_rgl_time.py`) and their reading `scripts/spec_lf_time.py`'s:

- "x is after y", "x is before y": `cmp(x) after y`, y a moment of the line or a code; "is not" puts it under `not`.
- "x is within the last N units": `cmp(x) after now - N units`, now the moment of the trigger. A number where a
  duration is due takes a unit of the pack after it, or the line is refused.
- "S has V-ed O", the perfect of an action verb, is a state: the history of that action (call 3), set by the action
  and unset by nothing (`has V(...)`); "since m" is a role of it. "has not V-ed a K" in a condition is refused as R4
  refuses "does not V a K".
- "the clock reaches m" is a trigger like any other action; "the clock" with no antecedent is the run's own (R11).

`model logic` has no reading of a comparison or a history yet: it refuses a line holding one, naming it ("no
translation of a comparison of moments", "no translation of the history of end"), as it refuses any construct it
has no translation for. The blocks below are read in the time fixture
(`tests/scripts/fixtures/codified-2-time/`, a stage's deadline a moment) by `tests/scripts/test_spec_lf_time.py`.

```reading-time
While a deadline of a stage is within the last 7 days, when the person runs `work start`, `work` shall print the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: deadline, x2: stage]
    of(x1, x2)
    cmp(x1) after now - 7 days
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x2)
```

```reading-time
While a deadline of a stage is after `2026-01-01` and the deadline is not before `2027-01-01`, when a session ends the stage, `work` shall print the stage.
shall [x3: moment `2026-01-01` (parameter), x4: moment `2027-01-01` (parameter), x6: tool `work` (constant)]
  while [x1: deadline, x2: stage]
    of(x1, x2)
    cmp(x1) after x3
    not
      cmp(x1) before x4
  when [x5: session]
    end(e1, subject: x5, object: x2)
  response
    print(e2, subject: x6, object: x2)
```

```reading-time
While a deadline of a stage is within the last 7, when the person runs `work start`, `work` shall print the stage.
refused: the number 7 is a duration and takes a unit of the time pack after it: second, minute, hour, day, week
```

```reading-time
When the clock reaches a deadline of a stage, `work` shall print the stage.
shall [x1: clock "the clock of the run" (indexical), x4: tool `work` (constant)]
  when [x2: deadline, x3: stage]
    of(x2, x3)
    reach(e1, subject: x1, object: x2)
  response
    print(e2, subject: x4, object: x3)
```

```reading-time
While a session has written no file since `2026-01-01`, when the session ends a stage, `work` shall print the stage.
shall [x3: moment `2026-01-01` (parameter), x5: tool `work` (constant)]
  while [x1: session]
    not [x2: file]
      has write(subject: x1, object: x2, since: x3)
  when [x4: stage]
    end(e1, subject: x1, object: x4)
  response
    print(e2, subject: x5, object: x4)
```

```reading-time
While a session has not written a file, when the person runs `work start`, `work` shall exit successfully.
refused: the While clause says "has not written a file", which reads two ways: say "has written no file" or "a file that the session has not written"
```

## Constructs

The constructs grammar 4 is completed with (b240), one subsection a construct: what it says, the real lines the
audit (`.shop/records/2026-11-10-grammar-4-audit.md`) found it missing in, by id, and its twins, each a block of a
line in the words of a fixture context and the form it is meant to have, or `refused: <reason>`. A construct's
blocks are written before it is built, and fail until it is.

The acceptance test of the language is the spec corpus, `grammar/corpus/spec/` (its README): every live line of this
repository's spec in the new language with the reading it is meant to have, checked by
`tests/scripts/test_corpus_spec.py` (it parses to that reading, the reading translates to `model logic`'s facts and
to `features generate`'s steps, every live line of a codified-2 file has its block, and the line linearises back
word for word). This section's twins are the constructs' tests; the corpus is the language's.

### "the K" outside the box its K is made in, and the cases of "or"

R2's accessibility over every box a line can make: a "no" or "not" box, the box of "every K", "only Ks" and a count
("at least two Ks"), and each case of an "or" (two conditions, or two noun phrases, joined by "or": a case holds what
its side says, and either side may be the one that holds). A K made inside one of them gives nothing to a "the K"
said outside it, later in the same clause or in a later part, so the line is refused, naming the noun and the box.
A K made before the box is seen inside it.

Found by the audit in design-model-check r231 ("While a precondition of a requirement uses ... or the trigger of the
requirement uses ...": the second case's "the requirement" is the first case's), backlog r6 ("`work` shall print
every item, the title of the item, ...") and batches r4 ("`work` shall print every item in the batch, every task of
the batch and the status of the task"): each said "the K" outside the box its K is made in, and was read as if it
were not. Such a line says what it means another way, each K given outside the box, or the "the K" said inside it.

```reading
When the person runs `work start`, `work` shall print every stage and the status of the stage.
refused: "the stage" has no antecedent: a stage is made inside "every stage ...", which gives nothing outside it
```

```reading
When the person runs `work start`, `work` shall print every session and the worktree of the session.
refused: "the session" has no antecedent: a session is made inside "every session ...", which gives nothing outside it
```

```reading
While a session follows a stage or the session has a worktree, when the person runs `work start`, `work` shall exit successfully.
refused: "the session" has no antecedent: a session is made inside one case of an "or", which gives nothing outside it
```

```reading
While a stage is `open` or a stage is `done`, when the person runs `work start`, `work` shall print the stage.
refused: "the stage" has no antecedent: a stage is made inside one case of an "or", which gives nothing outside it
```

```reading
When the person runs `work start`, `work` shall print a stage or a file, and `work` shall end the stage.
refused: "the stage" has no antecedent: a stage is made inside one case of an "or", which gives nothing outside it
```

```reading
While at least two sessions follow a stage, when the person runs `work start`, `work` shall print the session.
refused: "the session" has no antecedent: a session is made inside "at least two sessions ...", which gives nothing outside it
```

```reading
When the person runs `work start`, `work` shall print at least two stages and the status of the stage.
refused: "the stage" has no antecedent: a stage is made inside "at least two stages ...", which gives nothing outside it
```

```reading
When the person runs `work start`, `work` shall not write a file, and `work` shall print the file.
refused: "the file" has no antecedent: a file is made inside "no file ...", which gives nothing outside it
```

A K made before the box is seen in each case: "the stage" in the first case below is the stage the session follows.

```reading
While a session follows a stage and the stage is `open` or the session has a worktree, when the person runs `work start`, `work` shall print the stage.
shall [x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
    or
      case
        status(x2) = `open`
      case [x3: worktree]
        of(x3, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x2)
```

### "X conforms to A": conformance to a named artifact

"X conforms to A" says that X meets what the artifact A sets out: a form, a schema, a layout, the language reference.
A is a noun of a kind under `artifact` (the CLI pack's noun), said as a proper noun ("the comment form"), as "the K of
X" ("the requirement grammar of the upstream"), or as a code naming a file (`grammar/language.md`, a parameter). Every
artifact a line conforms to is declared with the part of speech (artifact): `- **the comment form** (artifact): ...`
is a proper noun of kind artifact, `- **layout** (artifact): ...` a noun under artifact. Its entry may give `Schema:`
(the schema type and its file, as in "Schema: json schema, `schemas/comment.json`."), and an attribute entry or a relation
row that is one of its fields may give `Field of: <artifact>` (an attribute in its entry, a row in a cell of its own);
the lexicon reads and keeps both, and nothing checks them yet (b241). The
verb is the CLI pack's state verb `conform` (Frame: thing conforms to artifact), and its atom is `conforms(x, a)`: in
a While or Where clause and a relative clause it is a state like any other, negated with "does not conform to A",
counted out with "no K conforms to A", and said "a K that conforms to A" or "a K that does not conform to A". A K of
another kind after "to" is refused, naming the verb's frame. "the K of X" after "does not conform to" is the K that X
has, there whether or not X conforms: it stays outside the `not`. In `model logic` the atom is a state like a
relation's (`crel(R, e_conform, x, a, pos)`, `neg` under a `not`), which clashes as any state does; in a scenario it is
a Given, "the file f1 does not conform to the stage form", which the codified-2 world records.

Found by the audit in requests r76, r77, r86 and r100 ("a comment that has a field block": a comment that conforms to
the comment form), r82 ("a request line that has no logical form": one that does not conform to the requirement
grammar of the upstream), r87 and r95 (b153); design-model-check r189, r195 and r196 (b152: "does not conform to the
request form", "the entry form", "the final layout"); readiness r21, r24 and r26 (b157: "does not match the
relation-row form", "the upstream-entry form", "the example-data form"). The design's own example (section 6.2):
"While a request comment does not conform to the comment schema, when a session runs `work sync`, `work` shall print
the comment and not write the comment."

```reading
While a file does not conform to the stage form, when the person runs `work start`, `work` shall print the file and not write the file.
shall [x2: artifact the stage form (constant), x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: file]
    not
      conforms(x1, x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x1)
    not
      write(e3, subject: x5, object: x1)
```

```reading
While a file conforms to the stage form and no worktree holds the file, when the person runs `work start`, `work` shall print the file.
shall [x2: artifact the stage form (constant), x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: file]
    conforms(x1, x2)
    not [x3: worktree]
      in(x1, x3)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x1)
```

```reading
If the person runs `work start` on a file that does not conform to the stage form, then `work` shall refuse the command and name the file.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x4: artifact the stage form (constant), x5: tool `work` (constant)]
  if [x3: file]
    not
      conforms(x3, x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```

```reading
When the person runs `work start`, `work` shall print every file that conforms to the stage form.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant), x5: artifact the stage form (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: file]
      conforms(x4, x5)
      scope
        print(e2, subject: x3, object: x4)
```

```reading
While no file conforms to the stage form, when the person runs `work start`, `work` shall exit successfully.
shall [x2: artifact the stage form (constant), x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while
    not [x1: file]
      conforms(x1, x2)
  when
    run(e1, subject: x3, object: x4)
  response
    exit(e2, subject: x5, successfully)
```

The artifact as "the K of X", the worktree's own layout: it is there whether or not the file conforms to it.

```reading
While a worktree holds a file that does not conform to the layout of the worktree, when the person runs `work start`, `work` shall print the file.
shall [x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: worktree, x2: file, x3: layout]
    of(x3, x1)
    not
      conforms(x2, x3)
    in(x2, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x2)
```

The artifact as a code naming a file: a parameter of kind artifact (R10).

```reading
While a file does not conform to `docs/stage.md`, when the person runs `work start`, `work` shall print the file.
shall [x2: artifact `docs/stage.md` (parameter), x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: file]
    not
      conforms(x1, x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x1)
```

```reading
While a file conforms to a stage, when the person runs `work start`, `work` shall print the file.
refused: the verb conform takes as its recipient artifact or a kind of it: thing conforms to artifact
```

### "the T of X is after v": ordered comparison

An attribute whose entry says `Order:` has ordered values, and a line may compare its value with a value: "the T of X
is after v", "is before v", "is not after v", "is not before v", and "is after v and before w". `Order: by number.`
orders the values by their numbers, as a release is ordered (`1.10.0` is after `1.9.0`), and any code of numbers
joined by dots is a value of it; `Order: as listed.` orders them as `Values:` lists them, and only those are its
values. "the T of X is v" and "X is v" take any such code too. The atom is `cmp(T(x)) after v` (the design's `cmp(x,
A, op, v)`), the time pack's comparison of moments said of an attribute (section "Time"); "is not before v" puts it
under `not`. A code that is no value of the attribute is refused, naming the code and the order; an attribute with
no `Order:` has no "after" or "before". In `model logic` a comparison is a condition as a value is (`ccmp(R, x, T,
after, point)`), checked exactly over the values the two lines of a pair name and the gaps between them (design call
9): two lines whose ranges share no value never fire together, and a value between two named values (`1.0.1`,
between `1.0.0` and `2.0.0`) is one that an attribute ordered by number may have and one ordered as listed has not.
In a scenario a comparison is a Given of one value on the right side of every value the line names, a value the
entry lists when one is: "the file f1 is `2.0.0`" for "after `1.0.0` and before `3.0.0`", "the file f1 is `3.0.1`"
for "after `3.0.0`".

Found by the audit in migration-tools r36, r39, r40, r41, r42, r45, r46, r51 and r55 (b156): each said a range of
releases as one value of the release (`0.23.1` for "before `0.24.0`") or as "lacks the verb-frames step and does not
lack the simplified-workflow step", which inverts what it means; and b161's line "While the release of the repository
is after `3.0.0` and before `4.0.0`, ...". Each says the range with "after" and "before".

```reading
While the version of a file is before `2.0.0`, when the person runs `work start`, `work` shall print the file.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: file]
    cmp(version(x1)) before `2.0.0`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

```reading
While the version of a file is after `1.0.0` and before `3.0.0`, when the person runs `work start`, `work` shall print the file.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: file]
    cmp(version(x1)) after `1.0.0`
    cmp(version(x1)) before `3.0.0`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

```reading
While the version of a file is not before `2.0.0`, when the person runs `work start`, `work` shall not write the file.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: file]
    not
      cmp(version(x1)) before `2.0.0`
  when
    run(e1, subject: x2, object: x3)
  response
    not
      write(e2, subject: x4, object: x1)
```

A value between two named values: `1.10.0` is after `1.9.0`, as a release is, and needs no entry of its own.

```reading
While the version of a file is after `1.9.0`, when the person runs `work start`, `work` shall print the file.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: file]
    cmp(version(x1)) after `1.9.0`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

A value that no entry lists is a value of an attribute ordered by number all the same:

```reading
While the version of a file is `1.0.1`, when the person runs `work start`, `work` shall print the file.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: file]
    version(x1) = `1.0.1`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

An attribute ordered as listed: `high` is after `low`.

```reading
While the priority of a stage is after `low`, when the person runs `work start`, `work` shall end the stage.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: stage]
    cmp(priority(x1)) after `low`
  when
    run(e1, subject: x2, object: x3)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While the version of a file is after `banana`, when the person runs `work start`, `work` shall print the file.
refused: `banana` is no value of the version of a file, which is ordered by number
```

```reading
While the priority of a stage is before `soon`, when the person runs `work start`, `work` shall end the stage.
refused: `soon` is no value of the priority of a stage, which is ordered as listed: `low`, `high`, `urgent`
```

### "is one of `a` or `b`", "is not `a` or `b`", "has no T": value sets and a value's absence

A line may name a set of an attribute's values: "the T of X is one of `a`, `b` or `c`" and "X is one of `a`, `b` or
`c`" say that the value is one of them, a case of an "or" for each value (section "the K outside the box ...": a case
holds what its side says); "the T of X is not `a`, `b` or `c`" and "X is not `a`, `b` or `c`" say that it is none of
them, a `not` for each value. "None of them" is not "some other value the entry lists": a thing whose T has no value
is none of them too. "X has no T" says that X's T has no value at all, the atom `T(x) = none`: a fact of its own,
which no listed value meets, so "has no T" and "is `a`" never hold of one thing together, while "has no T" and "is
not `a`" do. "every K of X is `v`" (and "is one of ...", "is not ...") says it of each K of X. The list names each
value once and takes at least two; a value of another attribute is no member of it. In `model logic` a set is the
"or" the check has, one split a value (`R#1`, `R#2` ...), in an `every` box `uin(R, x, T, v)` of each value; the
absence a condition on the value `absent` (`cond(R, x, T, absent, pos)`), which L3 and L4 read as no value. In a
scenario a set is a scenario a value, "is not" a Given of each value negated, and the absence the Given "the stage s1
has no priority".

Found by the audit in decision-tiers r13 ("untiered", said as "is not `check` and ... is not `judgement`", which also
holds of a tier outside the three; it is "has no tier") and r23 (the route a design-decision may have, a set of
values), backlog r28-r33 (one line a status the item may be in, when "is one of" says them in one line), migration-
tools r48 and r52-r54 and intake r10 ("is not `delivered` and the request is not `refused` and ...", which is "is not
`delivered`, `refused` or `withdrawn`"), and requests r60 ("has no origin": the command's origin absent).

```reading
While a line is one of `proposed`, `accepted` or `refused`, when the person runs `work start`, `work` shall print the line.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: line]
    or
      case
        outcome(x1) = `proposed`
      case
        outcome(x1) = `accepted`
      case
        outcome(x1) = `refused`
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

```reading
While the priority of a stage is one of `low` or `high`, when the person runs `work start`, `work` shall end the stage.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: stage]
    or
      case
        priority(x1) = `low`
      case
        priority(x1) = `high`
  when
    run(e1, subject: x2, object: x3)
  response
    end(e2, subject: x4, object: x1)
```

"is not `a`, `b` or `c`": none of them.

```reading
While a stage is `open` and a line of the stage is not `accepted`, `refused` or `withdrawn`, when the person runs `work start`, `work` shall print the line.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage, x2: line]
    status(x1) = `open`
    of(x2, x1)
    not
      outcome(x2) = `accepted`
    not
      outcome(x2) = `refused`
    not
      outcome(x2) = `withdrawn`
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x2)
```

```reading
While the priority of a stage is not `low` or `high`, when the person runs `work start`, `work` shall end the stage.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: stage]
    not
      priority(x1) = `low`
    not
      priority(x1) = `high`
  when
    run(e1, subject: x2, object: x3)
  response
    end(e2, subject: x4, object: x1)
```

"has no T": the value absent, which is no listed value.

```reading
While a stage is not `done` and the stage has no priority, when the person runs `work start`, `work` shall print the stage.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while [x1: stage]
    not
      status(x1) = `done`
    priority(x1) = none
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

"every K of X is `v`", and "is one of" said of each K of X:

```reading
While a stage is `open` and every line of the stage is `accepted`, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    every [x2: line]
      of(x2, x1)
      scope
        outcome(x2) = `accepted`
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x1)
```

```reading
While a stage is `open` and every line of the stage is one of `accepted`, `refused` or `withdrawn`, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    every [x2: line]
      of(x2, x1)
      scope
        or
          case
            outcome(x2) = `accepted`
          case
            outcome(x2) = `refused`
          case
            outcome(x2) = `withdrawn`
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x1)
```

```reading
While a line is one of `accepted` or `accepted`, when the person runs `work start`, `work` shall print the line.
refused: the list of the outcome of a line names `accepted` twice
```

### "the number of Ks that P": a count as a value

"the number of Ks that P" is a value: a line may print it, and may compare it with a number. Its noun is any kind's
in the plural with what restricts it ("lines of the stage", "sessions that follow the stage", "lines of the stage
whose outcome is `accepted`"). Printed, it is a referent of its own, `x: number`, and a `number` box that says what it
counts: `number x of [y: K]` over the restrictions of y; the Ks it counts are made inside the box, so no "the K"
outside it binds to them (R2). Compared, "the number of Ks that P is more than n" is the count box of R7 over the Ks
with nothing in its scope: "is more than", "is less than" (R7's "fewer than"), "is at least", "is at most" and "is"
(exactly), n a number word from one to ten or a code; a code of digits is that number, any other code (`batch_size`)
a parameter (R10), which the box names. In `model logic` a printed number is an object of its own whose restrictions
are the counted Ks', so two lines that print the numbers of two different sets of things never clash; a compared
number is a count in a condition (`ccount`), and two lines whose conditions count one set of things with bounds that
no number meets both of (a clingo `#count`, as two counts of one act are read) never fire together. In a scenario a
printed number brings in two Ks with their restrictions, and the Then says the number of them; a compared number
brings in as many Ks as the comparison needs at least (four for "more than three"), and a comparison with a
parameter is a Given of the comparison itself.

Found by the audit in analysis-tools r49, r50, r53, r56, r57, r58 and r64 (b154: "the run count of the coverage
map", "the test count of the function", "the untested count of the Python file", "the reference count of the
identifier", and a Python file that "exceeds" a size limit, each a noun or a verb that hides the number of things),
batch-measurement r23, r24, r25 and r27 (b156: "round-trip count", "tool-use count", "compaction count"),
feature-file-tools r45, r46, r61, r64, r79 and r80 (b157: "scenario count", and the counts a line of a capability
says), design-model-check r202, r203, r239 and r252 (b152), backlog r27 and intake r11 (b158, b159); and in a line of
batches, "While the number of tasks of the batch is more than `batch_size`, ...". Each says "the number of Ks that
P".

```reading
When a session ends a stage, `work` shall print the number of lines of the stage.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: line]
      of(x5, x2)
    print(e2, subject: x3, object: x4)
```

```reading
When a session ends a stage, `work` shall print the number of sessions that follow the stage.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: session]
      follow(subject: x5, object: x2)
    print(e2, subject: x3, object: x4)
```

```reading
When a session ends a stage, `work` shall print the number of lines of the stage whose outcome is `accepted`.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: line]
      of(x5, x2)
      outcome(x5) = `accepted`
    print(e2, subject: x3, object: x4)
```

"shall not print the number of Ks": under `not`, as any object of "shall not" (batch-measurement r24).

```reading
When a session ends a stage, `work` shall not print the number of lines of the stage.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response
    not [x4: number]
      number x4 of [x5: line]
        of(x5, x2)
      print(e2, subject: x3, object: x4)
```

Compared: R7's count box, with nothing in its scope.

```reading
While a stage is `open` and the number of lines of the stage is more than three, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    count more than 3 [x2: line]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x1)
```

```reading
While a stage is `open` and the number of lines of the stage is less than `3`, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    count fewer than 3 [x2: line]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x1)
```

```reading
While a stage is `open` and the number of lines of the stage is `0`, when the person runs `work start`, `work` shall end the stage.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    count exactly 0 [x2: line]
      of(x2, x1)
  when
    run(e1, subject: x3, object: x4)
  response
    end(e2, subject: x5, object: x1)
```

A code that is no number is a parameter:

```reading
While a stage is `open` and the number of lines of the stage is more than `limit`, when the person runs `work start`, `work` shall end the stage.
shall [x3: number `limit` (parameter), x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: stage]
    status(x1) = `open`
    count more than x3 [x2: line]
      of(x2, x1)
  when
    run(e1, subject: x4, object: x5)
  response
    end(e2, subject: x6, object: x1)
```

The Ks a number counts are made inside its box:

```reading
When a session ends a stage, `work` shall print the number of files in the worktree of the session, and `work` shall print the file.
refused: "the file" has no antecedent: a file is made inside "the number of files ...", which gives nothing outside it
```

### "another K", "a different K", "two Ks" and "the same K": identity and distinctness

Two noun phrases of one kind may name one thing or two. "a K" never says which: two Ks of a line may be one thing.
These four say it:

- "another K" and "a different K" (one meaning) are a K that is not the K before it: a referent of its part as "a K"
  is (R1), and the atom `distinct(y, x)`, x the referent "the K" would bind to by R2 in its place: the latest earlier
  referent of kind K (or of a kind under it) not made inside a box that does not hold it. When that referent came
  from "two Ks", y is distinct from both. With no such referent the line is refused, naming the noun, as R2 refuses
  "the K"; "another K" never names the image of a row nor the run's own K.
- "two Ks" are two Ks, each distinct from the other: two referents, the second with `distinct(y, x)`, and the clause
  said of each, as of "a K and a K" (so "two sessions follow a stage" is one stage both follow). What restricts the
  noun restricts each; a K its restriction makes is one K they share ("two files in a worktree": one worktree). A
  later "the K" names neither and is refused.
- "the same K" binds as "the K" does (R2): to the latest earlier K, else the image of a row, else the run's own K. When
  R2 gives it nothing and the line said "two Ks" before it, it is one new K (R1), which each of the two shares: "two
  sessions follow the same stage". Else it is refused as "the K" is.

`model logic` reads `distinct(y, x)` as two things its unification never makes one: when one line's two referents
it holds would be one thing of a pair (one code named of both, a definite both bind to), the pair is not read under
that unification. A trigger of one act on each of "two Ks" ("writes two files") is one act of the line, a trigger of
each part: two lines fire on one act when each part of either is a part of the other, so "writes a file" is not the
act of "writes two files". So two lines on one act whose states differ only in which things are one never clash:
"another file in the same worktree" and "another file in a different worktree" below (the twin of design-model-check
r276-r278, "another requirement of the same trigger and state"). `features generate` names the two things with two
names ("the session s1 gives the file f1 to the session s2"), which says they differ; a trigger of one act on each of
two Ks is a When each.

Found by the audit in design-model-check r176 (v15b, "two requirements share an id"), r179 (v15n, "another group"),
r199 ("another interpreter"), r218 ("two others"), r224 (v_t15, two senses of one term), r247-r249 and r276-r278
(two lines "of the same trigger and state", "another" requirement), migration-tools r28 and r29 ("a ledger entry
supersedes another ledger entry", said with a coined noun), telemetry r8 ("`measure compare` on two batches"),
backlog r26 and batches r20 and r22 (an item "not in the same batch"), backlog r39 ("an upstream branch of a
different name") and batches r32 (a scenario of another item than the task's). Each said the identity with a coined
noun, a rule code or not at all.

```reading
When a session gives a file to another session, `work` shall print the file.
shall [x4: tool `work` (constant)]
  when [x1: session, x2: file, x3: session]
    distinct(x3, x1)
    give(e1, subject: x1, object: x2, to: x3)
  response
    print(e2, subject: x4, object: x2)
```

```reading
When a session gives a file to a different session, `work` shall print the file.
shall [x4: tool `work` (constant)]
  when [x1: session, x2: file, x3: session]
    distinct(x3, x1)
    give(e1, subject: x1, object: x2, to: x3)
  response
    print(e2, subject: x4, object: x2)
```

"the same K" bound to the earlier K, the twin of "another requirement of the same trigger" (design-model-check
r276-r278):

```reading
While a session follows a stage and another session follows the same stage, when the person runs `work start`, `work` shall print the stage.
shall [x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: session, x2: stage, x3: session]
    follow(subject: x1, object: x2)
    distinct(x3, x1)
    follow(subject: x3, object: x2)
  when
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x2)
```

"two Ks" of "the same K", the twin of "two requirements share an id" (design-model-check r176):

```reading
While two sessions follow the same stage, when the person runs `work start`, `work` shall end the stage.
shall [x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: session, x3: stage, x2: session]
    follow(subject: x1, object: x3)
    distinct(x2, x1)
    follow(subject: x2, object: x3)
  when
    run(e1, subject: x4, object: x5)
  response
    end(e2, subject: x6, object: x3)
```

What restricts "two Ks" restricts each, and a K it makes is one both share:

```reading
When a session writes two files in a worktree, `work` shall print the worktree.
shall [x5: tool `work` (constant)]
  when [x1: session, x2: file, x3: worktree, x4: file]
    in(x2, x3)
    write(e1, subject: x1, object: x2)
    distinct(x4, x2)
    in(x4, x3)
    write(e2, subject: x1, object: x4)
  response
    print(e3, subject: x5, object: x3)
```

In a response, two new Ks:

```reading
When a session ends a stage, `work` shall write two files.
shall [x3: tool `work` (constant)]
  when [x1: session, x2: stage]
    end(e1, subject: x1, object: x2)
  response [x4: file, x5: file]
    write(e2, subject: x3, object: x4)
    distinct(x5, x4)
    write(e3, subject: x3, object: x5)
```

"another K" after "two Ks" is distinct from both:

```reading
When a session gives two files to a session, `work` shall write another file.
shall [x5: tool `work` (constant)]
  when [x1: session, x2: file, x4: session, x3: file]
    give(e1, subject: x1, object: x2, to: x4)
    distinct(x3, x2)
    give(e2, subject: x1, object: x3, to: x4)
  response [x6: file]
    distinct(x6, x2)
    distinct(x6, x3)
    write(e3, subject: x5, object: x6)
```

Two lines on one act in two states: the first's two files are in one worktree, the second's in two, so `model logic`
finds no witness where both fire, and no L1:

```reading
When a session writes a file in a worktree and another file in the same worktree, `work` shall print the worktree.
shall [x5: tool `work` (constant)]
  when [x1: session, x2: file, x3: worktree, x4: file]
    in(x2, x3)
    write(e1, subject: x1, object: x2)
    distinct(x4, x2)
    in(x4, x3)
    write(e2, subject: x1, object: x4)
  response
    print(e3, subject: x5, object: x3)
```

```reading
When a session writes a file in a worktree and another file in a different worktree, `work` shall not print the worktree.
shall [x6: tool `work` (constant)]
  when [x1: session, x2: file, x3: worktree, x4: file, x5: worktree]
    in(x2, x3)
    write(e1, subject: x1, object: x2)
    distinct(x4, x2)
    distinct(x5, x3)
    in(x4, x5)
    write(e2, subject: x1, object: x4)
  response
    not
      print(e3, subject: x6, object: x5)
```

The refusals: "another K" with no K before it, or with every K before it inside a box; "the same K" with neither an
antecedent nor "two Ks" before it; "the K" after "two Ks".

```reading
When a session ends another stage, `work` shall print the stage.
refused: "another stage" has no antecedent: no earlier noun phrase gives a stage
```

```reading
While no session follows a stage, when the person runs `work start`, `work` shall end another stage.
refused: "another stage" has no antecedent: a stage is made inside "no session ...", which gives nothing outside it
```

```reading
When the person runs `work start`, `work` shall end the same stage.
refused: "the same stage" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a stage
```

```reading
While two sessions follow a stage, when the person runs `work start`, `work` shall print the session.
refused: "the session" has no antecedent: "two sessions" gives two sessions, and "the session" names neither
```

### "X exists" and "no K exists": existence

"X exists" says that the thing X is there: a state of X whose frame takes no object, the atom `exists(x)`. Every kind
has it, with no entry in the glossary: "exist" is the base grammar's verb, a state, so a trigger may not say it ("When
a file exists" is refused as a state verb in a trigger is). "X does not exist" puts the atom under `not`; "no K
exists" is R3's "no K", a `not` box with its K; "a K that exists" and "a K whose T does not exist" are relative
clauses as any state gives them. In `model logic` existence is the one-place fluent `crel(R, exists, x, none, Pol)`
(the state whose frame takes no object, b219), and "no K exists" `rnone(R, exists, kind(K), none)`: "the `a` file
exists" clashes with "the `a` file does not exist" and with "no file exists", but not with "the `b` file does not
exist". In a scenario it is a Given, "the file f1 exists", "the `a` file does not exist" or "no file exists", which
the world meets by making the thing or leaving it out.

"has been written" is not existence: it is the perfect of an action, the history of section "Time" (built, and
refused by `model logic` as any history is). A line that means that a thing is there says "exists"; one that means
that an act happened before says the perfect.

Found by the audit in analysis-tools r37-r41 ("this file system holds the dot-venv interpreter": a container noun
and a row coined to say that a file is there; the interpreter that is used is the first that exists, each case
written with existence, the order a known limit, #14), r48 and r50-r55 ("this repository holds a coverage map", "holds
no coverage map"), and requests r72 ("a bounded context that has no host", the upstream's entry with no repository)
and r81 (every with no existential import: "every request line ... is `refused`" holds of a request with no lines,
so the line says that one exists too).

```reading
While the `a` file exists, when the person runs `work start`, `work` shall print the file.
shall [x1: file `a` (parameter), x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while
    exists(x1)
  when
    run(e1, subject: x2, object: x3)
  response
    print(e2, subject: x4, object: x1)
```

"X does not exist": each case of a first match said with existence (analysis-tools r38-r40).

```reading
While the `b` file exists and the `a` file does not exist, when the person runs `work start`, `work` shall print the `b` file.
shall [x1: file `b` (parameter), x2: file `a` (parameter), x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while
    exists(x1)
    not
      exists(x2)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x1)
```

```reading
While a file in a worktree exists, when the person runs `work start`, `work` shall print the file.
shall [x3: agent the person (constant), x4: command `work start` (parameter), x5: tool `work` (constant)]
  while [x1: file, x2: worktree]
    in(x1, x2)
    exists(x1)
  when
    run(e1, subject: x3, object: x4)
  response
    print(e2, subject: x5, object: x1)
```

"no K exists" (analysis-tools r55):

```reading
While no file exists, if the person runs `work start`, then `work` shall exit with an error naming `work start`.
shall [x2: agent the person (constant), x3: command `work start` (parameter), x4: tool `work` (constant)]
  while
    not [x1: file]
      exists(x1)
  if
    run(e1, subject: x2, object: x3)
  response
    exit(e2, subject: x4, with an error naming: x3)
```

"whose T does not exist" (requests r72):

```reading
If the person runs `work start` on a session whose worktree does not exist, then `work` shall exit with an error naming the session.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x5: tool `work` (constant)]
  if [x3: session, x4: worktree]
    of(x4, x3)
    not
      exists(x4)
    run(e1, subject: x1, object: x2, on: x3)
  response
    exit(e2, subject: x5, with an error naming: x3)
```

"every K of X is v" holds of an X with no K; "a K of X exists and every K of X is v" says there is one (requests r81):

```reading
While a stage is `open` and a line of the stage exists and every line of the stage is `refused`, when the person runs `work start`, `work` shall end the stage.
shall [x4: agent the person (constant), x5: command `work start` (parameter), x6: tool `work` (constant)]
  while [x1: stage, x2: line]
    status(x1) = `open`
    of(x2, x1)
    exists(x2)
    every [x3: line]
      of(x3, x1)
      scope
        outcome(x3) = `refused`
  when
    run(e1, subject: x4, object: x5)
  response
    end(e2, subject: x6, object: x1)
```

```reading
When the person runs `work start`, `work` shall print every file that exists.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: file]
      exists(x4)
      scope
        print(e2, subject: x3, object: x4)
```

```reading
When a session exists, `work` shall print the session.
refused: the verb exist is a state, and a trigger takes an action
```

### "runs C with the `--x` option": an option with its argument

A command's option is in the trigger, with the CLI pack's run: "runs C with the `--x` option", "with the `--x` and
`--y` options" (or "with the `--x` option and the `--y` option"), "with the `--x` option on a K", "with the `--x`
option set to v" (its argument: a code, or a thing the line says more of) and "without the `--x` option" (the option
not given). The run is one atom, `run(e, subject: agent, object: command, with: option ..., without: option ...,
on: thing)`, with every option it is given and every option it is not; an "and" list of options is one run with each
of them (not a run for each, as "and" gives of any other argument), an "or" list a case for each. An option's
argument is the atom `argument(option, v)` beside the run. In `model logic` the command a run runs is the command's
code with each option given and its argument when that is a code (`work start --every 5`); an option not given is not
in it, so the line pairs with every line on the command alone; a thing that an option is set to is what the run is on.
In a scenario the When names each option and its argument as the line does, and the step's Call gives them to its
handler (`options`: each option given with its argument, `without`: each option not given).

Found by the audit in requests r59 ("`work request --raised-for` on a request": the option glued into the command
code, which makes it a command apart from `work request`; with and on in one trigger were refused), r60 (none of
three options given), r61, r102 ("with `--source` and `--thread`"), r62 ("`--from` on a text": the option's argument
read as the run's object), r82 and r97-r101 (`work outcome accepted`, `work watch --hook`, `work watch --forward`),
analysis-tools r36 (`tools probe --python` on a Python interpreter), U16 and backlog r27 ("with the `--json` option",
one JSON object), and decision-tiers r20 and intake r13 ("an argument that `work decision` does not have": the option
not given on this run said as a property of the command).

One option (U16, backlog r27):

```reading
When the person runs `work start` with the `--json` option, `work` shall exit successfully.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--json` (parameter), x4: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response
    exit(e2, subject: x4, successfully)
```

Two options of one run (requests r61, r102), said either way:

```reading
If the person runs `work start` with the `--source` and `--thread` options, then `work` shall exit with an error naming `--source`.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--source` (parameter), x4: option `--thread` (parameter), x5: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, with: x3, with: x4)
  response
    exit(e2, subject: x5, with an error naming: x3)
```

```reading
If the person runs `work start` with the `--source` option and the `--thread` option, then `work` shall exit with an error naming `--source`.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--source` (parameter), x4: option `--thread` (parameter), x5: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, with: x3, with: x4)
  response
    exit(e2, subject: x5, with an error naming: x3)
```

An option and the thing the run is on (requests r59, analysis-tools r36):

```reading
When the person runs `work start` with the `--json` option on a stage, `work` shall print the stage.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--json` (parameter), x5: tool `work` (constant)]
  when [x4: stage]
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response
    print(e2, subject: x5, object: x4)
```

An option set to a code, its argument:

```reading
When the person runs `work start` with the `--every` option set to `5`, `work` shall exit successfully.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--every` (parameter), x4: thing `5` (parameter), x5: tool `work` (constant)]
  when
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    exit(e2, subject: x5, successfully)
```

An option set to a thing the line says more of (requests r62):

```reading
If the person runs `work start` with the `--from` option set to a stage whose status is not `done`, then `work` shall exit with an error naming the stage.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--from` (parameter), x5: tool `work` (constant)]
  if [x4: stage]
    not
      status(x4) = `done`
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    exit(e2, subject: x5, with an error naming: x4)
```

An option not given (decision-tiers r20), none of three (requests r60), and with the thing the run is on (intake
r13):

```reading
If the person runs `work start` without the `--summary` option, then `work` shall exit with an error naming `--summary`.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--summary` (parameter), x4: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3)
  response
    exit(e2, subject: x4, with an error naming: x3)
```

```reading
If the person runs `work start` without the `--source`, `--thread` and `--raised-for` options, then `work` shall exit with an error naming `--source`.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: option `--source` (parameter), x4: option `--thread` (parameter), x5: option `--raised-for` (parameter), x6: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3, without: x4, without: x5)
  response
    exit(e2, subject: x6, with an error naming: x3)
```

```reading
If a session runs `work start` without the `--reason` option on a line, then `work` shall exit with an error naming `--reason`.
shall [x2: command `work start` (parameter), x3: option `--reason` (parameter), x5: tool `work` (constant)]
  if [x1: session, x4: line]
    run(e1, subject: x1, object: x2, without: x3, on: x4)
  response
    exit(e2, subject: x5, with an error naming: x3)
```

The noun after two codes is plural: "with the `--source` and `--thread` option" does not parse (grammar/corpus/core-4.txt).

### "the push of the command", "the commit that the command makes": the run's own things

A thing a run makes is said as the image of the command by a row (`push | of | command | one`: "the push of the
command", the push of the command the trigger runs) or, for a kind whose entry has `This:`, as the run's own K (R11:
"the commit", "the commit that the command makes"). Nothing is built for them: each kind the audit names (the Python
interpreter, the decisions index, the git directory, the transcript, the push the command makes) gets its row or its
`This:` in the reword phase whose lines use it. These are the twins of each shape.

Found by the audit in analysis-tools r43-r46 and r66 ("the dot-venv interpreter", the interpreter `tools` runs
with), decision-tiers r19 ("a decisions index": the one index of the repository), conversation r6 (the git directory,
the transcript) and the push and the commit a `work` command makes.

```reading
When the person runs `work start`, `work` shall print the push of the command.
shall [x1: agent the person (constant), x2: command `work start` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: push]
    of(x4, x2)
    print(e2, subject: x3, object: x4)
```

```reading
When the person runs this command, `work` shall print the commit that the command makes.
shall [x1: agent the person (constant), x2: command "the command the run runs" (indexical), x3: tool `work` (constant), x4: commit "the commit the run makes" (indexical)]
  when
    run(e1, subject: x1, object: x2)
  response
    make(subject: x2, object: x4)
    print(e2, subject: x3, object: x4)
```

## What the language cannot say yet

The limits the rewording keeps, one subsection a limit: the construct the language has not, the lines that need it
by id, and the plain line each says instead. A corpus block of such a line gives `Known limit: #<n>` as its trace.

### #13: what a command would write

A line that says X differs from what a command writes now ("is not what `model decisions` would write") compares X
with a counterfactual: the output of a run that has not happened. The language has no noun phrase for it: "what
`model decisions` writes" is no noun phrase (no free relative), and "does not conform to" takes an artifact, which a
command's output is not. Lines: design-model-check r202, r203 (the decisions index), r220 (the rule catalogue).
Each says instead what the stale file lacks, in the item's words: "While a design-decision has an index entry that a
decisions index does not hold, if the person runs `model decisions --check`, then `model` shall exit with an error
naming the decisions index and change no file."; the rows that are extra or changed are lost.

### #6: a value compared with another thing's value

"after v" compares a value with a value a line names; the language has no comparison of two things' values ("the
release of the repository is after the release of the plugin"), which the check could not decide exactly over named
points (design call 9). Line: migration-tools r47 (b156: the repository's release `newer`, newer than the plugin's
own). It says instead the plugin's release the line is written for, as a value: "While the release of the repository
is after `4.0.0`, ...", and the line gets a new id when the plugin's release moves on.
