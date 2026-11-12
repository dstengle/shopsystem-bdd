# Collections, ordering and comparisons in formal specification languages and controlled natural languages

Scope: Alloy, Z, B, OCL and TLA+ (formal), and ACE, SBVR, EARS, Rabbit, PENG and other CNLs. For each: how it represents collections (set, bag, sequence), ordering (by element or by an attribute, and direction), membership and quantification, and comparisons between items. The aim is to inform a GF-based EARS-style requirement language whose logical form is DRT-like (referents, atoms, boxes).

Sourcing note: items marked **[bk]** under Inferences come from the researcher's background knowledge. They were not verified against a primary source in this session, and the writer should treat them as plausible but unconfirmed.

## Alloy: sets, relations, seq, util/ordering and "sorted by attribute"

### Takeaway
Alloy has two separate mechanisms:
- `seq T` is an indexed relation `Int->T`, an ordered collection value with duplicates allowed.
- `util/ordering[S]` is a single global total order imposed on a whole signature. It is not a property of any one collection, and it forces the signature's scope to be exact.

"Sorted by an attribute" has no built-in form in either mechanism. You write it as a fact over pairs of indices.

### Cited Findings
- A sequence is declared `books: seq Book`. "Under the hood" it has type `Int->Book`, so `s[0]` is the first element. Its length is bounded by a `seq` scope, e.g. `check X for 4 seq`. — [Alloy quick guide: sequences](https://alloytools.org/quickguide/seq.html)
- The sequence operations come from `util/sequniv.als` — [Alloy quick guide: sequences](https://alloytools.org/quickguide/seq.html):
  - `#s`
  - `s.elems`, the set of elements
  - `s.first` and `s.last`, which give the empty set on an empty sequence
  - `s.isEmpty`
  - `s.hasDups`
  - `s.inds`, the indices `{0..#s-1}`
  - `s.idxOf[x]`, the first index of `x`
  - `s.add[x]`, which appends only if the sequence is below its maximum length
- `open util/ordering[A]` places an ordering on signature A. It can be instantiated only once per signature. — [Alloy docs: util/ordering](https://alloy.readthedocs.io/en/latest/modules/ordering.html)
- `util/ordering` provides — [Alloy docs: util/ordering](https://alloy.readthedocs.io/en/latest/modules/ordering.html):
  - `first`, `last`
  - `next` and `prev`, which are relations `elem->elem`
  - `nexts[e]` and `prevs[e]`, the strict successors and predecessors
  - `smaller` and `larger`
  - `min[es]` and `max[es]`, each of type `lone elem`
  - the predicates `lt`, `gt`, `lte`, `gte`, where `lt[e1,e2]` holds iff `e1 in prevs[e2]`
- Caveat: "the ordering forces the signature to be exact". `open util/ordering[S] sig S {} run {#S = 2} for 3` has no instances, and an assertion may pass only because of this implicit constraint. — [Alloy docs: util/ordering](https://alloy.readthedocs.io/en/latest/modules/ordering.html)

### Inferences
- The concrete idiom for "a list of items ordered by priority, ascending" **[bk]** is:
  ```alloy
  sig Item { priority: one Int }
  sig Queue { items: seq Item }
  fact sorted { all q: Queue | all i: q.items.inds - q.items.lastIdx |
      q.items[i].priority <= q.items[i.add[1]].priority }   -- adjacent pairs
  -- or, all pairs: all i, j: q.items.inds | i < j implies q.items[i].priority <= q.items[j].priority
  ```
  Ordering by attribute is therefore an assertion over pairs, adjacent or all, never part of the type.
- `util/ordering` fits "the stages of a pipeline come in this order", a domain-wide order on a kind. It does not fit "this list is sorted by date". It is analogous to an attribute's `Order: as listed.`
- Alloy's `let` **[bk]** is a local macro: `let x = e | F`, or `let f[a] = e` at module level. `fun` and `pred` are named, parameterised definitions. Neither declares a type; types come only from `sig`.

### Gaps
- Exact definitions of `last`, `nexts`, `gt`, `max` were only linked from the ordering page, not shown. The standard library source `util/ordering.als` was not fetched.
- I found no official Alloy text on a "sortedBy" idiom. The fact above is the researcher's construction.

## Z and B: seq, ran, squash, filtering, bags

### Takeaway
In Z a sequence is a finite function from `1..n` to X. Selection operations are defined through `squash`, which compacts a partial function on ℕ₁ back into a sequence while keeping the order of its indices.

Sortedness is not a toolkit predicate. You write it as a quantified constraint on indices: ∀ i, j : dom s | i < j • key(s i) ≤ key(s j).

### Cited Findings
- The Z/EVES mathematical toolkit, which follows Spivey, lists these sequence operators — [Z/EVES 2.0 Mathematical Toolkit](https://www.pst.ifi.lmu.de/Lehre/WS0001/gse/unterlagen/Z/Toolkit.pdf):
  - `head`, `last`, `tail`, `front`, `rev`
  - extraction `E ↿ s` and filtering `s ↾ F`
  - `squash`
  - `prefix`, `suffix`, `in`
  - `disjoint`, `partition`
  - bags: `bag X`, `count`, and membership `x in B`
- Definitions — [Z/EVES 2.0 Mathematical Toolkit](https://www.pst.ifi.lmu.de/Lehre/WS0001/gse/unterlagen/Z/Toolkit.pdf):
  - `squash : (ℕ₁ ⇸ X) → seq X`, defined by: for every f, there is g : 1..#f ⤖ dom f with (∀ i, j : dom g | i < j • g(i) < g(j)) and squash f = g ⨾ f
  - `E ↿ s = squash(E ◁ s)`, i.e. extraction
  - `s ↾ F = squash(s ▷ F)`, i.e. filtering
  - The source text was decoded from PDF and the symbols reconstructed.
- `squash f` is "compaction" on Spivey's Z reference card. Spivey's *The Z Notation: A Reference Manual* (2nd ed., 1992) is the de facto standard. — [Spivey Z refcard (Bremen)](https://www.informatik.uni-bremen.de/agbs/lehre/ws0708/scs3/werkzeuge/refcard.pdf); [Wikipedia: Z notation](https://en.wikipedia.org/wiki/Z_notation)

### Inferences
- Concrete Z for "items ordered by date, newest first" **[bk]**:
  ```z
  queue : seq ITEM
  ∀ i, j : dom queue | i < j • date(queue i) ≥ date(queue j)
  ```
  "No duplicates" is `queue ∈ iseq ITEM`, the injective sequences. Membership is `x ∈ ran queue`. Quantification over members is `∀ x : ran queue • P x`. A schema `[ queue : seq ITEM | sorted-pred ]` is Z's way to declare a complex type with its invariant, and that is the closest analogue of a "Let ..." declaration.
- B **[bk]**:
  - `seq(T)`, `iseq(T)`, `ran`, `first`, `last`, `size`, `front`, `tail`, `↑`/`↓` restrictions
  - total orders only on INTEGER and similar types
  - sortedness written as `!(i,j).(i:1..size(s) & j:1..size(s) & i<j => key(s(i)) <= key(s(j)))`
- Z and B both make ordering an assertion on index pairs. A "sorted sequence" type exists only as a schema or set comprehension, `{s : seq X | ∀ i,j ...}`.

### Gaps
- I could not get B's reference (Atelier B manual or B-Book) text in this session, so the B details are **[bk]**.
- Spivey's own text of `squash` was seen only via the Z/EVES toolkit and the refcard.

## OCL: Set / Bag / Sequence / OrderedSet, sortedBy, iterators, let

### Takeaway
OCL is the only surveyed formal language with a built-in "ordered by key" operation. `sortedBy(e | expr)` returns a Sequence or OrderedSet ordered by the key, which needs a `<` on the key's type.

Its four collection kinds cross two properties:

| Kind | Ordered | Unique |
|---|---|---|
| Set | no | yes |
| OrderedSet | yes | yes |
| Bag | no | no |
| Sequence | yes | no |

Ordering in OCL is still a result of an operation, not a declared invariant. "Is sorted" is written `self.items = self.items->sortedBy(date)`.

### Cited Findings
- From the Eclipse OCL standard library, `Collection(T)` — [Eclipse OCL Standard Library: Collection](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/Collection.html):
  - `sortedBy(…) : Sequence(T)` "Results in the Collection containing all elements of the source collection".
  - `isUnique(body) : Boolean`, true "if body evaluates to a different value for each element".
  - `forAll` is true if body is true "for each element".
  - `exists`, true for at least one element.
  - `one`, true for exactly one element.
  - `any(body) : T[?]`, any element satisfying body.
  - `select` and `reject : Collection(T)`, sub-collections.
  - `collect : Collection(V)`, the body applied to every member.
  - `includes`, membership.
  - `size`.
- Collection itself allows duplicates ("if an object occurs twice in a collection, there are two elements"). Order is left to the subtypes: `=` is order-sensitive "in the case of an ordered collection type", and `asSequence()` orders "in an order dependent on the particular concrete collection type". — [Eclipse OCL: Collection](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/Collection.html)
- The Eclipse library describes itself as "a prototype of functionality for OCL 2.5". — [Eclipse OCL Standard Library index](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/StandardLibrary.html)

### Inferences
- Concrete OCL for "a queue's items ordered by priority, then the ones with the same priority by date" **[bk]**:
  ```ocl
  context Queue
  inv sortedByPriority: self.items = self.items->sortedBy(i | i.priority)
  -- adjacent-pairs form for an OrderedSet / Sequence:
  inv: Sequence{1..self.items->size()-1}->forAll(k |
         self.items->at(k).priority <= self.items->at(k+1).priority)
  inv noDupKeys: self.items->isUnique(i | i.id)
  ```
  - `sortedBy` is ascending only. Descending order needs `->reverse()` (OCL 2.4+) or a negated key.
  - A tie-break has no standard multi-key form. You write a tuple key with a user-defined `<`, or the pairwise form.
  - In OCL 2.4, `sortedBy` returns `OrderedSet(T)` for a Set or OrderedSet source and `Sequence(T)` for a Bag or Sequence source **[bk]**. Eclipse's Collection-level signature shows `Sequence(T)` only.
- An `{ordered}` association end in UML gives an OrderedSet. Ordering is then a property of the end's type, but the order is opaque: it says no key.
- OCL `let x : T = e in expr` and `def:` in a context declare local or derived names **[bk]**. This is the closest formal precedent for "Let ..." definitions inside a constraint.

### Gaps
- The OMG OCL 2.4 PDF was fetched but could not be text-extracted here, since there was no pdftotext or pypdf. The per-kind result types of `sortedBy`, `reverse` and `OrderedSet` operations are therefore **[bk]** and not quoted.

## TLA+: sequences and sortedness

### Takeaway
TLA+ sequences are functions on `1..n`. The standard Sequences module has no sort. The Community Modules give `IsSorted(s, op)` as an all-pairs predicate with a caller-supplied comparison, and `SetToSortSeq`.

### Cited Findings
- Sequences module: `∘` (concatenation), `Head`, `Tail`, `Append`, `Len`, `Seq`, `SubSeq`, `SelectSeq(s, Test)`, which gives the subsequence satisfying Test. A sequence is a function with domain `1..n`. — [TLA+ summary (Lamport)](https://www.pst.ifi.lmu.de/Lehre/WS0203/gse/TLA/tla-summary.pdf)
- From the SequencesExt community module — [tlaplus/CommunityModules SequencesExt.tla](https://raw.githubusercontent.com/tlaplus/CommunityModules/master/modules/SequencesExt.tla):
  - `IsSorted(s, op(_,_)) == \A i, j \in 1..Len(s) : i < j => op(s[i], s[j])`, with "no assumptions are made about op"
  - `ToSet(s) == { s[i] : i \in DOMAIN s }`
  - `SetToSortSeq(S, op) == SortSeq(SetToSeq(S), op)`

### Inferences
- "Ordered by date, newest first" in TLA+ is `IsSorted(q, LAMBDA a, b: a.date >= b.date)`. The key and the direction are folded into one comparison operator: an assertion over pairs, parameterised by a relation. `SortSeq` comes from the TLC module **[bk]**.

### Gaps
- `SortSeq`'s defining module (TLC) was not fetched.

## ACE (Attempto Controlled English): plurals, cardinality, "each of", comparisons, lists, DRS groups

### Takeaway
ACE resolves the collective/distributive ambiguity by fiat:
- a plural noun phrase is collective by default
- "each of" marks a distributive reading
- quantifier scope follows surface order
- "there is/are" and "for each of" widen scope

In the DRS a plural is one referent carrying a cardinality: `object(A,card,countable,na,eq,2)`. Its members appear only when distribution needs them, through `has_part(Group, Member)` inside an implication box.

ACE has comparatives and superlatives, and list and set *expressions*. It has no ordering-by-attribute of a collection.

### Cited Findings
- "By default, plural noun phrases have a collective reading; distributive reading is indicated by *each of*." Example: "A clerk enters two cards" (collective) vs "A clerk enters each of two cards" (distributive). — [ACE 6.7 Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)
- "Two girls lift a table" is one act of lifting by the group. "Each of two girls lifts a table" is two acts. — [ACE 6.7 Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)
- Construction rules — [ACE 6.7 Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html):
  - Generalised quantifiers take positive integers: "at least 2 cards", "at most 2", "more than 10", "less than 3", "exactly 3".
  - Each can be made distributive: "each of at least 2 cards".
  - "all cards" is syntactic sugar for "every card", and "no cards" for "no card".
  - Numbers can't appear after "there is/are". Numbers up to 12 may be words.
- Construction rules on comparison — [ACE 6.7 Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html):
  - Comparatives: "John is richer than Mary", "as rich as".
  - Superlatives: "a richest customer", "John is most fond-of Mary".
  - Comparison targets cannot be conjoined.
  - Formula comparisons `=`, `\=`, `>`, `>=`, `<`, `=<`, e.g. "X >= 13.4 and X < 20".
  - Saxon genitive: "John and Mary's dog" parses as John and {Mary's dog}.
- DRS representation (ACE 6.7 DRS report) — [Fuchs, Kaljurand, Kuhn: Discourse Representation Structures for ACE 6.7](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf); text decoded from PDF:
  - `object(Ref,Noun,Class,Unit,Op,Count)`, with Op one of `eq, geq, greater, leq, less, exactly, na`. Unit and Op "together define the cardinality or extent".
  - "some cards" → `object(A,card,countable,na,geq,2)`; "2 cards" → `object(A,card,countable,na,eq,2)`.
  - `has_part(GroupRef, MemberRef)` "define the memberships of objects in groups".
  - Noun phrase conjunction: "a customer and a clerk" gives a group C with `has_part(C,A)`, `has_part(C,B)` and `object(C,na,countable,na,eq,2)`.
  - Generalised quantifiers: a minimality condition ("at least", "more than") stays flat. A maximality condition ("exactly", "at most", "less than") brackets the conditions in its scope, "to capture the scope of the maximality restriction".
  - Adjective properties carry a Degree, one of `pos`, `pos_as`, `comp`, `comp_than`, `sup`, with a comparison target, e.g. 3-ary `property(Ref1,Adj,Ref2,Degree,CompTarget,Ref3)`.
- Distributive DRS — [ACE 6.7 DRS report](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf):
  - "2 girls lift each of 2 tables" gives the girls group A, the tables group B, and `[C | has_part(B,C)] => [D | predicate(D,lift,A,C)]`.
  - Section 11 shows eight readings of "2 girls lift 2 tables" that ACE can express, each with its own surface form.
- Lists and sets as expressions, with a "first" property on an element — [ACE 6.7 DRS report](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf):
  - "3 is the first element of [3,4.5,"ab",John,1+2]" → `relation(B,of,list([int(3),…]))`, `property(B,first,pos)`, `object(B,element,…)`.
  - "{3,6,[1,2]} contains 6" → `predicate(A,contain,set([…]),int(6))`.

### Inferences
- ACE's design is a direct precedent for a DRT logical form. A collection is a group referent with a cardinality condition, and members are reached by `has_part` inside a universally quantified box, i.e. the existing `every` box keyed on membership.
- ACE has no "ordered by" construct. "first" is a lexical adjective on an element of a literal list, with no general semantics of position. For ordering, ACE leaves the requirement writer to comparatives ("is older than") inside "every"/"if" sentences, which is the pairwise style.
- ACE's collective default is the opposite of what requirement writers usually mean by "the items" ("the tool prints the items" is distributive). A requirement CNL may prefer a distributive default, or refuse an unmarked plural.

### Gaps
- The DRS output for "John is richer than Mary" itself was not extracted, only the property arity and degree definitions.
- ACE's "definitions" (macros) were not researched in this session; see the CNL section's gap.

## SBVR Structured English, EARS, Rabbit, PENG and other CNLs on collections and ordering

### Takeaway
None of the surveyed requirement or ontology CNLs found in this session has a first-class "ordered by attribute" collection construct.
- EARS fixes clause order (While/When/Where/If-Then, then shall), not data structure.
- SBVR expresses everything through fact types with a fixed number of roles, plus quantifiers ("each", "at least n", "exactly n"). Ordering is a fact type ("x precedes y"), not a collection property.
- Rabbit and SOS map to OWL, which has no ordered collections. The OWL-list pattern is a workaround outside the CNL.

### Cited Findings
- EARS (Mavin et al., Rolls-Royce, RE'09) — [Wikipedia: EARS](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax); [EARS official guide (mirror)](https://hn.jakechampion.name/reader/https://alistairmavin.com/ears):
  - The general template is "While <precondition(s)>, when <trigger>, the <system name> shall <system response>", in temporal order: zero or many preconditions, zero or one trigger, one system, one or many responses.
  - The patterns are ubiquitous, event-driven (When), state-driven (While), optional-feature (Where) and unwanted behaviour (If … Then). A requirement with more than one keyword is "complex".
- EARS governs syntax, not semantics. It "is not an executable specification". — [DEV: EARS](https://dev.to/sebastian_dingler/ears-the-easy-approach-to-requirements-syntax-39a5) (secondary)
- SBVR fact types identify relationships among one or more roles, and every fact type has a fixed number of roles. — [AAAI SS-08-01-010](https://cdn.aaai.org/Symposia/Spring/2008/SS-08-01/SS08-01-010.pdf)
- An SBVR service-choreography paper proposes ordering *between fact types* to capture the sequencing of interactions. The ordering there is temporal and modelled outside the noun concepts. — [arXiv 1512.07685: Service Choreography, SBVR, and Time](https://arxiv.org/pdf/1512.07685)
- An SBVR fact type form "is a grammatically structured expression serving as a pattern for usage of the fact type designation". — [OMG issue SBVR11-86](https://issues.omg.org/issues/SBVR11-86)
- Rabbit (Ordnance Survey) is designed to map directly to OWL. It was compared with ACE and Sydney OWL Syntax for OWL 1.1. — [ROO poster, ESWC 2008](https://ceur-ws.org/Vol-367/ESWC2008_Poster_Denaux.pdf); [Schwitter et al., comparison of three CNLs for OWL 1.1](https://researchers.mq.edu.au/en/publications/a-comparison-of-three-controlled-natural-languages-for-owl-11/)
- Kuhn's survey covers 100 English-based CNLs from 1930 onward and proposes the PENS classification. It was published in *Computational Linguistics* 40(1):121–170, 2014. — [arXiv 1507.01701](https://arxiv.org/pdf/1507.01701); [ACL Anthology J14-1005](https://preview.aclanthology.org/setup/J14-1005)

### Inferences
- SBVR concrete form **[bk]**: "It is obligatory that each queue lists at least 1 item" and "It is necessary that each item has exactly one priority". An ordering would need an extra fact type, e.g. "item1 precedes item2 in queue", plus a rule: "It is obligatory that if item1 precedes item2 in a queue then the priority of item1 is at most the priority of item2". That is pairwise. SBVR's "is ordered by" was not found in any source.
- PENG and PENG-D/ASP (Schwitter) **[bk]** use DRS like ACE and support comparatives and numbers. No ordered-list construct is known.
- CLCE (Sowa) **[bk]** reads into conceptual graphs and has no sequence type.
- GF-based CNLs (the ACE-in-GF port, Ranta and Angelov's multilingual CNLs) **[bk]** use the RGL's `ConjNP`/`ListNP` for coordination ("A, B and C"). The RGL's `Det` with `num` covers cardinals. The resource grammar gives *syntax* for lists of NPs, not collection semantics, so semantics stays in the abstract syntax the CNL designer writes.
- Definitions and "Let":
  - ACE allows definitions of new words via sentences such as "A bachelor is a man who is not married" **[bk]**. These are conditionals and introduce no types.
  - Z schemas, OCL `let`/`def`, Alloy `let`/`fun` and mathematics' "Let S be a sequence of ... such that ..." all introduce a *name bound to a typed value with an invariant*.
  - In mathematical controlled languages such as Naproche/ForTheL **[bk]**, "Let x be a ..." introduces a variable with a type assumption scoped to the section. This is the nearest CNL precedent to a "Let ..." declaration of complex types.

### Gaps
- I found no source defining an SBVR "is ordered by" form, nor an ordered-collection construct in Rabbit, PENG, CLCE, Sydney OWL Syntax or EARS. Absence is reported from the searches above and from background knowledge, not proven.
- Kuhn's survey text was not read for collection or ordering coverage, only its bibliographic facts.
- ACE's definition and macro mechanism, Naproche/ForTheL "Let" and GF RGL docs on plurals were not fetched. Those points are **[bk]**.

## Ordering as a property of the collection type vs an assertion over pairs: trade-offs

### Takeaway
Almost every formal language makes "sorted by key" an assertion over index pairs, all pairs or adjacent pairs, sometimes wrapped in a parameterised predicate:
- Z: ∀ i<j
- B: !(i,j)
- Alloy: a fact over `inds`
- TLA+: `IsSorted(s, op)`

OCL alone has a key-based operation (`sortedBy`), and even there "sorted" is stated as equality with the sorted copy. Global orders on a kind are a separate concept: Alloy's `util/ordering`, or UML `{ordered}` with no key.

### Cited Findings
- TLA+ community: `IsSorted(s, op) == \A i, j \in 1..Len(s) : i < j => op(s[i], s[j])`, an all-pairs predicate parameterised by a relation. — [SequencesExt.tla](https://raw.githubusercontent.com/tlaplus/CommunityModules/master/modules/SequencesExt.tla)
- OCL `sortedBy` returns a Sequence of all source elements. Kind-level order is fixed by the concrete collection type. — [Eclipse OCL: Collection](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/Collection.html)
- Alloy's `util/ordering` is one total order per signature, forcing exact scope. — [Alloy docs: util/ordering](https://alloy.readthedocs.io/en/latest/modules/ordering.html)
- Z's `squash` keeps index order when filtering, so a sub-sequence of a sorted sequence stays sorted with no restatement. — [Z/EVES Toolkit](https://www.pst.ifi.lmu.de/Lehre/WS0001/gse/unterlagen/Z/Toolkit.pdf)

### Inferences
- **Ordering as a type property** ("a list of items ordered by date, newest first"):
  - Pros: one declaration, reused by every line. It reads like the domain ("the queue is ordered by priority"). A generator can derive both the pairwise check and test data, which is sorted by construction. It lets the *key* and *direction* be named once, e.g. in a "Let" declaration or a glossary entry.
  - Cons: it fixes a strict or non-strict order and the tie-breaking. It needs a total order on the key, like OCL's `<` requirement. Lines that talk about "the first" or "the newest" depend on a declaration elsewhere. It mirrors the attribute-level `Order:` already present in this repository's grammar.
- **Ordering as an assertion over pairs** ("every item comes before each item whose date is earlier"):
  - Pros: it is first-order, it fits the existing DRT boxes (`every` over two referents with `distinct` and a comparison atom), it is checkable directly by ASP, and it allows partial orders and conditional ordering.
  - Cons: it is verbose and easy to get wrong in English. "Adjacent" vs "all pairs" is equivalent only for transitive key orders. Tie handling (strict `<` vs `≤`) leaks into wording.
- A hybrid is common in practice and fits this project: declare "ordered by K, D" on a collection kind, and have the logical form *expand* it into the pairwise box. TLA+'s `IsSorted` and OCL's `self.items = self.items->sortedBy(k)` are both "named predicate, pairwise meaning".

### Gaps
- No empirical study comparing the two styles' error rates in requirement writing was found.

## Known ambiguity pitfalls when English talks about collections

### Takeaway
The main pitfalls follow. ACE's response is to fix one reading per surface form and make the other reading say itself differently.
- **Collective vs distributive plurals.** "Two girls lift a table": one act or two?
- **Quantifier scope.** "2 girls lift 2 tables" has eight readings in ACE's analysis.
- **Maximality of cardinals.** "has 2 cards" means at least 2 or exactly 2?
- **Coordination grouping.** "John and Mary's dog".
- **Order and direction words.** "first", "newest first", "in order".

### Cited Findings
- ACE lists eight readings of "2 girls lift 2 tables" and gives each a distinct ACE sentence. Scope follows surface position, and "there is/are" and "for each of" widen it. — [ACE 6.7 DRS report §11](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf)
- Collective is the default. "each of" marks the distributive reading. — [ACE Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)
- ACE separates minimality quantifiers ("at least", "more than", flat in the DRS) from maximality ones ("exactly", "at most", "less than"), which need a scoped box. — [ACE 6.7 DRS report §3.7](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf)
- "John and Mary's dog" parses as John and {Mary's dog}, because the genitive binds to a single noun. Comparison targets cannot be conjoined. — [ACE Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)
- "and" binds more strongly than "or". ",and" and ",or" override this. — [ACE Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)

### Inferences
- **"every item in order" / "prints the items in order"**: in which order? By insertion, by a declared key, or the order of the source collection? Without a declared order this is unverifiable, so a CNL should refuse "in order" with no "by K" or no declared collection order.
- **"newest first"** names the key implicitly (a date or creation time) and the direction (descending), but not the tie-break. It also conflicts with "first" meaning index 1: "the first item" after "newest first" is the newest. A CNL should say direction with the key: "ordered by date, latest first", or "by date descending".
- **"sorted by priority"** says nothing about direction ("higher priority first" vs ascending numeric value). This is a classic inversion where priority 1 is the highest. Direction should be obligatory, or the default fixed and documented, as OCL's `sortedBy` is ascending **[bk]**.
- **"each item's date is after the previous item's date"** introduces a positional anaphor ("the previous item"), which DRT handles only with an explicit successor relation like Alloy's `next`/`prev`. The grammar would need a "previous" or "next" image of a referent within a declared sequence.
- **"the items are older than the request"** is distributive in intent but collective by ACE's default. A requirement CNL should take either ACE's "each of" marker or a distributive default for state predicates.
- **"the first two items"** combines positional selection with cardinality. Alloy (`s.subseq`, **[bk]**), Z (`(1..2) ↿ s`) and TLA+ (`SubSeq`) all have it, but ACE has no positional selection beyond the lexical adjective "first".
- **Duplicates**: "a list of the items" vs "the set of items". Sequence vs set semantics (OCL's four kinds, Z's `seq` vs `iseq`) must be decided where the collection is declared. Otherwise "each item appears once" is an unstated assumption.

### Gaps
- No corpus study of collection ambiguities specifically in software requirements (as opposed to general CNL design) was found in this session.

## Introducing and referring to a complex object without explicit variables (alternatives to a requirement-level "Let L be ...")

The question is how a spec can say "the video list that holds every video from the channel, ordered by publication time, newest first" once, and have several requirement lines use it, without making the writer create variables.

### Takeaway
Seven mechanisms are surveyed below. Three fit a DRT-style controlled English with R2-style "the K" binding most cheaply:
- **(5)** an inline description carried once by a relative clause, then "the list";
- **(4)** an attribute or relation of a known thing, used as a functional image, e.g. "the videos of the channel, newest first";
- **(7)** a derived noun defined once, scoped to a capability or group.

All three reuse machinery the language already has: definite descriptions, functional images, and term entries.

Explicit variables (1) are the least ambiguous, but they are what the person finds awkward. ACE supports them anyway, as "a list X". Named schemas (3) and group preconditions (6) are best kept as the *generator's* concern, a Gherkin Background, rather than a writer's construct.

### Cited Findings
- ACE variables are noun phrase appositions: "Variables can be introduced as noun phrase apposition, and can then be used as noun phrases", e.g. "A man X sleeps. X is young." With "something" the head can be dropped: "X weighs 300 kg. X is heavy." — [ACE Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)
- ACE resolves a definite noun phrase to "the most recent and most specific accessible noun phrase antecedent that agrees in gender and number". — [ACE Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)
- ACE's accessibility rules, which match DRT — [ACE Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html):
  - Antecedents in negated, modal, subordinated, interrogative or command sentences are not accessible.
  - Antecedents in universally quantified and if-then sentences are not accessible, except that the if-part is accessible from the then-part.
  - A disjunct's antecedent is accessible only in later disjuncts.
- If a definite noun phrase cannot be resolved, ACE "interpret[s it] as an indefinite noun phrase introducing a new entity". — [ACE Interpretation Rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)
- ACE's anaphora crosses sentences: "All sentences can anaphorically refer to preceding declarative sentences". — [ACE Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)
  - Example: "Mary enters a card into a machine. Its screen blinks."
  - Coordinated noun phrases form a plural that "they" can pick up.
- Relative clauses follow a noun phrase and can be coordinated: "a customer who is rich and who is well-known". — [ACE Construction Rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)
- Gherkin Background — [Cucumber Gherkin reference](https://cucumber.io/docs/gherkin/reference/):
  - "A Background allows you to add some context to the scenarios that follow it."
  - It belongs to one Feature or one Rule, and there is only one per Feature or Rule. Its Givens run before each scenario in its scope.
  - Advice: keep it to about four lines.
  - `Rule` (Gherkin 6+) groups the scenarios of one business rule, each Rule with its own Background.
- EARS "While" carries preconditions per requirement. A requirement has "zero or many preconditions" before its trigger. — [Wikipedia: EARS](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)
- OCL `sortedBy` and the iterators build a derived collection as an expression, so the collection can be named by its defining expression rather than by a variable. — [Eclipse OCL: Collection](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/Collection.html)

### Inferences
The comparison below is the researcher's analysis. Points marked **[bk]** rest on unverified background knowledge.

| # | Mechanism (example) | Unambiguity | Verbosity | Scope reach | Gherkin serialisation | Cost for this CNL |
|---|---|---|---|---|---|---|
| 1 | Explicit binding: Z/OCL/Alloy `let` **[bk]**, maths "Let L be ...", ACE "a list X" | Highest. A name binds exactly one referent. | A declaration line plus a symbol in every line; an awkward register for requirement writers. | Lexical: one expression (`let ... in`) or one section ("Let" in maths). | Easy: a Given that brings in the instance (`a list l1 ...`), then lines name `l1`. | Medium. It needs a new referent origin "declared", a scope (group), and a variable token in the grammar. ACE shows apposition fits GF/DRS. |
| 2 | Anaphora / definite description resolved by rules ("the list", "it"), DRT accessibility | Good when rules are strict (ACE: most recent and most specific accessible, else new entity). It breaks across boxes (every, not, if) and with two candidates. | Lowest. | One discourse. In this project a line is one discourse, so this works *within* a line, not across lines, unless the group is a discourse. | Easy within a line. Across lines it needs the generator to share referents, which spec_steps4 already does "by kind and rank" for a later requirement. | Lowest. R2 already exists. Only the scope question (line vs group) is new. |
| 3 | Named reusable definitions: Z schema inclusion, Alloy `fun`/`pred`, OCL `def:` **[bk]** | High. The name is global and typed. | One definition plus a name per use. Parameters (`feed[c]`) add syntax foreign to English. | Module or context-wide. | Medium. Each use expands into its definition's Givens. | High as a writer construct: a parameterised definition language. Low as a generator-side expansion of (7). |
| 4 | Attribute or relation of a known thing ("the videos of the channel, newest first", "the channel's feed") | High when the relation is functional. "the T of x" is already a functional image in this grammar. The order phrase must attach to the collection, not to "the channel". | Low. | Wherever x is in scope. No new object kind is needed beyond a collection-valued attribute or relation. | Easy: a Given of x and of its members with their attribute values. The ordering Then compares adjacent members. | Low. spec_rgl_np already makes "the T of x" and "its T". It needs a collection-valued relation row plus an order modifier. |
| 5 | Inline description once, then a definite NP ("... returns a list that holds every video of the channel, ordered by publication time, newest first. ... the list ...") | High within the line: the relative clause is the restrictor of one referent, and later "the list" binds by R2. | Medium. The first mention is long, later mentions short. | The line, or the group if referents persist. | Easy: the restrictor becomes Givens and Thens on one instance. | Low. It is relative clauses plus R2. New: an `every` inside a restrictor ("holds every video of the channel"), which already exists as `uscope`/`every` boxes, plus an order phrase. |
| 6 | Group or section-level shared context: SBVR definitional rules **[bk]**, EARS While, Gherkin Background, SbE key examples **[bk]** | Medium. Readers must look up to the group to know what "the list" is, and precedence between group and line context must be fixed. | Low per line. | The group or Rule. Matches Gherkin's Background scope (Feature or Rule) exactly. | Easiest: it *is* a Background or the group's given block. | Medium. The grammar has groups with given blocks (example data). Promoting a description to a group-level *referent* that R2 can bind to is a new kind of antecedent. |
| 7 | A derived noun defined once and scoped ("feed list: the list that holds every video of a channel, newest first"), in a capability's `## Terms` rather than the glossary | High: one meaning per noun. Ambiguity moves to the definition's quality. | Lowest at use ("the feed list of the channel"). | The capability (its `## Terms` layer), or the group if a group-level Terms is added. | Medium. The generator unfolds the definition into Givens on each use, as it reads definitions of conditions. | Low to medium. Capability-scoped `## Terms` and layered lexicons exist. The new parts are a *defined* collection noun whose definition is a restrictor plus an ordering, unfolded in the logical form. |

Further inferences:
- **Cheapest adoption** is (5) plus (4), with (7) for reuse:
  - (5) is "a K that ... ordered by T, D", then "the K". Every part except the order phrase and "every" inside a restrictor is already grammar 4, and R2 already binds "the K" to the earlier referent.
  - (4) is "the Ks of x, ordered by T, D". It reuses "the T of x" images.
  - (7) is a capability-scoped term whose definition is exactly a (5) description with its owner as parameter ("the feed list of a channel"). It removes repetition across lines without variables, because the owner, a referent the line already has, plays the role of the parameter. This is the standard way CNLs avoid `fun feed[c]` syntax.
- **Explicit "Let"** (1) gives the clearest scope, but it adds a variable namespace, a declaration form, and rules for shadowing and scope (line, group, capability). Its main benefit over (5)/(7) is naming *two* objects of the same kind in one line ("the old list" vs "the new list"). The existing `distinct`/"another K" and "two Ks" constructs partly cover that need.
- **Cross-line reference** (2 and 6) is the risky part. DRT accessibility is defined within a discourse, and ACE's fallback (an unresolved "the" becomes a new entity) would hide errors in requirements. A requirement CNL should *refuse* an unresolved "the" rather than accommodate it, as this project's R2 already does. A group-level antecedent (6) is a deliberate extension of the discourse to the group, and should only be allowed for referents introduced in the group's own preamble.
- **Gherkin**: every option ends as Givens bringing in an instance and its members. Options (5), (6) and (7) serialise without new step templates beyond collection membership and order. Option (1) adds only a naming convention. The deciding factor is the writer's experience, not the generator.
- The person's example rewritten without a variable:
  - (4)/(5): "When a viewer runs `feed show`, `feed` shall print the videos of the channel, newest first."
  - (7): with "feed list (noun): the list that holds every video of a channel, ordered by publication time, newest first", the line becomes "... `feed` shall print the feed list of the channel."

### Gaps
- Primary sources for Z schema inclusion, OCL `def:`, Alloy `fun`, SBVR definitional rules and Specification by Example's "key examples" (Adzic) were not fetched in this session. Those rows rest on background knowledge **[bk]**.
- I found no study measuring writer error rates for explicit variables vs definite descriptions in CNL requirements.
- DRT's formal accessibility (Kamp & Reyle) was cited only through ACE's interpretation rules, which implement it.
