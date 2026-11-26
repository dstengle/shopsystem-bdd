# The language of grammar 4: its reading rules

What each construct of a grammar 4 requirement means, as the reading rules R1-R12 of the CNL 4 design (call 5,
section 7.3; I11b). A line's meaning is its logical form (`scripts/spec_lf.py`), which `spec parse --form` prints:
its modality and the referents no part introduces (actors and codes as constants, a code that is no word of the
context as a parameter, the request's own things as indexicals), then its Where, While, trigger and response, each a box
of referents, atoms and boxes. `scripts/spec_lf_read.py` holds the rules that resolve a word or refuse a line;
`spec parse` refuses a line one of them refuses, naming the words, with its tree.

Each rule names the real lines it was tested on, quoted as they were written then (in the CLI pack's words: a tool
that runs a command and prints or exits). Each rule's construct is shown here on a twin in request words (the domain
contract design, §9.4), in the smallest context with a domain model (`tests/scripts/fixtures/request-4/`: the request
pack, and a model of sessions, stages, lines, files and worktrees, whose work service answers the requests "opens the
board", "writes a file", "ends a stage", "gives a file to an agent", "settles a line"). Each block below is a line and
what grammar 4 reads it as: its logical form, or its refusal.
`tests/scripts/test_spec_lf_read.py` reads every block and fails when grammar 4 reads its line otherwise.

## R1. "a K": any K in a condition or a trigger, a new K in a response

"a K" in a While clause, a Where clause or a trigger is a referent of that part, any K: the line holds for each K
that meets it, and the response may name it again with "the K". In a response, "a K" is a new K the response brings
about. A bare plural in a response reads as "every" (R6).

Tested on requests r33 ("While a comment is unreadable, when a session runs `work sync`, `work` shall print the
comment ...": each unreadable comment is printed) and batches r13 ("While a commit of an item in a batch is uncited
...": any such commit refuses the review).

```reading
While a stage is `open`, when a session ends the stage, the work service shall return the stage.
shall [x3: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
  when [x2: session]
    request(e1, work.end, subject: x2, object: x1)
  response
    return(e2, subject: x3, object: x1)
```

```reading
When a session ends a stage, the work service shall write a file.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
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
When a session ends a stage, the work service shall return the status of a stage.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: stage, x5: status]
    status(x4) = x5
    return(e2, subject: x3, object: x5)
```

```reading
When a session ends a stage, the work service shall return the status of the stage.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: status]
    status(x2) = x4
    return(e2, subject: x3, object: x4)
```

```reading
While a session follows a stage, when the person opens the board, the work service shall end a stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
  when
    request(e1, work.open, subject: x3, the board)
  response [x5: stage]
    end(e2, subject: x4, object: x5)
```

```reading
While a session follows a stage, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x2)
```

## R2. "the K" binds to something the line gave, else it is refused

"the K" binds to the latest earlier referent of kind K (or of a kind under K) in the line: one a part introduced, an
actor, a code or an indexical. Else to the image of a relation row `K | of | S` of the one earlier referent of kind S
("the worktree" after "a session" is the worktree of the session). Else, when K's entry has `This:`, to the request's own
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
When a session ends a stage, the work service shall return the worktree.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: worktree]
    of(x4, x1)
    return(e2, subject: x3, object: x4)
```

```reading
When a session writes a file, the work service shall return the worktree of every session.
shall [x3: service the work service (constant)]
  when [x1: session, x2: file]
    request(e1, work.write, subject: x1, object: x2)
  response
    every [x4: session]
      scope [x5: worktree]
        of(x5, x4)
        return(e2, subject: x3, object: x5)
```

```reading
When the person opens the board, the work service shall return the request.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    return(e2, subject: x2, object: x3)
```

```reading
If the work service refuses a request, then the work service shall name the reason.
refused: "the reason" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a reason
```

```reading
When a session ends a stage that sessions follow, the work service shall return the worktree.
refused: "the worktree" has no antecedent: 2 earlier noun phrases may give it: say "the worktree of" one of them
```

```reading
While a session does not follow the stage, when a session ends a stage, the work service shall complete the request.
refused: "the stage" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a stage
```

```reading
While a session follows a stage and no session follows a stage whose status is `done`, when the person opens the board, the work service shall return the stage.
shall [x5: agent the person (constant), x6: service the work service (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
    not [x3: session, x4: stage]
      status(x4) = `done`
      follow(subject: x3, object: x4)
  when
    request(e1, work.open, subject: x5, the board)
  response
    return(e2, subject: x6, object: x2)
```

```reading
While no session follows a stage, when the person opens the board, the work service shall return the stage.
refused: "the stage" has no antecedent: a stage is made inside "no session ...", which gives nothing outside it
```

## R3. "no K": there is no K, within its own clause

"no K" (and "nothing") is a `not` box over its referent and the rest of its own clause, and over nothing outside it.

Tested on migration-tools r8 ("... `migrate` shall exit with an error naming the untracked file and change
nothing": the error is said, and no thing is changed).

```reading
If the work service refuses a request, then the work service shall name the request and change nothing.
shall [x1: service the work service (constant)]
  if [x2: request]
    refuse(e1, subject: x1, object: x2)
  response
    name(e2, subject: x1, object: x2)
    not [x3: thing]
      change(e3, subject: x1, object: x3)
```

```reading
While a session has no worktree, when the person opens the board, the work service shall refuse the request and name the session.
shall [x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: session]
    not [x2: worktree]
      of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

"holds nothing" (b274) is the same box over a thing of any kind: no thing at all is in the collection, which `model
logic` reads as no K of each kind a relation row `K | in | S` lets it hold. "holds no K" keeps its meaning (no K;
things of other kinds may be held), and "holds no thing" is refused: "nothing" is the one way to say it.

```reading
While a worktree holds nothing, when the person inspects the worktree, the work service shall return the worktree.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: worktree]
    not [x2: thing]
      in(x2, x1)
  when
    request(e1, work.inspect, subject: x3, object: x1)
  response
    return(e2, subject: x4, object: x1)
```

## R4. "does not V a K" in a condition is refused; under "shall not", "a K" is any K

In a While or Where clause, "X does not V a K" (or a bare plural) reads two ways: "X Vs no K", and "there is a K that
X does not V". The line is refused, naming the words, and the writer says one of the two. In a response, "shall not
V a K" is a `not` box over the K: no K at all.

Tested on requests r53, which needs "some comment the request does not hold" (a comment that is unrecorded) and which
ACE's reading ("holds no comment") would break, and on U5 ("A session shall not write a status": no status at all).

```reading
While a session does not follow a stage, when the person opens the board, the work service shall complete the request.
refused: the While clause says "does not follow a stage", which reads two ways: say "follows no stage" or "a stage that the session does not follow"
```

```reading
While a session follows no stage, when the person opens the board, the work service shall complete the request.
shall [x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: session]
    not [x2: stage]
      follow(subject: x1, object: x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    complete(e2, subject: x4, object: x5)
```

```reading
While a stage that a session does not follow is `open`, when the person opens the board, the work service shall complete the request.
shall [x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: stage, x2: session]
    not
      follow(subject: x2, object: x1)
    status(x1) = `open`
  when
    request(e1, work.open, subject: x3, the board)
  response
    complete(e2, subject: x4, object: x5)
```

```reading
When a session ends a stage, the work service shall not write a file.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response
    not [x4: file]
      write(e2, subject: x3, object: x4)
```

## R5. "X shall V only Ks that P": every K that X Vs meets P

"only" is an `only` box: its restrictor (the Ks and what restricts them) and its scope (the act). Every K the agent
Vs meets the restrictor; the line obliges no V. `spec logic` reads it so (I12a): it clashes only with a line in
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
of such a line gives two Ks, so it is not met vacuously (the generator's part is I14a's). `spec logic` reads it so
(I12a): the act is obliged of each K the restrictor allows, so it clashes with a line that forbids the act of a K of
that kind under the same trigger and state, though that line says more of its K ("a stage whose status is `done`").

Tested on batches r8 ("... and every task of the batch is `done` ...") and requests r37 ("... and every request line
proposed in the request is `refused` ...").

```reading
Where a stage is `open`, when a session writes a file, the work service shall return every file.
shall [x4: service the work service (constant)]
  where [x1: stage]
    status(x1) = `open`
  when [x2: session, x3: file]
    request(e1, work.write, subject: x2, object: x3)
  response
    every [x5: file]
      scope
        return(e2, subject: x4, object: x5)
```

## R7. "one K" is exactly one; "a K" at least one

"a K" is at least one K (R1). A count before a number (one to ten) and a noun, "at least", "at most", "exactly",
"more than" or "fewer than", is a `count` box over its noun (call 4, I15): its bound and number, its restrictor and its
scope, the clause said of each K counted. "one K" alone is exactly one. A count that admits no K ("at most", "fewer
than") obliges no act, as "only" does not. `spec logic` reads two counts of one act on one trigger and state: when no
number of Ks meets both, the pair is an L1 (I15).

Tested on U8 ("... a tool shall print one JSON object": exactly one).

```reading
When the person opens the board, the work service shall return one stage.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    count exactly 1 [x3: stage]
      scope
        return(e2, subject: x2, object: x3)
```

```reading
When the person opens the board, the work service shall return more than one stage whose status is `done`.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    count more than 1 [x3: stage]
      status(x3) = `done`
      scope
        return(e2, subject: x2, object: x3)
```

## R8. "its" binds to the subject of its clause, or the line is refused

"its K" (a row `K | of | S`) and "its T" (an attribute) are the image of the subject of the clause they are in. The
line is refused when that subject is of no kind the relation needs, or when another referent of such a kind was
given before it: the writer says "the K of" the one meant.

Tested on trials r2 and U7 ("A worker shall change only files in its worktree": the worker's own worktree).

```reading
When a session ends a stage, the work service shall return its status.
refused: "its status" binds to the work service, the subject of its clause, which has no status
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

`spec logic` reads the precedence as stated, never as a clash: an If line and a line of another form on one trigger
are no pair, since where the If line's state holds its response replaces the other's, and where it does not hold the
If line does not fire. Two If lines on one trigger are still checked against each other. A universal condition holds
in every trace, so it takes no precedence and none is taken over it: it is paired with each line it bears on, If or
not, and a line whose response it forbids under that line's trigger is an L1 naming it (b117). A pair of two
codified-1 lines keeps the reading of plugin 0.31 (an If line never paired with a line of another form) until its
files are reworded.

Tested on backlog r20 and r21 (in a tasked repository `work idea` refuses, If; in a tracking one it writes, When).

```reading
Where a stage is `open`, while sessions follow the stage, if a session ends the stage, then the work service shall refuse the request and name the stage.
shall [x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  where [x1: stage]
    status(x1) = `open`
  while [x2: session]
    follow(subject: x2, object: x1)
  if [x3: session]
    request(e1, work.end, subject: x3, object: x1)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## R10. A literal that names no declared constant is a parameter

A code that is no word of the context is a parameter: the scenario's given block binds it (call 7). One that is a
word of the context is a constant.

Tested on migration-tools r21 ("... `migrate` shall print "holds no version" and "banana"": example data, not
words of the context).

```reading
When the person opens the board with the interval `5`, the work service shall complete the request.
shall [x1: agent the person (constant), x2: thing `5` (parameter), x3: service the work service (constant), x4: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
    param(e1, interval, x2)
  response
    complete(e2, subject: x3, object: x4)
```

## R11. "this K", and an unbound "the K" whose entry has `This:`, are the request's own K

"this K" of a kind whose entry has `This:` is an indexical: the request's own K, as the entry glosses it (call 6): the
request pack's "this request", the request the trigger makes, and a context's own kind ("the commit", the commit the
request makes). An unbound "the K" of such a kind is the same (R2).

Tested on requests r6 ("While a command is originless, if the person runs `work request` ...": the command is the
one the run runs, now the request the trigger makes) and r33 (the comment is one `work sync` reads).

```reading
When the person opens the board, the work service shall return this request.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    return(e2, subject: x2, object: x3)
```

## R12. A line that obliges with no trigger, and neither "always" nor "never", is refused

A line with no When or If, and neither "always" nor "never", would oblige its response in every state; it is
refused. A line whose response obliges nothing, "shall not" or "only", forbids or restricts in every state, which is
what it means, and stands.

Tested on phase 2 fault 2 of the design's research (lines that read as "in every state").

```reading
The work service shall write a file.
refused: the line has no trigger and neither "always" nor "never": it would oblige its response in every state
```

```reading
While a stage is `open`, the work service shall complete the request.
refused: the line has no trigger and neither "always" nor "never": it would oblige its response in every state
```

```reading
The work service shall not change `spec/index.md`.
shall [x1: service the work service (constant), x2: thing `spec/index.md` (parameter)]
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
may come before it. `spec logic` does not read a necessity yet: it is no premise of a pair and hides no finding,
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
When a session ends a stage, the session may write a file, and the work service shall return the stage.
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
- "the clock reaches m" is a trigger like any other action; "the clock" with no antecedent is the time pack's one clock (R11).

`spec logic` has no reading of a comparison or a history yet: it refuses a line holding one, naming it ("no
translation of a comparison of moments", "no translation of the history of end"), as it refuses any construct it
has no translation for. The blocks below are read in the time fixture
(`tests/scripts/fixtures/codified-2-time/`, a stage's deadline a moment) by `tests/scripts/test_spec_lf_time.py`.

```reading-time
While a deadline of a stage is within the last 7 days, when the person opens the board, the work service shall return the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: deadline, x2: stage]
    of(x1, x2)
    cmp(x1) after now - 7 days
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x2)
```

```reading-time
While a deadline of a stage is after `2026-01-01` and the deadline is not before `2027-01-01`, when a session ends the stage, the work service shall return the stage.
shall [x3: moment `2026-01-01` (parameter), x4: moment `2027-01-01` (parameter), x6: service the work service (constant)]
  while [x1: deadline, x2: stage]
    of(x1, x2)
    cmp(x1) after x3
    not
      cmp(x1) before x4
  when [x5: session]
    request(e1, work.end, subject: x5, object: x2)
  response
    return(e2, subject: x6, object: x2)
```

```reading-time
While a deadline of a stage is within the last 7, when the person opens the board, the work service shall return the stage.
refused: the number 7 is a duration and takes a unit of the time pack after it: second, minute, hour, day, week
```

```reading-time
When the clock reaches a deadline of a stage, the work service shall return the stage.
shall [x1: clock "the clock of the run" (indexical), x4: service the work service (constant)]
  when [x2: deadline, x3: stage]
    of(x2, x3)
    reach(e1, subject: x1, object: x2)
  response
    return(e2, subject: x4, object: x3)
```

```reading-time
While a session has written no file since `2026-01-01`, when the session ends a stage, the work service shall return the stage.
shall [x3: moment `2026-01-01` (parameter), x5: service the work service (constant)]
  while [x1: session]
    not [x2: file]
      has write(subject: x1, object: x2, since: x3)
  when [x4: stage]
    request(e1, work.end, subject: x1, object: x4)
  response
    return(e2, subject: x5, object: x4)
```

```reading-time
While a session has not written a file, when the person opens the board, the work service shall complete the request.
refused: the While clause says "has not written a file", which reads two ways: say "has written no file" or "a file that the session has not written"
```

## Constructs

The constructs grammar 4 is completed with (b240), one subsection a construct: what it says, the real lines the
audit (`.shop/records/2026-11-10-grammar-4-audit.md`) found it missing in, by id, and its twins, each a block of a
line in the words of a fixture context and the form it is meant to have, or `refused: <reason>`. A construct's
blocks are written before it is built, and fail until it is.

The acceptance test of the language is the spec corpus, `grammar/corpus/spec/` (its README): every live line of this
repository's spec in the new language with the reading it is meant to have, checked by
`tests/scripts/test_corpus_spec.py` (it parses to that reading, the reading translates to `spec logic`'s facts and
to `features generate`'s steps, every live line of a codified-2 file has its block, and the line linearises back
word for word). This section's twins are the constructs' tests; the corpus is the language's. Every construct of the grammar, these among them, has a code in the construct catalogue,
`grammar/constructs.md` (`spec constructs --write`), by which a line about the language names it.

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
When the person opens the board, the work service shall return every stage and the status of the stage.
refused: "the stage" has no antecedent: a stage is made inside "every stage ...", which gives nothing outside it
```

```reading
When the person opens the board, the work service shall return every session and the worktree of the session.
refused: "the session" has no antecedent: a session is made inside "every session ...", which gives nothing outside it
```

```reading
While a session follows a stage or the session has a worktree, when the person opens the board, the work service shall complete the request.
refused: "the session" has no antecedent: a session is made inside one case of an "or", which gives nothing outside it
```

```reading
While a stage is `open` or a stage is `done`, when the person opens the board, the work service shall return the stage.
refused: "the stage" has no antecedent: a stage is made inside one case of an "or", which gives nothing outside it
```

```reading
When the person opens the board, the work service shall return a stage or a file, and the work service shall end the stage.
refused: "the stage" has no antecedent: a stage is made inside one case of an "or", which gives nothing outside it
```

```reading
While at least two sessions follow a stage, when the person opens the board, the work service shall return the session.
refused: "the session" has no antecedent: a session is made inside "at least two sessions ...", which gives nothing outside it
```

```reading
When the person opens the board, the work service shall return at least two stages and the status of the stage.
refused: "the stage" has no antecedent: a stage is made inside "at least two stages ...", which gives nothing outside it
```

```reading
When the person opens the board, the work service shall not write a file, and the work service shall return the file.
refused: "the file" has no antecedent: a file is made inside "no file ...", which gives nothing outside it
```

A K made before the box is seen in each case: "the stage" in the first case below is the stage the session follows.

```reading
While a session follows a stage and the stage is `open` or the session has a worktree, when the person opens the board, the work service shall return the stage.
shall [x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: session, x2: stage]
    follow(subject: x1, object: x2)
    or
      case
        status(x2) = `open`
      case [x3: worktree]
        of(x3, x1)
  when
    request(e1, work.open, subject: x4, the board)
  response
    return(e2, subject: x5, object: x2)
```

### "X conforms to A": conformance to a named artifact

"X conforms to A" says that X meets what the artifact A sets out: a form, a schema, a layout, the language reference.
A is a noun of a kind under `artifact` (the request pack's noun), said as a proper noun ("the comment form"), as "the K of
X" ("the requirement grammar of the upstream"), or as a code naming a file (`grammar/language.md`, a parameter). Every
artifact a line conforms to is an object of the domain model that is a kind of artifact (`object layout kind of
artifact`), named by a noun (`- **layout** (noun) → object layout.`) or, when the context keeps one, by a proper noun
(`- **the stage form** (proper noun) → object stage form.`); a context with a glossary declares it with the part of
speech (artifact), `- **the comment form** (artifact): ...` a proper noun of kind artifact. Its entry may give `Schema:`
(the schema type and its file, as in "Schema: json schema, `schemas/comment.json`."), and an attribute entry or a relation
row that is one of its fields may give `Field of: <artifact>` (an attribute in its entry, a row in a cell of its own);
the lexicon reads and keeps both, and nothing checks them yet (b241). The
verb is the request pack's state verb `conform` (Frame: thing conforms to artifact), and its atom is `conforms(x, a)`: in
a While or Where clause and a relative clause it is a state like any other, negated with "does not conform to A",
counted out with "no K conforms to A", and said "a K that conforms to A" or "a K that does not conform to A". A K of
another kind after "to" is refused, naming the verb's frame. "the K of X" after "does not conform to" is the K that X
has, there whether or not X conforms: it stays outside the `not`. In `spec logic` the atom is a state like a
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
While a file does not conform to the stage form, when the person opens the board, the work service shall return the file and not write the file.
shall [x2: artifact the stage form (constant), x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: file]
    not
      conforms(x1, x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x1)
    not
      write(e3, subject: x4, object: x1)
```

```reading
While a file conforms to the stage form and no worktree holds the file, when the person opens the board, the work service shall return the file.
shall [x2: artifact the stage form (constant), x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: file]
    conforms(x1, x2)
    not [x3: worktree]
      in(x1, x3)
  when
    request(e1, work.open, subject: x4, the board)
  response
    return(e2, subject: x5, object: x1)
```

```reading
If the person writes a file that does not conform to the stage form, then the work service shall refuse the request and name the file.
shall [x1: agent the person (constant), x3: artifact the stage form (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: file]
    not
      conforms(x2, x3)
    request(e1, work.write, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

```reading
When the person opens the board, the work service shall return every file that conforms to the stage form.
shall [x1: agent the person (constant), x2: service the work service (constant), x4: artifact the stage form (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    every [x3: file]
      conforms(x3, x4)
      scope
        return(e2, subject: x2, object: x3)
```

```reading
While no file conforms to the stage form, when the person opens the board, the work service shall complete the request.
shall [x2: artifact the stage form (constant), x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while
    not [x1: file]
      conforms(x1, x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    complete(e2, subject: x4, object: x5)
```

The artifact as "the K of X", the worktree's own layout: it is there whether or not the file conforms to it.

```reading
While a worktree holds a file that does not conform to the layout of the worktree, when the person opens the board, the work service shall return the file.
shall [x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: worktree, x2: file, x3: layout]
    of(x3, x1)
    not
      conforms(x2, x3)
    in(x2, x1)
  when
    request(e1, work.open, subject: x4, the board)
  response
    return(e2, subject: x5, object: x2)
```

The artifact as a code naming a file: a parameter of kind artifact (R10).

```reading
While a file does not conform to `docs/stage.md`, when the person opens the board, the work service shall return the file.
shall [x2: artifact `docs/stage.md` (parameter), x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: file]
    not
      conforms(x1, x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x1)
```

```reading
While a file conforms to a stage, when the person opens the board, the work service shall return the file.
refused: the verb conform takes as its recipient artifact or a kind of it: thing conforms to artifact
```

### "the T of X is v" and "X is v": a value, adjective or noun

A line says an attribute's value in the full form, "the T of X is v" ("the status of the item is `idea`", "an item
whose status is `idea`"), which any value takes. The short form "X is v" ("an item is `shaped`") leaves the attribute
out, so it reads as English only when v reads after "is" as an adjective or a participle; with a noun ("an item is
`idea`", "a design-decision is `check`"), a verb phrase ("an item is `needs-input`") or a release ("a repository is
`0.30.0`") it does not. So an attribute entry declares the kind of its values (b257): `Values (adjective):` lists those
the short form takes, `Values (noun):` every other, and an entry may give both. A line that says a noun value in the
short form, "is", "is not", "is one of" or "is not `a` or `b`" after the thing alone, is refused, naming the value,
the attribute and the full form. An entry that gives a plain `Values:` declares neither, and its values keep the short
form as they did in 0.33, which `spec check` warns of (`w_value_kind`). Generated Gherkin says every value in the full
form, "the status of the item i1 is `idea`", so that whoever binds a step reads the attribute in it; a value of "no K"
is "no item whose status is `idea` exists". The constructs are `attribute-is` and `adjective-value`.

Found in backlog r23, r24, r28-r31 (`idea`, `needs-input`), batches r27, r33, decision-tiers r14-r17 (the tiers),
r23 (a route's kind) and pr-review r4, r13-r15 (`judgement`, `fix now`), each reworded to the full form (b257).

```reading
While the tier of a stage is `review`, when the person opens the board, the work service shall end the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    tier(x1) = `review`
  when
    request(e1, work.open, subject: x2, the board)
  response
    end(e2, subject: x3, object: x1)
```

```reading
While a stage is `open`, when the person opens the board, the work service shall end the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
  when
    request(e1, work.open, subject: x2, the board)
  response
    end(e2, subject: x3, object: x1)
```

```reading
While a stage is `review`, when the person opens the board, the work service shall end the stage.
refused: `review` is a noun, a value of the tier of a stage: "a stage is `review`" does not read; write "the tier of the stage is `review`" or "a stage whose tier is `review`"
```

### "the T of X is after v": ordered comparison

An attribute whose entry says `Order:` has ordered values, and a line may compare its value with a value: "the T of X
is after v", "is before v", "is not after v", "is not before v", and "is after v and before w". `Order: by number.`
orders the values by their numbers, as a release is ordered (`1.10.0` is after `1.9.0`), and any code of numbers
joined by dots is a value of it; `Order: as listed.` orders them as `Values:` lists them, and only those are its
values. "the T of X is v" and "X is v" take any such code too. The atom is `cmp(T(x)) after v` (the design's `cmp(x,
A, op, v)`), the time pack's comparison of moments said of an attribute (section "Time"); "is not before v" puts it
under `not`. A code that is no value of the attribute is refused, naming the code and the order; an attribute with
no `Order:` has no "after" or "before". In `spec logic` a comparison is a condition as a value is (`ccmp(R, x, T,
after, point)`), checked exactly over the values the two lines of a pair name and the gaps between them (design call
9): two lines whose ranges share no value never fire together, and a value between two named values (`1.0.1`,
between `1.0.0` and `2.0.0`) is one that an attribute ordered by number may have and one ordered as listed has not.
In a scenario a comparison is a Given of one value on the right side of every value the line names, a value the
entry lists when one is: "the file f1 is `2.0.0`" for "after `1.0.0` and before `3.0.0`", "the file f1 is `3.0.1`"
for "after `3.0.0`".

Found by the audit in migration-tools r36, r39, r40, r41, r42, r45, r46, r51 and r55 (b156): each said a range of
releases as one value of the release (`0.23.1` for "before `0.24.0`") or as "lacks the verb-frames step and does not
lack the simplified-workflow step", which inverts what it means; and b161's line "While the release of the repository
is after `0.32.0` and before `0.33.0`, ..." (now r76). Each says the range with "after" and "before".

```reading
While the version of a file is before `2.0.0`, when the person opens the board, the work service shall return the file.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: file]
    cmp(version(x1)) before `2.0.0`
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

```reading
While the version of a file is after `1.0.0` and before `3.0.0`, when the person opens the board, the work service shall return the file.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: file]
    cmp(version(x1)) after `1.0.0`
    cmp(version(x1)) before `3.0.0`
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

```reading
While the version of a file is not before `2.0.0`, when the person opens the board, the work service shall not write the file.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: file]
    not
      cmp(version(x1)) before `2.0.0`
  when
    request(e1, work.open, subject: x2, the board)
  response
    not
      write(e2, subject: x3, object: x1)
```

A value between two named values: `1.10.0` is after `1.9.0`, as a release is, and needs no entry of its own.

```reading
While the version of a file is after `1.9.0`, when the person opens the board, the work service shall return the file.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: file]
    cmp(version(x1)) after `1.9.0`
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

A value that no entry lists is a value of an attribute ordered by number all the same:

```reading
While the version of a file is `1.0.1`, when the person opens the board, the work service shall return the file.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: file]
    version(x1) = `1.0.1`
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

An attribute ordered as listed: `high` is after `low`.

```reading
While the priority of a stage is after `low`, when the person opens the board, the work service shall end the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    cmp(priority(x1)) after `low`
  when
    request(e1, work.open, subject: x2, the board)
  response
    end(e2, subject: x3, object: x1)
```

```reading
While the version of a file is after `banana`, when the person opens the board, the work service shall return the file.
refused: `banana` is no value of the version of a file, which is ordered by number
```

```reading
While the priority of a stage is before `soon`, when the person opens the board, the work service shall end the stage.
refused: `soon` is no value of the priority of a stage, which is ordered as listed: `low`, `high`, `urgent`
```

### A value order: `Order:` or `Type:`

An attribute's value order (b275) is the order its entry's `Order:` gives (`by number`, `as listed`), or the order
of the type its entry's `Type:` declares: `Type: number.` (any decimal, `-2`, `3.5`), `Type: time.` (a date or a
moment, `2026-01-01`, `2026-01-01T10:00`) or `Type: text.` (any text, in the order of its characters). A value of a
typed attribute is any literal of its type, listed or not, and a typed attribute needs no `Values:` and no `Order:`.
Every comparison and every order below is of an attribute with a value order; on one with none it is refused,
naming the attribute.

```reading
While the status of a stage is after the status of another stage, when the person opens the board, the work service shall return the stage.
refused: the status of a stage has no value order: its entry says neither Order: nor Type:, so one status is never after or before another
```

### "the T of X is after the T of Y", "is the same as the T of Y": one thing's value compared with another's

"the T of X is after the T of Y" and "is before" (`value-compare`) compare two things' values of one attribute with a
value order; "the T of X is the same as the T of Y" (`value-same`) says them equal, of any attribute. Each is one atom,
`cmp(T(x), after, T(y))`, `cmp(T(x), same, T(y))`, under `not` when the line says "is not". In `spec logic` it is
`ccmp2(R, x, T, Op, y, Pol)`, read over the cells of the points the pair names: two lines whose comparisons of the
same two values contradict (one says after, the other before) never fire together, so their opposite acts are no L1.
A cycle of comparisons through three or more things in one gap of a dense order is taken as able to hold: an L1 may
be reported that could never fire, but none is hidden. In a scenario each thing is given a value that meets every
comparison and value the line names ("the version of the `a` file is `1.0.0`", "the version of the file f1 is
`0.0.0`"). The comparison words are after and before for every order; "more than", "at least" and the others between
two values are not yet said. The two sides may be two senses of one attribute word, each of its own entry's kind ("the
version of a worktree is after the version of a file", b287): read so when the two entries have one value order (the
same `Order:` or the same `Type:`), over that order's cells in `spec logic`, and refused naming the word when their
orders differ, for `value-compare` and `value-same` alike.

```reading
While the version of the `a` file is after the version of a file, when a session writes the file, the work service shall return the file.
shall [x1: file `a` (parameter), x4: service the work service (constant)]
  while [x2: file]
    cmp(version(x1), after, version(x2))
  when [x3: session]
    request(e1, work.write, subject: x3, object: x2)
  response
    return(e2, subject: x4, object: x2)
```

```reading
While the status of a stage is the same as the status of another stage, when the person opens the board, the work service shall return the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage, x2: stage]
    distinct(x2, x1)
    cmp(status(x1), same, status(x2))
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x2)
```

### ", ordered by T, in ascending order": a collection or a printed every in order

", ordered by T, in ascending order" or "in descending order" after a collection that holds members by a row `K1 |
in | K2` (`order-by`, T an attribute of K1: "a worktree that holds a file, ordered by version, in descending order")
or after a printed "every K" (`order-by-every`, T an attribute of K) requires the members, or what the agent prints,
in that order. The form keeps one atom, `ordered(x, T, ascending)`, beside the act, x a K that has T: after "every
K" the every's K; after a collection its members (b334), an every box over the K1s of the row, restricted by
`in(m, y)` of the collection y and with `ordered(m, T, ascending)` in its scope (`every [x6: file] in(x6, x4) scope
ordered(x6, version, descending)`), never the collection, which has no T; `spec logic` keeps it as a fact of the act, and two lines that require one collection, or one printing, in opposite orders on one trigger are an L1;
nothing else is proved of an order. A scenario gives three members distinct values of T, in neither the order nor
its reverse, and a Then that states the order ("`work` prints every file, ordered by version, in ascending order"),
which a handler checks by a sorted comparison of the output, not strictly, so that members of one value pass in
either order. A then-by key, a position ("the first K"), the top n and words such as "newest first" are not yet said.

An order that stands before what follows it in its clause, a recipient or an oblique, closes with a comma, as an
apposition does: "give every file, ordered by version, in ascending order, to the person" (b301). At the end of its
clause it takes none. The form without the closing comma ("in ascending order to the person") is read too, to the
same tree, and the comma form is the one written back; an order after the recipient ("to the person, ordered by
...") is refused, since the order belongs to its noun phrase.

```reading
When the person opens the board, the work service shall give every file, ordered by version, in ascending order, to the person.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    every [x3: file]
      scope
        give(e2, subject: x2, object: x3, to: x1)
        ordered(x3, version, ascending)
```

```reading
When the person opens the board, the work service shall return every file, ordered by version, in ascending order.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    every [x3: file]
      scope
        return(e2, subject: x2, object: x3)
        ordered(x3, version, ascending)
```

```reading
When the person opens the board, the work service shall return every line, ordered by verdict, in ascending order.
refused: the verdict of a line has no value order: its entry says neither Order: nor Type:, so no verdict comes before another, and nothing is ordered by it
```

An order has a reading only as a property of what a response prints (b285): one in a While or Where clause, in the
trigger, or in an act the line forbids ("shall not print ..., ordered by T": "not in this order" is no operation the
check or a scenario has) is refused, naming the order.

```reading
While a session has a worktree that holds a file, ordered by version, in descending order, when the person opens the board, the work service shall return the worktree.
refused: "ordered by version, in descending order" is in a precondition: an order is a property of what a response prints, and has no reading there
```

```reading
When the person inspects a worktree that holds a file, ordered by version, in descending order, the work service shall return the worktree.
refused: "ordered by version, in descending order" is in the trigger: an order is a property of what a response prints, and has no reading there
```

```reading
When the person opens the board, the work service shall not return every file, ordered by version, in ascending order.
refused: "ordered by version, in ascending order" is in an act the line forbids: an order is a property of what a response prints, and "not in this order" has no reading
```

### "is one of `a` or `b`", "is not `a` or `b`", "has no T": value sets and a value's absence

A line may name a set of an attribute's values: "the T of X is one of `a`, `b` or `c`" and "X is one of `a`, `b` or
`c`" say that the value is one of them, a case of an "or" for each value (section "the K outside the box ...": a case
holds what its side says); "the T of X is not `a`, `b` or `c`" and "X is not `a`, `b` or `c`" say that it is none of
them, a `not` for each value. "None of them" is not "some other value the entry lists": a thing whose T has no value
is none of them too. "X has no T" says that X's T has no value at all, the atom `T(x) = none`: a fact of its own,
which no listed value meets, so "has no T" and "is `a`" never hold of one thing together, while "has no T" and "is
not `a`" do. "every K of X is `v`" (and "is one of ...", "is not ...") says it of each K of X. The list names each
value once and takes at least two; a value of another attribute is no member of it. In `spec logic` a set is the
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
While a line is one of `proposed`, `accepted` or `refused`, when the person opens the board, the work service shall return the line.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: line]
    or
      case
        verdict(x1) = `proposed`
      case
        verdict(x1) = `accepted`
      case
        verdict(x1) = `refused`
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

```reading
While the priority of a stage is one of `low` or `high`, when the person opens the board, the work service shall end the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    or
      case
        priority(x1) = `low`
      case
        priority(x1) = `high`
  when
    request(e1, work.open, subject: x2, the board)
  response
    end(e2, subject: x3, object: x1)
```

"is not `a`, `b` or `c`": none of them.

```reading
While a stage is `open` and a line of the stage is not `accepted`, `refused` or `withdrawn`, when the person opens the board, the work service shall return the line.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage, x2: line]
    status(x1) = `open`
    of(x2, x1)
    not
      verdict(x2) = `accepted`
    not
      verdict(x2) = `refused`
    not
      verdict(x2) = `withdrawn`
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x2)
```

```reading
While the priority of a stage is not `low` or `high`, when the person opens the board, the work service shall end the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    not
      priority(x1) = `low`
    not
      priority(x1) = `high`
  when
    request(e1, work.open, subject: x2, the board)
  response
    end(e2, subject: x3, object: x1)
```

"has no T": the value absent, which is no listed value.

```reading
While a stage is not `done` and the stage has no priority, when the person opens the board, the work service shall return the stage.
shall [x2: agent the person (constant), x3: service the work service (constant)]
  while [x1: stage]
    not
      status(x1) = `done`
    priority(x1) = none
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

"every K of X is `v`", and "is one of" said of each K of X:

```reading
While a stage is `open` and every line of the stage is `accepted`, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    every [x2: line]
      of(x2, x1)
      scope
        verdict(x2) = `accepted`
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While a stage is `open` and every line of the stage is one of `accepted`, `refused` or `withdrawn`, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    every [x2: line]
      of(x2, x1)
      scope
        or
          case
            verdict(x2) = `accepted`
          case
            verdict(x2) = `refused`
          case
            verdict(x2) = `withdrawn`
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While a line is one of `accepted` or `accepted`, when the person opens the board, the work service shall return the line.
refused: the list of the verdict of a line names `accepted` twice
```

### "the number of Ks that P": a count as a value

"the number of Ks that P" is a value: a line may print it, and may compare it with a number. Its noun is any kind's
in the plural with what restricts it ("lines of the stage", "sessions that follow the stage", "lines of the stage
whose outcome is `accepted`"). Printed, it is a referent of its own, `x: number`, and a `number` box that says what it
counts: `number x of [y: K]` over the restrictions of y; the Ks it counts are made inside the box, so no "the K"
outside it binds to them (R2). Compared, "the number of Ks that P is more than n" is the count box of R7 over the Ks
with nothing in its scope: "is more than", "is less than" (R7's "fewer than"), "is at least", "is at most" and "is"
(exactly), n a number word from one to ten or a code; a code of digits is that number, any other code (`batch_size`)
a parameter (R10), which the box names. In `spec logic` a printed number is an object of its own whose restrictions
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
When a session ends a stage, the work service shall return the number of lines of the stage.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: line]
      of(x5, x2)
    return(e2, subject: x3, object: x4)
```

```reading
When a session ends a stage, the work service shall return the number of sessions that follow the stage.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: session]
      follow(subject: x5, object: x2)
    return(e2, subject: x3, object: x4)
```

```reading
When a session ends a stage, the work service shall return the number of lines of the stage whose verdict is `accepted`.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: number]
    number x4 of [x5: line]
      of(x5, x2)
      verdict(x5) = `accepted`
    return(e2, subject: x3, object: x4)
```

"shall not print the number of Ks": under `not`, as any object of "shall not" (batch-measurement r24).

```reading
When a session ends a stage, the work service shall not return the number of lines of the stage.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response
    not [x4: number]
      number x4 of [x5: line]
        of(x5, x2)
      return(e2, subject: x3, object: x4)
```

Compared: R7's count box, with nothing in its scope.

```reading
While a stage is `open` and the number of lines of the stage is more than three, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    count more than 3 [x2: line]
      of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While a stage is `open` and the number of lines of the stage is less than `3`, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    count fewer than 3 [x2: line]
      of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While a stage is `open` and the number of lines of the stage is `0`, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    count exactly 0 [x2: line]
      of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

A code that is no number is a parameter:

```reading
While a stage is `open` and the number of lines of the stage is more than `limit`, when the person opens the board, the work service shall end the stage.
shall [x3: number `limit` (parameter), x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: stage]
    status(x1) = `open`
    count more than x3 [x2: line]
      of(x2, x1)
  when
    request(e1, work.open, subject: x4, the board)
  response
    end(e2, subject: x5, object: x1)
```

The Ks a number counts are made inside its box:

```reading
When a session ends a stage, the work service shall return the number of files in the worktree of the session, and the work service shall return the file.
refused: "the file" has no antecedent: a file is made inside "the number of files ...", which gives nothing outside it
```

### "another K", "a different K", "two Ks" and "the same K": identity and distinctness

Two noun phrases of one kind may name one thing or two. "a K" never says which: two Ks of a line may be one thing.
These four say it:

- "another K" and "a different K" (one meaning) are a K that is not the K before it: a referent of its part as "a K"
  is (R1), and the atom `distinct(y, x)`, x the referent "the K" would bind to by R2 in its place: the latest earlier
  referent of kind K (or of a kind under it) not made inside a box that does not hold it. When that referent came
  from "two Ks", y is distinct from both. With no such referent the line is refused, naming the noun, as R2 refuses
  "the K"; "another K" never names the image of a row nor the request's own K.
- "two Ks" are two Ks, each distinct from the other: two referents, the second with `distinct(y, x)`, and the clause
  said of each, as of "a K and a K" (so "two sessions follow a stage" is one stage both follow). What restricts the
  noun restricts each; a K its restriction makes is one K they share ("two files in a worktree": one worktree). A
  later "the K" names neither and is refused.
- "the same K" binds as "the K" does (R2): to the latest earlier K, else the image of a row, else the request's own K. When
  R2 gives it nothing and the line said "two Ks" before it, it is one new K (R1), which each of the two shares: "two
  sessions follow the same stage". Else it is refused as "the K" is.

`spec logic` reads `distinct(y, x)` as two things its unification never makes one: when one line's two referents
it holds would be one thing of a pair (one code named of both, a definite both bind to), the pair is not read under
that unification. A trigger of one act on each of "two Ks" ("writes two files", of a verb naming no operation: a
request acts on one thing, so "two Ks" in a request's object is no reading, b420) is one act of the line, a trigger of
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
When a session gives a file to another session, the work service shall return the file.
shall [x4: service the work service (constant)]
  when [x1: session, x2: file, x3: session]
    distinct(x3, x1)
    request(e1, work.give, subject: x1, object: x2, to: x3)
  response
    return(e2, subject: x4, object: x2)
```

```reading
When a session gives a file to a different session, the work service shall return the file.
shall [x4: service the work service (constant)]
  when [x1: session, x2: file, x3: session]
    distinct(x3, x1)
    request(e1, work.give, subject: x1, object: x2, to: x3)
  response
    return(e2, subject: x4, object: x2)
```

"the same K" bound to the earlier K, the twin of "another requirement of the same trigger" (design-model-check
r276-r278):

```reading
While a session follows a stage and another session follows the same stage, when the person opens the board, the work service shall return the stage.
shall [x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: session, x2: stage, x3: session]
    follow(subject: x1, object: x2)
    distinct(x3, x1)
    follow(subject: x3, object: x2)
  when
    request(e1, work.open, subject: x4, the board)
  response
    return(e2, subject: x5, object: x2)
```

"two Ks" of "the same K", the twin of "two requirements share an id" (design-model-check r176):

```reading
While two sessions follow the same stage, when the person opens the board, the work service shall end the stage.
shall [x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: session, x3: stage, x2: session]
    follow(subject: x1, object: x3)
    distinct(x2, x1)
    follow(subject: x2, object: x3)
  when
    request(e1, work.open, subject: x4, the board)
  response
    end(e2, subject: x5, object: x3)
```

What restricts "two Ks" restricts each, and a K it makes is one both share:

```reading
While two files in a worktree cover a line, when the person opens the board, the work service shall return the worktree.
shall [x5: agent the person (constant), x6: service the work service (constant)]
  while [x1: file, x2: worktree, x4: line, x3: file]
    in(x1, x2)
    cover(subject: x1, object: x4)
    distinct(x3, x1)
    in(x3, x2)
    cover(subject: x3, object: x4)
  when
    request(e1, work.open, subject: x5, the board)
  response
    return(e2, subject: x6, object: x2)
```

In a response, two new Ks:

```reading
When a session ends a stage, the work service shall write two files.
shall [x3: service the work service (constant)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: file, x5: file]
    write(e2, subject: x3, object: x4)
    distinct(x5, x4)
    write(e3, subject: x3, object: x5)
```

"another K" after "two Ks" is distinct from both:

```reading
While two sessions follow a stage, when the person assigns another session, the work service shall return the stage.
shall [x4: agent the person (constant), x6: service the work service (constant)]
  while [x1: session, x3: stage, x2: session]
    follow(subject: x1, object: x3)
    distinct(x2, x1)
    follow(subject: x2, object: x3)
  when [x5: session]
    distinct(x5, x1)
    distinct(x5, x2)
    request(e1, work.assign, subject: x4, object: x5)
  response
    return(e2, subject: x6, object: x3)
```

Two lines on one request in two states: the first's two files are in one worktree, the second's in two, so `spec
logic` finds no witness where both fire, and no L1:

```reading
While a file in a worktree and another file in the same worktree cover a line, when the person opens the board, the work service shall return the worktree.
shall [x5: agent the person (constant), x6: service the work service (constant)]
  while [x1: file, x2: worktree, x4: line, x3: file]
    in(x1, x2)
    cover(subject: x1, object: x4)
    distinct(x3, x1)
    in(x3, x2)
    cover(subject: x3, object: x4)
  when
    request(e1, work.open, subject: x5, the board)
  response
    return(e2, subject: x6, object: x2)
```

```reading
While a file in a worktree and another file in a different worktree cover a line, when the person opens the board, the work service shall not return the worktree.
shall [x6: agent the person (constant), x7: service the work service (constant)]
  while [x1: file, x2: worktree, x5: line, x3: file, x4: worktree]
    in(x1, x2)
    cover(subject: x1, object: x5)
    distinct(x3, x1)
    distinct(x4, x2)
    in(x3, x4)
    cover(subject: x3, object: x5)
  when
    request(e1, work.open, subject: x6, the board)
  response
    not
      return(e2, subject: x7, object: x4)
```

The refusals: "another K" with no K before it, or with every K before it inside a box; "the same K" with neither an
antecedent nor "two Ks" before it; "the K" after "two Ks".

```reading
When a session ends another stage, the work service shall return the stage.
refused: "another stage" has no antecedent: no earlier noun phrase gives a stage
```

```reading
While no session follows a stage, when the person opens the board, the work service shall end another stage.
refused: "another stage" has no antecedent: a stage is made inside "no session ...", which gives nothing outside it
```

```reading
When the person opens the board, the work service shall end the same stage.
refused: "the same stage" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a stage
```

```reading
While two sessions follow a stage, when the person opens the board, the work service shall return the session.
refused: "the session" has no antecedent: "two sessions" gives two sessions, and "the session" names neither
```

### "X exists" and "no K exists": existence

"X exists" says that the thing X is there: a state of X whose frame takes no object, the atom `exists(x)`. Every kind
has it, with no entry in the glossary: "exist" is the base grammar's verb, a state, so a trigger may not say it ("When
a file exists" is refused as a state verb in a trigger is). "X does not exist" puts the atom under `not`; "no K
exists" is R3's "no K", a `not` box with its K; "a K that exists" and "a K whose T does not exist" are relative
clauses as any state gives them. In `spec logic` existence is the one-place fluent `crel(R, exists, x, none, Pol)`
(the state whose frame takes no object, b219), and "no K exists" `rnone(R, exists, kind(K), none)`: "the `a` file
exists" clashes with "the `a` file does not exist" and with "no file exists", but not with "the `b` file does not
exist". In a scenario it is a Given, "the file f1 exists", "the `a` file does not exist" or "no file exists", which
the world meets by making the thing or leaving it out.

"has been written" is not existence: it is the perfect of an action, the history of section "Time" (built, and
refused by `spec logic` as any history is). A line that means that a thing is there says "exists"; one that means
that an act happened before says the perfect.

Found by the audit in analysis-tools r37-r41 ("this file system holds the dot-venv interpreter": a container noun
and a row coined to say that a file is there; the interpreter that is used is the first that exists, each case
written with existence, the order a known limit, #14), r48 and r50-r55 ("this repository holds a coverage map", "holds
no coverage map"), and requests r72 ("a bounded context that has no host", the upstream's entry with no repository)
and r81 (every with no existential import: "every request line ... is `refused`" holds of a request with no lines,
so the line says that one exists too).

```reading
While the `a` file exists, when the person opens the board, the work service shall return the file.
shall [x1: file `a` (parameter), x2: agent the person (constant), x3: service the work service (constant)]
  while
    exists(x1)
  when
    request(e1, work.open, subject: x2, the board)
  response
    return(e2, subject: x3, object: x1)
```

"X does not exist": each case of a first match said with existence (analysis-tools r38-r40).

```reading
While the `b` file exists and the `a` file does not exist, when the person opens the board, the work service shall return the `b` file.
shall [x1: file `b` (parameter), x2: file `a` (parameter), x3: agent the person (constant), x4: service the work service (constant)]
  while
    exists(x1)
    not
      exists(x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x1)
```

```reading
While a file in a worktree exists, when the person opens the board, the work service shall return the file.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: file, x2: worktree]
    in(x1, x2)
    exists(x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    return(e2, subject: x4, object: x1)
```

"no K exists" (analysis-tools r55):

```reading
While no file exists, if the person opens the board, then the work service shall refuse the request and name `work start`.
shall [x2: agent the person (constant), x3: service the work service (constant), x4: request "the request the trigger makes" (indexical), x5: thing `work start` (parameter)]
  while
    not [x1: file]
      exists(x1)
  if
    request(e1, work.open, subject: x2, the board)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x5)
```

"whose T does not exist" (requests r72):

```reading
If the person assigns a session whose worktree does not exist, then the work service shall refuse the request and name the session.
shall [x1: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  if [x2: session, x3: worktree]
    of(x3, x2)
    not
      exists(x3)
    request(e1, work.assign, subject: x1, object: x2)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x2)
```

"every K of X is v" holds of an X with no K; "a K of X exists and every K of X is v" says there is one (requests r81):

```reading
While a stage is `open` and a line of the stage exists and every line of the stage is `refused`, when the person opens the board, the work service shall end the stage.
shall [x4: agent the person (constant), x5: service the work service (constant)]
  while [x1: stage, x2: line]
    status(x1) = `open`
    of(x2, x1)
    exists(x2)
    every [x3: line]
      of(x3, x1)
      scope
        verdict(x3) = `refused`
  when
    request(e1, work.open, subject: x4, the board)
  response
    end(e2, subject: x5, object: x1)
```

```reading
When the person opens the board, the work service shall return every file that exists.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    every [x3: file]
      exists(x3)
      scope
        return(e2, subject: x2, object: x3)
```

```reading
When a session exists, the work service shall return the session.
refused: the verb exist is a state, and a trigger takes an action
```

### "with the p v", "without a p": a request's parameters

A request's parameters are in the trigger, after the operation's object (the domain contract design, §5.1): "with the
p v" (a value of the parameter, a code, or a thing the line says more of), "with a p" (the parameter given, any value),
"with the p" of a flag (a boolean parameter, written `<p> (flag)` in the domain model), "without a p" and "without the
p" (not given); an "and" list says several of one request ("with a source and a thread", "without the summary and a
note": none of them). The parameters a line may say are its operation's, and the values a parameter takes its own:
grammar 4 generates no other. The request is one atom, `request(e, O, subject: requester, object: x)`, O the
operation's id, and each parameter `param(e, p, v)` (`some` of "with a p", `on` of a flag) or `noparam(e, p)` beside
it. In `spec logic` a request's trigger is its operation and the parameters the line says, as one key: a parameter
given in one line and absent in another makes two requests, so the line pairs with every line on the same parameter
set, and a thing a parameter names is part of what the request is on. In a scenario the When names each parameter as
the line does, and the step's Call gives them to its handler (`params`: each parameter with its value or None,
`without`: each parameter not given).

Found by the audit, in CLI words, in requests r59-r62, r102 (options of `work request`), U16 and backlog r27 ("with the
`--json` option"), and decision-tiers r20 and intake r13 (an argument not given); this repository rewords them as
requests with their parameters.

A flag:

```reading
When the person opens the board with the summary, the work service shall complete the request.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
    param(e1, summary, on)
  response
    complete(e2, subject: x2, object: x3)
```

Two parameters of one request, each given:

```reading
If the person opens the board with a source and a thread, then the work service shall refuse the request and name the source.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical), x4: parameter source (constant)]
  if
    request(e1, work.open, subject: x1, the board)
    param(e1, source, some)
    param(e1, thread, some)
  response
    refuse(e2, subject: x2, object: x3)
    name(e3, subject: x2, object: x4)
