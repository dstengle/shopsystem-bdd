---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s3
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S3: the facts (one translation per fun) and the context read once

## What changed

- `scripts/spec_facts.py` (new, 258 lines): `translate(vocab, ident, tree)`, `split(ident)`, `define(vocab, tree)`.
  These cover the clause, trigger and verb-phrase funs.
- `scripts/spec_facts_np.py` (new, 162 lines): noun phrases, common nouns and restrictions, choice points, and the
  defined-condition expansion.
- `scripts/spec_context.py` (new, 126 lines): `Statement`, `Context`, `load(root, extra=())`, and the fingerprint
  cache.
- `scripts/spec_logic_vocab.py`: adds `Vocab.def_lits` and `domain(vocab)`. `facts`, `pools` and `guards` are left
  as they were for S7.
- `CLAUDE.md`: adds rows for `spec_facts.py` with `spec_facts_np.py` and for `spec_context.py`. The
  `spec_logic_vocab.py` row now names `domain`.
- `tests/scripts/test_spec_facts.py` (new, 19 tests, cluster and glossary fixtures). The two vocabulary tests are
  ported as they were. The rest assert exact fact strings, one or more per row of design §3. They also test
  `domain` and the context cache.

`spec_logic.py`, `spec_logic_np.py` and `spec_solve.py` are untouched.

## Test runs

- Before the implementation (module moved aside): `test_spec_facts.py` fails with an ImportError on `spec_facts`.
- `timeout 600 python3 -m pytest -q -n 4 tests/scripts/test_spec_facts.py --durations=3`: 19 passed in 0.66 s. The
  slowest test takes 0.04 s.
- `python3 scripts/tools size --limit 300` exits 0.
- `ruff check` passes on the new and changed files.
- The module-map condition of `test_every_script_module_has_a_map_row` was checked inline, without running that file
  (it is in `$SLOW`): no module is missing.
- **Live spec, translation only (no solver):** `spec_context.load` on the live repository gives:
  - 415 statements, 0 refused, 3449 facts, every one of which `clingo.parse_term` reads;
  - no `ValueError`;
  - 6 split statements (23 `disj` facts).

  Facts by predicate: role 951, resp 719, form 432, trig 382, cond 287, ccond 192, crel 115, every 77, orel 62,
  named 59, oattr 58, set 37, disj 23, feat 18, uses 10, rnone 8, nouse 8, only 7, none 2, count 1, ocond 1.

## Decisions the plan or design left open

1. **`disj(R#k, R)`.** Each split's facts start with `disj("s#r5#1","s#r5").`, naming the split and the requirement
   it comes from. The design writes `disj(R,K)`, and the plan says only "naming the split". `split()` maps
   `R#n` back to R, U ids included (`U1#2` → `U1`).
2. **Object restrictions beyond `oattr`/`orel`.**
   - A negated value on a response's object is `onot(R,V,A,Val)`.
   - A condition on a response's object is `ocond(R,V,C,Pol)`. U2's "a resource that is not free" needs it.
   - The design's `oattr/4` and `orel/4` are kept for positive values and relations.
3. **`no K` as a relation argument** ("a result that gives no question", 8 in the live spec) is
   `rnone(R,Rel,X,Y)`, with the `no` side written `kind(K)`. The design names only `none` and `cnone`.
   - The restrictions of the `no` noun phrase's own noun are left out, as for `none` and `cnone`. Leaving them out
     makes the `none` stronger, so it only blocks more unifications: sound for clashes, and incomplete.
   - `no K is not v`, `no K is not C` and `no K holds R` raise `ValueError`. The live spec has none of them.
4. **`every(R,V)`** comes only from an `every` or plural noun phrase in a response's object or subject. In a
   condition ("research stages for an initiative are `waiting`"), a plural is an ordinary role, so S6 does not make
   a contrast for a condition role.
5. **`count(R,Res,N)`:** N is the integer for `CountNum` and the code string for `CountCode`
   (`count("U1",s_worker_slot,"`workers`")`).
6. **`HoldAtMost`, `uses` and `only` still take a conjunct number I**, so I stays the spoken conjunct order.
   `Hold` is `resp(R,I,Pol,hold(Res),D,none)`.
7. **A `Named` noun phrase** is a role with `role(R,V,K)` and `named(R,V,"`code`")`, and it binds its kind for later
   anaphora.
8. **A defined condition's expansion** walks the stored `Def` clause, with the definition's kind bound to the role
   and nothing else bound, so "the K" inside a definition never reaches the requirement's roles. A guard stops a
   definition from expanding itself. Inside an object restriction, the expansion stays in object facts.
9. **`Vocab.def_lits[cid]`** holds `(kind id, Def clause tree)`: the literals as a tree, translated where they are
   used. `define` also calls `vocab.define(cid)`, so the old `facts()` stays consistent until S7.
10. **Statement ids and groups.** A statement's id is `<cap>#<rid>`, and a U's id is bare (`U1`).
    `Statement.group` is the full `<cap>#<gid>`. `Context.refused` and `Context.facts` are keyed by statement id.
    A split requirement's facts (all its `R#n`) sit together under its one id.
11. **The cache fingerprint** also covers the plugin's `grammar/*.gf`, because a grammar edit changes the parses.

## For the gate and the next tasks

- **Speed: live context load is about 5.8 s, and parsing is most of it.**
  - `spec_grammar.parse` re-reads the lexicon three times per line and regenerates the GF sources per line. Without
    help, the load took 16.6 s.
  - `spec_context` memoises `spec_lexicon.read` and `spec_grammar.sources` by root, for the duration of one read
    only (`_once`), which brings the load to 5.8 s. `spec_grammar.py` is not edited, because S1 owns its `sources`
    lines.
  - The memo passes through any call with extra arguments, so S1's `sources(root, lex)` still works.
  - The remaining floor is pgf parsing itself, about 5 s for 533 parses.
  - Design §2's target of `model logic` under 2 s on the live spec is therefore not reachable from the context alone.
    It needs a cache of parse trees across processes, keyed by grammar sha and line. That falls to S5, S8 or S12.
- **For S4:** the facts carry `onot`, `ocond`, `rnone` and `named` beyond the design's table, and `disj` has the
  shape `disj(Split,Base)`. `#defined` lines for them keep `check.lp` free of warnings, whether or not it reads them.
- **For S6:**
  - Role order follows emission. Within a noun phrase, the role comes first, then its noun's restrictions, then any
    nested role.
  - A positive set gives `set/5` before its `resp`.
  - `ccond` of a defined condition is followed by the definition's `cond`/`crel` facts (r1: `ccond c_open` and then
    two `neg` conds).
