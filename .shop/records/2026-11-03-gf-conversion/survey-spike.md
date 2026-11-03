# Survey of the CNL spike (`.shop/scratch/spike-cnl/`)

Date: 2026-11-03. Branch `gf-conversion`. No code changed. All paths below are relative to
`.shop/scratch/spike-cnl/` unless they start with `scripts/` or `spec/`.

## 1. What is there

| File | Lines | What it is |
|---|---|---|
| `lexicon.py` | 73 | writes `gf-src/Lex.gf` and `gf-src/LexEng.gf` from the glossary in `spec/index.md` |
| `gf-src/Lex.gf`, `LexEng.gf` | 26, 25 | the generated lexicon: one GF category per closed word set |
| `gf-src/Ears.gf`, `EarsEng.gf` | 25, 23 | the requirement grammar (codified EARS), abstract + English concrete |
| `gf-src/Steps.gf`, `StepsEng.gf` | 16, 14 | the Gherkin step grammar, a second grammar over the same lexicon |
| `Ears.pgf`, `Steps.pgf` | binary | compiled grammars (I recompiled both from `gf-src/`: byte-identical) |
| `run.py` | 224 | parse with `pgf`, duplicate check, telingo conflict check, Gherkin generation |
| `resources.lp` | 32 | a separate, hand-written telingo model of exclusivity as held resources (not wired to `run.py`) |
| `cluster.ears`, `cluster-except.ears` | 21, 21 | supervision r66/r20/r59/r95 restated as 6 groups; the second adds an `except` to G2 |
| `out/generated.feature` | 13 | the one generated scenario; `out/g1.lp`, `out/last.lp` the telingo programs |
| `gfc` | 3 | shell wrapper: `LD_LIBRARY_PATH=gf/usr/lib:gf/usr/lib/x86_64-linux-ghc-9.6.7 exec gf/usr/bin/gf "$@"` |
| `gf/` | - | the GF 3.12 .deb extracted (`dpkg-deb -x`), not installed system-wide |
| `dl/gf-3.12-ubuntu-24.04.deb` | 9 MB | the download |
| `venv/` | - | Python 3.11.15 venv: `pgf 1.1`, `clingo 5.8.2`, `telingo 2.1.3`, `cffi`, `pycparser` |

## 2. Running it (what works)

All commands run from the spike directory with `venv/bin/python`; every one ran.

- `lexicon.py`: prints the four categories and three gaps on stderr (IStatus, `implement`, RoundKind are not in
  the glossary and come from `SUPPLEMENT`, `lexicon.py:14-18`). Rewrites `gf-src/Lex*.gf` identically.
- `run.py cluster.ears`: all 7 lines parse. Duplicate: "G3 and G4 state the same thing (r66, r95)". Conflicts:
  "G2 (r66) with G5 (r59): CONFLICT", "G2 (r66) with G6 (r20): CONFLICT". One scenario generated (G1), identical to
  `out/generated.feature`.
- `run.py cluster-except.ears`: the same two pairs become "consistent" once G2 carries
  `except the research or plan or implement stages of different work-items`.
- `run.py --reject`: three lines refused with GF's token error: `Unexpected token: "that"` (free phrasing),
  `Unexpected token: "`drafted`"` (a work-item status where an initiative status is typed: the grammar's type
  check catches the category error), `Unexpected token: "`review`"` (not a round kind).
- `venv/bin/telingo --imax=6 -q1 resources.lp`: SATISFIABLE; the trace runs round_a + workers within 3 slots, never
  both rounds (spec lock) together.
- `gfc -make EarsEng.gf` / `gfc -make StepsEng.gf` recompile the PGFs. Note: `gf -make EarsEng.gf StepsEng.gf` in
  one call writes only `Steps.pgf` (two abstracts); compile one concrete per call.
- `echo 'gr -number=3 | l' | gfc --run Ears.pgf` generates random sentences; it shows overgeneration (§3).

## 3. The grammar's coverage

