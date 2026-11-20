---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-20-where-the-readiness-bar-s-time-goes-and-what-would-remove-it
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-20
---

# Where the readiness bar's time goes, and what would remove it

Research on b430, "The readiness bar answers in seconds". The bar was measured on item b418 (11 lines, 6 retirements). Its lay changes spec/model and spec/vocabulary, so it changes grammar 4's sha (8265d0a7… before the lay, a51a033d… after). Four investigations ran: the stat calls, the parse cache, the bar's structure and the grammar compiles. A skeptic re-checked each one. Every number below comes from those runs. Other agents were loading the machine during the runs (load average 1-35), so the seconds are approximate. Paired runs were used, and outliers were dropped.

## 1. The measured picture

### Warm: the stat calls first

- `work ready` takes 7.4-8.1 s warm on current main when nothing profiles it. The record's 15 s was measured under cProfile, which roughly doubles the time.
- One warm bar run makes 1,383,845 syscalls:
  - 1,081,509 `newfstatat` (80%);
  - 77,652 `getdents64`;
  - 49,946 `openat`;
  - 60,790 `fstat`.
- About 1.0 M of the stats come from `spec_grammar4._state` (spec_grammar4.py:78-81). It runs on every `_context` call to check that the in-process grammar is still current.
- `_context` is called 5,403 times per run. `spec_rgl_vocab.read` recomputed only 2 times, before the lay and after it.
- Each check stats 185 files and walks spec/: 5,403 × 185 = 999,555 `posix.stat`, which matches cProfile's count exactly.
- The grammar reads only 22 of those files. Hooking `open` during a cold `_context` showed which:
  - spec/index.md;
  - spec/model/*.md (6);
  - spec/vocabulary/*.md (7);
  - the two imported packs;
  - the 4 base .gf files.

`newfstatat` by path in one warm run:

| Path under the bar's copy | stats | share |
|---|---|---|
| spec/decisions/* (111 files, never read by the grammar) | 600,621 | 56% |
| spec/capabilities/* (51 files, not read in a context with spec/model/) | 276,908 | 26% |
| spec/vocabulary/* | 37,878 | 3.5% |
| spec/model/* | 37,693 | 3.5% |
| path components of the copy and /tmp (`Path.resolve`, twice per `_context`) | 35,179 | 3.3% |
| grammar/packs/* | 21,638 | 2% |
| each base .gf | 5,408 each | |

Cost:
- `_state` costs 388-500 µs a call: 2.1-2.7 s per run in isolation, and 2.25 s measured inside a bar run.
- The `os.walk` alone takes 0.71 s.
- Smaller touches on the same path add up to under 0.2 s per run:
  - `rgl_path()` reopens the RGL's release file 5,402 times (0.08 s);
  - 10,806 calls to `Path.resolve` take 0.077 s.

Why `_context` is called so often:
- It is called per line read. `spec_language.parse` calls `spec_grammar4.parse` and then `load`, which fetches the context a second time. `model_domain.domain_line` also parses and then calls `load`.
- Each line is parsed 6 times per run:
  - Model.read before the lay: 2;
  - Model.read after the lay: 2;
  - `annotate`: 1;
  - `spec_context`: 1.
- That gives 2,452 parse calls for about 815 distinct line-states (405 before the lay, 410 after), and about 4,000 `spec_lf.form` calls.

### Warm: by stage (unprofiled)

| Stage | seconds |
|---|---|
| `_violations` before the lay | 2.40 |
| `annotate` | 0.77-1.16 |
| `_parses` of the item | 0.02 |
| `_logic` (entail included) | 1.25 |
| `_violations` after the lay | 2.15 |
| `_scenarios` | 0.72 |
| copytree, lay, lexicon | about 0.1 |
| total | 7.5-8.0 |

Fixed costs per state, warm:

| Cost | seconds |
|---|---|
| `_context` rebuild | 0.12 |
| `readPGF` | 0.20-0.30 |
| step grammar load | 0.21 |
| `spec_lexicon.read` (20 calls per run, each 30 ms) | 0.6 in total |

A warm parse-cache hit costs 6.0 ms per line, of which 3.0 ms is `_state`.

### Cold

The record measured 730 s with an empty cache. Its largest parts:
- 604 s of `Concr.parse` for 817 calls (83%);
- 3 compiles, 58.6 s in total.

What these investigations re-measured:
- **Compile.** A full Context compile takes 19.4-20.5 s at load 10-15, uses 1.09 GB RSS, and takes 33.8 s at load 34. Staged:
  - ContextEng's evaluation: 16.41 s;
  - PGF link and write: 4.31 s;
  - everything else: under 1 s.
- **Parse.**
  - A GF parse takes 0.74-1.08 s per line serially.
  - 95% of that time passes before the first tree.
  - Every one of the 405 lines has exactly 1 tree.
  - Parse time is about linear in the number of categories: 1.0 s a line at 2,000 cats, 1.4 s at 2,800.
- **Compiles in one bar run with an empty PGF cache.** There are three:
  1. Context before the lay: this is main's sha, because the key holds no path. 21.15 s.
  2. Context after the lay: 20.6-24.7 s. Its first reader is `annotate`.
  3. ContextSteps: 21.2-30.6 s.
- **Main's grammar cached:** 2 compiles, and the bar took 49.8 s. That run's parse cache was already filled for the after-lay sha, so it does not show a real first run.
- **Lay-cold** (main's parses cached, the after-lay sha's parse cache empty): 454.5 s. `annotate` was charged 445.65 s of that, because as the first reader after the lay it pays all 410 parses serially.

## 2. Causes, ranked by seconds

| # | Cause | Cold | Warm |
|---|---|---|---|
| 1 | The parse cache key is the whole grammar's sha, so any vocabulary change misses every line. "widget" missed 405 of 405 lines and changed none of their parses. | 370-450 s per vocabulary-changing lay; 604 s in the record | 0 |
| 2 | Misses are parsed serially on one core. | about 340 s of that cost | 0 |
| 3 | Each line is parsed 6 times and given a logical form about 5 times per run. | 0 extra | 2.6-2.8 s |
| 4 | `_state` stats 185 files on each of 5,403 calls, and finds a change twice. | 2.3 s | 2.25-2.6 s |
| 5 | Compiles run serially on the critical path. ContextSteps recompiles all of Context from source. | 20 s per new sha, plus about 15 s redundant | 0 |
| 6 | The before-lay state (main's spec) is recomputed on every run. | 0 extra | 2.40 s; about 0.35-0.5 s after #3 and #4 are fixed |
| 7 | `annotate` re-parses the whole spec only to silence v_a5 and v_a6. | where the lay-cold parse lands | 0.8-1.2 s |
| 8 | L8 (entailment) is computed and then discarded. | 0.35-0.4 s | 0.35-0.4 s |
| 9 | `spec_lexicon.read` has no cache: 20 calls per run. | 0.3 s | 0.3 s |
| 10 | Fun names are positional, so cached trees are invalid in any new grammar, and reordering two entries changes the sha. | blocks reuse | 0 |

## 3. Proposals

### Survived verification

**A. Stat once per state of the bar's copy** (stat-2, bar-structure-1, parse-cache-6)
- **Change.**
  - Add a scoped snapshot, `with spec_grammar4.held(root):`. Inside it, `_context` computes `_state` once and reuses it.
  - `lay_onto` and `unlay` call `invalidate(Path(root).resolve())` themselves.
  - `well_formed` opens one block before the lay and one after it.
  - `spec_lexicon.read` is memoised under the same snapshot.
  - Outside a block, nothing changes.
- **Files.** spec_grammar4.py, readiness_bar.py, backlog_lines.py, spec_lexicon.py.
- **Saving.** Warm 7.97 → 5.39 s, re-measured. `newfstatat` drops from 1.08 M to 50 K and `getdents64` from 77 K to 2 K. The lexicon memo saved about 0.3 s more in one run.
- **Soundness.**
  - The copy is a private mkdtemp, written only by copytree and `lay_onto`, and `lay_onto` does every writer's work.
  - `annotate` writes cli.toml and `features generate` writes features/. Neither is an input of the state.
  - This is stricter than today's (mtime, size) check: copytree keeps the old mtimes, and a same-size rewrite within one tick goes unseen today.
  - The block must clear on exit.
- **Skeptic's correction.** A global memo is unsound:
  - test_spec_grammar4_cache writes packs/cli.md in place;
  - scenario worlds and `batch_start` write spec files outside `lay_onto`;
  - a memo with no invalidation ran past 6 minutes on the stale grammar.

**B. Fetch the context once per parse** (stat-3)
- **Change.**
  - `parse` returns the vocab it used, so `spec_language` and `domain_line` stop calling `load`.
  - The root is resolved once per `_context` call.
  - `rgl_path()` is cached per process, keyed on its environment.
- **Files.** spec_grammar4.py, spec_language.py, model_domain.py, tools_grammar.py.
- **Saving.** About 1.0-1.1 s without A. With A, 0.12-0.16 s, re-measured; the claimed 0.2-0.3 s was too high.
- **Soundness.** It is more consistent than today. The sha uses the constant `RGL_RELEASE`.

**C. Stat only the grammar's inputs** (stat-1)
- **Change.**
  - Stat only index.md, model/*.md, vocabulary/*.md, spec/packs/*.md (even while that folder is absent), the plugin packs and the base .gf files.
  - Stat capabilities/*.md as well, but only when there is no spec/model/.
  - Take the list from one `inputs(root)` function beside the reader, with a test that hooks `open`.
- **Files.** spec_grammar4.py, spec_lexicon.py or spec_rgl_vocab.py, a test.
- **Saving.** Warm 7.97 → 6.14 s alone. About 0 inside A. It matters for `spec check`, `spec parse`, `features generate` and `batch_start`.
- **Soundness.** The skeptic traced every reader under `spec_rgl_vocab.read`; decisions are never inputs.
- **Skeptic's correction.** Add whether spec/model is a directory to the state. The readers switch on it, and `migrate init` makes an empty one. This is a blind spot today as well.

**D. One parse and one form per line per state, with a sound key** (bar-structure-2, corrected)
- **Change.** Inside A's block:
  - memoise `spec_language.parse` by (snapshot, text);
  - memoise forms by (that state's vocab object, tree);
  - or memoise only the pre-guard trees by the disk key and re-run the guards.
- **Files.** spec_grammar4.py, spec_language.py, spec_lf.py, model_spec.py, model_domain.py.
- **Saving.** 7.83 → 5.04 s alone; 3.82 s together with A.
- **Skeptic's correction.** The proposed key, (sha, words, text), is unsound:
  - The guards read vocab content and `<root>/grammar/constructs.md`, and neither is in the sha.
  - Measured counterexample: changing `merged` from adjective to noun leaves the sha at 8265d0a7…, yet measurement#r1 goes from a tree to a refusal. The memo would give a wrong pass.
  - `id(vocab)` is unsafe after `_contexts.clear()`.

**E. Drop `annotate` from the bar, and exclude v_a5 and v_a6** (bar-structure-4)
- **Change.** Remove the `annotate` call from `well_formed`, and add v_a5 and v_a6 to the codes the bar does not compare.
- **Files.** readiness_bar.py.
- **Saving.** 0.8-1.2 s warm today, less after D. In the lay-cold case the 445 s moves to the next reader, and F removes it.
- **Soundness.** model.lp reads `contract_op` and `op_holds` only in v_a5 and v_a6. On b418 the violation sets differ only in those two codes.
- **Side effect** (read from the code, not run). `annotate` parses every line before the r15 lexicon check, so a compile-breaking lexicon may raise an error instead of being named. Dropping `annotate` removes that.

**F. Parallel prefetch of the parse misses** (parse-cache-1, bar-structure-6)
- **Change.**
  - After the lay and after the lexicon check, collect the state's distinct texts.
  - Compute each key exactly as `spec_language` tokenises.
  - Parse the misses in a pool sized by the number of misses, by the cores and by memory.
  - Fall back to serial if the pool fails.
- **Files.** a new spec_prefetch.py, readiness_bar.py, and the whole-spec readers.
- **Saving.**
  - Lay-cold 454.5 s → 33.7 s, measured under load.
  - Idle machine: 402 lines take 28.2 s at 32 workers, 33.7 s at 16, and about 318 s serially.
  - 0 s warm.
- **Soundness.** It runs the same function on the same PGF with the same key. Entries are written with mkstemp + `os.replace`.
- **Skeptic's corrections.**
  - The machine has 16 cores with SMT; each parse takes 1.75 s at 32 workers, so "10-15 s idle" is about 2× too low.
  - clingo has already run when the pool starts. Use forkserver or spawn (0.2-1.2 s of PGF load per worker).
  - Refused lines keep a serial tail of `disagreeing` and `hint` re-parses.
  - Run the pool after the lexicon check.
  - Worker RSS was not measured.
  - The pool competes with a concurrent `pytest -n`.

**G. Reuse Context's .gfo files for the step grammar** (compile-1)
- **Change.**
  - Seed the steps folder with copies of the six Context .gfo files from `cache()/<context sha>/` (copies, not hard links).
  - Set every .gfo's mtime later than every .gf's.
  - Fall back to a full compile if any of the six is missing.
- **Files.** spec_gf.py, spec_rgl_steps.py.
- **Saving.** 37.7 → 9.1 s at load 34; about 21 → 6 s staged at normal load. That is about 15 s off the first run after a vocabulary change.
- **Soundness.**
  - The step sources hold Context's sources byte for byte, and the folder is keyed by their sha.
  - The skeptic reproduced a byte-identical PGF (sha256 b44d5cf7…).
  - GF's make check still guards.
  - The GF version is in neither key; add `gf --version` to both.

**H. No entailment in the bar** (bar-structure-5)
- **Change.** `spec_solve.run(copy, entail=False)`, and l2 skipped.
- **Saving.** 0.35-0.4 s.
- **Soundness.** Entail emits only L8 (spec_entail.py:162), which the bar never reads. L0, L1 and L3 are identical, and entail mutates nothing.

**I. Cache the before-lay result on disk** (bar-structure-3)
- **Change.** Key the stored result by a hash of the copy's spec/ (after `others`), the plugin's scripts, .lp, .gf and packs, the RGL release and the pgf version. Guard with an `open`-audit test.
- **Saving.** 2.40 → 0 s alone. After A and D, only about 0.35-0.5 s (not measured), with no cold gain beyond today's disk parse cache.
- **Gaps.** The key leaves out clingo's version, GF's version, `$SHOPSYSTEM_GF_RGL_SRC`, and a cli.toml program outside the root.

**J. Keep the grammar key free of the path** (stat-4)
- **Change.** Add a test that sha(repo) equals sha(copy).
- **Saving.** None today. It prevents a regression to a cold bar on every run.

**K. Content-derived, stable fun names** (parse-cache-2)
- **Change.**
  - Name each generated fun by what it encodes, not by its position.
  - Assert uniqueness at generation time.
  - Emit the source in sorted order.
  - Move every regex reader with the names: spec_lf_ids, spec_steps4*, spec_lf_ordered, spec_lf_member, spec_rgl_ops, features_vocab4.py:56-57, test_spec_rgl_np.
- **Saving.** 0 s alone. It is the prerequisite for reuse across grammars.
- **Evidence.** b418 changed the tree text of 200/399 lines and b420 of 339/402. In both, 0 differ in logical form.
- **Skeptic's correction.** The tie-break in `spec_meaning.one` depends on the spelling of names, so check that no line keeps a different tree. Rest the evidence on the logical-form comparison, not on masked digits.

**L. The literal callback keyed by the line's own words** (parse-cache-5)
- **Change.** Key on the vocabulary words that are also the line's tokens, not the whole word set.
- **Soundness.** Exact, because `literal` only tests the line's own tokens. A narrow key needs it.

### Refuted, or not worth doing

- **parse-cache-3, a hand-written vocabulary slice as the key.**
  - Recall was never tested: 0 lines changed in all three experiments.
  - A miss gives a silent wrong pass, and global constructs are not audited.
  - The backstop runs only after `work ready`.
  - Sounder variant: derive each line's dependencies from the generator.
- **parse-cache-4, a lazy PGF load.** The item's own lines always miss, and ContextSteps compiles regardless. It saves about 0 s in the bar.
- **parse-cache-7, a pruned grammar per line.** Not measured, and harder to make sound than the slice.
- **compile-2, background compiles.**
  - Only about 5 s of overlap holds in the realistic case.
  - A warm-up at `work line` would compile every intermediate sha (1.1 GB each).
  - The parse misses remain.
- **compile-3, an incrementally compiled, split Context.**
  - Not prototyped.
  - Renaming changes which tree is kept and which survive LIMIT=50.
  - The sequential split takes 23.1 s.
- **bar-structure-7, the composition as first stated.** It has D's unsound key and runs the prefetch before the lexicon check.
- **bar-structure-8, per-capability fact caching.** Its sha leaves out vocabulary content, and it saves at most 0.3 s.
- **Rejected by measurement:**
  - `--optimize-pgf`: 4 of 12 lines differed.
  - RTS heap tuning: every setting was slower.
  - A split without stable names: no gain.
  - Persisting only the Base/Time .gfo files: 0.13 s.
  - Parsing with the ContextSteps PGF: step phrasings would parse as requirements.

## 4. Recommended order

Seconds are b418, unprofiled. Lay-cold means the first run after a vocabulary change, with main's grammar and parses cached.

| Step | Proposals | Warm | Lay-cold | Empty cache |
|---|---|---|---|---|
| today | | 7.5-8.0 s | 454.5 s | 730 s (record) |
| 1 | A + B (C for callers outside the bar) | 5.4 s | about 450 s | about 725 s |
| 2 | D with a per-state key, plus the lexicon memo | 3.8 s | unchanged | unchanged |
| 3 | E + H + I | 1.9 s (measured floor, result unchanged) | unchanged | unchanged |
| 4 | F (after the lexicon check, forkserver) | 1.9 s | about 50 s (19.5 + 28 + 2) | about 95-100 s |
| 5 | G, and the after-lay compile overlapped with the before-lay stage | 1.9 s | about 35-45 s (estimate) | about 80 s (estimate) |
| 6 | K + L, then a generator-derived narrow key with a differential full re-parse at batch review | 1.9 s | about one compile (about 20 s) plus the dirty lines (b418: 17 lines, 3.2 s in parallel); not measured end to end | unchanged |

- Steps 1-3 are low-risk and reach "a few seconds warm".
- Step 4 is the only large, sound cold gain available now.
- "Cold bounded by one compile" needs step 6. It is high-risk, and the step grammar's parse cache has the same full-miss problem, which step 6 must also cover.

## 5. Open questions for the person

1. Should the target be stated against unprofiled wall time (7.5-8.0 s today, not 15 s)?
2. Must the bar still prove that `annotate` succeeds (b379), or may it exclude v_a5 and v_a6?
3. May `work ready` take 16-32 processes and about 6 GB of memory on a cold run, while a batch's `pytest -n` may be running on the same machine?
4. Is a narrow parse key acceptable at all? If so, may its differential re-parse (about 320 s serial, about 30 s in parallel) run at batch review rather than at `work ready`?
5. Should `--optimize-pgf`'s lost parses be investigated? It parsed 37 times faster on the sample.
6. Two existing gaps were found, outside b430's scope:
   - the copy has no grammar/constructs.md, so parsing#r6 never refuses in the bar;
   - the copy has no scripts/, so v_a3 fires both before and after the lay.

   Should each become an item?
7. Should cache eviction become an item? The cache holds 1.1 GB of PGFs and 361 MB of parses with no eviction.
8. Should the numbers be re-measured on an idle machine before the item is shaped?
