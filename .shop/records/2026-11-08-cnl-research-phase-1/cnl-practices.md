# CNL best practices and classification (b112 research, phase 1)

Strand: what the literature says a controlled natural language (CNL) is, how it is classified, how it is designed
well, and what is known about CNLs for requirements. Each practice is followed by a short note on whether this
repository's CNL (the requirement lines parsed by `grammar/Req.gf` and the generated modules) follows it, breaks it,
or leaves it unclear. Those notes are hypotheses for the later phases, not findings.

Sources I read in full text are marked (read). Sources I know only from abstracts, other papers' summaries or my
background knowledge are marked (secondary), and should be checked before anything rests on them.

---

## 1. Kuhn's survey and the PENS scheme

Tobias Kuhn, "A Survey and Classification of Controlled Natural Languages", *Computational Linguistics* 40(1),
121-170, 2014; open copy at arXiv:1507.01701 (read). It surveys 100 English-based CNLs from 1930 on.

### 1.1 What counts as a CNL

A language is a CNL when all four hold (Definition 2.1):

1. it is based on exactly one natural language (its *base language*);
2. its most important difference from the base language is that it is more restrictive in lexicon, syntax and/or
   semantics (it does not add new constructs);
3. it keeps most natural properties of the base language, so that a speaker understands its texts "at least to a
   substantial degree" (Kuhn reads this later as naturalness N3 or higher);
4. it is explicitly and consciously defined.

Kuhn also notes the distinction between *proscriptive* rules (say what is forbidden; you start from full English)
and *prescriptive* rules (say what is allowed; you start from nothing). A GF grammar is purely prescriptive.

### 1.2 The property letters (Table 1)

Kuhn deliberately keeps these few and clear-cut. They describe a language's *environment*, not the language itself:

| Letter | Meaning |
|---|---|
| C | the goal is comprehensibility (communication among humans) |
| T | the goal is translation |
| F | the goal is formal representation, including automatic execution |
| W | intended to be written |
| S | intended to be spoken |
| D | designed for a specific, narrow domain |
| A | originated in academia |
| I | originated in industry |
| G | originated in a government or UN agency |

He mentions that Wyner et al. (2010) listed more than 40 properties of CNLs, but most were too fuzzy to classify by.

### 1.3 The four PENS dimensions

PENS = **P**recision, **E**xpressiveness, **N**aturalness, **S**implicity. Each has five classes, with English at
one end (P1 E5 N5 S1) and propositional logic at the other (P5 E1 N1 S5). A language is written as a code such as
`P4E3N4S3`. The four dimensions first appeared as "design principles" in Kuhn's thesis (*Controlled English for
Knowledge Representation*, University of Zurich, 2010), where precision was called "clearness".

**Precision**: how far a text's meaning can be read off its form alone.

