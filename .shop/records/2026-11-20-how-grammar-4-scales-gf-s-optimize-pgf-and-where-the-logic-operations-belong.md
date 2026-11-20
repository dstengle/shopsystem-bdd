---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-20-how-grammar-4-scales-gf-s-optimize-pgf-and-where-the-logic-operations-belong
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-20
---

# How grammar 4 scales, GF's optimize-pgf, and where the logic operations belong

## 1. How grammar 4 scales

**What was measured.** The synthetic contexts had N objects, so N+9 kinds. Each object had 1 attribute with 3 values, 1 state verb, 1 action verb, a `has` and a `holds` row, and an `on` row on every third object. Each was compiled with GF 3.12 and parsed with the pgf C runtime. This repository was measured as a reference: 214 kinds, about 2,000 abstract categories and 8,853 functions. Main moved during the runs (batch-56), so the line counts are 402-413 depending on the snapshot. Every comparison was paired within one snapshot.

**Growth with independent kinds (the generator is linear):**

| N objects | 5 | 50 | 100 | 200 | 500 | 1000 |
|---|---|---|---|---|---|---|
| funs | 637 | 4,378 | 8,535 | 16,848 | 42,288 | 84,355 |
| PMCFG productions | 11,815 | 88,927 | 174,608 | 345,967 | 860,547 | – |
| compile (s, quiet) | 0.55 | 4.4 | 9.2 | 20.3 | 156 | 489 |
| peak RSS (MB) | 75 | 293 | 540 | 992 | 2,397 | 4,730 |
| PGF (MB) | 0.42 | 3.15 | 6.24 | 12.8 | 33.5 | 67.8 |
| parse, 21 short lines (ms, mean) | 11 | 63 | 149 | 345 | 1,006 | 2,210 |

- Functions grow by about 83 per kind and productions by exactly 1,714N + 3,245. RSS grows by about 4.7 MB per kind.
- Compile time grows faster than linearly: t ≈ 0.0047·N + 4.84e-4·N² s.
- Parse time grows about as N^1.17, even on lines that name only 3-5 kinds.
- This repository's 402 lines (mean 199 characters) parse in 1.02 s mean, 1.98 s p95 and 411 s summed. The Context compile takes 19-21 s and 1.1 GB.

**Categories are the wrong predictor.** Two investigations refute the earlier record's rule ("about linear in the number of categories"). Cost follows PMCFG productions and functions over heavy RGL records:
- This repository (2,000 categories, 360,550 productions) and syn200 (3,691 categories, 345,967 productions) parse alike (0.575 vs 0.526 s, paired).
- The factored grammar has 24% more categories and parses 12-14 times faster.
- A partial collapse to 1,102 categories parsed 3.5 times slower than today.

**Which generators multiply:**
- **The object relative clause `K_Obj_S_O`** (spec_rgl_rel.py:90-98) makes one function per (gap S,O) × kind under O, and each has 180 productions.
  - In this repository, 4 gaps over `thing` (k_interpreter, k_measurement, k_requirement and k_text `_Gap_k_thing`) × 214 kinds give 856 functions and 154,080 productions (44.5%). With `file` (39,600) and `text` (21,960) the share is 62%.
  - None of the 856 functions over `thing` is used by a live line. Of all 1,451 Obj functions, 25 are used.
  - A synthetic vocabulary with one broad frame per 25 kinds makes the grammar quadratic: P ≈ 1,828N + 7.04N². It compiles at 500 kinds in 324 s and 8.2 GB, and parses in 3.99 s a line.
- **`spec_rgl_np.senses`** (spec_rgl_np.py:95-107) makes 2·A·(A−1) functions for A attributes that share one word.
  - Today this is harmless: `status` is shared 9 ways, giving 168 functions and 1,344 productions.
  - At A=200 it gives 79,600 functions, a 265 s compile and 4.1 GB.
- **The lists `K_Two`/`K_More`** have 80 productions each, 9.9% today and 34% once the relative clause is factored.

