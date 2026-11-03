# Survey: design model v4 against the domain model and the grammar tools

2026-11-03, on branch `gf-conversion`, for the brief (`brief.md` beside this file). No code changed.

Read: `docs/design-model/README.md`, `design-model.md` (DM), `grammar.md` (G), the domain model
`.shop/records/2026-11-02-domain-model/domain-model.md` (DOM), `scripts/model`, `scripts/model.lp` (LP),
`scripts/model_{parse,facts,work,requests,check,report}.py`, the spike `.shop/scratch/spike-cnl/` (`gf-src/Ears.gf`,
`Lex.gf`, `run.py`, `resources.lp`, `cluster.ears`). Citations are `file:line`.

Verdicts: **keep** (fits a GF-parsed, telingo-checked language as is), **fit** (stays, changed as said),
**go** (removed, with the reason).

## 0. The one structural finding

v4 is two languages in one document, and the grammar tools touch only one of them.

1. **The graph of artifacts and work** (G §1-§5): kinds, typed edges, Datalog integrity constraints over facts read
   from frontmatter. This is a static, non-temporal check. clingo (plain ASP, `model.lp`) already does it well, and
   the GF conversion does not change its nature. Almost all of it is **keep** or a rename.
2. **The content of a requirement** (DM §2 "one EARS statement", G §6 `LINE = EARS`, LP's `v_e1`/`v_e2`): today a
   regex (`model_parse.py:212-260`). This is what the conversion replaces: GF parses every requirement (and every
   request line) against a lexicon generated from the glossary; telingo checks the parsed groups over traces
   (resources, exclusivity, universal conditions); Gherkin is linearised from the trees.

So v5 = v4's graph, renamed and fitted (requirement groups, generated scenarios, universal conditions, terms with
categories, the v3 leftovers removed), plus a new layer: the requirement language, owned by GF/telingo, attached to
the graph by a few facts (`parsed(Q)`, `unparsed(Q, Why)`, `ambiguous(Q)`, `member_of(Q, G)`, `generates(G, S)`).
The static checker and the temporal checker stay **separate programs**: `model.lp` stays plain clingo; the telingo
program is generated per group (as the spike's `run.py:60-120` does) and run by a different command.

## 1. Kinds (G §1, G:13-32; DM §2-§3a)

### Standing

| v4 kind | verdict | how / why |
|---|---|---|
| product-vision, job, context-seam | **keep** (dormant) | Product level; no files of these kinds exist in this repo, DOM does not name them. No effect on the requirement language. Rules over them (v4-v6, w_unserved_*, w_seam_unused) stay and stay silent. |
| bounded-context | **keep** | DOM §2.1. Its glossary becomes the GF lexicon's source: "the upstream's published terms" (DM:161-163) is now literal: a request line must parse against the upstream's lexicon. |
| capability | **keep** | Attributes group, narrator unchanged (DOM §2.1). DM §2 form row (DM:103) changes: Behaviour holds requirement groups (below). |
| capability-requirement | **fit: rename to requirement** | Decision 2. Now "one statement, one `shall`, parsed to one tree" (DOM:49). Its id `<capability>#r<n>` stays; ids fresh in the converted spec (decision 4). DM:104 "one EARS statement" becomes "one statement that parses in the requirement grammar". The narrator rule (DM:329, rule 11: response observable by the narrator) can stay only as judgement; GF can check it only if the lexicon marks which events a role observes (not proposed). |
| *(new)* requirement group | **add** | DOM:50, `<capability>#g<n>`, a title; statements share pre-state and trigger; one group = one scenario. Carries `restates` (decision 4). |
| acceptance-scenario | **fit: rename to scenario; generated** | DOM:54. "Evidence, never demand" (DM:105) holds more strongly: it is a linearisation of a group, so it cannot say more than its group. Its tag becomes the group id (`@g<n>`), not `@r<n>`. Its "title is free to change" (DM:105) goes: title = group title. |
| design-decision | **keep** | DM:106 unchanged; only the layout row (DM:417) is already superseded by live `spec/decisions/` (DM:427). |
| *(live extension)* term | **fit; promote to v5 kind** | LP:41 calls it an EXTENSION. DOM §0 gives every term a **category** (actor, kind, attribute, value, relation, event, resource, condition, universal condition): the grammar slot it fills. Glossary bullet form gains `(category)` and `Values: …` (DOM:33). |
| *(new)* universal condition | **add** | DOM §7, decision 5: `U<n>`, one file under `spec/` (e.g. `spec/universal.md`), checked on every trace (telingo `always`), never restated. |
| *(new)* step | **add** (outside the graph check) | DOM:55: one Given/When/Then, the linearisation of one step function, bound to exactly one step definition. DM:111-113 ("step definitions … sit outside the model") **fit**: the step *text* is now in the model (generated), the step *code* stays outside. |
| *(new)* feature | **fit** | DM:108-113 "containers, not artifacts" stays true; now generated, `Feature:` line still the capability title. |

### Roots and parts

| v4 kind | verdict | how / why |
|---|---|---|
| initiative | **keep** | DM §3, DOM §2.2. Statuses `proposed, started, done, abandoned` agree (G:263-265, DOM:114, `model_work.py:149`). Transitions `work start`, `work abandon` (decision 3) go into v5's lifecycle table. |
| job-thread | **keep** (dormant) | v4 root at product level. Live still treats it as a v3 *part* (`model.lp:42`, `model_work.py:157`): **fix to root**. |
| job-proposal, map-proposal, vision-proposal, map-escalation | **keep** (dormant) | Product level. |
| capability-proposal | **fit** | Lifecycle: v4 `drafted → approved → merged → formulated` (G:272-275); live adds `awaiting-answer`, `withdrawn` (`model_work.py:150`); DOM drops `merged` (DOM:115, 133). v5 = DOM's. `formulated` changes meaning: the group's scenario is **generated**, so the formulate round becomes mechanical (`features generate`), not a formulator session. A new guard at the front: a line that does not parse is refused before the gate (brief "Why"). |
| *(live)* glossary-proposal | **add** (as DOM's proposal supertype) | Not in v4. DOM:62 makes proposal the supertype with sorts capability-proposal and glossary-proposal. An approved glossary-proposal regenerates the lexicon (GF `Lex*.gf`); its term must carry a category, and a value must name its attribute. |
| work-item | **fit** | Statuses: v4 `awaiting-ruling` (DM:239, G:280) → live `awaiting-answer`, plus `failed`, `withdrawn` (`model_work.py:151`, DOM:117). `wkind` capability/guarantee/enabling keeps. See `accepts` and `under` in §2. |
| request | **keep** (fit its lines) | DM §3 fits well. Its lines "in strict EARS" (DM:153, G:53, G:335) become **lines that parse in the requirement grammar against the upstream's lexicon**; `rewritten` outcome (G:258) must parse too. A line that does not parse is refused by `work request` (today a regex: `workqueue_request.py:144`). Statuses agree across G:251-257, DOM:118, `model_work.py:154`. |
| *(v3, live)* cross-context-request | **go** | Retired in v4 (G:92-94); still in live `model_facts.py:297`, `model_work.py:158`, `model.lp:43,115-119,215-216,315`. No file has this kind. |

### Records

| v4 kind | verdict | how / why |
|---|---|---|
| observation, measurement, review-finding (origins) | **keep** | |
| decision-argument, initiative-archive (history) | **keep** | |
| *(DOM)* analysis, design | **add as history** | DOM:104. Live rejects `kind: design` today: `model check` prints "kind 'design' is not a record kind" for the domain-model record and for `brief.md` (`model_work.py:159,213`). Neither is an origin. |

## 2. Edges (G §2, G:59-90; DM:115-125)

| edge | verdict | how / why |
|---|---|---|
| orders, seam, pattern, pins, serves, using, depends_on (derived), of_job, enters, crosses | **keep** (dormant) | Structural, product/map level; no effect on the language. |
| in(C, X) | **keep**, **extend** | Add `in(G, C)` requirement group → capability (DOM:150). |
| has_req(C, Q) | **fit** | Becomes `member_of(Q, G)` n..1 plus `in(G, C)`; `has_req` derivable: `has_req(C,Q) :- member_of(Q,G), in(G,C)`. |
| has_sc(Q, S) (written by formulation) | **go → generates(G, S)** 1..1, written by the generator | A scenario tests a group, not a requirement (DOM:147). The `@r<n>` tag reading (`model_facts.py:527-535`) becomes `@g<n>`. |
| rests_on, supersedes | **keep** | |
| source | **keep** | Live keeps request sources as `req_source` (`model_requests.py:499`), a rename only. |
| part_of | **keep** | Live request part_of is `req_part_of`; unify with v4 names or keep the split, either is fine. |
| fulfils, raised_for | **keep** | Implemented (`model_work.py:271`, `model_requests.py:504`). |
| raises(W, Q) | **keep** (unimplemented) | Live records raised requests in `raised.jsonl` (`supervise_raise.py`), not as a work-item field; model does not read it. |
| resolution(Q, Rq, V) | **keep** | Live drops the version (`model_requests.py:507-512`, arity 2 in LP:99). With fresh ids, the resolution may name a group instead of each requirement; recommend: keep requirement ids (G rule 3 is about not naming scenarios). |
| argues | **fit** | v4 1..n (G:82) vs live exactly 1 for a capability-proposal (`model.lp:206-208`, v_k6) and DOM:141. v5: exactly one capability for a capability-proposal; a glossary-proposal argues the glossary. |
| adds, changes, removes | **fit** | Keep for requirements and groups, and for terms (DOM:142). `changes` on a requirement conflicts with "retire, never edit" (memory note; brief decision 4 applies it from the converted spec onward): recommend v5 says a changed requirement is `removes` old + `adds` new id; `changes` stays for groups (title, membership) and terms. |
| under(W, C) | **fit** | v4: work-item → capability (G:84; live `model_work.py:340`). DOM:143 says work-item → capability-proposal, which is `part_of`. Keep v4's `under → capability`; record DOM's reading as `part_of`. |
| for, check, blocked_by, wi_depends | **keep** | |
| accepts(W, S) | **fit** | v4: → acceptance-scenario (G:86). Live: → requirement (`model.lp:69` FIX, `model_work.py:350-360`). DOM:144: → requirement. With groups generating scenarios 1..1, the natural unit is the **group**: a work-item accepts `#g<n>` and its tests are the group's one scenario. Recommend `accepts → requirement group`; accepting a requirement may be allowed and read as its group. |
| about | **keep** | |
| *(new)* member_of, generates, restates (DOM:147-149) | **add** | `restates` is a source-only attribute: today's ids are not nodes after conversion, so it is not resolved (or resolved against a frozen index of the old spec). |
| *(new)* category(T, Cat), value_of(V, Attr), avoid(T, W) | **add** | Lexicon facts; `avoid` exists live (`model_facts.py:434`). |
| *(new)* has delegation, on, answers, for (stage), holds, writes, belongs to, merges into | **add to v5's vocabulary; not graph-checked** | DOM:155-163. They are the lexicon's relations for requirement *content* (the telingo layer); only `on`/`answers` have files today (questions in node bodies). Do not add them to `model.lp`. |

## 3. Rule codes (G §4, G:123-245; DM §4, DM:317-337)

Code clashes first: LP reuses v4 codes for different rules. v5 must pick one meaning per code.

| code | G (v4) | LP (live) | v5 |
|---|---|---|---|
| v3 | resolution names a requirement, never a scenario (G:131) | delivered request's resolution names a requirement the spec lacks (LP:97-99) | one rule, both clauses |
| v7 | asker/upstream across a seam (G:144) | cross-context-request names no capability (LP:116-117) | G's; LP's goes |
| v18 | v18a-c part_of/blocked_by/for across contexts (G:197-200) | a foreign work id (LP:267-269) | keep both, as v18a-c plus v18d (LP's) |
| v_d2 | job-thread built with an undelivered request (G:227) | abandoned initiative with a part open (LP:274-275) | G's v_d2; LP's renamed (e.g. v_d5) |
| w_many_requests | open requests per upstream (G:243) | per `across` seam (LP:314-315) | G's |
| w_stale_intake | accepted request with no initiative after 90 days (G:244) | initiative `proposed` > 90 days (LP:316-317) | G's, LP's kept as a second clause or dropped |

| rule | verdict | how / why |
|---|---|---|
| 1 (needs) | **go** | Retired in v4 (DM:319, G:124); LP still has v1 and `#defined needs/from_cap/across` (LP:22, 79-81). |
| 2 standing edges between standing | **keep**, extend to member_of, generates, restates | LP:83-95 written out per relation. |
| 3 | **keep** (merged, above) | |
| 4, 5, 6, 6b | **keep** (dormant) | |
| 7, 7c | **keep** G's; LP v7/v7b **go** | |
| 8 work-item names a capability | **keep** | |
| 9a-g | **keep**, fit 9d/9e | G:154-155 allows priority on request/job-thread, source on initiative/request/job-thread; LP still v3 (initiative only, LP:138-141) while live requests carry `source` under another fact name. v5 = G's. |
| 10a-c | **keep** | 19 of today's 62 violations are v10a (person/… sources naming nothing): a data issue, not a rule issue. |
| 11 one narrator | **keep** (second half judgement, §1) | |
| 12a-b, 13 | **keep** | |
| 14 no new kind without a trigger | **keep** | The trigger for groups, U<n>, terms-with-category is the brief's "Why". |
| 15a-d requirement ids | **keep**; **add** 15g-i for group ids `#g<n>` and `U<n>` (present, unique, never reused) | |
| 15e proposal changes a missing requirement | **fit** | With `changes` limited to groups/terms (§2). |
| 15f formulated proposal leaves a requirement without a scenario | **fit** | Becomes: a formulated proposal has a group with no generated scenario, i.e. the feature file is stale. |
| 16a-d | **keep** | LP v16a has a date cutoff `D > "2026-10-23"` (LP:256-258) for old initiatives; a fresh spec may keep or drop it (old initiatives are compacted/archived). 16b-d unimplemented. |
| 17 traced request | **keep** | 24 of today's violations; LP:260-265. |
| 18 | **keep** (with LP's as 18d) | |
| 19 / v_d1, v_d3, v_d4 | **keep** | v_d4 unimplemented (needs line ↔ requirement id, which the parse can now give: an accepted line's tree equals a requirement's tree). |
| v_k1, v_k2 (job, job-path) | **go** | Retired in v4 (G:202); still in LP:194-197. |
| v_k3-k5 | **keep** with LP's FIX (several capability-proposals, glossary-proposal as first part) | |
| v_k6 one capability per capability-proposal | **keep** (LP rule; v5 states it) | |
| v_b1, v_b3 | **keep** G's v_b3 (LP:217-218 is v3's) | |
| v_b2 | **go** | cross-context-request. |
| v_s1 a scenario names no requirement | **fit** | → a scenario names no group (only a hand-written or stale scenario can). |
| v_s2 a scenario names two requirements | **fit** | → a scenario generated from two groups: impossible by construction; keep as a guard or drop. |
| v_s3 a requirement has no scenario | **fit** | → a group has no scenario (stale generation); plus **new**: a requirement in no group / in two groups. Better also as `features generate --check` (like `model decisions --check`, `model_report.py:414-427`). guarantees exemption: keep for groups whose statements have no step linearisation (bounds checked by measurement). |
| v_w1-w4 | **keep** (v_w4 reads `accepts` group) | |
| live v_t1 a word the glossary avoids | **fit** | A requirement that parses can contain only lexicon words (plus code spans/quoted strings), and a scenario is generated, so v_t1 over requirements/scenarios becomes near-vacuous. Refit to "no avoided word is a lexicon entry or a word of a lexicon entry's linearisation", and optionally keep it over prose sections (Purpose, decisions). |
| live v_t2, v_t3 | **keep** | **Add** v_t4 every term has a category; v_t5 every value names exactly one attribute; v_t6 no two terms linearise the same. |
| live v_e1, v_e2 (regex EARS) | **go → parse rules** | Replaced by `v_p1` a requirement (or request line, or U) does not parse, `v_p2` it parses with more than one tree. Facts come from the GF parse in Python; the rule in LP is a one-liner like v_e1 today. |
| *(new, telingo, not in LP)* | **add** | Per group: the group is satisfiable (its pre-state, trigger and responses admit a trace); no two groups contradict (spike `run.py`, "conflicts"); no two groups are duplicates (equal trees, spike "duplicates"); every U<n> holds on every group's trace; resource exclusivity (`resources.lp`). |
| warnings w_unserved_cap/job, w_seam_unused, w_uncited_obs | **keep** | |

## 4. Lifecycles (G §5)

- request **keep** (lines must parse; `rewritten` text must parse).
- initiative **keep**; add `work start`, `work abandon` as the events.
- job-thread, map-escalation, product proposals **keep** (dormant).
- capability-proposal **fit** to DOM §3 (no `merged`; `awaiting-answer`; `formulated` = generated); glossary-proposal **add** (ends at `approved`).
- work-item **fit**: `awaiting-ruling` → `awaiting-answer`; `failed` (U6) and `work retry`; `withdrawn`.
- design-decision: DOM gives `proposed, accepted, rejected, superseded` (DOM:119); v4 has no lifecycle row for it: **add**.

## 5. Sentence forms (G §6, G:286-362)

- G §6 is a controlled language of the *model*, with no parser anywhere (G:378 "a parser of a few hundred lines"
  was never written; the facts come from frontmatter). It is **not** the requirement grammar.
- `LINE = EARS` (G:335) and `CAP "has requirement" RID ":" TEXT ("formulated as" SCEN)?` (G:291) **fit**: TEXT/LINE
  become `Req`, the start category of the GF requirement grammar; "formulated as" **goes** (generated).
- The other productions **keep as a reading form, non-normative**: it would be possible to host them as a second GF
  grammar (`Model`) sharing the lexicon, but nothing reads such sentences today and the brief does not ask for it.
  Recommend v5 says so and the refusal table (G:344-362) stays as documentation of the rules, run by `model check`
  over facts rather than by a parser.
- The spike's grammar (`gf-src/Ears.gf:1-25`) is per-construction (`TakeEvery`, `OneRoundAcross`, …): a grammar
  of 19 capabilities this way would be one function per statement. v5's grammar must be compositional:
  `Req = [Where] [While] [When|If] Actor shall Response`, with `Response`, `Trigger`, `Pre` built from the lexicon
  categories (actor, kind, attribute/value, relation, event, resource, condition). DOM §0 already maps each category
  to a grammar slot, a logic predicate and a Gherkin form: that table is the grammar's design.
- Tokenisation: the spike's input needs spaces before punctuation (`cluster.ears:8` "`work run` , … ."); the parser
  should tokenise, not the author.

## 6. DM sections, other than above

- §1, §3 (requests, trace, three structures), §3a, §6 (where work comes from), §7 (questions): **keep**. §7 "why does
  this requirement exist" (DM:397) gains `restates` back to today's ids.
- §5 flow (DM:341-363): **fit**: `form[one acceptance-scenario each]` → `generate[one scenario per group]`; add "parse
  and logic check" between the request's lines and the gate; work-item flow `awaiting-ruling` → `awaiting-answer`.
- §8 terms new in v4: **keep**; v5 adds the categories and the new kinds.
- §9 layout (DM:414-428): **fit** to live (`spec/decisions/`, `.shop/work`, `.shop/records`) plus `spec/universal.md`,
  and where the generated grammar lives (recommend generated, not tracked by hand: the glossary is the source).
- G §7 tooling (G:364-381): **fit**: add GF (lexicon generation, parse) and telingo (group programs, U<n>), keep the
  kb/SQL/SHACL notes as options.
- README.md:14-15 "model check still checks v3": becomes "v5".

## 7. How the scripts implement v4/v3 today

`scripts/model` (139 lines) is the CLI: `facts`, `check`, `rules`, `decisions`, `why` (`scripts/model:118-135`); its
docstring says "version 3" (`:2`) and its contract describes Behaviour bullets with `[r<n>]` and `@r<n>` tags
(`:51-60`). It is loaded **by path** by `workqueue.py:22-31` and `migrate_layout.py:123-129` for `frontmatter`, and
it re-exports `as_list, frontmatter, scenarios, section` (`:14`) for them.

- `model.lp` (334 lines): "grammar.md (version 3)" (`:1`) plus `FIX` and `EXTENSION` clauses. It implements v4
  piecemeal: v3 (resolution, LP:97-99), v16a, v17, v18 (LP:255-269) are v4 ideas under design-model-check ids; it
  still holds v3's needs/cross-context-request/job-thread-as-part/v_k1/v_k2. Kinds named `capability-requirement`,
  `acceptance-scenario` (LP:40). Today's run: 62 violations (v17 24, v10a 19, v_d1 9, v3 8, v_s3 2), 16 warnings
  (w_uncited_obs), 162 unresolved references, 5 file problems.
- `model_parse.py` (271): the frontmatter subset (`:12-47`, shared with work and migrate), sections and bullets,
  `behaviour_items` (bullets and `[r<n>]` table rows with lead sentences, `:134-168`), `scenarios` (`:171-197`),
  `glossary_entry` (`- **term**: def. Not: …`, `:200-209`), the EARS regex `ears` (`:212-260`), `mention` (`:263`).
- `model_facts.py` (287): `Model`; `KINDS` (`:295-298`, includes v3's cross-context-request); `read_capabilities`
  (`:446-504`) emits `capability-requirement` nodes, `req_id`, `has_req`, `ears_other`/`ears_many`; `read_features`
  (`:506-535`) reads `@r<n>` tags into `has_sc`, skipping `@deprecated`; `read_glossary` (`:419-435`).
- `model_work.py` (240): `STATUSES` (`:148-155`, `merged` still allowed), `PART_KINDS` (`:157-158`, job-thread and
  cross-context-request as parts), `RECORD_KINDS` (`:159`, no `design`/`analysis`), decisions, records,
  initiatives, parts; `accepts` → requirement with a file problem when no scenario names it (`:350-360`).
- `model_requests.py` (69): request frontmatter and `## Resolution` → `asker`, `req_part_of`, `req_source`,
  `req_raised_for`, `resolution` (no version). Lines and outcomes are **not** facts; `upstream` is implicit (this
  context).
- `model_check.py` (139): clingo solve, labels, re-exec under an interpreter that has clingo (`:42-92`).
- `model_report.py` (87): `decisions` (generated index, `--check`) and `why` (proposal → part_of chain → sources).
- Outside `model`: `workqueue_request.py:144` refuses a request line that fails `model_parse.ears`;
  `supervise_draft.py:10` uses `expand`; `supervise_worker.py:31` lists `model` among stage scripts.
- Tests bound to v3 behaviour: `features/design-model-check.feature` (938 lines), `tests/scenarios/design_model_check_*.py`
  (11 modules), `tests/scripts/test_model*.py` (5). Skills and agents that name LP rows: `formulating-features`
  (v_s1, v_s3, v_t1), `integrating-a-proposal`, `checking-spec-consistency` (v_t1-t3), `agents/initiative-round.md`.

## 8. What must change in the scripts

1. **`model.lp` → v5.** Rename kinds (requirement, scenario); add requirement group, universal condition, term as
   standing; job-thread a root. Remove v1, v7/v7b, v_b2, v_k1, v_k2 and the `needs/from_cap/across` inputs. Resolve
   the code clashes (§3). Add group-id, U-id, category and parse rules (v15g-i, v_t4-t6, v_p1-p2), refit v_s1-s3,
   v15f, v_w4. Rewrite its header against v5 and drop the FIX/EXTENSION notes that v5 absorbs. Stays plain clingo.
2. **A GF module** (new concern → new module and CLAUDE.md row, e.g. `scripts/spec_grammar.py`): build the lexicon
   (`Lex.gf`/`LexEng.gf`) from the glossary's categories, compile with `gf` into a PGF (cached, keyed by glossary
   hash), parse a line → tree / refusal reason / ambiguity, tokenise. Uses the `pgf` Python binding (the spike's
   venv) or `gf --run` as a subprocess. `tools_env.py` installs GF and the binding as real dependencies (brief).
3. **`model_parse.py`**: `ears()` goes, its two callers (`model_facts.py:499`, `workqueue_request.py:144`) call the
   GF module. `behaviour_items` reads groups (`### [g<n>] <title>` with `- [r<n>] …` bullets, `restates:` line) and
   drops table rows and lead sentences (a table row is not a statement). `glossary_entry` reads `(category)` and
   `Values:`. `frontmatter`, `section`, `scenarios`, `expand` stay (shared).
4. **`model_facts.py`** (already 287 lines, so split): move capability/feature reading to a new module (e.g.
   `model_spec.py`) emitting `member_of`, `in(G,C)`, `restates`, `generates` (from `@g<n>`), `parsed/unparsed/
   ambiguous`, U<n> nodes from `spec/universal.md`, term `category`/`value_of`. `KINDS` loses cross-context-request,
   gains requirement-group, universal-condition.
5. **`model_work.py`**: statuses per DOM §3 (drop `merged`; design-decision lifecycle); `PART_KINDS` loses job-thread
   and cross-context-request; `RECORD_KINDS` gains `design`, `analysis`; `accepts` reads group ids and checks a
   generated scenario exists.
6. **`model_requests.py`**: emit `line(Q,N,Text)`, `outcome(Q,N,O)`, `upstream(Q,X)` and the parse facts per line
   (lines parse against this context's lexicon), so v_d4 and v_p1 hold for requests.
7. **A telingo module** (new concern, new module, e.g. `scripts/spec_logic.py`): tree → telingo program per group
   (one translation per grammar construction, as `run.py:60-120`), plus the universal conditions and resources as
   `always` constraints (`resources.lp`); reports unsatisfiable groups, contradictions, duplicates, U violations. A
   new `model logic` subcommand (or part of `check` with a flag) so `model check` stays fast and static.
8. **Gherkin generation**: the Steps grammar linearises each group's tree into Given/When/Then; `features generate`
   (and `--check`) writes `features/<capability>.feature`, one scenario per group tagged `@g<n>`. Belongs to the
   `features*.py` family (new module + row).
9. **`model_check.py`**: keep; the re-exec-for-clingo logic can shrink once clingo/telingo are installed by
   `tools install` into the project interpreter (keep exit 2 with an install hint).
10. **`model_report.py`**: `why` follows `restates` to today's ids and names the group; `decisions` unchanged.
11. **`scripts/model`** contract text rewritten for v5 (groups, `@g<n>`, parse, U<n>); new subcommands `parse
    <line>` (debugging a refusal) and `logic`.
12. **Tests and docs**: rewrite `design-model-check` spec/feature/steps against v5; update the skills and the
    initiative-round agent that name v_s1/v_s3/v_t1 and the formulate round (which becomes generation).
