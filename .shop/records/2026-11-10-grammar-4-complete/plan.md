# Grammar 4 complete (b240) Implementation Plan

> **For agentic workers:** carried out as CLAUDE.md says a plan is: **fresh implementers carry the phases in order on
> one long-lived branch, `plan-grammar-4`, then one fresh reviewer reviews the whole branch.** One implementer a
> phase (a fresh agent each), never an implementer and a reviewer per phase. Steps use checkbox (`- [ ]`) syntax.

**Goal:** the rest of b112's grammar 4 work as one plan item (b240, the person in quote-22): the constructs the audit
found missing, every capability of this repository reworded once in grammar 4 against a corpus of intended readings,
the old pipeline removed, the upgrade step "the controlled language 4" and release 4.0.0. The grammar is done when
every line of the reworded spec parses to the reading its corpus gives it, and `model logic`, `features generate
--check`, `model check` and the suite pass over it.

**Folds:** b239 (phase 1), b236, b237, b238 (phase 12), b152-b159 (phases 13-23), b160 (phases 24-25), b161
(phase 26). The items' statuses are not changed by the plan; the main session closes them after the merge, citing
b240. Not in scope (b240's notes): the construct catalogue (audit construct 9, reopening b124); the authoring skills
(design I30); b234 and b235, which this plan does not need because it lays lines directly (see "How a line enters
the spec"), and which stay items of their own.

**Spec:** `.shop/backlog/b240.md` (its notes); the audit `.shop/records/2026-11-10-grammar-4-audit.md` and its folder
(each line's verdict and missing construct in `b15x-audit.tsv`, the reasoning in `b15x-audit.md`); the design
`.shop/records/2026-11-09-cnl-4/design.md` (calls 1-16, sections 6, 7, 9, 10.3 I19-I29); `grammar/language.md`; the
reword items `.shop/backlog/b152.md`-`b159.md` (their lines, notes and term bullets); b160, b161, b234-b239.

**Tech stack:** Python 3 (standard library), pytest with xdist, GF 3.12 with pgf, clingo. The project's commands
`scripts/model`, `scripts/features`, `scripts/tools`, `scripts/work`.

## Global constraints

- main's checkout is the reference. Never read leftover worktrees under `.shop/worktrees/` other than this plan's own
  (`.shop/worktrees/plan-grammar-4`) to learn the code; do not read other repositories. The batch-33 branches are
  read with git (`git show`, `git diff`, `git cherry-pick`), never through a worktree.
- Every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300` exits 0).
  `scripts/spec_lf_facts.py` is at 300 already: the first phase that changes it splits it first (by concern: the
  atoms of a clause, the boxes), in its own commit with the gate green.
- A new module gets a row in CLAUDE.md's module map; a module whose concern changes gets its row rewritten; a removed
  module's row goes. In the same commit.
- **A requirement line is never edited in place.** A changed line gets a new id; the old id goes to its file's
  `retired:`. A design-decision only through `work decision`; a record through `work record` (supporting files by
  hand). Nothing is written under `docs/superpowers/`.
- **Writing a requirement line** (the person's rules, and the audit's):
  - plain sentence structure and plain words. Never a coined adjective or noun that hides structure (the person: "A
    grammar is sentence structure combined with terms. We should not be defining simple english terms with domain
    specific meaning."). A state is said with structure: "an item whose status is not `delivered`", "a comment that
    does not conform to the comment form", never "undelivered", "unreadable".
  - a command's option is in the trigger's code with its argument: "When the person runs `work backlog` with the
    `--json` option, ...", never "Where `--json` is given".
  - a refusal is short: "... then `work` shall refuse the command and name the status."
  - the agent is explicit: every response says who does it (`work`, `model`, the session, ...).
  - example data goes in the group's given block, not the line (design call 7).
  - a line names the grammar as an artifact (the language reference `grammar/language.md`, the corpus) and never
    names a construct by a coined word. The construct-level checks are the corpus's, not requirement lines'.
- Commit messages cite the items: a last paragraph `Item: b240` and, where the phase folds one, `Item: b15x` (b239,
  b236 ...) on its own line; then the session's attribution lines.
- Push after every commit: `<wrapper> git push -u origin plan-grammar-4` (the wrapper the session gives unsets
  `GH_TOKEN` and gives git gh's credentials); gh as `env -u GH_TOKEN gh ...`.
- Give every long command a timeout: `timeout 600 python3 -m pytest -q` for the suite, a few minutes for the rest.

## The branch

Phase 1 creates it: `git worktree add .shop/worktrees/plan-grammar-4 -b plan-grammar-4 origin/main` (or reuse the
worktree if the session made it). Every phase works in that worktree. At the start of each phase, if `origin/main`
has moved, merge it into the branch (`git merge origin/main`) and run the gate before anything else; a conflict in
`spec/` or `features/` is a stop (below).

## The gate

Every phase ends with the whole gate green, and every commit inside a phase leaves it green where the phase says so.

| # | Command (from the worktree) | Passes when |
|---|---|---|
| G1 | `timeout 600 python3 -m pytest -q` | no failure and no error; xfails only for ids in an `unbuilt:` |
| G2 | `python3 scripts/model check` | its last line starts `0 violations` |
| G3 | `python3 scripts/features generate --check` | exit 0 |
| G4 | `python3 scripts/features vocab --check` | prints `every step has one handler` |
| G5 | `python3 scripts/tools size --limit 300` | exit 0 |
| G6 | `python3 scripts/tools check <each .py file the phase changed>` | ruff and vulture print `clean` |
| G7 | `python3 scripts/model logic` | no L0, no L1, no "no translation"; the L5, L6 and `aside` lines change only for a capability the phase rewords, and the commit message lists each change (main today: `45 findings: 4 L5, 31 L6, 10 aside`) |
| G8 | `python3 scripts/model decisions --check` | the same three `failing` lines as main (0086-0088, `tests/scenarios/vocab.py: exit 5`), every other decision `holds` |

The corpus tests (phase 2) are part of G1 from phase 2 on.

## When a phase proves bigger

The phases are sized for one implementer of a few hours. When one proves bigger, **stop at a green commit**: commit
nothing that leaves the gate red, push what is committed, and reply with the phase, the step reached, what is left
(as checkboxes), the last 30 lines of the failing command if any, and what needs deciding. Do not improvise around
the plan. The session dispatches a fresh implementer for the rest (the phase's remainder becomes phase Na). Stop
also when:

- a gate command fails and the fix is outside what the phase names;
- a line's intended reading cannot be had without a construct the plan lists as a known limit (write the best plain
  line, list it under the limit, go on; stop only if no plain line keeps the old meaning at all and the old line is
  not one the audit already marks unsayable);
- a merge of `origin/main` conflicts in `spec/`, `features/` or `grammar/`;
- `model logic` shows an L1 between two reworded lines that rewording within the line's meaning does not remove.

## The acceptance corpus (built in phase 2)

Two parts, both golden tests in G1.

**The construct twins**, in `grammar/language.md`: each construct of the language has its section, and each section
blocks of a line and its logical form, read in a fixture context (`tests/scripts/fixtures/codified-2/`, or another
fixture tagged as the time blocks are: ```` ```reading-time ````). `tests/scripts/test_spec_lf_read.py` (and
`test_spec_lf_time.py`) read every block and fail when grammar 4 reads its line otherwise. Each construct phase
adds its section and blocks here **first**, each twin taken from a real line the audit names (the section says
which), extends the fixture with the words the twin needs, and sees the new blocks fail before building.

**The spec corpus**, `grammar/corpus/spec/<capability>.md` (and `grammar/corpus/spec/universal.md`): every live line
of a codified-2 file, under its id, with its intended reading.

````
# requests: every live line with its intended reading (b240)

## r103
Retires: r45. From: b153 r89. Audit: distortion, fixed by section 5 ("not close the issue of the request").

```reading
If the person runs `work reply` on a request that this bounded context received, then `work` shall refuse the command and name the request.
shall [x1: agent the person (constant), ...]
  if [...]
    ...
  response
    ...
```
````

- The heading is the id; the `Retires:`/`From:`/`Audit:` line is the trace (the retired id, the item line it reuses,
  the audit's verdict and what fixed it, or `Known limit: #14` with the limit's construct number). A line kept from
  the old spec says `Kept.`
- The block is the line, word for word as the capability file has it, then its logical form as `model parse --form`
  prints it. The form is the **intended** reading: written before the line goes into the spec, from the old line's
  meaning, the audit row and the item's notes, not copied from the parser's output. Where the parser prints the form
  already, the implementer reads it against the old line, atom by atom, and writes down the form only when it agrees.
- `tests/scripts/test_corpus_spec.py` (new, phase 2) runs it:
  1. each block's line parses in the live repository (`spec_grammar4.parse(REPO, line)`) to one meaning, and
     `spec_lf.show(spec_lf.form(...))` equals the block's form;
  2. each block's form translates to the check's facts (`spec_lf_facts`) and to steps (`spec_steps4`) with no
     refusal ("no translation of ...", "no Then of ...", "no step of ...");
  3. for every file whose marker is codified-2, the set of headings equals the set of live ids, and each block's line
     equals the file's line of that id; a capability file still codified-1 needs no corpus file;
  4. the line linearises back word for word.
- **Done** is: every capability file and `spec/universal.md` say codified-2 (phase 24 makes the last ones), so check 3
  covers every line of the spec, and G1-G8 pass.

## How a line enters the spec

The plan writes lines directly on its branch, as `work batch start` lays an item (`backlog_lines.lay_onto` is the
reference for the shape), not through `work line`/`work ready`/`work batch`:

- a changed line gets the next free id of its capability: past every id the capability file holds, live or retired,
  and past every id an open item other than b152-b159 holds for it (b160, b161 and the gap items; as
  `backlog_lines.renumber` does). A line that parses unchanged in grammar 4 and means the same keeps its id.
- the old line leaves `## Behaviour`; its id goes into the file's `retired:`. Its group's successor carries the same
  `Restates:` as the old group (as batch-33-b154 did), so `model restates` keeps its coverage.
- the new id goes into `unbuilt:` while its scenario fails, and leaves it when its handler passes (strict xfail: a
  reworded line whose behaviour exists XPASSes and must leave `unbuilt:` at once).
- the capability's marker becomes `language: codified-2` in the same commit as its lines: a file switches whole
  (design call 15).
- terms: the coined terms its lines no longer use leave the capability's `## Terms` (and the glossary's, when no line
  of any capability uses them); new terms and rows come with the lines; `model check` (v_t codes) stays clean.
- features: `python3 scripts/features generate` writes the capability's feature; handlers follow.

The b15x items' `## Requirements` are the source of each reword's lines, not its target: they stay as they are.

---

## Phase 1: the branch, and grammar 4's caches (b239)

**Goal:** grammar 4 computes its sources and loads its grammar once per process for one lexicon, keeps parses in the
on-disk parse cache, and reuses the compiled PGF of unchanged sources. Every later phase pays for parsing; this goes
first. b239's requirement lines are not added here: they go into design-model-check in grammar 4 in phase 22.

- [ ] Make the branch and worktree (above). Run the gate on it and keep the numbers: the suite's pass count and time,
  `model check`'s warnings, `model logic`'s summary.
- [ ] Profile as b239 did: `readiness_bar.check` on b154's lines (21 s on main), and `python3 scripts/model parse
  --form` on one line. Write the numbers into the commit message.
- [ ] Test first, in `tests/scripts/test_spec_grammar4_cache.py`: (a) two `spec_grammar4.sources`/`load` calls for one
  lexicon in a process compute once (count with a monkeypatched inner function); (b) a change to a term of the
  lexicon, or to a pack, misses; (c) a parse of a line read twice through `spec_parse_cache` gives the same result,
  and the second makes no GF parse; (d) the compiled PGF is not rewritten while its sources are unchanged (mtime).
- [ ] Memoise `spec_grammar4`'s sources and load per process, keyed by the lexicon's and packs' content (invalidated
  when they change); route grammar 4's parses through `scripts/spec_parse_cache.py` with a key holding the grammar's
  sources, the grammar, the lexicon's words and the text; reuse the compiled PGF as `spec_grammar._compile` does.
- [ ] Results identical: `model logic --json` and `features generate --check` as before; the suite's pass count as
  before. The profile again; the commit message gives before and after.
- [ ] Gate; commit `grammar 4 caches its sources, grammar and parses` (Item: b240, Item: b239); push.

## Phase 2: the acceptance corpus

**Goal:** the harness of "The acceptance corpus", before any construct, so every later phase writes its readings
first.

- [ ] `grammar/corpus/spec/README.md`: what a spec corpus file is (the section above, shortened), and how to add a
  block (write the line and its intended form, run the test, see it fail, then lay the line).
- [ ] `tests/scripts/test_corpus_spec.py` with checks 1-4. While every file is codified-1 it finds no corpus file to
  require; prove it with a fixture: a copy of `tests/scripts/fixtures/codified-2/` with one capability, its corpus
  file and a deliberately wrong form (the test fails), then the right one (it passes).
- [ ] Check 2 needs a function that translates one form to facts and to steps without a whole context run: find it in
  `spec_context`/`spec_lf_facts`/`spec_steps4`, or add a small one beside them. No change of behaviour.
- [ ] In `grammar/language.md`, after the reading rules, two empty sections the later phases fill: `## Constructs`
  (one subsection a construct) and `## What the language cannot say yet` (one subsection a limit: the construct, its
  lines by id, the plain line used instead). Say there that the spec corpus is the acceptance test.
- [ ] Gate; commit; push.

## Phases 3-11: the constructs

In the audit's order (section 6). For each construct phase:

1. **Twins first.** Add the construct's subsection under `## Constructs` with its blocks: each twin a line of the
   fixture's words shaped like the real line the phase names, with the form it is meant to have; refusals as
   `refused: <reason>` blocks. Add the words the twins need to the fixture (a new fixture beside it if the words
   would change other blocks' readings). Run the tests: the new blocks fail.
2. **Build** the construct through every reader: the grammar (`grammar/Base*.gf`, or the generated parts in
   `scripts/spec_rgl*.py`), the form (`scripts/spec_lf_*.py`, the reading rules in `spec_lf_read.py`), the check
   (`scripts/spec_lf_facts.py` and `grammar/check.lp`), the steps (`scripts/spec_steps4*.py`, `grammar/Steps4*.gf` or
   `spec_rgl_steps.py`) and a generic handler for the new step in the codified-2 world (`tests/scenarios/codified2_*`).
   A construct that the check or the generator cannot read is not done: the corpus's check 2 holds for every twin.
3. **Refusals** the construct brings go into `grammar/corpus/refused.txt` or `core-4.txt` with their reasons.
4. No requirement line is added by a construct phase. G7 unchanged (no capability is reworded yet).

### Phase 3: R2 accessibility and the boxes of "or" (audit section 3, faults)

- Real lines: design-model-check r231 (b152), backlog r6, batches r4 (b158): `the item` and `the task` bound
  outside the `every` box they were made in; and the cases of an "or", which are not boxes today.
- Build: R2 refuses a "the K" whose only antecedent sits inside a `not`, `every`, `only`, count or `or` box it is
  outside of; the cases of an "or" are boxes. The refusal names the noun and the box ("the task" is made inside
  "every task ..."). Check what of the spec still parses: no codified-1 line is read by R2, so only the twins move.
- Also: requests r63 ("assign the line outcome of a request line") and r199 ("use an interpreter") show R1 making a
  new referent where an old one is meant. That is a writing fault: add a twin of each to R1's section showing the
  reading, so the reword phases write "the ..."; no code.

### Phase 4: conformance to a named artifact (#5)

- Real lines: requests r76, r77, r82, r86, r87, r95, r100 (b153); design-model-check r189, r195, r196 (b152);
  readiness r21, r24, r26 (b157). The design's own example (section 6.2): "While a request comment does not conform to
  the comment schema, when a session runs `work sync`, `work` shall print the comment and not write the comment."
- Build: "X conforms to A", "X does not conform to A", and "a K that conforms to A" in a relative clause, where A is a
  noun of a kind under an artifact kind (a form, a schema, the language reference) or a code naming a file; the atom
  `conforms(x, a)` (design 7.2) in the form, a state fact in the check (it can clash like any state), a Given
  "the comment does not conform to the comment form" in the steps. Decide in the grammar whether `conform` is base
  grammar or a CLI-pack verb with a frame `thing conforms to artifact`; prefer the pack if it needs no new
  category. Split `spec_lf_facts.py` first (Global constraints).
- Counterfactual lines (#13) whose "would write" is a generator's output ("is not what `model decisions` would
  write", design-model-check r202, r203, r220) are said "does not conform to what `model decisions` writes" only if
  the twin reads cleanly; else they are a known limit (phase 26's list).

### Phase 5: ordered comparison (#6)

- Real lines: migration-tools r36, r39-r42, r45, r47, r51, r55 (b156; "lacks the verb-frames step" inverts 16
  lines); b161's grammar 4 form "While the release of the repository is after `3.0.0` and before `4.0.0`, ...".
- Build: an attribute entry may declare its values ordered (the spelling is the builder's, read from the entry
  alone; a release orders by its numbers); "is after v", "is before v", "is not after v", and "is v or after"
  if a twin needs it, over such an attribute; `cmp(x, A, op, v)` in the form; in the check, exact over the finite
  points the lines name and the gaps between them (design call 9); Givens with a value on the right side of each
  point. The time pack's moments already compare (language.md "Time"): reuse its form, do not fork it.

### Phase 6: value sets and attribute absence (#4)

- Real lines: decision-tiers r13 ("is not `superseded`, not `rejected` and not ..."; "untiered") and r23 (b159);
  backlog r28-r33 (b158); migration-tools r48, r52-r54 (b156); requests r60 (b153); intake r10 (b159).
- Build: "the T of x is one of `a`, `b` or `c`", "is not `a`, `b` or `c`" (a value set; its negation is "none of
  them", not "some other declared value"), "x has no T" (the attribute absent); and "every K of x is `v`" where the
  audit's lines say "every line is settled". Facts: a set as the disjunction the check already has for "or", or a
  set atom; absence as its own fact, distinct from every declared value.

### Phase 7: the number of (#3)

- Real lines: analysis-tools r49-r51, r53, r56-r58, r64 (b154; "the test count of the function"); batch-measurement
  r23-r25, r27 (b156); feature-file-tools r45, r46, r61, r64, r79, r80 (b157); design-model-check r202, r203, r239,
  r252 (b152); backlog r27 (b158); intake r11 (b159); U16 (b155, "one JSON object", a count already, call 4).
- Build: "the number of Ks that P" as a value: printed ("`tools` shall print the number of tests that execute the
  function"), compared ("While the number of tasks of the batch is more than `batch_size`") against a constant or a
  code; a clingo `#count` in the check (call 4's counts exist: `spec_lf_core` count boxes; extend them to a value);
  steps that give the scenario that many Ks.

### Phase 8: identity and distinctness, the grammar and the form (#2)

- Real lines: design-model-check r176 ("two requirements share an id"), r179, r199, r218, r224, r247-r249, r276-r278
  (b152; r276-r278 are the L1 lines that link only through a shared act, so any two lines on one act clash);
  migration-tools r28, r29 (b156); telemetry r8 (b156); backlog r26, r39; batches r20, r22, r32 (b158).
- Build: "the same K" (one referent named twice: "two requirements whose id is the same id" → "two requirements of
  the same id"), "another K" and "a different K" (a referent distinct from an earlier one of its kind), "two Ks"
  meaning two distinct; the form's `distinct(x, y)` and `same` binding. The reading rules gain the rule (R13 or a
  subsection; say which earlier referent "another" is distinct from: the latest of its kind, as R2).

### Phase 9: identity and distinctness, the check and the steps (#2)

- Build: `distinct(x, y)` in the facts and `check.lp` (two referents never unified), "of the same trigger and state"
  for the L1 lines of design-model-check (the twin of r276-r278 must not clash for two lines on one act with different
  states); the steps give two named instances and say they differ. G7: main's findings unchanged.

### Phase 10: existence (#7)

- Real lines: analysis-tools r37-r41, r48, r50, r52-r55 (b154; "this file system holds the dot-venv interpreter");
  requests r72, r81 (b153).
- Build: "X exists", "no K exists", and the perfect of a write as existence where the twin needs it ("has been
  written" is history, already built: reuse it); `exists(x)` in the form, a state fact in the check, a Given that
  makes the file or leaves it out.

### Phase 11: the option with its argument, and the run's own things (#12, #11)

- Real lines: requests r59-r62, r82, r97-r102 (b153; options glued into the command code: "with `--source` and
  `--thread`", "with `--forward`"); analysis-tools r36, r43-r46, r66 (b154; `This:` on the Python interpreter);
  U16; backlog r27; decision-tiers r19, r20; intake r13 (b159).
- Build: "runs `cmd` with the `--x` option", "with the `--x` and `--y` options", "with the `--x` option on a K",
  "with the `--x` option set to `v`" (the argument), and "without the `--x` option"; `run(e, agent, command,
  options)` carries each option and its argument (design 7.2); the trigger's step names them. The run's own things
  are glossary work: `This:` on the kinds the audit names (Python interpreter, decisions index, git directory,
  transcript, the push the command makes): add the entries in the reword phases that use them; here only twins of
  each shape ("the push of the command", "the commit that the command makes").

### Phase 12: the bar and the generator accept every form that parses (b236, b237, b238)

**Goal:** a line that parses to one meaning is never refused by `model logic`, the readiness bar or `features
generate` for want of a translation. After this phase the corpus's check 2 is the guard.

- Twins first, in `## Constructs` (or the R-sections they belong to), one for each gap:
  - b236: a verb with two frames of one role label is stepped in the frame its referents' kinds pick (the frame the
    parse typed the clause by), in `spec_steps4.Reader.frame`. Twin of migration-tools' supersede and
    decision-tiers' enforce.
  - b237: a Then for a negated response over a K the line names nowhere before ("`work` shall not pick an item that
    has the dependency", "shall write no scenario line of the requirement group"): "no K ... is V-ed" in
    `spec_steps4_boxes.acts`.
  - b238: a `no K` box whose restriction holds a negated attribute of an inner referent ("no dependency on an item
    whose status is not `delivered`") translated in `spec_lf_facts`' `none` (`rnone` over the pair with the inner
    value negated).
  - the audit's two: "every function of the Python file that no test executes" (the bar refuses it; the generator
    and the check must read an `every` in a response's relative clause), and "not close the issue of the request" (a
    Then of a negated response over a relation's image).
- Then sweep: run check 2 over every twin in `grammar/language.md` and every line of the b152-b159 items' `##
  Requirements` that parses today (a throwaway script in the scratchpad, `spec_grammar4.parse` on each); list each
  "no translation"/"no Then"/"no step" left; fix each that a construct phase built; each left over is either a
  known limit (write it in language.md's limits now, with the line) or a stop.
- b236-b238's own lines are not added: their coined words (reframing, refraining, screening) are what the artifact
  lines of phases 21 and 22 replace.

## Phases 13-23: every capability reworded once

For each reword phase, per capability:

1. **Read**: the capability file; its item's `## Requirements`, notes and term bullets (b15x); its rows in
   `b15x-audit.tsv` (verdict, construct, evidence) and the reasoning in `b15x-audit.md`; the audit's section 5 rows for
   it; the design's b118 faults for it (section 10.3, I21-I27's table).
2. **Choose each line**: a line the audit marks `fine` is reused as the item has it. A `distortion` or `unsayable`
   line is rewritten with section 5's fix, or with the construct phase 3-12 built for it, from the **old** line's
   meaning (never the item's distorted wording). A `coined` line loses its coined word for structure. A line whose
   construct is a known limit is written as plainly as it can be and listed under the limit in language.md.
3. **Corpus first**: write `grammar/corpus/spec/<capability>.md`, every line with its trace and its intended form
   (check 1 fails: the lines are not in the spec yet, and their terms may be missing).
4. **Lay**: terms and rows, then the lines (How a line enters the spec), the marker codified-2; `features generate`;
   check 1-4 pass; G2, G3, G7.
5. **Handlers**: reuse the batch-33 code where it is named (cherry-pick, or `git show <commit>:<path>` and adapt);
   write the rest; take ids out of `unbuilt:` as they pass. A phase may end with ids still `unbuilt:` only where it
   says so.
6. **Gate**, one commit for lines, terms, corpus and features (Item: b240, Item: b15x), one or more for handlers.

### Phase 13: the codified-2 scenario tooling, and trials (b154 part)

- Tooling from batch-33, two attempts at one thing, made one: b154's `5ce8fd84b` (`tests/scenarios/vocab4.py`,
  `scripts/features_vocab4.py`, `scripts/features`, `scripts/spec_unbuilt.py`, `tests/scenarios/vocab.py`,
  `tests/scripts/test_spec_steps4.py`: a codified-2 feature's steps read by pytest-bdd and `features vocab --check`,
  unbuilt ids marked) and b153's `fba1d39fb` (`scripts/spec_rgl_steps.py`: step parses cached on disk;
  `tests/scenarios/work_queue_world.py`: `bind_all`; its own `spec_unbuilt` and `features` changes). Take b154's as
  the base and add b153's step-parse cache (through phase 1's cache if it fits) and `bind_all`; one change to
  `spec_unbuilt` and `scripts/features`. Tests from both commits.
- trials (5 lines, b154's r6-r10; audit 3 fine, 2 distortion fixed by section 5: "no-trigger only invariants", r7,
  r8): reuse `3407ca0ea` (trials in grammar 4, `tests/scripts/test_spec_guarantees.py`).

### Phase 14: the universal conditions (b155)

- 5 lines, b155's U12-U16 retiring U4, U5, U7, U8, U11. Section 5: U15, U16 (worktree re-glossed; rows `worktree |
  of | session | one`, `command | of | tool | one`, and `commit | of | text` for U13, added to `spec/index.md`'s `##
  Relations` directly; U15 narrowed to a task's dispatch); U16 with the option in the trigger (phase 11); U14 "shall
  not write a transition" is a known limit of #8 (attribute change) unless phase 11 or later gives a plain form.
- `spec/universal.md` says codified-2; corpus `grammar/corpus/spec/universal.md`. `tests/scenarios/vocab.py`'s U4,
  U8 and U11 checks after every scenario keep passing under their new ids (and decisions 0086-0088's `enforced_by`
  stay as on main).

### Phase 15: decision-tiers, pr-review, intake, conversation, brainstorming (b159)

- 31 lines (b159's 28 written, plus decision-tiers' lines added since). Audit: decision-tiers 5 fine of 11, pr-review
  8 of 9, intake 0 of 4, conversation 2 of 4, brainstorming 2 of 3. Constructs: value sets (r13 untiered, r23),
  options (r20, intake r13), number of (intake r11), b236 (enforce's frames). Section 5: decision-tiers r19 (`This:`
  on decisions index), r23 (route an attribute with `Values:`); intake r11 (a verb "counter"), r12 (the reason of the
  line); conversation r6 (git directory and transcript named); brainstorming r5 (a frame for the quoted words).

### Phase 16: backlog and batches (b158)

- 40 lines. Audit: backlog 14 fine of 21, batches 15 of 21. Constructs: value sets (backlog r28-r33), identity
  (backlog r26, r39; batches r20, r22, r32), R2 fix (backlog r6, batches r4), b237, b238 (batches r20, r22), count
  (backlog r27). Section 5: backlog r27 ("one JSON object" with the `--json` option), r36 (the remote of this
  repository); batches r20, r30, r9 (the in-batch Then explicit; a "from" frame for remove, "of" for propose; merge's
  gloss). Bounded time (backlog r37's push timeout) is a known limit (#16, b127).

### Phase 17: requests (b153)

- 44 lines (b153's r59-r102). Audit 18 fine, 16 distortion, 10 coined. Constructs: conformance (r76, r77, r82, r86,
  r87, r95, r100), option (r59-r62, r82, r97-r102), existence (r72, r81), value sets (r60). Section 5: r61, r102,
  r97-r101 (options), r76 ("does not hold the comment"), r81 (the dropped conjunct), r84 (r79's form), r99 (the real
  waiting condition), r89, r90 ("not close the issue of the request").
- Handlers: reuse `83ed16ea5` (`requests_handlers*.py`, `requests_handlers_givens.py`, `requests_handlers_thens.py`,
  `requests_world.py`, `world_fallbacks.py`, `scripts/shop_files.py`: git's refusal names the repository) against the
  new steps; its spec and feature hunks are not reused (the lines differ).

### Phase 18: analysis-tools (b154)

- 35 lines (b154's r36-r67, r7 and r8 kept). Audit 8 fine, 23 distortion, 2 unsayable. Constructs: existence
  (r37-r41, r48-r55), number of (r49-r58, r64), option (r36), `This:` (r43-r46, r66). Section 5: r26 (a `tools refs
  --json` line), r43-r46, r66 (`This:` on Python interpreter), r44, r54 (a plain verb "pin"; refuse a name). The
  first-match rule over four interpreters (r37-r41) is ordered choice (#14), a known limit: write each case with
  existence and list them.
- Handlers: reuse `0e2284899` (`analysis_tools_handlers.py`, `analysis_tools_handlers_thens.py`,
  `analysis_tools_world.py`, `world_cli.py`, `scripts/tools`: `tools <command> --python`).

### Phase 19: migration-tools, telemetry, batch-measurement (b156)

- 39 lines (b156's migration-tools r26-r55, telemetry r5-r8, batch-measurement r23-r27). Audit: 4 fine of 39.
  Constructs: ordered comparison (the 16 "lack" lines), number of (batch-measurement, telemetry r6), identity
  (r28, r29, telemetry r8), value sets (r48, r52-r54), b236 (supersede). Section 5: r34, r35 ("uncommitted change"),
  r48, r52 ("of this repository"; "whose asker is not this bounded context"); telemetry r5 (four figures as
  attributes); telemetry r8, batch-measurement r26 ("two batches ... each of the batches"). The ratio (r26) is a
  known limit (#18).
- Not b161's line: phase 26 adds it.

### Phase 20: readiness (b157 part)

- 27 lines (b157's readiness r20-r37, r4 kept, and the lines added since). Audit 12 fine, 8 distortion, 7 coined.
  Constructs: conformance (r21, r24, r26), number of (r27, r30). Section 5: r33 ("does not meet"), r29, r37 (relate
  the id to a live requirement), r31, r35 (a `language` attribute of capability with `Values:` `codified-1`,
  `codified-2`, in place of "codified-2 marker").

### Phase 21: feature-file-tools, with the artifact lines (b157 part, b236, b237)

- 67 lines today, 51 of them coined: the generator's construct lines (b197, b215-b222: r23-r44; b157's reworded
  r66-r87 with nouns of structure). These are what the person's direction replaces: **one artifact line covers
  them**, and the corpus and language.md's twins are their tests. Retire each construct line with the artifact line
  as its successor (its group's `Restates:` carried), and write in the corpus trace `Retires: r30. Successor: r<n>
  (the corpus checks the construct: language.md "<section>")`.
- The artifact lines (the intended meaning; the exact words are checked with `model parse --form` and written to
  the corpus; terms `language reference` (noun, the file `grammar/language.md`, Kind of: file, `This:` the language
  reference of the plugin the command runs) and `corpus` likewise, in the glossary):
  - "When the person runs `features generate` on a capability whose requirements conform to the language reference,
    `features` shall write a scenario of every requirement group of the capability."
  - "When the person runs `features generate` with the `--check` option on a capability whose feature file is what
    `features generate` writes, `features` shall exit successfully." (keep the existing line if it says this)
- The other lines: audit 7 fine, 9 distortion. Section 5: r55, r60, r49 (an "every" While clause; restore
  "codified"; split r49 in two); r31, r35, r65, r66-r87 (the `language` attribute, phase 20's).

### Phase 22: design-model-check, the lines (b152, b239, b238)

- 115 lines. Too many to build in one phase, so this phase lays every line, corpus and term with the ids whose
  scenarios fail in `unbuilt:`, and phase 23 builds them. The file switches whole here.
- Audit: 47 fine, 44 distortion, 3 unsayable, 21 coined. Section 5: r207, r214 ("a term has no frame"); r230, r251
  ("does not agree"; "no premise entails the consequence"); r192, r194 (a section kind with "or"); r174 (restore "0
  violations"); the rule-code lines ("While a capability violates `v15a`") stay, by the person's choice of the
  catalogue (b123). Constructs: identity (r176, r179, r199, r218, r224, r247-r249, r276-r278), number of, conformance
  (r189, r195, r196), counterfactual (r202, r203, r220: phase 4's form or a known limit), R2 (r231).
- The gap items' construct lines (b197, b215-b222 as r265-r278; b238's screening, unscreened) are retired for the
  artifact lines, as phase 21 does:
  - "When the person runs `model parse` on a requirement that conforms to the language reference, `model` shall
    print one logical form of the requirement and exit successfully." (or r240 kept, if it says this)
  - "If the person runs `model parse` on a requirement that does not conform to the language reference, then
    `model` shall refuse the command and name the requirement."
  - "When the person runs `model logic` on a capability whose requirements conform to the language reference,
    `model` shall exit successfully and print no requirement that it cannot translate." (the words to be settled
    against the parser: the meaning is "every conforming line reaches the check")
  - "While the corpus holds a requirement of this bounded context, when the person runs `model parse` with the
    `--form` option on the requirement, `model` shall print the logical form that the corpus holds for the
    requirement."
- b239's three lines (r174-r176 in b239, renumbered): written with the history construct if it says "unchanged
  since" plainly ("a requirement that `model parse` has parsed since its lexicon last changed"); else as b239 has
  them and listed as a known limit with their coined words (the audit's advice).
- Handlers: none yet beyond what passes; the WIP of `1ec195aa1` (b152) is phase 23's.

### Phase 23: design-model-check, the handlers (b152)

- Reuse `1ec195aa1` (`tests/scenarios/design_model_check_handlers_facts.py`, `design_model_check_worlds.py`, the
  `vocab.py` and `work_queue_world.py` hunks), adapted to phase 22's steps. Build until `unbuilt:` is empty for
  design-model-check. If it does not empty in a few hours, stop at a green commit with the ids left (they are still
  green as xfails); phase 23a takes the rest.

## Phases 24-26: one language, and the release

### Phase 24: the old pipeline removed, the reading (b160)

- The capabilities with no live line (code-research, delivery, formulation, planning, red-green, review,
  role-boundaries, spec-consistency, spec-integration, spec-migration, supervision, work-queue) say codified-2; their
  `## Terms` that no live line uses go.
- b160's line in grammar 4 into design-model-check, with the `language` attribute of phase 20: "If the person runs
  `model check` on a capability whose language is `codified-1`, then `model` shall refuse the command and name
  `migrate upgrade`." `v_p0` refuses a codified-1 file so (test first, in its handler).
- Remove the codified-1 reading: `grammar/Core*.gf`, `Req*.gf`; `scripts/spec_typed.py`, `spec_typed_verbs.py`,
  `spec_typed_def.py`, `spec_facts.py`, `spec_facts_np.py`, `spec_steps_facts.py`, `spec_context_ids.py` and the
  codified-1 branches of `spec_context`, `spec_read`, `spec_language`, `spec_grammar`, `model_spec`, `readiness_bar`,
  `request_lines`, `backlog_lines`; their tests. Every remaining caller reads grammar 4 alone. Rows out of CLAUDE.md's
  module map, rows rewritten where a module's concern narrows.
- G7 now reads grammar 4 alone: its summary must equal phase 23's.

### Phase 25: the old pipeline removed, the steps and the corpus (b160)

- Remove the old step grammar and its reading (`grammar/Steps.gf`, `StepsEng.gf`, `scripts/features_vocab.py`,
  `features_vocab_gf.py`, `features_generate.py`'s codified-1 path, `tests/scenarios/vocab.py`'s grammar-3 matching,
  keeping its U checks and marks), and rename what is left of the `4` modules only if the rename is mechanical
  (otherwise leave names; a rename is not this plan's).
- `grammar/corpus/` keeps only grammar 4: the grammar-3 files (`core.txt`, `<capability>.txt`) go with their tests;
  `core-4.txt`, `time-4.txt`, `refused.txt` (grammar 4's), `spec/` stay.
- `model decisions --check`: a decision whose `enforced_by` names a removed test is rewritten only through `work
  decision` (a new decision superseding it); stop if that seems needed.

### Phase 26: the upgrade step "the controlled language 4" and release 4.0.0 (b161)

- `scripts/migrate_upgrade_cnl4.py`, registered after "verb frames" (design I29, b161's notes): rewrites only the
  mechanical parts (each file's marker; `imports: [cli]`; `(verb)` to `(verb, action)`/`(verb, state)` where decidable)
  and reports, by file and id, everything else b161 lists. Tests first with b161's given block.
- b161's line in grammar 4 into migration-tools, with phase 5's comparison: "While the release of the repository is
  after `3.0.0` and before `4.0.0`, when the person runs `migrate upgrade`, `migrate` shall rewrite `spec/index.md`,
  rewrite every capability and print "the controlled language 4"." (the `rewrite every capability` part plainly, as
  b161 joins them).
- Release: README's 4.0.0 section (what changed, the upgrade step, the known limits by name),
  `.claude-plugin/plugin.json`, `.shop/plugin-version`, migration-tools' version given blocks: 4.0.0.
- `grammar/language.md`'s `## What the language cannot say yet` complete: one subsection a limit, each with its lines
  by id from the reworded spec: #1 construct catalogue (the coined meta-level words left, listed; b124), #8 attribute
  change and negated state, #9 and #10 beyond plain "every" and "each of", #13 counterfactual (the rest phase 4 could
  not carry), #14 ordered choice, #15 frame adjuncts, #16 bounded time and liveness (b127), #17 default value, #18 the
  singletons, b239's words if phase 22 kept them. Every line the corpus traces `Known limit: #n` appears there, and
  the reverse: a test in `test_corpus_spec.py` checks it.

## The review, and what the plan did

- One fresh reviewer reviews the whole branch against this plan, b240's notes and the audit: every retired line
  against its successor's form and the old line's meaning (the corpus traces make this a walk down each file), no
  coined word the plan did not list as a limit, the gate.
- The last implementer (or the session) writes the record of what the plan did with `work record "Grammar 4
  complete: what the plan did" --kind analysis`: each phase's commits, numbers (suite, `model logic`, the profile of
  phase 1), each stop and how it was resumed, and what is left as items (`work idea` for each, in the same turn).
- The session merges the branch to main and closes b240 and the items it folds.
