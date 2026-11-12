---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-12-collections-research
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-12
---

# Collections, ordering and comparisons in requirement lines and their Gherkin

# Make list order a claim about pairs

A correct Gherkin scenario for a line like "`feed` shall return a video list that holds every video from the channel, newest first by publication time" needs five things the language does not hold today. It needs a **collection referent with membership** (`in(m, L)`), and a **closure** that says whether the list holds the restrictor's members at least, at most or exactly. It needs an **order** that every formal language surveyed reduces to a claim over pairs of members compared by a key attribute and a direction. It needs a **population** of at least three members with distinct key values plus one non-member, given in an order that is not the expected one. And it needs an **expected sequence** that the generator computes from those values and prints in a Then that names its comparison mode. Grammar 4's logical form already has most of the parts: the `every` and `only` boxes, the `in` relation row, `distinct`, and a `cmp` atom shape. What is missing is the comparison of two things' values (known limit #6, b266) and a reading of order over a collection (b267). Given blocks also have to stop being opaque and bind to the line's referents. The recommendation is to keep requirement lines free of variables and to accept a short order phrase ("newest first by publication time") as sugar that the **logical form** expands into a pairwise `every` box. Every reader then sees one representation: `model parse --form`, `model logic` and `spec_steps4`. The person's "list" type belongs on the collection noun's glossary entry as a default order. The "Let" belongs in the group's given block, which should name the instances the line's referents become and give their values, rather than in the lines. The work stages as b268 (Then order), then b266 (two-thing comparisons), then b267 split into closure-plus-binding and order. This report closes b269.

## Thirteen assertion families reduce to five primitives