| Class | Definition (paraphrase, with Kuhn's key words) |
|---|---|
| P1 imprecise | virtually every sentence is vague; automatic interpretation is "AI-complete". All natural languages. |
| P2 less imprecise | much less ambiguity and context dependence, but still too much for reliable automatic interpretation; usually no formal underpinning (ASD-STE100, Basic English). |
| P3 reliably interpretable | syntax heavily restricted, not necessarily formally defined; there is a logical underpinning, but mapping a sentence to it needs "external background knowledge, heuristics, or user feedback" (SBVR-SE, RuleSpeak, CPL). |
| P4 deterministically interpretable | syntax fully formal (a formal grammar); each text is "deterministically parsed" to a logic representation, or a small set of all and only the possible ones; the representation may be *underspecified*, needing "parameters, background axioms, external resources, or heuristics" for sensible deductions (ACE). |
| P5 fixed semantics | syntax and semantics fully formal; "each text has exactly one meaning, which can be automatically derived"; consistency and consequence are defined "with mathematical rigor" without heuristics or external resources (PENG, CLCE, Gherkin as typically used). |

**Expressiveness**: judged by five features, each counting only when it is "an integral part of the language and
not just manifested by a few special cases": (a) universal quantification over individuals (possibly limited),
(b) relations of arity greater than 1, (c) general rule structures (if-then with multiple universal quantification
that can target all argument positions of relations), (d) negation (strong or as failure), (e) second-order
universal quantification over concepts and relations.

| Class | Has |
|---|---|
| E1 | lacks (a) or (b) (propositional logic) |
| E2 | (a) and (b) (description logics) |
| E3 | (a)-(d) (first-order logic) |
| E4 | (a)-(e) (second-order logic) |
| E5 | anything two humans can communicate (natural languages) |

Kuhn uses Felleisen's weak notion: a construct adds expressiveness if removing it would force a global
reorganisation of the text.

**Naturalness**: closeness to the base language in readability and understandability.

| Class | Definition |
|---|---|
| N1 | looks unnatural: symbols, brackets, unnatural keywords |
| N2 | natural words present but dominated by unnatural elements; speakers "typically fail to intuitively understand" |
| N3 | natural elements dominate, but sentences are not valid natural sentences; understood "to a substantial degree" |
| N4 | sentences are valid natural sentences, understood without training; minor means of clarification (colour, capitalisation, hyphens) allowed if they do not break the flow; but whole texts are "very clumsy and repetitive" and lack natural flow (ACE) |
| N5 | whole texts read naturally |

**Simplicity**: the length of an exact and comprehensive description of syntax *and semantics* (vocabulary
excluded), written for a grammar engineer who must implement a full parser, at about 700 words per page.

| Class | Description length |
|---|---|
| S1 | cannot be described exactly (natural language) |
| S2 | much simpler than natural language but still no exhaustive description possible (SBVR-SE, RuleSpeak, CPL) |
| S3 | more than ten pages (ACE) |
| S4 | two to ten pages (first-order logic) |
| S5 | one page (propositional logic) |

### 1.4 Relatives of this CNL as Kuhn classifies them

| Language | Code | Letters | Note |
|---|---|---|---|
| ACE | P4E3N4S3 | F W A | DRS to first-order logic; content words open |
| PENG | P5E3N4S3 | F W A | first CNL with a predictive editor |
| SBVR Structured English | P3E4N4S2 | C F W I | business rules; necessity vs obligation |
| RuleSpeak | P3E4N4S2 | C F W I | no formal grammar |
| CPL (Boeing) | P3E3N4S2 | | heuristics, paraphrase back |
| Gherkin | P5E3N4S3 | F W D A | keywords fixed; the rest restricted by step definitions |
| PROSPER Controlled English | P4E3N4S3 | | hardware specifications, mapped to temporal logic |
| ucsCNL | P5E2N4S4 | | use case specifications for testing |
| TBNLS | P5E2N3S4 | | 15 templates for vehicle control software tests, propositional logic with temporal relations |
| RECON | P5E3N4S3 | | industrial facts and rules to first-order logic |
| Rabbit | P5E2N4S4 | | ontology authoring; "mixed results" in comprehension tests |

Kuhn reports strong correlations across the 100 languages (Spearman): precision with simplicity 0.90,
expressiveness against simplicity -0.82, naturalness with expressiveness 0.77, naturalness against simplicity -0.76,
precision against naturalness -0.67. That is the trade-off in numbers: precise languages tend to be simple, and
simple languages tend to be less natural and less expressive. He insists PENS describes a language's nature, not its
quality: it is for placing a language, not ranking it.

### 1.5 How to score this repository's CNL (a starting point for a later phase)

| Dimension | Provisional class | Why, and what would move it |
|---|---|---|
| P | P4, with P5 islands | GF syntax is formal and the corpus demands exactly one tree. But the meaning of a large part of each line lives outside the logic: 142 of 167 conditions are prose (an opaque atom), and translation is fixed fun by fun in `spec_facts.py` rather than by a compositional semantics. That is Kuhn's "underspecified ... external resources". Lines whose every condition is defined are close to P5 for the two-state reading `check.lp` gives them. |
| E | E2, arguably weak E3 | (a) `every` exists but in limited positions; (b) binary relations exist (relation rows, verb frames); (d) negation exists (`shall not`, `is not`). (c) general rules with several universally quantified variables in any argument position is doubtful: EARS clauses with "a ... the" give one implicit universal per kind. Whether (c) is "integral" decides E2 vs E3. |
| N | N4 (texts N3-N4) | Lines are mostly valid English sentences; backticked codes and `` `work` `` as subject are allowed clarifications. A capability's behaviour section reads, as Kuhn says of N4, "clumsy and repetitive". |
| S | S3 | A full description must cover `Req.gf`, the generated modules' patterns, the translation to facts and `check.lp`: well over ten pages. |
| Letters | F W D (I) | The goal is formal (facts, Gherkin); written; the core holds domain funs (`Print`, `ExitOk`, `Runs` a command, `Hold` a resource), so narrow-domain; neither academic nor government. |

---

## 2. Design principles from the literature

### 2.1 Fixed function words, open content words, defined meanings

ACE's vocabulary is predefined *function words* (determiners, quantifiers, coordinators, negation, pronouns, the
copula, modal auxiliaries, the Saxon genitive) and fixed phrases ("there is", "it is false that"), which users cannot
change, plus open *content words* (nouns, proper names, verbs, adjectives, adverbs, prepositions) that users add
(ACE construction rules, attempto.ifi.uzh.ch (read); Schwitter 2010 (read)). Crucially, Schwitter notes that in ACE
"the meaning of words ... is not predefined; the user is expected to define their meaning by ACE sentences or import
these definitions from an existing formal ontology." The structure that carries logic is in the closed class; the
open class is only names.

