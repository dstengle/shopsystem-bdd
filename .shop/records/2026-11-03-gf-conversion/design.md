---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-design
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion: the written design

Read with `brief.md` (the request, decisions 1-5, constraints) and the four surveys beside this file
(`survey-v4.md`, `survey-spike.md`, `survey-flow.md`, `survey-spec.md`). The domain model is
`.shop/records/2026-11-02-domain-model/domain-model.md` (DOM). The build plan is `plan.md`. Every call below was
taken under the person's delegation; a builder should not need to ask the person anything. Where this design leaves
a choice to the builder, §16 says so.

## 1. Intent, and why

Today a requirement is a free English sentence with an `[r<n>]` id. A regex (`model_parse.ears`) checks only its
outline. Such a sentence can be read two ways. The formulator reads one, the implementer another. Rounds then raise
spec questions, and the suite grows by hand. The conversion makes the requirement a sentence of a **controlled
language**:

- the bounded context's glossary is the **lexicon**, and every term has a category (DOM §0);
- **GF** parses every requirement and every request line against a grammar built from that lexicon. A line that does
  not parse is refused before any session reads it, and a line that parses has exactly one tree;
- **telingo/clingo** checks the logic of the parsed spec: groups that cannot happen, groups that contradict, resources
  and exclusivity, and the universal conditions on every trace;
- **Gherkin is generated** from the trees by a second grammar (Steps), with a fixed step vocabulary, so the formulate
  round becomes a script.

The graph of artifacts and work (v4's kinds, edges and Datalog rules) is static and already checked well by clingo,
so it stays. The conversion replaces only what a requirement says and how it becomes a scenario (survey-v4 §0).

## 2. Goals

1. G1. Every requirement of all 19 capabilities, and the universal conditions, is a codified statement that parses to
   one tree in the context's grammar. Each has a fresh id and a `restates` trace back to today's ids.
2. G2. `work request` refuses a line that does not parse in its upstream's grammar, and says why (the token and
   position GF reports).
3. G3. `model check` runs v5: the graph rules plus the parse rules. `model logic` runs the temporal check and names the
   requirements in conflict.
4. G4. `features generate` writes every service capability's feature file from its groups, deterministically.
   `features generate --check` fails when a feature file differs from what generate gives.
5. G5. Step definitions are written against a fixed vocabulary. Code is written once per term (a kind, an event, a
   command), not once per step text.
6. G6. `work run` takes a new request from intake through integrate, gate, apply and a scripted formulate, then drafts
   work-items and delivers them, with the parse and logic checks inside the flow.
7. G7. `tools install` installs GF 3.12, pgf 1.1, clingo 5.8.2 and telingo 2.1.3, and `tools probe` reports them.
8. G8. The suite is green, every tracked Python file is at most 300 lines, and every new concern has its own module
   and a row in CLAUDE.md.

## 3. Non-goals

- A grammar for languages other than English, and any use of the GF RGL (all lincats are records of `Str`).
- Parsing v4's G §6 sentence forms (the "reading form" of the model). They stay documentation (§5).
- Proving two different trees equivalent. Duplicates are found by equal normalised trees only.
- Several examples (Scenario Outlines) per group. One group gives one scenario. Its quantifier witnesses supply the
  boundary cases (§9.3).
- Carrying other repositories' free-English specs to codified lines automatically. `migrate upgrade` gives a scaffold
  and a report, and a session rewrites the lines (§13.5).
- Changing delivery: the pool, workers, merge, review, faults and done stay as they are.
- `main` is untouched, and no PR is opened.

## 4. Anti-goals: what this must not become

- **No escape hatch in the language.** There is no "free text" requirement and no `raw:` line. A thing the grammar
  cannot say is reworded, split, or left in prose under `## Not yet`, never smuggled in as a requirement.
- **No grammar function per sentence.** The spike's phrase-per-requirement funs (`TakeEvery`, `OneRoundAcross`) do not
  scale. The core grammar is compositional, and a new core fun needs a construct that recurs in at least two
  capabilities.
- **No hand edits to a generated feature file.** `features generate --check` and `model check` catch them, and
  `bdd-red-green` forbids them.