```

A parameter of a request on a thing:

```reading
When the person settles a line with a note, the work service shall return the line.
shall [x1: agent the person (constant), x3: service the work service (constant)]
  when [x2: line]
    request(e1, work.settle, subject: x1, object: x2)
    param(e1, note, some)
  response
    return(e2, subject: x3, object: x2)
```

A parameter's value, a code:

```reading
When the person opens the board with the interval `5`, the work service shall complete the request.
shall [x1: agent the person (constant), x2: thing `5` (parameter), x3: service the work service (constant), x4: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
    param(e1, interval, x2)
  response
    complete(e2, subject: x3, object: x4)
```

A parameter that names a thing the line says more of:

```reading
If the person opens the board with a stage whose status is not `done`, then the work service shall refuse the request and name the stage.
shall [x1: agent the person (constant), x3: service the work service (constant), x4: request "the request the trigger makes" (indexical)]
  if [x2: stage]
    not
      status(x2) = `done`
    request(e1, work.open, subject: x1, the board)
    param(e1, stage, x2)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x2)
```

A parameter not given, two not given, and not given on a request on a thing:

```reading
If the person opens the board without the summary, then the work service shall refuse the request and name the summary.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical), x4: parameter summary (constant)]
  if
    request(e1, work.open, subject: x1, the board)
    noparam(e1, summary)
  response
    refuse(e2, subject: x2, object: x3)
    name(e3, subject: x2, object: x4)
