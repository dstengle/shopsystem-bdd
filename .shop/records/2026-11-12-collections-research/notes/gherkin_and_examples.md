# How BDD and example-based tools express collections, ordered results and example data, and the oracle problem for generated scenarios

Scope note: this covers about 18 tool calls. Several primary pages could not be fetched: the Cucumber-JVM DataTable README and javadoc returned 404, the Veizaga MODELS 2020 PDF failed TLS and no PDF extractor was available, and the Concordion match-strategy page was not found. Facts that rest only on search-result snippets are marked "(snippet)". I found no source for the books (The Cucumber Book, BDD in Action, Specification by Example, Writing Great Specifications), so nothing below is attributed to them.

## 1. Cucumber/Gherkin data tables: Given tables of entities, Then tables of expected collections, ordered vs unordered diff

### Takeaway
Cucumber's own vocabulary separates the two questions: `DataTable.diff` compares in order, and `unorderedDiff` compares as a set. Both throw `TableDiffException` ("Tables were not identical") and mark rows with -/+. So "which members" and "in which order" are two different comparisons the step definition picks between. The Gherkin text itself never says which one is meant. Practitioner guidance on tables in Then steps is thin and mixed; one widely copied guide says to limit tables to Given steps.

### Cited Findings
- Cucumber-JVM 2.x `DataTable` has `unorderedDiff(DataTable)` and `unorderedDiff(List)`. Row order is ignored and the comparison works as a set difference. The ordered `diff` methods are the stricter form. Both throw `TableDiffException` (snippet). — [cucumber-core 2.0.0 DataTable javadoc](https://www.javadoc.io/static/io.cucumber/cucumber-core/2.0.0/cucumber/api/DataTable.html)
- The current standalone `io.cucumber.datatable` library (7.20.1) keeps `unorderedDiff` alongside `diff`, both throwing `TableDiffException` (snippet). — [io.cucumber.datatable 7.20.1 DataTable javadoc](https://javadoc.io/static/io.cucumber/datatable/7.20.1/io/cucumber/datatable/DataTable.html)
- A failure report reads "Tables were not identical" followed by the mismatched rows, from `TableDiffer.calculateDiffs` / `DataTable.diff` (snippet). — [Apache ServiceComb SCB-2201](https://issues.apache.org/jira/browse/SCB-2201)
- Cucumber-Ruby has a feature file documenting table diffing. Its output marks missing rows `(-)` and surplus rows `(+)` under "Tables were not identical" (snippet). — [cucumber-ruby table_diffing.feature (Debian sources copy)](https://sources.debian.org/src/ruby-cucumber-wire/0.0.1-3/features/table_diffing.feature)
- Best-practice guide: "Step tables may be attached to any step ... but as a best practice, it should be limited to Given steps" (snippet). The guide also says a single Then is preferred unless the rule has several related outcomes. — [andredesousa/gherkin-best-practices](https://github.com/andredesousa/gherkin-best-practices)
- A plain list makes you depend on item order, and one source suggests a map (key → attributes) for input data to avoid that (snippet). — via search, [helpmetest Gherkin best practices](https://helpmetest.com/blog/gherkin-scenarios-best-practices/)
- Cucumber's "Writing better Gherkin" asks: "Will this wording need to change if the implementation does?" It warns that "having too many implementation details in a scenario, makes it harder to understand the intended behaviour". It recommends moving specifics into step definitions. The page does not discuss data tables. — [cucumber.io: Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/)

### Inferences
- Concrete idioms the tools support (Gherkin shown as typically written; the data-table mechanics are the documented ones):
  ```gherkin
  Given the following items exist:
    | name | status    | created    |
    | a    | idea      | 2026-01-03 |
    | b    | shaped    | 2026-01-01 |
    | c    | delivered | 2026-01-02 |
  When I list the items newest first
  Then the listed items are, in order:
    | name |
    | a    |
    | c    |
    | b    |
  ```
  The step definition calls `expected.diff(actual)` for "in order" and `expected.unorderedDiff(actual)` for "are exactly" / "include". The words in the step text ("in order", "in any order") are the only place the reader learns which comparison is used, so a generator should put that word in the step it writes.
- Column subsetting is the norm. The Then table lists only the columns that matter to the rule ("name" above). The Given table lists the attributes the rule's conditions mention, plus a key. This addresses "incidental details" directly.
- A "transposed" table (attributes as rows) suits one entity with many attributes. Rows=items, columns=attributes suits collections.
- Background holds Givens shared by every scenario of a feature. That is relevant if the generator wants one population of items shared across a group's scenarios, but it costs locality.

### Gaps
- I could not retrieve the canonical Cucumber-JVM DataTable docs text (404). The exact current semantics of `diff` with respect to column subsets and the `asMaps` / `asList` / `transpose` signatures are unconfirmed here.
- I found no cited practitioner text (Cucumber Book, BDD in Action, Adzic, Seb Rose) specifically on "results are sorted newest first". The two common styles are (a) a Then table of the expected order and (b) a declarative step "the results are sorted by created, newest first" checked by a sortedness predicate. Both are well known but unsourced here.

## 2. FitNesse, Concordion, Gauge, Robot: how they split "which rows" from "in which order"

### Takeaway
FitNesse makes the split explicit with table types. A Query table is unordered set matching with missing/surplus reporting. An Ordered query table adds a relative order check. A Subset query table, by name, tolerates surplus rows; its page was not retrieved. Concordion's verifyRows is ordered by default, the author is told to sort, and match strategies were added in 2.0.

### Cited Findings
- FitNesse Query table: "The order of the rows is irrelevant." Rows match left to right by key column. An unmatched expected row is "missing", and an unmatched actual row is appended and marked "surplus". A blank cell is filled in from the actual result and counted as ignored. A `#`-prefixed header is a comment column. — [FitNesse QueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/QueryTable.html)
- FitNesse Ordered query table (`Ordered query:`) checks order *relatively*. With table {A,B,C} and result {B,C,A}, B and C are green and only A is red ("out of order: row 3", where 3 is the position in the result). The first table row can never be out of order. — [FitNesse OrderedQueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/OrderedQueryTable.html)
- Concordion `verify-rows` (`#var : expression`): "the order of the items in the table being verified must match the iteration order of the items returned by the expression". The docs advise sorting results so the order is predictable, and want the test to fail "If too many, too few, or the wrong users were returned". Since 2.0.0 a "match strategy" can define how rows are matched. — [Concordion instrumenting docs](https://concordion.org/instrumenting/java/html/#verify-rows-command)
- Concordion marks surplus rows with CSS class `surplus` and reports missing rows separately. — [Concordion verifyRows spec](https://concordion.github.io/concordion/latest/spec/common/command/verifyRows/VerifyRows.html); [Surplus rows](https://concordion.github.io/concordion/latest/spec/common/command/verifyRows/results/SurplusRows.html)

### Inferences
- These tools encode three comparison modes as distinct constructs: exact set (query), exact sequence (ordered query, verifyRows default), and subset/contains (subset query). A generator from requirement lines should map each to a distinct, readable step phrase, for example "holds exactly", "holds, in order", "holds at least". It should not leave the choice to the step definition.
- FitNesse's blank-cell rule ("ignored") is a precedent for a Then table that does not constrain some attributes. It is the dual of incidental-detail avoidance.
- FitNesse's relative order check gives better diagnostics than a positional one: one misplaced item is one red row, not a cascade.

### Gaps
- FitNesse Subset Query table semantics, Concordion's named match strategies, Gauge tables and Robot Framework list keywords were not retrieved. I have no sourced details on them.

## 3. Property-based testing and the oracle problem

### Takeaway
Property-based tools avoid writing expected outputs. They state properties: sortedness as "each adjacent pair is ordered", membership as "the output is a permutation of / a subset of the input", or agreement with a simpler model or reference implementation. Hypothesis's stateful testing runs the real system and a model side by side and asserts that they agree. For a generator of scenarios from rules, the analogue is a choice. The generator computes the expected Then from the rule (a model oracle), or the step checks a property over the actual output (a property oracle), or the author writes the expected table (a human oracle).

### Cited Findings
- Hypothesis `RuleBasedStateMachine`: `@rule` methods are chained in generated orders. A `Bundle` is "a named collection of generated values that can be reused by other operations". `@initialize`, `@precondition` and `@invariant` are provided. The example compares a real database with a simple in-memory model in every rule and "looks for discrepancies in their behaviour". — [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- Hypothesis article: when two implementations should agree, call both and assert equal outputs. A slow bubble sort served as the reference for a merge sort and exposed dropped leftover elements. — [hypothesis.works: Testing performance optimizations](https://hypothesis.works/articles/testing-performance-optimizations/)
- Hughes, "How to Specify It!" (TFP 2019, LNCS 12053, 2020) gives five generic ways to write properties, including model-based and metamorphic ones. His reported comparison found metamorphic and model-based properties most effective at finding bugs (secondary report). — [Chalmers research record](https://research.chalmers.se/publication/517894); [InfoQ summary](https://www.infoq.com/news/2020/02/property-based-testing-guide)
- The oracle problem in general: Barr, Harman, McMinn, Shahbaz, Yoo, "The Oracle Problem in Software Testing: A Survey", IEEE TSE 41(5), 2015, which classifies specified, derived, implicit and human oracles (not fetched in this session; cited from the known DOI). — [DOI 10.1109/TSE.2014.2372785](https://doi.org/10.1109/TSE.2014.2372785)

### Inferences
- Properties fit the ordering part of a rule well: "sorted by X descending" is checkable over any actual output without an expected table. Membership ("every K whose status is v appears") is checkable as the expected set computed by filtering the Given population. That expected set is a model oracle the generator can compute from the line's restrictor, because the Givens are generated too.
- A generator that already knows the Given population and the rule's restrictor/order key can *print* the computed expected table in the Then (the readable, example-style result) *and* rely on a property check in the step definition. This gives documentation value and robustness together, provided the line itself is the model. The danger is circularity: if the generator's reading of the line is wrong, the expected table is wrong in the same way. The human oracle (an author-written table) is the only guard against a misreading.
- Hypothesis Bundles are an analogue of named example instances: values produced by one step and referred to by later steps.

### Gaps
- No source found that discusses the oracle problem specifically for Gherkin generated from rules.

## 4. Binding named example entities to steps; anti-patterns

### Takeaway
Gherkin has no binding mechanism in the language beyond literal text and Scenario Outline `<placeholders>`. Named instances live in the step definitions' world/context, keyed by the names the steps use. The recognised anti-pattern is incidental detail: data that does not bear on the rule.

### Cited Findings
- Cucumber advises keeping specifics out of scenario text when they don't express behaviour, and asks whether the wording would change with the implementation. — [cucumber.io: Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/)
- FitNesse's key-column matching (the leftmost field identifies the row) is a form of binding expected rows to actual entities by name. — [FitNesse QueryTable](https://fitnesse.org/FitNesse/UserGuide/WritingAcceptanceTests/SliM/QueryTable.html)
- Hypothesis Bundles carry generated values from one rule to another by bundle name. — [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)

### Inferences
- For this tool: a Given table whose first column is the instance name (the same names steps use: `i1`, `i2` or `a`, `b`) binds rows to referents. Columns are restricted to the attributes the line's conditions and order key mention. A Then table keyed on that same column binds expected rows to them. This replaces the opaque "the <noun> `name` holds:" docstring with data bound to referents.
- The minimal-population heuristic ("two instances for every K") is sound for membership, but an order rule needs at least three items with distinct key values to tell ascending from descending and from insertion order. A filter rule needs at least one non-member, so the "which rows" check can fail.

### Gaps
- No sourced practitioner guidance found on minimal example counts for ordering.

## 5. Generating Gherkin from models, rules and controlled language

### Takeaway
The closest academic precedent is Veizaga et al. (MODELS 2020). It derives Gherkin acceptance criteria from UML models plus requirements in the Rimay controlled natural language, and reports that experts found no relevant information it missed (recall 100%). Most 2024-2026 work is LLM-based generation from user stories, and it reports invented information and inconsistent preconditions. That argues for deterministic generation from a parsed line, not free-text generation.

### Cited Findings
- Veizaga, Alférez, Torre, Sabetzadeh, Briand, Pitskhelauri, "Leveraging Natural-language Requirements for Deriving Better Acceptance Criteria from Models", MODELS 2020, DOI 10.1145/3365438.3410953. Acceptance criteria are expressed as sequences of Gherkin scenarios. Requirements are in Rimay, a CNL developed with a financial-domain partner. Experts "could not pinpoint any additional information ... relevant to AC but which had not already been brought to their attention" (recall 100%) (snippet). — [orbilu record](https://orbilu.uni.lu/handle/10993/43900); [Rimay thesis](https://orbilu.uni.lu/bitstream/10993/52324/1/UL-Thesis-Alvaro.pdf)
- Private-GPT study: LLMs with retrieval can produce conformant Gherkin from natural language but sometimes invent information (snippet). — [arXiv 2506.06509](https://arxiv.org/pdf/2506.06509)
- AgileGen discussion notes generated Gherkin with inconsistent preconditions across scenarios (snippet). — [arXiv 2507.14969](https://arxiv.org/pdf/2507.14969)
- AutoUAT: an LLM generates Gherkin from user stories, then Cypress scripts, with each step evaluated (snippet). — [arXiv 2504.07244](https://arxiv.org/pdf/2504.07244v1)
- Conformiq SmartGen converts requirements to Gherkin scenarios (vendor page, not read). — [Conformiq](https://conformiq.atlassian.net/wiki/spaces/CS/pages/3305209857/Converting+Requirements+to+Gherkin+Scenarios+through+SmartGen)

### Inferences
- On the trade-off between a verbose rule line and a sophisticated serializer, the evidence is indirect. Veizaga et al. needed *both* the model and the CNL text to get complete acceptance criteria. This suggests that the line should carry the semantic content (the restrictor, the order key and direction, and the comparison mode: exact, in order, or at least), while the serializer chooses the example population and prints tables. A line that omits the order key cannot be serialized into an ordered Then at all.

### Gaps
- GraphWalker, Specmatic and EARS-specific Gherkin generation papers were not found or not researched within budget.
- I could not read the full Veizaga text (TLS failure, no PDF extractor), so how it produces concrete example values is unknown.