**Extrapolation (disputed; it rests on assumptions).**
- Today's grammar at this repository's density, parsed serially and cold:
  - 5,000 lines take about 85 minutes at 214 kinds.
  - At 500 kinds about 2.8 s a line (3.8 h). At 1,000 kinds about 6.2 s a line (8.6 h).
  - If broad frames grow with the vocabulary, about 11-25 s a line.
  - A compile at 1,000 kinds takes 480-490 s and 3.3-4.7 GB, and a bar run does 2-3 compiles.
- The skeptic disputes these figures:
  - They assume 500-1,000 kinds come with 5,000 lines.
  - They scale long lines by an exponent fitted on short lines.
  - Parsing is serial today: no module but model_decisions uses a process pool.
  - Each worker would also load the PGF: 0.25 s and +80 MB today, 1.14 s and +399 MB at 1,000 kinds.

**Two facts that make cold runs the normal case:**
- The parse cache key (spec_parse_cache.key, line 23) includes the sha of the grammar's sources. Any new term therefore invalidates every cached parse.
- The readiness bar lays an item's lines on a copy of the spec. An item that adds a term therefore pays a cold parse of every line.

**GF compile phases (disputed).**
- On the factored prototype, from 200 to 500 kinds:
  - The abstract check went from 2.0 to 15.3 s.
  - The link and PGF write went from 3.6 to 41 s.
  - The same functions as 4 chained modules checked in 3.5 s instead of 15.8 s.
- GHC's garbage collector took 25-35% of the time, and no RTS flag helped.
- The exponents rest on two points each and are not established.

## 2. `--optimize-pgf`

**What it does.** It removes concrete labels (fields) that the start category `Req` never uses. Our lincats are full RGL records (VP, NP, CN), and the C parser carries every field.

| | plain | optimized |
|---|---|---|
| labels | 39,207 | 6,113 |
| fid × labels | 457,807 | 60,890 |
| cncfuns | 120,101 | 20,467 |
| PGF size | 13.0 MB | 2.3 MB |
| readPGF | 0.20 s | 0.035 s |
| process RSS after one parse | 165 MB | 24 MB |

- Examples: `k_agent_V` goes from 96 labels to 10, and the `k_*_St` state frames lose 8,415 labels.
- Categories and fids do not change (1,997 and 14,807).
- Compile time changes by less than 1 s.

**Every differing line has one cause, a GF bug.**
- Unfixed, the optimized PGF fails to parse 102 of 405 lines (25%). Each of the 102 is a ParseError, never a different tree.
- The parses stop at 28 distinct tokens, all next to the mis-sorted range: 'Python' and 'before' 14 times each, '`L1`' 13, '`in-batch`' 11, '`idea`' 10, and others.
- The earlier record's "4 of 12 lines differ" is the same bug.
- The cause, checked by both investigator and skeptic in the sources:
  - `PGF/Optimize.hs` (reorderSeqs/ciCmp, lines 181-184) sorts case-sensitively only when the flag `case_sensitive` is `"on"`. The same code is on gf-core master.
  - The compiler never writes `"on"`: `GF/Infra/Option.hs:238` writes only `"off"`.
  - The C runtime treats a missing flag as case-sensitive (`scanner.c:133-145`) and binary-searches the table that way (`parser.c:911-950`).
  - So the table is sorted in one order and searched in another. It has 11 case-sensitive inversions, such as '`awaiting-upstream`' before '`Behaviour`'. The unoptimized path (`GrammarToPGF.hs:61`) is consistent.
- This is GF's bug, not our grammar's.

**With the table re-sorted case-sensitively ("optfix"):**
- 405 of 405 lines give identical trees, with a median paired speed-up of 30.8 times (6.7-63.3).
- End to end through `spec_grammar4.parse` with the cache bypassed:
  - 413 live lines: 0 differences (442.6 s → 18.3 s).
  - 105 mutated lines: 0 differences in refusal text and error offsets.
  - The ambiguity refusal: identical.