```

```reading
If the person opens the board without a source and a thread, then the work service shall refuse the request and name the source.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: request "the request the trigger makes" (indexical), x4: parameter source (constant)]
  if
    request(e1, work.open, subject: x1, the board)
    noparam(e1, source)
    noparam(e1, thread)
  response
    refuse(e2, subject: x2, object: x3)
    name(e3, subject: x2, object: x4)
```

```reading
If a session settles a line without a note, then the work service shall refuse the request and name the note.
shall [x3: service the work service (constant), x4: request "the request the trigger makes" (indexical), x5: parameter note (constant)]
  if [x1: session, x2: line]
    request(e1, work.settle, subject: x1, object: x2)
    noparam(e1, note)
  response
    refuse(e2, subject: x3, object: x4)
    name(e3, subject: x3, object: x5)
```

A parameter the operation does not declare is no word of the line: "with a colour" does not parse.

### "with the T of another K": a value in use

A parameter that is the word of an attribute T takes, beside a code and a value T lists, "the T of" a thing of a kind
that has T as its value (b418, construct `param-of`): "with the verdict of another line" is a request whose parameter
is the value another line has. Every wording of a parameter's value is one referent of the logical form with
conditions on it (design-decision 0110): `param(e, T, v)` beside `T(x) = v`, and a code given as the value (of kind T,
as the image is) or a value T lists is that referent too. In `spec logic` the parameter's value is part of what the
request is on, so a line of the value in use and a line of a code or a listed value on the same request are one
request when the unification keeps one value, and their responses are checked against each other. In a scenario the
other thing is brought in by a Given with a value made up (a text's its referent's name, `t1`; of a T with listed
values its first), and the When's request is given the same value as a code: nothing reads a collection.

```reading
If a session settles a line with the verdict of another line, then the work service shall refuse the request.
shall [x5: service the work service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x1: session, x2: line, x3: line, x4: verdict]
    distinct(x3, x2)
    verdict(x3) = x4
    request(e1, work.settle, subject: x1, object: x2)
    param(e1, verdict, x4)
  response
    refuse(e2, subject: x5, object: x6)