**Requirement forms** (`gf-src/Ears.gf:6-8`, `EarsEng.gf:4-6`): three of EARS's five patterns.
- `When T, S .` (event-driven), `While P, S .` (state-driven), `S .` (ubiquitous; also how a universal condition
  would be written). Missing: `Where <feature>` (optional feature), `If T, then S` (unwanted behaviour), and the
  complex combination (`While P, when T, S`).
- Triggers/preconditions: exactly three, each a fixed phrase: `StartedNoInitiative`, `MoreThanOne`,
  `ReadyShareNoFile` (`Ears.gf:10-12`).
- Statements: seven fixed phrases, one per requirement of the cluster: `TakeEvery`, `SideBySide`,
  `OnePerInitiative`, `OnePerInitiativeExcept`, `OneRoundAcross`, `TogetherEach` (`Ears.gf:14-19`).
- Lists: `ISList` ("not X and not Y"), `WSList`/`StageList` ("X or Y"), `KindList` ("X , Y and Z", at least 2)
  (`Ears.gf:21-24`).
- So the grammar is phrase-level ("one fun per sentence shape"), not compositional: there is no subject/verb/object
  structure, no general noun phrase over the lexicon's kinds, no quantifiers other than baked-in phrases. Every new
  requirement shape needs a new `fun`. The lexicon declares `cat Kind` (`Lex.gf:2`) but has no words in it.
- Lincats are all `Str` (`EarsEng.gf:2`, `LexEng.gf:2`): no agreement, no number, no RGL. That is enough for one
  language and keeps compile instant, but plural/singular is handled by writing separate phrases.
- Overgeneration seen with `gr`: duplicate list members ("`integrate` , `formulate` , `formulate` and
  `formulate`"), `TogetherEach` without a trigger ("shall start the review stage of each of them" — "them" has no
  antecedent), `While ... claimed and their claims share no file` (any status). Type-level only; no semantic
  well-formedness (dependent types or a post-parse check would be needed).

**Lexicon** (`lexicon.py:30-46`): read by regex from `spec/index.md`'s glossary (`- **term**: ...` lines,
backticked words). Categories: `WStatus` (10), `Stage` (research, plan, implementation, review + supplemented
`implement`), `IStatus` (3, supplemented), `RoundKind` (3, supplemented), `Actor` (only `WorkRun`, hard-coded at
`lexicon.py:55-57`). Backticked words linearize with backticks (`lexicon.py:61-62`). Words with hyphens become
`Cat_awaiting_answer`. The brief says the lexicon's source is now the domain model
(`.shop/records/2026-11-02-domain-model/domain-model.md`, e.g. its status table at line 117), not `spec/index.md`.

**Groups and restates** (`run.py:122-131`, `cluster.ears`): a file of `group <Id> "<title>" restates <old ids>`
headers, each followed by indented requirement lines; `#` comments. A group = one scenario. `restates` is kept as a
raw string and used only in the duplicate/conflict messages (`run.py:257-267`). No validation that restated ids
exist, no file per capability, no requirement ids per line (decision 4 of the brief wants fresh ids, `U<n>` for
universals: absent).

## 4. How Gherkin is generated

- `Steps.gf` is a second grammar over the same `Lex`: one `fun` per step definition (`Steps.gf:8-15`), `Name :
  String -> Inst` for instance names, `Two`/`More` for lists. `run.py:207-208` linearizes an expression string built
  in Python (`lin("GivenInitiative (Name \"i1\") IStatus_started")`).
- The trigger/statement → scenario mapping is hand-coded per construction in `scenario()` (`run.py:222-235`) and
  only for the `StartedNoInitiative` trigger (`run.py:271`): G1 is the only group that yields a scenario. G2-G6 give
  none.
- The Given/Then content comes from telingo's first model (`run.py:183-202`): state 0's `status/2` atoms become
  `Given an initiative iN that is S`; state 1's `taken/1` become `Then ... takes`, the rest `Then ... does not take`,
  `side_by_side/2` gives `ThenSideBySide`. The witness (four initiatives, one per excluded status, the rest
  `started`) is forced by constraints in `program()` (`run.py:158-161`, `178-179`). So the example is the solver's
  model, i.e. a scenario is a satisfying trace of the requirement.