- **No step text typed in Python.** Patterns come from the Steps grammar, and code hangs off terms.
- **No session doing a mechanical job.** Parsing, the logic check, generation and the formulate round run as scripts.
- **No solver output scraped as text.** telingo and clingo are driven through their Python APIs.
- **No silent lexicon supplement** (the spike's `SUPPLEMENT`). A missing word is a refusal that names the word, and it
  is fixed by a glossary entry.

## 5. Constraints

As in the brief, plus:

- The plugin's scripts run under whatever `python3` launches them (3.11 here). pgf, clingo and telingo are imported
  lazily. If one is missing, the command exits 2 and names `tools install`, as `model_check.py` does for clingo
  today.
- GF is a native binary. It is needed only to compile a grammar, which happens when the lexicon changes. Parsing at
  run time uses the `pgf` wheel.
- Generation is deterministic: the same spec gives the same bytes, and editing one group changes only that group's
  scenario. Sorting is by id, and instance names and witnesses are chosen by fixed rules, never from a solver's model.

## 6. Decisions taken (brief §10, restated with what they mean here)

1. **Design model v5 is v4 fitted to the domain model**, not a rewrite. Where v4 and the live files disagree, the
   grammar tools decide. §7 lists every change from v4 with its reason.
2. **Kind names are `requirement` and `scenario`.** v5 says once that v4's `capability-requirement` and
   `acceptance-scenario` are these.
3. **Initiative transitions** are `work start` (proposed → started) and `work abandon` (started → abandoned), plus the
   condition *complete* (started → done).
4. **A fresh spec with fresh ids.** Each converted requirement and group gets a new id. Today's ids survive only in
   the group's `Restates:` line, written `r<n>@0.29` so they cannot be confused with the new ids. From the converted
   spec on, a changed requirement is retired and replaced under a new id; it is never edited.
5. **Universal conditions** get ids `U<n>` in `spec/universal.md`. They are checked on every trace and never restated
   in a requirement.

Further calls this design makes (all under the delegation):

6. **Requirements keep `r<n>` and groups take `g<n>`**, both numbered within their capability. A scenario is tagged
   with its group id and with every member requirement's id (`@g3 @r7 @r8`). `accepts:` may name requirements or
   groups (a group means its members), so `work_items.py`, `supervise_draft.py`, `accepted_scenarios` and
   `work resolve` keep working on `<cap>#r<n>` (survey-flow §3).
7. **The capability `.md` file keeps its layout.** The Behaviour section holds groups (§10), so `supervise_drafts`,
   `supervise_change`, the proposal machinery and `migrate_*` keep reading the same files.
8. **The glossary is the union** of `spec/index.md`'s `## Glossary` and the `## Terms` section of each capability
   file, in one entry form. Terms can then sit next to their use, and capability conversions can run in parallel
   without editing one shared file. A glossary-proposal adds to `spec/index.md` unless it names a capability.
9. **The temporal check is its own subcommand** (`model logic`). `model check` stays static plain clingo and fast, and
   only reads parse facts (`v_p1`, `v_p2`).
10. **Formulate is a script step**, with no session. The `approved → formulated` transition and the serial spec lock
    stay.
11. **Generated feature files carry no `@deprecated` scenarios.** A removed group's scenario disappears with it, and
    git keeps the old one. The retire work-item comes from the proposal's `removes` list, not from `Deprecated for:`
    lines.
12. **Guarantees capabilities get no feature file.** Their requirements parse and are logic-checked, and measurement
    or trials check them. Today's `spec-consistency` and `spec-integration` feature files go. Any of their
    requirements about a script move to that script's service capability.
13. **The plugin goes to version 1.0.0.** The conversion is one `migrate upgrade` step.

## 7. Design model v5

v5 replaces `docs/design-model/design-model.md` and `grammar.md` in place. `README.md` says v5 and that `model check`
checks v5, and `spec/index.md`'s Constraints say v5. `how-we-got-here.md` gains a v4 → v5 section. v5 holds two
languages and says so in its first section:

- **the graph**: kinds, edges and rules over frontmatter facts, checked by `model check` (clingo, `scripts/model.lp`);
- **the requirement language**: the GF grammars and the lexicon, plus the temporal check (`model logic`, telingo).

The two are joined by the facts `parsed(Q)`, `unparsed(Q,Why)`, `ambiguous(Q)`, `member_of(Q,G)`, `in(G,C)`,
`generates(G,S)` and `restates(G,Old)`.

### 7.1 Changes from v4, each with its reason

| # | change | reason |
|---|---|---|
| C1 | `capability-requirement` → **requirement**, `acceptance-scenario` → **scenario** | decision 2; the glossary forbids "capability requirement" |
| C2 | A requirement is "one statement that parses to one tree in the requirement grammar", not "one EARS statement" | the parse is now the check; it replaces the regex |
| C3 | New kind **requirement group** `<cap>#g<n>`, with a title and `restates` | DOM §2.1: one group is one scenario; statements share a pre-state and a trigger |
| C4 | A scenario is **generated**: one per group, title = group title, tags `@g<n>` plus the members' `@r<n>`; "title free to change" goes | a scenario is a linearisation of its group, so it cannot say more than the group |
| C5 | `has_req(C,Q)` → `member_of(Q,G)` + `in(G,C)` (`has_req` is derived) | requirements sit inside groups |
| C6 | `has_sc(Q,S)` → `generates(G,S)`, 1..1, written by the generator | a scenario tests a group (DOM §4) |
| C7 | New standing kind **universal condition** `U<n>`, in `spec/universal.md` | decision 5 |
| C8 | **term** is promoted to a kind and has a **category**: actor, kind, attribute, value, relation, event, resource, condition | DOM §0; the category is the grammar slot |
| C9 | New kinds **step** and **feature** (generated). Step code stays outside the model | DOM §2.1 |
| C10 | **proposal** becomes a supertype with the sorts capability-proposal and glossary-proposal | DOM §2.2; the live code already has glossary-proposals |
| C11 | capability-proposal lifecycle: `drafted, awaiting-answer, approved, formulated, withdrawn`; `merged` goes | DOM §3; no line uses `merged` |
| C12 | `formulated` means "its groups' scenarios are generated and committed" | formulate is a script (decision 10) |
| C13 | work-item: `awaiting-ruling` → `awaiting-answer`, plus `failed` (U6), `work retry` and `withdrawn` | matches the live code and DOM §3 |
| C14 | The design-decision lifecycle is added: `proposed, accepted, rejected, superseded` | DOM §3; v4 had none |
| C15 | The initiative lifecycle names its events: `work start`, `work abandon`, *complete* | decision 3 |
| C16 | `argues`: exactly one capability for a capability-proposal; a glossary-proposal argues the glossary | live rule v_k6 and DOM §4; v4 said 1..n |
| C17 | `accepts(W,X)`: X is a requirement or a group (a group means its members) | the live code and DOM say requirement; groups are the scenario unit (decision 6) |
| C18 | `changes` applies only to groups (title, membership) and terms. A changed requirement is `removes` old + `adds` new | "retire, never edit" (decision 4) |
| C19 | `resolution(Q,R)` has no version | the live code dropped it; ids are never reused, so the version adds nothing |
| C20 | A request line is "a line that parses in the upstream's grammar", not "strict EARS" | G2 |
| C21 | Record kinds `design` and `analysis` are added (history) | the live `model check` rejects `kind: design` on these very records |
| C22 | `cross-context-request` goes, with v1, v7/v7b (LP's), v_b2, v_k1, v_k2 and the `needs/from_cap/across` inputs | retired in v4, still in the live code |
| C23 | job-thread is a root, not a part | v4 says root; the live code still treats it as a v3 part |
| C24 | Rule codes get one meaning each (§7.2) | grammar.md and `model.lp` reuse six codes for different rules |
| C25 | v_e1/v_e2 (the regex check) → **v_p1** (does not parse), **v_p2** (more than one tree) | C2 |
| C26 | New id rules **v15g** (group id form and uniqueness), **v15h** (`U<n>` form and uniqueness), **v15i** (an id is never reused: it is neither live nor in `retired:`), **v15j** (a `Restates:` id existed in 0.29 per `spec/restated.json`) | fresh ids, decision 4 |
| C27 | New term rules **v_t4** (a term has a category), **v_t5** (a value names exactly one attribute of one kind), **v_t6** (no two terms linearise the same). v_t1 now checks prose sections only | categories make the lexicon well-typed; a parsed line can only use lexicon words |
| C28 | v_s1–v_s3 and v15f work on groups: a scenario names no group; a group has no scenario (and is not logic-only); a requirement is in no group or in two | C4, C6 |
| C29 | The temporal checks L1–L4 (§12) live in `model logic`, outside `model.lp` | decision 9 |
| C30 | G §6 sentence forms stay as a non-normative reading form; `LINE = EARS` and "formulated as" go | no parser was ever written for them; the requirement grammar is the GF grammar |
| C31 | v4's layout section is fitted to the live layout: `spec/decisions/`, `.shop/work`, `.shop/records`, plus `spec/universal.md`, `spec/restated.json`, `grammar/` (the plugin's core grammars) and the grammar cache (§11.3) | live files |
| C32 | `under(W,C)` stays work-item → capability. DOM's reading (work-item → proposal) is `part_of` | v4 and the live code agree |

### 7.2 Rule codes with one meaning each

| code | v5 meaning | what happens to the other meaning |
|---|---|---|
| v3 | a resolution names a requirement (never a scenario), and the spec has it | LP's and G's clauses merge into one rule |
| v7 | asker and upstream sit across a seam (G's) | LP's (a cross-context-request names no capability) goes with C22 |
| v18a–c, v18d | part_of/blocked_by/for across contexts (G's); v18d: a foreign work id (LP's) | |
| v_d2 | a job-thread built with an undelivered request (G's) | LP's (an abandoned initiative with an open part) becomes **v_d5** |
| w_many_requests | open requests per upstream (G's) | LP's per-seam count goes |
| w_stale_intake | an accepted request with no initiative after 90 days (G's) | LP's (an initiative `proposed` for over 90 days) becomes **w_stale_proposed** |

Every other v4 rule keeps its code and meaning (survey-v4 §3). v16a's date cutoff goes: the conversion compacts old
initiatives anyway.

## 8. The requirement language

### 8.1 Patterns (EARS)

All six EARS forms, with the clauses in a fixed order. `Actor` is a lexicon actor, and `Resp` is
`shall` (or `shall not`) followed by a verb phrase:

| form | shape | logic | Gherkin |
|---|---|---|---|
| ubiquitous | `Actor shall V.` | `always` | a property: Givens from the witness, Then; no When |
| event-driven | `When T, Actor shall V.` | T at step k → V at step k+1 | When T, Then V |
| state-driven | `While C, Actor shall V.` | `always`: C → V | Given C, Then V |
| optional feature | `Where F, Actor shall V.` | F as a fact of the context → V | Given F |
| unwanted behaviour | `If T, then Actor shall V.` | as event-driven, T an unwanted input | Given/When with the invalid input, Then V |
| complex | `[Where F,] [While C,] When/If T, Actor shall V.` | the conjunction | in clause order |

One sentence and one `shall` per requirement. A list response ("shall print X and Y") is one VP with a coordinated
object, which the grammar allows. Two verbs are two requirements in one group.

### 8.2 Groups as scenarios

A group is the set of requirements that make one scenario: they share a pre-state (Where/While) and a trigger
(When/If), which are written in full in each statement. `model check` checks that all statements of a group share the
same trigger tree and condition tree (**v15k**, normalised; ubiquitous groups are exempt). A group has a title (free
English, not parsed, used as the scenario title) and an optional `given` example block (§10).

### 8.3 Restates

`Restates: r66@0.29, r95@0.29` lists the 0.29 ids the group replaces. A bare `r<n>@0.29` is an id of the group's own
capability; an id of another capability is written `<cap>#r<n>@0.29` (`Restates: formulation#r5@0.29`). It is a source
only: these ids are not nodes. `spec/restated.json`, frozen from commit 96818f71, is keyed `<cap>#r<n>` (0.29 ids repeat
across capabilities) and maps each to `{"text": …, "line": …}`. It is used by v15j, by `model why` (it shows the old
text) and by `model restates` (§15), the coverage check: every 0.29 id is restated by a group, or listed under the
capability's own `## Dropped` section (§10.2) with its reason, or listed there as `moved to <cap>`, in which case a
group of `<cap>` must restate it once `<cap>` is codified. The capability that loses a line records the move; the
capability that gains it writes the group. Each package touches only its own capability files.

### 8.4 Universal conditions

`spec/universal.md` holds `- [U<n>] <statement>`, each a ubiquitous or `Where` requirement in the same grammar. U1–U10
are DOM §7's, worded to parse. They are translated into `#program always` constraints added to every check's
background (§12), and they are never restated. Where a U is observable in a test (U3 refuse: exit non-zero and no
change; U8 `--json` prints one object), the conftest checks it after every scenario that makes the U's trigger true.
That check is a hook in `tests/scenarios/conftest.py`, not a step.

### 8.5 Resources

Resources are lexicon terms of category `resource`, marked `exclusive` or `counted by <code>` (DOM §6). The grammar
has `holds` and `is free`. "Exclusivity" is never written as "one at a time, except": a stage's need for a resource
is a requirement (`When `work run` starts an integrate round, the round shall hold the spec lock.`), and U2 does the
rest. The background theory (§12.2) turns these into the constraints `resources.lp` showed.

## 9. The grammar

### 9.1 Files

- `grammar/Req.gf`, `grammar/ReqEng.gf`: the core requirement grammar (abstract and English), hand-written,
  plugin-owned. It extends the generated `Lex` and `Typed` modules.
- `grammar/Steps.gf`, `grammar/StepsEng.gf`: the core step grammar, hand-written, extending the same `Lex` and `Typed`.
- The spike's grammar sources are `.shop/scratch/spike-cnl/gf-src/*.gf` (`gf/` there is the unpacked GF install). They
  are a reference only, and nothing is copied from them unchanged.
- `grammar/corpus/*.txt`: sentences that must parse with exactly one tree (one file per capability, sampled during
  the grammar's build), and `grammar/corpus/refused.txt`: sentences that must be refused.
- Generated for each context into the cache (§11.3), never tracked: `Lex.gf`/`LexEng.gf` (words) and
  `Typed.gf`/`TypedEng.gf` (typed slots for each kind and attribute, see below).

### 9.2 Core (abstract), the shape a builder starts from

```
cat Req; Clause; Feat; Cond; Trig; Resp; VP; NP; Code; Quoted; Num; Conds; NPs;
fun
  Ubiq : Resp -> Req;  When : Trig -> Resp -> Req;  While : Cond -> Resp -> Req;
  Where : Feat -> Resp -> Req;  IfThen : Trig -> Resp -> Req;
  WhileWhen : Cond -> Trig -> Resp -> Req;  WhereWhen, WhereWhile, WhileIf : ...;
  Shall, ShallNot : Actor -> VP -> Resp;
  -- triggers and conditions that are not tied to a kind
  Runs : Actor -> Code -> Trig;            -- the person runs `work start`
  RunsOn : Actor -> Code -> NP -> Trig;    -- the person runs `work start` on an initiative that is …
  Happens : Actor -> Event -> NP -> Trig;  -- a session ends a stage
  Holds : NP -> Resource -> Cond;  IsFree : Resource -> Cond;
  And2 : Cond -> Cond -> Cond;  NotC : Cond -> Cond;
  -- verb phrases
  Do : Event -> NP -> VP;  DoTo : Event -> NP -> NP -> VP;
  Print : NPs -> VP;  PrintCode : Code -> VP;  Write : NP -> VP;
  Refuse : NP -> VP;  ExitOk : VP;  ExitErr : NP -> VP;  Commit : NP -> VP;
  Hold : Resource -> VP;  HoldAtMost : Num -> Resource -> VP;
  -- noun phrases not tied to a kind
  CodeNP : Code -> NP;  QuotedNP : Quoted -> NP;  NumberOf : NP -> NP;  ItNP : NP;
  OneNP : NP -> NPs;  MoreNP : NP -> NPs -> NPs;
  CodeLit : String -> Code;  QuotedLit : String -> Quoted;  NumLit : Int -> Num;
```

`Typed.gf` is generated from templates, one block per kind `K`, per attribute `A` of `K`, and per relation
`R : K1 → K2`. It is what makes "an initiative that is `drafted`" fail to parse (a work-item status in an initiative
slot), the property the spike's `--reject` showed, without dependent types (the pgf C runtime does not check them):

```
cat K_CN; K_NP; K_A;                          -- K_A: the closed values of attribute A of K
fun K : K_CN;  K_Every, K_An, K_The, K_AtMostOne : K_CN -> K_NP;  K_Named : Code -> K_NP;
    K_ThatIs_A : K_CN -> K_A -> K_CN;  K_WhoseNot_A : K_CN -> K_As -> K_CN;   -- value lists, no repeats
    K_Cond_c : K_CN -> K_CN;                  -- named condition c of K: "an open initiative"
    K_Is_A : K_NP -> K_A -> Cond;  K_Becomes_A : K_NP -> K_A -> Trig;  K_Set_A : K_NP -> K_A -> VP;
    K_IsC_c : K_NP -> Cond;                   -- "the initiative is complete"
    R_K1_K2 : K1_CN -> K2_NP -> K1_CN;        -- "a work-item under p1"
    K_toNP : K_NP -> NP;                      -- into the untyped slots (print, write, refuse …)
```

`ReqEng` uses records (`{s : Str; n : Number}` for NPs, `{inf, s3, part : Str}` for events) only where agreement
needs them. There is no RGL.

### 9.3 Over-generation guards

GF's types alone accept repeated list members and "it" with no antecedent (survey-spike §3). `spec_grammar.parse`
runs a post-parse check on the tree: a value list has no repeats, `ItNP` appears only after an NP in the same
sentence, `AtMostOne` takes no plural, and the literal rules of §9.4 hold. A tree that fails the check is dropped. When
no tree is left, the line is refused like a parse failure, with the reason.

### 9.4 Tokenising

`spec_grammar.tokenise` does what the author should not have to: it splits off punctuation, keeps a backticked span as
one token (backticks included), keeps a double-quoted string as one token (quotes included), and keeps numbers. GF lins
write multi-word backticked terms as one string token, as the spike does. pgf's `String` literal matches any token, so a
backticked lexicon word (`` `drafted` ``) also parses as `CodeLit`. The post-parse guard (§9.3) settles it before trees
are counted: it drops a tree whose `CodeLit` holds a token that is a lexicon word, or a token without backticks, and a
tree whose `QuotedLit` holds a token without double quotes. A lexicon word therefore parses only as the word, and
ambiguity (v_p2) is counted after the guard. P2's corpus has lines with backticked lexicon words and with code literals,
each with exactly one tree.

### 9.6 Identifiers

`spec_lexicon.ident(term, category)` maps a term to a GF identifier: lower case, each run of characters outside
`[a-z0-9]` becomes `_`, prefixed by the category's letter (`k_work_item`, `a_work_run`), with collisions numbered in
sorted order. The lin keeps the term's own spelling (`` `work run` ``, `work-item`).

### 9.5 Growth rule

A core fun is added only for a construct that recurs in at least two capabilities. Otherwise the line is reworded.
Grammar changes are plugin changes. They are made in this repository, with a corpus line for each new fun, and never
by a proposal in a target project. A target project grows its language by glossary entries only.

## 10. The lexicon and the spec file format

### 10.1 A term entry

```
- **initiative** (kind): the delivery of one request's accepted lines. Plural: initiatives. Not: epic.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **open** (condition of initiative): Means: its status is not `done` and not `abandoned`.
- **under** (relation work-item → capability-proposal): a work-item delivers part of a proposal.
- **start** (event): Forms: starts, started.
- **spec lock** (resource, exclusive): held by every integrate, apply and formulate round.
- **worker slot** (resource, counted by `workers`): …
- **`work run`** (actor): the supervisor …
```

- There is one reader of terms: `spec_lexicon` (P2). `spec_lexicon.read(root)` scans `spec/index.md`'s `## Glossary`
  and every capability's `## Terms`, and `spec_lexicon.entry(bullet, where)` parses one entry. `spec_read` skips
  `## Terms` and has no terms field. Until P5 moves `model` onto `spec_lexicon`,
  the legacy `model_parse.glossary_entry` is widened (by P3) to accept the `(category …)` after the term, and it reads
  only the term and `Not:`.
- Category is required (v_t4). For `attribute`, `condition` and `relation`, the kinds come after `of` or as
  `K1 → K2`. A value belongs to exactly one (kind, attribute) (v_t5); the same word in two attributes is two values
  (`` `done` `` of initiative status, `` `done` `` of work-item status), which the typed slots keep apart.
- `Means:` of a condition must parse as a `Cond` of its kind. It becomes the condition's rule in the logic.
- `Transitions:` of an attribute give the background theory's transition facts (§12.2).
- `Forms:` and `Plural:` are needed only where English is irregular (the default is `+s`/`+ed`).
- `Not:` stays (avoided words, v_t1 on prose).

The glossary is converted from DOM §1–§8 (its terms, categories, values, transitions, resources and conditions) and
from today's 51 terms. DOM's record is the draft, and `spec/index.md` is the live source, which glossary-proposals
change.

### 10.2 The capability file

```
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/work-queue
title: Work queue
narrator: the person
group: service
language: codified-1        # this file's Behaviour is codified groups (§13.4)
rests_on: [...]
retired: []                 # r<n> and g<n> retired since 1.0.0
---

# Work queue

## Purpose
(prose, unchanged in kind)

## Terms
(term entries local to this capability, same form as the glossary)

## Behaviour

### [g1] `work start` starts a proposed initiative
Restates: r3@0.29, r4@0.29.
- [r1] When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`.
- [r2] When the person runs `work start` on an initiative that is `proposed`, `work` shall commit the transition.

```given
an initiative i1 that is `proposed`
```

## Implementation, may change
## Not yet
## Dropped
- r7@0.29: restated U3 (a refusal writes nothing).
- r12@0.29: moved to supervision.
```

- Requirement ids are numbered from r1 across the file, groups from g1. Numbers are never reused (v15i).
- The optional fenced `given` block holds Steps-grammar Given lines. These are example data the requirement does not
  carry (file contents, question texts). `features generate` parses them in Steps and puts them before the generated
  Givens. A line there that does not parse in Steps is v_p3.
- Multi-line data in a `given` block: a Steps line ending in `:` (template `GivenCodeText`, e.g.
  ``the file `spec/index.md` holds:``) takes the lines indented two spaces under it. Indented lines that start with `|`
  become the step's Gherkin data table, and any other indented lines become its docstring (`"""`). The generator writes
  them under the step, and the handler receives them as pytest-bdd's `docstring` or `datatable` argument.
- `## Dropped` (prose, not parsed) lists each 0.29 id that no group restates, with its reason or `moved to <cap>`. It
  is written once by the conversion and kept as the record of what was dropped.
- Tables of requirements (today's design-model-check rows) are gone: each row becomes a statement.
- `spec/universal.md` has frontmatter `id: .../universal`, `group: guarantees`, and a Behaviour list of `- [U<n>] …`
  with no groups.
- `docs/capability-format.md` is rewritten to this format: the EARS table of §8.1, groups, ids, terms, the `given`
  block, and the lessons of "lines that leave nothing to infer" that still apply.

## 11. The toolchain

### 11.1 What is installed, and where

| tool | version | how | where |
|---|---|---|---|
| GF | 3.12 | download `https://github.com/GrammaticalFramework/gf-core/releases/download/release-3.12/gf-3.12-ubuntu-24.04.deb`, check sha256 `17aa5452b713f1e00a0755a1bad998a926acbffb96eefde2c3800ca72536b4d8`, unpack with `dpkg-deb -x` (required: there is no other unpacker; without it `tools install` exits 1 naming `dpkg-deb` and `$SHOPSYSTEM_GF`), write a `bin/gf` wrapper that sets `LD_LIBRARY_PATH` | `${XDG_DATA_HOME:-~/.local/share}/shopsystem-bdd/gf-3.12/` |
| pgf | 1.1 | pip wheel (it bundles libpgf) | the interpreter that runs the plugin's scripts |
| clingo | 5.8.2 | pip wheel | same |
| telingo | 2.1.3 | pip wheel | same |

### 11.2 `tools install` and `tools probe`

- `tools_env.py` keeps the project-interpreter tools (ruff, vulture …). `RUFF_PIN` becomes `PINS = {name: version}`.
- A new `scripts/tools_grammar.py` owns the **grammar tools**: the pinned wheels and GF. `tools install` installs them
  every time, alongside the analysis tools. The wheels go into `sys.executable` (with `--user` outside a virtualenv;
  when pip refuses an externally managed interpreter, `tools install` exits 1 naming `--python`). GF goes to the path
  above and is checked by sha256. Running it again is a no-op. It prints one line per grammar tool: `gf 3.12
  downloaded` or `gf 3.12 already installed`, and `<wheel> <version> installed` or `<wheel> <version> already installed`.
- Supported platform: Linux x86_64 only (the only GF 3.12 binary build used, and pgf 1.1 has no linux-aarch64 wheel).
  Elsewhere `tools install` exits 1 saying the platform is unsupported and naming `$SHOPSYSTEM_GF` for a GF built by
  hand. This is a stated limit of the experimental branch, not a gap.
- `tools probe --json` is new: one JSON object with the analysis tools, the interpreter and a `grammar` block
  `{"gf": "3.12.0"|null, "pgf": "1.1"|null, "clingo": …, "telingo": …}`.
- `tools probe` gains a `grammar` block: the gf version (from `gf --version`), pgf, clingo and telingo, each present or
  missing, and what the workflow cannot do without it ("requirements cannot be parsed: `work request` and
  `model check` refuse").
- GF is found by `spec_grammar.gf_binary()` in this order: `$SHOPSYSTEM_GF`, the install path above, then `gf` on PATH
  if `gf --version` says "Grammatical Framework". The PATH lookup is `shutil.which` run without a shell, so the zsh
  `gf` git alias never interferes.

### 11.3 Compile and cache

`spec_grammar.load(root, grammar)` (grammar is `"Req"` or `"Steps"`):

1. reads the lexicon (`spec_lexicon.read(root)`);
2. generates `Lex*.gf` and `Typed*.gf`;
3. takes the sha256 of those plus the core `grammar/*.gf`;
4. looks in `${XDG_CACHE_HOME:-~/.cache}/shopsystem-bdd/pgf/<sha>/<grammar>.pgf`. On a miss it runs
   `gf -make --output-dir=<dir>` once per concrete grammar (one call per grammar: the spike found that one call
   writes only one PGF);
5. returns a `pgf.PGF`.

A compile writes into a fresh `tempfile.mkdtemp(dir=<cache>/pgf)` and then `os.rename`s it to `<sha>`. If the rename
finds `<sha>` already there (another pytest-xdist worker or worktree won the race), the temporary directory is removed
and the existing one used. Tests that share a glossary share the cache.

An upstream's grammar (G2) needs no lookup. `work request` runs in the upstream's repository: it writes
`.shop/work/requests/q<n>.md` under the `root` it is given. `supervise_raise` already resolves that root from
`## Upstreams` (`upstream_root`), so the grammar is `spec_grammar.load(root)`. The lines are parsed with `Req` when
`root`'s `spec/index.md` is codified (§13.4), and with the legacy shape check otherwise.

The suite needs the grammar tools. `tests/toolchain.py` (P2) gives `require()`, which every fixture that compiles or
parses calls. When GF, pgf, clingo or telingo is missing, it fails the test (never skips it) with one message naming
`python3 scripts/tools install`.

## 12. The logic check (`model logic`)

### 12.1 Translation

`scripts/spec_logic.py` has one translation per abstract fun (core and typed templates), not per requirement. A tree
becomes a telingo program part:

- typed slots → state atoms `kind(X,K)`, `attr(X,A,V)`, `rel(R,X,Y)`; a quantified NP → a fresh variable bound by its
  kind atom;
- triggers → event atoms at a step, `ev(Actor,Event,Args)`; `Runs` → `ev(Actor,run,Code)`;
- responses: `Set` → `attr(X,A,V)` at the next step; `Hold` → `holds(S,R)`; `Do`/`Print`/`Write`/`Refuse`/`Exit` →
  observable atoms `does(Actor,Event,Obj)`. These are free, so they conflict only with a `shall not` or with an
  exclusive resource or a count;
- When T, A shall V → `#program dynamic.  :- 'T, not V.` (the response at the next step); While C → `#program always.
  :- C, not V.`; `shall not` → `:- C, V.`;
- each requirement's constraint is guarded by an assumption atom `on(r<n>)`, so an unsatisfiable core names
  requirements.

### 12.2 Background theory

`grammar/background.lp` is fixed and plugin-owned: frame axioms (a state atom persists unless an event changes it),
"at most one value per (thing, attribute)", the resource rules of the spike's `resources.lp` (two running sessions
never hold the same exclusive resource; a counted resource never exceeds its number), and "a status changes only along
a transition". The context's facts (kinds, values, transitions, resources) are generated from the lexicon. The
universal conditions are translated like requirements and guarded by `on(U<n>)`.

### 12.3 Checks

For each group G, solve: background + all requirements of the context and the U's (each guarded) + G's witness (its
Where/While true at step 0, its trigger at step 1, its responses due at step 2), over a `clingo.Control`.
`telingo.imain` takes no extra assumptions and no core callback, so `spec_solve` uses its own loop. It is a copy of
imain's grounding of `initial`/`always`/`dynamic` parts and of its `Theory.translate`, kept with telingo's MIT notice.
It grounds states 0..H once (H = 3, the horizon), fixes `__final(H)`, and calls `solve(assumptions=future ∪ on-atoms,
on_core=…)`. The background allows a step with no event (stutter), so a model at a shorter horizon extends to H, and
one solve at H decides L1.

- **L1** (unsatisfiable or contradictory): no model. The unsat core over the `on/1` assumptions names the requirements
  and U's involved: `g5 (r12, r13) cannot happen: conflicts with supervision#r40, U2`. This covers both the spike's
  "conflict" and a group that contradicts itself.
- **L2** (duplicate): two requirements with equal normalised trees (lists sorted, articles normalised). A warning that
  names both.
- **L3** (transition): a `Set` names a status change that no transition allows.
- **L4** (unreachable): a value in a group's pre-state (directly, or through a condition's `Means:`) cannot be reached
  in the attribute's transition graph from an initial value. An attribute's initial values are those that no
  transition enters. When every value is entered (a cycle), all values count as initial and L4 cannot fire for that
  attribute. This is a graph search, not a solve, and has no horizon. It is a warning.

`model logic [--json] [<capability>]` exits 0 when there are no L1/L3 findings and 1 otherwise. The integrate round's
check (§13.3) runs it on spec plus drafts. The cost is one small solve per group, about 300 solves, well under a minute.

## 13. The flow: request → intake → integrate/gate/apply → formulate → work-items → delivery

| step | today | under v5 | code |
|---|---|---|---|
| raise (`work request`) | regex `ears()` per line | each line parses in the upstream's `Req` grammar, or the request is refused naming the line, the token and the position | `workqueue_request.py:143-145` → `spec_grammar.parse` |
| raise from an integrate round | `supervise_raise` → `request()` | unchanged code; the brief says "codified, parsing in the upstream's grammar" | `supervise_brief.py` wording |
| intake | session judges English lines | unchanged session; the brief gives each line beside its normal form (its tree linearised) | `supervise_intake.py` (small) |
| start | `work start` | unchanged | — |
| integrate | `capability-writer` writes English lines, and the round checks by hand | the writer drafts codified groups in the §10 format and terms in `## Terms` or a glossary-proposal. When the round's result comes back, `work run` itself parses every drafted requirement and runs `model logic` on spec + drafts. On a failure it sends the round back with the refusal text (the existing send-back, at most twice), then asks the person | `supervise_outputs.py` gains `uncodified()`; agent and skill rewritten |
| gate | person sees lines and questions | unchanged; the brief also shows each drafted group's generated scenario (`features generate --preview`) | `supervise_brief.py` |
| apply | session copies drafts, runs `model check` | unchanged; expects no new v_p/v_s rows | skill text |
| formulate | `feature-formulator` sessions hand-write Gherkin | **script, no session**: `features generate <cap>` for each capability of each approved proposal, then `features generate --check`, `model check` (no new rows), commit `features/`, proposal → `formulated`. It still runs under the spec lock and one at a time across initiatives | new `supervise_formulate.py`; `supervise_rounds.py` calls it for kind `formulate` |
| draft work-items | one per capability, `accepts` from the change list; retires from `Deprecated for:` | `accepts` from the change list (requirement ids). A retire work-item comes from the proposal's `removes`, with the check `python3 -m pytest` | `supervise_draft.py` |
| delivery | scout, planner, implementer, reviewers | unchanged. The implementer writes handlers for new vocabulary uses (§14) and never edits a feature | `bdd-red-green` one paragraph |
| hand-back ruling | "formulation question" goes to the formulator | a wrong generated scenario is a wrong requirement (back to integration) or a plugin defect (grammar or generator: a request to the plugin) | `bdd-red-green`, `initiative-round` |

### 13.1 What goes

- `agents/feature-formulator.md` is deleted.
- `agents/initiative-round.md`: the formulate kind is removed.
- `skills/formulating-features` is rewritten to about 40 lines: "run `features generate`; never write a scenario by
  hand; a wrong scenario means a wrong requirement or a plugin defect".
- The formulation-question paths are removed with their spec lines: `NOTHING_FORMULATED`, `formulated_nothing` and
  `sent_back` for formulate, and `route` back from formulate.

### 13.2 What changes

- `agents/capability-writer.md` (codified groups; it keeps no shell, since the round parses).
- `skills/integrating-a-proposal` (step 2 adds the parse and logic checks; step 4's expected rows).
- `skills/checking-spec-consistency` and `agents/spec-checker.md` shrink to what a parser cannot judge: whether a
  term's definition is clear, whether a response is observable by the narrator, whether a group leaves something to
  infer.
- `skills/bdd-red-green` (rulings).
- `skills/migrating-to-capabilities` (a note that it produces 0.29-format specs, followed by `migrate upgrade`).
- New `skills/raising-a-request/SKILL.md` (about 60 lines): it turns a person's English intent into codified lines.
  It covers the EARS table of §8.1, finding words with `model lexicon`, checking every line with
  `model parse --file <lines>` before `work request`, rewording from the refusal's hint, and, when a word is missing,
  a line asking for a glossary entry instead of a synonym. It is the help the brief's "lines written or checked as
  codified" needs: a session with this skill writes them, and `work request` checks them.

### 13.3 What stays

Request lifecycle, turns, `work outcome/ask/reply/turn/delegate/resolve`, initiatives, proposals, `supervise_change`,
`supervise_glossary`, `supervise_answers`, `supervise_all`, `supervise_done`, `supervise_analysis`, the pool,
worker, merge, review, faults, and the agents `code-scout`, `bdd-planner`, `bdd-implementer`, both reviewers,
`delegation-answerer`, `batch-analyst` and `trial-runner`.

### 13.4 The transition: codified and uncodified contexts

Codified is a property **of each file**, not of the context, because the conversion goes one capability at a time:

- a capability file (and `spec/universal.md`) is codified when its own frontmatter has `language: codified-1`. Its
  Behaviour is then read as groups. Otherwise it is read as 0.29 bullets by `model_legacy.py`;
- `spec/index.md` is codified when its frontmatter has `language: codified-1`. That means its glossary is in typed
  form (§10.1), so the context's grammar can be built. P3 sets it in layer 1. From P5 on, `work request` parses lines
  with `Req` when the upstream's index is codified, and keeps the 0.29 shape check (in `model_legacy.py`) otherwise.

`spec_read.codified(path)` answers for one file. Every reader (`model_spec`, `features_generate`, `model logic`,
`model restates`) dispatches per file. Unconverted capabilities therefore stay readable next to converted ones, and
each conversion package's checks pass in its own worktree.

`features generate`:
- `features generate <c>…`: exit 0 when written; exit 2 with `spec/capabilities/<c>.md is not codified: run
  \`migrate upgrade\`` when a named capability is not codified (nothing is written).
- `features generate --check [<c>…]` with no names checks every codified service capability, prints
  `skipped <c>: not codified` for each other service capability, and exits 0 when every checked file matches, 1 when
  one differs. A named uncodified capability gives exit 2, as above.

The release package (plan P14) deletes `model_legacy.py` and the uncodified paths. After that, a capability file or
index without the marker is refused by `model check` (rule **v_p0**), by `features generate` (exit 2), and by
`work request`, each naming `migrate upgrade`.

**Old references.** Work-items and requests written before 1.0.0 name 0.29 ids (`requests#r39`), and fresh numbering
reuses those numbers. The 1.0.0 upgrade step rewrites every `<cap>#r<n>` in `.shop/work/**` that predates the
conversion (every file in the repository at the commit `spec/restated.json` was frozen from) to `<cap>#r<n>@0.29`.
`model` resolves such a reference through `spec/restated.json` and never against the live spec. On this repository,
P14 runs `migrate upgrade` after the conversion. The step skips capability files that are already codified, so on a
converted repository it only writes the references and the plugin version.

## 14. Gherkin generation and the fixed step vocabulary

### 14.1 Steps grammar

The step grammar's core funs are templates over categories, one per DOM §0 "in Gherkin" cell:

| Steps template | text | from |
|---|---|---|
| GivenK_A | `a K i1 that is v` | a K slot with an attribute value, in a condition or a witness |
| GivenR | `the work-item w1 is under the capability-proposal p1` | a relation frame |
| GivenHolds | `the session s1 holds the spec lock` | Holds |
| GivenCode / GivenCodeText | `the file `x` holds "…"` / `the file `x` holds:` + indented block (from `given` blocks) | example data |
| WhenRuns | `the person runs `work start` on the initiative i1` / `the person runs `work list`` | Runs/RunsOn |
| WhenHappens | `a session ends the stage of the work-item w1` | Happens |
| WhenBecomes | `the work-item w1 becomes `ready`` | K_Becomes_A |
| ThenK_A | `the initiative i1 is `started`` | Set |

**Every instance is named with its kind word**: `a K i1` where it is introduced, and `the K i1` after that. Each typed
fun's text therefore carries a literal kind word. Its pytest-bdd pattern is unique to (template, kind), and the
handler key is read from the text, never inferred from the instance prefix. Within a kind, two attributes never share
a value word (v_t5 per kind), so a (template, kind) step resolves the attribute from the value through the lexicon.
| ThenDoes / ThenDoesNot | `` `work run` starts the research stage of w1 `` | Do (and shall not, and excluded witnesses) |
| ThenPrints | `` `work` prints … `` | Print/PrintCode |
| ThenExitsOk / ThenExitsErr | `` `work` exits successfully `` / `` exits with an error naming … `` | ExitOk/ExitErr/Refuse |
| ThenHolds | `the round holds the spec lock` | Hold |

`Typed.gf` instantiates them for each kind and attribute, so a typed Steps fun such as `GivenInitiative_status`
exists for each pair. That gives **the fixed step vocabulary**: a fixed set of about 15 templates, and as many typed
funs as the lexicon gives them.

### 14.2 Generation

`features_generate.py` maps each group to one scenario:

- **Instances.** The kind's first letter plus a number, in order of first mention (`i1`, `w1`, `p1`, `q1`), as
  today's tests already name them. A `Named` code keeps its code.
- **Witnesses.** These are chosen by fixed rules, not by the solver (the spike used telingo's model; that breaks
  determinism). `Every K whose A is not v1, v2` gives one instance with the first other value plus one instance per
  excluded value. Each included instance gets the Then; each excluded one gets ThenDoesNot. `K_An` gives one instance.
  A condition expands through its `Means:`. `If` uses the first value that falsifies the expected condition.
- **Order.** The `given` block, Givens (Where, While, witnesses), When (the trigger), Thens (one per requirement, in id
  order).
- **Logic-only groups.** A group whose statements are all ubiquitous `Hold`/`HoldAtMost`/resource statements has no
  Steps linearisation. It is logic-only: no scenario, `model_spec` emits `logic_only(G)`, and v_s3 exempts it. The one
  decision is `spec_tree.logic_only(trees) -> bool` (P2), which `model_spec` and `features_generate` both call.
- **File.** The header `# generated from spec/capabilities/<c>.md by features generate; do not edit`, then
  `Feature: <title>`, `Narrator: <narrator>`, then scenarios sorted by group number, each tagged `@g<n> @r…`.
- `features generate --check` regenerates in memory and diffs. `--preview <file>` generates from a draft file.

### 14.3 Step definitions

- `scripts/features_vocab.py` reads the Steps PGF. For each typed fun it linearises the fun with typed holes, giving a
  pytest-bdd `parsers.parse` pattern (`"an initiative {i} that is {v}"`), and builds a table of
  fun → (template, kind, attribute, pattern).
- `tests/scenarios/vocab.py` registers one pytest-bdd step for each (template, kind) row. The step dispatches to a
  **handler** looked up by (template, term): `@handler("GivenK_A", "initiative")`, `@handler("WhenRuns", "`work start`")`,
  `@handler("ThenPrints", "`work`")`. The handler gets the parsed, typed arguments and the shared `repo`/`context`/`run`
  fixtures. A handler for the bare template is the fallback (for example, every `WhenRuns` runs the command in the
  repo).
- Handlers live in `tests/scenarios/<cap>_handlers*.py`, one set per capability. `conftest.py` imports every
  `*_handlers*.py` by glob, so a conversion package adds handlers without editing `conftest.py`, `vocab.py` or
  `world_*.py`, which are frozen after layer 2. A handler that two capabilities need is written in each, or raised to
  the orchestrator, which moves it into `world_*.py` on `gf-conversion` between layers.
- `features vocab --check --tests tests/scenarios [<feature>…]` replaces `test_bound.py`'s file list. It fails when a
  scenario of the named feature files (all of them when none are named) uses a fun with no handler, or when two
  handlers claim one key.
- Marks: conftest registers `g<n>`/`r<n>` marks from the spec (no more `range(1,200)`), and `work_items.py` selects by
  them as today.
- The value of today's 13k lines is the bodies (world builders in `*_world.py`/`*_given*.py`, and assertions). They
  are kept and re-hung under handlers. The packed regex steps go.

## 15. The tools

| tool | change |
|---|---|
| `model` | `check` runs v5 (§7). New `parse <line>|--file F [--grammar Req|Steps]` (with `model`'s `--root`) prints the tree or the refusal, and on a refusal also the longest prefix that parsed and the lexicon words nearest the refused token (difflib), so a person or session can reword; `lexicon [--check]` lists terms by category and gives v_t4–v_t6 as a report; `logic` (§12); `restates [--json] [<cap>]` (§8.3): exit 0 when every 0.29 id of `<cap>` (all capabilities when none is named) is restated, dropped or moved, and every move into a codified capability is restated there (a move into an uncodified one is shown as pending, not a failure). `why` follows `restates` to the 0.29 text. `facts` emits the new facts. `decisions` is unchanged. The contract text in `scripts/model` is rewritten for v5 |
| `features` | New `generate [--check] [--preview F] [<cap>…]` and `vocab [--check] [--tests DIR]`. `count`, `list`, `bindings` and `deprecated` stay (they read Gherkin). `tag`, `move`, `deprecate`, `retire`, `rebind` and `verify-moved` are removed with their spec lines: the generator owns the files |
| `tools` | `install`/`probe` gain the grammar tools (§11.2). `map`, `tests-of`, `untested`, `refs`, `check`, `size` are unchanged |
| `measure` | Unchanged in code. A formulate round now has no session, so it shows no tokens. Its spec is converted like any other |
| `migrate` | New upgrade step `1.0.0 "codified requirements"` (`migrate_upgrade_codified.py`): it writes `spec/restated.json` from the repo's live ids, turns each capability's Behaviour into a scaffold (one group per old line, `Restates:` filled, the old text as an HTML comment, no requirement bullets), deletes `@deprecated` scenarios, and reports what is left for a session to write. The other migrate subcommands (old system → layout) stay and produce 0.29 format, followed by the upgrade |
| `work` | `work request` parses (§13). Its refusal carries `model parse`'s hint. `work show` of a request shows each line's parse status. Nothing else changes |

`model_parse.ears` and `behaviour_items`' table and lead-sentence reading go. `model_facts.py` (287 lines) splits:
reading capabilities, groups, U's and features moves to a new `model_spec.py`.

## 16. Converting today's spec and tests

### 16.1 Order and unit

One capability is one unit of conversion. Within it:

1. rewrite Behaviour as codified groups with fresh ids and `Restates:`, add `## Terms` for any new words, list the
   rest under `## Dropped`, and set `language: codified-1` in the file's frontmatter;
2. run `model parse --file`, `model check`, `model logic <cap>` and `model restates <cap>`, all clean;
3. for service capabilities, run `features generate <cap>`;
4. re-hang the step bodies as handlers and delete the old step modules and binder;
5. run `pytest tests/scenarios/test_<cap>.py` green.

A 0.29 line the grammar cannot say is reworded or split. If it still cannot be said, it goes to `## Not yet` as prose
and under the capability's `## Dropped` with the reason. Expect 800–1100 statements from the 581 lines, and about 300 groups.

### 16.2 Scale

- **Guarantees** (11 capabilities, 156 requirements: code-research 10, delivery 14, formulation 14, planning 8,
  red-green 13, review 20, role-boundaries 7, spec-consistency 18, spec-integration 26, spec-migration 21, trials 5):
  parse and logic only. Each formulation line is either dropped (no formulator) or listed `moved to supervision`, and
  P12 writes supervision groups restating it as `formulation#r<n>@0.29`. A spec-integration line about a script is
  listed `moved to <cap>`, where `<cap>` is the service capability that owns the script (design-model-check for
  `model`, feature-file-tools for `features`, supervision for `work run`). The package converting `<cap>` restates it.
- **Service, small** (analysis-tools, batch-measurement, feature-file-tools, migration-tools: 114 requirements).
- **Service, core** (work-queue, requests, design-model-check: 147 requirements; design-model-check is rewritten
  against v5 and its 39 table rows become statements).
- **Supervision** (164 requirements, 34 step modules) is last, after the flow changes, because its scenarios test the
  new formulate script and the integrate check.
- **Universal conditions**: U1–U10 in `spec/universal.md`. Lines that only restated a U are dropped and give it as the
  reason.

### 16.3 The baseline

The failing tests recorded in `baseline-failures.txt` before layer 1 are not carried over. The surveys counted 23
(22 scenarios with no step definitions and 1 unimplemented line); the recorded file is authoritative, not that count.
They are not carried over. Their
lines get fresh ids. A line that is implemented today is converted. An unimplemented one goes to `## Not yet` unless
the conversion package implements it.

## 17. Left to the builder

- The exact English of each core fun's linearisation, and the record fields of lincats.
- Which core funs beyond §9.2's sketch are needed. The corpus decides, under the growth rule (§9.5).
- How a handler module is split for each capability (the 300-line limit decides), and the naming of
  `tests/scenarios` modules.
- Whether `model logic`'s horizon of 3 needs to be raised for some group. If so, add a `--horizon` flag, not a
  per-group setting.
- The wording of each converted requirement, and the grouping of statements, within §8.
- Whether the post-scenario U checks cover more than U3 and U8.
- Whether `spec_grammar` keeps loaded PGFs in a per-process dict (it should, if parsing shows up in profiles).
- Failure text formats, as long as each refusal names the line, the token or rule, and the position or id.

## 18. Calls made in the check

`builder-check.md` raised 31 points. Each is settled here under the delegation. The design sections above carry the
settled text, and `plan.md` carries the ownership and check fixes. Numbers are the builder check's.

### Contradictions

1. **Codified per file, not per context.** Each capability file (and `spec/universal.md`) carries its own
   `language: codified-1`. Readers dispatch per file, and unconverted capabilities stay on `model_legacy.py` until
   the release. `spec/index.md`'s marker means only "the glossary is typed", is set by P3 in layer 1, and switches
   `work request` to parsing. The layer 3 gate no longer sees supervision's unparsed lines, because supervision is read
   by the legacy reader until P12 marks it (§13.4).
2. **Exit codes of `features generate`.** Naming an uncodified capability gives exit 2. `--check` with no names skips
   uncodified capabilities with a `skipped <c>: not codified` line and exits 0 or 1 on the files it checked. P7's live
   check (`--check`, no names, nothing codified) is therefore exit 0 (§13.4).
3. **Guarantees count** corrected to 156, per capability (§16.2). The total of 581 stands.
4. **Kind words in step text.** Every instance after its introduction is `the <kind> <name>`. ThenK_A gives
   ``the initiative i1 is `started` ``, WhenBecomes gives ``the work-item w1 becomes `ready` ``. A (template, kind)
   pattern is unique, and the attribute is resolved from the value by the lexicon (§14.1).
5. **Moved lines.** A cross-capability `Restates:` is written `<cap>#r<n>@0.29`. The losing capability lists the id
   under its own `## Dropped` as `moved to <cap>`, and the gaining capability's package writes the restating group.
   P9 lists formulation's lines as dropped or `moved to supervision`, and P12 restates them. spec-integration's
   script lines are moved to design-model-check (P11), feature-file-tools (P10) or supervision (P12) by the script
   they name. `model restates` checks it, and a move into a not-yet-codified capability is pending, not a failure
   (§8.3, §15, §16.2).

### Questions

6. **`restated.json`** is keyed `<cap>#r<n>` with `{text, line}`. A bare `r<n>@0.29` is read in the group's own
   capability (§8.3).
7. **One reader of terms:** `spec_lexicon` (P2) scans the Glossary and Terms sections and parses entries.
   `spec_read` has no terms field. P3 widens only the
   legacy `model_parse.glossary_entry` so `model check` keeps reading the typed glossary until P5 (§10.1).
8. **`logic_only`** is one function, `spec_tree.logic_only(trees)` (P2). P5 and P7 call it (§14.2).
9. **Upstream grammar:** no lookup. `work request` runs with the upstream's repository as `root` (it writes
   `.shop/work/requests/` there), and `supervise_raise.upstream_root` already resolves that root from `## Upstreams`
   (§11.3).
10. **telingo:** `spec_solve` copies imain's grounding loop (with telingo's MIT notice) to pass the `on/1`
    assumptions and `on_core`. It does one solve at the fixed horizon H = 3 (states 0..3). The witness puts the trigger
    at step 1 and the responses at step 2, and stutter steps make a shorter model extend to H. L1 means "unsat at H"
    (§12.3).
11. **L4** is a graph search over each attribute's transitions from its initial values (those no transition enters).
    It needs no solver and no horizon, and fires on a pre-state value that no path reaches (§12.3).
12. **Backticked lexicon words.** The guard drops a tree whose `CodeLit` holds a lexicon word or an unbackticked token,
    and a `QuotedLit` on an unquoted token, before trees are counted. P2's corpus covers it (§9.3, §9.4).
13. **Multi-line `given` data.** A Steps line ending in `:` takes the lines indented under it: lines starting with `|`
    are a data table, and any other lines are a docstring (§10.2).
14. **English requests.** A new skill `raising-a-request` (P8) guides a session from English to codified lines with
    `model lexicon` and `model parse`. `model parse` and `work request` refusals give the longest parsed prefix and the
    nearest lexicon words (§13.2, §15).

### Gaps in ownership (fixed in plan.md)

15. P8 owns `scripts/supervise_worker.py`, `skills/delivering-an-initiative/`, `skills/migrating-to-capabilities/`
    and `tests/scripts/test_agents.py`. Its grep covers `agents skills scripts tests`. README.md is the release's
    (P14), whose check greps it.
16. P10 owns `scripts/features` (in layer 3), `features_edit.py`, `features_bindings.py`, `features_report.py`,
    `test_features.py`, `test_features_deprecating.py` and `test_features_scenarios.py`.
17. `conftest.py`, `vocab.py` and `world_*.py` are P7's in layer 2 and frozen after it. Handlers go in
    `<cap>_handlers*.py`, which conftest imports by glob. A shared change goes through the orchestrator between layers
    (§14.3).
18. Legacy removal moves to its own release package, P14 (layer 5). P14 owns `model.lp`, `model_check.py`,
    `model_spec.py`, `model_parse.py`, `model_legacy.py`, `workqueue_request.py`, `features_generate.py` and
    `spec_read.py`, so v_p0 and the deletions are within its files. The upgrade step stays in layer 4 as P13.
19. P1's Goal includes `tools probe --json` (§11.2).
20. Test ownership names real files. P1 owns `test_tools.py`, P3 owns `test_model_glossary.py`, P4 owns
    `test_model.py`, `test_model_reading.py`, `test_model_output.py` and `test_model_withdrawn.py` in layer 1, and P5
    owns those plus `test_model_glossary.py` and `test_workqueue_request_asker.py` in layer 2. P8 owns
    `test_supervise_outputs.py`, `test_work_items.py`, `test_work_items_worker.py` and a new `test_supervise_draft.py`.
    P9 owns `features/spec-consistency.feature`, which has no step module or test file (its 16 scenarios are unbound
    today) and is deleted.
21. The spike's sources are in `.shop/scratch/spike-cnl/gf-src/`. `gf/` is the GF install (§9.1).
22. A smoke test `tests/scripts/test_tools_codified_smoke.py` (P14) runs `measure show` on a kept measurement,
    `tools map --json`, `tools tests-of`, `tools untested --json`, and `features count`, `list` and `bindings` on the
    live converted repo. Each must exit 0 with non-empty output. It is in the layer 5 gate.

### Checks rewritten (in plan.md)

23. P4 uses `! python3 scripts/model check 2>&1 | grep -q "kind 'design'"` and real test files.
24. P8 creates `tests/scripts/test_supervise_draft.py`.
25. P3 runs two greps.
26. `features vocab --check` takes feature files as arguments (P7), and P10 names its four.
27. P1 checks the `already installed` lines and the absence of `downloaded`.
28. The live run stays evidence (P16), not a gate.
29. The baseline is whatever `baseline-failures.txt` records before layer 1. The plan also records
    `baseline-model-check.txt` for P3's no-new-rows check.

### Toolchain

30. Confirmed facts, kept.
31. Settled risks:
    - **No fallback unpacker.** `dpkg-deb` is required, and `zstandard` is not used (§11.1).
    - **Platforms.** Linux x86_64 only, a stated limit. Elsewhere `tools install` exits 1 naming `$SHOPSYSTEM_GF`
      (§11.2).
    - **The zsh `gf` alias.** PATH lookup uses `shutil.which` with no shell (§11.2).
    - **Cache race.** Compiles go to a temporary directory and are renamed into place, and the loser of a race discards
      its copy (§11.3).
    - **Tests need GF.** `tests/toolchain.py` `require()` fails loudly, naming `tools install`, and never skips
      (§11.3).
    - **Grammar size.** P2 records cold compile time and the number of corpus lines with more than one tree before the
      guard in `p2-grammar.md`. The layer 3 gate requires a cold compile of the live grammar to take under 180 s.
      Above that, the orchestrator splits `Typed` per kind before layer 4.
    - **Term names.** `spec_lexicon.ident` maps them to identifiers (§9.6).

### Found while settling

- **Old references.** Fresh ids reuse 0.29 numbers that old work-items and requests name. The 1.0.0 upgrade step
  rewrites those references to `<cap>#r<n>@0.29`, and `model` resolves them through `restated.json`. P14 runs the
  step on this repository (§13.4).
- **Layers.** Splitting the release out (point 18) gives six layers: P13 (upgrade step) runs beside P12 in layer 4,
  P14 (release and legacy removal) is layer 5, and the end-to-end package, renumbered P15 (test) and P16 (live
  run, evidence), is layer 6.
