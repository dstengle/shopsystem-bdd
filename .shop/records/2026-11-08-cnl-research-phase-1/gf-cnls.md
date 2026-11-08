# GF as a platform for controlled languages, and how this repository uses it

Phase 1 research for b112, strand: Grammatical Framework (GF). Researched 2026-11-08 from the web and from main's
checkout. I compiled and ran a throwaway spike against the GF Resource Grammar Library (RGL) in the session scratchpad
(section 4). Nothing in the repository was changed apart from this file.

## 1. Summary

- GF was built for this kind of work. Ranta and Angelov's "Implementing Controlled Languages in GF" (CNL 2009) uses
  Attempto Controlled English (ACE) as its worked example. Their method: write the CNL as an **application grammar**
  (a small, domain-shaped abstract syntax). Its concrete syntax calls the **RGL** for morphology and syntax
  (agreement, relative clauses, negation, coordination, genitives), so the CNL author never writes those strings by
  hand.
- **This repository does not use the RGL.** `grammar/CoreEng.gf` says so itself: "There is no RGL: records carry
  agreement only where English needs it (number of a noun phrase)." Every surface form is a hand-written string,
  generated per kind, attribute, condition, relation row and verb frame. The cost is concrete: the main grammar
  has **4,841 generated funs**, of which **672 exist only to say "not"**. There is a live **agreement defect**:
  "When sessions writes a file, ..." parses, and "When sessions write a file, ..." is refused with a misleading
  message (section 3.2). There are no relative clauses with a verb ("a channel that a viewer subscribes to"), and no
  genitive ("the request's credentials").
- An RGL-based application grammar would keep this repository's best idea unchanged: typed categories generated per
  kind and frame, with ambiguity refused when two trees survive. Only the linearisations change. My spike parses
  the three target constructions with typing intact. It also showed the RGL's defaults that would need overriding:
  contracted "doesn't", no comma after an adverbial clause, and "which"/"that".
- The risks are smaller than feared, measured on the spike. The RGL's English API compiled cold in about 0.5 s. A
  generated RGL-based grammar of 320 kinds and 160 verbs (about 2,560 funs) compiled in 6.1 s, with a PGF of 860 KB.
  For comparison, this repo's own grammar (4,841 funs) compiles in 0.7 s to a 766 KB PGF. Parsing 20-30-token
  sentences took about 4 ms. Ambiguity in an application grammar comes from the abstract syntax you expose, not
  from the RGL behind it. Compile time grows by roughly 10x per fun, which the existing sha-keyed PGF cache absorbs.
- GF gives no **semantics** by itself. ACE-in-GF leaves meaning to ACE's own DRS pipeline (APE). AnaCon (contracts)
  translates GF trees to a separate formal language, CL. Abstract syntax trees *can* serve as the logical form
  (Ranta 2011), but someone still writes the tree-to-logic translation. This confirms hypothesis 1 of the context,
  and GF cannot fix it alone (section 5).

## 2. GF's own CNL work

