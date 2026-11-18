---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-18-features-as-gf-concrete
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-18
---

# Can the features script be a GF concrete grammar?

The person's question (2026-11-18): "Please start a background research task on whether the features script can be
replaced by a concrete grammar in grammatical framework."

## Verdict

**Mostly no, with a small yes.** Most of what the question hopes for is done already: every step of a generated
scenario is linearised by GF from a tree of the step grammar 4 (`ContextSteps`, `spec_rgl_steps.text`). What Python
still does is **build those trees from the logical form**. That is planning, not linearisation. It names referents in
order of first mention, keeps one set of known referents across a whole group, splits cases, writes counter-examples
and leaves out entailed Thens using a clingo solve. A GF concrete grammar is compositional by definition: the
linearisation of a tree is a function of its subtrees' linearisations alone (GF reference manual, "Overview of GF" and
"Linearization definitions, lin": the mapping is "compositional, i.e. homomorphic"). So a concrete grammar cannot do
this part. GF's abstract-syntax computation (`def` rules, `pt -compute`, `pt -transfer`) could in principle do it.
In this installation it is unusable from Python, and it would be harder to write and debug than the Python it would
replace (spike below).

What is worth doing is small: move the **scenario layout** and the step text's **punctuation repairs** into the step
grammar. That is about 40 lines of Python, which a scenario abstract syntax over `Step` would take. The rest stays in
Python.

## What exists, by stage, with line counts

| stage | modules (lines) | already GF? | could a concrete grammar do it? |
|---|---|---|---|
| step surface: words, agreement, determiners, "the stage s1", "a stage s1", holds-blocks | `grammar/Steps4.gf` 15, `Steps4Eng.gf` 18, generated `ContextSteps` via `spec_rgl_steps.modules` (~40 of its 145), over `Base`/`BaseEng` 41+94, `Time*` 39, and Context from `spec_rgl.py` 207, `spec_rgl_np.py` 214, `spec_rgl_rel.py` 110, `spec_rgl_vocab.py` 140, `spec_rgl_time.py` 59 | **yes** | it already is |
| tree written out | `spec_rgl_steps.text` (~10 lines: two regexes repairing commas around an order, b275, b301; the colon of a block Given) | GF plus regex repairs | **yes**: the commas can be `BIND`/`SOFT_BIND` in the order's lin, and the colon too |
| scenario layout: tags, title and case, `And` for a repeated keyword, `# comment`, docstring and table blocks | `features_generate.written` (~20 lines) | no | **yes**: a `Scenario` category over `Step` lists. `And` is compositional if the abstract groups steps by keyword: a block's first step says the keyword and the rest say "And" |
| LF to step trees: referent naming, "the" bound to earlier referents, Givens at first mention, frame choice by kinds | `spec_steps4.py` 298 (`Reader.bind`, `name`, `introduce`, `bring_in`, `frame`, `np`, `read`) | no | **no**: one mutable state per scenario (`names`, `counts`, `known`, `shared`, `brought`, `dets`, `images`) threaded through every atom. `frame` picks among frames by kind ancestry (`boxes.fits`) |
| boxes: no, every, only, counts, images, Then order | `spec_steps4_boxes.py` 299 (`given`, `bring_response`, `no`, `link`, `acts`, `order`, `image`, `np_image`, `subst`) | no | **no**: `order` reorders the response so each description follows the act that brings its thing in (b268). That is a global reordering of the response, not a homomorphism |
| counter-examples and boundaries | `spec_steps4_counter.py` 170 (`each`, `failing`, `counter`, `unmet`, `only`, `upper`, `members`, `boundary`), `spec_steps4_held.py` 66 | no | **no**: it builds a new referent that fails the restriction's last atom, picking another value of an attribute from the lexicon. That is search over the vocabulary, not a reading of the tree |
| or-cases | `spec_steps4.cases` with `spec_lf_core.next_choice` | no | **no as linearisation**. GF `variants` give every combination of every `or` box, but the cases must stay consistent with one another (one choice per box, shared by every step), so variants would over-generate |
| the constructs' step parts | the `given`/`then`/`said`/`slot_arg`/`compared`/`every` functions of `spec_lf_option`, `_number`, `_ordered`, `_compare`, `_member`, `_order`, `_values`, `_exist`, `_set` (~250-320 lines, measured with `ast`) | no | mostly no: each reads the Reader's state (names, known referents, values chosen so far, `spec_lf_compare.values`) |
| entailed Thens | `features_generate4.entailed` (~20 lines) over `spec_entail.py` 158, `spec_entail_rules.py` 218, `grammar/entail.lp` | no (clingo) | **no**: a stratified answer-set solve |
| example data Givens | `features_generate4._example` | parses with GF, re-linearises with GF | already GF |
| reading features back: Gherkin, bindings, report, steps parsed into Calls | `features_gherkin.py` 142, `features_bindings.py` 145, `features_report.py` 77, `features_vocab4.py` 174, `scripts/features` 248 | `features_vocab4` parses with GF | **no**: these parse Gherkin files and pytest bindings, and report. That is not generation |