- The re-sort is the identity on an unoptimized PGF (0 of 6,454 sequences moved).
- The skeptic re-ran 10 lines holding `L1`, `in-batch`, `Behaviour`, 'Python' or 'before': identical, at 0.017-0.074 s against 0.41-1.82 s.

**Workarounds that do not work:**
- `--case_sensitive=on` and `flags case_sensitive = on` give a byte-identical PGF, so the flag is still missing.
- `--case_sensitive=off` avoids the loss but changes the language. It accepts 'the Person', ' Shall ' and '`MISSING`' for `missing`, and reads a code `l1` two ways beside the value `L1`.

**A second failure class: subtree linearization aborts (our code).**
- Linearizing a non-start subtree on the optimized PGF kills the process with SIGABRT: `pgf_lzr_linearize_tree (pgf/linearizer.c:925): precondition failed lin_idx < fun->n_lins`.
  - 167 of 1,105 categories abort, among them k_artifact_NP, k_agent_V and 55 `k_*_St`.
  - Python cannot catch it. A crashed `work ready` or pytest worker results, not a refusal.
- Our code does this in several places:
  - `spec_grammar4._words`, used by `_two` (the ambiguity refusal) and by `spec_one_thing.refusal` (b420).
  - The 8 call sites in features_vocab4.py:153-170, through `spec_rgl_steps.text`.
