# Plugin 4.0: the controlled language rebuilt on sentence structure (b112)

This is the design of plugin 4.0.0, the outcome of b112 ("Review the controlled language's grammar: sentence
structures over coined adjectives, balancing parsing, clarity and verbosity"). It rests on four research records and
the brainstorming of 2026-11-08 and 2026-11-09, whose settled points are in b112's `## Notes`:

- `.shop/records/2026-11-08-cnl-research-phase-1.md`: the field, and this language end to end.
- `.shop/records/2026-11-08-cnl-research-phase-2.md`: 27 lines rewritten, their meaning, and a prototype grammar
  over GF's Resource Grammar Library (RGL).
- `.shop/records/2026-11-08-cnl-research-phase-3.md`: all 265 lines and 170 adjectives sorted, with a candidate
  rewrite of every line (`a.tsv` to `d.tsv` in its folder).
- `.shop/records/2026-11-09-model-logic-at-scale.md`: performance is not a constraint; the clingo rewrite
  (`check_fast.lp`) and the entailed-Then check (`comp.py`).

Supporting files beside this design, in this folder: `entailment/` (the study's `comp.py`, `cex.py`, `common.py`,
`gen.py` and the k = 1 results, saved as `.txt` from the session's scratchpad so they survive it and stay out of the
300-line rule), and `prototype/` (the prototype's generator `gen.py` and `parse.py`, the same; its grammar files are
in phase 2's folder, `prototype/Proto.gf` and `ProtoEng.gf`).

Sections 4 and 5 keep apart what the person decided and what this session decided while the person was offline.
Each call in section 5 gives its evidence, so a reader can reverse it without redoing the research.

## 1. Why

The person, 2026-11-08, on b107's r73:

> "We should review the underlying grammar of the CNL and make sure it is constructed in ways that balance parsing
> easily and reading/writing clarity vs verbosity (or other factors)."

> "A grammar is sentence structure combined with terms. We should not be defining simple english terms with domain
> specific meaning."

> "Do we have a set of base grammar that allows statements to be made using a restricted set of linguistic
> structures that yields unambiguous statements about the relationships between subjects and objects."

What prompted it. A condition (`While C`) can only be built from a noun and an adjective term, a relation row, a verb
clause or a held resource. Anything else becomes a coined one-word adjective with a prose definition: 145 of 170
condition entries are prose. feed's `quiet` was coined only because the grammar has no relative clause, and its
definition ("no video is from a channel that the viewer subscribes to") does not say which videos. `listless` is
defined by a sentence that would parse as a requirement's condition itself. `idle` (migration-tools r19) does not
tell a reader how a repository is idle.

The person's direction:

- Common English words keep their English meaning.
- A small fixed set of general adjectives (empty, given, defined) may be universal.
- The structures carry the meaning: subject-verb-object frames, relative clauses, "whose", quantifier scope. The
  glossary does not.

The research names the problem **poor habitability**: writers cannot say what they need, so they work around it. The
coined adjective is the escape hatch that 2.x's "no escape hatch" rule pushed into the lexicon (phase 1, "Why it is
where it is"). Phase 3 measured it: 137 of 265 lines lose a coined adjective once the noun phrase is rich enough; 66
of 170 adjectives are dead; the missing constructs are mostly in the noun phrase ("of" in 77 lines, "no X" in 53,
"has" in 49, relative clauses in 67, "whose" in 30).

A second reason is meaning. Today a line means something only through `grammar/check.lp`'s pairwise clash search.
There is no formula with truth conditions, so "is this Then already entailed?" has no basis, and the Gherkin
generator and the check read `every`, `only` and negated objects differently (phase 1, weakness 1; b114, b116).

## 2. Goals, non-goals, anti-goals

### Goals

1. **Structure, not vocabulary.** A base grammar, free of any domain, gives the sentence structures: clauses from
   verb frames, noun phrases with "of", "its", "whose", "no", relative clauses on any frame, lists, "only", counts,
   comparisons, time words and three modalities. A line that needs a state says it with these structures.
2. **Layers of vocabulary.** The base grammar, then importable term packs (CLI, time) that bring words with their
   logical meaning, then the product's terms, then the bounded context's terms. A word means one thing in a context.
3. **One meaning, written down.** Every line has one logical form (section 7). The clash check, the Gherkin
   generator and the entailment check all read it. The reading rules are written in a language reference, each
   tested against real lines.
4. **Entailment used.** A consequence the spec entails (U11 after a refusal) is found, shown to readers by
   `model explain`, guaranteed by one code path, tested once and left out of each scenario.
5. **Short lines where the logic allows.** Refusals say "shall refuse the command and name X"; command options are
   arguments in the trigger; example data lives in given blocks.
6. **Time and modality, first version.** Time as domain data, time as a trigger (a clock), the order of domain
   events; obligation, necessity and permission.
7. **Every consumer upgrades** through one `migrate upgrade` step that reports what to reword and rewords nothing.
8. **This repository's spec reworded** to the new language, with b118's faults fixed on the way.

### Non-goals

- **Operational timing** ("within N", "always" as a temporal operator, "eventually") and runtime monitors: deferred
  to b127.
- **Level 2 of the rule catalogue** (rule labels written in the controlled language, a spec-vocabulary pack): b124,
  after this release.
- **An HTTP pack.** The pack mechanism allows it; no line here needs it. A consumer asks for it by a request.
- **Reading another repository's packs** (an upstream's or the product's) at check time. A context keeps a copy.
- **Predictive authoring** (GF's completion offering next words in an editor). 4.0 uses completion only in refusal
  hints.
- **Word choice.** The grammar can make a verb name what it takes, not choose the verb (as in 3.0).
- **Speed work beyond b119's rewrite.** Bins, a per-pair cache, Soufflé: later, when a spec reaches about 10,000
  lines (the scale record, section 4).

### Anti-goals: it fails even if it works when

- **Coined adjectives come back under another name**: a defined condition, a "named state", an attribute whose only
  values are yes and no, or a pack word with a narrow meaning standing in for a structure the base grammar has.
  The test: a condition entry whose definition is itself a sentence of the base grammar should be that sentence in
  the line (`model check` warns, section 5, call 13).
- **Meaning hides in the glossary**: a gloss that adds a role, a scope or a condition the frame does not show. A
  frame says who does what to what; the gloss only explains.
- **A passive with no agent** parses, or any clause loses the agent its frame has (3.0 call 3 stands).
- **Gherkin and the logic disagree** on any construct: one logical form, two readers.
- **A line parses to two meanings** and one is picked silently.
- **A common English word is given a domain meaning** without `Redefines:` on its entry.
- **The rewording hides a change of behaviour**: a reworded line that means something else keeps its old id.
- **The language grows by special cases**: a core construct added for one line. A new construct recurs in two
  capabilities or in a pack (2.x's growth rule, kept for the base grammar).

## 3. Constraints

| Constraint | What it means here |
|---|---|
| GF 3.12 and clingo stay | The grammar is GF; the logic is clingo. |
| New dependencies where justified | The RGL (gf-rgl, pinned release `20250812`, the one phase 1 and 2 compiled against), installed and probed by `tools install` / `tools probe`. Z3 is allowed only beside clingo, for ordered values and counts, if needed: this design does not need it (call 9). |
| 300-line files | Every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`). New modules are split by concern from the start. |
| `features generate` byte-stable | Same spec in, same bytes out, before and after every item. |
| `migrate upgrade` step | One step, "the controlled language 4", that rewrites only what is mechanical and reports every line to reword; it rewords no requirement (as 3.0's "verb frames" did). |
| Requirements never edited in place | A line whose text changes gets a new id; the old id goes to `retired:`; its scenario is regenerated (design-decision/requirements-retired-never-edited). |
| Requests only propose | Lines accepted from a request are written in this context's terms. |
| One fresh agent per plan or batch | The work is cut into items sized for one batch task (section 10). |
| Performance is not a constraint | b119's studies: the rewrite runs 0.8 s at 5k lines and about 3 s at 10k; the entailment check about 5 s at 5k (mixed). |

## 4. What the person decided

As written in b112's notes, grouped. These are settled.

### 4.1 Requirements and their routes (2026-11-08)

- **Definitions** (types, "is a", relations) are timeless vocabulary.
- **Requirements** are effect rules, structural rules, state invariants, transition rules and liveness. Each is a
  premise of the logic with its own verification route: scenarios, a check, judgement through a design-decision, or
  runtime monitors by sampling.
- **Only ubiquitous lines need a route**, and the route is carried by a design-decision (a `verified_by` beside
  `enforced_by`), never inside the sentence.
- **A coined adjective is a state missing its structure.** requests r33's `unreadable` becomes "a request comment
  does not conform to the comment schema".
- **Formats live in external artifacts** (a schema) that a line names and conforms to, read in as facts where a line
  needs their fields.

### 4.2 Layers, packs, words across contexts (2026-11-09)

- **Layers**: a domain-free base grammar; importable term packs such as CLI and HTTP, each bringing words with their
  logical meaning; the product's terms; the bounded context's terms.
- **A context may redefine a word**, marked on its entry (`Redefines:`).
- **Seam patterns** decide how words cross contexts.
- **Compounds** are attribute-derived ("batch status"), relation-derived ("request comment") or named and declared
  ("pull request"). An **attributive noun** is the way to tell different things apart ("http status", "work item").
- **A verb may have several frames**, its subject and object kinds picking the meaning. One meaning with a wider
  frame shares one predicate. Different meanings told apart by kinds are separate predicates. Two meanings with the
  same kinds need different words, and are refused otherwise. This partly reverses b84's one `Frame:` per verb.
- **design-model-check's lines name model check's rules from a catalogue artifact** (b123), labels in plain English
  for now; the labels in the controlled language later (b124).
- **Performance is not a constraint** (b119's studies).

### 4.3 Triggers and refusals (2026-11-09)

- **Command options and API parameters are arguments in the trigger**: "When the person runs `work backlog` with the
  `--json` option". **Where** is kept for product features.
- **Refusal lines say "shall refuse the command and name X"**. The rest is entailed by U11 and the CLI pack's
  definition of refuse (b122), shown to readers by an explain command (b126) and in the generated Gherkin, and
  carried into the implementation and tests once (b125).

### 4.4 Time (2026-11-09)

The first version covers:

1. **Time as domain data**: time values and durations as attributes, units, "after", "before", "within the last N",
   "newest", "oldest". The function words are in the base grammar; the units are in a time pack.
2. **Time as a trigger**: a clock actor in the time pack; schedules and moments as events.
3. **The order of domain events**: "after", "before", "since" over events; history ("has published").

Operational timing ("within N", "always", "eventually") is deferred to b127.

### 4.5 Modality (2026-11-09)

All three kinds in the first version:

| Kind | Words | Route |
|---|---|---|
| obligation | shall / shall not | scenarios |
| necessity | always / never: true by definition | a premise of the logic and a check on the data; relation cardinality covers the common case |
| permission | may | no test; the logic reports a line that forbids what a permission allows |

## 5. The session's calls

Made by this session, with the person offline. Each says what was decided and the evidence. Check these.

### Call 1. The base grammar is an application grammar over GF's RGL, with typed categories per kind and frame

The surface forms (agreement, negation, relative clauses, genitives, "a"/"an") come from the RGL. The typing that
makes a wrong-kind noun fail to parse stays: one category per kind, a verb fun typed by its frame, kind-of coercions.

Evidence: phase 2's prototype parsed all 27 candidates with no rewording, 26 to one tree and one to two (a real
ambiguity), round-tripped every tree word for word, and refused all 17 bad sentences (agreement, wrong kind, wrong
value, agentless passive, undefined adjective, untyped code). At about this repository's vocabulary it compiles in
2.1-2.3 s and parses in about 9 ms a line. A core of 28 funs and a 306-line generator (`prototype/gen.py.txt`) did
it, against today's 4,841 generated funs.

Design points carried from the prototype (`prototype-grammar.md` §2-§5):

- Determiners are one core `Det` category (`K_Det : Det -> K_CN -> K_NP0`): 504 funs instead of 791, same results.
- A noun modifier ("of", "on", "in") takes a bare noun head (`K_N`), so modifiers do not stack to the left. With
  modifiers on any `K_CN`, 3 of 27 lines got a second tree.
- Lists and "only" build `K_NP` from `K_NP0`, so a coordinated noun phrase is never coerced to a super-kind.
- Polarity is one argument (`PPos` / `PNeg`), not `*Not` funs (today: 672 funs only to say "not").
- RGL defaults to override: "does not" (not "doesn't"), no comma after a While clause, "that" (not "which").
- The whole corpus round-trips on every build: the prototype's first build silently dropped "not" and only the
  round trip caught it.

### Call 2. One meaning, or refused

2.x's rule was "one tree or refused". 4.0's rule is **one logical form or refused**. A line whose trees all give the
same logical form is accepted (the first tree in a fixed order is kept). A line whose trees give different logical
forms is refused, naming the words that have two readings.

Evidence: compounds give two surface forms of one meaning by the person's decision ("the batch status", "the status
of the batch"); telemetry r1 has two trees of different meaning that typing cannot separate and that a post-parse
rule must refuse (prototype §4.1). The tree count no longer measures ambiguity; the meaning does.

### Call 3. Verbs are marked state or action in the glossary

The part of speech says it: `(verb, state)` or `(verb, action)`. A state verb goes in While clauses and relative
clauses ("a channel that a viewer subscribes to"). An action verb goes in triggers (When, If) and responses. An
action verb in the perfect ("has published") is a state: the history of that action (section 4.4, item 3).

Evidence: the prototype's one design choice that mattered (phase 2: "verbs split into states and actions"); the
event calculus's fluent/event split; it keeps relative clauses from multiplying trees. Marked rather than inferred
because inference from use fails on a verb used once, and the mark is one word per verb (43 verbs here).

### Call 4. Collections and counts, Attempto-style

| Form | Reading |
|---|---|
| "a K", "an K" | at least one (in a condition or trigger: any K; in a response: a new K) |
| "one K" | exactly one |
| "every K", plural "Ks" in a response | each K (distributive) |
| "no K" | none (narrow scope) |
| "at least n Ks", "at most n Ks", "exactly n Ks", "more than n Ks", "fewer than n Ks" | a count over the noun phrase |
| "each of the Ks" | each K of a definite collection |

No collective readings in 4.0 ("the tasks are done" means each task is done). The check reads counts with clingo
aggregates (`#count`).

Evidence: ACE's plurals and counts (phase 1 `logic-cnls.md`), PENG-ASP mapping "exactly one" to a clingo cardinality
rule; phase 3 counts COUNT and COUNT-CMP in 13 lines; U8's "one JSON object" means exactly one, which today reads as
"a".

### Call 5. Written reading rules, each tested against real lines first

The reading rules of section 7.3 are written in a language reference, `grammar/language.md`, each with the real lines
it was tested on and their logical forms. The two rules that differ from ACE:

- **A negated indefinite in a condition is refused.** "While an item does not hold a commit" is ambiguous between
  "holds no commit" and "there is a commit it does not hold". The writer says one of those two. Under "shall not" in
  a response, "a K" reads as any K ("`work` shall not write a status": no status at all).
  Evidence: requests r53 needs today's reading (some comment not held), and ACE's reading would break it (phase 3,
  "What this means", point 4). Refusing the form keeps both meanings sayable and neither guessed.
- **"the" never means "the only one in the world".** It binds to an earlier referent, else the image of a functional
  relation, else a declared indexical, else the line is refused.
  Evidence: 7 sample lines (phase 2 fault 3) and 7 design-model-check lines ("naming the term" with no term).

### Call 6. The indexicals: the run's own things

A kind entry may carry `This: <gloss>`. Then "this K" and a "the K" that binds to nothing earlier refer to the run's
own K. The CLI pack declares `This:` for `command` (the command the run runs). This repository declares it for
`bounded context` ("the bounded context whose repository the command runs in"), `repository` and `session`.

Evidence: phase 2 fault 4 (requests r6: the originless command is not tied to the command run; r33: the comment is
not one `work sync` reads); phase 3 counts "this bounded context" in 12 lines. A glossary field, not base grammar,
because which things a run has is the domain's.

### Call 7. Example data out of lines: a writing rule, a reading and a check

- **Writing rule** (in the authoring skills): a line names kinds and declared constants; sample values go in the
  group's given block.
- **Reading**: a code or quoted string in a line that names no declared constant (an actor, a named instance, a
  command, an option, an attribute value, a rule code, a pack constant) is a **parameter**: its value is bound by the
  scenario, not a constant of the rule.
- **Check**: `model check` warns of each such literal (`w_example`), so a writer sees it; it does not refuse, because
  consumers have many (feature-file-tools here: 19 of 20 lines).

Evidence: phase 2 fault 5 (read literally, migration-tools r21 requires printing "banana" in every misversioned
repository); phase 3 counts 66 lines with EXAMPLE-DATA-OUT.

### Call 8. A defined logical form between tree and facts

A DRS-like form (section 7), produced from the tree by one translation per grammar template (about 40 templates), not
per fun. It is read by three consumers: the clash check (translated once to `check.lp`'s facts), the Gherkin
generator, and the entailment check. Nothing reads the tree after the form is made.

Evidence: phase 1's "What the field offers" (ACE: sentence to DRS to logic; PENG-ASP: DRS-like form to ASP);
`sample-semantics.md` §3.5 gives the minimal predicates and boxes that cover all 27 sample lines; today `spec_facts`
and `spec_steps` translate fun by fun and disagree (b114).

### Call 9. The logic's encoding: b119's `check_fast.lp` is the base; no Z3 in 4.0

b119's rewrite is adopted first, as its own item, on today's grammar. 4.0's new readings extend it, keeping its
header rule (never join two requirement-level facts on a vocabulary word). The entailment check is `comp.py`
(`entailment/comp.py.txt`) rebuilt over the logical form.

Ordered values and counts stay in clingo. Every comparison in this repository's 265 lines is against a constant
(phase 3, COMPARE: "after `1.0.0`", "another name"); comparisons against constants are exact over a finite set of
points (the constants named plus the gaps between them), and counts are clingo aggregates. Z3 joins only if a line
must compare two unknown values with an order (a date against a date), which no line here does.

Evidence: the scale record's recommendation 1 and 4; Z3 answers "unknown" on some quantified queries where clingo
never does.

### Call 10. How packs are stored and imported

- **Plugin packs** live in the plugin: `grammar/packs/<name>.md`, in the glossary's entry form, with optional
  `## Relations` and `## Definitions` (definitions written in the base grammar, such as refuse). 4.0 ships `cli.md`
  and `time.md`.
- **A context's own packs** (the product's terms, or a copy of an upstream's published terms) live at
  `spec/packs/<name>.md`, same form, with a `source:` line naming where they were copied from.
- **A context imports packs** in `spec/index.md`'s frontmatter: `imports: [cli, time]`. A name that is both a plugin
  pack and a context pack is refused.
- **Layer order**: base grammar, then imported packs in the order listed, then the glossary of `spec/index.md`, then
  each capability's `## Terms`. A word defined in a lower layer and again in a higher one needs
  `Redefines: <pack>` on the higher entry, else `model check` refuses it (`v_t16`).
- **Seam patterns** are recorded on an upstream entry under `## Upstreams` as `seam:` with one of `shared-kernel`
  (both contexts import the same pack), `conformist` (this context copies the upstream's pack and imports it) or
  `anticorruption` (this context's own words, marked `Redefines:` where they take an upstream's word). 4.0 reads and
  checks the field; it does not fetch anything across repositories. Request lines keep being parsed in the
  upstream's grammar, as today.

Evidence: the person's layers (4.2); the existing `## Upstreams` entries (`backlog_forms`' `--upstream`); "Product-
level artifacts ... read from a product repository" is already a `## Not yet` of design-model-check.

### Call 11. What the CLI pack holds

The fixed response verbs of today's core become ordinary pack verbs with frames: the base grammar knows no
command-line words.

| Word | Entry |
|---|---|
| tool (noun) | a program a person or a session runs |
| command (noun) | what a person or a session runs; `This:` the command the run runs |
| option (noun) | a named argument of a command, written as a code (`--json`) |
| reason (noun) | why a tool refuses a command |
| output (noun) | what a tool prints |
| run (verb, action) | Frame: agent runs command. Frame: agent runs command with option. Frame: agent runs command on thing. |
| print (verb, action) | Frame: tool prints thing. |
| exit (verb, action) | "exit successfully"; "exit with an error naming thing" |
| change (verb, action) | Frame: agent changes thing; "change nothing" |
| refuse (verb, action) | Frame: tool refuses command. Definition: a tool refuses a command when it exits with an error on it. |
| name (verb, action) | Frame: agent names thing ("refuse the command and name the reason") |

The pack's `## Definitions` carry refuse (b122). U11 stays in this repository's `spec/universal.md` (it is this
plugin's rule that a refusal changes nothing), not in the pack: a consumer's tool may refuse differently. The
builder may move U11 into the pack if every consumer agrees; that is a request, not this design.

Evidence: phase 1: the fixed verbs are 246 of 443 response conjuncts and have no frame; 93% of triggers are "X runs
`cmd`".

### Call 12. The If precedence is a stated reading rule, shown by `model explain`

An If line names an unwanted event. Where its state holds, its response replaces the response of every When line of
the same trigger. The check does not report that pair as a clash; `model explain` on the When line lists each If line
that takes precedence over it; the language reference states the rule.

Evidence: b117 offers "make the If precedence a stated rule of the language or pair them and report". backlog r20
(tasked: refuse `work idea`) over r21 (tracking: write an item) is the intended behaviour, not a fault: on a task
branch the refusal must win. Reporting every such pair would flood the check with intended overrides; hiding them is
what b117 objects to. Stating and showing does neither.

### Call 13. Defined conditions stay, as sentences of the base grammar

A condition entry (adjective) may still be defined, but only by a sentence of the base grammar
(`A repository is idle when ...`), never by prose. A prose-defined condition is refused by `model check` after the
switch (`v_t19`). A defined condition whose definition is used by one line only is warned (`w_inline`): put the
sentence in the line. The universal adjectives (empty, given, defined) are base grammar words.

Evidence: the person: "common English words keep their English meaning", "a small fixed set of general adjectives
(empty, given, defined) may be universal"; requests r36 and r39 want named composite states (phase 3, open choice 5);
the anti-goal of coined adjectives returning.

### Call 14. Relation rows: a fixed word set and one reading of a blank cardinality

A relation row's word is a preposition from a fixed set (of, in, on, for, with, from, to, by, at) or a role noun
(upstream, target). A row whose word is a verb (adds, changes, removes) becomes a verb with a frame (3.0 call 4,
finished). A blank cardinality means **any number** for every word; `one` makes the relation functional. The language
reference says so.

Evidence: b115 (the check reads blank as functional for five prepositions only, and nothing says so); 70 of 98 rows
here are blank; b109 (an L1 through a blank row) is moot once blank has one reading.

### Call 15. Transition by a per-file language marker; one release

The new pipeline is built beside the old one, item by item, and switched on per file by the existing marker:
`language: codified-2` in a capability's frontmatter (and in `spec/index.md` for the glossary and for `model parse`).
This repository's files are reworded one share at a time; the last item removes the old pipeline. Release 4.0.0 is
tagged only then: consumers never see two languages.

Evidence: the 3.0 design's stance ("Reword everything, we are still in early alpha"; no period with both grammars)
applies to what consumers get. Inside the build, a per-file switch lets each item pass its tests on its own, which
one batch task an hour requires. 265 lines and 52 scenario test files cannot be reworded in one task.

### Call 16. This repository's spec reworded, b118 folded in

Every line is reworded from phase 3's candidate (the starting point, not the answer), with the faults b118 lists
fixed in the same share. A line whose text changes gets a new id. Dead vocabulary (66 adjectives, unused kinds,
verbs and resources) is removed with the glossary item. design-model-check's 47 meta-level lines name rules from
b123's catalogue.

## 6. The language at a glance

For the builder: what 4.0 lines and entries look like. The exact spelling is the builder's where this does not fix
it, as long as each fact is read from one place.

### 6.1 Entries

```
- **subscribe** (verb, state): a viewer follows a channel's uploads. Forms: subscribes, subscribed.
  Frame: viewer subscribes to channel.
- **write** (verb, action): an agent puts text into a file. Forms: writes, written.
  Frame: agent writes text. Frame: agent writes text to file.
- **name** (verb, action): an agent says which thing it means. Frame: agent names thing.
- **name** (verb, state): a text holds a thing's name. Frame: text names thing.
- **print** (verb, action): Redefines: cli. `work` prints in the person's terminal. Frame: tool prints thing.
- **bounded context** (noun): ... This: the bounded context whose repository the command runs in.
- **pull request** (noun): ... Kind of: thing.
- **idle** (adjective of repository): A repository is idle when the release of the repository is `own` and no
  initiative of the repository is open.
```

- The part of speech is in the parentheses, with the aspect for a verb.
- Several `Frame:` lines in one entry are one meaning, one predicate.
- Two entries of one word are two meanings, two predicates; the kinds must tell them apart (agent against text
  above). Entries whose frames overlap in every slot (same kinds, or one under the other) are refused (`v_t15`).
- `spec/index.md` frontmatter: `language: codified-2`, `imports: [cli]`.

Compounds: "the batch status" is derived from `status (attribute of batch)`; "a request comment" from the row
`comment | of | request`; both mean what "the status of the batch" and "a comment of a request" mean. A declared
compound ("pull request") is a noun entry. A declared compound that a row or attribute also derives is refused
(`v_t18`).

### 6.2 Lines

| Construct | Example (candidate lines from phase 2 and 3) |
|---|---|
| state in While, conformance | While a request comment does not conform to the comment schema, when a session runs `work sync`, `work` shall print the comment and not write the comment. |
| "of", "no" | While a commit of an item in a batch cites no item, if the person runs `work batch review` on the batch, then `work` shall refuse the command and name the commit. |
| short refusal | If the person runs `work ready` on an item whose status is not `shaped`, then `work` shall refuse the command and name the status. |
| option in the trigger | When the person runs `work backlog` with the `--json` option, `work` shall print one JSON object. |
| relative clause | While no video is from a channel that the viewer subscribes to, ... |
| whose | ... a verb whose entry has no frame ... |
| only | A worker shall change only files in its worktree. |
| count | ... `work` shall pick at most five items. |
| comparison | While the release of the repository is after `1.0.0` and before `3.0.0`, ... |
| time | While the newest video of a channel was published within the last seven days, ... |
| clock trigger | When the clock reaches the publish time of a video, ... |
| history | While the batch has published a pull request, ... |
| indexical | ... `work` shall write a request to the upstream of this bounded context. |
| necessity | A batch always has exactly one batch plan. |
| permission | A session may read any file. |
| Where (product feature) | Where the plugin is installed with hooks, when a session starts, ... |

## 7. The logical form and the reading rules

### 7.1 Referents

A referent has a kind and an origin: `while`, `trigger` (both universally quantified over the line and accessible in
the response), `response` (new), `indexical` (the run's command, repository, session, this bounded context),
`parameter` (bound by the scenario's given block), `constant` (an actor, a named instance, a value, a rule code).

### 7.2 Atoms and boxes

| Atom | Covers |
|---|---|
| `kind(x, K)` with sub-kinds | every noun |
| `attr(x, A, v)`, `cmp(x, A, op, v)` with the attribute's declared order | status, release, versions, times |
| `rel(R, x, y)` with cardinality; `fn(R, y) = x` for "the R of y" | of, in, upstream of |
| `event(e, verb, sense, roles)` with subject, object, recipient, prepositional roles | every action verb |
| `state(verb, sense, roles)` | every state verb |
| `run(e, agent, command, options)` | every CLI trigger (a pack verb, kept as its own atom for the pair index) |
| `conforms(x, artifact)` | conformance to a named schema or format |
| `defined(C, box)` | a defined condition, as its definition's box |
| `history(verb, sense, roles)` | "has published": set by the event, never unset |
| `initiates(e, f)`, `terminates(e, f)`, `nochange(e)` | write, remove, set; change nothing |

| Box | Covers |
|---|---|
| rule: modality, While, trigger (When or If), Where, response | every line; If carries a precedence tag (call 12) |
| not: narrow scope over its referents | "no K", "does not", "shall not" |
| every: restrictor, scope | every, plurals in a response, each of |
| only: agent, verb, restrictor | "shall V only Ks that ...": every K the agent Vs satisfies the restrictor; obliges nothing |
| count: op, n, restrictor, scope | at least / at most / exactly / more than / fewer than |
| or | today's case split (`R#n`) |
| necessity, permission | always / never; may |

Times: the time pack's `moment` and `duration` kinds; "within the last N units" is `cmp(x, A, after, now - N)`, with
`now` the moment of the trigger; "newest" and "oldest" are an order over a definite collection.

### 7.3 The reading rules

Each rule goes into `grammar/language.md` with the real lines it was tested on. The builder runs each against the
lines named before writing it, and changes the rule, not the lines, if a line's intended meaning disagrees.

| # | Rule | Test lines |
|---|---|---|
| R1 | "a K" in a While clause or a trigger means any K; in a response, a new K. | requests r33, batches r13 |
| R2 | "the K" binds to an earlier referent of kind K in the line; else to the image of a functional relation ("the branch of the task"); else to a declared indexical; else the line is refused, naming the noun. | design-model-check r58-r61, migration-tools r13-r16 |
| R3 | "no K" is "there is no K", with scope only over its own clause. | migration-tools r8 |
| R4 | "does not V a K" in a condition is refused (say "Vs no K" or "a K that X does not V"); under "shall not", "a K" means any K. | requests r53, U5 |
| R5 | "X shall V only Ks that P": every K that X Vs satisfies P. It obliges no V. | U7, trials r2 |
| R6 | "every K that P" in a response: for each such K. The generated scenario gives two Ks, so the line is not vacuous. | batches r8, requests r37 |
| R7 | "one K" is exactly one; "a K" at least one; counts as call 4. | U8 |
| R8 | "its" binds to the subject of its clause; if a second referent of the kind the relation needs is accessible, the line is refused. | trials r2 |
| R9 | When is an event (an edge); While a state that holds when the event happens (a level); If an unwanted event whose response takes precedence (call 12). Response at the next step; inertia for every state not changed. | backlog r20/r21 |
| R10 | A literal that names no declared constant is a parameter (call 7). | migration-tools r21 |
| R11 | "this K" and an unbound "the K" with a `This:` entry are the run's own K (call 6). | requests r6, r33 |
| R12 | A line with no trigger and no "always"/"never" is refused: it would read as "in every state". | phase 2 fault 2 |

### 7.4 What reads the form

- **The clash check**: the form translated once to `check.lp`'s facts (`spec_lf_facts`). New readings: every, only,
  counts, negated scopes, the If tag, necessity premises (constraints in both states), permissions (L7: a "may" line
  whose action a "shall not" forbids in an overlapping state and trigger).
- **The entailment check**: `comp.py`'s method over the form. Each entailed response names its premises (a universal
  condition, a pack definition, a necessity line). `model logic` reports a line all of whose Thens are entailed by
  other lines (L8, a warning: analysis-tools r26, feature-file-tools r7).
- **The Gherkin generator**: Givens from the While and trigger referents, a When from the trigger, Thens from the
  response, leaving out each Then the entailment check marks entailed by a universal condition or pack definition
  (it writes a `# entailed: U11` comment in its place, byte-stable), since one shared code path and one check after
  every scenario guarantee it (b125).

## 8. The backlog items around b112

| Item | Placement |
|---|---|
| b107 object relative clauses | folded into I9; withdrawn when I9 is shaped, citing it |
| b10 prose conditions defined in the language | folded: prose conditions become structure in the rewords (I21-I27) or base-grammar definitions (call 13); withdrawn citing I20 |
| b109 L1 through a blank-cardinality row | superseded by call 14 (folded into I12); withdrawn citing it |
| b113 subject-verb agreement | folded into I7 (the RGL agrees); its lines are I7's |
| b114 check and Gherkin read every, only, at most one, negated indefinite alike | folded into I11-I14 (one form) |
| b115 blank cardinality read one way and stated | folded into I12 (call 14) |
| b116 only keeps its meaning | folded into I11 (R5) and I12 |
| b117 universal statements paired; If precedence stated | folded into I12 (pairing) and call 12; `model explain` (I13) shows the precedence |
| b118 the line faults | folded into the rewords I21-I27, each share fixing its own (listed per item) |
| b119 the clingo rewrite (with b120) | kept as itself: I1, first, on today's grammar |
| b120 an unsatisfiable solve reported | folded into b119 (I1), as b119's notes ask |
| b121 actor Kind of: in the domain facts | folded into I12 (the facts are rebuilt from the form) |
| b122 refuse defined | folded into I6 (the CLI pack's definition) |
| b123 the rule catalogue | kept as itself: I2, before the design-model-check reword |
| b124 catalogue labels in the controlled language | left out: after 4.0 |
| b125 entailment into implementation and tests | folded into I13 (check side) and I14 (generator and the one refusal path) |
| b126 `model explain` | folded into I13 |
| b127 operational timing | left out: deferred |

## 9. What changes, module by module

Against CLAUDE.md's module map. "New" rows are added to the map by the item that makes the module.

| Module | Change | Item |
|---|---|---|
| `grammar/check.lp` | `check_fast.lp` adopted; then extended for every, only, counts, negated scopes, the If tag, necessity, permission (L7) | I1, I12, I15-I17 |
| `scripts/spec_solve.py` | `spec_solve_fast.diff`; an unsatisfiable solve an error (b120) | I1 |
| `scripts/model.lp` | new codes and labels: `v_t14`-`v_t19`, `v_d9`, `w_example`, `w_unrouted`, `w_inline`; `v_t2` relabelled (two entries of one word allowed for verbs whose kinds differ); `v_p2` relabelled "more than one meaning"; `v_p0` names codified-2 | I3, I5, I6, I10, I18, I28 |
| `scripts/tools_grammar.py` | the RGL pinned, installed and probed; its compiled `.gfo` cached | I4 |
| `scripts/spec_lexicon.py` | aspect in the part of speech, several entries per verb word, `This:`, `Redefines:`, `imports:`; layers merged | I5, I6 |
| `scripts/spec_frames.py` | several frames per entry; senses; overlap refusal (`v_t15`); aspect missing (`v_t14`) | I5 |
| **new** `scripts/spec_packs.py` | the packs: read from `grammar/packs/` and `spec/packs/`, imports, layer order, `Redefines:` (`v_t16`), unknown import (`v_t17`) | I6 |
| **new** `grammar/packs/cli.md`, `grammar/packs/time.md` | the two packs | I6, I16 |
| `scripts/spec_relations.py` | the fixed word set; blank cardinality any number | I12 |
| **new** `grammar/Base.gf`, `grammar/BaseEng.gf` | the hand-written core over the RGL (about 30 funs): clauses, EARS frames, Det, polarity, lists, modality | I7-I9, I15-I17 |
| **new** `scripts/spec_rgl.py`, `scripts/spec_rgl_np.py` | the generator over the lexicon: per kind, frame, attribute, row; noun-phrase templates. Replace `spec_typed.py`, `spec_typed_verbs.py`, `spec_typed_def.py` | I7-I9 |
| `scripts/spec_grammar.py` | builds grammar 4 for a codified-2 context; one meaning or refused; cache keys include the RGL release | I7, I9 |
| `scripts/spec_frames_refusal.py`, `scripts/spec_tree.py` | refusals and guards on the base grammar's categories; GF completion in the hint | I10 |
| **new** `scripts/spec_lf.py`, `scripts/spec_lf_read.py` | the logical form's types and the per-template translation; the reading rules (R1-R12), indexicals, parameters | I11 |
| **new** `grammar/language.md` | the language reference: constructs, reading rules, tested lines | I11 (extended by I12-I17) |
| **new** `scripts/spec_lf_facts.py` | the form to `check.lp`'s facts, with actors' Kind of: (b121). Replaces `spec_facts.py`, `spec_facts_np.py` | I12 |
| `scripts/spec_logic_vocab.py` | domain facts from the packs and lexicon: actor kinds, definitions, orders of values | I12 |
| `scripts/spec_findings.py` | L7, L8 worded | I13, I17 |
| **new** `scripts/spec_entail.py` | the entailed-Then check from `comp.py`, over the form | I13 |
| **new** `scripts/model_explain.py` | `model explain <cap>#r<n>` | I13 |
| `scripts/spec_steps.py` | steps from the form; entailed Thens left out with a comment. Replaces `spec_steps_facts.py` | I14 |
| `grammar/Steps.gf`, `StepsEng.gf`; `scripts/features_vocab.py`, `features_vocab_gf.py` | the step grammar over Base; the vocabulary read back from it | I14 |
| `scripts/features_generate.py` | the form's groups; entailed Thens; byte-stable | I14 |
| `scripts/spec_context.py`, `scripts/spec_read.py`, `scripts/model_spec.py` | each file read through its marker's pipeline; codified-2 accepted | I19 |
| `scripts/model_parse.py` | grammar from `spec/index.md`'s marker (I7a), or from a capability file's with `--capability` (I19); `--form` prints the logical form | I7a, I11a, I19 |
| `scripts/readiness_bar.py`, `scripts/request_lines.py`, `scripts/backlog_lines.py` | unchanged APIs over the switched pipeline, each line parsed in its capability file's grammar; checked by their tests | I19 |
| `scripts/backlog_lines.py`, `scripts/backlog_section.py`, `scripts/backlog_forms.py` | `work line --retires` (a block's `retired:` written, laid and taken out) (I0); `--recodify` (the marker in a block, laid and taken out) (I19) | I0, I19 |
| `scripts/shop_files.py`, `scripts/tools_grammar.py`, `scripts/tools_env.py`, `scripts/features_gherkin.py`, `scripts/transcripts.py` | the four other `Refused` classes subclass `shop_files.Refused` | I14b |
| **new** `scripts/spec_example.py` | literals that name no constant (`w_example`); defined conditions used once (`w_inline`) | I18 |
| `scripts/model_decisions.py`, `scripts/decision_write.py` | `verified_by:` read and checked (`v_d9`); `--verified-by`; `w_unrouted` | I3 |
| `tests/scenarios/vocab.py` and handlers | step definitions matched by the new step grammar; the U11 check kept as the one test of refusals | I14, I21-I27 |
| **new** `scripts/migrate_upgrade_cnl4.py` | the upgrade step "the controlled language 4" | I29 |
| removed | `grammar/Core*.gf`, `Req*.gf`; `spec_typed*.py`, `spec_facts*.py`, `spec_steps_facts.py`; codified-1 reading | I28 |
| `grammar/corpus/` | rewritten for grammar 4 share by share; `refused.txt` gains the anti-goals (agentless passive, negated indefinite in While, antecedentless "the", two meanings) | I7-I11, I21-I27 |
| README, `.claude-plugin/plugin.json`, `.shop/plugin-version`, migration-tools' version given blocks | 4.0.0 | I29 |
| `skills/shaping-items`, `skills/raising-a-request`, `skills/taking-in-a-request`, `skills/building-a-batch` | the writing rules: structures over adjectives, example data out, states in While, short refusals, packs, `model explain` | I30 |

## 10. The work, in items

Thirty-seven items in dependency order (revised 2026-11-10 after a builder's check, section 13). Each is sized for one
batch task (a builder subagent of about an hour; I21 and I22 are the two longer tasks, section 13 point 9). I0 gives
`work line` the retiring of a line; I1-I18 add the new pipeline beside the old; I19 switches files by marker; I20-I27
reword this repository; I28 removes the old pipeline; I29 releases; I30 updates the skills. Where the rest of this
design names a split item by its number alone (I7, I11-I14, I21-I23), it means all its parts.

Three items have no requirement line and are carried as plans, not through `work batch` (the readiness bar refuses
an item with no line, `scripts/readiness_bar.py:119`): I14b, I20 and I30. Each is a record
`.shop/records/<date>-<topic>/plan-<item>.md`, carried out by one fresh agent and reviewed by one fresh reviewer of
the whole branch (CLAUDE.md's rule for a plan), after the batches it depends on have merged. The session's call
(section 13 point 2).

### 10.1 About the draft lines

- Lines are drafted **in today's grammar** about the tools' observable behaviour, as b106's were, without ids
  (`work line` gives them). Each shape was checked with `python3 scripts/model parse` using an existing adjective
  in place of the new one.
- This forces coined adjectives (`relative`, `antecedentless` ...), the very thing 4.0 removes. They are kept to the
  meta level (adjectives of requirement, term, capability) and each is reworded by I21 (design-model-check) or the
  share that holds it, using the rule catalogue (b123) and the new noun phrase.
- **A line is parsed in its capability file's grammar** (the session's call, section 13 point 3): the grammar its
  file's marker names once the item is laid, `language: codified-1` the old grammar, `codified-2` grammar 4.
  `request_lines`, `readiness_bar` and `backlog_lines` take the grammar from the capability file, not from
  `spec/index.md`; `model parse --capability <cap>` does the same, and falls back to the index's marker without it.
  So a line for a capability not yet reworded is written in today's grammar even after I20, and a reword item's lines
  (I21-I27) are grammar 4 because the item switches its file's marker (`work line --recodify`, I19). I28's and I29's
  lines are written in grammar 4, since their capabilities are reworded by then; both forms are shown.
- **A coined adjective may share its word with another kind's** (answered by the sources, section 13 point 6):
  `malformed` has entries of four kinds today (term, relation row, upstream entry, given block) and `model check`
  passes, so `stale` (of rule catalogue), `plural` (of requirement) and `compound` (of requirement) stand beside
  today's `stale` (of decisions index), `plural` (of capability-proposal) and `compound` (of requirement group).
- Where a line needs a new noun, its term bullet is given; nouns that are files say `Kind of: file`.

### 10.2 Summary

| # | Title | Capabilities | Depends on | Lines |
|---|---|---|---|---|
| I0 | `work line --retires`: a line that replaces another | readiness | - | 2 |
| I1 | b119: the clingo rewrite of `check.lp`, with b120 | design-model-check | - | 1 |
| I2 | b123: the rule catalogue | design-model-check | - | 2 |
| I3 | Verification routes on design-decisions | decision-tiers | - | 3 |
| I4 | The RGL pinned by `tools install` | analysis-tools | - | 2 |
| I5 | The 4.0 term entry: aspect, several frames, senses, `This:` | design-model-check | - | 4 |
| I6 | Packs: storage, imports, layers, `Redefines:`; the CLI pack | design-model-check | I5 | 4 |
| I7a | The base grammar over the RGL: core, generator, agreement, `model parse` switch, corpus twin, the smallest codified-2 world | design-model-check | I4, I6 | 2 |
| I7b | The base grammar: options in the trigger, the aspect refusal | design-model-check | I7a | 2 |
| I8 | Noun phrases 1: of, its, no, has, lists, only, compounds | design-model-check | I7b | 4 |
| I9 | Noun phrases 2: relative clauses, whose; one meaning or refused | design-model-check | I8 | 3 |
| I10 | Refusals and hints on the base grammar | design-model-check | I9 | 1 |
| I11a | The logical form: types, translation, `--form`, indexicals | design-model-check | I9 | 2 |
| I11b | The reading rules R1-R12 and their refusals; `grammar/language.md` | design-model-check | I11a | 3 |
| I12a | The form to the check: translation, every, only, actor kinds | design-model-check | I1, I11b | 2 |
| I12b | The check's new rules: scopes, If precedence, universal pairing, blank cardinality | design-model-check | I12a | 2 |
| I13a | The entailment check (L8) | design-model-check | I6, I12b | 1 |
| I13b | `model explain` | design-model-check | I13a, I0 | 4 |
| I14a | Steps from the form; entailed Thens left out | feature-file-tools | I13a | 1 |
| I14b | One refusal path (plan) | - | I14a | 0 |
| I15 | Collections and counts | design-model-check | I12b | 2 |
| I16 | The time pack and time constructs | design-model-check | I12b | 4 |
| I17 | Modality: always, never, may | design-model-check | I12b | 3 |
| I18 | Example data out of lines | design-model-check | I11b | 1 |
| I19 | The switch: codified-2 files through the new pipeline | design-model-check, feature-file-tools, readiness | I10, I14a | 3 |
| I20 | This repository's glossary in 4.0 (plan) | - | I14b, I15-I19 | 0 |
| I21 | Reword design-model-check | design-model-check | I0, I2, I20 | 47 reworded |
| I22 | Reword requests | requests | I0, I20 | 44 reworded |
| I23a | Reword analysis-tools and trials | analysis-tools, trials | I0, I20 | 38 reworded |
| I23b | Reword the universal conditions | `spec/universal.md` | I0, I20 | 5 reworded |
| I24 | Reword migration-tools, telemetry and batch-measurement | migration-tools, telemetry, batch-measurement | I0, I20 | 32 reworded |
| I25 | Reword feature-file-tools and readiness | feature-file-tools, readiness | I0, I20 | 32 reworded, plus I0's and I19's own |
| I26 | Reword backlog and batches | backlog, batches | I0, I20 | 39 reworded |
| I27 | Reword decision-tiers, pr-review, intake, conversation, brainstorming | decision-tiers, pr-review, intake, conversation, brainstorming | I0, I3, I20 | 28 reworded |
| I28 | The old pipeline removed | design-model-check | I21-I27 | 1 |
| I29 | The upgrade step "the controlled language 4" and release 4.0.0 | migration-tools | I28 | 2 |
| I30 | The authoring skills in 4.0 (plan) | - | I28 | 0 |

"Lines" counts the requirement lines an item adds (term bullets apart); a reword's count is its live lines, each kept
or replaced under a new id. The reworded counts of I23a-I27 are today's live lines and may move by the lines earlier
items add (I0, I1-I19 add to design-model-check, feature-file-tools, readiness, decision-tiers, analysis-tools); each
reword covers every line its capabilities hold when it is shaped.

I0-I5 have no dependencies and can go in the first batch. I21-I27 are independent of each other.

### 10.3 The items

#### I0. `work line --retires`: a line that replaces another

The session's call (section 13 point 1). `work line --retires <cap>#r<n> "<line>"` gives the new line the next id of
its capability, as `work line` does, and writes the old id under the capability block's `retired:` in the item's
`## Requirements` (`backlog_section` reads and writes it; `backlog_lines.lay_onto` moves the old line out of the
capability's Behaviour and its id into `retired:`, `unlay` puts both back, `renumber` keeps the retired id). The new
id goes into `unbuilt:` like any laid line; a task builds it by taking it out of `unbuilt:` (a reworded line whose
behaviour exists already XPASSes until it does, which is the signal). An id that the capability does not hold, or
holds only under `retired:`, is refused.

readiness:

- **nonexistent** (adjective of requirement): a requirement named by an id that no capability holds as a live
  requirement.
- Where `--retires` is given, when the person runs `work line` on an item, `work` shall write a requirement and commit
  the item.
- Where `--retires` is given, if the person runs `work line` on a requirement that is nonexistent, then `work` shall
  exit with an error naming the requirement and change nothing.

#### I1. b119: the clingo rewrite of `check.lp`, with b120

Builds what b119's notes and the scale record's recommendation 1 say: `check_fast.lp` as `grammar/check.lp`,
`spec_solve_fast.diff` into `spec_solve.py`, the two test edits, the header rule, a timing test on a 4x scaled spec,
and b120 (an unsatisfiable solve is an error naming the capability, and one pair never makes the program
unsatisfiable: the pair marked out, the others' findings kept). Same findings as today on this repository.

design-model-check:

- **unpairable** (adjective of capability): a capability two of whose requirements share a named code that
  `grammar/check.lp` cannot unify, and two others of whose requirements conflict (an L1).
- When the person runs `model logic` on a capability that is unpairable, `model` shall print a requirement and print
  "L1".

The pair set aside is printed (its requirements), and the other pair's L1 is still found: that is b120's soft form.
The hard error (an unsatisfiable solve reported as an error naming the capability) cannot be reached from a scenario
once the pair is soft, so it is tested once in `tests/scripts/`, with a `check.lp` made unsatisfiable on purpose. The
session's call (section 13 point 5).

#### I2. b123: the rule catalogue

As b123 says. The catalogue is the plugin's generated file (`grammar/rules.md`: each rule's code, label, severity,
where it is implemented, the lines citing it, a failing and a passing example), checked current by `--check`. Each
code becomes a named instance of `rule`, and a verb `violate` (Frame: thing violates rule) lets a line name a code.

design-model-check:

- **rule catalogue** (noun): the generated file `grammar/rules.md`, one entry a rule. Kind of: file.
- **violate** (verb, action in 4.0): Forms: violates, violated. Frame: thing violates rule.
- **stale** (adjective of rule catalogue): a rule catalogue that is not what `model rules --write` would write.
- Where `--write` is given, when the person runs `model rules`, `model` shall write the rule catalogue and exit
  successfully.
- Where `--check` is given, if the person runs `model rules` on a rule catalogue that is stale, then `model` shall
  exit with an error naming the rule catalogue and change nothing.

Plain `model rules` keeps design-model-check r54 ("shall print every rule"); `--write` writes `grammar/rules.md` and
`--check` compares it (the session's call, section 13 point 6). `stale` gets a second entry, of rule catalogue, as
`malformed` has four today.

#### I3. Verification routes on design-decisions

A decision may carry `verified_by: [scenario | check | judgement | monitor]` beside `enforced_by`. `work decision
--verified-by <route>` writes it. `model check` refuses a route outside the four (`v_d9`) and warns of a universal
condition that no decision's `verified_by` covers (`w_unrouted`; a decision covers a universal condition by citing
its id in `rests_on` or the decision's text, the builder's choice). This repository's U4, U5, U7, U8, U11 get their
routes in this item (check after each scenario for U4, U8, U11; judgement for U5, U7).

decision-tiers:

- **unrouted** (adjective of universal condition): a universal condition that no design-decision's `verified_by`
  covers.
- **misrouted** (adjective of design-decision): a design-decision whose `verified_by` names a route other than
  `scenario`, `check`, `judgement` or `monitor`.
- Where `--verified-by` is given, when the person runs `work decision`, `work` shall write a design-decision and
  commit the design-decision.
- When the person runs `model check` on a universal condition that is unrouted, `model` shall print the universal
  condition.
- If the person runs `model check` on a design-decision that is misrouted, then `model` shall exit with an error
  naming the design-decision.

#### I4. The RGL pinned by `tools install`

`tools install` fetches and builds gf-rgl at the pinned release into the plugin's tool directory beside GF;
`tools probe` reports it in the grammar block (and `--json`); `spec_grammar` finds it through `tools_grammar`.

analysis-tools:

- While the analysis tool `gf-rgl` is `missing`, when the person runs `tools install`, `tools` shall install the
  analysis tool `gf-rgl`.
- When the person runs `tools probe`, `tools` shall print the analysis tool `gf-rgl`.

#### I5. The 4.0 term entry: aspect, several frames, senses, `This:`

`spec_lexicon` and `spec_frames` read `(verb, state)` and `(verb, action)`, several `Frame:` lines in one entry (one
predicate), two entries of one verb word (two predicates), and `This:` on a kind. `model check` refuses a verb with
no aspect (`v_t14`) and two senses that overlap (`v_t15`); `v_t2` allows two verb entries whose kinds differ. The
old grammar keeps working: it ignores the aspect and makes one fun per frame, as it does today. This item adds the
aspect to this repository's 43 verb entries (term edits, not requirement edits), so `model check` stays clean.

design-model-check:

- **aspectless** (adjective of term): a verb whose entry says neither `state` nor `action`.
- **multiframed** (adjective of term): a verb whose entry has two `Frame:` lines.
- **polysemous** (adjective of term): a verb with two entries whose frames take kinds that do not overlap.
- **overlapping** (adjective of term): a verb with two entries whose frames take, in every slot, the same kind or
  one kind under the other.
- If the person runs `model check` on a term that is aspectless, then `model` shall exit with an error naming the
  term.
- When the person runs `model check` on a term that is multiframed, `model` shall exit successfully.
- When the person runs `model check` on a term that is polysemous, `model` shall exit successfully.
- If the person runs `model check` on a term that is overlapping, then `model` shall exit with an error naming the
  term.

#### I6. Packs: storage, imports, layers, `Redefines:`; the CLI pack

`spec_packs` reads `grammar/packs/*.md` and `spec/packs/*.md`, `imports:` in `spec/index.md`, merges layers in call
10's order, and checks `Redefines:` (`v_t16`) and unknown imports (`v_t17`). `grammar/packs/cli.md` holds call 11's words and
refuse's definition (b122). `model lexicon` shows each term's layer. The old grammar keeps its core verbs; the CLI
pack's words are read but only grammar 4 uses them.

design-model-check:

- **pack** (noun): a file of terms a bounded context imports: `grammar/packs/<name>.md` of the plugin, or
  `spec/packs/<name>.md` of the bounded context. Kind of: file.
- **importing** (adjective of bounded context): a bounded context whose `spec/index.md` imports a pack.
- **misimporting** (adjective of bounded context): a bounded context whose `spec/index.md` imports a pack that
  neither the plugin nor the bounded context has.
- **unmarked** (adjective of term): a term that a pack the bounded context imports defines too, whose entry has no
  `Redefines:`.
- **redefining** (adjective of term): a term whose entry has `Redefines:` naming a pack that defines it.
- When the person runs `model lexicon` on a bounded context that is importing, `model` shall print every term and
  exit successfully.
- If the person runs `model check` on a bounded context that is misimporting, then `model` shall exit with an error
  naming the pack.
- If the person runs `model check` on a term that is unmarked, then `model` shall exit with an error naming the term.
- When the person runs `model check` on a term that is redefining, `model` shall exit successfully.

#### I7a. The base grammar over the RGL: core, generator, agreement, the `model parse` switch, the corpus twin

`grammar/Base.gf` and `BaseEng.gf` (the core: While, When, If, Where, shall, polarity, Det, lists) and
`spec_rgl.py` (per kind, actor, attribute and value, frame by aspect). Agreement from the RGL (b113). `model parse`
uses grammar 4 when `spec/index.md` says `language: codified-2`. The corpus `grammar/corpus/core.txt` gets a grammar
4 twin that round-trips. The scenario worlds gain the smallest codified-2 context: a `spec/index.md` with `language:
codified-2` and `imports: [cli]`, and one capability (the session's call, section 13 point 4); I7b-I18 use it for
their `model parse` and `model logic` scenarios, and I19 extends it to a mixed spec.

design-model-check:

- **plural** (adjective of requirement): a requirement whose subject is plural and whose verb agrees with it, as in
  "When sessions write a file".
- **disagreeing** (adjective of requirement): a requirement whose verb does not agree in number with its subject, as
  in "When sessions writes a file".
- When the person runs `model parse` on a requirement that is plural, `model` shall exit successfully.
- If the person runs `model parse` on a requirement that is disagreeing, then `model` shall exit with an error naming
  the term.

#### I7b. The base grammar: options in the trigger, the aspect refusal

The CLI pack's run with an option in the trigger. An action verb in a While clause or a state verb in a trigger is
refused. Both added to the grammar 4 corpus.

design-model-check:

- **misaspected** (adjective of requirement): a requirement with an action verb in its While clause or a state verb
  in its trigger.
- **optioned** (adjective of requirement): a requirement whose trigger runs a command with an option, as in "runs
  `work backlog` with the `--json` option".
- If the person runs `model parse` on a requirement that is misaspected, then `model` shall exit with an error naming
  the term.
- When the person runs `model parse` on a requirement that is optioned, `model` shall exit successfully.

#### I8. Noun phrases 1: of, its, no, has, lists, only, compounds

`spec_rgl_np.py`: "the R of y" and "its R" over rows and attributes (modifier on a bare noun head), "no K" as subject
and object, has/holds as frames, noun-phrase lists with and/or, "only", attribute-derived and relation-derived
compounds, a declared compound that is also derived refused (`v_t18`).

design-model-check:

- **genitive** (adjective of requirement): a requirement with "of" or "its" over a relation row or an attribute, as
  in "the branch of the task".
- **denying** (adjective of requirement): a requirement with "no" before a noun as a subject or an object, as in "a
  verb has no frame".
- **compound** (adjective of requirement): a requirement with a compound noun that an attribute or a relation row
  derives, as in "the batch status".
- **restrictive** (adjective of requirement): a requirement with "only" before an object, as in "a worker shall
  change only files in its worktree".
- When the person runs `model parse` on a requirement that is genitive, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is denying, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is compound, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is restrictive, `model` shall exit successfully.

#### I9. Noun phrases 2: relative clauses, whose; one meaning or refused

Subject and object relative clauses on any state frame ("a channel that a viewer subscribes to"), "whose" over rows
and attributes, negated forms. The post-parse step keeps a line whose trees give one meaning and refuses one with
two (call 2); until I11 lands, "meaning" is the normalised tree, and I11 swaps in the logical form. b107 folds in.

design-model-check:

- **relative** (adjective of requirement): a requirement with a relative clause on a verb's frame, as in "a channel
  that a viewer subscribes to".
- **possessive** (adjective of requirement): a requirement with "whose" over a relation row or an attribute, as in
  "a verb whose entry has no frame".
- **ambiguous** (adjective of requirement): a requirement with two readings that mean different things, as in a list
  that may belong to either of two verbs.
- When the person runs `model parse` on a requirement that is relative, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is possessive, `model` shall exit successfully.
- If the person runs `model parse` on a requirement that is ambiguous, then `model` shall exit with an error naming
  the requirement.

#### I10. Refusals and hints on the base grammar

`spec_frames_refusal` and `spec_tree` rebuilt on grammar 4's categories, so r58, r59, r63 and r65 hold for a
codified-2 context (their scenarios run against I7a's codified-2 world). The hint lists what may follow where GF
stopped (GF's completion), as terms.

design-model-check:

- **unfinished** (adjective of requirement): a requirement that stops where its frame needs another word.
- If the person runs `model parse` on a requirement that is unfinished, then `model` shall exit with an error naming
  the requirement and print a term.

#### I11a. The logical form: types, translation, `--form`, indexicals

`spec_lf.py` (types, one translation per template), indexicals from `This:` and parameters. `model parse --form`
prints the form.

design-model-check:

- **logical form** (noun): what a requirement means, as referents, atoms and boxes, printed by `model parse
  --form`.
- **indexical** (adjective of requirement): a requirement that says "this" before a kind whose entry has `This:`.
- Where `--form` is given, when the person runs `model parse` on a requirement, `model` shall print a logical form
  and exit successfully.
- When the person runs `model parse` on a requirement that is indexical, `model` shall exit successfully.

#### I11b. The reading rules R1-R12 and their refusals

`spec_lf_read.py` (R1-R12 over the form). `grammar/language.md` written, each rule with its test lines (section 7.3)
and their forms. The refusals of R2, R4, R8 and R12.

design-model-check:

- **antecedentless** (adjective of requirement): a requirement with "the" before a noun that no earlier noun phrase,
  functional relation or declared indexical gives.
- **unquantified** (adjective of requirement): a requirement whose While clause says "does not" before a noun phrase
  with "a" or "an", as in "an item does not hold a commit".
- **triggerless** (adjective of requirement): a requirement with no trigger and neither "always" nor "never".
- If the person runs `model parse` on a requirement that is antecedentless, then `model` shall exit with an error
  naming the term.
- If the person runs `model parse` on a requirement that is unquantified, then `model` shall exit with an error naming
  the term.
- If the person runs `model parse` on a requirement that is triggerless, then `model` shall exit with an error naming
  the requirement.

#### I12a. The form to the check: translation, every, only, actor kinds

`spec_lf_facts.py` translates the form to `check.lp`'s facts; `check.lp` (the rewrite) gains rules for every on an
object and only; actors' Kind of: in the domain facts (b121). For codified-1 files `spec_facts` keeps producing
today's facts until I28; both feed one check. Header rule kept.

design-model-check:

- **restricting** (adjective of capability): a capability with a line that obliges an agent to change only things of
  one kind, and a line in which the agent changes a thing of that kind.
- **exhaustive** (adjective of capability): a capability with a line that obliges a tool to print every thing of a
  kind and a line that forbids it to print a thing of that kind, under one trigger and state.
- When the person runs `model logic` on a capability that is restricting, `model` shall not print "L1".
- When the person runs `model logic` on a capability that is exhaustive, `model` shall print "L1".

#### I12b. The check's new rules: scopes, If precedence, universal pairing, blank cardinality

`check.lp` gains negated scopes, the If tag (call 12), a universal condition paired with each line it bears on
(b117), and blank cardinality as any number (b115, call 14; `spec_relations`' fixed word set).

design-model-check:

- **overriding** (adjective of capability): a capability with an If line and a When line of one trigger whose
  responses differ, where the If line's state holds.
- **contravening** (adjective of capability): a capability with a line whose response a universal condition forbids,
  under the line's trigger.
- When the person runs `model logic` on a capability that is overriding, `model` shall not print "L1".
- When the person runs `model logic` on a capability that is contravening, `model` shall print the universal
  condition.

#### I13a. The entailment check (L8)

`spec_entail.py` builds `comp.py`'s method over the form: each premise one clingo rule, every query in one
stratified model, each entailed response naming its premises. `model logic` reports L8 (every Then of a line is
entailed by other lines). Tested against a frozen copy of today's spec kept as a test fixture, not the live spec (the
session's call, section 13 point 10): on it, 20 Thens are entailed without the refuse definition and 55 with it, as
`entailment/k1_entailed.txt` records.

design-model-check:

- **restating** (adjective of requirement): a requirement each of whose Thens other requirements entail.
- When the person runs `model logic` on a requirement that is restating, `model` shall print "L8".

#### I13b. `model explain`

`model explain <cap>#r<n>` prints the line, "which also means:" each entailed consequence with its premise (U11; the
CLI pack's refuse), and each If line that takes precedence over it (call 12). An id no capability holds is refused,
with I0's `nonexistent` (a meta-level adjective, reworded by I21 and I25, whose lines use it, as "a requirement id
that no capability holds"; section 13 point 11).

design-model-check:

- **refusing** (adjective of requirement): a requirement whose response says that the tool shall refuse the command.
- **overridden** (adjective of requirement): a When requirement over which an If requirement of the same trigger
  takes precedence.
- When the person runs `model explain` on a requirement, `model` shall print the requirement and exit successfully.
- When the person runs `model explain` on a requirement that is refusing, `model` shall print a universal condition
  and a term.
- When the person runs `model explain` on a requirement that is overridden, `model` shall print a requirement that is
  refusing.
- If the person runs `model explain` on a requirement that is nonexistent, then `model` shall exit with an error
  naming the requirement and change nothing.

#### I14a. Steps from the form; entailed Thens left out

`spec_steps` rebuilt over the form; `Steps.gf` over Base; `features_vocab` reads steps back through it. A Then that
a universal condition or a pack definition entails is left out, with a `# entailed: <premise>` comment (byte-
stable). `features generate` runs on a capability and writes a feature file, so the line says that (the session's
call, section 13 point 7).

feature-file-tools:

- **declining** (adjective of capability): a capability with a requirement whose response says that the tool shall
  refuse the command.
- **overstated** (adjective of file): a feature file with a Then step that a universal condition or a pack's
  definition entails from the other steps of its scenario.
- When the person runs `features generate` on a capability that is declining, `features` shall not write a file that
  is overstated.

#### I14b. One refusal path (plan)

A design-decision (tier `check`), written by `work decision`: every refusal of every command reaches one shared base
exception, `shop_files.Refused`, exits with an error naming the reason and leaves the repository unchanged, enforced
by a test of that path and by vocab.py's U11 check after every scenario (b125). Today there are five `Refused`
classes (`shop_files`, `tools_grammar`, `tools_env`, `features_gherkin`, `transcripts`); the other four become
subclasses of `shop_files.Refused`, so every refusal reaches the same path and the U11 check covers them all. That is
one task, not a sweep across every command (the session's call, section 13 point 8). It adds no requirement line (U11
holds already), so it is carried as a plan.

#### I15. Collections and counts

Call 4's forms in grammar 4, the form's count box, and `check.lp`'s reading by `#count`; "one" as exactly one.

design-model-check:

- **counted** (adjective of requirement): a requirement with "at least", "at most", "exactly", "more than" or "fewer
  than" before a number and a noun.
- **overcounted** (adjective of capability): a capability with two lines of one trigger and state whose counts of one
  kind cannot both hold.
- When the person runs `model parse` on a requirement that is counted, `model` shall exit successfully.
- When the person runs `model logic` on a capability that is overcounted, `model` shall print "L1".

#### I16. The time pack and time constructs

`grammar/packs/time.md`: units, `moment`, `duration`, the clock (actor), `reach` (Frame: clock reaches moment),
schedules. Base grammar: after, before, since, within the last N units, newest, oldest; the perfect of an action
verb as history. The form's `cmp` with `now` and the history atom; `check.lp` reads both (comparisons over the
constants named, call 9).

design-model-check:

- **timed** (adjective of requirement): a requirement that compares a moment or a duration with "after", "before",
  "since" or "within the last".
- **clocked** (adjective of requirement): a requirement whose trigger is the clock reaching a moment.
- **historical** (adjective of requirement): a requirement whose While clause says that an agent has done an action,
  as in "the batch has published a pull request".
- **unitless** (adjective of requirement): a requirement with a number where a duration is due and no unit of the
  time pack after it.
- When the person runs `model parse` on a requirement that is timed, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is clocked, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is historical, `model` shall exit successfully.
- If the person runs `model parse` on a requirement that is unitless, then `model` shall exit with an error naming
  the requirement.

#### I17. Modality: always, never, may

"always" and "never" statements with no trigger (necessity: a premise in both states of the check, and a route on a
decision, I3); "may" (permission: no scenario; L7 when a "shall not" line forbids it under an overlapping state and
trigger). `features generate` writes no scenario for a permission and a necessity line's scenario only if its
decision's route is `scenario`.

design-model-check:

- **permissive** (adjective of requirement): a requirement that says an agent may do an action.
- **invariant** (adjective of requirement): a requirement with no trigger that says a thing always holds or never
  holds.
- **forbidding** (adjective of capability): a capability with a line that forbids what another of its lines says an
  agent may do.
- When the person runs `model parse` on a requirement that is permissive, `model` shall exit successfully.
- When the person runs `model parse` on a requirement that is invariant, `model` shall exit successfully.
- When the person runs `model logic` on a capability that is forbidding, `model` shall print "L7".

#### I18. Example data out of lines

`spec_example.py`: each literal in a line that names no declared constant is a parameter (bound by the given block)
and warned by `model check` (`w_example`); a defined condition used by one line only is warned (`w_inline`).

design-model-check:

- **exemplified** (adjective of requirement): a requirement holding a code or a quoted string that names no actor,
  command, option, value, rule or named instance.
- When the person runs `model check` on a requirement that is exemplified, `model` shall print the requirement.

#### I19. The switch: codified-2 files through the new pipeline

`spec_context` loads each capability through its marker's pipeline: codified-2 through grammar 4, the form, its
facts and steps; codified-1 as today. `model logic`, `features generate`, the readiness bar, `work line`, `work
outcome` and the request lines all work over a mixed spec, each line parsed in its capability file's grammar (section
10.1); `model parse --capability <cap>` takes the grammar from that file and falls back to the index's marker.
`model check`'s `v_p0` accepts codified-2. `work line --recodify <cap>` writes the marker switch into the item's
capability block, so a reword item lays its lines into a file that says codified-2 and the bar checks them in grammar
4 (`unlay` puts the old marker back). I7a's world extended to a mixed spec.

design-model-check / feature-file-tools:

- **recodified** (adjective of capability): a capability whose file has `language: codified-2` in its frontmatter.
- When the person runs `model logic` on a capability that is recodified, `model` shall exit successfully.
- When the person runs `features generate` on a capability that is recodified, `features` shall print the feature
  file `features/shelf.feature`. (feature-file-tools, as r17 says it)
- Where `--recodify` is given, when the person runs `work line` on an item, `work` shall write a capability and
  commit the item. (readiness)

#### I20. This repository's glossary in 4.0

`spec/index.md` to `language: codified-2` and `imports: [cli]`; the core's response words replaced by the pack's;
aspects (from I5), senses split (phase 3's SENSE cases: name, list, use, keep against record ...), `This:` on
bounded context, repository, session; relation rows to the word set with explicit `one` where the old check read a
blank as functional; dead terms removed (66 adjectives, unused kinds, verbs, resources, as far as no live line or
row uses them); prose conditions that no line needs removed. Capability `## Terms` that only these shares use move
with their reword. No requirement line changes here; codified-1 capabilities keep parsing through the old pipeline
over the 4.0 glossary (I5 and I6 made the old reader accept it). Lines: none, so carried as a plan (section 10
intro).

#### I21-I27. The rewords

Each reword item, for its capabilities: every line reworded in grammar 4 from phase 3's candidate (`a.tsv` to
`d.tsv`), a new id for each changed line and the old id into `retired:`, example data moved into given blocks,
short refusals, the capability's coined adjectives replaced by structure (or by a base-grammar definition, call 13),
the marker set to codified-2, scenarios regenerated, handlers updated, the corpus file rewritten, and the b118
faults of the share fixed. The lines are the reworded lines themselves; no new behaviour. A line that parses
unchanged and means the same keeps its id.

Each reword is shaped with I0's and I19's commands: `work line --recodify <cap>` once a capability, then `work line
--retires <cap>#r<n> "<grammar 4 line>"` for each changed line. The per-file marker (call 15) means a file switches
whole, so a single capability is never split across tasks: I21 (47 lines) and I22 (44) stay one task each, the two
longer tasks of 4.0 (the session's call, section 13 point 9; a half-switched file would not parse in either grammar).
I23 is split so the universal conditions, which every scenario checks, are a task of their own.

| Item | Capabilities (live lines) | b118's faults in this share |
|---|---|---|
| I21 | design-model-check (47) | r36 two rules; r44, r52 state only in the group title; r58-r61, r63, r65, r70 "naming the term" with no term; r11, r19 naming retired things; the 47 meta lines name rules from b123's catalogue; the I1-I18 adjectives reworded (`nonexistent` as "a requirement id that no capability holds") |
| I22 | requests (44) | r16 downstream for sent; r8 adds nothing to r6; r18/r49 clash; r7 against its group title; r28 unhosted context not tied to the command; r45-r47 no error clause; six refusals without change nothing (now short refusals) |
| I23a | analysis-tools (33), trials (5) | analysis r17, r20, r33 thin; r26 restates r25; r6's positive half; trials r2 keeps its verb |
| I23b | universal (5), `spec/universal.md`'s own marker | U5 and U7 name retired things (U7: "A worker shall change only files in its worktree" needs its worker); U8 to an option in the trigger; vocab.py's U4, U8 and U11 checks after each scenario kept passing |
| I24 | migration-tools (23), telemetry (4), batch-measurement (5) | migration-tools r13, r16, r24 several rules in a line; r13, r20 thin; r13-r16, r24, r25 "the repository" (now an indexical); telemetry r1 `measure` as include's subject; versions compared (call 9) |
| I25 | feature-file-tools (20), readiness (12) | f1, f17, f19 thin; r7 restates r6; r15/r16 clash under the If precedence (now stated); "exit with an error" in two senses (found something against refused: a finding is printed and the exit is 1, not a refusal) |
| I26 | backlog (21), batches (18) | backlog r20/r21 (the precedence stated, call 12); batches r1, r18 thin; batches r2, r6 Thens repeated from a verb's gloss |
| I27 | decision-tiers (9), pr-review (8), intake (4), conversation (4), brainstorming (3) | decision-tiers r8 entailed by r9, r7 the index committed too; pr-review r5, r7, r9 and brainstorming r3 wrong agent; pr-review r3 two rules; conversation r2 keep for store |

#### I28. The old pipeline removed

Removes codified-1 reading and its modules (section 9, "removed"). `v_p0` refuses a codified-1 file naming `migrate
upgrade`. `grammar/corpus/` keeps only grammar 4. Lines in grammar 4; today's draft:

design-model-check:

- **unrecodified** (adjective of capability): a capability whose file has `language: codified-1` in its frontmatter.
- If the person runs `model check` on a capability that is unrecodified, then `model` shall exit with an error naming
  `migrate upgrade`.

Grammar 4 form: "If the person runs `model check` on a capability whose language is `codified-1`, then `model` shall
refuse the command and name `migrate upgrade`."

#### I29. The upgrade step "the controlled language 4" and release 4.0.0

`migrate_upgrade_cnl4.py`, registered after "verb frames". It rewrites only what is mechanical: each file's marker to
codified-2, `imports: [cli]` into `spec/index.md` when any line uses a CLI word, `(verb)` to `(verb, action)` for a
verb used in no While clause and no relative clause (`(verb, state)` for one used only there). It reports, by file
and id: each line that no longer parses with the refusal's reason; each prose-defined condition and each line using
it; each line holding example data; each long-form refusal that can be shortened; each verb whose aspect it could not
decide; each blank-cardinality row on of/for/with/on/in that the old check read as functional; each term an imported
pack defines; each antecedentless "the"; each negated indefinite in a While clause. It rewords no requirement. README
4.0.0 section, `plugin.json`, `.shop/plugin-version`, migration-tools' version given blocks.

migration-tools, today's draft:

- **unpacked** (adjective of repository): a repository whose `.shop/plugin-version` names a release from 3.0.0 and
  before 4.0.0.
- While the repository is unpacked, when the person runs `migrate upgrade`, `migrate` shall rewrite `spec/index.md`
  and print "the controlled language 4" and "v_t14".
- While the repository is unpacked, when the person runs `migrate upgrade`, `migrate` shall rewrite every capability.

Grammar 4 form of the first: "While the release of the repository is after `3.0.0` and before `4.0.0`, when the
person runs `migrate upgrade`, `migrate` shall rewrite `spec/index.md` and print "the controlled language 4"."

#### I30. The authoring skills in 4.0

`skills/shaping-items`, `raising-a-request`, `taking-in-a-request`, `building-a-batch`: write states with structures,
not new adjectives; example data in the given block; states in While, not in the trigger's noun phrase (phase 3's
STATE-MOVE, 45 lines); short refusals; options in the trigger; packs and `Redefines:`; `model parse --form` and
`model explain` to check a line's meaning; `work line --retires` and `--recodify`. No requirement lines (the skills
have no capability), so carried as a plan (section 10 intro).

## 11. Build notes

- **Batches.** I0-I5 first (independent). Then I6, I7a, I7b, I8, I9, I10 in order. I11a-I18 after I9 as the table
  shows; I15, I16, I17 and I18 can share a batch. I14b as a plan once I14a has merged. I19, then I20 (a plan), then
  I21-I27 in one or two batches (independent), then I28, I29, and I30 (a plan).
- **Every item keeps `main` green**: old and new pipelines both pass their tests until I28. The per-file marker is
  what makes that possible (call 15).
- **The corpus is the oracle.** Each grammar item adds its sentences and refusals to a grammar 4 corpus that must
  parse, refuse and round-trip on every build.
- **Byte-stability.** `features generate` over an unchanged spec gives the same bytes after every item. Rewords
  change features only for their own capabilities.
- **No line is reworded silently.** I21-I27's reviewers diff each retired line against its successor's logical form
  (`model parse --form`) and the phase 3 candidate.

## 12. Left to the builder

- Every spelling not fixed above: GF category and fun names, the logical form's Python types, the exact entry syntax
  of aspects and senses as long as each fact is read from the entry and nowhere else.
- The numbering of new rule codes (`v_t14` ... are this design's working names) and their labels' wording.
- Where `grammar/rules.md` is written from (`model.lp` labels and the Python v_t codes), and how a decision "covers"
  a universal condition (I3).
- How much of the RGL to open (which constructors); overriding its defaults (call 1).
- The split of each new module to stay under 300 lines.
- Whether a defined condition used once is a warning or nothing (call 13), after seeing the counts on this
  repository.
- The witness wording of L7 and L8; `model explain`'s exact layout.
- Which phase 3 candidates to improve on: they are research material, not lines.
- Follow-ups to file as ideas when met, not built here: an HTTP pack; reading an upstream's pack across repositories;
  bins and the per-pair cache past 10k lines; predictive authoring.

## 13. The builder check (2026-11-10)

A fresh builder read this design against main's `scripts/`, `spec/` and `.shop/backlog/` and returned eleven
questions, none marked for the person. The person was offline and asked for 4.0 to be carried through, so each is
settled here as the session's call (or answered by the sources), and section 10 carries the result. The new and
changed lines were checked in shape with `python3 scripts/model parse`, an existing adjective standing in for each
new one (`renumbered` for a capability's, `unparsed` for a requirement's, `dirty` for a file's, `stale` of decisions
index for rule catalogue's).

1. **Retiring a line (MINOR, the session's call).** Nothing writes `retired:` today: `backlog_lines.py` and
   `backlog_forms.py` only read it, and `work line` only adds. A new item I0, `work line --retires <cap>#r<n>`, lays
   the new line and moves the old id into `retired:`, and taking it out puts it back. I21-I27 depend on it.
2. **Items with no line (MINOR, the session's call).** The readiness bar refuses an item with no requirement line
   (`scripts/readiness_bar.py:119`). I20, I30 and the new I14b are carried as plans under `.shop/records/`, one
   fresh agent and one fresh reviewer each, outside `work batch`.
3. **The grammar of a line in a mixed spec (MINOR, the session's call).** A line is parsed in its capability file's
   grammar. `model parse --capability <cap>` falls back to the index's marker when not given (I19). A reword item
   switches its file with `work line --recodify <cap>` (I19), so its grammar 4 lines are checked in grammar 4.
4. **The codified-2 world before I19 (MINOR, the session's call).** I7a adds the smallest codified-2 world (a
   `spec/index.md` with `language: codified-2` and `imports: [cli]`, and one capability); I10 and the items after
   it use it; I19 extends it to a mixed spec.
5. **I1's unreachable line (MINOR, the session's call).** With b120's soft pair, no scenario can build an
   unsatisfiable capability. The line is now about the soft case (`unpairable`: the pair set aside printed and the
   other L1 still found); the hard error is tested once in `tests/scripts/` with a `check.lp` made unsatisfiable on
   purpose.
6. **I2 against r54 (MINOR, the session's call; `stale` answered by the sources).** Plain `model rules` stays r54;
   `--write` writes `grammar/rules.md` and `--check` compares it. A second entry of `stale` is allowed: `malformed`
   has entries of four kinds in today's spec and `model check` passes. The same holds for `plural` and `compound`,
   which already exist for capability-proposal and requirement group.
7. **I14's noun and verb (MINOR, the session's call).** `features generate` runs on a capability and writes a feature
   file. "step" is not a kind of text, so `write` cannot take it; the line names the file instead: "When the person
   runs `features generate` on a capability that is declining, `features` shall not write a file that is
   overstated." I19's line says "print the feature file", as r17 does.
8. **One refusal path (MINOR, the session's call).** Five `Refused` classes exist today. The decision names
   `shop_files.Refused` as the shared base; the other four subclass it. One task, I14b.
9. **Item size (MINOR, the session's call).** I7, I11, I12, I13 and I14 are split in two (a and b); I23 is split so
   the universal conditions are their own task (I23b). I21 and I22 stay one task each: the per-file marker switches
   a file whole, and a file half reworded would parse in neither grammar; they are the two longer tasks.
10. **I13's numbers (MINOR, the session's call).** They are tested against a frozen copy of today's spec kept as a
    fixture, not the live spec.
11. **`nonexistent` (MINOR, the session's call).** Defined once, in I0 (readiness), as "a requirement named by an id
    that no capability holds as a live requirement", reused by I13b, and reworded by the rewords of the capabilities
    whose lines use it (I21, I25) as "a requirement id that no capability holds".

## 14. For the person to check

None of the builder's questions needed the person: each is settled from the sources or as the session's call
(section 13). Two calls are the most likely to be worth a look on return, most important first:

1. I21 (47 lines) and I22 (44 lines) are each one batch task, longer than the others, because a capability's file
   switches grammar whole (section 13 point 9).
2. I14b, I20 and I30 go outside `work batch`, as plans (section 13 point 2).