| Work | What it shows | Source |
|---|---|---|
| Ranta & Angelov, "Implementing Controlled Languages in GF", CNL 2009 (CEUR 448); extended LNCS 5972 (2010), pp. 82-101 | Builds a CNL as an application grammar over the RGL. The worked example is ACE 6.0's construction rules in GF, ported to French, German and Swedish (Finnish and Italian in the LNCS version). Authoring aids and translation come with the grammar. | research.chalmers.se/en/publication/105696; research.chalmers.se/publication/131247 |
| Kaljurand & Kuhn, "A Multilingual Semantic Wiki Based on Attempto Controlled English and Grammatical Framework", ESWC 2013 (arXiv 1303.4293) | ACE-in-GF in production (AceWiki-GF). The English grammar "accesses the GF English resource grammar through the language-independent API". About 30 RGL-based modules and about 100 linearisation rules. Covers all 19,422 Codeco test sentences (up to 10 tokens). About 3% of the sentences were ambiguous, all harmlessly so. In other languages, reparsing found "semantically severe" ambiguities (subject vs object relative clauses in Dutch and German, double negation in Romance languages). A look-ahead editor shows only legal continuations. Adding a word is "a line" on a lexicon page. OWL output goes through ACE's APE, not GF. | ar5iv.arxiv.org/html/1303.4293 |
| MOLTO, FP7 grant 247914, 2010-2013 | "Multilingual controlled language systems": domain-specific semantic grammars in GF, choosing precision over coverage. Outcome: the GF web tools (cloud editor, Minibar, the web service with completion), still maintained by the GF community. | cordis.europa.eu (MOLTO annual report 2011); Ranta, MT Summit 2013 (aclweb.org/anthology/2013.mtsummit-european.12) |
| Angelov, "Incremental Parsing with Parallel Multiple Context-Free Grammars", EACL 2009 | GF's parser is top-down and incremental on PMCFG directly, which makes **word completion** possible for any compiled grammar with no extra work. The PGF web service exposes a `complete` call. Angelov & Ljunglöf (EACL 2014) add statistical ranking. | research.chalmers.se/en/publication/82866; research.chalmers.se/publication/205189 |
| Ranta, "The GF Resource Grammar Library", LiLT 2(2), 2009 | The RGL (now about 40 languages) and the split between **resource** grammars (linguistic structure) and **application** grammars (domain semantics). It notes that resource structures do not always give translation equivalence. | journals.colorado.edu/index.php/lilt/article/view/1205 |
| Ranta, "Translating between Language and Logic: What Is Easy and What Is Difficult", CADE-23, LNCS 6803, 2011, pp. 5-25 | Simple NL interfaces to formal systems are easy with GF: the abstract syntax is the logic's syntax, linearised into language. Full generality (anaphora, quantifier scope, idiomatic paraphrase) is hard. | doi 10.1007/978-3-642-22438-6_3 |
| Angelov, Camilleri & Schneider, "A Framework for Conflict Analysis of Normative Texts Written in Controlled Natural Language" (AnaCon), JLAP 82, 2013 | A GF CNL for contracts, translated into the contract logic CL. The CLAN tool finds conflicting obligations and permissions, and GF renders the counterexamples back into CNL. This is the closest published analogue to this repo's parse → facts → clingo → findings loop. | research.chalmers.se/en/publication/181436 |
| Camilleri, Paganelli & Schneider, "A CNL for Contract-Oriented Diagrams", CNL 2014 | A GF CNL front-end over C-O diagrams with a conflict checker behind it. | cse.chalmers.se/~gersch/cnl2014.pdf |
| Listenmaa, Hanafiah, Cheong & Källberg, "Towards CNL-based Verbalization of Computational Contracts", CNL 2021 | L4 (SMU computational law) generates its CNL with GF **on the RGL**, with legal constructions added on top. It explicitly leaves semantics to the L4 DSL and resolves ambiguity interactively. | aclanthology.org/2021.cnl-1.10 |
| Pathak, "GFLean", arXiv 2404.01234, 2024 | Recent GF use: parses simple mathematical English and linearises it to Lean. | ar5iv.labs.arxiv.org/html/2404.01234 |

On GF and LLMs, I found no substantial published 2024-25 work that couples GF with LLMs as a CNL authoring aid. One
search turned up only grammar-constrained decoding work (GRAMMAR-LLM, ACL Findings 2025) that is not GF-based. I am
unsure here and did not search exhaustively. An authoring pattern of "the LLM drafts, the GF parser accepts or
refuses with a hint" is what this repo already does, with `spec_grammar.hint`.

