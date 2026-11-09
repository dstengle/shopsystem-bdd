# Study: Datalog for `model logic` — Soufflé for the index, and for the whole check

(Saved by the session from the study agent's reply; its own write of this file was refused.)

Study folder: `scratchpad/b112/scale/datalog/`. The repository was not changed. Timings single-threaded unless a `-j` is
given, on a 32-core machine while other studies ran.

## Summary

- **The index in Soufflé works and is fast.** check.lp's lines 14-61, plus self-clash, L3, L4 and L5, ported to
  Soufflé 2.5 (`idx2.dl`, 147 lines). Exactly clingo's pairs and findings in every mode, k=1 to 160. 0.22 s at k=20,
  where clingo grounding today's check takes 33.5 s. The same rules run in clingo still take 18 s at k=20 and 111 s at
  k=40: most of the gain is the engine, not the rewrite.
- **The whole check in Soufflé is exact.** `full2.dl` (378 lines) lists every unification of each candidate pair as a
  tuple. Its shown atoms matched clingo's on every spec tested: the unmutated specs in all three modes wherever clingo
  finished (up to k=40 mixed), and 80 mutated specs carrying about 2,200 L1 pair clashes, 1,000 self clashes, 1,800 L6,
  130 L3, 150 L4 and 370 L5. Defined conditions, L6's prose dependence and `every` are all stratified within one
  unification, so nothing in them needs a guess.
- **Speed of the full check.** k=40 mixed (10,405 lines): 4.8 s single-threaded, 1.6 s with `-j16`; today's check
  takes 230 s and 13.8 GB. k=80 (20,805 lines): 18 s single-threaded, 5 s with `-j16`, 2.8 GB.
- **Witnesses.** clingo's witness was among Soufflé's listed witnesses in 125 of 125 cases, and the same as Soufflé's
  pick in 123. Only the wording of a report could differ, never a finding.
- **Where it breaks.** Unifications per pair grow exponentially with same-kind roles. Today's worst pair has 224; two
  9-role lines of one kind would have 17.6 M per pair. Needs a role-count limit with a clingo fallback.
- **The hybrid** (Soufflé's pairs fed to clingo) is also exact and about 13x faster than today at k=40, but still
  113 s and 8 GB at k=80: clingo's cost per pair keeps growing.
- **Growth on this data.** No variant grows linearly here: gen.py shares event triggers such as `e_write` across
  copies, so the candidate pairs themselves grow faster than the lines.
- **Other engines.** Nemo 0.10.1 installed and measured: same pairs, about half Soufflé's speed, binaries for every
  OS. DDlog is archived (2023). Nothing practical does incremental evaluation of a program like this.
- **Recommendation:** the Soufflé interpreter for the whole check, with the role-count limit; the hybrid as a first
  step if two encodings of the check are unwanted. Install: the 18.5 MB release deb on Linux x86_64, Homebrew on macOS;
  no Windows build, no PyPI wheel. Compiled mode not worth it (needs g++ and dev libraries; the interpreter with `-j`
  is within 25%).

## 1. Installing Soufflé

- `gh release download 2.5 -R souffle-lang/souffle -p x86_64-ubuntu-2404-souffle-2.5-Linux.deb` (SHA-512 matched),
  `dpkg-deb -x` into `datalog/souffle/`; run as `souffle/usr/bin/souffle --no-preprocessor` (mcpp not installed; these
  programs need no preprocessor).
- One 18.5 MB binary; needs libffi8, libgomp, libncurses6, libsqlite3, zlib, libstdc++, and glibc >= 2.38 for the 24.04
  deb.
- Compiled mode (`-o`): `CPATH=souffle/usr/include`, g++, sqlite3/zlib/ncurses dev libraries; compile 18 s (`idx2`),
  37 s (`full2`) at -O3; binaries 1.8 / 3.6 MB; a binary runs in parallel only when generated with `-j auto`.
- For plugin users via `tools install`: Linux x86_64 extract the release deb (releases only for Ubuntu 22.04/24.04 and
  Fedora/Oracle, x86_64); macOS Homebrew bottles (arm64, x86_64); Windows none; no PyPI wheel.
- Terms: every term a Soufflé `symbol` holding its clingo text (strings keep their quotes, `tofacts.py`). Soufflé 2.5
  compares symbols lexicographically, so `A < B` and `Y0 < Y` order as in clingo, keeping pair orientation and the
  `pos_neg`/`neg_pos` labels. Function terms are split (`rnone`'s `kind(K)` -> `rnone_k1`/`rnone_k2`; `set(T,V)`/
  `hold(S)` events -> `stative_in`); `b(Y0)` built by string concatenation.

## 2. The deterministic part: the index

- `index.dl`, a straight port: identical, still quadratic (1.36 s at k=10).
- `idx2.dl` adds a `pre(A,B)` filter like `check_spike.lp` (pairs sharing a trigger `tp`, an untriggered side's kind,
  a universal's vocabulary, a use against a "shall not use"); every `cc` rule limited to `pre`, `kin`/`doerk` to `tp`.
  Exact, because each `cand` body already implies `pre`.

Pairs identical to clingo's in every row:

| mode | k | lines | pairs | clingo today (ground+solve, RSS) | Soufflé idx2 interpreted | idx2 compiled | Nemo |
|---|---|---|---|---|---|---|---|
| own | 20 | 5,205 | 2,616 | 33.5+0.4 s, 3.5 GB | 0.22 s | 0.16 s | 0.45 s |
| own | 40 | 10,405 | 7,226 | - | 0.62 s | 0.39 s | 1.30 s |
| own | 80 | 20,805 | 22,446 | - | 2.13 s | 1.51 s | 4.45 s |
| own | 160 | 41,605 | 76,886 | - | 8.08 s | 7.57 s | - |
| mixed | 40 | 10,405 | 11,186 | 218.4+11.9 s, 13.8 GB | 0.87 s | 0.61 s | 1.88 s |
| mixed | 80 | 20,805 | 30,366 | - | 3.59 s | 1.99 s | 5.49 s |
| shared | 40 | 10,405 | 58,706 | - | 4.53 s | 3.35 s | - |

- idx2 memory 30-220 MB; interpreter with `-j16` about 0.5 s at k=80; writing facts as TSV in Python 0.5 s at k=20,
  3.7 s at k=80.
- The same filter in clingo (`idx2.lp`): identical pairs, grounds in 18 s at k=20 and 111 s at k=40 (own); mixed 14.5 s
  and 89.8 s. clingo's grounder does 100-200x more work than Soufflé on the same rules.
- Not linear because `tp` grows 68 k / 199 k / 651 k at own k=20/40/80: shared event triggers make 19,800 of the 22,446
  pairs at own k=80 cross-copy pairs. Soufflé's time follows its output size.

## 3. The search part in Datalog

### Encoding

- check.lp guesses `map(A,B,Y,X)`, a partial injective map from B's roles to A's roles of a compatible kind. In Datalog
  the unifications are listed by recursion over B's roles in order: `M` packs 4 bits per role of B (0 unmapped, or 1 +
  the index of A's role); a bitmask of A's roles taken enforces injectivity (constraint 69); constraints 70 and 72 are
  local to one choice and filter options; constraint 71 (a code named on both sides) forces that choice and reserves
  its X.
- Every relation from check.lp line 74 on carries the record `I = [A,B,M]`;
  `clash(A,B,W) :- cl(I,W), un(I,A,B), !depends(I).` and `maybe(A,B,W,C) :- cl(I,W), un(I,A,B), dep(I,C).`
- Exact because different pairs share no choice in check.lp, so a brave consequence of check.lp means exactly that some
  unification of that pair yields it.
- One difference: global UNSAT. clingo returns nothing if one pair has no admissible unification (a forced map clashes
  in kind or `oattr`); Datalog reports the other pairs and flags `stuck(A,B)`. `stuck` was empty on every run.
- `full2` adds a demand filter: derive `clc` (`cl` without `ok`) first, then states, `out` and the prose dependence only
  for those unifications (11% of them at k=10 mixed): half the time. Matched `full` on every bench row and the fuzz.

### Correctness evidence

- Unmutated specs: SAME at k=1, 4, 10 in all three modes, and on every bench run where clingo finished (own up to 20,
  mixed up to 40, shared up to 10).
- Mutated specs (`fuzz.py`, `fuzz2.py`), 80: 40 own k=1, 20 mixed k=2, 20 shared k=1. Mutations: `resp` polarity
  flipped (sometimes both ways: a self-clash); a `cond` dropped, flipped or revalued (including an unreachable
  `v_nowhere`); a `set` revalued; a `ccond`/`crel` flipped or dropped; a role's kind swapped (not on named roles);
  triggers merged; `dlit`/`ucond`/`uccond` flipped; `none`/`initial` dropped. All 80 identical for `full.dl` and
  `full2.dl`.
- Defined-condition rules exercised: `ask`/`ent`/`refuted`/`umatch` hold 432/288/72/504 tuples at mixed k=10.
- Witnesses (`cmp_witness.py`, 6 mutated specs): clingo's focused witness equals the pre-state of one of Soufflé's
  hitting unifications in 125 of 125; the least `M` gives clingo's witness in 123. Datalog's choice is deterministic.

### Size of the enumeration

- Totals: own 12.8 k unifications at k=10, 200 k at k=40, 3.18 M at k=160; mixed 820 k at k=80.
- Worst pair: 224 (`pr-review#r3`, 7 roles, two of kind `k_commit`, paired with its copy on the shared event
  `e_write`).
- Bound for n mutually compatible roles each side, sum_k C(n,k)^2 k!: n=5 1,546; 6 13,327; 7 130,922; 8 1.44 M;
  9 17.6 M; 10 235 M. clingo never lists this space. **This is where Datalog breaks.** Mitigation (not built): count a
  pair's unifications before materialising them; pairs above a limit go to clingo.

### Full-check timings (seconds; RSS where noted)

| mode | k | today (clingo) | hybrid | full2 interpreted | full2 compiled | full2 interp. `-j16` | full2 compiled (`-j auto`) `-j16` |
|---|---|---|---|---|---|---|---|
| own | 20 | 33.5+0.4, 3.5 GB | 1.6+0.3, 0.34 GB | 1.16 | 0.88 | 0.55 | - |
| own | 40 | - | 6.1+2.4, 1.2 GB | 4.35, 0.7 GB | 3.41 | 1.50 | - |
| own | 80 | - | 56.8+20.2, 7.8 GB | 17.3, 2.7 GB | 13.8 | 5.08 | 4.14 |
| mixed | 20 | 38.3+1.1, 3.5 GB | 2.0+0.9, 0.41 GB | 1.37 | 1.05 | 0.57 | - |
| mixed | 40 | 218.4+11.9, 13.8 GB | 6.9+9.4, 1.3 GB | 4.80, 0.7 GB | 3.77 | 1.58 | - |
| mixed | 80 | - | 57.5+55.5, 8.0 GB | 18.0, 2.8 GB | 14.3 | 5.08 | 4.34 |

- Unfiltered `full` at own k=160: 149 s interpreted, 114 s compiled, 16.6-21.9 GB.
- The hybrid's clingo part grows faster than its pairs: own k=40 to 80, pairs x3.1, grounding x9.

## 4. Threads and compiled mode

Compiled is 1.2-1.6x faster than interpreted single-threaded; a binary generated without `-j` ignores `-j`. `full2`
generated with `-j auto`, own k=80: 13.5 s at `-j1`, 5.5 s at `-j4`, 4.1 s at `-j16`, identical findings. The
interpreter scales about as well (17.3, 7.6, 5.1 s): the interpreter is enough.

## 5. Incremental and other engines

- DDlog: archived (`vmware-archive/differential-datalog`, last pushed 2023-07-07).
- Soufflé: no incremental mode in releases (an incremental Soufflé existed only as a research prototype: from memory,
  not verified).
- differential-dataflow, Ascent, Crepe: Rust libraries; a Rust binary per platform, no Python bindings (from
  documentation, not tried).
- Nemo 0.10.1, installed and measured: a 16.8 MB static `nmo` (libc only), release binaries for Linux, macOS, Windows;
  `nemo-python` wheels for all three (the Linux `.so` is 244 MB). `to_nemo.py` translates `idx2.dl` (no `<` on strings,
  so terms became integers in clingo's order; 0.10.1 panics on a head repeating a variable, so an equality instead).
  Same pairs k=1 to 80, about 2x slower than the Soufflé interpreter, 74 MB at k=80.
- pyDatalog, DuckDB (an index of about 30 SQL views): not ported, not measured.
- No practical incremental engine handles stratified negation today; incrementality would come from the plugin
  (re-check only the pairs whose lines changed).

## 6. Recommendation and costs

- **A: Soufflé for the index, clingo for the pairs.** About 90 lines of `.dl`; `spec_solve` writes TSV, runs Soufflé,
  adds the pair facts; witnesses unchanged. Exact, about 13x faster than today at k=40 (18 s vs 230 s; 1.3 GB vs
  13.8 GB). Still about 113 s and 8 GB at k=80.
- **B: Soufflé for everything (`full2`).** Exact, deterministic witnesses, 5 s at 20 k lines with `-j16`, 2.8 GB.
  check.lp re-expressed as about 380 lines of Soufflé; if both encodings are kept, every change is made twice, and the
  fuzz harness should become a test holding them together. Needs the role-count limit with a clingo fallback.
- **C: neither.** Not supported by the data: clingo is 100-200x slower than Soufflé on the same index rules.
- **Recommendation: B with the guard; A as the low-risk first step.** B's memory can be cut further by keying A-side
  relations per requirement rather than per unification.
- Dependency (A and B): the Soufflé 2.5 interpreter (18.5 MB, `--no-preprocessor`); Linux x86_64 via the extracted deb
  in `tools install`, macOS via Homebrew; no Windows, no aarch64-Linux deb, no PyPI wheel, so `tools probe` checks for
  it as it checks GF; no compiled mode needed. Pip-only fallback: Nemo runs the index at about half Soufflé's speed
  (not tried on the search part).

## Files

Programs `index.dl`, `idx2.dl`, `search.dl`, `search2.dl`, `full.dl`, `full2.dl`, `witness.dl`, `idx2.lp`,
`check_hybrid.lp`; converters `tofacts.py`, `to_nemo.py`, `lib.py`; comparison and benchmark scripts `cmp_index.py`,
`cmp_full.py`, `cmp_full2.py`, `fuzz.py`, `fuzz2.py`, `cmp_witness.py`, `bench.py`, `bench2.py`, `bench_nemo.py`,
`clingo_one.py`, `clingo_idx.py`; raw results `bench_j1.jsonl`, `bench_shared.jsonl`, `bench2.jsonl`; tools
`souffle/`, `nemo/`, `venv/`.
