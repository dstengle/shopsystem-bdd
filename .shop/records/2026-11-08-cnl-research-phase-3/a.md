# b112 phase 3, share a: design-model-check, decision-tiers, pr-review, brainstorming

67 lines: design-model-check 47, decision-tiers 9, pr-review 8, brainstorming 3. Rows in `a.tsv` beside this file.
Construct names are phase 2's list (sample-rewrites.md §1.3), plus one new name:

- **COUNT-CMP** (new): a comparison on a count, "more than one", "at least two". COUNT is exactly n; these lines need
  "more than" (design-model-check r5, r11, r57).

## Counts

| Pattern | Lines | | Route | Lines |
|---|---|---|---|---|
| refusal | 38 | | scenario | 58 |
| effect | 26 | | judgement | 8 |
| invariant | 2 | | static-check | 1 |
| liveness | 1 | | check-after-each, monitor | 0 |

The share is almost all next-step effects: design-model-check is one template repeated 47 times ("If the person runs
`model check`/`model parse` on a X that is <adj>, then `model` shall exit with an error naming <code>"). The judgement
lines are pr-review's and brainstorming's: guarantees of an agent's or session's conduct, which no scenario can drive.
pr-review r9 gets static-check because `work batch reviewed` already refuses an ungraded or untriaged finding.

| Construct | Lines | | Construct | Lines |
|---|---|---|---|---|
| SENSE | 22 | | CONFORMS | 7 |
| NEG-EXIST | 22 | | COMPARE | 6 |
| HAS | 19 | | STATE-MOVE | 6 |
| WHOSE-REL | 16 | | COUNT-CMP (new) | 3 |
| RC-OBJ | 15 | | POSS | 3 |
| OF | 12 | | WITH-ARG | 3 |
| RC-SUBJ | 11 | | COUNT | 2 |
| ADJUNCT-PP | 9 | | EXAMPLE-DATA-OUT | 2 |
| NP-LIST | 7 | | ONLY, HISTORY, VP-COORD-NEG | 1 each |

13 candidates need no new construct (8 lines stay as they are). Example data: 2 lines (r68, r69, whose
*definitions* hold the example `viewer subscribes to channel`; no line itself carries any).

**Adjectives:** 47 lines lose a coined adjective (45 distinct words; `untested` and `untiered` appear twice).
One stays: `failing` (decision-tiers r5), a plain-English state of a test whose definition only restates it. Three
removals cost nothing: decision-tiers r2 (`untested`), r3 (`unrequired`) and pr-review r7 (`clean`) parse today
written out, because their definitions were already sentences of the grammar ("enforced by no test", "no review
finding on the pull request is `fix now`"). Status and tier values (`check`, `requirement`, `accepted`,
`superseded`, `fix now`, `delivered`, `judgement`) stay as values.

SENSE leads because design-model-check talks about documents that do things: a scenario *names* a requirement, a
resolution *names* a requirement, an entry *lists* a word, a requirement *uses* a verb, a definition *names* a kind,
a requirement *negates* a verb. Today every one of these verbs has a single frame with an agent as subject. HAS and
NEG-EXIST follow: most violations are "X has no Y" or "X has two/more than one Y".

## Hard lines

- **design-model-check r6 (`repeating`)**: the definition says "the features, condition and trigger of another
  group's statement". "Features" here is neither a feature file (the glossary's sense) nor anything defined; I left
  it out pending its meaning. "Another group" needs identity between groups (COMPARE).
- **r47 (`clingoless`)**: the adjective hides the behaviour itself (`model` tries again under another interpreter),
  and the line states only an output, "0 violations", which also needs a sound context. "An interpreter is
  clingoless" binds no interpreter to `model`. The candidate states the retry.
