# Logic-based and knowledge-representation CNLs, and their semantics

Phase 1 of the b112 CNL research, logic and knowledge-representation strand: Attempto Controlled English (ACE), SBVR
Structured English and RuleSpeak, PENG and PENG-ASP, and briefly Sydney OWL Syntax, Rabbit, CLCE, E2V, PROSPER
and TBNLS. Each is compared with this repository's grammar (`grammar/Req.gf`, the generated `Typed` modules), its
translation (`scripts/spec_facts.py`, `scripts/spec_facts_np.py`) and its check (`grammar/check.lp`).

Where this report says what the repository does, that comes from reading main's code and running
`python3 scripts/model parse`. Where it says what the literature does, a source is named. Where I am unsure, I say so.

## 1. Verdicts in brief

| Hypothesis | Verdict from the literature | How the others solved it |
|---|---|---|
| 1. No formal semantics | **Partly confirmed.** The repository does have one written translation per fun (design-r3 §3), so meaning is not ad hoc. But the meaning of a line is defined only by what `check.lp` does with its facts. There is no formula with truth conditions, and no reasoner other than the clash search can use it. | ACE: construction rules build a DRS compositionally, and the DRS maps to first-order logic with standard model theory. PENG-ASP: DRS-like internal format, then an answer set program, round-trippable. |
| 2. Articles and quantifiers under negation and in While | **Confirmed as a real risk.** It is the classic donkey and negation-scope problem. ACE and PENG treat it with fixed accessibility and scope rules. The repository reads every noun phrase as a generic instance (`role(R,V,K)`) and unifies instances across a pair of lines. That gives "a" universal force in a While clause, which is right. But the scope of "a" under "not" is not stated anywhere. | ACE: an indefinite inside an if-part or negation sits in a sub-DRS. "If a farmer owns a donkey then he beats it" gets universal force over both, and "John does not enter a card" means no card. |
| 4. Modality: only shall / shall not | **Confirmed.** SBVR's whole rule taxonomy rests on the difference between necessity (definitional) and obligation (behavioural). ACE has can/must/should/may and "it is necessary/possible that". | SBVR: "It is necessary that …" vs "It is obligatory that …", with permitted, prohibited, possible and impossible. ACE: modal operators as DRS boxes, whose reasoning is left to background axioms. |
| 6. Collections | **Confirmed.** ACE and PENG-ASP have plurals (collective or distributive), "each of", and "at least / at most / exactly n". In PENG-ASP these map straight to clingo cardinality rules. | ACE plural objects in the DRS. PENG-ASP: "Every node is assigned to exactly one colour" becomes `1 { assigned(N,C) : colour(C) } 1 :- node(N)`. |
| 8. Noun phrases | **Confirmed, and the most important finding for b112.** Every logic CNL surveyed has general relative clauses ("a customer that owns a card", "every country that borders no body of water"). That construction is exactly what removes the need to coin adjectives. The repository has `that is <condition/value>` and `whose <attribute> is <value>`, but no relative clause with a verb. | ACE, PENG, SBVR and CLCE all have relative clauses built from any verb phrase. ACE→OWL turns "Every X that VP is a Y" into a defined class. |

Hypotheses 3 (time), 5 (quantity) and 7 (vocabulary) also come up below. On time, only PENG-ASP's event calculus
extension does what the owner wants: facts, actions and resulting states, solved with clingo.

## 2. Attempto Controlled English (ACE)

### 2.1 What it is

ACE is a subset of English that translates automatically and without ambiguity into first-order logic. It was first
presented in 1996 as a language for software specifications, and its focus later moved to knowledge representation
(Kuhn 2014, §4.1; Fuchs, Kaljurand and Kuhn 2008). The current documented version is ACE 6.7. Its parser is APE
(ACE Parsing Engine): SWI-Prolog, open source at github.com/Attempto/APE. APE can output a DRS, FOL, TPTP,
OWL/SWRL, RuleML and ACE paraphrases. It runs as a command, an HTTP server or a socket server. (The public web
service at attempto.ifi.uzh.ch returned 404 when I tried it on 2026-11-08, so the DRS examples below come from the
documentation, not from runs.)

### 2.2 Lexicon: function words fixed, content words defined by the user

