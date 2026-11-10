---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-10-grammar-4-audit
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-10
---

# Grammar 4 against every line: what it cannot say yet

## 1. What was audited and how

The audit asks one question of every grammar-4 line written so far: does the line say what the old line meant, in
grammar 4's own structures? It was run after several reword items needed workarounds. Its purpose is to decide what
grammar 4 must still learn before plugin 4.0 (b112) is released.

**Sources.** Eight audits, one for each reword item:

| Item | Capabilities | Lines |
|---|---|---|
| b152 | design-model-check, and the gap items' lines in feature-file-tools, readiness and batches (b197, b215-b222, b234-b239) | 149 |
| b153 | requests | 44 |
| b154 | analysis-tools, trials | 40 |
| b155 | `spec/universal.md` | 5 |
| b156 | migration-tools, telemetry, batch-measurement | 39 |
| b157 | feature-file-tools, readiness | 62 |
| b158 | backlog, batches | 40 |
| b159 | decision-tiers, pr-review, intake, conversation, brainstorming | 31 |
| **Total** | | **410** |

**Method.** Each audit laid its item's lines over a scratch copy of `spec/` (`backlog_lines.lay` or `lay_onto`). It
then ran `model parse --form` on every line and read the logical form against the old line and the item's glossary.
Where a construct looked missing, the audit parsed alternative wordings to check whether the grammar really lacks it
or the writer only avoided it. In all, about 60 alternatives were parsed. Nothing in the repository was changed. The
per-line rows are in each audit's `audit.tsv` and the reasoning in its `audit.md`, under
`scratchpad/b112/audit/b15x/`.

Every line parses, and each parses to one logical form. The failures are all of meaning, not of parsing.

**Verdicts.**

| Verdict | Meaning |
|---|---|
| fine | The form says what the old line meant. |
| distortion | The line parses, but its form means something else: narrower, wider, a dropped condition, a changed response. |
| unsayable | The meaning cannot be written in grammar 4 at all, and the line was left weaker. |
| coined | The line parses only because a new noun, verb or proper noun hides the structure in its gloss. This is the anti-goal "meaning hides in the glossary" (design section 2). |

## 2. The counts

| Capability | Lines | Fine | Distortion | Unsayable | Coined |
|---|---|---|---|---|---|
| design-model-check | 115 | 47 | 44 | 3 | 21 |
| feature-file-tools | 67 | 7 | 9 | 0 | 51 |
| requests | 44 | 18 | 16 | 0 | 10 |
| analysis-tools | 35 | 8 | 23 | 2 | 2 |
| migration-tools | 30 | 3 | 23 | 1 | 3 |
| readiness | 27 | 12 | 8 | 0 | 7 |
| backlog | 21 | 14 | 4 | 3 | 0 |
| batches | 21 | 15 | 5 | 1 | 0 |
| decision-tiers | 11 | 5 | 4 | 0 | 2 |
| pr-review | 9 | 8 | 0 | 1 | 0 |
| trials | 5 | 3 | 2 | 0 | 0 |
| universal | 5 | 1 | 2 | 0 | 2 |
| batch-measurement | 5 | 0 | 5 | 0 | 0 |
| telemetry | 4 | 1 | 2 | 0 | 1 |
| conversation | 4 | 2 | 1 | 1 | 0 |
| intake | 4 | 0 | 4 | 0 | 0 |
| brainstorming | 3 | 2 | 1 | 0 | 0 |
| **Total** | **410** | **146 (36%)** | **153 (37%)** | **12 (3%)** | **99 (24%)** |

Fewer than two lines in five are fine. Most of the rest fall into two groups:

- **Meta-level lines** (design-model-check, feature-file-tools) are mostly coined. They talk about the language's own
  sentences, and grammar 4 has no way to name a construct.
- **Lines about files, versions and counts** (analysis-tools, migration-tools, batch-measurement) are mostly
  distorted. They need existence, ordered values and "the number of".

The plain workflow capabilities (backlog, batches, pr-review) are mostly fine. The grammar works for what it was
designed around: actions, relations, "of", "no", relative clauses and short refusals.

## 3. The missing constructs

Line counts are summed across the audits. A line can need more than one construct, so the column does not add up to
the distorted, unsayable and coined total. "Planned" refers to the design `.shop/records/2026-11-09-cnl-4/design.md`.
The sizes are rough: S is under a day of grammar and logic work, M is one item, and L is several items or a design call.

