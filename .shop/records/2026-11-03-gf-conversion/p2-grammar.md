---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-p2-grammar
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# P2: the requirement grammar as built

What package P2 of `plan.md` built (design §9, §10.1, §11.3, §14.2), the figures the plan asks for, and the calls
the builder made where design §17 leaves them open.

## Figures (plan P2, design §18.31)

Measured with GF 3.12.0 (`$SHOPSYSTEM_GF` = the spike's `gfc`) and pgf 1.1, on the fixture glossary
`tests/scripts/fixtures/glossary/` (DOM §1–§8: 153 term entries, of them 22 actors, 55 kinds, 12 attributes,
25 relations, 28 events, 5 resources, 6 conditions).

| figure | value |
|---|---|
| generated sources | `Typed.gf` 571 lines (about 500 fun declarations), `TypedEng.gf` 1054 lines, `Lex*.gf` 58 lines each |
| cold compile of the fixture's `Req` grammar (empty cache, three runs) | 0.16–0.18 s |
| corpus lines (19 capability files, `universal.txt`) | 182, every one with exactly one tree after the guard |
| corpus lines with more than one tree **before** the guard | 166 of 182 (most trees on one line: 57) |

The pre-guard trees come from two sources only. A `String` literal slot (`CodeLit`, `QuotedLit`) reads any token,
so every lexicon word or plain word in an NP slot has a literal reading too; and "it" or "its" is read once in every
kind. The guard (§9.3, §9.4) drops all of them. No corpus line has two trees left that differ in structure. Ambiguity
that is English's own, such as "a request line in a request that is `accepted`" (`accepted` is a value of both
kinds), is left as two trees and counted (`ambiguous: 2 trees`), and the corpus does not use it.

`spec_grammar.LIMIT` (2000) caps the trees read from one parse before the guard.

## The modules