Totals: the Python that builds scenario trees (`spec_steps4*` 833 lines, about 300 lines of construct step parts,
`features_generate*.py` 190) is about **1,300 lines**. A concrete grammar could take about **40** of them. The rest
of the `features` command (`features_gherkin`, `_bindings`, `_report`, `_vocab4`, the CLI: 786 lines) reads and
reports rather than generates, and is outside the question.

## The spike: can GF's abstract computation do the planning?

The spike is in this record's folder (`Lf.gf`, `LfEng.gf`, `run.sh`). It has a toy logical form (`Rule while when
response`), a toy scenario (`Scen` of `SCons` steps) and a transfer `toScen` written as `def` rules over `data`
constructors. That is the only way GF computes on trees (manual, "Function definitions, def" and "Data constructors").
The spike found three things:

1. **The GF shell computes it.** `pt -compute (toScen ...) | l` gives "Given a the stage s 1 / Given the stage s 1 is
   `done` / When ... / Then ...". This also works with `pt -transfer=f` (`help pt`: "apply this transfer function to all
   maximal subtrees of suitable type").
2. **A missing case fails silently.** `givens (Cons (Writes ...) Nil)`, which has no equation for its argument, is
   left unevaluated with no error. The manual says abstract syntax checks types only, "with no exhaustiveness or
   overshadowing checks". If a constructor is not declared `data`, it silently turns into a variable pattern. Every
   missing construct, which is now a `TraceError` naming it, would become a stuck tree that linearises as nonsense or
   fails much later.
3. **The plugin's runtime cannot compute it.** `pgf.PGF.compute` in pgf 1.1, the C runtime's Python binding that the
   plugin loads, returns a tree with no defined function in it unchanged. On any tree that needs a `def` equation it
   **segfaults** (exit 139). The runtime API page (grammaticalframework.org/doc/runtime-api.html) documents parse,
   linearize, `Expr`/`unpack` and the visitor `embed`, and documents no computation. So a GF transfer would need the
   Haskell `gf` binary as a subprocess for each group, outside the parse cache, or a different runtime.

Even if the runtime worked, the planning state would have to be written as data threaded through every `def`
equation. That means Peano or list-encoded counters for "s1, s2", an equality function per pair of constructors to
check "already introduced", an association list for `names`, and a choice sequence for `or`. All of it would have to
be **generated per context**, because `ContextSteps`' funs are typed per kind (`K_Inst`, `K_Given`, `S_Does`), and
`spec_rgl_steps.py` would generate it. The Python would not disappear. It would move into a Python generator of GF
`def` rules, which is harder to read than the Python it replaces.

## Options weighed

- **A. Gherkin concrete syntax of grammar 4's requirement trees** (one `lin` per Base/Context fun, giving a
  scenario). Not possible. The scenario's shape depends on more than the tree: earlier requirements of the group,
  entailment by other lines, the lexicon's values for counter-examples. And the tree is not the meaning: the reading
  rules R1-R12 (`spec_lf_read`) and the "two meanings" refusal (`spec_meaning`) work on the logical form.
- **B. The logical form as a GF abstract syntax, with a Gherkin concrete syntax.** This runs into the same wall. The
  logical form's referents are variables with identity. GF trees have no shared nodes or binding apart from
  higher-order abstract syntax, and HOAS linearises bound variables as fresh symbols, not "s1, s2 by kind". Each
  step's text depends on whether its referent was mentioned before, which is context, not a subtree.
- **C. GF transfer (`def`, `pt -compute`/`-transfer`) from an LF abstract syntax to a scenario abstract syntax.**
  Possible in the gf shell (spike 1). It is ruled out by spikes 2 and 3 and by the generated per-context `def` rules.
- **D. The split: Python plans, GF writes.** This is **what the plugin already does** at the step level. It could go
  one level up: a `Scenario` abstract syntax in `Steps4.gf` (`Scen : Tags -> Title -> Blocks -> Scenario`, `GivenBlock
  : [Step] -> Block` and so on, `Comment : String -> Block`), with the comma and colon repairs moved into the lins.
  Python would hand GF one tree for each scenario rather than one for each step. This shrinks `features_generate.written`
  and `spec_rgl_steps.text`'s regexes (about 40 lines) and puts the punctuation where GF's `BIND` belongs. It does not
  shrink `spec_steps4*`.
- **E. PGF tree operations** (`Expr`, `unpack`, `visit`/`embed`). These are Python tree walks. `spec_gf.tree`/`expr`
  already convert to nested tuples, which the planners use. Moving to `pgf.Expr` objects would change only the
  representation.

## Costs and risks of option D (the only one worth doing)

- **Compile and cache.** `Steps4.gf` is a base file in every step grammar's sha (`spec_rgl_steps._load`), so any change
  recompiles every context's `ContextSteps`, about 20 s each, and invalidates every cached step parse
  (`spec_parse_cache`) once. That is a one-time cost and not per term. b351's cost is unchanged.
- **Parsing back.** `features_vocab4` parses each step with `startcat = Step`, and it must keep doing so. A `Scenario`
  start category would be for linearisation only. If Gherkin's layout lives in the grammar, the parser must not see
  it, or every step parse would also explore the scenario rules.
- **Debugging.** GF errors in a generated module, and `&+` or `BIND` behaviour in linearisation (the spike's raw
  shell output shows `&+` unbound without an unlexer), are less familiar than a Python regex. The current regexes are
  documented and tested.
- **Byte stability.** `features generate` output must stay byte-identical (`features generate --check`, the docs
  test). A move needs a regeneration of all 13 features with no diff as its check.

## What a split would look like (if taken up)

1. `Steps4.gf`: add `Scenario`, `Block`, `[Step]` and `Comment`. Use `Steps4Eng` lins for the keyword with "And" on
   the rest of a block, and `BIND` for the colon of a block Given and for an order's commas (the b275 and b301 rules).
2. `features_generate.written` builds one `Scenario` tree and linearises it. Docstrings and tables stay outside GF,
   because they are verbatim user text and GF tokenises.
3. `spec_rgl_steps.text` loses its regexes.
4. Check: `features generate` on every capability gives no diff.

The gain is small: about 40 lines, plus punctuation rules where the grammar can see them. It suits being done next
time something else touches `Steps4.gf`, rather than as an item of its own.

## Open questions for the person

1. Was the hope that GF would remove the **planning** (spec_steps4 and its kin, about 1,100 lines)? If so, the answer
   is no: that code is non-compositional by nature, and the GF route is crashing in pgf 1.1 or silent in the gf
   shell. Should it be closed there?
2. Is option D worth an idea item (`work idea`) on its own, or only as part of the next item that changes
   `Steps4.gf`?
3. Is reducing the planning code itself (a different question) of interest, for example by making `spec_steps4`'s
   Reader state explicit and smaller? That is a Python refactor, not a GF one.

## Sources

- GF reference manual, https://www.grammaticalframework.org/doc/gf-refman.html: "Overview of GF" (linearisation
  homomorphic), "Linearization definitions, lin", "Function definitions, def", "Data constructors", "Pattern
  matching" (no exhaustiveness check).
- GF runtime API, https://www.grammaticalframework.org/doc/runtime-api.html: Python's parse, linearize,
  `Expr`/`unpack`, `embed`/visitor. No computation is documented.
- `gf` 3.12 shell, `help pt`: `-compute`, `-transfer`.
- Spike: this record's folder, `run.sh` (GF 3.12, pgf 1.1, gf-rgl 20250812 as `tools probe` reports).