- `GivenWorkItems`, `WhenRun`, `ThenStartsTogether` exist in `Steps.gf` but are never used. Instance names are
  solver constants (`i1`), not glossary-like names. No step definitions (pytest-bdd) exist for the generated
  steps, no `@r<n>` tags, no Background, one model only (no boundary/negative examples), no multiple examples per
  requirement.

## 5. How the logic check works

- `program()` (`run.py:139-180`) translates each AST to a telingo program with two states (`--imin=2 --imax=2`,
  `run.py:188`): `#program initial` is the Given, `#program dynamic` the step after the trigger, with frame rules
  `p :- 'p.` copied by hand for every predicate (`run.py:141-143`). One Python branch per `fun`; `OneRoundAcross`
  has no translation at all, and `ReadyShareNoFile` ignores "claims share no file" (treated as `MoreThanOne`,
  `run.py:149-150`).
- Duplicate check: structural equality of AST tuples across groups (`run.py:253-259`). Catches only identical
  trees, not equivalent ones.
- Conflict check: hard-coded pairing of "pacing" groups (`Always` + `OnePerInitiative*`) with "together" groups
  (`TogetherEach`) (`run.py:261-267`); a pair conflicts when telingo finds no model (`solve()` returns None on
  UNSATISFIABLE). Not a general all-pairs or whole-spec check; no explanation of which constraint fails (no unsat
  core).
- telingo is called as a subprocess (`venv/bin/telingo`) and its text output is scraped with regexes
  (`run.py:189-202`), fragile; telingo has a Python API, and clingo's Python API could be used directly.
- `resources.lp` is the better model for the universal conditions: sessions hold resources (`spec_lock`,
  `initiative(I)`, `item(W)`, `slot`), one rule forbids two running sessions holding the same exclusive resource,
  one bounds slots (r60), and "start whatever may start" (`resources.lp:27-29`). It replaces "except" clauses with
  resources (the comment at line 1). It is not generated from requirements and not used by `run.py`.

## 6. What a production version needs

1. **A compositional grammar** over the domain model's typed glossary: nodes (initiative, work-item, request,
   proposal...), statuses per node, actors (every command, `work run`, sessions), resources; the five EARS
   patterns plus the complex form; universal conditions `U<n>`; quantifiers ("every", "at most one", "each"),
   negation, lists without duplicates. Phrase-per-requirement `fun`s do not scale to 19 capabilities.
2. **A semantic layer**: one ASP translation per grammar `fun` (not per requirement), generic frame axioms, the
   domain model's transitions (§3 table) and resources (from `resources.lp`) as the background theory, universal
   conditions as `#program always` constraints checked on every trace.
3. **A spec file format**: per-capability files of groups with fresh ids, `restates` validated against today's
   `[r<n>]` ids, `U<n>` file under `spec/`; a parser that refuses non-parsing lines with GF's error and position.
4. **Checks**: all-pairs/whole-spec consistency with unsat cores naming the requirements in conflict; equivalence
   (not just identity) for duplicates; overgeneration guards (duplicate list members, dangling "them").
5. **Generation**: a Steps function per statement/trigger kind, several examples per requirement (positive, the
   boundary, the excluded case), readable instance names, `@<id>` tags, one `.feature` per capability, and step
   definitions (generic, one per Steps `fun`) in `tests/scenarios/`.
6. **Lexicon from the domain model**, with gaps reported as refusals (not silently supplemented, `lexicon.py:14-18`).
7. **Build**: `.gf` → `.pgf` compiled by `gf` whenever the lexicon changes (the pgf binding cannot compile);
   PGFs cached and rebuilt on glossary change. Use clingo/telingo Python APIs, not subprocess scraping.
8. **Modules under 300 lines** and rows in CLAUDE.md's module map (`run.py` alone is 224 lines for one cluster).

## 7. How GF, pgf, telingo/clingo were installed (to make them real dependencies)