```

An operation whose object is its `done →` outcome's and that no parameter names makes its object: a scenario brings
it in in the When ("When the person adds a note n1 with a title"), never by a Given, which a test could read as the
thing put in the store first.

### "shall hold the product with the quantity of the order": a response makes a request

A response's act whose verb names an operation, said with its parameters after "with" and "without" as a trigger's
request is, is a request too (b543, construct `response-request`; design-decisions 0115 and 0122): the core asks a
driven port, or any service, for an operation, its doer the requester. Its logical form is a trigger's: `request(e,
O, subject: D, ...)` with `param` and `noparam` (`request-params`). `spec check` counts it as a request of O (v_m7),
and a line triggered on the refusal of the thing O is on states O's refusal reasons (v_m4). A response's act of such a
verb said with no parameter keeps its event atom. What the request then sets off in the service's own lines is not
followed yet.

```reading
When a session ends a stage, the work service shall settle a line with the note `n1` and without a verdict.
shall [x3: service the work service (constant), x5: thing `n1` (parameter)]
  when [x1: session, x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response [x4: line]
    request(e2, work.settle, subject: x3, object: x4)
    param(e2, note, x5)
    noparam(e2, verdict)
```

### "completes the request to settle a line": a trigger on a reply

A trigger may be a service's reply to a request (b626, construct `reply-trigger`; design-decisions 0121, 0127 and
0134): the request pack's complete, return or refuse said of "the request to <operation verb> <np>", the request of
the operation the verb names on the thing its frame's object gives, so a compensation or a lifecycle waiting on a
reply can be written ("If the registry refuses the request to publish a design-decision, then ..."). It is generated
for every frame of a verb naming an operation, over the frame's arguments; the request's parameters are not said in
it. Its logical form is a referent r of kind `request` with `request(r, O, object: x)`, the reply's act on r; "the
request" after it in the line is r. Its noun phrases are read as any are: R2 binds "the K" in it to an earlier K, so
the first mention of the request's object is "a K".

```reading
When the work service completes the request to settle a line, the work service shall keep the line.
shall [x1: service the work service (constant)]
  when [x2: request, x3: line]
    request(x2, work.settle, object: x3)
    complete(e1, subject: x1, object: x2)
  response
    keep(e2, subject: x1, object: x3)
```

```reading
If the work service refuses the request to end a stage, then the work service shall not set the status of the stage to `done`.
shall [x1: service the work service (constant)]
  if [x2: request, x3: stage]
    request(x2, work.end, object: x3)
    refuse(e1, subject: x1, object: x2)
  response
    not
      initiates(e2, subject: x1, status(x3) = `done`)
```

`spec logic` reads a reply as the trigger `trig(R, reply(K), req(O,()), D, X)` (b724), K the outcome the reply's
verb says, D the service that replies and X the replied request's object, so two lines on one reply clash (decision
0121); `spec check`'s bound check counts a core line on a reply of an outcome's kind to the request of a port's
operation as handling that outcome (v_pb2), a refusal each of its reasons; `features generate` brings the replied
request's object in by a Given, says the core's request of it as a Given in the present by the response's doer, and
the reply as the When.

### "the person lists a checklist", "the person lists the checklists": a request acts on one thing

A request, a verb naming an operation in a trigger, acts on one thing (b420, design-decision 0111): a slot its frame
names a kind of takes one thing's noun phrase, never one in the plural, with "every", a count or a number word, or a
list joined by "and". A collection a request acts on is said by its frame's own words, and one verb may name several
operations, one by each frame: "Frame: <actor> lists <checklist>." (the items of one checklist) beside "Frame: <actor>
lists the checklists." (every checklist) read "the person lists the checklists" by the second frame alone, since the
first frame's object would be a plural. A line whose every reading gives a request a plural object is refused naming
the object and the verb; one request on several objects is several requests. A response's act of such a verb is no
request and keeps its plurals ("the toolchain service shall install every analysis tool"), and so do the frames of a
verb naming no operation. A line that still reads two ways is refused naming its words and, when its readings are two
frames of one verb, both frames.

```reading
When the person ends every stage, the work service shall complete the request.
refused: a request acts on one thing: "every stage" is a plural object of end; say one thing, or the collection by its frame's own words
```

### "this request", "the commit", "the push of the commit": the request's own things

A thing a request makes is said, for a kind whose entry has `This:`, as the request's own K (R11: "the commit", "this
commit"), and as the image of it by a row (`commit has → push (one)`: "the push of the commit", the push of the commit
the request makes); the request itself is the request pack's `This:` ("this request", "the request"). Nothing is
built for them: each kind the audit names (the Python interpreter, the decisions index, the git directory, the
transcript, the push a command makes) gets its row or its `This:` in the reword whose lines use it. These are the
twins of each shape.

Found by the audit in analysis-tools r43-r46 and r66 ("the dot-venv interpreter", the interpreter `tools` runs
with), decision-tiers r19 ("a decisions index": the one index of the repository), conversation r6 (the git directory,
the transcript) and the push and the commit a `work` command makes.

```reading
When the person opens the board, the work service shall return the push of the commit.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: commit "the commit the request makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
  response [x4: push]
    of(x4, x3)
    return(e2, subject: x2, object: x4)
```

```reading
When the person opens the board, the work service shall keep this commit and return this request.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: commit "the commit the request makes" (indexical), x4: request "the request the trigger makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    keep(e2, subject: x2, object: x3)
    return(e3, subject: x2, object: x4)
```

### What parses is read: a verb of two frames, "shall not V a K that P", "no K that P", "every K that no K Vs"

A line that parses to one meaning is read by `spec logic`'s check and by `features generate`'s steps, never refused
for want of a translation (b236, b237, b238, and the audit's section 3: "the generator and the bar lag the grammar").
Nothing new is said here; these are the shapes the check or the steps had no reading of:

- a verb whose entry has two `Frame:` lines of the same role labels ("Frame: file covers line. Frame: stage covers
  line.") is stepped in the frame its referents' kinds pick, the frame the parse typed the clause by (b236:
  migration-tools' supersede, b156 r29 and r30; decision-tiers' enforce, b159 r15);
- "shall not V a K that P", "shall V no K that P" and "shall not V a K of x", over a K the line names nowhere before
  (R4: under "shall not", "a K" is any K), is a Then that the agent does not V a K brought in with what the line says
  of it (b237: feature-file-tools r86 and r87, b157, "not write a scenario line of the requirement group"; batches
  r22, b158, "shall not pick an item that has the dependency"); "not V the T of x", over a row's image, was read
  already (the audit's "not close the issue of the request");
- "no K that is related to a K whose T is not v" (a `not` inside the "no" box, on its own K) is read by the check as
  a box of its own: no instances of its Ks are so related in the state the pair merges, with the inner one's T known
  to be another value (b238: batches r20, b158, "the item has no dependency on an item whose status is not
  `delivered`"); its Given, as of any "no" box of more than one atom, is said of the box's link to the thing outside
  it ("the session s1 has no worktree"), which makes the line's state hold (b159 r15, "no review finding on the pull
  request is `fix now`");
- "every K that no K2 Vs" and "every K that x does not V" in a response (the audit's "every function of the Python
  file that no test executes") are, in the check, a negated restriction of the object as "whose T is not v" is
  (`onrel`: it agrees only with the same restriction on the other line's object), and in the steps a Given said of
  "no K2" for each K brought in;
- "V a K that holds only K2s that P" and "V a K that holds at most n K2s" (`only` and `count` over the row or state
  of a response's object, R5 and R7, `holds-relation`) are, in the check, restrictions of that object it keeps and
  proves nothing of (`oonly`, `ocount`, decision 0093): they oblige no act of their own, agree with any line on the
  act and clash with nothing, and a Then on such an object is never asked of the entailment check; in the steps, the
  Then is the property said of the object, "the worktree w1 holds only files whose version is `2.0.0`", "the
  worktree w1 holds at most three files" (b272). `spec logic` prints each line it has no translation of, `unread
  <id>: <what it cannot read>`, and never `no findings` beside one.

```reading
While a stage covers a line, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage, x2: line]
    cover(subject: x1, object: x2)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While a line is `proposed` and no stage covers the line, if the person opens the board, then the work service shall refuse the request and name the line.