- **r48 (`unfound`)**: an adjective of one interpreter carrying a fact about all of them ("no interpreter `model`
  tries can"). A quantifier packed into a word.
- **r61 (`relational`)** and its rule v_t12: meta-linguistic (it is about the word `the` inside a definition). The
  rule exists because conditions stand in for relative clauses; the redesign may retire it rather than rewrite it.
- **r1 (`sound`)**: circular. A sound context is one where `model check` finds nothing, so "on a sound context,
  `model check` prints 0 violations" says only the output form.
- **r58, r59, r63**: "the frame of the verb names" an object, a recipient or a kind: the line's subject is a
  requirement but the condition is about a verb's use inside it. "A requirement that uses a verb without the object
  that the frame of the verb names" works but stacks two relative clauses and an of-phrase.

## The meta-level problem

design-model-check's lines are about the spec's own artifacts: a requirement, a term, a verb, a frame, a scenario's
tags, an id. A rewrite needs these as kinds of the vocabulary (verb, frame, requirement bullet, id, glossary entry,
term entry form, frame form, requirement tag, part of speech), and many of the adjectives' definitions are the
*definition of a rule* in `scripts/model.lp`. Each line restates one rule and names its code. Two ways to write them:

1. Write each rule's condition out in the line (the TSV does this): 25 to 40 words a line, mostly of meta-vocabulary.
2. Treat the rule catalogue (`model.lp`'s labels, or `model rules`' output) as a named artifact, like the owner's
   comment schema: "If the person runs `model check` on a capability that violates `v15a`, then `model` shall exit
   with an error naming `v15a`." That is short but circular unless the rule's text lives in an artifact the line
   names. It is CONFORMS turned around (VIOLATES a named rule).

The owner should choose. The second keeps design-model-check readable and puts the rule texts where they already are.

## Words with more than one meaning

| Word | Senses |
|---|---|
| untested | a requirement no scenario names (design-model-check); a design-decision enforced by no test (decision-tiers) |
| uncited | an observation no source names (requests, used in design-model-check r43); a commit citing no item (batches) |
| unparsed | a requirement not parsing in its context's grammar; a request line not parsing in its upstream's (requests) |
| malformed / misformed / unreadable | all "does not conform to a form": term bullet, request, comment; malformed has four senses spec-wide |
| untiered | a decision's frontmatter with no tier (r1); reused in r8 for a command missing `--tier` |
| use | "use the test" = run it (decision-tiers r4); "use `work ready`" / "use `work quote`" = run a command (brainstorming) |
| publish | put a branch up as a pull request (glossary); pr-review r6 uses it for the push of a re-review |
| condition | an adjective entry (glossary); a While clause (r64's `verbal`) |
| enforced by | two relation rows: design-decision to test (index.md), to requirement (decision-tiers) |
| the term | in "naming the term" (r58-r61, r63, r65, r70) with no term in the line: a definite with no antecedent, meaning the verb |

## Other findings

- **Wrong agents**: pr-review r5 and r7 trigger on "`pr-reviewer` writes a review" but `work` sets the status when a
  session runs `work batch reviewed`. pr-review r9 says `pr-reviewer` writes a file; the Implementation says it has
  no Write and the batch session saves the reply. pr-review r1: the batch session dispatches the reviewer, not
  publication. brainstorming r3 says the session writes a quote; conversation r1 says `work` writes it.
- **States missing from the line, present in the group title**: design-model-check r44 ("a context with no job") and
  r52 ("a current index"). As written, r52 holds only because the If lines r51 and decision-tiers r5 take
  precedence.
- **Two rules in one line**: design-model-check r36 (id form or no Behaviour), pr-review r3 (a first review's
  reading, plus the invariant "read only the batch's commits").
- **Entailed lines**: decision-tiers r8 is r9 with `--tier` as the absent argument. design-model-check r56's
  "commit the record" is U4 if a record is a transition.
- **Incomplete**: decision-tiers r7 commits only the decision, but `work decision` commits the index too.
- **Dead vocabulary**: r19's `job-thread` and r11's `@deprecated` exception name 1.x things the upgrades removed.
- **One option written two ways**: "Where `--check` is given" plus `model decisions` (design-model-check r51, r52)
  against `model decisions --check` as the command (decision-tiers r4, r5).
- **A property of the command written as one of a thing**: decision-tiers r9 (`absent` argument "on" which the
  command runs), design-model-check r57 (`unattributed` record, which does not exist yet). Both become WITH-ARG.
- **pr-review r2** is a negative effect on one trigger (a task becomes `done`) standing for an invariant: the
  reviewer reviews only pull requests.

## What the candidate form cannot say yet

- An attribute with no value ("has no tier", decision-tiers r1): values are enumerated and absence is not one.
- Counts beyond exactly-n (COUNT-CMP), and "two" read as "at least two" (r23) rather than "exactly two".
- "no X or no Y" and "no X and no Y" as coordinated negated objects or subjects (r40, r43) need a written reading
  rule.
- Thin responses ("exit successfully" on r62, r64, r66, r68, r69) say nothing of what parsing produced. The rewrite
  cannot add what the line never said.
- The meta-level rules (above) need either a large meta-vocabulary or a rule catalogue named as an artifact.
