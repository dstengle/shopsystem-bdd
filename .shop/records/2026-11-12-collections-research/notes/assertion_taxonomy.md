# Collection assertions in business rules and test assertion libraries

Scope: assertions about collections of domain objects and their attributes (membership, emptiness, counts, uniqueness, ordering, positions, aggregates, comparisons between items, grouping, subsets, set vs sequence equality, filtering), as named by test assertion libraries (AssertJ, Hamcrest, Jest, Chai, NUnit) and as expressed in business-rule standards and rule languages (SBVR, RuleSpeak, DMN/FEEL, Drools DRL). UI assertions are out of scope.

## Q1. What kinds of collection assertions do business rules and tests make? (taxonomy)

### Takeaway
Across all sources the same roughly 12 families recur: (1) membership "contains", (2) "only" (nothing else), (3) "exactly" (same members, with or without order), (4) emptiness, (5) counts and bounds, (6) uniqueness, (7) quantified predicates (every/some/none/exactly n satisfy P), (8) ordering (natural or by a key, ascending or descending, then-by), (9) position (first/last/nth/single), (10) subsequence and contiguous sequence, (11) aggregates (sum, min, max, mean, count), (12) extract/filter/map as the step that turns domain objects into the values being asserted. Business-rule languages cover 1, 4, 5, 6, 7 and 11 richly, but ordering and positions almost only appear in the test libraries and in FEEL's `sort`.

### Cited Findings