shall [x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while [x1: line]
    verdict(x1) = `proposed`
    not [x2: stage]
      cover(subject: x2, object: x1)
  if
    request(e1, work.open, subject: x3, the board)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

```reading
When the person opens the board, the work service shall end no stage that a session follows.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response
    not [x3: stage, x4: session]
      follow(subject: x4, object: x3)
      end(e2, subject: x2, object: x3)
```

```reading
When the person ends a stage, the work service shall not return a line of the stage.
shall [x1: agent the person (constant), x3: service the work service (constant)]
  when [x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response
    not [x4: line]
      of(x4, x2)
      return(e2, subject: x3, object: x4)
```

```reading
While a stage has a line whose verdict is not `accepted`, when the person opens the board, the work service shall not end a stage that has the line.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage, x2: line]
    not
      verdict(x2) = `accepted`
    of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    not [x5: stage]
      of(x2, x5)
      end(e2, subject: x4, object: x5)
```

```reading
When the person opens the board, the work service shall not return the push of the commit.
shall [x1: agent the person (constant), x2: service the work service (constant), x3: commit "the commit the request makes" (indexical)]
  when
    request(e1, work.open, subject: x1, the board)
  response [x4: push]
    of(x4, x3)
    not
      return(e2, subject: x2, object: x4)
```

```reading
While a session has no worktree that holds a file whose version is not `2.0.0`, when the person opens the board, the work service shall complete the request.
shall [x4: agent the person (constant), x5: service the work service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: session]
    not [x2: worktree, x3: file]
      not
        version(x3) = `2.0.0`
      in(x3, x2)
      of(x2, x1)
  when
    request(e1, work.open, subject: x4, the board)
  response
    complete(e2, subject: x5, object: x6)
```

```reading
While a stage has no line whose verdict is not `accepted`, when the person opens the board, the work service shall end the stage.
shall [x3: agent the person (constant), x4: service the work service (constant)]
  while [x1: stage]
    not [x2: line]
      not
        verdict(x2) = `accepted`
      of(x2, x1)
  when
    request(e1, work.open, subject: x3, the board)
  response
    end(e2, subject: x4, object: x1)
```

```reading
While no line of a stage is `accepted`, when the person opens the board, the work service shall complete the request.
shall [x3: agent the person (constant), x4: service the work service (constant), x5: request "the request the trigger makes" (indexical)]
  while
    not [x1: line, x2: stage]
      of(x1, x2)
      verdict(x1) = `accepted`
  when
    request(e1, work.open, subject: x3, the board)
  response
    complete(e2, subject: x4, object: x5)
```

```reading
When the person ends a stage, the work service shall return every line of the stage that no file covers.
shall [x1: agent the person (constant), x3: service the work service (constant)]
  when [x2: stage]
    request(e1, work.end, subject: x1, object: x2)
  response
    every [x4: line]
      of(x4, x2)
      not [x5: file]
        cover(subject: x5, object: x4)
      scope
        return(e2, subject: x3, object: x4)
```

```reading
When the person assigns a session, the work service shall return every stage that the session does not follow.
shall [x1: agent the person (constant), x3: service the work service (constant)]
  when [x2: session]
    request(e1, work.assign, subject: x1, object: x2)
  response
    every [x4: stage]
      not
        follow(subject: x2, object: x4)
      scope
        return(e2, subject: x3, object: x4)
```

```reading
When the person opens the board, the work service shall return a worktree that holds only files whose version is `2.0.0`.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response [x3: worktree]
    only [x4: file]
      version(x4) = `2.0.0`
      scope
        in(x4, x3)
    return(e2, subject: x2, object: x3)
```

```reading
When the person opens the board, the work service shall return a worktree that holds at most three files.
shall [x1: agent the person (constant), x2: service the work service (constant)]
  when
    request(e1, work.open, subject: x1, the board)
  response [x3: worktree]
    count at most 3 [x4: file]
      scope
        in(x4, x3)
    return(e2, subject: x2, object: x3)
```

## What the language cannot say yet

The limits the rewording keeps, one subsection a limit: the construct the language has not, the lines that need it
by id, and the plain line each says instead. A corpus block of such a line gives `Known limit: #<n>` as its trace.

### #1: words about the language that no construct's code says

A line about a line names the construct it uses by its code in the construct catalogue ("a requirement that uses
`count`", the spec pack's use and violate, b124); a few things a line says of a requirement are no construct of the
catalogue, and their words stay meta-level words of the glossary: a frame's role a requirement leaves out (omit,
object, recipient), two counts no number meets both of (contradict), and a refusal or a construct the context does
not read (the clock trigger of the time pack this repository does not import, the perfect whose construct code
`done` is a value here, a number where a duration is due). Lines: design-model-check r205, r206 (omit an object, a
recipient), r253 (a count that contradicts a count), r255 (a clock trigger), r256 (a perfect), r257 (a number that
has no unit). Each says the thing in the glossary's words, the word a term of the capability.

### #13: what a command would write

A line that says X differs from what a command writes now ("is not what `spec decisions` would write") compares X
with a counterfactual: the output of a run that has not happened. The language has no noun phrase for it: "what
`spec decisions` writes" is no noun phrase (no free relative), and "does not conform to" takes an artifact, which a
command's output is not. Lines: design-model-check r202, r203 (the decisions index), r220 (the rule catalogue),
feature-file-tools r106 (a feature that is not what `features generate` writes).
Each says instead what the stale file lacks, in the item's words: "While a design-decision has an index entry that a
decisions index does not hold, if the person runs `spec decisions --check`, then `model` shall exit with an error
naming the decisions index and change no file."; the rows that are extra or changed are lost.
readiness r33 (b157 r27: the scenarios `features generate` would write of an item's lines) says what the item's
scenario holds as if the item had it: "While an item is `shaped` and a scenario of the item has a step that holds a
placeholder, ...".

### #6: a value compared with another thing's value

The language says it now (b275, `value-compare` and `value-same`: "the release of the repository is after the release
of `migrate`"; b287, over two senses of one term). b284 reworded the lines that said the plugin's own release as a
value (r77, r78 and r79 retired for r81, r82 and r83: "While the release of this repository is the same as the release
of `migrate`, ..."), so they no longer get a new id when the plugin's release moves on. The line that still waits on
it keeps its plain wording until a reword item retires it: migration-tools r80, of the release 0.34.1 (r62-r64 were
0.33.0's, r65-r68 0.34.0's). It says the release the line is written for, as a value: "While the release of this
repository is `0.33.0`, ...".

### #8: a change of an attribute's value

"set the T of x to v" says that an agent gives an attribute one value; the language has no form for an agent changing
an attribute to any value, or for not changing it ("change the status of an item", "shall not change the status of a
node"): `change` takes a thing, and an attribute is no thing. Lines: universal U13, U14 (b155: U4 "`work` shall commit
every transition and push the commit", U5 "A session shall not write a status"). They say instead what the noun
*transition* (the glossary: one change of a node's status, written by `work`) stands for: "When `work` writes a
transition, `work` shall commit the transition and push the commit of the transition." and "A session shall not
write a transition."

### #15: an adjunct of a verb's frame

A frame names a verb's subject, object and the fixed words before a third thing; the language has no adjunct that
ties a thing to the act ("refuses a command for a reason", "the reason it refuses the command"). Line: universal U12
(b155: U11 "exit with an error naming the reason"). It says instead "If a tool refuses a command, then the tool
shall exit with an error naming a reason and change nothing.": the reason is any reason, and the link from the
reason to the refusal is in the gloss of *reason* only.

### #14: ordered choice

An order of a collection or of a printed every is said (b275, `order-by`, `order-by-every`); a choice by position over
an order is not. A rule that takes the first of a list that meets a condition ("the first of `.venv/bin/python`, `venv/bin/python`
and `$VIRTUAL_ENV/bin/python` that exists, else the interpreter running the script") has no construct: the language
has no "the first K that P" over an order the line gives. Lines: analysis-tools r37-r41 (b154: the Python
interpreter `tools probe` takes when `--python` is not given). Each case is a line of its own, said with existence
("X exists", "X does not exist"): the case of the n-th interpreter says that it exists and that each before it does
not, and r41 says that the second is not printed while the first exists. The order lives only in which cases the
lines spell out; a fifth interpreter would need every line after it rewritten.

### The Given of a "no" box beside the link it is said by

A "no" box of more than one item ("the session has no worktree that holds a file whose version is not `2.0.0`") is
given in a scenario by its link to the thing outside it ("the session s1 has no worktree"), which is more than the
line says and makes its state hold. A line that also gives that thing a K by the same link ("While a session has a
worktree and the session has no worktree that holds a file whose version is not `2.0.0`, ...") would be given two
steps that contradict each other, so `features generate` has no scenario of it ("no Given of no there"); `model
logic` reads it. No line of b152-b159 has the shape (b240 phase 12's sweep). It says instead what the K it gives
meets: "While a session has a worktree and every file in the worktree is `2.0.0`, ...".

### #10: for each X, its Y

"every K" in a response is a box of its own, so a list of them ("print every item, every title of an item and every
batch") prints each K but does not pair a thing with its own Y; "every item with its title" has no form (an "its"
binds to its clause's subject, R8, not to an "every" of a response list). Line: conversation r8 (b159: the names
table, each item beside its title). It says instead each "every" apart, and the pairing is the Implementation's.

### #11: the outcome of the response's own act

A line whose condition is what the response's own act gives ("a test that fails when `model` runs it") has no form:
a condition holds before the trigger, and the request's own things (R11) are what a request makes, not what a test it
runs gives. Line: decision-tiers r17 (b159). It says instead the test's last outcome, an attribute of test ("a test
whose outcome is `failed`"), which the scenario gives before the run.

### #16: liveness

When is the next step (R9); "eventually" has no form (deferred to b127). Line: pr-review r1, kept (a review follows the
publication of a pull request after `work batch brief`, not at the next step). It says instead the next-step
obligation, which the batch session meets by its own steps (skill `building-a-batch`).

### #12: an option set to a value of an attribute

"with the `--x` option set to v" takes a code, or a thing the line says more of; a code that is a declared value of
an attribute (`high-value`, a value of an item's value) is no argument, so a line cannot say that a command sets an
attribute to the value an option gives it. Line: backlog r25 (b158: `work rate` with `--value`, `--urgency` and
`--size`). It says instead the command with its arguments in its code, as one example: "When the person runs `work
rate --value high-value --urgency low-urgency --size small` on an item, `work` shall set the value of the item to
`high-value`, ..."; the rule that each rating is set to the one given is not said.

### #14: up to a number, in rank order

The language has no ordered choice: "the first K in rank order", "up to `batch_size` Ks", "unless what blocks it is
picked earlier in the same pick". Line: batches r22 (b158 r20, `work batch start`'s pick). It says what holds of an
item that nothing blocks, "While an item is `ready` and the item passes the readiness bar and the item has no
dependency on an item whose status is not `delivered`, ... `work` shall pick the item ..."; the bound `batch_size`,
the rank order and an item picked after the item it depends on in the same pick stay in the capability's
Implementation section.

### #16: an answer within a time

"within the last 7 days" compares a moment with the clock; the language has no bound on how long an act takes ("no
answer within the push timeout", `$SHOPSYSTEM_PUSH_TIMEOUT`), which b127 defers. Line: backlog r33 (b158 r37, a remote
that does not answer `work idea`'s push in time). It says instead "While the remote of this repository does not
answer the push of the command, ...", which reads that no answer comes at all; the timeout stays in the capability's
Implementation section.

### #8: an attribute set to the value a command is given, and an attribute left as it was

"set the T of X to `v`" sets a value the line names; the language has no form for the value a command is given as its
argument ("set the line outcome of the request line to the outcome the command gives"), and no negated act on an
attribute ("not change the side of the request": `change` takes a file, and an attribute is no thing). Lines: requests
r63 (b153: `work outcome` writes the line outcome it is given), which says instead the case of one value, the value in
the command's code: "When the person runs `work outcome accepted` on a request line proposed in the request, `work`
shall set the line outcome of the request line to `accepted` ..." (r82 names the command so too); requests r80 and
r96, which say "keep the side of the request" (role-boundaries' keep, an act of the agent, not the absence of a
change), so `spec logic` does not read them as leaving the value as it was.

### #3: one above the highest

"the number of Ks" counts; the language has no aggregate over values: the highest of a set, a sum, one above the
highest. Lines: migration-tools r32 (a ledger entry with no number is numbered from one above the decision ledger's
highest) and r33 (a Behaviour line with no id gets one above the highest id its capability has used or retired), b156.
Each says instead that `migrate` gives the thing a ledger number or a line id; which one is the implementation's.

### #10: each of the Ks

"two Ks" in a trigger are two things, but the language has no "each of the Ks" to say a thing of each in a response:
"the measurement of the batch" after "two batches" names neither (R2), and "every batch" is every batch there is.
Lines: telemetry r8 and batch-measurement r26 (b156), `measure compare` on two batches or two measurements. Each says
instead "two measurements" or "two total rows", which are not tied to the batches or measurements the command names.

### #17: a default value

A value a thing is taken to have when it has none ("a repository with no plugin version file is on `0.23.1`") is no
construct: a release's code is a value, and a value is not a thing a tool prints. Line: migration-tools r38 (b156). It
says instead what the default makes `migrate status` print: every upgrade step, each being pending on `0.23.1`.

### #18: the ratio of two figures

A figure of one measurement divided by the same figure of another is arithmetic, which the language has not. Lines:
telemetry r8 and batch-measurement r26 (b156). Each says "a ratio", a noun of the glossary, glossed as the second's
figure divided by the first's.

### #10: one thing counted for each of another's

"`features count` counts each examples row of a scenario outline as a scenario" pairs each row with a scenario it
counts as; the language has no "for each X, a Y" (distribution, the audit's #10), and "the number of scenarios" counts
only the Ks the line names. Line: feature-file-tools r89 (b157 r46, "count every examples row"). It says instead the
case where the rows are the only scenarios: "While a feature file has a scenario outline and the feature file has no
scenario, ... `features` shall print the number of examples rows of the scenario outline."

### A thing in a thing at any depth

"every feature file under the directory, however deep" is the closure of `in` over directories; the language has no
closure, and a row `feature file | in | subdirectory` is one level. Line: feature-file-tools r91 (b157 r48, where the
depth was in the gloss of "subdirectory"). It says one subdirectory, and the gloss no longer says "at any depth".

### #16: history, moments, and an "or" of a response, in `spec logic` and `features generate`

The constructs `done`, `done-since`, `moment-compare` and `within` of grammar/constructs.md parse and `spec parse
--form` prints their reading, but `spec logic` has no translation of a history or of a comparison of moments, and
`features generate` writes no scenario of a line that uses one; nor of a line that uses `or-list` between the objects
of its response ("shall print a file or a stage"). Until they do, a requirement that uses one of them does not conform
to the language reference: the scenario of feature-file-tools' catalogue line is written of every other "shall" example of the
catalogue (tests/scenarios/feature_file_tools_world.py reads the codes from this section).

### #16: "unchanged since" a moment the line does not name

"S has V-ed O since m" takes a moment m of the line; "the lexicon has not changed since `spec parse` last parsed the
requirement" needs the moment of an earlier run, which no line names. Lines: design-model-check r282, r283, r284
(b239's parse cache and compiled grammar). Each says instead what the cache holds: the parse of a requirement, whose
entry gives the cache's key (the requirement's text, its grammar's sources and its lexicon's words), so "a parse
cache holds the parse of a requirement" is true only while none of them has changed: "While a parse cache holds the
parse of a requirement, when the person runs `spec parse` on the requirement, `model` shall read the parse cache,
write no compiled grammar and exit successfully."

### A `not` over a verb inside a "no" box

"no K that no K2 Vs" and "no K that a K2 does not V" parse, but `spec logic` reads a `not` inside a "no" box only
over an attribute of the box's own referent ("no dependency on an item whose status is not `delivered`"), not over a
verb. Line: design-model-check r251 ("a requirement has no consequence that no premise entails"). It says instead,
with the verb add (a requirement adds a consequence that no premise entails): "While a requirement has a consequence
and the requirement adds no consequence, when the person runs `spec logic`, `model` shall print `L8`."
