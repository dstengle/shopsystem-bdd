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

## R2. "the K" binds to something the line gave, else it is refused

"the K" binds to the latest earlier referent of kind K (or of a kind under K) in the line: one a part introduced, an
actor, a code or an indexical. Else to the image of a relation row `K | of | S` of the one earlier referent of kind S
("the worktree" after "a session" is the worktree of the session). Else, when K's entry has `This:`, to the run's own
K (R11). Else the line is refused, naming the noun: "the" never means the only K in the world. "Earlier" is said
before it in the line: a "the K" that only a later noun phrase gives is refused too.

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
Vs meets the restrictor; the line obliges no V.

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
of such a line gives two Ks, so it is not met vacuously (the generator's part is I14a's).

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

"a K" is at least one K (R1). Counts ("one", "at least", "at most", "exactly") are I15's (call 4); grammar 4 has no
count yet.

Tested on U8 ("... a tool shall print one JSON object": exactly one).

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