The function words are predefined and cannot be changed by users: determiners, quantifiers, coordinators,
negation, pronouns, query words, modal auxiliaries, the copula and the genitive 's. Content words are nouns,
verbs, adjectives, adverbs and prepositions, and they come from a lexicon. APE ships about 2,000 entries, and users
supply their own with `-ulextext` or `-ulexfile` (ACE 6.7 construction rules; APE README). A content word can be a
hyphenated compound ("check-code", "fills-in"). This matches this repository's split, where the core is fixed and
the glossary generates the rest. The difference is that **ACE content words carry no definitions**. A word's
meaning comes only from the sentences that use it. The coined-adjective pattern ("unreadable (adjective of
comment): a comment whose block of fields does not parse") has no counterpart in ACE. In ACE you would write the
definition as a sentence of the text ("Every comment whose block does not parse is unreadable."), or not coin the
word at all.

### 2.3 Construction rules (what you may write)

From the ACE 6.7 construction rules (attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html):

- Simple sentences: subject + verb phrase, with intransitive, transitive and ditransitive verbs. "A customer gives
  a clerk a card."
- Copula with a noun phrase or an adjective: "John is a rich customer."
- Coordination with *and* and *or*. *and* binds tighter, and *, and* / *, or* override that.
- Conditionals: "If John enters a card then the automated-teller accepts it."
- Modality: *can*, *must* / *has to*, *should*, *may* on the verb phrase ("John may not wait."), and sentence-level
  "It is possible that John waits." / "It is not necessary that John enters a card and that he types a code."
- Negation: "John does not enter a code.", "no card", "It is false that a screen blinks." Negation as failure,
  separately: "It is not provable that a screen blinks."
