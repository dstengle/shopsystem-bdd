# b112 phase 3, share c: analysis-tools, feature-file-tools, trials, universal

63 lines: analysis-tools 33, feature-file-tools 20, trials 5, universal 5. Per-line results are in `c.tsv` beside this
file. Candidates were written by hand and not run through `model parse`. Phase 2 already wrote f3, f14, t2, t4, U4, U7
and U11; I kept its candidates and added an OF to U4 ("push the commit of the transition").

## Counts

**Pattern**

| Pattern | Lines | Where |
|---|---|---|
| effect | 45 | analysis 27, features 15, trials 3 |
| refusal | 12 | analysis 6, features 5, U11 |
| invariant | 4 | trials r2, r3; U5, U7 |
| transition | 2 | U4, U8 |
| precedence, bounded, liveness | 0 | |

Five of the 12 refusals are written as When lines today: analysis r12, r30 and r31, plus the two missing-tool lines
classed as effect (r8, r29). Five If-line "refusals" are really check findings: features r13, r15, r18 and r19, and
analysis r28 (classed as effect). Exit code 1 means "a check failed or something was refused" (see the words section).

**Route:** scenario 53, judgement 7, check-after-each 3 (U4, U8, U11). Trials is a guarantees capability run by an LLM
agent, so all 5 of its lines go to judgement, with U5 and U7. U5 and trials r3 could become monitors.

**Example data:** 42 of 63 lines carry example data (paths, function names, output literals, versions). In
feature-file-tools that is 19 of 20 lines; in analysis-tools 23 of 33. The pattern is the one phase 1 found: in about
half of these lines the rule is stated only by the example data, and the line itself is thin (see below).

**Constructs, by number of lines that need each**

| Construct | Lines | | Construct | Lines |
|---|---|---|---|---|
| EXAMPLE-DATA-OUT | 40 | | STATE-MOVE | 7 |
| OF | 27 | | ADJUNCT-PP | 7 |
| WITH-ARG | 18 | | WHOSE-REL | 7 |
| HAS | 15 | | POSS | 6 |
| EXISTS (new) | 14 | | COUNT | 5 |
| NEG-EXIST | 12 | | NP-LIST | 4 |
| RC-OBJ | 11 | | OR-NP (new), VP-COORD-NEG, COMPARE, ONLY | 3 each |
| RC-SUBJ | 11 | | HISTORY, REL-COPULA, TRIGGER-AS-ACTION | 1 each |
| SENSE | 11 | | CONFORMS, NEVER/ALWAYS, MAY, ONLY-AFTER | 0 |

Two new construct names:

- **EXISTS**: an existence predicate, "X exists" / "X does not exist" ("While the Python interpreter
  `.venv/bin/python` exists"; "While no coverage map exists"). It replaces *present* in all of its senses. HISTORY
  ("`tools map` has written a coverage map") would say the coverage-map sense more exactly. EXISTS is shorter and
  enough for every line here.
- **OR-NP**: "or" between noun phrases or between relative clauses ("neither `.venv/bin/python` nor
  `venv/bin/python`", "every scenario that has the tag or whose feature file has the tag"). universal.md's own note on
  U7 already asks for this ("Carried forward to R14").

WITH-ARG is the third most common construct only because I replaced every "Where `--json` is given" / "Where
`--check` is given" with "with `--json`". EARS's Where is for an optional *feature*, not a command option (r1, r16,
r26, f7, f11, f16, f18, U8). If the redesign keeps Where for options, take 7 off that count.

Only 5 lines stay as they are (`=`): analysis r7 and r8, trials r1, U5, U7. Five lines need no construct.

**Adjectives:** 12 coined adjectives are removed, across 25 lines:

- *present*: 14 lines. It has two senses in this share (an interpreter's file exists; `tools map` has written the map)
  and a third in batch-measurement.
- *nested*: 2 lines.
- *outlined, sectioned, deprecating, undeprecated, resolving, dangling, sweeping, partial, withholding*: 1 line each.

Kept, with why:

- *missing, uninstallable*: values of the attribute *presence*.
- *virtualenv, system*: values of the attribute *environment*. They are written as if they were adjectives of the
  interpreter and need OF ("the environment of the Python interpreter is `virtualenv`").
- *failing*: plain English.
- *codified*: a domain term, though defined twice (capability, change list).

All nine feature-file-tools adjectives disappear. They are pure test-fixture descriptions: each names one feature file
or test module shape used by one line.

## Hard lines

- **analysis r2-r6** are one rule: a first-match order over five interpreters. They are spread over five lines whose
  While clauses spell out every negated predecessor, and r6's positive half is entailed by r2. The candidate form has
  no "the first of these that exists", so the rewrite keeps five lines. r4 also forgets r1: with `--python` given and
  only `$VIRTUAL_ENV` present, r1 and r4 both apply and name different interpreters.
- **analysis r18**: "for each file, the number of its tests that executed the function" is a distribution the form
  cannot say. The candidate repeats the relative clause.
- **analysis r21**: "a function its file does not have" refers to something that does not exist. The candidate
  refuses a *name* that no function of the file has.
- **analysis r10**: "install ... and change nothing" is false as written. The rule means no dependency file, which
  only the given block tests.
- **analysis r11**: `ruff==0.17.0` is a string in install's analysis-tool slot, and it changes with every release. The
  rule is "the version the plugin pins".
- **features r4**: "however deep" is transitive containment, and the form has no closure.
- **features r18**: "differs from what `features generate` would write" is counterfactual, and the form has no
  "would".
- **features r2**: "one scenario per Examples row" is a counting rule that today lives only in the example data.
- **Thin lines.** Several lines state nothing of their rule, which only their group title and given block carry:
  - "print every test" (r17, r20) means the whole suite as written;
  - r33 never mentions 300;
  - f1 says only "print the number of scenarios";
  - f19 names the feature but not the step;
  - f17 says print where the group says write;
  - trials r5 does not say where the measurement is named.

  These are rewrites of content, not only of form.
- **features r15/r16 clash** under universal.md's If-precedence rule. r15 is an If line on the same command string as
  r16, with an overlapping state, so wherever r15 holds, r16 does not apply. Only the shared given block makes them
  agree. Either r16 becomes an If line, or r15 says what `--json` adds.
- **features r15**: *partial* is put on the test module, but the fault is a scenario that no module binds. The
  adjective sits on the wrong kind.

## Words with more than one meaning

- **present**: an interpreter's file exists; the coverage map has been written; a measurement is already written.
- **exit with an error**: "refused, changed nothing" (U11) versus "something was found" (analysis r28 and r32;
  features r13, r15, r18, r19). The If + "change nothing" form is used for check findings that refuse nothing.
- **Where**: an EARS optional feature, used here for command options.
- **name** (verb): its gloss says "a message or a file names a thing", but its frame is `agent names thing`. trials r4
  needs the gloss and r5 uses the frame.
- **feature / feature file**: one generated file under two nouns (f17-f20 against f1-f16).
- **tag**: a glossary verb (`session tags scenario`), used as a noun in f1, f3, f5, f9 to f11, with no noun entry.
- **the number of tests**: all tests run (r16) versus the tests that executed the target (r17).
- **worker / worktree** (U7): glossed as `work run`'s, a retired workflow, while the line is kept for a batch's task
  subagent. U5's note also still speaks of `work run`.
- **replace** (r14): used when there may be nothing to replace.

## What the candidate form cannot say

1. **An ordered choice or a default**: first match, "300 when none is given" (r2-r6, r33).
2. **Distribution**: "for each X, its Y" (r18; f2's "one per row").
3. **Transitive containment**: "however deep" (f4).
4. **A counterfactual**: "what generate would write" (f18).
5. **Output layout**: one line, under its tool's heading, `== ruff ==`, "Probe: tools ->" (r9, r28). These belong in a
   named format artifact (CONFORMS), as the owner proposed for schemas. No line here needed CONFORMS for an input.
6. **A reference to a non-existent thing** (r21). Lines must refuse a name, not a thing.
7. **Meta-vocabulary about the grammar itself**: f20's "a requirement whose response is a negated verb with a
   recipient". This is sayable with WHOSE-REL, but only if response, negated verb and recipient become nouns of the
   frame model.

The share needs nothing of time or modality: no precedence, bounded or liveness line, and no MAY. As in phase 2, the
gap is noun phrases (OF, HAS, relative clauses, NEG-EXIST, EXISTS), command arguments (WITH-ARG) and moving example
data out.