- On the plain PGF, a VP-level subtree already linearizes to ''.
- **The step grammar.** The skeptic optimized and re-sorted ContextSteps and read all 1,599 distinct steps of features/*.feature:
  - 1,405 read identically and 8 fail identically.
  - 186 (11.6%) abort.
  - So the option cannot be applied to ContextSteps until subtree linearization goes through `bracketedLinearize` of the whole tree.
- The proposal that cited spec_grammar4.py:208 is stale on main. The skeptic found the sites above.

**Other effects:**
- GF's `complete()` is incomplete on both PGFs, missing a different token on 1 of 180 prefixes. Only hints are affected.
- With the bug unfixed, the refusal pipeline can turn a lost parse into a wrong but plausible message, e.g. batches#r50: "the verb change takes as its subject agent…". A guard is needed in case the sort ever regresses.
- Not measured:
  - Optimized PGFs at other vocabulary sizes.
  - The other contexts the suite parses (fixtures, docs, constructs).

**The other options give nothing:**
- `--optimize=none|values|parametrize|all` write PGFs byte-identical to plain.
- The heuristic search factor is equal at 0-0.5 and slower at 0.95 (103.5 s against 85 s).
- The start category is already `Req`.

## 3. The grammar's health

**Ambiguity.** All 405 live lines have exactly 1 tree, even with up to 200 trees taken. Coercions never stack: each `K_Up_A` goes from NP0 to NP once per (kind, ancestor). So `spec_meaning.one`'s tie-break and `LIMIT=50` never choose on a live line.

**Issues, ranked by parse-time cost (paired, families removed or factored):**
1. **Object relative clause `K_Obj_S_O`.**
   - It is 16.5% of the functions and 67% of the PGF's bytes.
   - Removing it takes the parse to ×0.10. Factoring it takes the parse to ×0.074-0.11 and keeps every line.
   - Fix it in our grammar.
2. **Subject relative clause `K_Rel_S` (482 functions) and `K_Whose_*` (397).**
   - Factored together with Obj ("factor4"), the parse is ×0.074 (skeptic ×0.082) and every line is kept.
   - The skeptic refuted the claim that Rel and Whose alone give a further gain: it is a share of productions, not a measured time.
3. **The `K_Up_K` coercions (393).** Removing them gives ×0.47 on top of the factored grammar, but breaks 75 of 81 lines. They are needed.
4. **The lists and counts** (And, Or, Two, More, Only, NamedAnd, NumberOf). Removing them gives ×0.67.
   - The proposal to list `K_NP0` instead of `K_NP` is refuted: 65 of 402 lines list a code or a coerced NP, e.g. line 104 '`holds-exactly` and `of-relation`'.
5. **`senses`.** Latent and quadratic (section 1).
6. **Dead weight** (no parse cost; the optimizer prunes it):
   - `t_revision_4_Val` has no producing function. It comes from `revision (text)` with no values, spec/model/analysis.md:25, and 5 functions consume it. Plain completion offers 'revision' and 'coverage', which can never finish a sentence.
   - 93-95 categories are unreachable from `Req` in Context. Some are reached by ContextSteps' `r<n>_<word>_Is` (rows 9, 20 and 27), so they cannot all be dropped.
   - BaseEng.gf:73-81 gives 6 ambiguous-constructor warnings for mkAdN and mkQuant.

**Costs in our scripts, not the grammar:**
- **Hints.** `spec_follow4._next` re-parses each completion candidate. At '... shall keep a' that is 181 candidates × 0.52 s, about 95 s per hint (about 6 s factored).
  - The re-parse is load-bearing. `complete()` takes no literal callback, so 43% of candidates (1,229 of 2,832) on prefixes with no code are false, e.g. ('when', 'Behaviour').
  - Skipping the re-parse is refuted.
- **ContextSteps recompiles all of Context from source** in a fresh mkdtemp (spec_rgl_steps.py:72-89 → spec_gf.py:86).
  - Copying Context's .gf and .gfo with their mtimes gives a byte-identical PGF.
  - It takes 8.45-10.6 s → 2.57-2.81 s at 100 kinds.

**How we use GF and the RGL against normal practice:**
- **Calls.** The start category is Req. The heuristic and the String callback are not levers: 15.8 callback calls a line cost under 1%. 92.5% of a parse passes before the first tree, in chart construction that the grammar's shape decides.
- **The RGL.** It is used as intended for agreement, negation, relative clauses and NPs: mkCN 3,670, mkRS 2,330, mkNP 1,734. Hand-rolled `{s : Str}` appears only for values, codes, counts and request parameters. These are small families and deliberate.
- **Where we differ from normal practice:** we multiply relative clauses per kind. The RGL builds an RS once and attaches it with RelCN. Factoring brings us back to the RGL's shape.
- **One category per kind against dependent types.** The pgf C runtime erases dependent types. It parsed 'a person opens a person' to `Pred ? aPerson opens aPerson`, and `checkExpr` accepts the ill-typed tree too. Only GF's Haskell shell rejects it. So with our runtime, dependent types cannot check kinds, and "few categories" always means a check after the parse.
- **Per-kind typing.** It costs through the per-kind families (Obj, Rel, Whose, lists), not through the Up coercions, which are 3,930 of 360,550 productions (1.1%). The toy's "3 times parse, 16 times compile" does not carry over to the real grammar.

## 4. The spike: vocabulary-independent categories with a clingo kind check

**What was built.**
- Category names were rewritten kind-free (K, T, O), and functions with identical type and lin were merged.
- Context went from 2,008 to 25 categories and from 8,929 to 1,254 functions.
- A positive, stratified `kind.lp` and a `pick.lp` (clingo 5.8.2) replay today's typing over each line's forest of trees.

**Numbers on today's spec:**

| | today | spike |
|---|---|---|
| compile | 22.7 s, 1,118 MB | 0.6 s, 78 MB |
| PGF | 13.0 MB | 0.54 MB |
| parse (median, paired) | 0.764 s | 0.0155 s (49 times faster; the skeptic got 0.570 s vs 0.0116 s, also 49 times) |
| trees per line | 1 | 1 on 301 lines, up to 125 (689 in all) |
| after the clingo check | – | exactly 1 per line; tree and logical form equal to today's on 410/410 |
| clingo check | – | median 0.027 s, sum 13.2 s (a non-stratified version: 0.55 s median, 58 s worst) |
| cold spec, one core | about 330 s | about 37 s |

- Verdicts agree on 615 lines: 73/73 construct examples, 117/117 core-4, 15/15 time-4.
- 8 kind refusals move from GF to clingo, and 21 stay in GF.
- Parse time stays nearly flat as words are added: +8% at 9 times the lexical functions.

**Where it differs from today:**
- Refusals point at a function and slot, not a token. A wrong subject is blamed on the Event function, not on the verb. 'merges the item of the batch' is blamed on the of-row.
- No wording exists for these refusals yet.

**Why it fails (skeptic, measured):**
- Ambiguity grows as 5^k with the modifiers in a line. The skeptic repeated measurement#r2's NP k times:
  - The kind-free grammar gives 5, 25, 125, 625, 3,125, 15,625 and 78,125 trees at k=1..7. Today's grammar gives 1 at every k.
  - Parse plus check at k=6 is 20.2 s against today's 3.05 s, and the parse alone at k=7 is 53.6 s.
  - The proposed tree cap (5,000) would refuse lines that today read with 1 tree.
  - The live corpus already has k=3 (125 trees).
- The pgf Python binding only enumerates trees and never exposes the packed chart, so any check after the parse pays per tree.
- A middle path (kinds kept on N, CN, St, V and Gap; NP and Arg collapsed) is 3.5 times slower than today.
- Python still makes correctness decisions in the spike: the merge map comes from regexes, `forest()` decides literal categories, and `spec_meaning.one` picks among trees.
- Per-line kind typing is grammaticality, which GF already checks declaratively. It is not the cross-line reasoning or logic operations the person's note assigns to clingo.

**Verdict:** do not adopt. The one idea that survives is better kind refusals, as a separate change to spec_refusal4.

## 5. Where each cost lies

| Cost | Whose |
|---|---|
| Per-kind object relative clause (44.5-62% of productions, about 10 times the parse) | ours: the grammar we generate |
| Per-kind subject relative clause and whose, lists | ours: grammar |
| `senses` quadratic over a shared attribute word | ours: grammar (latent) |
| Empty `t_revision_4_Val`, unreachable categories, 6 warnings | ours: grammar (hygiene) |
| ContextSteps recompiling Context from source | ours: scripts |
| Parse cache keyed by the whole grammar sha; serial parsing | ours: scripts |
| Hints re-parsing every candidate | ours: scripts (the re-parse is needed; its cost follows the grammar) |
| Subtree linearization (empty on plain, abort on optimized) | ours: scripts |
| Unused RGL fields carried by the parser | GF: unoptimized PGF; `--optimize-pgf` removes them |
| `--optimize-pgf` case-order mismatch | GF bug |
| Incomplete `complete()` | GF |
| Superlinear compile (abstract check, link) | GF (exponents disputed) |
| Mild superlinear parse growth even when factored (about N^1.26) | GF's parser together with our grammar; not profiled |
| L1-L7 single-threaded brave enumeration | ours: how spec_solve calls clingo |
| L1 depending on referent names | ours: facts plus check.lp |
| 8 flipped twins never found | ours: check.lp |
| Python translation to the logical form, 1.2 ms a line | ours: scripts, not a performance problem |

## 6. The logic operations

**What kind of reasoning each one is** (clasp statistics):
- **Tree to logical form** (spec_lf*, spec_meaning, spec_lf_facts*) is deterministic translation. It is compositional apart from one discourse pass: referent numbering and R2's binding of "the" (spec_lf_read.py:60). It takes 0.50 s for 405 lines.
- **The reading rules R1-R12** are stratified-Datalog-shaped logic, but they are implemented in Python today (spec_lf_read).
- **model.lp** (`spec check`; it is scripts/model.lp) is stratified Datalog: 0 choices, 31,621 rules, a 0.06 s solve.
- **L8 (entail.lp)** is closed-world forward chaining in one stratified model: 0 choices, 1 model, 43,461 rules, 0.51 s. It is not first-order entailment.
- **L1-L7 (check.lp)** are a bounded existential search per pair of requirements. The one choice rule (check.lp:155) builds an injective partial `map`; the merged pre-state must be consistent and the responses opposite. Brave reasoning takes the union over pairs. It is not open-ended model finding.

**Tools surveyed:**

| Tool | Guarantee | Integration | Measured |
|---|---|---|---|
| clingo (in use) | declarative; stratification can be tested (0 choices, 1 model) | pip wheel, in use | yes |
| Z3 4.15 (MIT) | SMT; unsat cores and witnesses | 28 MB wheel | L1 pos_neg/neg_pos prototype |
| cvc5 1.4.2 (BSD), egglog 13.2 (MIT) | SMT, e-graphs | wheels exist | no |
| Souffle | rejects non-stratified programs at compile time | no official wheel; no choice rules, so it cannot host L1 | no |
| ACE → DRS → FOL with RACE, Vampire or E | closest prior art: DRS accessibility is R2, DRS boxes are spec_lf's | not installed | no (design only, disputed) |
| Alloy, TLA+ | bounded model finding; suit reachability, not today's checks | Java, no wheel | no |
| Lean | proof-grade | heavy | no |

**Performance at scale.** Synthetic copies of this spec were used: 1x is 405-411 requirements, about 2x is 822, 5x is 2,055 and 12x is 4,932.
- The pairs check.lp grounds: 91, 276, 1,395 and 7,296. Ground time: 0.06, 0.14, 0.51 and 2.37 s.
- **About 800 requirements:** 276 pairs and a 0.14 s ground. This is trivial next to GF parsing.
- **About 5,000 requirements, clean:**
  - Single-threaded: 2.2-4.8 s ground and 4.3-8.2 s solve (443 models).
  - With `-t 4`: a 0.50 s solve.
- **With contradictions:**
  - 12x with 720 contradictions: 229 s single-threaded, 19.9 s at `-t 4`, 8.9 s at `-t 8`, with identical brave sets.
  - The skeptic found the 20 s LIMIT is passed much earlier: 300 contradictions at 5x take 29-39 s single-threaded, which becomes an L0 that hides the findings.
- **The synthetic copies overstate the pairing:** pairs grow 80 times for 12 times the requirements, and the clean 12x spec has 132 clashes the real one does not. L8 and model_explain were not scaled.

**Prototype numbers (Z3, L1 only):**
- It matched clingo on clean specs: 0 = 0, 20 = 20 and 132 = 132, in 0.09, 0.65 and 4.2 s at 47-93 MB.
- Getting there needed 5 more of check.lp's 41 `out` families: it first reported 15 false clashes on the real spec.
- On injected specs it still differs by 0.6-2% (281 vs 284, 1,080 vs 1,067, 2,549 vs 2,507).
- At 12x injected, Z3 takes 6.8-7.9 s at 105 MB, against clingo `-t 8` at 15.5 s and 1.5 GB.
- The speed comes from splitting the work per pair, not from SMT.
- The skeptic found Z3 misses the same 8 twins clingo misses, so a differential between them cannot catch a shared blind spot.

**Defects found in check.lp's use (confirmed):**
- **L1 depends on referent names.** check.lp:184 and :187 keep a referent with no `role/3` as a constant, so it unifies by name across lines.
  - 6 such referents sit in 5 live lines: scenarios#r3 x10, measurement#r1 x9, context-requests#r14 x6, review-guarantees#r9 x4/x6, directives#r2 x4.
  - Renaming referents leaves the real spec's findings unchanged (60 → 60), but on an injected spec 954 → 949. The lost atoms include the genuine self-contradiction `clash("scenarios#r3","scenarios#r3~neg",pos_neg)`.
  - Only disappearances were observed.
  - x10 is the image under `each` x9, so a plain role would change the meaning.
- **8 of 300 flipped twins are found by neither clingo nor Z3** (consistency#r18, r23, r24, r25 and r30 copies, each returning the constant `L1`). Each pair is cand, pair, coded and fit, but has no `cl`. This is unexplained.
- **The printed witness depends on the thread count.** At 1x with 60 injected twins, `-t 1` and `-t 4` give 149 pre-state atoms and `-t 8` gives 147. Parallel witness solves would make `spec logic` output machine-dependent.
- **The heuristic's claimed 3.5-4.2 times is refuted.** It came from an added `#show cl/3`. With spec_solve's real `#show` set: 1,005 models in 29.0-31.5 s against 29.1-29.4 s.

**Where each operation should live:**
- **L1-L7:** in clingo (check.lp). Do not port to Z3. Fix the name hole and the missed twins.
- **L8 and model.lp:** in clingo, with a test that asserts 0 choices and 1 model.
- **Reading rules:** clingo is a natural home under the person's note. The migration is large, not medium: R2 is called mid-translation and makes image referents (spec_lf_read.py:55-60), so a two-phase rewrite of spec_lf_clause and spec_lf_np would be needed. Cost is unmeasured. A study, not a next step.
- **Tree to logical form:** Python today.
  - A generated GF concrete syntax could carry the compositional part.
  - GF's `pg -missing` already checks totality. Failing on any warning would refuse today's grammar because of the mkQuant/mkAdN warnings.
  - Pairs, numbers and orders would stay in a post-pass. Compile cost unmeasured.
- **Kind typing of a single line:** in GF. It is grammar. Moving it costs exponential trees (section 4).
- **A "small trusted witness checker":** refuted. It would re-decide all 41 `out` families: a second encoding, and in Python.

## 7. Options

**A. Factor the relative clauses** (Obj first, then Rel and Whose) the way RelCN does.
- **Where correctness lives:** the GF grammar.
- **Measured:**
  - Parse 1.02 → 0.08-0.12 s a line, about 10-14 times.
  - Compile about 20 → 6-6.7 s; RSS 1.1 GB → about 360 MB; PGF 12.8 → 5.1-5.4 MB.
  - Slope per added kind 2.5 → 0.12 ms.
  - Same trees up to a bijective renaming on 402-405 lines.
  - 321/321 perturbations agree, though only 24 of them parse.
- **Risk: low for the language, wide for the code.**
  - The Python readers that match function names must follow: spec_lf_np.py:249-259 and model_constructs_table.py:84-98, including the negated-RC pattern at :98, which must match PNeg after the new fun.
  - So must the Python that writes these trees: spec_lf_number.py:143-148, spec_steps4_boxes.py:90, spec_steps4_held.py:47, features_vocab4.py:80/104 and spec_one_thing.py:35.
  - model_constructs' `uncovered` check needs the new functions covered by patterns. grammar/constructs.md's Functions regexes and every consumer's catalogue change.
  - Whose needs one function per (attribute, base kind).
  - Run the refused corpus and the hints on the factored grammar before adopting.

**B. `--optimize-pgf` on Context only, with a re-sort of the sequence table at build time.**
- **Where correctness lives:** GF. The re-sort is a Python build step over the PGF 2.1 format. It decides no meaning.
- **Measured:** 24-31 times on the whole-line parse; 0 differences on 413 live and 105 mutated lines.
- **Before it can ship:**
  - Every subtree linearization (`spec_grammar4._words`, `spec_one_thing.refusal`) must take its words from `bracketedLinearize` of the whole tree.
  - Add a guard: check the PGF version; the re-sort must be the identity on an unoptimized PGF; the sequences must be in case-sensitive order. Linearize one subtree of every reachable category in a forked child.
  - Never optimize ContextSteps until features_vocab4's 8 sites move the same way (186 aborts today).
  - Include the option in the cache sha.
  - Report the bug to gf-core (the one-line fix: `/= Just (LStr "off")`) and drop the re-sort once a fixed release is pinned.
- **Risk:**
  - Coupling to the binary format.
  - An abort is a process kill.
  - Not yet run on the other contexts or at other sizes.

**C. Reuse Context's compiled modules for ContextSteps.**
- **Where correctness lives:** unchanged; the PGF is byte-identical.
- **Measured:** about 8.5-10.6 → 2.6-2.8 s a step-grammar compile.
- **Risk:** none to the language. Do it under a lock, given spec_gf.compile's rename race.

**D. Guards on the generator.**
- Count the functions whose arguments are VPSlash, ClSlash or RS against the number of kinds, on the generated Context.gf text, with no compile.
- Add a parse-time budget on a fixed line set.
- **Where correctness lives:** a Python measurement only.
- **Risk:** none.

**E. clingo `-t N` on spec_solve's brave solve only.**
- Cap it with an environment variable, with a default of 1 in tests. Keep the witness solve at `-t 1` or make it canonical.
- **Where correctness lives:** clingo.
- **Measured:** 15 times at 5x with contradictions, 29.4 → 1.95 s, with an identical set. No gain at today's size (0.1 s).
- **Risk:** CPU oversubscription under 32 test workers (unmeasured).

**F. Fix check.lp's referent-name dependence and explain the 8 missed twins.**
- Give each role-less referent an each-aware kind, or report it as `unread` for its requirement, not as L0.
- Add metamorphic tests: alpha-renaming, flipped twins and fact order (brave set only). Add the Datalog guarantee tests for entail.lp and model.lp.
- **Where correctness lives:** clingo, with Python for the facts.
- **Risk:** low, but the fix touches spec_findings, spec_entail_rules and spec_solve_pairs if the term shape changes.

**G. Not recommended:**
- The kind-free grammar with a clingo kind check: exponential ambiguity.
- Factoring lists over `K_NP0`: refuted by 65 lines.
- A word-level `senses` fix as written: it reads a same-entry comparison two ways. Remove the per-entry funs first, then measure.
- `--case_sensitive=off`; the heuristic search factor; a domain heuristic in check.lp.
- Porting L1-L7 to Z3; a Python witness checker.
- Pruning functions by usage: that shrinks the language.
- A module chain for the compile alone: -14% to -24%, RSS +13%, and no reuse in a fresh mkdtemp.

**Recommendation:** in order, A, then C, then B (Context only, after its preconditions), then D, F and E.
- A and C keep correctness in the GF grammar, which the person prefers, and remove the largest cost.
- B gains about as much again but needs the linearization fix first.
- Cross-line logic stays in clingo, where it is declarative.
- No option moves checking into Python.
- Whether A and B combine multiplicatively is not measured, so expect at least A's factor and do not assume the product.

## 8. Open questions

- Does the factored grammar still need `--optimize-pgf`, and do their gains combine? Measure the parse of an optimized factored PGF on the 413 lines.
- How do optimized PGFs scale at 2,000-2,800 categories and in synthetic series? The speed-up is measured at one vocabulary size.
- Even factored, parse grows about N^1.26. Does GF's C parser have a prediction filter that our grammar defeats? It needs profiling.
- Which part of GF's link and PGF write grows so fast (3.6 → 41 s, 200 → 500 kinds)? It sets the compile ceiling at 1,000 kinds (about 480 s even factored).
- Is ContextSteps' cost dominated by the same Obj family? It was not compiled or timed factored.
- How does the real vocabulary grow with lines, and how dense will broad frames (over thing, file and text) become?
- Why do the 8 flipped twins that return a constant escape check.lp's `cl`?
- Should the 6 role-less referents get a kind from their row's image under `each`, or be refused by a reading rule?
- Does `-t N` hold up under the parallel test suite? It is unmeasured.
- Is an incomplete hint from `complete()` acceptable, given that the re-parse already filters it and it costs a parse per candidate?
- Should text attributes such as `revision` get a setter that takes a code? That is a language decision.
- The tools not installed here (ACE/RACE, Vampire, Alloy) were not measured. Is a reachability check over sequences of requests wanted, which is where Alloy or TLA+ would fit?