- `grammar/Core.gf`, `CoreEng.gf` (hand-written, **not** in P2's owned list): the categories every grammar shares,
  with their lincats and the opers the generated English uses. `Lex` extends `Core`, `Typed` extends `Lex`, and `Req`
  extends `Typed`. The design's sketch put the core categories in `Req`. They cannot be there, because `Typed`'s funs
  return `Cond`, `Trig`, `VP` and `NP`, and `Typed` sits below `Req`. `Steps` (P7) extends `Typed` the same way.
- `grammar/Req.gf`, `ReqEng.gf`: the six EARS forms and the slots tied to no kind.
- `scripts/spec_typed.py` (new, **not** in P2's owned list): writes `Lex.gf`/`LexEng.gf`/`Typed.gf`/`TypedEng.gf`
  from a lexicon. It is a module of its own because `spec_grammar` would otherwise exceed 300 lines.
- `scripts/spec_lexicon.py`: the one reader of term entries, `ident`, `Lexicon.ids()` (collisions numbered in
  sorted key order), `problems` (v_t4–v_t6) and `words`.
- `scripts/spec_grammar.py`: `gf_binary`, `tokenise`, `normalise`, `sources`, `load`, `parse` → `Parse(tree, refusal,
  trees, before)`, `linearise` and `hint`.
- `scripts/spec_tree.py`: `guard`, `normal`, `parts`, `logic_only`, `nodes` and `show`.

## Calls made (design §17)

1. **Typed fun names.** For a kind `k`: `k`, `k_An|Every|The|No|AtMostOne|One|Pl|Its : k_CN -> k_NP`,
   `k_Named : Code -> k_NP` ("the initiative `i1`"), `k_It`, `k_toNP`, `k_NumberOf`. For an attribute `t` of a kind:
   value funs `v_…`, `t_One`/`t_More` (value lists, "`a`, `b` or `c`"), `t_ThatIs`, `t_ThatIsNot`, `t_Whose`,
   `t_WhoseNot`, `t_Pre` ("an `integrate` round"), `t_Is`, `t_IsNot`, `t_Becomes`, `t_Set`, `t_Of` ("the status of
   X", "its status"). For a condition `c`: `c_Pre` ("an open initiative"), `c_ThatIs`, `c_ThatIsNot`, `c_Is`,
   `c_IsNot`. A relation `r` gives `r : k1_CN -> k2_NP -> k1_CN`. Each attribute spelling gives an untyped
   `n_<word> : NP` ("a status").
2. **Relations.** A relation whose last word is a preposition (under, of, for, on, in, with, outside, by, …)
   reads "a work-item under p1". Any other relation is a verb: "an initiative that fulfils the request".
3. **Spans as one token.** GF's lexer splits on spaces, so inside a backticked or quoted span a space is passed as
   U+E000 (`spec_typed.PLACEHOLDER`). The generated lins of multi-word backticked terms use it too, and
   `linearise` turns it back into a space.
4. **The first word.** The grammar writes every form in lower case. `tokenise` lowers the first word when it is
   capitalised, and `linearise`/`normalise` raise it again. "a"/"an" is GF's `pre`. The C runtime does not check
   `pre` when it parses, so "a initiative" parses, but it linearises as "an initiative" and fails the corpus check.
5. **"its X".** `attrOf` does not speak its noun phrase when that is "it". The parse then has a metavariable there,
   and `spec_grammar._tree` fills it with that slot kind's `It`, which is the only noun phrase that can be unspoken.
6. **Guards beyond §9.3/§9.4.** A tree with a gap is dropped. `DoTo`'s second object may not be a bare code or
   quote, because "use the interpreter `x`" is the named interpreter and not two objects. A guard refusal reports a
   structural reason ("it" with no antecedent, a repeated member) before a literal one.
7. **Reserved verbs.** `run`, `print`, `hold`, `exit`, `become`, `set` and `be` are spelled by the core. An event of
   that name is v_t6, because it would make two trees of one line.
8. **v_t6** is read as two entries of one category, spelling and kinds. An actor spelled as a determiner plus a kind
   word ("a session" next to the kind session) is also v_t6, because it makes the subject ambiguous.
9. **Core funs added by the corpus (growth rule §9.5).** `IsRun` ("`tools size` is run"), `Undergoes` ("a command is
   refused"), `HappensI`, `RefuseErr` ("exit with an error naming X and change nothing", about 48 lines today),
   `CommitPush` ("commit X and push the commit", about 34), `ChangeNothing`, `Only`, `HoldsA`/`HoldA` ("holds a worker
   slot"), and `Cmd` (`CmdCode`, `CmdActor`), so "runs `work run`" reads the actor and never a literal. `PrintCode`,
   `Write`, `Refuse` and `Commit` from the sketch were dropped: they duplicate `Print (OneNP (CodeNP …))` and the
   lexicon's events. `NotC` and `And2` became `IsNot` and a right-recursive `CondOne`/`CondAnd`, so "A and B and C"
   has one tree.

## The universal conditions as worded (`grammar/corpus/universal.txt`)

P3 writes `spec/universal.md` and may reword these. Each one parses in the fixture grammar. Wording changes from
DOM §7:

- U3 is an `If … then` statement ("If a command is refused, then it shall exit with an error naming the reason and
  change nothing.") and not a `Where` statement, because its trigger is an event.
- U4 is one statement: "`work` shall commit every transition and push the commit."
- U5 is "A session shall not write a status." The grammar has no "only X shall".
- U7 is narrowed to "A worker shall change only files in its worktree." The stage directory needs a coordination
  of two kinds' noun phrases, which the grammar lacks. A U7b, or a `file in a stage directory` relation, would put
  it back.
- U9 is "A delivery shall change no initiative directory of an initiative outside the delivery."
- U10 is "When `work run` starts a stage, `work run` shall give the stage only a brief."

## For the packages that follow

- **P3:** the fixture glossary shows the entry forms the reader takes, including continuation lines indented under
  a bullet. `spec_lexicon.problems` gives v_t4–v_t6 as `(code, term, message)`.
- **P5:** `Parse.tree` is set only when exactly one tree is left. `refusal` is `does not parse at <token> (token i
  of n)`, `the line ends before its sentence does`, `refused: <guard reason>` or `ambiguous: n trees`. `before`
  counts the trees before the guard. `spec_tree.parts(tree)` gives the clauses for v15k, after `normal`.
- **P7:** `load(root, "Steps")` compiles `grammar/StepsEng.gf` once it exists. `sources()` already takes every
  `grammar/*.gf`. The typed Steps funs (`GivenK_A` …) are not generated yet: `spec_typed.modules` writes only the
  Req slots, and P7 adds the Steps templates (a `spec_typed` change, or a module beside it).
- **Everyone:** a test that compiles or parses calls `toolchain.require()`. Without `$SHOPSYSTEM_GF`, the P1 install,
  or a `gf` on PATH, those tests fail and say to run `python3 scripts/tools install`. They are never skipped.
