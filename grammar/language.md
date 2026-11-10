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