- Noun modifiers: relative clauses ("a customer who is rich and who is well-known", and any verb phrase: "a
  customer that owns a card"), *of* genitives ("a customer of John"), Saxon 's, and possessive pronouns.
- Plurals: collective ("the cards") or distributive ("each of the cards"). Generalised quantifiers: "at least 2
  cards", "at most 2 cards", "exactly 3 cards", "more than 10 cards". Also "nothing but apples".
- Universal quantification: *every*, and global "For every code a clerk enters it."
- Queries and commands.
- Tense: **only the simple present** in declaratives. A passive is allowed **only with a "by" phrase** ("A card
  is entered by John."). ACE thus forbids exactly the agentless passive the owner calls a fault.

### 2.4 Interpretation rules (how each construct is read)

From the ACE 6.7 interpretation rules (attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html):

- A prepositional phrase attaches to the verb, and a relative clause to the noun immediately before it.
- **Quantifier scope is textual**: it runs from the quantifier to the end of the sentence (or of its coordinated
  sentence). "For every …" extends it over the whole sentence.
- **"A" is existential.** "A cat is an animal" means there is a cat that is an animal. A general statement needs
  "every" or "if-then".
- Plurals are collective by default ("Two girls lift a table" is one lifting). "Each of" makes them distributive.
- Negation and "it is false that" scope over the first clause only, unless "that" is repeated.
- The then-part of if-then runs to the end of the coordination.
- **Anaphora by accessibility (from DRT)**: a noun phrase inside a negated, modal, subordinated, interrogative
  or universally quantified sentence, or inside a then-part, is not accessible from later sentences. A noun phrase
  in an if-part *is* accessible in its then-part. "If a customer has a card then he enters it." is fine, while
  "John does not enter a card. *It is correct." is refused.
- A **definite noun phrase** resolves to the most recent, most specific accessible antecedent. **If there is
  none, it introduces a new entity.**
- A pronoun resolves to the most recent accessible noun phrase that agrees in number and gender and is not the
  subject of the same verb phrase.

### 2.5 Discourse Representation Structures and first-order logic

APE builds a DRS for the whole text: a box of discourse referents and conditions. Conditions use a few fixed
predicates whose arguments are the content words, so the DRS is "flat" or reified. `object/…` is a thing,
`predicate/…` an eventuality with a Davidsonian event referent, then `property`, `relation`, `modifier_pp`,
`modifier_adv` and `has_part`. Complex conditions are negation `-`, negation as failure `~`, possibility `<>`,
necessity `[]`, implication `=>`, disjunction `v`, and sentence subordination `X:drs`. This is from the
ACE course notes "Logical Background", Fuchs and Kaljurand, December 2006 (attempto.ifi.uzh.ch/site/courses/files/
ACE.Course.UniZH.1206.Logical_Background.pdf), and the DRS technical reports for ACE 5 to 6.6 by Fuchs, Kaljurand
and Kuhn, which I could not retrieve. Their example, in ACE 5 notation:

```
Every company that buys at least 2 standard machines gets a discount.

[]
  [A, B, C]
  object(A, atomic, company, object, cardinality, count_unit, eq, 1)
  object(B, group, machine, object, cardinality, count_unit, geq, 2)
  property(B, standard)
  predicate(C, event, buy, A, B)
  =>
  [D, E]
  object(D, atomic, discount, object, cardinality, count_unit, eq, 1)
  predicate(E, event, get, A, D)
```

The DRS then maps to FOL in the standard way. "Every man sleeps." becomes `forall(A, object(A,…man…) =>
exists(B, predicate(B, unspecified, sleep, A)))` (same source). The text's meaning *is* that formula's meaning,
under ordinary model theory, Herbrand semantics or a proof-theoretic reading, which the notes discuss. A theorem
prover can then decide consistency and entailment of whole texts: RACE, the Attempto reasoner, proves that one
ACE text follows from another and gives the justification back in ACE.

Note how the DRS handles the **donkey sentence**. The referents A (company) and B (machines) are introduced in
the left box of `=>`. DRT's rule is that referents of the antecedent box are universally quantified over the whole
implication, so "If a farmer owns a donkey then he beats it" gets the reading ∀x∀y (farmer(x) ∧ donkey(y) ∧
owns(x,y) → beats(x,y)). That is the right one, and "it" can refer to the donkey because the then-box is inside the
if-box's scope. ACE does not solve donkey sentences with special cases. The DRS construction solves them as a
by-product of accessibility.

Kuhn's caveat (2014, §4.1): ACE's DRSs are **underspecified** for plurals and modal verbs. Deductions about them
need background axioms that ACE itself does not fix. This is deliberate, so that different tools (ontology editors,
rule systems, provers) can give the same DRS slightly different semantics.

### 2.6 The OWL fragment (ACE→OWL) and rules (AceRules)

Kaljurand's ACE→OWL/SWRL maps a subset of ACE to OWL 2 (attempto.ifi.uzh.ch/site/docs/owl_to_ace.html; Kaljurand
2007, PhD thesis, *Attempto Controlled English as a Semantic Web Language*, Tartu). Named classes are common nouns,
individuals proper names, and properties transitive verbs or *of*-constructs, with an inverse as passive or 's.
Class expressions are relative clauses: "something that does not own a car", "something that borders at least 2
countries". Axioms: "Every country that borders no bodies-of-water is a landlocked-country." (subclass), "If X owns
something that is-part-of Y then X owns Y." (property chain), "If X is-child-of Y then it is false that X
is-spouse-of Y." (disjoint properties). **The first example is exactly what b112 asks for.** A coined term is
defined by a relative clause over relations, and lines can then use either the term or the relative clause
itself.

AceRules (Kuhn 2007, RR 2007, LNCS 4524) runs ACE rule texts under courteous, stable-model and
stable-model-with-strong-negation semantics, reading ACE's "does not" as strong negation and "it is not provable
that" as negation as failure: one CNL surface feeding an ASP-style engine.

### 2.7 Time in ACE

ACE has **no temporal semantics**. Declaratives are simple present only. Every verb gets a Davidsonian event or state
referent (`predicate(C, event, buy, A, B)`; ACE 5 tagged eventualities as `event` or `state`), but nothing orders
these referents. Time can only be modelled with content words ("at a time-point", "before", user-defined
prepositions), and ordering axioms then have to be written by hand. I found no ACE extension with situations or
fluents in the Attempto documentation.

## 3. SBVR Structured English and RuleSpeak

### 3.1 What it is

SBVR (OMG, *Semantics of Business Vocabulary and Business Rules*, version 1.5, December 2019, formal/19-10-02) is a
metamodel for business vocabularies and rules. Its informative annexes include SBVR Structured English and
RuleSpeak as notations. SBVR SE has four kinds of text, each in its own font style: **term** (noun concepts,
underlined green), **name** (individuals, double-underlined), **verb** (verb concepts, italic blue) and **keyword**
(the fixed words: "each", "it is obligatory that", "at most", "that", "only if"). See "SBVR Speaks (5)", Business
Rules Journal 7(4), 2006.

### 3.2 Vocabulary

- A **noun concept** has a term and a definition in genus-and-differentia form: a more general term, then "that",
  then the characteristics. "agency: branch that is not located at a EU-Rent-owned site and is operated by some
  agent" ("SBVR Speaks (6)", BRJ 7(5), 2006). Every definition is itself a sentence of the language, so it can be
  read formally. This is the repository's "defined condition", but required for every term, not optional.
- A **verb concept** (called a fact type before 1.0) is given by a wording that names its roles: "branch has car
  storage capacity", "date/time₁ is after date/time₂". This is close to the repository's 3.0 `Frame:`. A verb
  concept with one role is a **characteristic** ("car is damaged"). That is SBVR's unary state, and the nearest
  thing to the repository's adjectives. Even so, a characteristic is a verb concept with a role, and it can be
  given a formal definition.

### 3.3 Two kinds of rule

SBVR divides rules by modality. This is the distinction the owner has already adopted:

| | Definitional (structural, alethic) | Behavioural (operative, deontic) |
|---|---|---|
| Prefixed form | It is necessary that … / It is impossible that … / It is possible that … | It is obligatory that … / It is prohibited that … / It is permitted that … |
| Embedded form | always, never, sometimes | must, must not, may |
| Can it be broken? | No: it constrains what counts as a valid state | Yes: people or systems can act against it, so it carries an enforcement level |

Examples: "It is obligatory that each rental car is owned by exactly one branch." "A rental must have at most three
additional drivers." "A rental must be guaranteed by a credit card before a car is assigned to the rental."
(BRJ 2006; Kuhn 2014).

### 3.4 The weak point: no formal grammar

Kuhn (2014, §4.1): SBVR's semantics rests on second-order logic with Henkin semantics, but SBVR SE **has no formal
grammar**. Constituent order, *and*/*or* scope, quantifier scope and anaphora are all ambiguous, and "a" is defined
as "universal or existential quantification, depending on context based on English rules" (PENS class P3E4N4S2,
against ACE's P4E3N4S3). SBVR got the rule taxonomy and the vocabulary discipline right and left the syntax to the
reader. This repository has the opposite profile: a strict grammar with a thin taxonomy.

### 3.5 Time in SBVR

SBVR has no temporal logic of its own. Time was handed to a separate OMG standard, the **Date-Time Vocabulary**
(DTV 1.3, 2017). DTV adopts SBVR's "occurrence" and "what-happens state of affairs" and adds verb concepts such as
"occurs before", "occurs while" and "occurs throughout" (OMG issue DTV-2, DTV-21). The SBVR team decided to keep
these out of SBVR itself (DTV-2). I did not read the DTV text, only its issue tracker.

## 4. PENG and PENG-ASP

### 4.1 Language

PENG ("Processable English", Schwitter 2002) is ACE-inspired, translates via DRSs to FOL, and was designed around a
predictive editor that shows the user what may come next. Its descendants are PENG-D (OWL), PENG Light (TPTP),
**Sydney OWL Syntax** (a full two-way mapping to OWL: "The class adult is fully defined as any person that has at
least 20 as an age."; Cregan, Schwitter and Meyer 2007) and **PENG-ASP** (Guy and Schwitter 2017, *Language
Resources and Evaluation* 51:67–92), which targets answer set programs.

PENG-ASP sentences, from Schwitter 2018 ("Specifying and Verbalising Answer Set Programs in Controlled Natural
Language", TPLP 18:691–705, arXiv:1804.10765):

| CNL | ASP |
|---|---|
| Every student who works is successful. | `successful(A) :- student(A), work(A).` |
| Every student who studies at Macquarie University works or parties. | `work(B) ; party(B) :- student(B), study_at(B,macquarie_university).` |
| It is not the case that a student who is enrolled in Information Technology parties. | `:- student(C), enrolled_in(C,information_technology), party(C).` |
| Bob studies at Macquarie University and does not work. | `study_at(bob,…). -work(bob).` (strong negation) |
| If a student does not provably work then the student does not work. | `-work(X) :- student(X), not work(X).` (weak in the body, strong in the head) |
| Every node is assigned to exactly one colour. | a cardinality choice rule `1 { … } 1` |
| It is not the case that a node X is assigned to a colour and a node Y is assigned to the colour and the node X is connected to the node Y. | a constraint, with explicit variables X, Y telling apart noun phrases of the same form |

Points that bear on this repository:

- **The two negations are told apart in the words.** "does not" is strong (classical) negation, and "does not
  provably" is negation as failure. Integrity constraints have their own keyword phrase, "It is not the case that".
- **Anaphora by structure**: a definite noun phrase may refer to an antecedent in the same rule list or a list
  above it. The body of a rule is above its head, but not the other way round. A definite noun phrase with no
  accessible antecedent is treated as an indefinite (as in ACE).
- **Explicit variables** ("a location A … a location B") settle what articles cannot, at a small cost in
  naturalness.
- **Round-tripping**: one bidirectional grammar parses CNL to ASP and verbalises ASP back. Equivalence is checked
  by getting the same program and the same answer sets (Schwitter 2018; 2020).

### 4.2 Time: event calculus in clingo

Schwitter 2019 ("Augmenting an Answer Set Based Controlled Natural Language with Temporal Expressions", PRICAI 2019,
LNAI 11670:500–513) adds temporal expressions. Fluents, the commonsense law of inertia and continuous change are
written in the CNL and run by "a linguistically motivated version of the Event Calculus" implemented in ASP on
clingo. I read only the abstract of that paper. The IJCAI 2020 demonstration paper (Schwitter, "Lossless Semantic
Round-Tripping in PENG ASP", IJCAI-20 Demos, 5291–5293) shows the language in full:

```
1.  The parcel is in Epping on 2020-02-16 at 08:00.
2.  Rona is in Epping at 08:50 and picks up the parcel at 09:00.
9.  If a person drives from a location A to a location B at a time point
    then the person will be in B afterwards.
10. If a person drives from a location A to a location B at a time point
    then the person will no longer be in A afterwards.
11. If a person is in a location at a time point and an object is in the same location at the
    same time point and the person picks up the object at that time point
    then the person will be holding the object afterwards.
15. It is not the case that an object is in a location A at a time point and the same object is in a
    location B at the same time point and the location A is not the same as the location B.
16. Where is the parcel at 09:25?
```

The sentences translate to event-calculus ASP. A state verb ("is in") becomes a fluent with `holds_at(fluent(…),
T)`, and an action verb ("picks up") becomes `happens(event(…), T)`. "will be … afterwards" becomes
`initiated_at(fluent(…), T) :- happens(event(…), T), …` and "will no longer be … afterwards" becomes
`terminated_at(…)`. Sentence 15 becomes a constraint over `holds_at`, and inertia carries fluents forward between
events. Sentences 13 and 14 handle ramifications (indirect effects).

This is the owner's "facts, actions and resulting states" in a CNL that is solved by clingo, and in that sense the
nearest relative of this repository. Three features match the repository's structures directly:

| PENG-ASP | This repository |
|---|---|
| state verb + "at a time point" → `holds_at` | a While condition → `cond`, `ccond`, `crel` in the pre-state |
| action verb + time → `happens` | a When trigger → `trig(R,P,E,D,V)` |
| "then X will be Y afterwards" / "will no longer be" → `initiated_at` / `terminated_at` | a response `set(R,I,V,A,Val)` (new value), and L3/L4 over transitions |
| "It is not the case that …" over fluents → constraint | nothing: no state invariant can be written (owner's "a list has items or is empty") |
| inertia axiom over a timeline of many events | two states, before and after one trigger |

## 5. Other logic CNLs, briefly

- **Rabbit** (Hart, Johnson and Dolbear 2008; Ordnance Survey), for OWL, has a few sentence patterns, and declaring
  a word is itself a sentence ("Sheep is a concept, plural Sheep."; "Every River flows into exactly one of River,
  Lake or Sea."). Comprehension results were mixed (Kuhn 2014).
- **CLCE** (Sowa 2004) maps to Common Logic / CGIF. It has no plurals, present tense only, and **variables in place
  of pronouns** ("If some person x is the mother of a person y, then the person y is a child of the person x."). It
  declares verbs with all their argument patterns in one sentence: "Declare give as verb (agent gives recipient
  theme) (agent gives theme to recipient) (theme is given to recipient by agent) …" (Kuhn 2014). That is a fuller
  form of this repository's `Frame:`, including the passive with its agent.
- **E2V** (Pratt-Hartmann 2003) maps to the **two-variable fragment** of FOL, so satisfiability is decidable
  (NEXPTIME-complete). Yet it keeps relative clauses and nested quantifiers: "Every artist who employs a
  carpenter despises every beekeeper who admires him."
- **PROSPER Controlled English** (Grover et al. 2000, hardware verification) maps to temporal logic: "If sigi is
  high and then is low on the next cycle, then sigo is low and after one cycle becomes high and then after one more
  cycle becomes low." **TBNLS** (Esser and Struss 2007, automotive test specs) has 15 templates and maps to
  propositional logic with temporal relations: "If Button B4 is down occurs, then Lamp L3 is red hold immediately,
  until 10 seconds elapsed." Both show EARS-like templates with ordering and duration ("then", "on the next cycle",
  "until") added to them.

## 6. Comparison with this repository, hypothesis by hypothesis

### H1: formal semantics

The repository is better off than the hypothesis feared. `spec_facts.py` states that it is "the only reading of a
requirement's meaning in the plugin", with one translation per fun, and an unknown fun is refused rather than given
partial facts. That is a written, deterministic semantics. What it lacks compared with ACE:

1. **No compositional target with model theory.** ACE's meaning is a FOL formula, so "true in a model",
   "entails" and "consistent" are defined independently of any tool. Here, a line's facts mean something only
   through `check.lp`, a meta-encoding that searches *pairs* of lines for a clash on one trigger. So the set of
   lines as a whole has no defined models. Questions such as "does the spec entail that X?" or "is this ubiquitous
   line redundant?" (the owner wants Gherkin only for what is not already entailed) have no semantic footing. ACE
   (RACE) and PENG-ASP (answer sets) answer them directly.
2. **The meaning is decided per fun, not by construction rules.** Each new GF fun needs a new hand translation,
   and its interaction with negation, `every` and `no` is coded case by case. Examples are `spec_facts_np`'s
   "a restriction the check cannot match (negated, a condition) … gives no conclusion" and `check.lp`'s separate
   rules for `none`, `cnone`, `rnone`, `uall`, `ucond` and `uccond`. In a DRS, negation, implication and
   quantification are three box constructors that every noun phrase and verb passes through in the same way.
3. **Prose conditions are outside the logic.** 142 of 167 conditions are opaque atoms (L6). In ACE and SBVR,
   every definition is a sentence of the language, so nothing is opaque.

The literature's answer: build a DRS-like intermediate representation (referents plus conditions, with
negation/implication/disjunction boxes), give it a fixed translation to logic, and let the clash check, Gherkin
generation and an entailment check all read that representation. PENG-ASP shows this can target clingo directly.

### H2: articles, quantifiers, donkey sentences

What the repository does (from `spec_facts_np.py` and `check.lp`): each noun phrase of a kind is a role `v<n>`; "the"
and "it" pick the role bound before for the kind; a "the" with no antecedent is a fresh role marked `the(R,V)`,
"the one thing of its kind"; "no K" in a clause is not a role but `none`/`cnone`/`rnone`; "every K" as a clause's
subject is a universal `u<n>`. The check then treats each role as a generic instance, mapped onto the other line's
roles of a compatible kind.

Compared with ACE and PENG:

- **"a" in While/When.** It has universal force here, because any instance may be unified. That matches DRT's
  reading of indefinites in an if-part ("If a farmer owns a donkey …"). This is fine, and it is the same answer as
  ACE's, reached by a different route.
- **"a" under "not".** ACE is explicit: "John does not enter a card" puts the card inside the negation box, so
  no card is entered. In the repository, "While a session does not hold a lock …" yields `crel(R,Rel,V,W,neg)` with
  W an ordinary role. As I read it, that says this session does not hold *this particular* lock W: a wide-scope,
  specific reading. The two readings differ in exactly the cases the check is used for. The repository also has a
  separate `no` (`rnone`) for the narrow reading. So "does not hold a lock" and "holds no lock" both exist and mean
  different things. That may be intended, but nothing written down tells a writer which is which. ACE settles this
  with one rule (§2.4). **Confirmed as a real weakness: undocumented scope.**
- **"the" with no antecedent.** ACE and PENG treat it as a new entity, like "a". The repository treats it as the
  unique thing of its kind. The repository's choice suits singletons ("the spec lock", "the person"), but it
  changes the meaning of a line silently depending on whether an earlier noun phrase exists. ACE's reading is
  safer. The repository's could be kept if it were a stated interpretation rule, or if singletons were proper nouns
  (as actors already are).
- **Explicit variables.** PENG-ASP and CLCE allow "a location A … a location B" for two noun phrases of one kind.
  The repository has no way to tell two instances of the same kind apart within one line.

### H4: modality

The owner already distinguishes structural rules (necessity) from operative ones (obligation), safety from liveness.
SBVR is the standard that makes this distinction, with fixed keywords for six modal operators. ACE has can, must,
should and may, plus "it is necessary/possible that", as DRS operator boxes. The repository has only shall and
shall not on a system response, so:

- a **necessity** ("It is necessary that each request has exactly one upstream", or an owner's state invariant
  "a list has items or is empty") cannot be written;
- a **permission** ("`work` may print a warning") is refused: `model parse` stops at "may";
- **"never" / "always"** are refused ("`work` shall never write …" stops at "never").

Lesson: keep modality to a small fixed set of keywords. Map necessity to a constraint over states (PENG-ASP's "It
is not the case that …" becomes an integrity constraint) and obligation to an effect rule. SBVR's point that only
behavioural rules can be violated, and so monitored, fits the owner's `verified_by` routes. ACE's warning: give
each modal a fixed logical reading, or it stays underspecified (Kuhn 2014).

### H6: collections

ACE has plural noun phrases with collective and distributive readings ("each of"), number quantifiers ("at least
2", "at most", "exactly", "more than") and "nothing but". PENG-ASP maps "exactly one" straight to a clingo cardinality
rule. The repository has `every K` as a print object, `NumberOf` ("the number of …") and `HoldAtMost`, but no general
plural and no "at least / at most n K" in a noun phrase. "The channels a viewer subscribes to" as a set would be
"every channel that the viewer subscribes to" in ACE, a universal with a relative clause. Since clingo has
aggregates (`#count`) and cardinality bounds, the target logic already supports what PENG-ASP shows on the surface.

### H8: noun phrases

Every system surveyed except Rabbit has **relative clauses built from any verb phrase**, and SBVR builds every
definition from one. The repository's generated modules have, per kind and attribute, `_ThatIs` / `_ThatIsNot`
("a comment that is unreadable"), `_Whose` / `_WhoseNot` ("a request whose status is `open`"), `_Pre` and the
relation-row modifier. They have no "a comment that `work` wrote", "a viewer that subscribes to no channel" or
"a request whose upstream is unhosted". ACE's `of` is general ("a customer of John"); the repository's `_Of` exists
only for attributes.

This is the structural root of b112. Without a relative clause over verbs and relations, a writer who needs "a
viewer that subscribes to no channel" has to coin "listless" and define it in prose. ACE→OWL's "Every country that
borders no bodies-of-water is a landlocked-country" shows both cures:

1. allow the relative clause inline in requirement lines, and
2. when a name is still wanted, write its definition in the same grammar ("Every viewer that subscribes to no
   channel is listless."), making it a *defined* condition by construction, never a prose one.

Two smaller points confirm the owner's other instincts:

- **Agentless passives**: ACE allows a passive only with a "by" phrase, which is the owner's rule.
- **Formats as external artifacts**: no surveyed CNL builds schemas from sentences. ACE→OWL and SOS import
  ontologies, and Rabbit has import statements. "Conforms to the comment schema", with the schema read as facts,
  matches that practice.

### H3, H5, H7 (in passing)

- **H3 time**: confirmed as a limit. ACE, SBVR and the OWL CNLs have no time at all. PENG-ASP's event calculus
  (fluents, happens, initiates/terminates, inertia, "afterwards", "no longer", "at a time point") is the worked
  example, on clingo. PROSPER and TBNLS show "then / on the next cycle / until n seconds elapsed" in
  requirement-style templates. Note that the repository's two-state check is in effect a one-step event calculus
  without inertia. Moving to an event-calculus encoding is a generalisation, not a rewrite of the idea.
- **H7 vocabulary**: SBVR's verb concepts with named roles and characteristics as one-role verb concepts, and
  CLCE's `Declare … as verb (…)` with all argument patterns, are richer versions of `Frame:`. SBVR treats actors as
  ordinary noun concepts with names, not as a separate category.

## 7. What this suggests (options for phase 2, not decisions)

1. **Write down DRT-style interpretation rules**, as ACE does: textual scope, accessibility for "the" and "it", "a"
   under "not", and a definite with no antecedent. This documents what lines mean before anything changes.
2. **Put a DRS-like representation** between GF trees and facts: referents, a few fixed atomic predicates, and boxes
   for not, if/then, or and the modal keywords. Translate it once to clingo, and let the clash check, the steps and
   an entailment check all read it.
3. **Add general relative clauses** (a verb phrase, a relation, "no" inside them), so that a coined adjective is
   either unnecessary or defined in the grammar.
4. **Add a small modal set on the SBVR pattern**: necessity ("It is necessary that" / "always" / "never") for
   invariants, obligation (shall) and permission (may), each with a fixed logical reading.
5. **Take PENG-ASP's event calculus as the model for time**: state verbs as fluents, action verbs as events,
   "afterwards" / "no longer" as initiates/terminates, "It is not the case that" as a state constraint, with
   inertia. In EARS terms, While is a fluent, When an event, and shall an effect.
6. **Allow explicit variables** ("a session S … a session T") for the rare line with two instances of one kind.

## Sources

- Fuchs, N. E., Kaljurand, K., Kuhn, T. (2008). Attempto Controlled English for Knowledge Representation. *Reasoning
  Web 2008*, LNCS 5224, 104–124. Springer.
- Attempto project. ACE 6.7 Construction Rules. https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html
- Attempto project. ACE 6.7 Interpretation Rules. https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html
- Attempto project. OWL/SWRL verbalisation in ACE. https://attempto.ifi.uzh.ch/site/docs/owl_to_ace.html
- Attempto project. APE web service. https://attempto.ifi.uzh.ch/site/docs/ape_webservice.html (endpoint returned
  404 on 2026-11-08)
- Kaljurand, K., Fuchs, N. E., Kuhn, T. APE source and README. https://github.com/Attempto/APE
- Fuchs, N. E., Kaljurand, K. (December 2006). ACE: Language, Tools and Applications — Logical Background (course
  slides). https://attempto.ifi.uzh.ch/site/courses/files/ACE.Course.UniZH.1206.Logical_Background.pdf
- Fuchs, N. E., Kaljurand, K., Kuhn, T. Discourse Representation Structures for ACE 6.5 / 6.6. Technical reports
  ifi-2009.04 and IFI-2010.0010, University of Zurich. (Cited from catalogue entries. I could not retrieve the PDFs.)
- Kaljurand, K. (2007). *Attempto Controlled English as a Semantic Web Language*. PhD thesis, University of Tartu.
- Kuhn, T. (2007). AceRules: Executing Rules in Controlled Natural Language. *Web Reasoning and Rule Systems (RR
  2007)*, LNCS 4524. Springer.
- Kuhn, T. (2014). A Survey and Classification of Controlled Natural Languages. *Computational Linguistics* 40(1),
  121–170. arXiv:1507.01701.
- OMG (2019). Semantics of Business Vocabulary and Business Rules (SBVR) 1.5, formal/19-10-02.
  https://www.omg.org/spec/SBVR/
- The SBVR Team (2006). SBVR Speaks: (5) Notations for Business Rule Expression. *Business Rules Journal* 7(4).
  https://brcommunity.com/articles.php?id=b286
- The SBVR Team (2006). SBVR Speaks: (6) Concepts and Definitions in SBVR. *Business Rules Journal* 7(5).
  https://www.brcommunity.com/articles.php?id=b288
- OMG. Date-Time Vocabulary (DTV) 1.3 (2017), https://www.omg.org/spec/DTV/, and issues DTV-2, DTV-4, DTV-21 at
  https://issues.omg.org/issues/spec/DTV
- Guy, S., Schwitter, R. (2017). The PENG^ASP system: architecture, language and authoring tool. *Language
  Resources and Evaluation* 51(1), 67–92.
- Schwitter, R. (2018). Specifying and Verbalising Answer Set Programs in Controlled Natural Language. *TPLP*
  18(3-4), 691–705. arXiv:1804.10765.
- Schwitter, R. (2019). Augmenting an Answer Set Based Controlled Natural Language with Temporal Expressions. *PRICAI
  2019*, LNAI 11670, 500–513. (Abstract only read.)
- Schwitter, R. (2020). Lossless Semantic Round-Tripping in PENG ASP. *IJCAI-20 Demonstrations*, 5291–5293.
  https://www.ijcai.org/proceedings/2020/0773.pdf
- Schwitter, R. (2014). Controlled Natural Language Processing as Answer Set Programming: an Experiment.
  arXiv:1408.2466.
- Cregan, A., Schwitter, R., Meyer, T. (2007). Sydney OWL Syntax — towards a Controlled Natural Language Syntax for
  OWL 1.1. OWLED 2007. (Cited through Kuhn 2014.)
- Hart, G., Johnson, M., Dolbear, C. (2008). Rabbit: Developing a Control Natural Language for Authoring Ontologies.
  ESWC 2008. (Cited through Kuhn 2014.)
- Sowa, J. F. (2004). Common Logic Controlled English. Draft. (Cited through Kuhn 2014.)
- Pratt-Hartmann, I. (2003). A two-variable fragment of English. *Journal of Logic, Language and Information*
  12(1). (Cited through Kuhn 2014.)
- Grover, C. et al. (2000), PROSPER Controlled English; Esser, M., Struss, P. (2007), TBNLS. (Both cited through
  Kuhn 2014.)
