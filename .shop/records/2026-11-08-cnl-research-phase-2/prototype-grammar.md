# A throwaway prototype grammar for the candidate lines

Phase 2 of b112's research (`.shop/backlog/b112.md`). This is a spike: an application grammar over the GF Resource
Grammar Library (RGL). It parses the 27 candidate lines of `sample-rewrites.md`, and its purpose is to show what a
redesigned CNL costs and where it gets hard. Nothing in the repository was changed except this file. The grammar,
generator and scripts are in the session scratchpad,
`/tmp/claude-1000/-home-vscode-shopsystem-bdd/72e23fa5-6dee-49f3-a1d1-7e79096a0501/scratchpad/b112/proto/`. It is
built with the repository's gf 3.12 and pgf 1.1, against gf-rgl `20250812` (phase 1's spike download, reused).

## 1. Summary

- **All 27 candidates parse**: 26 to exactly one tree and 1 to two trees (telemetry#r1, coordination scope, §4.1).
  Every tree linearises back to the input word for word. A whole candidate parses in 0.2-6 ms.
- **17 bad sentences are all refused**: agreement errors (4), a noun of the wrong kind in a frame, row, whose or
  coordination slot (5), a value of the wrong kind or attribute (3), agentless passives (2), coined adjectives with no
  definition (2), and an untyped code (`` `spec/index.md` ``) where a kind is required (1). Determiner agreement
  ("every tasks", "tasks ... is") was checked separately and is refused too.
- **Cost.** The hand-written core is 28 funs. A 300-line Python generator emits **791 typed funs** (250 categories)
  from a vocabulary of 50 kinds, 27 relation rows, 2 role nouns, 25 verb frames, 7 attributes and 1 condition.
  Determiners are 43% of the generated funs. Moving them into the core as one `Det` category brings the total to
  **504 generated funs**, with the same results. A clean compile takes 0.55-0.7 s and the PGF is 329 KB. At 4x the
  vocabulary, roughly this repository's size (166 kinds, 43 verbs, 34 attributes), it takes 2.1-2.3 s, 1.1-1.2 MB
  and 8-9 ms per line.
- **What typing buys.** Typing by kind settles most attachment questions on its own. Restricting a noun modifier
  ("of", "on", "in") to a bare noun head removes the rest. With modifiers allowed on any common noun, 3 candidates
  have two trees instead of 1.
- **What it does not buy:** scope (an indefinite under "no", accessibility of While nouns in the response), the
  antecedent of "its" and of a definite with no antecedent, and the implicit comparison in "a different name". The
  tree keeps enough structure for a semantics layer to decide these (§6), but the grammar does not decide them.

## 2. What was built

| File (in `proto/`) | Lines | What |
|---|---|---|
| `gen.py` | 306 | the vocabulary (about 70 lines of Python data) and the generator writing `Lex.gf` and `LexEng.gf`; it also runs the experiments: `SCALE=n` (n copies of the vocabulary), `CN_OF=1` (modifier on any CN), `DETCORE=1` (one core `Det` category) |
| `Proto.gf`, `ProtoEng.gf` | 34, 36 | the hand-written core (appendix A) |
| `Lex.gf`, `LexEng.gf` | 797, 1046 | generated |
| `parse.py` | 94 | tokenise, parse with a literal callback, count trees, linearise and compare, time |
| `build.sh` | 5 | compile against the spike's built RGL |
| `candidates.tsv`, `bad.tsv`, `good.tsv`, `trees.txt` | | inputs and the trees of every candidate |

### 2.1 Shape of the abstract syntax

The repository's idea is kept: **one GF category per kind, so a noun of the wrong kind does not parse**. The
categories are layered as follows:

| Layer | Categories (per kind K unless noted) | Note |
|---|---|---|
| noun | `K_N` (lexical), `K_CN` (with modifiers, relative clauses) | a modifier takes `K_N` as its head, so it cannot stack to the left (§3.3) |
| noun phrase | `K_NP0` (simple: determiner + CN, a name, a literal), `K_NP` (what a slot takes) | **kind-of coercion** `Up_K_S : K_NP0 -> S_NP0`, one per parent edge; lists and "only" make `K_NP` from `K_NP0`, so a coordinated NP is never coerced and coercion never multiplies trees |
| lists | `K_List` for slot kinds only (kinds that are an object of some frame or row) | RGL `ListNP`, "and"/"or" |
| verb phrase | `S_VP` per subject kind of a **state** verb; `S_Act` per subject kind of an **action** verb | a verb fun is typed by its frame: `cite_commit_item : item_NP -> commit_VP`. States go in While and in relative clauses, actions go in When/If and in responses. This split is new vocabulary data (§5) |
| clause | `Atom` (state clause), `Trig` (event clause), `Cond` (`Pol` + `Atom`, "and") | polarity is one argument `Pol` (`PPos`/`PNeg`), so no `*Not` funs |
| attribute | `K_A_Val` (values), `K_A_Pred` ("is `v`", "after `v`", ...), `K_A_ANP` ("the status of X") | a status value of the wrong kind is refused |
| response | `Shall : agent_NP -> ActList -> Resp`, `ActP : Pol -> agent_Act -> ActItem` | "shall print the comment and not write the comment" is one list of polarised items |

The generated fun templates, with counts for the 27-line vocabulary:

| Template | Example | Count |
|---|---|---|
| noun (+ aliases) | `commit_n = mkN "commit"`, `request_comment_n2` "comment" | 50 |
| N to CN | `commit_UseN` | 49 |
| determiners a, the, every, no, one, plural, its | `commit_No cn = mkNP no_Quant cn` | 343 |
| named instance | `` tool_work ``, `hook_the_sessionstart_hook` | 8 |
| NP0 to NP | `commit_Simple` | 52 |
| kind-of coercion | `Up_untracked_file_file` | 51 |
| only, list base/cons, and, or (slot kinds) | `thing_And` | 90 |
| predication per subject kind | `commit_Pred : commit_NP -> commit_VP -> Atom` | 10 |
| event per subject kind | `batch_Event : batch_NP -> batch_Act -> Trig` | 2 |
| subject relative clause per kind and super-kind | `measurement_Rel_measurement : Pol -> measurement_CN -> measurement_VP -> measurement_CN` | 12 |
| row: noun modifier (of/on/in) | `commit_on_branch : commit_N -> branch_NP -> commit_CN` | 22 |
| row: copula (on/in) | `repository_on_branch_Is : repository_NP -> branch_NP -> Atom` | 3 |
| row: whose | `verb_Whose_glossary_entry_glossary_entry : Pol -> verb_CN -> glossary_entry_VP -> verb_CN` | 8 |
| row: has/holds | `commit_holds_text : text_NP -> commit_VP` | 5 |
| role row (bare, of, whose) | `upstream_bare : bounded_context_CN`, `upstream_branch_of_branch` | 5 |
| verb frame (with an optional adjunct preposition) | `refuse_agent_command_for_reason : command_NP -> reason_NP -> agent_Act` | 25 |
| attribute (values, is, after/before/and, direct, relative, of, holds, set, as a thing, has a different) | `batch_status_Set : batch_status_ANP -> batch_status_Val -> agent_Act` | 54 |
| condition (a defined adjective) | `initiative_open_Is`, `initiative_open_Rel` | 2 |
| **total generated** | | **791** |

That is about 40 templates. **The semantics would be written once per template, not once per fun.** For example,
`K_A` is always "a new discourse referent of kind K". Today `spec_facts` translates the grammar fun by fun.

## 3. Results on the 27 candidates

### 3.1 Per line

Tokens are counted after the tokeniser has joined each backquoted or quoted span into one token. The time is the
median of 5 parses with the Python `pgf` runtime. "Raw" is the number of trees GF returns before the literal filter
(§4.4).

| Line | Tokens | Trees | Raw | ms | Round trip |
|---|---|---|---|---|---|
| requests#r33 | 29 | 1 | 1 | 3.7 | same |
| requests#r38 | 40 | 1 | 1 | 5.6 | same |
| requests#r6 | 24 | 1 | 1 | 4.7 | same |
| requests#r24 | 33 | 1 | 1 | 5.4 | same |
| batches#r8 | 42 | 1 | 1 | 3.6 | same |
| batches#r13 | 39 | 1 | 1 | 5.9 | same |
| batches#r17 | 29 | 1 | 1 | 2.5 | same |
| batches#r16 | 21 | 1 | 1 | 1.2 | same |
| backlog#r20 | 31 | 1 | 1 | 3.7 | same |
| backlog#r21 | 39 | 1 | 1 | 4.9 | same (but see §4.3) |
| migration-tools#r19 | 39 | 1 | 2 | 3.6 | same |
| migration-tools#r14 | 23 | 1 | 2 | 3.3 | same |
| migration-tools#r25 | 30 | 1 | 8 | 4.5 | same |
| migration-tools#r8 | 36 | 1 | 1 | 5.8 | same |
| migration-tools#r21 | 32 | 1 | 2 | 2.9 | same |
| feature-file-tools#r3 | 37 | 1 | 1 | 4.8 | same |
| feature-file-tools#r14 | 27 | 1 | 1 | 1.2 | same |
| trials#r1 | 15 | 1 | 1 | 1.7 | same |
| trials#r2 | 9 | 1 | 1 | 0.2 | same |
| trials#r4 | 22 | 1 | 1 | 2.3 | same |
| design-model-check#r60 | 26 | 1 | 1 | 2.9 | same |
| design-model-check#r69 | 19 | 1 | 1 | 1.8 | same |
| conversation#r2 | 17 | 1 | 1 | 1.0 | same |
| telemetry#r1 | 33 | **2** | 9 | 5.9 | same, both trees |
| universal#U4 | 16 | 1 | 1 | 1.8 | same |
| universal#U7 | 10 | 1 | 1 | 1.2 | same |
| universal#U11 | 25 | 1 | 1 | 2.7 | same |

**No candidate needed rewording to parse.** Two lines needed a vocabulary row that `sample-rewrites.md` had not
listed: target | of | trial (trials#r4, "the target of the trial") beside target | of | tool ("its target",
trials#r2), and a second frame of remove with a "from" place (batches#r17). Both are vocabulary, not grammar.

An example tree (batches#r13, with the `_Simple`/`Up_` wrappers abbreviated as `·`):

```
WhileIf (CondP PPos (commit_Pred ·(commit_A (commit_on_branch commit_n
            ·(branch_The (branch_of_task branch_n ·(task_A (task_of_batch task_n ·(batch_A (batch_UseN batch_n)))))))))
          (cite_commit_item ·(item_No (item_UseN item_n)))))
        (RunsOn ·(person_The ·) (CmdCode (CodeLit "`work batch review`")) ·(batch_The ·))
        (OneResp (Shall ·tool_work (AndAct (ActP PPos (ExitErr ·(commit_The ·))) (OneAct (ActP PPos (change_agent_thing ·Nothing))))))
```

### 3.2 Bad sentences (all refused)

| Case | Sentence | Refused at |
|---|---|---|
| agreement, subject | When the person **run** `work idea`, ... | "run" |
| agreement, copula | While every task of the batch **are** `done`, ... | "are" |
| agreement after shall | `work` shall **prints** the comment. | "prints" |
| agreement, negation | While a request line **do not** conform to the comment schema, ... | "do" |
| determiner agreement (extra, `det.tsv`) | While every **tasks** of the batch is `done` / While tasks of the batch **is** ... | "tasks" / "is" |
| wrong kind, subject of a frame | When **a session parks** the item, ... (park: batch parks item) | "parks" |
| wrong kind, object of a frame | While a commit cites no **batch**, ... | "batch" |
| wrong kind, object and row | ... `work` shall publish a **commit** of the batch. | "commit" |
| wrong kind, whose | ... a verb whose **frame** has no glossary entry ... | "frame" |
| wrong kind in a coordination | ... whose text has a tag and **a branch**, `features` ... | "`features`" (see below) |
| status value of another kind | While a batch is **`done`**, ... (done is a task's) | "`done`" |
| value of another attribute | While the plugin version of a repository is **`own`**, ... | "`own`" |
| set to a value of another kind | ... set the status of the batch to **`done`**. | "`done`" |
| agentless passive | While the comment **is written**, ... / While a request comment **is printed**, ... | "is" |
| coined adjective (undefined) | While a comment **is unreadable**, ... / While an initiative **is idle**, ... | "is" / "idle" |
| untyped code where a kind is needed | `work` shall publish **`spec/index.md`**. | the code |

For contrast, the defined adjective survives: "While no initiative of the repository is open, `migrate` shall exit
successfully." parses, because *open* is a condition entry of initiative. "When sessions run `work sync`, `work` shall
print every request comment." parses, with agreement handled inside the frame.

**Where a refusal is reported.** GF reports the first token at which no continuation exists, and that can come after
the fault. In the coordination case, "a tag and a branch" is accepted as far as the comma, because "and a branch
..." could still begin a second condition ("... and a branch has a different name"). The repository's refusal
messages, which say which frame a line breaks (`spec_frames.refusal`), would have to be rebuilt on the new
categories. GF's completion (`complete`) could list what may follow at the point of refusal.

**"a" or "an".** The RGL's `pre` choice of "a"/"an" is lenient when parsing: "the text of a untracked file" parses,
and linearises back as "an untracked file". The round-trip check catches this, and a linter could rewrite the line.

### 3.3 Two designs measured

| Variant | Generated funs | Candidates: 1 tree / 2 trees | Bad refused | Clean compile | PGF |
|---|---|---|---|---|---|
| as built: modifier on `K_N`, 7 determiner funs per kind | 791 | 26 / 1 | 17/17 | 0.55-0.7 s | 329 KB |
| modifier on any `K_CN` (`CN_OF=1`) | 791 | 24 / 3 | | | |
| one core `Det` category, `K_Det : Det -> K_CN -> K_NP0` (`DETCORE=1`) | 504 | 26 / 1 | 17/17 | 0.65 s | 297 KB |

With modifiers allowed on any CN, batches#r13 gets a second tree, "[the branch of a task] of a batch". It is well
typed, since branch | of | batch is a row. trials#r4 also gets a second tree, "[a measurement of the trial that
names the target] of the trial". Restricting a modifier's head to a bare noun (right-branching only) loses nothing
that the 27 lines use.

### 3.4 Scale

`SCALE=n` copies the whole vocabulary n times under new nouns ("x2 commit"), keeping the verb words, so a verb
also has n frames. All runs give the same results on the 27 lines.

| Vocabulary | Generated funs (7 dets / core Det) | Compile, clean (s) | PGF | Mean / max parse per line |
|---|---|---|---|---|
| 1x (50 kinds, 25 frames) | 791 / 504 | 0.55-0.7 | 329 KB / 297 KB | 2.5 / 5.9 ms |
| 2x | 1,562 / - | 1.4 | 627 KB | 4.4 / 7.9 ms |
| 4x (about this repository's size) | 3,104 / 1,935 | 2.3 / 2.1 | 1.2 MB / 1.1 MB | 8.8 / 15.7 ms (7.8 / 17.2) |
| 8x | 6,188 / 3,843 | 4.6 / 4.0 | 2.4 MB / 2.1 MB | 18 / 32 ms |
| *repository today (phase 1)* | *4,841* | *0.7* | *766 KB* | |

Compile time and PGF size grow linearly. Parse time grows with the number of categories, about 2 ms per line for
each additional copy of the vocabulary. The RGL's own modules are compiled once (`.gfo` cached) and are not counted.
A full port would probably compile in a few seconds per glossary change. The repository's SHA-keyed PGF cache makes
that a one-off per change.

## 4. The hard cases

### 4.1 Coordination scope (telemetry#r1): the one ambiguity

"`measure` shall write a measurement of the batch that includes "wall time", "session time", "tokens" and "cost by
role"." has two trees:

1. write [a measurement ... that includes ("wall time", "session time", "tokens" and "cost by role")]
2. write ([a measurement ... that includes "wall time"], "session time", "tokens" and "cost by role")

Typing cannot separate them, because both lists are lists of things that `write` takes. Two remedies:

- **A post-parse guard** in the style the repository already uses: "a relative clause runs to the end of its
  clause". In tree terms, a list conjunct that ends in a relative clause must be the last conjunct, so keep reading
  1. This is cheap, but it is a rule that authors have to learn.
- **In the grammar**: split NP0 into closed and open (ending in a relative clause), and let only closed NPs stand
  before the last conjunct. That doubles the NP and CN categories of every slot kind, at roughly +20% funs. I did
  not build it.

I would take the guard. The same scope question will come back whenever a relative clause and a list meet.

### 4.2 "its" and definites with no antecedent

"its upstream", "its target" and "its worktree" parse as `K_Its` on the head noun's kind. **The tree does not say
whose.** The possessor has to be resolved in semantics, as the nearest antecedent whose kind has a row to the head
noun:

- request line | upstream | bounded context
- target | of | tool, with `trial-runner` the antecedent
- worktree | of | worker

This is unambiguous when the head noun has one row. It is ambiguous when the head has two: branch | of | task and
branch | of | batch would make "its branch" ambiguous, but no candidate says that. The alternative is a per-row `Its`
fun, `upstream_its_request_line`. That puts the possessor's kind in the tree, but it gives two trees for "its branch"
and grows the grammar per row. Either way the antecedent itself is chosen in semantics.

Several definites have no antecedent in their line: "the session" in conversation#r2, "the comment schema" and "the
git directory" (singletons, which is fine), and "the commit" in U4. In U4, "the commit" is the result of the action
"commit the transition", not a noun mentioned earlier. The grammar parses all of these. Telling a singleton artifact
("the comment schema") from a missing antecedent needs a vocabulary mark ("one per bounded context"), which the
sample's vocabulary notes ask for anyway.

### 4.3 "a different name" (backlog#r21): parses, but clumsy

"a branch whose upstream branch has a different name" parses through a generated `branch_name_HasDifferent :
branch_VP`. "different" is relational, though: different from the outer branch. The tree has no argument for the
comparison, so semantics must supply "the branch the whose-clause hangs on". I supported it by adding one template
per value-less attribute, rather than adding a general comparison construct.

My reword, not built: "While a repository is on a branch whose name is not the name of its upstream branch, ...".
It needs one general atom, `K_A_ANP is (not) K_A_ANP`, which fixes the comparison in the tree. It adds four words.

### 4.4 Literals

Commands, codes and quoted strings are GF `String` literals read by a callback, as in `spec_grammar`. The pgf
Python runtime calls one callback for every `String` slot, so a backquoted token can be read as `Quoted` and a quoted
one as `Code`. That is where the raw counts of 2-9 in §3.1 come from (migration-tools#r25: 8 raw trees, 1 after the
filter). `parse.py` drops trees whose literal kind does not match its quote mark. A real implementation should make
the two literal kinds distinct before GF sees them: the tokeniser can tag them, or there can be one literal category
with the kind decided after parsing.

A code carries no kind, so `` `spec/index.md` `` can only fill a `thing` slot. migration-tools#r25's "rewrite
`spec/index.md`" works only because rewrite's object is `thing`. Typed codes (a file path as a file) would need a
vocabulary entry per code, or a "code of kind K" form ("the file `spec/index.md`").

### 4.5 Scope inside While (migration-tools#r8)

"While no commit holds the text of an untracked file, if ..., then `migrate` shall exit with an error naming the
untracked file ..." parses to one tree, with `untracked_file_A` inside `commit_No`. The surface order puts the
indefinite under "no". The response's "the untracked file" needs the file outside the negation. The tree records the
structure but not the scope. Semantics needs a fixed rule (§6.3), and a writing rule should say it.

### 4.6 Things the candidates did not need, and the grammar lacks

- object relative clauses ("a requirement that an item proposes"). This needs one more fun per state frame using
  RGL `mkClSlash`; it is cheap to generate.
- plural definites ("the branches of a task"): add `ThePl` to the determiners.
- "or" between conditions, "may", "only after", counts beyond "one", and comparison between attribute NPs.
- events as triggers from state verbs ("When a commit cites an item"): refused by design, since a state verb is not
  an event. Whether "becomes" should exist is a question for the semantics strand.

## 5. RGL defaults overridden, and gotchas

| # | Default | What I did |
|---|---|---|
| 1 | contracted negation ("doesn't") | `ExtraEng.UncNeg` as `PNeg` |
| 2 | no "shall" in the RGL; `auxVV` gives only the present | responses are built as strings: subject + "shall" + `ResEng.infVP VVAux vp ... polarity` per item, so "shall print X and not write Y" is one coordinated infinitive list. "shall" agrees with nothing, which is right for English |
| 3 | **a `Pol` argument whose string field is unused becomes a metavariable `?` in the parse tree** | the first build dropped the negation in "and not write the comment": the tree said `ActP ?` and linearised positive. The fix is to put `p.s` (empty) into the linearisation. **A round-trip check found it.** A real implementation must run the round trip on its corpus |
| 4 | `mkPN` on a literal glues "'s" at run time (a compile error) | literal NPs as raw records `{s = \\_ => s ; a = P3 Sg}` |
| 5 | multi-word noun strings do not parse (one token with a space) | `compoundN` for every compound ("plugin version file") |
| 6 | attribute values have no category | values as adverbs (`mkAdv "`own`"`), so "is `own`", "is after `1.0.0` and before `3.0.0`" come from `mkVP Adv` and `mkAdv and_Conj`. It works, but it is a hack |
| 7 | irregular verbs | present tense only, which the lines use; forms given where needed (`run`, `set`) |
| 8 | lists use a bound comma (`SOFT_BIND`) | the tokeniser splits commas and the parser accepts "a , b"; output is "a, b", normalised before comparing |
| 9 | name clashes (`mkQuant`, `mkAdv` in both `SyntaxEng` and `ParadigmsEng`) | qualified names |
| 10 | `which_RP` is "that" | kept: "that" is the house style |
| 11 | "a"/"an" lenient in parsing (§3.2) | caught by the round trip |
| 12 | sentence-initial capital | lowered by the tokeniser and raised on output, as `spec_grammar` does |

## 6. Logical forms from three trees

These are sketches. The point is that each generated template maps to one condition in a discourse representation
structure (DRS), and the EARS form decides the layout:

- `While`/`When`/`If` give the left box of a conditional, an obligation over the right box. Nouns introduced on the
  left are accessible on the right, so "the comment" resolves.
- `CondP PNeg` is a negated box. `K_A` is a new referent, `K_The` a resolved one, `K_No` a negated box, and
  `K_Every` a duplex condition.
- A state verb is a fluent that holds at the trigger's time. An action verb is an event.

### 6.1 requests#r33

Tree (wrappers removed): `WhileWhen (CondP PNeg (text_Pred (request_comment_A ·) (conform_text_artifact
(comment_schema_The ·)))) (Runs (session_A ·) "work sync") (Shall work (AndAct (ActP PPos (print (request_comment_The
n2))) (OneAct (ActP PNeg (write (request_comment_The n2))))))`

```
[c, k, s, e | request_comment(c), comment_schema(k), session(s),
              ¬[ | conforms_to(c, k)],                         -- While, CondP PNeg: a fluent false at t
              e: run(s, "work sync")]                          -- When: the trigger event at t
  ⇒ O[ e1 | e1: print(work, c) ]                               -- ActP PPos: obligation
    O¬[ e2 | e2: write(work, c) ]                              -- ActP PNeg: prohibition
```

Event calculus: `¬HoldsAt(conforms_to(c,k), t) ∧ Happens(run(s,"work sync"), t) → Happens(print(work,c), t+) ∧
¬∃e Happens(write(work,c), t+)`. Gherkin: Given a request comment that does not conform to the comment schema; When
a session runs `work sync`; Then `work` prints the comment; And `work` does not write the comment. `request_comment_n2`
("comment") is the same kind as `request_comment_n`, so "the comment" resolves to c with no special rule.

### 6.2 batches#r8 (every, attribute set)

Tree: `WhileWhen (CondAnd (CondP PPos (batch_status_Direct (batch_A ·) building)) (CondP PPos (task_status_Direct
(task_Every (task_of_batch task_n (batch_The ·))) done))) (RunsOn (person_The ·) "work batch review" (batch_The ·))
(Shall work (AndAct (ActP PPos (publish (pull_request_A (pull_request_of_batch pull_request_n (batch_The ·)))))
(OneAct (ActP PPos (batch_status_Set (batch_status_Of (batch_The ·)) in-review)))))`

```
[b, p, e | batch(b), status(b) = building,
           [t | task(t), of(t, b)] ⇒ [ | status(t) = done],      -- task_Every over task_of_batch: duplex
           person(p), e: run(p, "work batch review", on: b)]
  ⇒ O[ r, e1 | pull_request(r), of(r, b), e1: publish(work, r) ]
    O[ | status(b)@after = in-review ]                          -- _Set: a transition of the attribute fluent
```

`batch_status_Set` is the template that carries the change of state: before is `building`, after is `in-review`.
This is the two-state reading `check.lp` already uses, but it comes from a template rather than a hand-written
translation of each fun.

### 6.3 migration-tools#r8 (no, and the indefinite's scope)

Tree: `WhileIf (CondP PPos (commit_Pred (commit_No ·) (commit_holds_text (text_The (text_of_file text_n
(untracked_file_A ·)))))) (RunsOn (person_The ·) "migrate run" (bounded_context_A ·)) (Shall migrate (AndAct (ActP
PPos (ExitErr (untracked_file_The ·))) (OneAct (ActP PPos (change Nothing)))))`

The surface reading puts f inside the negation:

```
¬[ c, f | commit(c), untracked_file(f), holds(c, text_of(f)) ]
```

That leaves "the untracked file" in the response with no antecedent. The intended reading raises f to the
condition box:

```
[f, x, p, e | untracked_file(f), ¬[ c | commit(c), holds(c, text_of(f)) ],
              bounded_context(x), person(p), e: run(p, "migrate run", on: x)]
  ⇒ O[ e1 | e1: exit_with_error(migrate, naming: f) ]  O[ | unchanged ]
```

The rule that produces this, "an indefinite inside a negated While condition that a later definite picks up takes
scope over the negation", is decided on the tree: find `K_A` under `K_No`, then a `K_The` of the same kind in the
response. It cannot be read off the surface words alone. This is hypothesis 2 of phase 1 in a real line. The
grammar's job is to keep `K_A`, `K_No` and `K_The` as distinct funs, and it does.

## 7. What a real implementation would need

1. **The vocabulary model grows by three fields.** Each verb needs an aspect (state or action). Rows need their word
   to be one of of/on/in/has/holds, or a role noun ("upstream", "upstream branch"). Attributes need an order where
   one is compared ("after `1.0.0`"). The rest (kinds with `Kind of:`, frames, adjunct prepositions such as "from",
   "with", "for", "in", value lists) is what the glossary has or what the sample asked for.
2. **A generator of about 300 lines plus a core of about 30 funs**, against `spec_typed.py`/`spec_typed_verbs.py`
   today. Most of the current hand-written surface code (agreement, `*Not` funs, number) goes, because the RGL does
   it.
3. **Pin the RGL** beside gf 3.12 in `tools install` (phase 1: 44 MB tarball, English subset compiles in about
   0.5 s), and cache the built `.gfo` files.
4. **Guards after parsing**: the coordination-scope rule (§4.1), the literal-kind filter (§4.4), and the existing
   two-trees-means-refused policy.
5. **A round-trip check on every corpus line**, which this spike shows is necessary, not optional (§5 items 3, 11).
6. **A semantics layer written per template** (about 40 generated templates plus the core) into a DRS or
   event-calculus facts, with three decisions made there: the antecedents of "its" and of definites, the scope of
   indefinites under "no" in While, and implicit comparisons.
7. **Refusal messages rebuilt** on the new categories (which frame, which kind), with `complete` for hints.
8. **Fewer generated funs where kinds do not matter**: determiners as one core `Det` category (−287 funs, same
   results). Lists and "only" could go the same way for slot kinds.

## Appendix A. The core abstract syntax (`Proto.gf`)

```gf
abstract Proto = Lex ** {
  flags startcat = Req ;
  cat Req ; Cond ; Resp ; Resps ; ActItem ; ActList ; Cmd ; Code ; Quoted ;
  fun
    Ubiq : Resps -> Req ;                       -- R.
    When : Trig -> Resps -> Req ;               -- When T, R.
    IfThen : Trig -> Resps -> Req ;             -- If T, then R.
    While : Cond -> Resps -> Req ;              -- While C, R.
    WhileWhen : Cond -> Trig -> Resps -> Req ;  -- While C, when T, R.
    WhileIf : Cond -> Trig -> Resps -> Req ;    -- While C, if T, then R.
    PPos, PNeg : Pol ;
    CondP : Pol -> Atom -> Cond ;               -- a request is (not) `accepted`
    CondAnd : Cond -> Cond -> Cond ;            -- A and B
    Runs : agent_NP -> Cmd -> Trig ;            -- the person runs `work idea`
    RunsOn : agent_NP -> Cmd -> thing_NP -> Trig ;    -- ... on the request
    RunsWith : agent_NP -> Cmd -> thing_NP -> Trig ;  -- ... with no origin option
    Shall : agent_NP -> ActList -> Resp ;       -- `work` shall A, B and not C
    OneResp : Resp -> Resps ;
    AndResp : Resp -> Resps -> Resps ;          -- R1, and R2
    ActP : Pol -> agent_Act -> ActItem ;        -- (not) print the comment
    OneAct : ActItem -> ActList ;
    AndAct : ActItem -> ActList -> ActList ;    -- A and B / A, B and C
    ExitOk : agent_Act ;                        -- exit successfully
    ExitErr : thing_NP -> agent_Act ;           -- exit with an error naming X
    Nothing : thing_NP0 ;                       -- (change) nothing
    CodeNP : Code -> thing_NP0 ;                -- `spec/index.md`
    QuotedNP : Quoted -> text_NP0 ;             -- "wall time"
    CmdCode : Code -> Cmd ;                     -- `work sync`
    CmdActor : tool_NP0 -> Cmd ;                -- `trial-runner` (an actor named as the command it is)
    CodeLit : String -> Code ;
    QuotedLit : String -> Quoted ;
}
```

The core relies on four categories that every vocabulary generates: `thing` (the top kind), `agent`, `text` and
`tool`. `Atom`, `Trig` and `Pol` are declared in the generated `Lex`, so that generated funs can return them.

## Appendix B. Generated code for one kind (`commit`, from `LexEng.gf`)

```gf
commit_n = mkN "commit" ;
commit_UseN n = mkCN n ;
commit_A cn = mkNP a_Det cn ;            -- also _The, _Every, _No, _One, _Pl, _Its
commit_Simple x = x ;
Up_commit_thing x = x ;
commit_Only x = mkNP only_Predet x ;     -- also _Base, _Cons, _And, _Or (commit is a slot kind)
commit_Pred x v = mkCl x v ;
commit_Rel_commit p cn v = mkCN cn (mkRS p (mkRCl which_RP v)) ;
commit_on_branch n np = mkCN (mkCN n) (SyntaxEng.mkAdv (mkPrep "on") np) ;
commit_on_branch_Is a b = mkCl a (SyntaxEng.mkAdv (mkPrep "on") b) ;
commit_holds_text o = mkVP (mkV2 (mkV "hold")) o ;
cite_commit_item o = mkVP (mkV2 (mkV "cite")) o ;
```

## Sources

- A. Ranta, K. Angelov, "Implementing Controlled Languages in GF", CNL 2009, LNCS 5972 (2010) 82-101 (the application
  grammar over the RGL method), as summarised in phase 1's `gf-cnls.md`.
- A. Ranta, "The GF Resource Grammar Library", LiLT 2(2), 2009; gf-rgl release 20250812,
  https://github.com/GrammaticalFramework/gf-rgl (the source of `ExtraEng.UncNeg`, `GenRP`, `ResEng.infVP` used here,
  read from the downloaded sources).
- H. Kamp, U. Reyle, *From Discourse to Logic*, Kluwer 1993 (DRS accessibility, used informally in §6; from memory,
  not re-checked in this session).
- This repository: `grammar/Req.gf`, `grammar/ReqEng.gf`, `scripts/spec_grammar.py` (tokenising, the literal
  callback), and phase 2's `sample-rewrites.md` (the candidates and their vocabulary).