**GF compiler (`gf` 3.12)** — needed to compile `.gf` → `.pgf`:
- Downloaded `gf-3.12-ubuntu-24.04.deb` from the official release:
  `https://github.com/GrammaticalFramework/gf-core/releases/download/release-3.12/gf-3.12-ubuntu-24.04.deb`
  (note the tag is `release-3.12`, not `3.12`: `.../download/3.12/...` is a 404).
  sha256 `17aa5452b713f1e00a0755a1bad998a926acbffb96eefde2c3800ca72536b4d8`, matching GitHub's published digest.
  Other assets: `gf-3.12-macos-arm.pkg`, `gf-3.12-macos-intel.pkg`, `gf-3.12-windows.zip`.
- Not installed with dpkg (no root needed): extracted with `dpkg-deb -x dl/gf-3.12-ubuntu-24.04.deb gf/`. The
  binary `gf/usr/bin/gf` (GHC 9.6.7 build, "version 3.12.0, commit fa2826d") is dynamically linked against
  `libpgf.so.0`, `libgu.so.0` (in `gf/usr/lib`) and `libHSgf-3.12.0-*.so` (in
  `gf/usr/lib/x86_64-linux-ghc-9.6.7`), hence the `gfc` wrapper setting `LD_LIBRARY_PATH`. System deps from the
  deb's control: `libc6 >= 2.34`, `libgmp10`, `libtinfo6`; all present on this Debian 13 (trixie) host.
- The deb also ships a `pgf` Python egg for system Python 3.12 (`gf/usr/local/lib/python3.12/dist-packages/`); it
  is unused (wrong Python, not in the venv).
- `gf` is not on PATH (`gf` in zsh is a git alias: name the binary by path or install it as e.g. `.shop/bin/gf`).
- The grammars use no RGL (all lincats `Str`), so no `gf-rgl` download is needed.

**pgf Python binding (`pgf` 1.1)** — parsing and linearizing at runtime:
- Installed from PyPI into the venv (`INSTALLER` = pip): a manylinux wheel
  (`cp311-...-manylinux2014_x86_64/manylinux_2_28_x86_64`) that bundles its own `libpgf`/`libgu` in `pgf.libs/`.
  It does not need the deb. Wheels exist for cp311, cp312 and cp313 (checked with `pip download --only-binary`).
  So `pip install pgf==1.1` is enough for runtime parsing on x86_64 Linux.

**telingo / clingo** — the logic check:
- `pip install telingo` → `telingo 2.1.3`, pulling `clingo 5.8.2` (+ `cffi 2.1.1`, `pycparser`). Both are
  manylinux wheels; `venv/bin/telingo` is the CLI that `run.py` shells out to.

**Fitting into `scripts/tools_env.py`**:
- Today `TOOLS` (`scripts/tools_env.py:8-22`) is a tuple of (name, pip package, purpose, without-it) and
  `cmd_install` (`:82-106`) pip-installs each missing package into the project's virtualenv, found by
  `interpreter()` (`:34-43`: `--python`, `.venv/bin/python`, `venv/bin/python`, `$VIRTUAL_ENV`); a pin exists only
  for ruff (`RUFF_PIN`, `:23`). `probe` reads versions via `importlib.metadata` (`VERSIONS`, `:24-27`).
- `pgf`, `clingo`, `telingo` fit that scheme directly: add rows (pinned `pgf==1.1`, `telingo==2.1.3`,
  `clingo==5.8.2`, generalising `RUFF_PIN` to a pin per tool). But these are needed by the plugin's own scripts at
  run time (parsing the spec), not only analysis tools of the target project; they belong in the interpreter that
  runs `scripts/` too. This repo has no `.venv`/`venv` today and no `pyproject.toml`/`requirements.txt`.
- `gf` is not a pip package: `install` needs a new step that downloads the release asset for the platform, checks
  the sha256 above, extracts it (`dpkg-deb -x`, or Python's `ar`+`tarfile` to avoid needing dpkg) into a
  plugin-owned directory, and exposes a wrapper with `LD_LIBRARY_PATH`; `probe` runs `gf --version`. Alternative:
  ship the compiled `.pgf` files and require `gf` only when the lexicon changes.