**Here: partly follows, partly breaks.** The closed core (`Req.gf`) plus open glossary entries is the same split.
But (i) the meaning of most content words is given in prose, not in the CNL (142 of 167 conditions), which is
exactly what ACE avoids; and (ii) the closed class is thin, so meaning that ACE would carry in function words
(relative clauses, "whose", "of", counts, "no ... that") is pushed into coined content words ("listless",
"idless", "idle"). This is the person's complaint in b112, and the literature backs it: definitions belong in the
language itself.

### 2.2 One word, one meaning

ASD-STE100 (Simplified Technical English, aerospace) is built on "one word, one part of speech, one meaning":
each approved word may be used only in its listed part of speech and meaning; "test" is approved as a noun, not as
a verb; a meaning not in the dictionary may not be used. Technical names and technical verbs specific to a product
form an open, separately kept vocabulary (Wikipedia, "Simplified Technical English" (read); asd-ste100.org
(secondary)). The same principle runs through Basic English and most C-type CNLs.

**Here: breaks.** Ordinary English adjectives are given domain meanings, sometimes several by kind: `closed` has four
definitions (request, capability-proposal, glossary-proposal, work-item), `open` two, `malformed` four, `present`
three (`spec/index.md`, `spec/capabilities/*.md`). "Free", "clean", "idle", "quiet" each mean something a reader
cannot guess. STE would allow a technical noun or verb, but not a reassigned common adjective.

### 2.3 Interpretation rules: one reading, predictable

ACE is defined by *construction rules* (which sentences are allowed) and *interpretation rules* (which single
reading each gets). Every ACE sentence has exactly one meaning, and because the rules are fixed a reader can predict
it. Examples: prepositional phrases attach to the verb; a relative clause modifies the noun just before it; "and"
binds tighter than "or", and ", and" / ", or" override; "a" is existential, "every" universal; quantifier scope runs
to the end of the sentence or coordinated clause; noun phrases are inaccessible for later reference inside negation,
modal sentences, universal sentences and the consequent of an if-then, but a noun phrase in an if-clause is
accessible in the then-clause; a definite noun phrase resolves to the most recent, most specific antecedent, or
introduces a new entity; passives must name the agent with "by" (ACE interpretation rules, attempto.ifi.uzh.ch
(read)). CLCE and SQUALL likewise resolve every ambiguity by fixed rules at parse time (Kuhn 2014).