**Dependent types.** GF's abstract syntax allows dependent types. The tutorial's example lets you "dim a light" but
not "dim a fan", through a `Kind` index (GF tutorial, Lesson 5, "A dependent type system"). Parsing with them is a
context-free parse followed by "filtering through type checker". Only the Haskell runtime does that check. Angelov
on gf-dev (2019): "dependent types were never fully implemented so I wouldn't count on them". The C runtime, which
this repo uses through the `pgf` Python wheel, does not check them (groups.google.com/g/gf-dev/c/8HkK7mYg9Gs). This
repo's choice, one generated category per kind (`k_channel_NP`, `<T>_Sb`, `<T>_Ob`), is therefore the right
engineering for GF's C runtime: it gets typing from plain categories, which every runtime enforces during the
parse. The cost is a module that grows with the glossary.

**Lexicon tools.** The RGL's "smart paradigms" (`mkN "viewer"`, `mkV "subscribe"`, `mkV2 v (mkPrep "to")`) build full
paradigms from one or two forms (Détrez & Ranta, "Smart paradigms and the predictability and complexity of
inflectional morphology", EACL 2012). `spec_typed.plural` and `event_forms` hand-roll a small subset of this. There
is also gf-wordnet, a large GF lexicon aligned with WordNet (Angelov, LREC 2020). It would let glossary entries
point at senses, but that is beyond what b112 needs.

## 3. How this repository uses GF

### 3.1 The shape

- `Core.gf` declares about 17 shared categories. `Req.gf` holds the EARS forms (`When`, `While`, `WhileWhen` ...),
  `Shall`/`ShallNot`, and coordination of verb phrases and responses. `Steps.gf` adds Gherkin step funs.
- `spec_typed.py` generates `Lex`/`Typed` from the glossary. Each kind gets `_CN`/`_NP` categories and nine
  determiner funs (`An`, `Every`, `The`, `No`, `AtMostOne`, `One`, `Pl`, `Its`, plus `Named`, `It`, `NumberOf`).
  Each attribute gets `_ThatIs`/`_ThatIsNot`/`_Whose`/`_WhoseNot`/`_Pre`/`_Is`/`_IsNot`/`_Becomes`/`_Set`/`_Of`.
  Each condition gets `_Pre`/`_ThatIs`/`_ThatIsNot`/`_Is`/`_IsNot`. Each relation row gets a modifier and
  `_Atom`/`_AtomNot`.
- `spec_typed_verbs.py` generates, per verb frame, `__Happens`, `__Do`, `__Does`, `__DoesNot`, `__DoTo`, steps and so
  on, over `<T>_Sb`/`<T>_Ob` categories filled by every kind below T.
- `spec_typed_def.py` adds a `Def` grammar ("a K is C when Cond.").
- `spec_grammar.py` compiles with gf 3.12 into a PGF cached by the sha of the sources, parses with the C runtime
  (`pgf` 1.1), caps the parse at 2,000 trees (`LIMIT`), keeps GF's parses on disk (`spec_parse_cache`), applies
  post-parse guards, and refuses a line with zero or more than one surviving tree.

I generated this repo's grammar into the scratchpad and measured it. The sources come to 8,844 lines. `Typed.gf`
has 4,841 funs, and 672 of them end in `Not`. gf compiles `ReqEng.gf` in 0.7 s, and `Req.pgf` is 766 KB.

### 3.2 What hand-written strings cost

| Concern | How the repo does it | Cost |
|---|---|---|
| Subject-verb agreement | `NPr` carries `n : Number`, but a verb frame's subject `<T>_Sb` has `lincat = Str`. `e__Happens s x = s ++ t ++ x.s` always uses the third-person-singular form. | **Defect, reproduced:** `model parse "When sessions writes a file, ..."` gives a tree with `k_session_Pl`. `"When sessions write a file, ..."` is refused with "the verb write takes as its subject agent or a kind of it", which names the wrong cause. |
| Negation | A separate fun for every positive form: `_IsNot`, `_ThatIsNot`, `_WhoseNot`, `_AtomNot`, `__DoesNot`, `__SDoesNot`, `__SDoesToNot` ... | 672 funs. Every new construction has to be written twice, and polarity is not a parameter the facts layer can read uniformly. |
| Relative clauses | Only "that is V/C" (copular) and the relation row's "that has X". No relative clause built from a verb frame, no object relative ("a channel that a viewer subscribes to"), no "whose" except attribute values. | Hypothesis 8 of the context, confirmed in the code. |
| Of-phrase / genitive | "the status of X" for attributes (`attrOf`), and a relation row whose word ends in a preposition (`file of initiative` gives "a file of the initiative"). No "'s". | An "of" row is fixed to one preposition per kind pair, and the determiner is always singular (`det "the" cn` takes `cn.s ! Sg`), so a plural-only noun like "credentials" reads wrongly. |
| Coordination | `AndVP`/`OrVP`/`AndResp`/`CondAnd`/`CondOr`/`MoreNP`, each with its own `Many` bookkeeping for the Oxford-comma pattern. | NP coordination does not affect agreement ("a file and a directory is ..."). |
| Morphology | `spec_typed.plural` (regular rules) plus glossary `Forms:`. `art` handles a/an by `pre`. | Works for this lexicon. Irregulars rely on authors. |

None of this makes the grammar ambiguous. It makes it **thin**: each construction is hand-built for each kind, so
adding one (a relative clause, "may", a count) multiplies funs and is costly to justify. That supports the owner's
diagnosis that meaning gets packed into coined adjectives instead.

### 3.3 What building on the RGL would change

- **The lincats change, the abstract syntax barely does.** `<T>_NP = NP` (RGL), `Atom = Cl` (RGL clause: tense and
  polarity left open), `Cond`/`Resp = S`. A verb frame becomes a `V2`/`V3` built with `mkV2 (mkV "subscribe")
  (mkPrep "to")`, and agreement, "does not", the third-person -s and preposition stranding all come from the RGL.
- **Negation becomes a parameter.** One `Pos, Neg : Atom -> Cond` (or a `Pol` argument) replaces the `*Not` funs.
  The facts layer then reads one `Neg` node instead of 15 fun suffixes, which is better for spec_facts too.
- **New constructions are cheap per frame**: object and subject relative clauses (`mkRCl which_RP (mkClSlash np
  v2)`), genitives (`ExtraEng.GenNP`), "may"/"must" (`auxVV`), counts (`mkDet (mkNumeral ...)`), and comparatives.
  Each is a generator line, not a new hand-written string table.
- **The guards and refusal model stay**: typed categories, two-tree ambiguity refused, the hint, the parse cache.
- **Multilinguality comes free but is not wanted here.** The ACE experience is that other languages bring in
  severe ambiguities, so keep English only.

## 4. Spike: the three constructions in an RGL-based typed grammar

I did compile this. I downloaded gf-rgl tag `20250812` into the scratchpad (sources of `abstract`, `common`,
`prelude`, `english`, `api` only) and compiled it with the repo's gf 3.12. The files are in
`/tmp/claude-1000/-home-vscode-shopsystem-bdd/72e23fa5-6dee-49f3-a1d1-7e79096a0501/scratchpad/b112/gf-spike/`
(`Spike.gf`, `SpikeEng.gf`, `scale/gen.py`). Abridged:

```gf
abstract Spike = {
  cat Req ; Resp ; Cond ; Atom ; Viewer_CN ; Viewer_NP ; Channel_CN ; Channel_NP ;
      Request_NP ; Cred_NP ; Comment_CN ; Comment_NP ; Schema_NP ; Actor ;
  fun
    subscribe_Atom    : Viewer_NP -> Channel_NP -> Atom ;       -- a viewer subscribes to a channel
    subscribe_RelObj  : Channel_CN -> Viewer_NP -> Channel_CN ; -- channel that a viewer subscribes to
    subscribe_RelSubj : Viewer_CN -> Channel_NP -> Viewer_CN ;  -- viewer that subscribes to the channel
    Cred_Of   : Request_NP -> Cred_NP ;                         -- the credentials of the request
    Cred_Poss : Request_NP -> Cred_NP ;                         -- the request's credentials
    conform_Atom : Comment_NP -> Schema_NP -> Atom ;            -- ... conforms to the comment schema
    conform_RelSubjNeg : Comment_CN -> Schema_NP -> Comment_CN ;-- comment that does not conform to ...
    Pos, Neg : Atom -> Cond ;
    While : Cond -> Resp -> Req ;
    ...
}
concrete SpikeEng of Spike = open SyntaxEng, ParadigmsEng, (E = ExtraEng), (G = GrammarEng) in {
  lincat Atom = Cl ; Cond, Resp = S ; Viewer_NP, Channel_NP, Cred_NP, Comment_NP = NP ; ...
  oper subscribe_V2 = mkV2 (mkV "subscribe") (mkPrep "to") ;
       conform_V2   = mkV2 (mkV "conform") (mkPrep "to") ;
       shall_VV     = auxVV (mkV "shall" "shall" "should" "should" "shalling") ;
  lin
    subscribe_Atom v c    = mkCl v subscribe_V2 c ;
    subscribe_RelObj cn v = mkCN cn (mkRS (mkRCl which_RP (mkClSlash v subscribe_V2))) ;
    subscribe_RelSubj cn c = mkCN cn (mkRS (mkRCl which_RP subscribe_V2 c)) ;
    Cred_Of r   = mkNP thePl_Det (mkCN credentials (SyntaxEng.mkAdv possess_Prep r)) ;
    Cred_Poss r = mkNP (mkDet (E.GenNP r) pluralNum) credentials ;
    conform_Atom c s = mkCl c conform_V2 s ;
    conform_RelSubjNeg cn s = mkCN cn (mkRS E.UncNeg (mkRCl which_RP conform_V2 s)) ;
    Pos a = mkS a ;  Neg a = mkS E.UncNeg a ;
    While c r = mkUtt (G.ExtAdvS (SyntaxEng.mkAdv (mkSubj "while") c) r) ;
}
```

Results (`gf --run Spike.pgf`, `p` = parse):

| Input | Result |
|---|---|
| while a request comment does not conform to the comment schema , \`work\` shall print the request comment | one tree: `While (Neg (conform_Atom ...)) (print_Comment ...)` |
| while every viewer subscribes to a channel that a viewer subscribes to , \`work\` shall print a comment that does not conform to the comment schema | one tree, with `subscribe_RelObj` and `conform_RelSubjNeg` |
| \`work\` shall not print the credentials of the request / ... the request's credentials | one tree each, `Cred_Of` / `Cred_Poss` |
| while viewers subscribe to the channels that viewers subscribe to , ... | one tree. Agreement works in the main clause and inside the relative clause (`l -table` gives "channels that viewers subscribe to"). |
| while viewers **subscribes** to a channel , ... | refused at "subscribes" (agreement enforced) |
| while a **channel** subscribes to a viewer , ... | refused at "channel" (the frame's typing enforced) |
| ... a channel **which** a viewer subscribes to ... | refused: `which_RP` linearises as "that" in this RGL version (default since 2016) |

Things to know before adopting the RGL, all found in the spike:

1. The RGL's default negation is contracted ("doesn't"). You need `ExtraEng.UncNeg` (or `Extend.UncontractedNeg`)
   to get "does not".
2. `mkS (mkAdv subj s) s'` gives no comma after "while ...". `ExtAdvS` adds it. The repo's comma-as-token
   tokenising would need to match.
3. A compound noun ("request comment") is lexical (`compoundN "request" (mkN "comment")`). A typed, productive
   compound, where only a request noun may stand before "comment", would need the kind's `N` in the lincat, not
   only its `CN`.
4. "shall" has no RGL entry. An `auxVV` with made-up forms works for the present tense only. That is fine here,
   since lines use "shall" in one form.

The repo's hand-written equivalent of the object relative clause, as `spec_typed_verbs` would have to generate it,
looks like this:

```gf
e_subscribe__RelObj : k_channel_CN -> viewer_Sb -> k_channel_CN ;
e_subscribe__RelObj cn s = post cn (\\_ => "that" ++ s ++ "subscribes" ++ "to") ;   -- s : Str, number lost
```

`<T>_Sb` is a `Str`, so "channels that viewers subscribe to" cannot be written until `Sb` carries number. Then
every `Happens`/`Does`/`DoesNot`/step fun has to be rewritten to agree. The RGL version gets all of that from
`mkClSlash`. "conforms to the comment schema" is already expressible in the repo today, as a prepositional verb
frame (b106: "comment conforms to schema") if "schema" is a kind. What it lacks is naming an external artifact
(a file, a schema) as the object rather than a kind's instance, which is a vocabulary question, not a GF one.

### 4.1 Scale and speed (spike, measured)

I wrote `scale/gen.py` to generate an RGL-based grammar shaped like this repo's: K kinds, each with a CN and five
determiners, and V verbs, each with an atom, an object relative, a subject relative and a negated subject relative,
plus `Pos`/`Neg`/`While`. Compiled with gf 3.12 (RGL `.gfo` already built):

| K kinds / V verbs | approx. funs | compile | PGF |
|---|---|---|---|
| 20 / 10 | 160 | under 1 s | 54 KB |
| 160 / 80 | 1,280 | 3.2 s | 426 KB |
| 320 / 160 | 2,560 | 6.1 s | 862 KB |
| *this repo, hand-written* | *4,841* | *0.7 s* | *766 KB* |

Parsing 8 random sentences of 19-29 tokens from the 320/160 grammar with the Python `pgf` runtime took 3-4 ms
each, with one tree each. Compile time grows linearly, at roughly 10x the repo's cost per fun, because RGL lincats
(`NP` with case and agreement, `Cl` with tense, anteriority, polarity and word order) expand into more PMCFG rules.
A full port would probably compile in tens of seconds once per glossary change. The sha-keyed PGF cache in
`spec_grammar` already makes that a one-off, but `tests/` that build many fixture grammars would feel it. I did not
measure a full port. This is an extrapolation.

## 5. Risks and limits

- **Ambiguity growth.** It is controlled by what the application abstract syntax exposes. The RGL is used only at
  compile time, through opers, and none of its own funs reach the PGF unless they are re-exported. ACE-in-GF's
  English stayed at about 3% harmless ambiguity over 19k sentences (Kaljurand & Kuhn 2013). New ambiguity would
  come from new constructions, for example a relative clause that could attach to either noun in "the file of the
  item that a session writes". The repo's existing policy (two trees means refused, with a hint) catches that. It
  should be paired with a corpus round-trip check: linearise every tree and reparse it, as AceWiki-GF did.
- **Parse speed.** Not a concern at these sizes (milliseconds). The on-disk parse cache stays useful because the
  2,000-tree cap and the String-literal callback, not the grammar's size, drive the worst cases.
- **Debuggability.** RGL types are opaque to authors who do not know GF, and errors come from deep inside RGL
  modules. Generated code means only the generator's author needs this knowledge.
- **Dependency.** The RGL would have to be installed and pinned beside gf 3.12 in `tools install`. The tarball is
  44 MB and the English subset compiles in about 0.5 s.
- **Semantics is not solved by GF.** No GF CNL I found derives logic automatically. ACE-in-GF relies on APE's DRS,
  AnaCon and C-O diagrams translate trees to CL by hand, and L4 disclaims CNL semantics. Ranta (2011) argues that
  abstract syntax *is* a good logical form for simple interfaces. In practice that means designing the abstract
  syntax as the logic: `Neg`, quantifier determiners, `RelObj` as set comprehension, so that `spec_facts`
  translates a small, principled set of funs instead of 4,800 generated ones. An RGL-based redesign is the
  natural moment to do that. Funs that mean the same thing would collapse, which shrinks the translation surface
  that hypothesis 1 complains about.
- **Donkey anaphora and scope** ("every viewer subscribes to a channel that a viewer subscribes to": are the two
  viewers the same?) are not touched by the RGL. They need a decision in the semantics layer. Researchers on
  ACE/DRS should own that.

## 6. Recommendation for phase 2 (for discussion, not settled)

1. Prototype an RGL-based `CoreEng`/`TypedEng` generator for one capability's vocabulary. Keep the abstract
   categories and the guards. Replace the `*Not` funs with a polarity argument, and give `Sb` agreement through
   RGL `NP`. Check it against `grammar/corpus/` by round-trip.
2. Add constructions by frame, not by hand: object and subject relative clauses, a genitive, "may". Measure tree
   counts on the corpus.
3. Whatever happens with the RGL, fix the agreement defect in section 3.2 (plural subjects of verb frames).
4. Consider exposing GF's completion (`complete` in the PGF runtime) to the authoring skill as a "what can follow
   here" hint, in the spirit of the AceWiki look-ahead editor.

## Sources

- A. Ranta, K. Angelov, "Implementing Controlled Languages in GF", CNL 2009, CEUR-WS 448; LNCS 5972 (2010) 82-101.
  https://research.chalmers.se/en/publication/105696 , https://research.chalmers.se/publication/131247
- K. Kaljurand, T. Kuhn, "A Multilingual Semantic Wiki Based on Attempto Controlled English and Grammatical
  Framework", ESWC 2013, arXiv 1303.4293. https://ar5iv.arxiv.org/html/1303.4293
- A. Ranta, "The GF Resource Grammar Library", LiLT 2(2), 2009. https://journals.colorado.edu/index.php/lilt/article/view/1205
- A. Ranta, "Translating between Language and Logic: What Is Easy and What Is Difficult", CADE-23, LNCS 6803 (2011)
  5-25. https://www.springerprofessional.de/en/translating-between-language-and-logic-what-is-easy-and-what-is-/3689848
- K. Angelov, "Incremental Parsing with Parallel Multiple Context-Free Grammars", EACL 2009.
  https://research.chalmers.se/en/publication/82866 ; K. Angelov, P. Ljunglöf, "Fast Statistical Parsing with
  PMCFG", EACL 2014. https://research.chalmers.se/publication/205189
- MOLTO (FP7 247914): annual report 2011,
  https://cordis.europa.eu/docs/projects/cnect/4/247914/080/publishing/readmore/molto-annual-report-2011.pdf ;
  A. Ranta, MT Summit 2013, https://aclweb.org/anthology/2013.mtsummit-european.12.pdf
- K. Angelov, J. J. Camilleri, G. Schneider, "A Framework for Conflict Analysis of Normative Texts Written in
  Controlled Natural Language", JLAP 82 (2013) 216-240. https://research.chalmers.se/en/publication/181436
- J. J. Camilleri, G. Paganelli, G. Schneider, "A CNL for Contract-Oriented Diagrams", CNL 2014.
  https://www.cse.chalmers.se/~gersch/cnl2014.pdf
- I. Listenmaa, M. M. Hanafiah, R. Cheong, A. Källberg, "Towards CNL-based Verbalization of Computational
  Contracts", CNL 2021. https://aclanthology.org/2021.cnl-1.10
- S. Pathak, "GFLean: An Autoformalisation Framework for Lean via GF", arXiv 2404.01234 (2024).
- GF tutorial (Lessons 3-5: resource library, functors, dependent types, `def`).
  https://www.grammaticalframework.org/doc/tutorial/gf-tutorial.html
- gf-dev thread "typecheck not working" (2019), K. Angelov on dependent types in the C runtime.
  https://groups.google.com/g/gf-dev/c/8HkK7mYg9Gs/m/DdurKNXdAgAJ
- G. Détrez, A. Ranta, "Smart paradigms and the predictability and complexity of inflectional morphology", EACL
  2012 (from memory: not re-fetched in this session).
- K. Angelov, gf-wordnet, LREC 2020 (from memory: not re-fetched in this session).
- gf-rgl release 20250812, https://github.com/GrammaticalFramework/gf-rgl (used for the spike).