**Membership, "only", "exactly" (the key three-way split)**
- AssertJ separates presence from exclusivity from exact equality: `contains` checks that the given values are present in any order, other elements allowed; `containsOnly` checks that the group holds only the given values in any order, ignoring duplicates ("once a value is found, its duplicates are also considered found"); `containsExactly` checks for exactly the given values and nothing else, **in order**; `containsExactlyInAnyOrder` is the same without the order (a multiset/bag equality) — [AssertJ docs](https://assertj.github.io/doc/)
- AssertJ also has `containsOnlyOnce` (each given value appears once) and `containsAnyOf` (at least one of the given values, an OR) — [AssertJ docs](https://assertj.github.io/doc/)
- Hamcrest: `hasItem` (at least one item matches or equals), `hasItems` (each given value found), `contains` (one pass yields items equal to the given items **in the same order**, i.e. exact sequence), `containsInAnyOrder` (each item matched by one of the given items, any order) — [Hamcrest 2.2 Matchers javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html). Note the naming clash: Hamcrest's `contains` is AssertJ's `containsExactly`, not AssertJ's `contains`.
- Chai: `.members(set)` = same members, any order, same length (strict `===`); `.deep` compares by structure; `.ordered` makes order matter; `.include.members` turns it into a superset test that ignores duplicates in the expected list; with `.ordered.include` the order is compared from the start of both arrays (prefix) — [Chai BDD API](https://www.chaijs.com/api/bdd/)
- Jest: `toContain(item)` (one item `===`), `toContainEqual(item)` (one item deeply equal), `expect.arrayContaining(array)` (all expected elements present, extras allowed, order ignored), `toEqual` on arrays (index-wise, order matters); Jest documents no order-insensitive exact-equality matcher and no sorted matcher — [Jest expect docs](https://jestjs.io/docs/expect)
- NUnit's collection constraints: `Is.EquivalentTo` (same items regardless of order), `Is.SubsetOf`, `Is.SupersetOf`, `Is.AnyOf` — [NUnit constraints](https://docs.nunit.org/articles/nunit/writing-tests/constraints/Constraints.html)
- Drools DRL: `contains` (a collection field contains a value: `/familyTree[ countries contains "UK" ]`) and `memberOf` (a field is a member of a collection variable) — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- FEEL: `list contains(list, element)`, `union`, `index of(list, match)` returning positions — [Camunda FEEL list functions](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)

**Emptiness, counts, bounds**
- Hamcrest `empty`, `emptyIterable`, `hasSize(n | matcher)`, `iterableWithSize(n | matcher)` — size may itself be compared with a matcher (e.g. greaterThan) — [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)
- Chai `.lengthOf(n)` chainable with `.above`, `.below`, `.least`, `.most`, `.within(start, finish)` (inclusive); Chai's docs recommend asserting the exact length instead of a range — [Chai BDD API](https://www.chaijs.com/api/bdd/)
- NUnit `Is.Empty`, `Has.Exactly(n)` — [NUnit constraints](https://docs.nunit.org/articles/nunit/writing-tests/constraints/Constraints.html)
- FEEL `count(list)`, Camunda's extension `is empty(list)` — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- SBVR Structured English quantifiers: "each", "at least one", "at least n", "at most one", "at most n", "at least n and at most m"; examples "It is obligatory that each rental has at most three additional drivers." and "...each rental car is owned by exactly one branch." — [SBVR Speaks (5), BRCommunity](https://brcommunity.com/articles.php?id=b286)
- SBVR's metamodel treats existential as at-least-n with n=1, and "exactly n" as at-least-n ∩ at-most-n; the OMG issue tracker notes "at most 1" in its intensive form is a uniqueness rule — [search summary of OMG SBVR issues SBVR-66/67, SBVR11-112](https://issues.omg.org/issues/SBVR11-112) (summary via search snippets; not read from the spec text itself)

**Uniqueness / duplicates**
- AssertJ `doesNotHaveDuplicates` and `containsOnlyOnce` — [AssertJ docs](https://assertj.github.io/doc/) (`doesNotHaveDuplicates` is named in the API but not described on the overview page)
- NUnit `Is.Unique` (UniqueItemsConstraint) — [NUnit constraints](https://docs.nunit.org/articles/nunit/writing-tests/constraints/Constraints.html)
- FEEL `distinct values(list)`, Camunda's `duplicate values(list)` (values occurring more than once) — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Drools `collectSet` accumulate function — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)

**Quantified predicates over items (every / some / none / exactly n)**
- AssertJ `allSatisfy`/`anySatisfy`/`noneSatisfy` (take nested assertions) and `allMatch`/`anyMatch`/`noneMatch` (take a predicate); `allSatisfy` reports every failing element — [AssertJ docs](https://assertj.github.io/doc/)
- Hamcrest `everyItem(matcher)`, `hasItem(matcher)` — [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)
- Jest `expect.arrayOf(value)` (every element matches) — [Jest expect docs](https://jestjs.io/docs/expect)
- NUnit `Is.All`, `Has.Some`, `Has.None`, `Has.Exactly(n)` — the only library seen with a counted quantifier over a predicate — [NUnit constraints](https://docs.nunit.org/articles/nunit/writing-tests/constraints/Constraints.html)
- FEEL quantified expressions `some x in L satisfies P` / `every x in L satisfies P`, e.g. `every i in [1,2,3] satisfies i <= 3`; `all(list)`/`any(list)` over booleans (all is true on an empty list) — [Trisotech FEEL reference](https://cloud.trisotech.com/help/decision-modeler/feel-basic-types-operators-and-statements.html); [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Drools `exists`, `not`, `forall( p1 p2 ...)` ≡ `not( p1 and not( and p2 ... ) )`; example "All full-time employees have red ID badges" — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- RuleSpeak "the following" clauses carry a threshold over a list of conditions: "All the following must be true...", "...if any of the following is true", "At least 2 of the following...", "At most only one of the following may be true...", "A customer must be exactly one of the following:"; bullets not numbers because order carries no meaning — [RuleSpeak tabulation](https://www.brcommunity.com/articles.php?id=b695)

**Ordering**
- AssertJ `isSorted()` "Verifies that the actual list is sorted in ascending order according to the natural ordering of its elements"; `isSortedAccordingTo(Comparator)` "...sorted according to the given comparator" — [AssertJ AbstractListAssert source](https://raw.githubusercontent.com/assertj/assertj/main/assertj-core/src/main/java/org/assertj/core/api/AbstractListAssert.java). The javadoc does not state whether equal neighbours pass (non-strict).
- NUnit is the richest: `Is.Ordered` (ascending default), `.Ascending`, `.Descending`, `.By("Length")` (by a named property), `.Then.By(...)` (secondary keys, each with its own direction), `.Using(IComparer | Comparison<T>)`; e.g. `Is.Ordered.By("Age").Then.By("Name")`, `Is.Ordered.Descending.By("Length")`; empty and one-element collections always count as ordered — [NUnit CollectionOrderedConstraint](https://docs.nunit.org/articles/nunit/writing-tests/constraints/CollectionOrderedConstraint.html)
- Chai has no "is sorted" assertion; `.ordered.members` compares order against an expected list — [Chai BDD API](https://www.chaijs.com/api/bdd/)
- Jest documents no sorted/ordered matcher; the doc's workaround is sorting both arrays then `toEqual` — [Jest expect docs](https://jestjs.io/docs/expect)
- FEEL `sort(list, precedes: function(x, y) -> boolean)`, e.g. `function(x,y) x < y` — ordering is a comparator ("precedes") function, not a key; also `reverse` — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Drools has no collection-ordering condition; ordering appears only as comparison operators on comparable properties, e.g. `/persons[ birthDate < $otherBirthDate ]` — which is the "one item's attribute vs another's" form — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- SBVR Speaks lists no ordering or collection keywords — [SBVR Speaks (5)](https://brcommunity.com/articles.php?id=b286)

**Relative order, subsequence, contiguous sequence**
- AssertJ `containsSequence` (in order, no extras between) vs `containsSubsequence` (in order, extras allowed between) — [AssertJ docs](https://assertj.github.io/doc/)
- Hamcrest `containsInRelativeOrder` (relative order, others allowed between) — [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)

**Position: first / last / nth / single**
- AssertJ `first()`, `last()`, `element(index)`, `singleElement()` (exactly one element, then navigate to it); `has(condition, index)`, `satisfies(requirements, index)` — [AssertJ docs](https://assertj.github.io/doc/); [AssertJ AbstractListAssert source](https://raw.githubusercontent.com/assertj/assertj/main/assertj-core/src/main/java/org/assertj/core/api/AbstractListAssert.java)
- FEEL `sublist(list, start[, length])`, 1-based, `-1` the last — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Jest `toHaveProperty('a.b[0]')` index path — [Jest expect docs](https://jestjs.io/docs/expect)

**Aggregates**
- FEEL `count`, `min`, `max`, `sum`, `product`, `mean`, `median`, `stddev`, `mode` — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Drools `accumulate( SOURCE; FUNCTIONS [; CONSTRAINTS] )` with `average`, `min`, `max`, `count`, `sum`, `collectList`, `collectSet`; example `accumulate( /orderItems( order == $order, $cost : cost, $price : price ); $avgProfit : average( 1 - $cost / $price ) )` — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- Test libraries have no aggregate assertions as such; one extracts then asserts (below).

**Extract / filter / map (projection from domain objects to values)**
- AssertJ `extracting(name | function)` (one value per element; several values as `tuple`s), `flatExtracting`, `map`; `filteredOn(predicate | property, value | function)` with `not`, `in`, `notIn`; `filteredOnNull`; `filteredOnAssertions`; `usingElementComparator` — [AssertJ docs](https://assertj.github.io/doc/)
- Hamcrest `hasProperty(name, matcher)` — [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)
- NUnit `.By("Property")` inside the ordering constraint — [NUnit](https://docs.nunit.org/articles/nunit/writing-tests/constraints/CollectionOrderedConstraint.html)
- FEEL filter expression `list[condition]` is a textual expression in the grammar — [DMN 1.4 FEEL grammar (dsntk mirror)](https://rust-digger.code-maven.com/src/dsntk-feel-grammar-0.0.9/DMN-1.4.md)
- Jest `toMatchObject` on arrays: same length, each element a partial-object match, index-wise — [Jest expect docs](https://jestjs.io/docs/expect)

**Comparisons between items**
- Only Drools shows a native form: a pattern binds one fact's attribute and a second pattern compares to it (`birthDate < $otherBirthDate`) — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- SBVR's "another" introduces a referent that is a different thing (distinctness), the basis for pairwise rules — [SBVR Speaks (5)](https://brcommunity.com/articles.php?id=b286)
- Test libraries express it indirectly: via sortedness (`isSortedAccordingTo`, `Is.Ordered.By`) or by extracting two elements and comparing them (`greaterThan`, `comparesEqualTo` on Comparables) — [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)

**Grouping / partition**
- Camunda FEEL `partition(list, size)` (chunks, not grouping by key) — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/). No library or rule standard read offered a first-class "group by key" assertion; Drools' accumulate with a constraint on the grouping fact (`order == $order`) is the closest (per-group aggregate) — [Drools](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)

### Inferences
- The three-way "contains / only / exactly" distinction, crossed with "ordered / any order", gives six membership assertions; the libraries disagree on names (Hamcrest `contains` = AssertJ `containsExactly`), so a requirement language should pick unambiguous English: "includes", "includes only", "is exactly ... in this order", "is exactly ... in any order".
- Multiset vs set semantics matter: AssertJ `containsOnly` and Chai `.include.members` ignore duplicates, `containsExactlyInAnyOrder` and NUnit `EquivalentTo` count them. A spec language must say which.
- Ordering in business rules is almost absent from SBVR/RuleSpeak/Drools; it appears in rule languages only as a function (FEEL `sort` with a precedes comparator). The test-library side (NUnit especially) shows the full shape needed: key(s), direction per key, then-by, custom comparator, empty/singleton trivially ordered.
- Strictness of ordering (ties allowed or not) is underspecified even in AssertJ's javadoc; a language should state it (non-strict "in ascending order of T" vs strict "each later item's T is greater").
- Item-vs-item comparison ("one item's T is before another's") reduces to two bound referents plus a comparison operator (Drools pattern), which is what "another" + an ordered comparison gives.

### Gaps
- Whether AssertJ `isSorted` accepts equal neighbours is not stated in the javadoc read; not verified from source code.
- SBVR spec text itself (ordinal/ordering concepts) was not read; SBVR quantifier facts come from the BRCommunity article and OMG issue snippets.
- FEEL filter-expression worked examples were not read from the OMG spec (the spec PDF exceeded fetch size); only the grammar mirror and vendor docs.

## Q2. How do test assertion libraries name these, and which are most used?

### Takeaway
Equality dominates: about half of all Hamcrest/AssertJ assertions found on GitHub are `equalTo`/`isEqualTo`, and developers use a small fraction of the API (51/87 Hamcrest matchers, 75/376 AssertJ methods ever appear). No per-method frequency for collection assertions was retrieved, so "how often" for each collection family is not empirically sourced here.

### Cited Findings
- Leotta et al. mined GitHub (repos with ≥6 commits, ≥2 contributors, ≥1 star/watcher, not forks): 44,592 Hamcrest hits in 2,279 files and 12,798 AssertJ hits in 770 files from 210 repositories; the top 45 matchers/methods cover 99.97% (Hamcrest) and 99.34% (AssertJ) of uses; "about the 50% of the assertions use equalTo or isEqualTo, and only 51 out of 87 Hamcrest matchers and 75 out of 376 AssertJ methods are used at least once" — [Leotta et al., Hamcrest vs AssertJ (QUATIC 2019)](https://sepl.dibris.unige.it/publications/2019-leotta-QUATIC.pdf)
- The same paper's illustrative chained collection assertion: `assertThat(fellowshipOfTheRing).hasSize(9).contains(frodo, sam).doesNotContain(sauron);` — [Leotta et al. 2019](https://sepl.dibris.unige.it/publications/2019-leotta-QUATIC.pdf)
- GitHub import counts (not method counts): ~3.18M for `org.junit.Assert` vs ~304K for `org.assertj.core.api` — [java-assertion-comparison](https://github.com/jrh3k5/java-assertion-comparison) (author notes GitHub search is not exhaustive)
- Zerouali & Mens studied 4,532 Java projects: AssertJ's share rising, >40% of AssertJ projects also use Hamcrest — [Zerouali & Mens, testing library evolution (slides/PDF)](https://www.researchgate.net/profile/Ahmed-Zerouali-2/publication/315637686_Analyzing_the_evolution_of_testing_library_usage_in_open_source_Java_projects/links/5c1a41d6458515a4c7e9c100/Analyzing-the-evolution-of-testing-library-usage-in-open-source-Java-projects.pdf) (via search summary of slides)
- Zhang & Mesbah (FSE 2015) classify assertions by content type only as number/string/boolean/object (no collection class) and by method type (assertTrue/False, assertEquals/NotEquals, assertNull/NotNull) — [Zhang & Mesbah, FSE 2015](https://people.ece.ubc.ca/amesbah/resources/papers/fse15.pdf)
- Aniche et al. (2013) report asserted object types including lists/arrays, with null checks ~3.8% (figure from slides, secondary) — [slides](https://www.slideshare.net/slideshow/slides-16987500/16987500); [paper](https://www.ime.usp.br/~gerosa/papers/What_Do_the_Asserts_in_a_Unit_Test_Tell_Us_about_Code_Quality_A_Study_on_Open_Source_and_Industrial_Projects.pdf)

Name crosswalk (from the docs cited in Q1):

| Concept | AssertJ | Hamcrest | Jest | Chai | NUnit | FEEL / Drools |
|---|---|---|---|---|---|---|
| has item(s), extras OK | `contains` | `hasItem(s)` | `toContain`, `arrayContaining` | `include`, `include.members` | `Has.Some`, `Is.SupersetOf` | `list contains`, `contains`, `memberOf` |
| only these (set) | `containsOnly` | — | — | — | `Is.SubsetOf` | — |
| exactly, any order (bag) | `containsExactlyInAnyOrder` | `containsInAnyOrder` | (length + arrayContaining) | `members` | `Is.EquivalentTo` | — |
| exactly, in order | `containsExactly` | `contains` | `toEqual` | `ordered.members` | (equality) | list `=` |
| relative order, gaps OK | `containsSubsequence` | `containsInRelativeOrder` | — | — | — | — |
| contiguous run | `containsSequence` | — | — | — | — | — |
| empty | `isEmpty` | `empty` | `toHaveLength(0)` | `empty` | `Is.Empty` | `is empty` (Camunda) |
| size / bound | `hasSize` | `hasSize(matcher)` | `toHaveLength` | `lengthOf().above…` | `Has.Exactly(n)` | `count` |
| unique | `doesNotHaveDuplicates` | — | — | — | `Is.Unique` | `distinct values` |
| every / some / none | `allSatisfy`, `anyMatch`, `noneMatch` | `everyItem`, `hasItem` | `arrayOf` | `satisfy` | `Is.All`, `Has.Some`, `Has.None` | `every/some … satisfies`; `forall`, `exists`, `not` |
| exactly n satisfy P | — | — | — | — | `Has.Exactly(n)` | — |
| sorted | `isSorted`, `isSortedAccordingTo` | — | — | — | `Is.Ordered[.Descending].By(p).Then.By(q)` | `sort(list, precedes)` |
| position | `first`, `last`, `element(i)`, `singleElement` | — | `toHaveProperty('[0]')` | — | — | `sublist` |
| project / filter | `extracting`, `filteredOn` | `hasProperty` | `toMatchObject` | — | `.By(p)` | `list[cond]`, patterns |
| aggregate | — | — | — | — | — | `sum/min/max/mean/count`, `accumulate` |

### Inferences
- Since ~50% of assertions are plain equality, most collection assertions in practice are likely `hasSize`/`isEmpty`/`contains`/`containsExactly` on extracted values; this is plausible but not measured in the sources read.
- The fact that only ~20% of AssertJ's API is ever used supports a small primitive set rather than mirroring a library.

### Gaps
- Leotta et al.'s Table 1 (top-45 methods with percentages) is in the PDF but its rows were not extractable as text; the per-method ranks for `hasSize`, `contains`, `containsExactly`, `isEmpty`, etc. are therefore not reported here. Reading the table from the PDF image would close this.
- No empirical study was found that measures how often business rules (as opposed to tests) state ordering or aggregates.
- No pytest-specific idiom documentation was fetched; Python tests typically compare lists with `==`, sets with `set(a) == set(b)`, `sorted(xs, key=...) == xs`, `all(...)`/`any(...)` (common knowledge, unsourced here).

## Q3. How do business-rule standards and decision languages express them?

### Takeaway
SBVR and RuleSpeak express collection constraints almost entirely through quantifiers on fact types ("each", "at least n", "at most one", "exactly one", "another") and thresholded condition lists; they have no ordering vocabulary. Executable rule languages add the computational side: FEEL has quantified and filter expressions plus list functions including `sort` with a precedes function and statistics; Drools has `exists`/`not`/`forall`, `contains`/`memberOf`, and `accumulate` aggregates, with ordering only as attribute comparisons between bound facts.

### Cited Findings
- SBVR keywords: "each" (universal), "at least one" (existential), "at least n", "at most one", "at most n", "at least n and at most m"; "a"/"an" universal or existential by context; "another" adds that the referent is a different thing. Modality prefixes "It is obligatory that", "It is necessary that", "It is prohibited that", "It is impossible that", "It is permitted that", "It is possible that"; embedded "must", "must not", "may", "always", "never", "sometimes" — [SBVR Speaks (5)](https://brcommunity.com/articles.php?id=b286)
- RuleSpeak: each rule statement uses exactly one of "must" or "only"; "if" for continuous conditions, "when" for points in time — [RuleSpeak sentence forms](https://www.brcommunity.com/articles.php?id=b472)
- RuleSpeak thresholded lists ("all", "any", "at least n", "at most only one", "exactly one of the following") — [RuleSpeak tabulation](https://www.brcommunity.com/articles.php?id=b695)
- Ross calls his classification schemes for rule types "the heart of Ross Method" — [Exploring Business Rules preface](https://brcommunity.com/articles.php?id=a439); a 2019 study found ten different classification schemes for business rules in the literature, i.e. no single accepted taxonomy — [Haan, Spruit, Zoet 2019](https://liacs.leidenuniv.nl/~spruitmr/pub/2019%20-%20Haan%20Spruit%20Zoet.pdf) (via search summary); some argue cardinality is a data-model constraint rather than a business rule — [BRCommunity, "Cardinality Is Not a Business Rule"](https://brcommunity.com/articles.php?id=b919)
- FEEL quantified expression grammar: `some|every name in expr (, name in expr)* satisfies expr`, returns a boolean; examples `every name in ["DMN","BPMN","CMMN"] satisfies ends with(name,"MN")` — [Trisotech FEEL](https://cloud.trisotech.com/help/decision-modeler/feel-basic-types-operators-and-statements.html); [DMN 1.4 grammar mirror](https://rust-digger.code-maven.com/src/dsntk-feel-grammar-0.0.9/DMN-1.4.md)
- FEEL list functions incl. `sort(list, precedes)`, `min/max` (require comparable elements), `sum/mean/median/stddev/mode`, `distinct values`, `index of`, `sublist`, `reverse`, `all/any` — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)
- Drools: `exists`, `not`, `forall`, `accumulate` (average/min/max/count/sum/collectList/collectSet), `memberOf`, `contains`, comparisons `<, <=, >, >=` only on comparable properties — [Drools language reference](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)

### Inferences
- An EARS-style language already resembling SBVR (each/no/at least n/another) is close to the rule-standard side; what it lacks is the FEEL/test-library side: a sequence value, a key/attribute projection, a comparator, aggregates.
- Business-rule standards mostly constrain the *state* of a fact population ("each X has at most n Y"); test libraries assert on the *output* of an operation (a returned/printed list, its order). For a CLI requirement language (lines about what `tool` prints), the output-sequence side (ordering, position, exact sequence) is the gap.

### Gaps
- Ross's own category list (e.g. whether he has an "ordering" or "sequence" rule type) was not retrieved.
- No SBVR text on ordinals ("first", "last", "nth") was found.

## Q4. What minimal set of primitives covers most of these?

### Takeaway
Nearly every assertion above is expressible as: a collection (set, bag, or sequence) + an optional filter (restrictor predicate) + an optional projection (key: an item's attribute) + one of {quantifier with count bound, comparison against an expected collection under set/bag/sequence equality and inclusion, ordering by key(s) with direction, position selector, aggregate compared to a value}. Ordering itself reduces to "every adjacent pair satisfies precedes-or-equal(key)", and item-vs-item comparison to two bound referents plus an ordered comparison.

### Cited Findings (evidence that these primitives are the ones the sources compose)
- Projection + assertion composition: AssertJ `extracting(...)` then any iterable assertion; NUnit `.By(property)`; Hamcrest `hasProperty` — [AssertJ docs](https://assertj.github.io/doc/); [NUnit ordered](https://docs.nunit.org/articles/nunit/writing-tests/constraints/CollectionOrderedConstraint.html); [Hamcrest javadoc](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)
- Filter + assertion: AssertJ `filteredOn`, FEEL `list[cond]`, Drools pattern constraints — [AssertJ docs](https://assertj.github.io/doc/); [DMN grammar mirror](https://rust-digger.code-maven.com/src/dsntk-feel-grammar-0.0.9/DMN-1.4.md); [Drools](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)
- Quantifier with counts as one family: SBVR at-least-n / at-most-n / exactly n = both; existential = at least 1 — [SBVR Speaks (5)](https://brcommunity.com/articles.php?id=b286); NUnit `Has.Exactly(n)`, `Has.None`, `Is.All` — [NUnit](https://docs.nunit.org/articles/nunit/writing-tests/constraints/Constraints.html)
- Ordering as comparator: FEEL `sort(list, precedes)`; AssertJ `isSortedAccordingTo(Comparator)`; NUnit `.Using(comparer)`, `.Then.By` for lexicographic multi-key — [Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/); [AssertJ source](https://raw.githubusercontent.com/assertj/assertj/main/assertj-core/src/main/java/org/assertj/core/api/AbstractListAssert.java); [NUnit](https://docs.nunit.org/articles/nunit/writing-tests/constraints/CollectionOrderedConstraint.html)
- `forall(p1 p2)` ≡ `not(p1 and not p2)` shows universal quantification reduces to negated existence — [Drools](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)

### Inferences (proposed primitive set; derived, not from a single source)
1. **Collection kind**: set (no order, no duplicates), bag (no order, duplicates count), sequence (order). Needed because libraries split exactly on this (containsOnly vs containsExactlyInAnyOrder vs containsExactly).
2. **Restrictor** (filter): "every K that P", "the Ks whose T is v" — already partly in the language (relative clauses, whose).
3. **Key** (projection): "by T", "the T of each K".
4. **Quantifier with bound**: every / some / no / at least n / at most n / exactly n — mostly present already (counts, every, no).
5. **Collection relation** against an expected list: includes, includes only, equals-as-set, equals-as-bag, equals-as-sequence, subsequence (gaps allowed), contiguous — the sequence variants are the new ones.
6. **Order**: "in ascending/descending order of T[, then of U]" with stated tie behaviour; empty and single-item trivially ordered (NUnit convention). Desugars to an adjacent-pair comparison.
7. **Position**: first, last, nth, the only one.
8. **Aggregate**: number (present), sum, min, max (mean/median rarer — only in FEEL/Drools).
9. **Pairwise comparison**: "the T of x is before/after/greater than the T of y" with x, y distinct referents ("another") — the Drools bound-pattern form.
- Frequency guess (not measured): families 4, 5 (includes/exactly) and emptiness/size likely dominate; ordering by one key is the most needed new primitive for CLI output; multi-key then-by, aggregates beyond count, contiguous sequences and grouping are rarer.

### Gaps
- No source quantifies how much of real-world rule or test corpora each primitive covers; the "covers most" claim is an inference from the API surfaces, not a measured coverage figure.