**Here: unclear, likely partly broken.** The grammar guarantees one *tree*, but there is no written set of
interpretation rules telling a reader what "a" and "the" mean in a While clause, under `shall not`, or across
responses. The answer is in `spec_facts.py`'s per-fun code (hypothesis 1 and 2 of the context file). An ACE-style
rule list, short enough to put in front of a writer, is the cheap fix even before any change to the logic. ACE's
mandatory "by"-agent on passives matches the person's rule that an agentless passive is a fault.

### 2.4 A formal semantics, compositionally defined

The "logical era" CNLs (Kuhn 2014, from the mid-1990s) map sentences to logic by a defined route: ACE via Discourse
Representation Structures (Kamp and Reyle 1993) to first-order logic; PENG the same with anaphora resolved during
parsing (Schwitter 2010 (read)). Schwitter's summary of what an ideal machine-oriented CNL needs starts with "(a) a
well-defined syntax and a precise semantics that is defined by an unambiguous mapping into a logic-based
representation". In GF terms, Angelov and Ranta ("Implementing Controlled Languages in GF", CNL 2009, LNCS 5972,
2010 (secondary)) recommend treating the abstract syntax as the semantic representation, and building concrete
syntax on GF's Resource Grammar Library so that agreement, inflection and word order come for free.

**Here: breaks in part.** The abstract syntax is close to semantics (typed funs per frame), but the meaning of
each fun is decided case by case in Python, and `ReqEng.gf` concatenates strings rather than using the RGL. Both
make each new sentence structure costly, which may be one reason the core has so few (hypothesis 1).

### 2.5 Paraphrase back to the writer

ACE ships a paraphraser that "reflects the interpretation of the machine in CNL"; CPL makes a best guess and
paraphrases the logic back for the user to confirm; PENG generates a paraphrase for each sentence entered (Schwitter
2010 (read); Kuhn 2014 (read)).

**Here: partly follows.** `model parse` shows the tree, and the generated Gherkin is a kind of paraphrase of the
facts, but nothing shows a writer, in English, the reading of a line (which "a" is universal, which "the" refers
where, what state holds before and after). A paraphrase from the facts would make the hidden interpretation rules
visible.

### 2.6 Writing support: error messages, conceptual authoring, predictive editing

