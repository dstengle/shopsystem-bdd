# This repository's CNL as it is, end to end (b112, research phase 1)

The other side of the comparison with Attempto, SBVR, FRET, EARS and GF-based CNLs. Read off main at a45dc02f
(2026-11-08). Every count was measured by scripts in the session's scratchpad (`b112/ourcnl/count.py`,
`count2.py`, `count3.py`, `prose.py`, `facts.py`) using the plugin's own readers (`spec_context.load`), so the
numbers are the tools' view of the spec, not a regex's. Every parse shown was run with `python3 scripts/model parse`.

## 0. The pipeline in one paragraph

A line is tokenised (a backticked or double-quoted span is one token, `spec_typed.py:18`), parsed by GF in a grammar
made of a fixed core (`grammar/Core.gf`, `Req.gf`) and modules generated from the glossary (`Lex`, `Typed`, `Def`,
`StepsTyped`). The parse must leave exactly one tree after post-parse guards (`spec_grammar.py:242-270`: "ambiguous:
n trees" is a refusal). The tree is put in a normal form (`spec_typed_verbs.normal`), translated fun by fun into
ground facts (`spec_facts.py`, `spec_facts_np.py`), and the facts are read twice: by `grammar/check.lp` (a clingo
search for conflicting pairs, findings L0-L6) and by `spec_steps.py` (Gherkin Givens/When/Thens). There is no
intermediate logical form between the tree and the facts; the facts are the meaning.

## 1. Syntax

### 1.1 Sentence forms (`grammar/Req.gf:51-60`)

Ten forms, clauses in a fixed order, one per requirement: `Ubiq` (R.), `When T, R.`, `While C, R.`, `Where F, R.`,
`If T, then R.`, and the combinations `While C, when T`, `Where F, when T`, `Where F, while C`, `While C, if T,
then`, `Where F, if T, then`. There is no `Where F, while C, when T` (three clauses), no `unless` (considered and
deferred, design-r3 §4), no "only after", "before", "until", "within".

### 1.2 Responses (`Req.gf:61-68`)

- `Shall : Subj -> VPs -> Resp` ("X shall A, B and C"), `ShallNot : Subj -> VPor -> Resp` ("X shall not A or B",
  read as neither). `and` under `shall not` is refused (corpus `refused.txt`).
- `AndResp`: "R1, and R2" for responses with different subjects (or the same subject with different polarity,
  as in requests r33 "`work` shall print the comment, and `work` shall not write the comment"). There is no
  mixed-polarity VP list: "shall print the comment and not write the comment" is refused (tested; GF stops at "not",
  and the frame guard reports it).
- Subjects: an actor (`ActorSubj`) or a noun phrase (`NPSubj`). No modal other than `shall`: "may", "must",
  "should", "always", "eventually" all fail at that token (tested).

### 1.3 Triggers (`Req.gf:72-76`, `spec_typed_verbs.py:119-134`, `spec_typed.py:104-105`)

- `Runs`: "S runs `cmd`"; `RunsOn`: "S runs `cmd` on NP"; `IsRun`: "`cmd` is run". The command is a code literal
  or an actor named as a command (`CmdActor`).
- Per verb frame: `e__Happens` ("S verbs O"), `e__HappensI` (no object), `e__HappensTo` ("S verbs O to R").
- Per attribute: `<attr>_Becomes` ("X becomes `v`").
- A trigger is one clause: "When a session runs `work sync` and a comment is unrecorded" is refused at "and".

### 1.4 Conditions and atoms (`Req.gf:77-84`)

`Cond` is a flat list of atoms joined by `and` or `or` (`CondAnd`, `CondOr`, right-recursive, no brackets). A
`Where` takes `FeatGiven` ("`--json` is given") or any atom (`FeatAtom`). The atoms are:

| atom | source | English |
|---|---|---|
| `Holds`, `HoldsA`, `IsFree` | core | "a session holds the spec lock", "the spec lock is free" |
| `<attr>_Is`, `_IsNot` | per attribute and kind (`spec_typed.py:104`) | "a request is `delivered`" / "is not" |
| `<cond>_Is`, `_IsNot` | per condition and kind (`spec_typed.py:124-129`) | "a comment is unreadable" |
| `rel_<k1>_<w>_<k2>_Atom`, `_AtomNot` | per relation row (`spec_typed.py:143-155`) | "a comment is on a request", "a comment holds a foreign entry", "does not hold" |
| `e__Does`, `e__DoesNot` | per verb with an object (`spec_typed_verbs.py:127-131`) | "`work` posts a comment" as a state (b85) |

What an atom cannot be: a value list on a clause ("a request is `delivered` or `refused`" is refused; it parses
only as a modifier, "a request whose status is `delivered` or `refused`"); an adjective coordination ("is unreadable
and unrecorded"); "the status of a request is `v`" (the attribute's `_Of` is a noun phrase only, no `Is` on it);
"empty"; a comparison or number ("the number of comments is 2"); a possessive; a relation with no row ("a request
has no comment" fails at "has").

### 1.5 Verb phrases (`Req.gf:87-93`, `spec_typed_verbs.py:119-134`, `spec_typed.py:106`)

Core verbs with no frame (any subject): `print NPs`, `exit successfully`, `exit with an error naming NP`, `change
nothing`, `hold the R`, `hold a R`, `hold at most N Rs at a time`. Per frame: `e__Do` (verb + object), `e__DoI`
(intransitive), `e__DoTo` (object, then "to" recipient: one order only, the double-object order is refused, verb-frames
design call 2). Per attribute: `<attr>_Set` ("set the status of X to `v`"). Seven verbs are reserved because the core
spells them (`spec_lexicon.py:27`, v_t6).

### 1.6 Noun phrases (`spec_typed.py:20-22, 82-93`; `Req.gf:95-106`)

Per kind, eight determiners: `An` (a/an), `Every`, `The`, `No`, `AtMostOne` ("at most one"), `One`, `Pl` (a bare
plural: "comments"; "the comments" is refused), `Its`; plus `Named` ("the comment `x`", a kind with a code giving it
identity), `It`, and `NumberOf` ("the number of comments", an untyped NP). Kindless NPs: `CodeNP`, `QuotedNP`,
`QuotedFor` ("\"turns\" for the stage"), `Only NP`, attribute `_Of` ("the status of X"), the attribute's bare word
`n_<attr>` ("a status").

Common-noun modifiers, all post-nominal except `Pre`, stacking by recursion on `CN`:

- attribute: `_Pre` ("a `drafted` item"), `_ThatIs`/`_ThatIsNot` ("an item that is `drafted`"), `_Whose`/`_WhoseNot`
  with a value list ("a request whose status is `delivered` or `refused`") (`spec_typed.py:100-117`);
- condition: `_Pre` ("an unreadable comment"), `_ThatIs`/`_ThatIsNot` (`spec_typed.py:124-129`);
- relation row: `rel_<k1>_<w>_<k2>` ("a comment on a request"; for a verb-word row, "a comment that holds a foreign
  entry", `CoreEng.gf:30` `verbal`).

There is no relative clause built from a verb frame ("a comment that `work` posts" is refused at `` `work` ``;
the verb-frames design §"What changes" planned one, it was not built), no "whose" over a relation ("a comment whose
request is closed" is refused), no "of" except where a row's word is "of" (18 of 98 rows), no "'s", no relative
clause after a negation ("a comment that is not on a request" is refused), no conjunction of modifiers with "and that".

### 1.7 Literals and coordination

Codes in backticks and quoted strings are opaque tokens (`Req.gf:101-104`). Guards (`spec_tree.py:51-97`): a code
must have backticks and must not be a lexicon word; a quoted text must have quotes; no repeated list member; "it"
only after an NP of its kind, "its" only after any NP. NP lists (`MoreNP`: "A, B and C") appear only under `print`.
`Count` is a number or a code, used only by `HoldAtMost`.

### 1.8 What each glossary entry generates

| entry | part of speech (`spec_lexicon.py:67-69`) | generated |
|---|---|---|
| kind | `(noun)`, optional `Kind of:`, `Plural:` | `K_CN`, `K_NP`, the 8 determiners, `Named`, `It`, `toNP`, `NumberOf` |
| actor | `(proper noun)`, optional `Kind of:` | one `Actor` constant (and a member of each `T_Sb` it falls under) |
| condition | `(adjective of K[, K2])` | `Pre`, `ThatIs`, `ThatIsNot`, `Is`, `IsNot` per kind; one `Def` fun per kind |
| attribute | `(attribute of K)`, `Values:`, `Transitions:` | value constants, value lists, `ThatIs(Not)`, `Whose(Not)`, `Pre`, `Is(Not)`, `Becomes`, `Set`, `Of`, the bare word |
| resource | `(noun, exclusive)` / `(noun, counted by …)` | one `Resource` constant |
| verb | `(verb)`, `Frame:`, `Forms:` | `T_Sb`/`T_Ob` categories for its frame's kinds, `Happens*`, `Do*`, `Does(Not)`, and step funs |
| relation row | `| from | word | to | card |` in `## Relations` | modifier, `_Atom`, `_AtomNot`, for each sub-kind pair (`spec_relations.py:75-88`) |

A verb's frame is read by string search (`spec_frames.py:56-82`): subject, the verb's third-person form, an optional
preposition (b106, delivered in batch-20; none of this repository's 43 verbs uses one yet), object, optional
"to" recipient. A subject slot accepts any noun whose kind or actor is at or below the frame's (`spec_frames.below`),
and a code; an object slot accepts those, codes, quoted texts, `only`, attribute `Of`, `NumberOf` and bare attribute
words (`spec_typed_verbs.py:94-118`). So "`work` shall change the status of the request" type-checks against any frame
whose object is a kind, because the attribute NP is kindless.

### 1.9 The Def grammar (`spec_typed_def.py:23-33`)

One fun per (condition, kind): `c_<cond>_<kind>_Def : Cond -> Def`, English "a K is C when <Cond>." The body is a
requirement condition, so a definition can say exactly what a While clause can say, no more. "it" is refused (the
subject is "the K", `spec_typed_def.py:36-41`). A definition that does not parse is silently a *prose* condition: the
condition is a gloss, nothing refuses it.

### 1.10 The step grammar (`grammar/Steps.gf`, `spec_typed_verbs.py:138-155`, `features_vocab_gf.py:26-33`)

A step is a Req atom (`SAtom`), feature (`SFeat`), trigger (`STrig`), the fixed `SPrints`/`SPrintsNot`,
`SExitsOk`, `SExitsErr`, `SChangesNothing`, a verb's `SDoes`/`SDoesNot`/`SDoesTo`/`SDoesToNot`/`SDoesI`/
`SDoesINot`, and per kind an instance mention `K_Inst` ("the comment c1") and Givens `K_Given` ("a comment c1"),
`<attr>_Given` ("a request q1 that is `awaiting-asker`"). Note the step grammar has negated forms for verbs and
`print` that the requirement grammar spells only through `shall not`.

## 2. Semantics: tree to facts to `check.lp`

### 2.1 The fact vocabulary (`spec_facts.py:1-20`, `spec_facts_np.py:1-18`)

Each NP of a kind becomes a role `v<n>` (`role(R,V,K)`), one generic instance, numbered by mention. Pre-state
literals: `cond(R,V,Attr,Val,Pol)`, `ccond(R,V,C,Pol)`, `crel(R,Rel,X,Y,Pol)`, `holds`, `free`, `feat`. Trigger:
`trig(R,P,E,D,X)`, P ∈ {ran, does, becomes}. Responses: `resp(R,I,Pol,E,D,X)` per conjunct; `set(R,I,X,Attr,Val)`.
Object restrictions: `oattr`, `onot`, `orel`, `ocond`. Quantifier facts: `every(R,V)`, `none/4`, `cnone/3`,
`rnone/4`, `uall`, `uattr`, `urel`, `ucond`, `uccond`, `the(R,V)`, `named(R,V,C)`. Others: `only(R,I,K)`,
`count(R,Res,N)`, `uses/nouse`, `form`, `disj` (a split for each `or`/value-list choice, `spec_facts.py:254-267`).

### 2.2 Each construct, read

Measured by translating test lines (scratchpad `facts.py`):

| construct, position | facts | logical reading |
|---|---|---|
| "a K" anywhere | fresh role | a free variable; in `check.lp` it can merge with any compatible role of the other requirement, so in effect the generic/donkey reading ∀x (C(x) ∧ T → R(x)) |
| "the K" after a K | the bound role (`spec_facts_np.py:137-141`) | anaphor resolved **by kind**, to the last role of that kind |
| "the K" with no K before | fresh role + `the(R,V)` (`:142-145`) | "the one thing of its kind": `check.lp:73-96` forces every same-kind role the other side names onto it |
| "no K is C" in a condition | `cnone(R,K,C)`, no role (`spec_facts.py:147-154`) | ¬∃x K(x) ∧ C(x) over the merged pre-state (`check.lp:126-130`) |
| "X holds no K" (relation) | `rnone` | ¬∃y rel(x,y) |
| "X does not hold a K" | role y + `crel(…,neg)` | **∃y ¬rel(x,y)**: a fresh K the comment does not hold, not "holds none" |
| "a K is not C" in a condition | role + `ccond(…,neg)` | ∃x K(x) ∧ ¬C(x) (fine: the role is the one acted on) |
| "`work` does not post a K" in While | role + `crel(R,e_post,…,neg)` | ∃y ¬post(work,y), a verb read as a static relation, scope as above |
| "every K is C" in a condition | `uall`, `uccond` (`spec_facts_np.py:177-201`) | ∀x K(x) ∧ restrictions → C(x) (`check.lp:161-172`); a negated or condition restriction gives no conclusion |
| "every K" / plural as object or response subject | role + `every(R,V)` (`spec_facts.py:62-67, 225-226`) | **ignored by `check.lp`** (no rule reads `every/2`); one generic instance; only Gherkin reads it, as a contrast |
| "shall not V a K that is C" | role + `ocond` + `resp(…,neg)` | ¬V(x) for the generic x with C |
| "shall V no K" | role + `resp(…,neg)` (`spec_facts.py:227-240`) | same as "shall not V a K" |
| "at most one K", "one K" | as "a K" | **the count is lost** |
| "only a K" | `only(R,I,K)`, no `resp` (`:209-213`) | **ignored by `check.lp`** |
| "hold at most N Rs" | `count(R,Res,N)` | **ignored by `check.lp`** (no rule; and no line uses it) |
| `C1 or C2`, `whose A is v1 or v2` | the requirement split into R#1, R#2 | disjunction by case split |
| a defined condition, positive | `ccond` + its Def's literals on the same role (`spec_facts_np.py:98-109`) | an abbreviation, expanded |
| a defined condition, negated / under `no` / `every` | `dalt`/`dlit` domain facts (`spec_facts.py:276-293`) | read through the definition only when every literal is an attribute value on its own subject |
| a prose condition | `ccond` only; `prose(C)` | an opaque one-place fluent; a clash depending on it is L6 |
| "the status of X" | the term `value(t_status,X)` | a functional term, usable only as an object |
| "the number of Ks" | the constant `number(k)` | a constant, not relative to any owner |
| `Where F` with an atom | same as `While` | no distinction between configuration and state |
| "X runs `cmd`" | `trig(R,ran,"`cmd`",X,none)` | an event whose identity is the command string |

### 2.3 What `check.lp` does

- **Candidate pairs** (`check.lp:29-61`): two requirements are a candidate only if their responses can clash
  (opposite polarity of one event, two values set of one attribute, `exit_ok` against `exit_error`, `change_nothing`
  against a changing event, use against no-use) and their triggers are one event with compatible kinds of doer and
  object; or one is untriggered. An `If` requirement never pairs with a non-`If` one: the unwanted-behaviour form
  is a priority exception (`check.lp:57-61`), a small piece of defeasibility.
- **Unification** (`check.lp:63-96`): a choice rule maps each role of B to a compatible role of A or to its own
  instance; named codes are one thing; `the` forces uniqueness; triggers must coincide.
- **Two states** (`check.lp:98-121`): state 0 is the pre-state where the trigger happens; state 1 is state 0 with
  the triggered side's `set`s applied (frame axiom: unset values persist, `:106-108`). An untriggered requirement
  paired with a triggered one is read at state 1. Responses other than `set` are events with no effect on state.
- **Consistency** (`:109-135`): two values of one attribute, a literal both ways, `none`/`cnone`/`rnone` violated, a
  functional relation (`fun(Q)`: cardinality "one", or a blank-cardinality row whose word is for/with/on/of/in,
  `spec_logic_vocab.py:30-38`) with two images, a resource both free and held.
- **Findings**: L1 clash (`:174-207`) and self-contradiction (`:209-221`); L6 the same clash when it rests on a
  prose condition stated on one side only (`:198-207`); L3 a `set` with no transition from its pre-value (`:223-228`);
  L4 a pre-state value unreachable from an initial value (`:229-232`); L5 an untriggered positive event obligation
  (`:233-240`); L2 equal normalised trees and L0 the 20 s limit are in `spec_solve.py:5-9, 91, 172`.

Today's run: 8 findings, 4 L5 (U4, U4, U7, U8: "U4 obliges `work` to commit a transition in every state") and 4 L6
(requests r32/r33, r33/r52, r33/r53 on "unreadable and unrecorded"; migration-tools r14/r25 on "unframed").

The intended temporal reading is stated as G(T → X R) for When and G(C → R) for While (design-r3 §9 call 1); the
check unrolls it once for pairs. Not checked: chains (a response triggering another requirement), realizability,
timing, any property over more than two states, and conflicts among three or more requirements (design-r3 §2).

## 3. Gherkin (`spec_steps.py:204-241`, `spec_steps_facts.py`, `features_generate.py`)

One group is one scenario; no solver. Givens: `feat`, then pre-state facts in order (`cond`, `ccond`, `crel`, `holds`,
`free`), each instance introduced by a `K_Given` or `<attr>_Given` the first time it appears
(`spec_steps.py:122-133`); then for each `every` role with a restriction a *contrast* instance that fails it
(`spec_steps_facts.py:111-128`), whose Then is the negated response. When: the trigger. Thens: each response, its
object's restrictions after a positive response, its sets worded once. A later requirement of the group shares
instances by kind and rank (`spec_steps_facts.py:61-73`). A defined condition is shown as its name, not its
expansion (`spec_steps_facts.py:36-49`). Example data from the group's `given` block goes first.

Requests r32 shows the result and the gaps at once:

```
Given a comment c1 / And the comment c1 is unrecorded / And a comment c2 / And the comment c2 is not unrecorded
When the session s1 runs `work sync`
Then `work` writes the comment c1 / And `work` prints the request q1 / And `work` does not write the comment c2
```

"every request" became one request `q1`, never introduced; the session `s1` is never introduced.

Known gaps, from b7 (needs-input, parked from batch-11) and b108 (idea): a negated `exit with an error` gives a
bracketed placeholder step; an object of a negative response loses its modifier or relation ("does not lend the book
b1" for "shall not lend a book that is out"); `no` and `every` in a precondition give no Given (`none` is skipped by
design, design-r3 §3.3); an instance named by the When or a Then is not introduced; "every video from the channel"
becomes one video (feed's report). The scenario steps are matched back by grammar (`tests/scenarios/vocab.py`) and the
meaning of each prose condition lives in a hand-written handler (e.g. `unreadable`:
`tests/scenarios/requests_handlers_issues.py:60-66`). For a prose condition, the test handler is the only executable
definition the system has.

## 4. Vocabulary model (measured)

| category | entries |
|---|---|
| kind (noun) | 166, of which 55 have `Kind of:`; supertypes most used: text 19, file 12, thing 9, tool 7, dispatch 6 |
| actor (proper noun) | 27, 19 with `Kind of:` |
| condition (adjective) | 170 (condition, kind) ids; **25 defined, 145 prose** (55 prose ones used by no line); 95 distinct used |
| attribute | 34, 6 with `Transitions:` |
| verb | 43, all framed; 43 with an object, 1 with a recipient, 0 prepositional |
| resource | 9, **used by no line** (left over from the retired supervision capability) |
| relation rows | 98: 28 cardinality "one", 70 blank; words: of 18, on 8, for 6, in 5, with 5, then verbs (changes, cites, gives, removes, adds, "enforced by", "broken by", "changed by", "added by" …) |

(The context file's "142 of 167" counted entries; this counts each (condition, kind) the logic sees.)

The hierarchy is a single-parent tree (`Kind of:` is one string, `spec_lexicon.py:117`; `spec_relations.py:53-68`).
Kinds and actors share it since 3.0: an actor is an individual typed by its `Kind of:`. Attributes are enumerations
of backticked values; there is no numeric, string, date or set-valued attribute, and no attribute whose value is a
thing (that is what relation rows do). A relation row's cardinality is "one" or blank, and blank is silently read
as functional when the word is one of five prepositions (`spec_logic_vocab.py:30-38`). Nothing imports an external
artifact: a schema, a file layout, a CLI's arguments are all inside code literals or prose glosses.

The 25 defined conditions are mostly value abbreviations: `closed` (×4 kinds), `open` (×2), `settled`, `behind`,
`ahead`, `current`, `outdated`, `queued` ("a repository is queued when the repository is `1.0.0`"); a few combine
("idle": "`own` and no initiative is open"; "passing": "well-formed and every request line of the item is settled";
"clean": "no review finding on the pull request is `fix now`"; "listless": "the result gives no change list").

Fifteen typical prose conditions, most used first (the gloss is the whole definition):

| condition (kind) | uses | definition |
|---|---|---|
| present (Python interpreter) | 11 | a Python interpreter whose file exists. |
| present (coverage map) | 9 | `tools map` has written the coverage map. |
| unrecorded (comment) | 5 | a comment on a request's issue that its request does not yet hold. |
| blocked (item) | 3 | an item with a dependency on an item that is not `delivered` and is not in the same batch. |
| downstream (bounded context) | 3 | a bounded context whose `spec/index.md` lists an upstream under `## Upstreams`. |
| received (request) | 3 | a request whose record is kept in its upstream's repository and whose asker is another bounded context. |
| sent (request) | 3 | a request whose record is kept in its asker's repository and whose upstream is another bounded context. |
| uncommittable (repository) | 3 | a repository in which git refuses to commit a request's record, as when a pre-commit hook fails … |
| unreadable (comment) | 3 | a comment whose block of fields does not parse. |
| absent (argument) | 2 | an argument that a command requires and that is not given. |
| failing (test) | 2 | the test fails when it runs. |
| misversioned (repository) | 2 | a repository whose `.shop/plugin-version` holds no version. |
| originless (command) | 2 | a command that gives none of `--source`, `--thread` and `--raised-for`. |
| uncited (observation) | 2 | an observation that the `source` of no initiative and of no request names. |
| untiered (design-decision) | 2 | a design-decision that is not `superseded` or `rejected` and whose frontmatter gives no `tier`. |

Nearly every one is a relative clause ("whose", "that … holds", "with a … that is not"), a negated existential ("no
version", "none of"), an event in the past ("has written"), a modal ("can import"), or a format test ("does not
parse"). Each is a structure the grammar lacks, named with a coined word. design-model-check alone has 57
conditions, most of them file-shape adjectives (headless, idless, misfiled, misnamed, overtagged, renumbered, reusing …).

## 5. Measured usage (265 lines: 260 in 16 capabilities, 5 in `spec/universal.md`; 0 refused)

| form | lines | | construct | lines |
|---|---|---|---|---|
| While-When | 87 | | a backticked code | 244 (92%) |
| When | 78 | | a condition, defined or prose (any position) | 145 (55%) |
| If-then | 40 | | a verb clause (framed verb) | 94 |
| While-If | 35 | | an attribute or value | 86 |
| Where-When | 14 | | a relation row (atom or modifier) | 48 |
| Where-If | 5 | | a quoted string | 34 |
| Ubiquitous | 5 (3 of them U-lines) | | `every` | 26 |
| Where | 1 | | `shall not` | 25 |
| | | | `no` | 1 |
| | | | `, and` between responses | 16 |
| | | | resource (hold, free) | 0 |
| | | | `or` in a condition | 0 |

- **Triggers**: 242 of 259 triggered lines (93%) are "X runs `cmd`" (130 `Runs`, 112 `RunsOn`); 16 are a verb
  frame; 1 is `Becomes`. 85 distinct command strings; 74 lines put arguments or example data in the code
  (`` `tools tests-of src/cart.py:total --by-file` ``).
- **Condition atoms** in While/Where clauses (165): condition `Is` 90 and `IsNot` 16 (64%), attribute `Is` 48 and
  `IsNot` 1, relation atom 10, verb as condition 0, resource 0; plus 20 `FeatGiven`.
- **Responses** (by conjunct): framed verb `Do` 142 + 20 negated + 1 `DoTo`; `print` 83 + 7 negated; `exit with an
  error naming` 85; `change nothing` 39; `exit successfully` 32; `set` 32 + 2 negated.
- **Modifiers**: relation modifier 66, condition `that is` 51, attribute `that is` 36 (`that is not` 4); `whose`
  lines exist only in `_Whose` value tests.
- **Determiners**: a 328, the 256, Named 62, every 31, number-of 10, it 2, plural 1, its 1, one 1, no 1, at-most-one 0.
- **Most used conditions**: present 20, passing 5, settled 5, unrecorded 5, malformed 4 (four different kinds),
  blocked, uncited, behind, downstream, unreadable, uncommittable, received, sent 3 each.
- Lines average 24.1 words (median 22, max 57).

The language as used is: *while <thing> is <coined adjective>, when <actor> runs `<command line>`, `<tool>` shall
print / exit with an error naming / change nothing / <verb> <thing>*. The grammar's quantifiers, resources,
disjunctions and `Becomes` are almost unused.

## 6. The hypotheses, tested

**1. No formal semantics — confirmed, with a qualification.** The meaning of a tree is whatever `spec_facts`'s ~500
lines emit, fun by fun, into a bespoke predicate set, read only by one fixed ASP program. There is no
truth-conditional semantics per sentence (no DRS, no FOL), so two readers (the check and the generator) can and do
disagree: `every` in an object is a universal for Gherkin and a single instance for the check. Several funs parse and
then mean nothing: `AtMostOne` and `One` translate as `An`, `only` and `count` are emitted and never read. The
qualification: the intended temporal semantics is written down (G(T→X R), G(C→R)), the translation is compositional
and total over the funs (an unknown fun raises, `spec_facts.py:19-20`), and `check.lp` is a precise operational
semantics of the conflict question.

**2. Quantifiers and articles — confirmed.** "a" is a free variable that unification may identify with anything
compatible (a generic/donkey reading, never declared). "the" binds by kind to the last role of that kind, so two
things of one kind can be told apart only by `Named` codes; "the" with no antecedent means unique. "no" is universal
negation in a condition, plain negation on an object. Negation and the indefinite scope the wrong way for
relations and verbs in conditions: "a comment does not hold a foreign entry" is ∃y ¬holds(c,y), while "holds no
foreign entry" is ¬∃y; both parse, with different meanings an English reader would not expect. A negated relation
under `every` or on an object raises "no translation" (`spec_facts_np.py:85-88`). In a While clause the variables
are effectively universally quantified over the pre-state (a role is a witness that the check searches over), but
`every` itself is read only as a clause subject.

**3. Time — confirmed.** Two states, one instantaneous trigger, responses as events at the next state, only `set`
changing state (`check.lp:98-108`). No ordering ("only after", "before" refused), no duration ("within" refused), no
"until", no sequences, no chains. A verb used as a condition ("While `work` posts a comment") becomes a timeless
relation fact. Ubiquitous lines with a verb ("`work` shall commit every transition and push the commit") are read as
an event in every state and draw L5: the logic has no way to say "every transition is eventually committed"
(liveness) or "no commit without a push" (an ordering invariant). Lifecycles exist only as attribute transition
graphs (6 of 34 attributes), checked by graph search (L3, L4).

**4. Modality — confirmed.** `shall` and `shall not` only; every response needs an agent and a verb phrase, so a
structural rule ("a comment is on one request", "every comment shall be on a request") does not parse; such rules
live only in relation-row cardinality. No may/should, no necessity vs obligation, no permission. One hidden modal
distinction exists: the `If` form overrides other forms on the same trigger (`check.lp:57-61`).

**5. Number and quantity — confirmed.** No "empty", no comparisons, no counts beyond `at most one` (meaning dropped)
and `hold at most N` (a resource form no line uses); "at most 3 comments" is refused. "the number of Ks" is a
printable constant, not relative to an owner and not comparable. The workaround in use is an enumerated attribute
(delegation's `wording`: `empty`, `written`) or a coined adjective (misversioned: "holds no version").

**6. Collections — confirmed.** A plural is only "every", bare ("comments"); "the comments", "the comments that are
unrecorded", "the channels a viewer subscribes to" do not parse. NP lists exist only under `print`. There is no
set-valued term, no membership, no "all of", and the check reads plural objects as one instance.

**7. Vocabulary model — partly confirmed.** One single-parent kind tree, coarse parts of speech (5 plus resource),
one-place adjectives, enumerated attributes only, and no imported artifacts: confirmed. "Actors apart from kinds" is
now refuted: since 3.0, 19 of 27 actors have `Kind of:` and fill typed frame slots. New finding: the 166 kinds are
largely file and text types (`Kind of: text` 19, `file` 12), so the ontology is a type hierarchy of artifacts with
little relational structure (98 rows, 48 lines use any).

**8. Noun phrases — confirmed.** No relative clause from a verb frame, no "whose" over a relation, no general "of",
no possessive, no relative clause after negation; one word per relation row and kind pair (a second relation needs a
new word, design-r2 §4.2). What exists is "that is <adjective/value>", "whose <attribute> is <values>", and the
row's own word ("a comment on a request", "a comment that holds a foreign entry").

### Weaknesses not on the list

1. **Triggers are command strings.** 93% of triggers are "X runs `cmd`"; event identity is string equality on the
   code, arguments and example data included, so the check can only pair lines with byte-identical commands, and
   flags are not modelled as features. The language describes a CLI's test cases more than its behaviour.
2. **Requirements carry example data.** Paths, versions and names inside codes (`src/cart.py:refund`, defined
   conditions like "behind: the repository is `0.23.1`") make lines into scenario instances, not rules.
3. **The fixed response verbs dominate and have no frame.** `print`, `exit with an error naming`, `change nothing`,
   `exit successfully` account for 246 of 443 response conjuncts; their subject is unchecked and `change nothing`
   needs a special exception rule for the line's own events (`check.lp:32-39`).
4. **Silent prose.** A condition whose definition fails to parse becomes prose with no diagnostic; nothing nudges
   the author, and the gloss is often a sentence just outside the grammar.
5. **Where = While.** A `Where` atom is translated as a pre-state literal like a `While` atom; only `FeatGiven`
   distinguishes features.
6. **Definition expressiveness is capped at the While clause.** A Def can only say what a condition can, so every
   gap in §1.4 is also a gap in definitions: that is why 145 of 170 are prose.
7. **Default functional relations.** A blank cardinality on a for/with/on/of/in row means "exactly one image" in the
   check, unstated in the spec.
8. **Dead vocabulary.** 9 resources and 55 prose conditions are used by no line, and nothing reports them.
9. **"it" ambiguity is refused, not resolved**: "… `work` shall post a comment, and a session shall print it" gives 2
   trees and is refused; the author must repeat the noun. Fine for clarity, costly for verbosity.
10. **Gherkin and logic diverge** on every, only and negated objects (§3), so a scenario can test something the check
    never saw, and the reverse.

## 7. The design principles and how they shaped the CNL

From the GF conversion design (`.shop/records/2026-11-03-gf-conversion/design.md`) and its revisions:

- **One tree or refused** (design §1, design-r2 §4): unambiguity is enforced by refusing, not resolving. It made the
  grammar shy of any construct that creates attachment ambiguity: PP attachment is typed by relation rows (design-r2
  §4.2), and relative clauses, "of" and possessives were left out because they multiply trees.
- **No escape hatch** (design §4): no free-text requirement. Combined with the next rule, it pushed meaning into the
  only open slot left, the glossary: a coined adjective with a prose gloss is the escape hatch the rule forbids in
  lines, moved into the lexicon.
- **Growth rule** (design §9.5, `Req.gf:44-45`): "A core fun is added only for a construct that recurs in at least
  two capabilities. Otherwise the line is reworded." and "A target project grows its language by glossary entries
  only." This is the direct cause of the adjective count: a consumer cannot add a structure, only a term, so a missing
  structure becomes a term. It also biases growth toward what the existing spec already says, which was written in
  the old grammar's terms.
- **No grammar function per sentence** (design §4): compositionality, kept.
- **Basic English, restricted; part of speech on every term; a verb's frame in the glossary; a clause is subject,
  verb and the nouns the verb takes; passive with no agent refused** (verb-frames design, b82/b84, 3.0.0): moved
  verbs from untyped to typed and caught objectless and agentless lines. It also introduced v_t12, refusing a condition
  whose definition names another kind with "the" ("a relation between two kinds is a verb between them"), the first
  rule that pushes back against relational adjectives. Its own non-goals left "the X" with no antecedent and nested
  NPs ("a caller with the YouTube access of a viewer") unsettled, and the relative clause from a frame it listed under
  "What changes" was not built.
- **One translation, read twice; small questions** (design-r3 §1-2): replaced the telingo whole-system model (227 s
  for one capability) with two states and pairwise witnesses (4 ms). This is what fixed time at two states, and
  "one generic instance per noun phrase" (design-r3 §9 call 3) is what makes `every`, counts and plurals hard to
  read.
- **Opaque prose conditions** (design-r3 §3.2, corrected by report-checker-gaps): first claimed sound, then found to
  give false hits; L6 was added to report those as "possible", and every prose condition turned into a Def was
  expected to sharpen the check "with no code change". 115 prose conditions at the time; 145 now.
- **No `unless`** (design-r3 §4): exceptions stay as negated conditions in the line, which is why `no` and `IsNot`
  carry exception logic, and why their scoping matters.

In short, the principles optimised for a parse with one tree, a check that runs in milliseconds, and generation with
no solver. They kept the core small and froze consumers out of growing it, and the result is a sentence skeleton
(EARS plus about 30 core funs) whose logical content is mostly in coined one-place adjectives that the logic cannot
see into.