Test libraries and rule languages assert about collections in roughly a dozen recurring ways. **Membership ("contains")** and **exclusivity ("only")** are the first two. **Exact equality** comes in three flavours (set, bag, sequence), and the rest are **emptiness**, **counts and bounds**, **uniqueness**, **quantified predicates** (every, some, none, exactly n), **ordering by a key** with a direction and a then-by, **position** (first, last, nth, single), **subsequence and contiguous run**, **aggregates**, and **projection and filtering**. AssertJ is the clearest on the membership split. `contains` allows extras in any order, `containsOnly` allows no extras and ignores duplicates, `containsExactly` means exactly these elements in this order, and `containsExactlyInAnyOrder` is bag equality ([AssertJ](https://assertj.github.io/doc/)). Library names disagree here and invite misreading: Hamcrest's `contains` is AssertJ's `containsExactly`, not its `contains` ([Hamcrest 2.2](https://hamcrest.org/JavaHamcrest/javadoc/2.2/org/hamcrest/Matchers.html)). A requirement language should therefore pick English that cannot be confused, such as "holds", "holds only" and "holds exactly … in this order". NUnit carries the fullest ordering vocabulary: `Is.Ordered.Descending.By("Length")`, `.Then.By(...)` for secondary keys each with its own direction, a custom comparer, and the rule that empty and one-element collections always count as ordered ([NUnit](https://docs.nunit.org/articles/nunit/writing-tests/constraints/CollectionOrderedConstraint.html)).

Business-rule standards cover a different half of the space. SBVR Structured English has "each", "at least n", "at most n", "exactly n" and "another", but no ordering vocabulary ([SBVR Speaks](https://brcommunity.com/articles.php?id=b286)). Drools has `exists`, `not`, `forall`, `contains`, `memberOf` and `accumulate` aggregates. It expresses order only as one bound fact's attribute compared with another's (`birthDate < $otherBirthDate`) ([Drools](https://docs.drools.org/latest/drools-docs/drools/language-reference/index.html)). Among the decision languages, FEEL has `sort(list, precedes)` with a comparator function ([Camunda FEEL](https://docs.camunda.io/docs/components/modeler/feel/builtin-functions/feel-built-in-functions-list/)). The split matters for this project. Rule standards constrain the *state* of a population ("each rental has at most three drivers"). Test libraries assert on the *output* of an operation, its returned list and its order. A CLI requirement language describes what a tool returns or prints, so it needs both, and the output-sequence side is the gap.

Usage data argues for a small primitive set over mirroring a library API. A GitHub mining study found that about half of all Hamcrest and AssertJ assertions are plain `equalTo`/`isEqualTo`. Only 51 of 87 Hamcrest matchers and 75 of 376 AssertJ methods appear at all ([Leotta et al. 2019](https://sepl.dibris.unige.it/publications/2019-leotta-QUATIC.pdf)). Per-method frequencies for the collection families were not recovered, so the priority order below is a judgement from this repository's own lines, not a measurement. The repository's phase 3 count is still telling. It found **24 lines needing COMPARE** (order or difference between values) and **16 needing NP-LIST**, against 1 to 4 each for AGGREGATE and ONLY ([phase 3 record](.shop/records/2026-11-08-cnl-research-phase-3.md)).

Every family composes from five primitives: a collection (set, bag or sequence), a **restrictor** (filter), a **key** (an attribute projected from each member), a **quantifier with a bound**, and a **relation** to either an expected collection or between members. Mapped onto grammar 4:

| Family | English a line would say | Grammar 4 today | Gap |
|---|---|---|---|
| Membership | "holds every video from the channel" | `every` box over an `in` row (works: TRIAL g5) | none |
| Only (⊆) | "holds only videos from the channel" | `only` box (works: TRIAL) | none |
| Exactly, as a set | "holds exactly the videos from the channel" | every + only, two clauses | one construct for both |
| Exactly, as a sequence | "holds, newest first by publication time, …" | none | **new: order** |
| Emptiness | "holds no video" | `no` box | none |
| Counts, bounds | "at most `n` videos", "the number of videos" | `count`, `number` boxes | none |
| Uniqueness | "no two videos of the list are the same video" | partial (`two`, `same`) | sequence vs set decided at the kind |
| Quantified predicate | "every video in the list is from the channel" | `every`, `count` in conditions | none |
| Ordering by key | "newest first by publication time" | only `Order:` on an attribute's *values* | **new** (b267) |
| Position | "the newest video", "the first K that P" | none (b189, limit #14) | later |
| Subsequence / run | "v1 comes before v2" | none | the pairwise atom covers relative order |
| Aggregates | "the highest release", "the sum" | `number` only (limit #3) | later |
| Pairwise comparison | "the publication time of x is after that of y" | parses in the time pack, unread downstream (limit #6) | **new** (b266) |
| Distribution | "every item with its title" | none (limit #10) | later |

The bold rows are the minimum a correct ordered-list scenario needs. Everything above them already exists in grammar 4.

## Formal languages state order as a claim over pairs

The formal specification languages agree on one point: **"sorted by key" is an assertion over pairs of positions, not a property of a type.** TLA+'s community module defines `IsSorted(s, op) == \A i, j \in 1..Len(s) : i < j => op(s[i], s[j])`, with "no assumptions … made about op" ([SequencesExt.tla](https://raw.githubusercontent.com/tlaplus/CommunityModules/master/modules/SequencesExt.tla)). The key and the direction fold into the comparison operator. Z makes a sequence a finite function from `1..n`, and it filters through `squash`, which keeps index order. A filtered sorted sequence therefore stays sorted without being restated ([Z/EVES toolkit](https://www.pst.ifi.lmu.de/Lehre/WS0001/gse/unterlagen/Z/Toolkit.pdf)). Alloy keeps two separate mechanisms. `seq T` is an indexed relation `Int->T` with `first`, `last`, `idxOf` and `hasDups` ([Alloy sequences](https://alloytools.org/quickguide/seq.html)). `util/ordering[S]` imposes one global total order on a whole signature, can be instantiated only once per signature, and "forces the signature to be exact" ([Alloy util/ordering](https://alloy.readthedocs.io/en/latest/modules/ordering.html)). That second mechanism is the counterpart of this repository's `Order: as listed.` on an attribute. It orders a domain, not a list. OCL is the one language with a key-based operation: `sortedBy(e | expr)` returns a Sequence of all source elements. Its four collection kinds cross ordered and unique: Set, OrderedSet, Bag and Sequence ([Eclipse OCL](https://help.eclipse.org/latest/topic/org.eclipse.ocl.doc/help/Collection.html)). Even in OCL, "is sorted" is written as equality with the sorted copy, which is a named predicate whose meaning is pairwise.

Controlled natural languages give the representation a DRT-style logical form should copy. ACE turns a plural into **one group referent with a cardinality**. Its members appear only through `has_part(Group, Member)` inside an implication box when a sentence distributes over them ([ACE 6.7 DRS report](https://attempto.ifi.uzh.ch/site/pubs/papers/drs_report_67.pdf)). Collective is ACE's default, and "each of" marks the distributive reading ([ACE interpretation rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)). ACE has comparatives and superlatives ("John is richer than Mary", "a richest customer") and list literals with "first element of". It has no ordering of a collection by an attribute ([ACE construction rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)). Grammar 4 has already chosen the other default. Its design says "No collective readings in 4.0", so "the tasks are done" means each task is done ([CNL 4 design](.shop/records/2026-11-09-cnl-4/design.md)). The `every` box over an `in` row is therefore ACE's `has_part` implication, already built. EARS fixes clause order (While, When, Where, If-Then), not data, and "is not an executable specification" ([Wikipedia: EARS](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)). SBVR fact types have a fixed number of roles ([AAAI SS-08-01](https://cdn.aaai.org/Symposia/Spring/2008/SS-08-01/SS08-01-010.pdf)), so an order in SBVR would have to be a fact type like "item1 precedes item2 in queue" plus a pairwise rule. The surveyed requirement and ontology CNLs (EARS, SBVR, Rabbit, PENG) showed no first-class "ordered by attribute" construct. That absence comes from the searches, not from a proof.

Example-based tools make the opposite split, and it is the one a generated Then must carry. Cucumber's `DataTable` offers `diff` (ordered) and `unorderedDiff` (as a set). The Gherkin text never says which one a step definition uses ([cucumber-core DataTable](https://www.javadoc.io/static/io.cucumber/cucumber-core/2.0.0/cucumber/api/DataTable.html)). FitNesse puts the choice in the table type. A Query table ignores row order and reports "missing" and "surplus" rows. An Ordered query table checks *relative* order, so one misplaced row is one red row, not a cascade ([FitNesse QueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/QueryTable.html); [OrderedQueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/OrderedQueryTable.html)). Concordion's `verify-rows` is ordered by default and tells authors to sort results so the order is predictable ([Concordion](https://concordion.org/instrumenting/java/html/#verify-rows-command)). The lesson for a generator is that **the comparison mode must be a word in the step text** ("in this order", "in any order", "and nothing else"). Otherwise the reader cannot tell what the scenario claims.

The two styles have clear trade-offs. Ordering as a type property is declared once and reads like the domain, and a generator can derive both the check and the data from it. It fixes one order per kind, though, and it puts a line's meaning in a declaration elsewhere. Ordering as a pairwise assertion is first-order and fits the existing `every` box and `distinct` atom, and clingo can check it directly. Written out in English it is verbose and easy to get wrong. The common hybrid is **a named order phrase whose meaning is the pairwise box**, which is what `IsSorted` and OCL's `= sortedBy` are. That hybrid is the recommendation here.

## Today's r9 loses its intent at three seams

The external context's latest-videos r9 shows exactly where the intent drains away. Its line today is "`feed` shall return a video list whose order is `newest-first` to the caller and return every video from the channel to the caller". `model parse --form` reads it as `order(x7) = newest-first`, a return of the list x7, and a separate `every [x8: video] from(x8, x2) scope return(e3, …, object: x8, …)`: a return of each video, not membership in the list ([repo baseline](.shop/records/2026-11-12-collections-research/notes/repo_baseline.md)).

**At the lexicon seam**, "newest first" lives only in the prose gloss of the noun value `newest-first`. *publication time* is a noun with `Kind of: result`, not an ordered attribute of video, so not even a comparison against a constant is available. The glossary's `video | in | video list` row goes unused.

**At the form seam**, nothing relates the list to its members, and no atom says anything about any pair of them.

**At the Gherkin seam**, the scenario brings in two videos with no publication times. It never says the returned list holds them. It asserts the order constant *before* the act that brings the list in, which is b268, caused by `acts` writing a response's non-event atoms in body order ([spec_steps4.py](scripts/spec_steps4.py)). Whatever step definition handles "the order of the video list v3 is `newest-first`" has to embed the whole rule, so the scenario documents nothing.

Two trials show how close the language already is. "`feed` shall return a video list that holds every video from the channel to the caller" parses to `every [x8: video] from(x8, x2) scope in(x8, x7)`. `features generate` then writes `the video list v4 holds the video v3` and `… holds the video v5`, so **membership works today**. "A video list that holds only videos from a channel" gives an `only` box, the "nothing else" closure. The trials also mark what fails. "The newest video" does not parse. Coordinated relative clauses on one noun ("whose order is … and that holds …") stop at the second clause. Making publication time a `moment` (to borrow the time pack's comparisons) broke r7, because a kind has one place in one kind tree, and `features generate` refused the moment comparison anyway ("no translation of a comparison of moments").

## Put the sophistication in the logical form, the oracle in the generator

Verbosity can sit in one of three places, and each choice also decides who computes the expected Then.

**Verbose line, simple serializer.** The writer spells out the pairwise rule: "every video in the returned list comes before each video in it whose publication time is earlier". The generator stays dumb, but the English is long and easy to misstate, and the strict-versus-non-strict question leaks into the wording.

**Short line, smart serializer.** The writer says "newest first by publication time", and `features generate` knows what that means. This is compact. But the meaning then lives in the serializer, invisible to `model logic` and `model parse --form`, and the lines and their tests can drift apart.

**Short line, desugared in the logical form.** This is the recommendation. The order phrase is a construct whose translation in `spec_lf` *is* the pairwise box. The check reads it as pairs, the generator reads it as pairs plus a population, and `model parse --form` shows both the phrase and its expansion. The repository already works this way for ordered comparisons against constants. `spec_lf_order` gives one translation of each construct "in each place a line is read": form, check facts and Given ([spec_lf_order.py](scripts/spec_lf_order.py)). The academic precedent points the same way. Veizaga et al. derived complete Gherkin acceptance criteria only from a CNL *and* a domain model together, and experts found no missing information ([Veizaga et al., MODELS 2020](https://orbilu.uni.lu/handle/10993/43900)). LLM generation from free text, by contrast, invents information and writes inconsistent preconditions ([arXiv 2506.06509](https://arxiv.org/pdf/2506.06509); [arXiv 2507.14969](https://arxiv.org/pdf/2507.14969)). The line must carry the semantic content (restrictor, key, direction, closure). The machinery chooses the example population and prints the tables.

**The oracle question has three answers**, and the generator should use two of them.

**A model oracle.** The generator computes the expected Then from the line. The generator writes the population itself, so it knows each member's key value and can sort them. This is the oracle a reader can check by eye: the expected sequence is printed in the scenario.

**A property oracle.** The step definition checks a predicate over the actual output, for example that each adjacent pair satisfies the key comparison. Property-based testing takes this route. Hypothesis's stateful testing runs the real system beside a simple model and looks for discrepancies ([Hypothesis stateful](https://hypothesis.readthedocs.io/en/latest/stateful.html)). Hughes found model-based and metamorphic properties the most effective at finding bugs ([InfoQ on Hughes 2020](https://www.infoq.com/news/2020/02/property-based-testing-guide)).

**A human oracle.** The author writes the expected table.

The danger of the model oracle is circularity: if the generator misreads the line, the expected sequence is wrong in the same way, and the test passes against a wrong program. The guard is that the generated scenario is a review artifact. A person reading "Then the video list v3 holds, in this order: v4, v2, v5" next to the Givens' times can see a misreading at once. A property-only Then ("the list is newest first") gives no such chance, because the rule hides inside the handler. The recommendation: **print the computed sequence and compare it exactly, in order**. A step definition can additionally check the sortedness property for a better failure message. FitNesse's relative-order diagnostics are the model for that message.

**The population is the part the generator does not do yet.** Today `spec_steps4` invents instance names and existence, but attribute values only where an ordered comparison forces one. An `every` box gives two copies so the line is not met vacuously ([spec_steps4.py](scripts/spec_steps4.py)). That is enough for membership but not for order. Two members cannot tell "newest first" from "insertion order" when they were inserted newest first. The rules for an ordered closure are:

- At least **three members** with **distinct** key values.
- **Given in an order that is neither the expected order nor its reverse**, so that insertion order, ascending order and descending order all differ.
- When the line states exclusivity, **one non-member** that fails the restrictor (a video from another channel), so the "nothing else" check can fail.
- If the population has a tie on the key, the generator refuses it unless the line states a tie-break. Without one, the expected sequence would be ambiguous.

This is the same move as `spec_lf_order.given`, which already writes "a Given of one value on the right side of every point the line names". It is extended from one thing against a constant to members against each other.

**Given blocks must bind to the line's referents.** Today a group's fenced `given` block may only say "the <words> `name` holds:" plus data. Each line is parsed as a Given sentence and prepended verbatim, and nothing ties its named instance to the generated ones. In batch-measurement g24 the block names "the measurement `m2`" while the scenario introduces "a measurement m1" and runs `measure show` on m1 ([batch-measurement.feature](features/batch-measurement.feature); [capability-file.md](docs/reference/capability-file.md)). The binding rule should be simple and visible:

- A block may hold any Given sentence of the step grammar 4 in its full form. That includes "a video v4 from the channel c1" and "the publication time of the video v4 is `2026-11-03T09:00Z`".
- An instance a block names is the line's referent of that kind, by **rank among the referents of that kind** (the same "kind and rank" rule `spec_steps4.bind` already uses across a group's lines), or by **name** when the generator would give that name.
- A block value **overrides** a generated value.
- A block that names **more** instances of a kind than the generator would bring **extends the population**. Three videos where `every` brings two is the case that ordering needs.
- A block value that **contradicts** the line refuses the group, naming the line and the value. One example is a block video that is not from the channel, standing where the line needs a member.

FitNesse's key column and Hypothesis's Bundles are the precedents. Rows bind to entities by a name the steps share ([FitNesse QueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/QueryTable.html); [Hypothesis stateful](https://hypothesis.readthedocs.io/en/latest/stateful.html)). Columns should be only the attributes the line's conditions and key mention. That also answers Cucumber's warning against incidental detail ([Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/)).

## The "list" type works as a default; the "Let" belongs in the given block

**The proposed "list" type**: a set of <object> ordered by <object> or by <object>.<attribute>. It is the type-property side of the hybrid and is sound as long as it does three things. First, it must **expand into the pairwise box** in the logical form, not be a primitive the check treats as opaque. Second, it must **make direction obligatory** and spell it with the key's order: newest or oldest first for a moment, highest or lowest first for a number, first or last first for an `Order: as listed.` domain. "Sorted by priority" alone is the classic inversion where priority 1 is the highest. Third, it must **decide set versus sequence**: whether a list may hold one video twice. OCL needed four collection kinds for exactly this reason. The two variants map onto the lexicon as it stands.

- **"Ordered by <object>"** orders members by their own value. That needs the member kind's values to be ordered, as a release's are by `Order: by number.`
- **"Ordered by <object>.<attribute>"** orders members by a key attribute. That needs the attribute to carry an `Order:`.

The natural home is the collection noun's entry. Its fields would be a member kind (the `in` row's other side) and the existing field name `Order:`, widened from "this attribute's values" to "this kind's members, by an attribute of theirs". For example:

```
video list (noun): the videos `feed` returns to a caller. Kind of: result.
  Members: video. Order: by publication time, newest first.

publication time (attribute of video): when the channel published the video.
  Order: by time.
```

A kind-level order has one weakness: a context that returns the same videos oldest first in another command needs a second kind. So the line should also accept the order phrase itself, which overrides the kind's default. The phrase alone is enough for a first stage. The kind-level default is a convenience that can follow.

For the Then, the proposed concrete Gherkin syntax should be a new step-grammar template that names its mode and takes a table keyed on instance names. A pairwise sentence form covers lines that state relative order without closure:

```gherkin
Then the video list v3 holds, in this order:
  | video |
  | v4    |
  | v2    |
  | v5    |
And the video list v3 holds no other video
```

```gherkin
Then the video list v3 holds the video v4 before the video v2
```

The first is FitNesse's ordered query, with the mode in the words. The second is Hamcrest's `containsInRelativeOrder` for one pair. Both must be readings of the step grammar 4, so that `features_vocab4` can read them back into a `Call` and `docs` tests can check them like every other step.

**The proposed "Let"** has a sound instinct behind it. The person wants to spell out the instances the lines speak of, close to the requirements, without writing glossary definitions. Explicit variables (ACE's apposition "a list X", maths' "Let L be …") are the least ambiguous mechanism, and ACE shows they fit a DRS ([ACE construction rules](https://attempto.ifi.uzh.ch/site/docs/ace_constructionrules.html)). They also add a variable namespace, a declaration form and shadowing rules to a language whose lines currently have none. The alternatives against the person's four criteria, grounded in what the repository has:

| Mechanism | Example | Ambiguity | Verbosity | Scope | Serialization | Exists today? |
|---|---|---|---|---|---|---|
| Explicit Let | "Let L be a video list that holds …" then "L" | lowest | a declaration plus a symbol per use | the group | easy: a Given brings L in | no: new origin, variable token, scope rules |
| Inline description, then "the K" | "return a video list that holds every video from the channel, newest first …"; later in the line "the video list" | low within a line (R2 binds to the latest accessible referent, else refuses) | first mention long, later short | one line | easy: the restrictor becomes Givens and Thens on one instance | **yes**: relative clauses and R2; new only the order phrase |
| Attribute or relation of a known thing | "the videos of the channel, newest first" | low when the row is functional | low | wherever the owner is | easy: Givens of the owner and its members | **mostly**: "the T of x", `of` images; new a collection-valued row |
| Capability- or group-scoped derived noun | `## Terms`: "feed list (noun): a video list that holds every video of a channel, newest first …"; line: "the feed list of the channel" | low; ambiguity moves into the definition | lowest at use | context-wide today (capability `## Terms` are pooled, not scoped) | medium: the definition unfolds into Givens at each use | partly: entries, but a noun's definition is unread |
| Group-level context | a group preamble introducing "the video list"; each line says "the video list" | medium: the reader looks up to the group | low per line | the group, the same as a Gherkin Rule's Background | easiest: it *is* a Background | no: a new antecedent source for R2 |
| Cross-line anaphora | line 1 introduces the list; line 2 says "the video list" | risky: binding depends on line order, and silent misbinding hides errors | lowest | the group as one discourse | needs response referents shared across lines | no: `st.refs` starts empty per line |

The ranking follows from the repository's own principle that **an unresolved "the" is refused, not accommodated**. ACE's fallback turns an unresolvable definite into a new entity ([ACE interpretation rules](https://attempto.ifi.uzh.ch/site/docs/ace_interpretationrules.html)), and grammar 4's R2 refuses instead, which is the right choice for requirements. Cross-line anaphora weakens that guarantee and should not be adopted. A group-level context helps only when several lines must speak of *one* response object. Grammar 4 has no origin for that: the shared referent would be a response-side thing that no line's trigger brings, and `model logic` would have to decide whether a group's lines join on it, against check.lp's rule "never join two requirement-level facts on a vocabulary word" ([check.lp](grammar/check.lp)). The inline description works with no new machinery beyond the order phrase. The attribute-of form costs little, and the derived noun gives reuse once a noun's definition is read.

The way out of the awkwardness: **what the person wants a Let for is already the job of the given block.** The block is group-scoped. It sits next to the lines and outside them. It names instances. It is serialized as the scenario's first Givens. Its only fault is that it binds to nothing. Once the binding rule above is in place, the block *is* the Let. It spells out the variables the lines use (the three videos, their channel, their publication times) in step sentences, and lines stay variable-free English that a reader takes as rules. The group of r9 would read:

````markdown
### g5 Latest videos, newest first

```given
a video v2 from the channel c1
the publication time of the video v2 is `2026-11-02T09:00Z`
a video v4 from the channel c1
the publication time of the video v4 is `2026-11-03T09:00Z`
a video v5 from the channel c1
the publication time of the video v5 is `2026-11-01T09:00Z`
```

- [r9] While a viewer subscribes to a channel, when a caller with the YouTube access of the viewer requests a video list, `feed` shall return a video list that holds every video from the channel, newest first by publication time.
````

The cost of this approach is the coupling to the generator's naming (v2, c1 and so on). Binding by kind and rank lets the block use any names it likes, so that coupling is a convenience, not a requirement.

## Worked example: r9 as line, form and scenario

**The line** stays as the person wrote it: "While a viewer subscribes to a channel, when a caller with the YouTube access of the viewer requests a video list, `feed` shall return a video list that holds every video from the channel, newest first by publication time." Two points of reading need fixing in `language.md`.

The first is **attachment**. The order phrase follows a relative clause, and it modifies the head noun "a video list", never the inner noun phrase "the channel". That is a grammar rule: an order phrase attaches only to a noun whose kind has a `Members:` (or an `in` row), and the key must be an attribute of that member kind.

The second is **closure**. "Holds every video from the channel" gives ⊇ only. If the intent is "and no other video", the line should say "holds exactly the videos from the channel", which reads as `every` plus `only`. Whether a bare "holds every K that P" in a response implies exactness is an open decision. Keeping it ⊇ keeps the language compositional.

**The lexicon** changes in two places: *publication time* becomes `(attribute of video)` with an `Order:` by time, and *video list* gains `Members: video`. The noun value `newest-first` and the attribute *order* retire.

**The logical form**, as `model parse --form` would show it. The trigger part is abbreviated from today's reading, and the order part is new:

```
while    [x1: viewer, x2: channel]  subscribe(x1, x2)
when     [x3: caller, x4: YouTube access, x5: video list]
         of(x4, x1)  with(x3, x4)  request(e1, subject: x3, object: x5)
response [x6: feed (constant), x7: video list]
         return(e2, subject: x6, object: x7, to: x3)
         every [x8: video] from(x8, x2)  scope in(x8, x7)
         order(x7, publication time, desc)
           = every [x9: video, x10: video] in(x9, x7) in(x10, x7) distinct(x9, x10)
                   before(x9, x10, x7)
             scope cmp(publication time(x9), at-or-after, publication time(x10))
```

The one new atom is `before(x, y, L)`: x comes before y in L, a strict order over positions. The one new comparison is `cmp` with a **referent's attribute on both sides**, which is b266's construct. The phrase "newest first" fixes `desc` and the non-strict `at-or-after`, so ties are allowed. `model logic` reads `in`, `before` and two-referent `cmp` as facts. Two lines that order one collection kind in opposite directions on one trigger then become an L1 conflict, decidable once a pair has two members with distinct keys. One way to decide two unknown values without Z3 is to let clingo guess a total preorder over the pair's own referents. The CNL 4 design reserved Z3 for exactly this case ([CNL 4 design](.shop/records/2026-11-09-cnl-4/design.md)), and the finite-preorder alternative is untested.

**The given data** is the block above: three members from c1, given in the order v2, v4, v5 with times 2nd, 3rd and 1st, so that insertion, ascending and descending orders all differ. If the line said "exactly", the generator would add a fourth video, v6, from a second channel c3, as the non-member. Without a block, the generator writes the same population itself with generated times that meet the same rule.

**The generated scenario**, with b268's fix (the act before its object's restrictions) and the expected sequence computed from the Givens' values:

```gherkin
Scenario: Latest videos, newest first
  Given a video v2 from the channel c1
  And the publication time of the video v2 is `2026-11-02T09:00Z`
  And a video v4 from the channel c1
  And the publication time of the video v4 is `2026-11-03T09:00Z`
  And a video v5 from the channel c1
  And the publication time of the video v5 is `2026-11-01T09:00Z`
  And a viewer v1
  And the viewer v1 subscribes to the channel c1
  And a caller c2 with the YouTube access of the viewer v1
  When the caller c2 requests a video list v6
  Then `feed` returns a video list v3 to the caller c2
  And the video list v3 holds, in this order:
    | video |
    | v4    |
    | v2    |
    | v5    |
```

The sequence v4, v2, v5 is the model oracle's output. A reviewer checks it against three timestamps in the Givens above it. The step definition diffs the actual list against the table in order. It can also check sortedness for its failure message, as FitNesse's ordered query marks only the misplaced row. Under "exactly", one more line would follow: "And the video list v3 holds no other video". The request's list keeps the name the generator gives it. The response's list is a new referent because the line says "a video list". Whether the response list should *be* the requested one ("return the video list it requested", which R2 already binds to x5 in the trial) is a modelling choice for the external context, and b266 names it.

## Open decisions and a four-stage plan

These decisions are the person's to make. The defaults recommended here are the second clause of each.

1. **Closure of "holds every K that P" in a response.** Recommended: ⊇ only, with a separate "holds exactly the Ks that P" for every-plus-only.
2. **Set or sequence.** May a list hold one thing twice? Recommended: a collection kind with `Members:` holds each thing at most once, which is OCL's OrderedSet. A bag waits for a line that needs one.
3. **Strictness and ties.** Recommended: non-strict. Equal keys may come in either order, and the generator never gives a tie. A then-by key ("then by title") waits for a line.
4. **Where the order is said.** Recommended: the line's order phrase first, with a kind-level `Order:` default on a collection noun as a later convenience.
5. **Direction words.** Recommended: tied to the key's `Order:` type: newest or oldest first for `by time`, highest or lowest first for `by number`, and spelled-out "in listed order" or "in reverse listed order" for `as listed`. Bare "sorted by T" and "in order" are refused.
6. **Moments as attribute values.** Recommended: a new `Order: by time.` on an attribute whose values are timestamps, instead of making the key a `moment` kind. The trial showed that a kind cannot sit in two places in the tree.
7. **The Then syntax.** Recommended: the ordered table form for a closure with three or more members, and the pairwise "holds x before y" sentence for relative-order lines. The table is a new step template with a table argument, and the docs' Gherkin tests then cover it.
8. **Given-block binding.** Recommended: by kind and rank, override on a value, extension on extra instances, and refusal on contradiction. This is not in b266–b268's reach and needs an item of its own.
9. **"Let".** Recommended: no variables in lines. The bound given block plays the Let's part. A group-level antecedent is reconsidered only if a group's lines must share one response object.
10. **`model logic`'s reading of two-referent comparisons.** Recommended: a guessed finite preorder over a pair's referents in clingo first, and Z3 only if that fails on real lines.

**The staged plan** maps the backlog onto these stages.

**Stage 1 is b268.** The generator writes a response referent's introducing act before its restrictions. It is small, independent and needed by every later Then. Without it a collection Then reads backwards.

**Stage 2 is b266.** It brings two things' values compared ("the publication time of x is after the publication time of y") in the grammar, the form's `cmp` with a referent's attribute on both sides, `model logic`'s reading of it, and `spec_steps4`'s Givens that give each thing a value meeting it. It retires known limit #6, lets migration-tools r77–r80 compare the repository's release with the plugin's, and lays the atom that the order expansion stands on. Response identity ("the video list it requested") sits here too, since b266 already names it.

**Stage 3 is b267 part A, closure and binding.** It covers "holds exactly the Ks that P", coordinated relative clauses on one noun ("whose … and that …"), the `Members:` field, and the given-block binding of decision 8. Binding should be carved out as a new item, because it also repairs batch-measurement g24's m2-versus-m1 split, which has nothing to do with order.

**Stage 4 is b267 part B, order.** It adds the order phrase and its pairwise expansion in `spec_lf`, the `before` atom, `Order: by time`, the generator's population rules (three members, distinct keys, a shuffled insertion order, a non-member under exactness), the computed expected sequence and the ordered-table Then.

Later work builds on the same atoms. **b189** ("the newest K") becomes a position over a declared order rather than a stand-alone superlative. Known limit #14's ordered choice and "up to n in rank order" are a position and a bound over an ordered collection. Limit #10's "each of the Ks" and "every item with its title" are distribution over members. Aggregates (#3) come last. **b269** is closed by this report.

## Conclusion

The question looked like "what syntax should a list have". The answer turns on **where meaning lives**. Every formal tradition agrees that order is a claim over pairs, and this repository already has the habit of giving each construct one translation that every reader shares. Putting the order phrase's meaning in the logical form, rather than in a type or in the serializer, makes the line, the check and the scenario agree by construction. It also means the generator's computed expected sequence is never a second opinion. The remaining risk is circularity: a misread line yields a scenario that agrees with the misreading. The defence is to make the scenario readable enough that a person checks the sequence against three printed timestamps, and that is why the Then should be a printed table and not a property.

The second shift concerns "Let". The person's discomfort with variables in requirement lines is well founded, and the need behind it is real. The given block already does that job, group-scoped and outside the lines. It is simply disconnected. Binding it to the line's referents serves the Let's purpose with no new syntax in the requirement language. It also fixes an unrelated defect (g24) and gives ordering the one thing it cannot do without: concrete key values in a known order. Done in that order (b268, b266, binding, then order), each stage stands on its own and delivers lines that could not be written before.