Schwitter (2010, read) names three techniques: *error messages* (the writer learns the rules; on failure the system
suggests a fix; weakness: a useful message for an arbitrary unrestricted sentence needs near full natural language
understanding), *conceptual authoring* or WYSIWYM (edit the model through menus; weakness: cannot say anything not
already in the knowledge base), and *predictive feedback* (a look-ahead editor that shows, after each word, which
categories and words may come next, so the writer cannot leave the language). PENG was built for it (ECOLE,
Schwitter et al. 2003); Kuhn's thesis experiments found predictive editors usable by untrained users and he argues
it is the best support (Schwitter 2010, reporting Kuhn 2010). Kuhn later gave grammar requirements for predictive
editing, the Codeco notation ("A Principled Approach to Grammars for Controlled Natural Languages and Predictive
Editors", *J. Logic, Language and Information* 22(1), 2013 (secondary)).

**Here: follows the weakest technique.** Writing support is error messages: a refusal with a hint (`spec_grammar`)
and the frame refusal naming the verb and role (`spec_frames.refusal`). The writers are mostly LLM sessions, which
changes the calculus (they recover from messages cheaply), but GF's PGF runtime supports completion, so look-ahead
("what may follow `While a request`") is available at low cost and would show writers the structures that exist
instead of letting them coin an adjective.

### 2.7 Habitability: easy to read, hard to write

The standing failure mode of CNLs is that they are easy to read and hard to write: a reader needs no training, but
a writer must stay inside invisible bounds (Schwitter 2010: writing "requires that the author either learns the
language ... or that he uses an intelligent authoring tool"). The older name is *habitability* (W. C. Watt,
"Habitability", *American Documentation* 19(3), 1968 (secondary)): a language is habitable when users can say what
they need without stepping outside it. When a CNL is not habitable, writers route around it: they bend a supported
structure to carry a meaning it was not made for.

**Here: this is the observed failure.** The coined adjective with a prose definition is exactly a writer routing
around a missing structure: the While slot accepts only "X is <adjective>", so any state that needs a relation,
count, negated existential or reference to an external artifact becomes a new adjective. 170 adjective entries
across the glossary and capability terms is a habitability measurement.

### 2.8 The naturalness / precision / expressiveness trade-off is deliberate

Kuhn (2014) frames the designer's two key questions as "How expressive should the resulting language be, and how
natural?", and the correlations in section 1.4 show that adding precision usually costs naturalness. Schwitter's
four requirements (well-defined semantics; as natural as possible; easy to write, understand and process;
expressive enough for the domain) "can be in conflict with each other and therefore careful compromises need to be
made". Kuhn's examples: KCE's SGML tags raise precision but "heavily impede its naturalness"; EasyEnglish's
restrictions are only suggested, so it is no more precise than English.

**Here: unclear.** The repository has optimised for precision (one tree, guards) and simplicity of the core, and
paid in expressiveness; the payment then leaks back into prose definitions, which lowers effective precision. A
design should state its target PENS code explicitly.

### 2.9 A small number of sentence patterns does not scale

CLOnE has eleven sentence patterns matching eleven OWL axiom patterns, and Schwitter (2010) remarks it is "unclear
whether CLOnE can be extended in a systematic way to cover larger fragments of OWL". The general-purpose CNLs that
lasted (ACE, PENG) instead have a compositional grammar: noun phrases with relative clauses, quantifiers,
coordination and negation that combine freely.

**Here: breaks.** The core is a fixed list of EARS forms with a few slot fillers (`Holds`, `IsFree`, `Print`,
`ExitOk` ...), and the rule in `Req.gf` that a core fun is added only for a construct recurring in two
capabilities keeps it pattern-like. Noun phrases have no relative clauses, no "whose", no general "of"
(hypothesis 8).

### 2.10 Vocabulary kept by type, with definitions as rules

SBVR Structured English (OMG, *Semantics of Business Vocabulary and Business Rules*, 2008 (secondary)) keeps four
kinds of constituent, each typeset differently: terms (concepts), names (individuals), verbs (fact types, i.e.
relations) and keywords. A concept is defined in the vocabulary, with definitions that are themselves rules.
SBVR separates *definitional (structural) rules*, "It is necessary that ...", from *behavioural (operative) rules*,
"It is obligatory that ...", with "It is possible / permitted that ..." as their duals. Gellish builds on a fixed
upper ontology of relation types (Kuhn 2014).

**Here: partly follows.** Nouns, proper nouns (actors), verbs with frames and relation rows match SBVR's terms,
names and fact types well; plugin 3.0's frames are a step towards SBVR fact types. Missing: SBVR's split between
necessity and obligation (only `shall` / `shall not`; hypothesis 4), and conditions as first-class fact types
rather than adjectives.

### 2.11 Evaluate with users, not only by coverage

Schwitter (2010) groups CNL evaluations into task-based (write with a tool), paraphrase-based (choose the right
natural paraphrase) and graph-based experiments (Kuhn 2010: judge statements true or false against a diagram;
also Kuhn, "The Understandability of OWL Statements in Controlled English", *Semantic Web* 4(1), 2013
(secondary)). Kuhn (2014) concludes that results depend on "the precise problem domain, the background of the
users" and the design quality.

**Here: not done.** There is a parse/refuse corpus (`grammar/corpus/`), which tests coverage, not
understandability or writability. A later phase could run a small task-based test: give a writer (a session) a
behaviour in English and count how often it reaches for a new adjective.

---

## 3. CNLs for requirements

### 3.1 EARS

Mavin, Wilkinson, Harwood and Novak, "Easy Approach to Requirements Syntax (EARS)", RE'09, 2009 (read). Five
patterns keyed by a leading word, with the system response always "the <system> shall <response>": ubiquitous (no
keyword), event-driven (When), state-driven (While), unwanted behaviour (If ... then), optional feature (Where),
and complex combinations. The authors chose it against heavier notations because "use of any of these non-textual
notations often requires complex translation", and "requirements authors are unlikely to seek excessive formality
and complex training". In their case study the templates removed complexity, omission (with caution), duplication,
implementation detail and untestability, but ambiguity, vagueness and wordiness were "reduced, but not eliminated",
due to lexical ambiguity (a precondition understood by inference but not written), the innate vagueness of high-level
requirements, and clumsy long requirements with many conditional clauses. Limits they state: 36 requirements, all
high-level safety requirements; "other types ... may exist that cannot be adequately represented". Follow-ups:
"Big EARS" (Mavin and Wilkinson, RE'10) and "Listens Learned (8 Lessons Learned Applying EARS)" (Mavin et al.,
RE'16) (both secondary; I could not reach the text). Practitioner guidance recommends EARS for requirements with few
preconditions and decision tables when conditions multiply (secondary, search summaries).

The key point for b112: **EARS constrains clause order, not clause content.** "While <precondition>" and "When
<trigger>" are free English in EARS. It was designed for human readers (Kuhn's C type), not as a formal language.
Using EARS as the *whole* grammar of an F-type CNL leaves the inside of each clause to be invented; this repository
filled the While slot with "X is <adjective>" and that is where the coined adjectives come from.

**Here: follows EARS faithfully, and inherits its gap.** The ten forms of `Req.gf` are EARS and its combinations.

### 3.2 Rupp's template (MASTeR) and boilerplates

Chris Rupp's SOPHIST template (MASTeR, in Pohl and Rupp's IREB study guide) fixes slots: an optional condition,
the system, a legal obligation keyword (shall / should / will, i.e. mandatory / desired / intended), a kind of
activity (independent: "<process verb>"; user interaction: "provide <whom> with the ability to <process verb>";
interface: "be able to <process verb>"), then object and its details (secondary: Monett lecture slides; Mazo et al.
2019). The point of interest is that the template names *process verbs* as the core of a requirement and
recommends defining each one precisely, as this repository's verb frames now do; and it grades obligation, which
EARS does not.

Mazo, Jaramillo, Vallejo and Medina, "Towards a new template for the specification of requirements in
semi-structured natural language", *J. Software Engineering Research and Development* 8:3, 2019/2020 (read in part)
report that "anyone who has used the Rupp template in real projects has realized that some requirements cannot be
expressed with that structure without some degree of ambiguity or inconsistency", and that templates fail for some
functional and non-functional requirements and constraints and for self-adaptive, product-line and embedded systems
(e.g. no slot for the other system a message goes to or from; no way to say a requirement is variable across a
product line).

Boilerplates (Hull, Jackson and Dick, *Requirements Engineering*, Springer; the CESAR project) are fixed templates
with placeholders. Arora, Sabetzadeh, Briand and Zimmer showed conformance can be checked automatically by text
chunking, noting that manual checking is "laborious and error prone" and that industrial glossaries are often
incomplete (ESEM 2013; RePa 2014; Arora's thesis, Luxembourg 2016) (secondary: abstracts). A boilerplate checker
only checks shape: like EARS, boilerplates leave the placeholders' content free.

**Here: follows the template idea, goes further than boilerplates (it parses the content too), and lacks graded
modality.**

### 3.3 Requirements CNLs with a formal semantics

These are closer to what b112 wants than EARS or Rupp, because they give the inside of each clause a meaning:

- **Property specification patterns** (Dwyer, Avrunin and Corbett, ICSE 1999; real-time extension with a
  structured English grammar by Konrad and Cheng, ICSE 2005) (secondary). Each requirement = a *scope* (globally,
  before Q, after Q, between Q and R, after Q until R) plus a *pattern* (absence, universality, existence, response,
  precedence, bounded existence ...), each mapped to LTL/CTL/MTL. Directly addresses "only after", "always", "at most
  n times" (hypotheses 3 and 5) and the person's split into structural, transition and liveness rules.
- **FRETish** (NASA FRET; Giannakopoulou, Pressburger, Mavridou, Rhein, Schumann and Shi, "Formal Requirements
  Elicitation with FRET", 2020) (secondary). Fields: scope, condition, component, *shall*, timing, response; each
  requirement is formalised in past- and future-time metric temporal logic, and the tool explains its meaning back
  in English and as a timing diagram (paraphrase back, 2.5).
- **PROSPER Controlled English** (P4E3N4S3, hardware specifications to temporal logic), **TBNLS** (15 templates with
  temporal relations), **ucsCNL** (use cases for testing) (Kuhn 2014, read).
- **RELAX** (Whittle et al., RE'09) (secondary): temporal and uncertainty operators (UNTIL, AFTER, AS EARLY AS
  POSSIBLE) for self-adaptive systems; used by Mazo et al. as a reference.
- **ACE for specifications**: Fuchs, Schwitter and Schwertel, "Attempto Controlled English: Not Just Another Logic
  Specification Language" (LOPSTR 1998) (secondary), and Schwitter's note that ACE's applications include "software
  and hardware specifications" (2010, read).

**Here: unclear.** None of these is used. The scope/pattern split of Dwyer et al. and FRETish's timing field are the
nearest proven answers to the two-state limit.

---

## 4. Known failure modes of CNLs in practice

1. **Hard to write** (2.7): habitability failures push writers into workarounds. Observed here as coined adjectives.
2. **Restrictions not enforced**: a CNL without a checker drifts back to English (EasyEnglish; Global English has
   no checking tool) (Kuhn 2014). *Here: avoided*: every line is parsed and refused.
3. **Hidden interpretation**: users cannot predict the reading, so they mistrust or misuse it; the remedy is
   written interpretation rules and paraphrase (2.3, 2.5). *Here: present.*
4. **Pattern lists that do not compose** (CLOnE, 2.9). *Here: present.*
5. **Vocabulary drift and polysemy**: one word, several meanings (2.2). *Here: present.*
6. **Templates that leave content free** (EARS, boilerplates, 3.1-3.2): the shape is checked, the meaning is not.
   *Here: avoided for most slots, present for conditions, through prose definitions.*
7. **Domain fit**: CNL results depend on domain and users (Kuhn 2014); requirements templates fail for system types
   they were not built for (Mazo et al.). *Here: the core holds domain funs (`Print`, `ExitOk`, `Runs`), which ties
   the grammar to command-line tools.*

---

## 5. Summary: practices against this repository's CNL

| Practice | Source | Here |
|---|---|---|
| Closed function words, open content words | ACE; Schwitter 2010 | follows the split; closed class too thin |
| Content words' meaning defined in the CNL itself | ACE; SBVR | **breaks** (142/167 conditions prose) |
| One word, one part of speech, one meaning | ASD-STE100 | **breaks** (`closed` x4, `open` x2, common words reassigned) |
| Written interpretation rules; one predictable reading | ACE; CLCE | unclear: one tree, reading only in code |
| Compositional formal semantics | ACE (DRS); PENG; GF abstract syntax | partial: per-fun translation |
| Agent explicit; passive needs "by" | ACE | follows (person's rule) |
| Paraphrase the reading back | ACE; CPL; PENG; FRET | partial (tree, Gherkin), no English reading |
| Predictive / look-ahead writing support | PENG; Kuhn 2010, 2013 | breaks: error messages only (GF could complete) |
| Restrictions enforced by a checker | Kuhn 2014 | follows |
| Compositional NPs (relative clauses, of, whose, counts) | ACE; PENG | **breaks** |
| Explicit trade-off target (PENS) | Kuhn 2014; Schwitter 2010 | unclear |
| Typed vocabulary: terms, names, fact types, keywords | SBVR | follows (frames, relations, actors) |
| Necessity vs obligation; graded modality | SBVR; Rupp | **breaks** (shall / shall not only) |
| Clause order by EARS | Mavin et al. 2009 | follows, inherits free clause content |
| Scope and temporal patterns for ordering, liveness | Dwyer et al. 1999; FRETish | absent |
| User evaluation of reading and writing | Kuhn 2010; Schwitter 2010 | absent (coverage corpus only) |

---

## 6. Sources and confidence

Read in full or in the relevant part:

- T. Kuhn, "A Survey and Classification of Controlled Natural Languages", *Computational Linguistics* 40(1):121-170,
  2014. https://arxiv.org/abs/1507.01701
- R. Schwitter, "Controlled Natural Languages for Knowledge Representation", COLING 2010 (posters), 1113-1121.
  https://aclanthology.org/C10-2128.pdf
- A. Mavin, P. Wilkinson, A. Harwood, M. Novak, "Easy Approach to Requirements Syntax (EARS)", RE'09, 2009.
- R. Mazo, C. A. Jaramillo, P. Vallejo, J. H. Medina, "Towards a new template for the specification of requirements
  in semi-structured natural language", *JSERD* 8:3, 2020. https://distantreader.org/stacks/journals/jserd/jserd-473.pdf
- Attempto: ACE construction rules and interpretation rules (ACE 6.7).
  http://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html,
  http://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html
- "Simplified Technical English", Wikipedia. https://en.wikipedia.org/wiki/Simplified_Technical_English

Known from abstracts, summaries or background, to be checked before relying on details:

- A. Wyner et al., "On Controlled Natural Languages: Properties and Prospects", CNL 2009, LNCS 5972, 2010
  (doi:10.1007/978-3-642-14418-9_17). Full text not reached; cited only through Kuhn's remark about its 40+ properties.
- T. Kuhn, *Controlled English for Knowledge Representation*, PhD thesis, University of Zurich, 2010.
- T. Kuhn, "A Principled Approach to Grammars for Controlled Natural Languages and Predictive Editors", *JoLLI*
  22(1), 2013; "The Understandability of OWL Statements in Controlled English", *Semantic Web* 4(1), 2013.
- N. E. Fuchs, K. Kaljurand, T. Kuhn, "Attempto Controlled English for Knowledge Representation", Reasoning Web
  2008, LNCS 5224.
- K. Angelov, A. Ranta, "Implementing Controlled Languages in GF", CNL 2009, LNCS 5972, 2010.
- OMG, *Semantics of Business Vocabulary and Business Rules (SBVR)*, 2008.
- A. Mavin, P. Wilkinson, "Big Ears", RE'10; A. Mavin et al., "Listens Learned (8 Lessons Learned Applying EARS)",
  RE'16 (doi:10.1109/RE.2016.38).
- C. Arora, M. Sabetzadeh, L. Briand, F. Zimmer, boilerplate conformance checking, ESEM 2013 and RePa 2014;
  C. Arora, PhD thesis, University of Luxembourg, 2016.
- M. Dwyer, G. Avrunin, J. Corbett, "Patterns in Property Specifications for Finite-State Verification", ICSE 1999;
  S. Konrad, B. Cheng, "Real-time Specification Patterns", ICSE 2005.
- D. Giannakopoulou et al., "Formal Requirements Elicitation with FRET", 2020 (NASA NTRS).
- J. Whittle et al., "RELAX: Incorporating Uncertainty into the Specification of Self-Adaptive Systems", RE'09.
- W. C. Watt, "Habitability", *American Documentation* 19(3), 1968.
- C. Rupp and SOPHIST, MASTeR templates; K. Pohl, C. Rupp, *Requirements Engineering Fundamentals* (IREB).