| # | Construct | What it is | Lines | Before (old meaning) / after (grammar-4 line) | Planned? | Size |
|---|---|---|---|---|---|---|
| 1 | Mention of a construct | A line names a sentence construct of the language ("a requirement whose precondition has a universal") as a thing, not as a coined adjective or noun. | ~90 (rule codes 24, gap-item adjectives 26, meta nouns 16 + 25) | b236 "reframing", b237 "refraining"; r271 "boxed noun phrase" / no plain form | No. Only rule codes, through b123's catalogue | L |
| 2 | Identity and distinctness | "the same trigger and state", "another K", "two other Ks", "the earlier K" | 20 | "two lines of one trigger and state clash" / r276-r278 link only through a shared act, so any two lines on one act need L1 | No. Call 9 covers only comparison with constants | M |
| 3 | The number of | A count as a value ("the number of tests that execute f"), and comparisons of counts | 20 (count nouns 14, aggregates 4, count comparison 2) | analysis r50 "the test count of the function" | Partly. Call 4 has "at least n Ks", not "the number of" as a value | M |
| 4 | Value sets and attribute absence | "is one of A, B, C", "is not A, B or C", "has no tier", "every line is settled" | 20 | decision-tiers r13 "untiered" / three "is not" clauses, which also match a tier outside the three | Partly. VALUE-SET in phase 3; call 13 defined conditions | S-M |
| 5 | Conformance to an artifact | `conforms(x, artifact)`: a comment, path or file matches a named schema or form | 17 | requests r77 "does not conform to the comment schema" does not parse / "has no field block" | Yes. Section 6.2's own example and 7.2's atom, but not built | M |
| 6 | Ordered comparison | Release or version "before" or "after" a constant | 16 | migration-tools r55 "lacks the verb-frames step and does not lack the simplified-workflow step" | Yes. Section 6.2, call 9 | S-M |
| 7 | Existence | "X exists", "has been written" | 14 | analysis r37 "this file system holds the dot-venv interpreter" | No. EXISTS was 14 lines in phase 3 | S |
| 8 | Attribute change and negated state | "change the status of a node", "not change the status", "fails" | 13 | U14 "shall not write a transition"; r203 "lacks", r205 "omits" | No | M |
| 9 | Quantifiers inside clauses | "every" in a condition's object, "every/no" in a response's relative clause, "or" between relative clauses, a negated restriction | 13 | requests r88 "rejects a commit" for every commit; analysis r56 prints one function, not every untested one | Partly. Call 4 and R6; the bar and generator refuse some forms that parse | M |
| 10 | Distribution "for each X its Y" | Pairing in a list ("every item with its title"), plural triggers ("on two batches") | 10 | telemetry r8 "on batches" reads as one batch; conversation r8 loses item-title pairing | Partly. Call 4 "each of the Ks" | M |
| 11 | The run's own thing | The interpreter in use, the push this command makes, the commit it just made, the outcome of its own act | 9 | analysis r43 "the dot-venv interpreter" makes the example the rule | Yes. Call 6 (`This:`); several lines need only an entry | S |
| 12 | Option with its argument | "runs `work request` with `--raised-for` on a request"; a required option not given | 8 | requests r59 glues the option into the command code | Yes. Goal 5, section 6.2; partly built | S |
| 13 | Counterfactual | "is not what `model decisions` would write" | 8 | r202, r203, r220 now catch missing entries only | No | M (or route through #5) |
| 14 | Ordered choice | First match in a list; "up to `batch_size` in rank order" | 6 | analysis r37-r41: four proper nouns, each line spelling out the earlier negations | No | M |
| 15 | Frame adjuncts | "refuses a command for a reason", "remove X from Y", a second object | 5 | U12 "naming a reason" reads as a new, unrelated reason | No. ADJUNCT-PP was 24 lines in phase 3 | M |
| 16 | Time beyond history | "unchanged since", "within the push timeout", liveness | 5 | b239 "outdated", "uncached"; backlog r37 drops the timeout | History yes (4.4). Bounded time and liveness deferred to b127 | M / deferred |
| 17 | Default value | "300 lines when `--limit` gives none" | 3 | analysis r65 "the default size limit" | No | S |
| 18 | Small singletons | Output layout (2), reported content (1), ratio (2), reflexive (1), necessity (1) | 7 | batch-measurement r26 "a ratio" | Necessity yes (4.5), the rest no | - |

The audits also found faults that are not missing constructs:

- **R2 accessibility is not enforced.** The lines design-model-check r231, backlog r6 and batches r4 parse
  to forms with a variable outside its box (`the item` and `the task` outside the `every` box). R2 should refuse them.
  The cases of an "or" are not treated as boxes.
- **R1 makes new referents where an old one is meant.** requests r63 "assign the line outcome of a request line" and
  r199 "use an interpreter".
- **The generator and the bar lag the grammar.** "every function of the Python file that no test executes" parses
  but the readiness bar refuses it. "not close the issue of the request" parses but `features generate` has no Then
  for it.

## 4. The coined words

The 99 coined lines repeat the pattern the anti-goal names: a word whose gloss carries the structure the line should
show. They come in four kinds.

| Kind | Examples | What the gloss hides |
|---|---|---|
| Meta-level adjectives (gap items' fixtures) | distributing, reframing, refraining, screening (b197, b236-b238) | Another line's construct: "a capability with a line whose response is plural", a frame change, a negated response |
| Meta-level nouns (rewordings) | boxed noun phrase, negated modifier, unification failure, later sense, outer definite, codified-2 marker | A construct of the logical form, a solver outcome, a file marker that is really an attribute value |
| Domain nouns hiding a relation or condition | field block, block, host, origin, transition, figure, scenario count, index entry, route list | Conformance; "every line settled"; a github entry; an attribute change; a list of four figures; "the number of"; a counterfactual |
| Verbs and proper nouns hiding conditions | verify, pick, differ, count, subdirectory; "the design model", "the capability id form" | An in-force status plus a relation; a status change; a counterfactual; distribution; transitive closure; a schema |

The domain nouns go away once constructs #3-#13 exist. The meta-level words are the hard case. design-model-check,
feature-file-tools and readiness test the language itself, so their lines must name sentence structures. Today they do
so through 66 or more words the person never chose.

**How the language could talk about its own structure.** The rule catalogue (b123, `grammar/rules.md`) already shows
the way for rules: a generated artifact gives each rule a code and a label, and a line names the rule by its code
("While a capability violates `v15a`"). The same move applies to constructs:

- **A construct catalogue** (`grammar/constructs.md`), generated from the grammar, with one entry per construct of the
  logical form: its code, a plain-English label, and the form's atom it matches (`every` box, negated modifier,
  `Def` condition, plural response, frame role, and so on).
- **One frame over it**: "a requirement uses a construct", and "a construct of a requirement is `c_every`". With
  "of", "whose" and "no", this covers "a requirement whose precondition uses `c_every`" and "a capability with no
  requirement that uses `c_plural`".
- **The fixtures stop being adjectives.** b236's "reframing" becomes "a requirement that uses `c_frame_change`". The
  test reads the line's form, so the code and the grammar cannot drift apart.

This is level 2 of the rule catalogue in another shape, and the design names it a non-goal (b124). The audit is the
evidence for reopening that non-goal: about 90 lines rest on it, more than on any other construct. Codes alone are
not enough. The 12 identity lines (#2) are meta-level too ("two requirements of one trigger and state"), and they
need #2 even with a catalogue.

## 5. Distortions a rewording alone fixes

Each of these was checked by parsing the alternative. None needs a grammar change. Some need a glossary entry, a
`This:` or a relation row.

| Capability | Lines | The fix |
|---|---|---|
| design-model-check | r207, r214 | "a term has no frame" |
| design-model-check | r230, r251 | "does not agree"; "no premise entails the consequence". spec_facts and spec_steps forced these verbs, not the grammar. |
| design-model-check | r192, r194 | a section kind with "or" |
| design-model-check | r174 | restore "0 violations" |
| design-model-check | ~10 rule-code lines | written out, if the person reopens the catalogue choice for them |
| requests | r61, r102, r97-r101 | "with `--source` and `--thread`", "with `--forward`" in place of glued flags |
| requests | r76 | "does not hold the comment" |
| requests | r81 | restore the dropped conjunct "a request line ... is `refused`" |
| requests | r84 | r79's three-negation form |
| requests | r99 | state the real waiting condition |
| requests | r89, r90 | "not close the issue of the request" (parses; the generator needs a Then) |
| analysis-tools | r26 | a `tools refs --json` line |
| analysis-tools | r43-r46, r66 | `This:` on Python interpreter |
| analysis-tools | r44, r54 | a plain verb "pin"; refuse a name |
| trials | r7, r8 | no-trigger "only" invariants |
| universal | U15, U16 | re-gloss worktree, add rows (worktree of session, command of tool), narrow U15 to a task's dispatch |
| migration-tools | r34, r35 | "uncommitted change" |
| migration-tools | r48, r52 | "of this repository"; "whose asker is not this bounded context" |
| telemetry | r5 | list the four figures as attributes |
| telemetry, batch-measurement | r8, r26 | "two batches ... each of the batches" |
| feature-file-tools | r55, r60, r49 | an "every" While clause; restore "codified"; split r49 in two |
| readiness | r33, r29, r37 | "does not meet"; relate the id to a live requirement |
| readiness, feature-file-tools | r31, r35, r65, r66-r87 (marker) | a `language` attribute entry with values, in place of "codified-2 marker" |
| backlog | r27, r36 | "one JSON object" with the `--json` option; bind the remote to this repository |
| batches | r20, r30, r9 | make the in-batch Then explicit and trim pick's gloss; a "from" frame for remove and "of" for propose; merge's gloss |
| decision-tiers | r19, r23 | `This:` on decisions index; route as an attribute with `Values:` |
| intake | r11, r12 | a verb "counter"; the reason of the line, not the CLI pack's reason |
| conversation | r6 | git directory and transcript named |
| brainstorming | r5 | a frame for the quoted words |

That is about 60 lines, roughly 40% of the distortions. Rewording these lines does not depend on any grammar work, so
it can start now.

## 6. Recommendation

### Build before 4.0

The criterion: the construct is needed by many lines in more than one capability (the design's growth rule), or its
absence silently changes a line's meaning.

| Order | Construct (section 3) | Lines | Why before 4.0 |
|---|---|---|---|
| 1 | Fix R2 accessibility and "or" boxes | 3 known | A parser fault. Lines that should be refused are accepted. |
| 2 | #5 conformance | 17 | Planned and shown in the design's own example; three capabilities |
| 3 | #6 ordered comparison | 16 | Planned (call 9); the "lack" workaround inverts the meaning of 16 lines |
| 4 | #4 value sets and attribute absence | 20 | Five capabilities; today's workaround widens the meaning (decision-tiers r13) |
| 5 | #3 the number of | 20 | Five capabilities; extends call 4's counts to a value |
| 6 | #2 identity and distinctness | 20 | The worst distortions: L1 lines that now fire for any two lines on one act |
| 7 | #7 existence | 14 | Small; analysis-tools and migration-tools rest on it |
| 8 | #12 option with argument, #11 the run's own thing | 17 | Planned and partly built; mostly glossary and `This:` |
| 9 | #1 construct catalogue | ~90 | The largest. A design call is needed first: it reopens b124's non-goal. |

Also, the readiness bar and `features generate` should accept every form that parses: an "every" in a response's
relative clause, and a negated response over a relation's image.

Item 9 is the release question. Without it, design-model-check and feature-file-tools keep about 60 coined
meta-level words, and 4.0 ships with its own anti-goal in its own spec. If it is not built, that must be stated in
the release as a known limit, with the coined words listed.

### Accept as known limits for 4.0, and document

Write these in `grammar/language.md` under "what the language cannot say yet", each with its lines:

- #13 counterfactual (8 lines). Where the "would write" is the output of a generator, #5 can carry it as "does not
  conform to what `X` writes"; the rest is a limit.
- #14 ordered choice (6), #17 default value (3), #15 frame adjuncts (5).
- #16 bounded time and liveness: already deferred to b127.
- #8 attribute change (13): consider it for 4.1. Some lines are fixable with a frame of "change" over attributes.
- #9 and #10, the parts that are not plain "every" or "each of" (13 and 10).
- #18, the singletons. Each is under two lines, so the growth rule forbids a construct for it.

### batch-33 (b152-b154, building)

Do not merge batch-33's lines as they stand. b152 alone has 44 distortions and 3 unsayable lines. Among them are the
L1 lines that change meaning (r248, r253, r276-r278), and a merged distortion keeps its id while meaning something
else, which is an anti-goal. Each fix after the merge would cost a second set of retired ids.

- Stop the batch before `work batch review`. Abandon it (`work batch abandon`) once its handler code is saved on a
  branch, so the items return to `ready` and their lines can be reshaped.
- Re-line b152-b154 after constructs 1-8 are built. Apply the section-5 rewordings at the same time.
- If the person wants b153 (18 fine, mostly mechanical fixes) delivered sooner, it can be reshaped with its section-5
  fixes alone. Its conformance lines (8) wait for #5.

### The remaining reword items

- **b155-b159 (shaped).** Do not make them ready. Apply the section-5 rewordings now, then re-line the rest after the
  constructs they need. b158 (27 fine of 40) and b159 (17 of 31) are closest; b156 and b157 depend most on
  constructs #1, #3 and #6.
- **The gap items b234 and b236-b238 (ready).** Their lines are coined meta-level adjectives. Hold them until the
  construct-catalogue call is made, or deliver them knowing their lines will be retired once more.
- **b239 (ready, high urgency).** Its three coined words (reparsed, outdated, uncached) hide "unchanged since". The
  cache is worth delivering. Accept the coined words as a known limit and name it in the item.

Each construct to build, the construct-catalogue design call and the `language.md` known-limits section should become
backlog items (`work idea`) in the same session that accepts this record.
