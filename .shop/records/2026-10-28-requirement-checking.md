# Can tools check a requirement line before the gate? (clingo, NLP, a System-1 judge)

Read-only study. Repository paths are relative to `/home/vscode/shopsystem-bdd`. Scripts and outputs are in
`.shop/records/2026-10-28-requirement-checking/`, called `req/` below (the large derived JSON, `req/snap/` and the venv were not kept; the scripts regenerate them; they are kept as `.py.txt`, rename to run).
The question record is the 42 rows of `question-wording-report.md` (the sibling report), cited as `#n`.

## 0. Verdict

**Yes, in part. The part that pays is set-level, and clingo is the right engine for it.** Of the 42 recorded questions,
24 come from line wording (8 request wording, 13 existing spec wording, 3 terms). Here is what each layer would have flagged
before the gate:

| Layer | Recorded questions it flags (of 42) | Effort | Precision on the current spec |
|---|---|---|---|
| (b) EARS-part parser + clingo, set-level | **10**: #2, #4, #10, #11, #12, #15, #16, #18, #25, #27 | Small: about 150 lines of Python facts and a 47-line `.lp`, extending `model` | about 50% on catch-all pairs; small flag counts |
| (a) English structure (spaCy) + two lexicons | **3–4**: #1, #30, #31, and part of #32/#34, all from the lexicons. The generic smells catch **0** causally | Small for the lexicons. The generic smells are not worth wiring in | generic smells fire on 30–46% of lines |
| (c) System-1 judge (Haiku), per line and per candidate pair | **up to 9 more** in reach: #3, #5, #8, #13, #17, #19, #23, #26, #36, #41. **Not measured** | Medium: a prompt, a JSON schema, an eval harness | unknown until the eval in §4 is run |
| None (instruction or brief gaps, genuine decisions) | 12 cause-4 rows and the 6 genuine decisions | — | — |

Three things to keep in mind:

- **The repository already runs clingo over the spec.** `model check` solves `scripts/model.lp` (332 lines) over facts
  from `scripts/model_facts.py`. A line's EARS shape is already a fact: `ears_other` and `ears_many` come from
  `model_parse.ears` (`scripts/model_parse.py:216`), which gives rules `v_e1` and `v_e2` (`scripts/model.lp:293-299`).
  `work request` refuses a line that fails the same `ears()` (`scripts/workqueue_request.py:137`).
- **All 539 current lines pass `v_e1` and `v_e2`.** The per-line form is not where questions come from. The gap is
  **between** lines.
- **The PoC's ontology was written while looking at the known pairs.** Read the 10 as an upper bound for this ontology,
  not a blind result. §2.5 says what a fair test needs.

## 1. Parser coverage on the current spec

`req/lines.py` reads every Behaviour line with the repository's own `behaviour_items` and gets 539 lines, 45 of them
table rows. `req/parse.py` is a deterministic regex parser. It protects code spans, splits the clauses Where, While, When
and If…then, and splits off the system and the response. It also splits the trigger into subject, event verb and
qualifier, and the response into verb and object.

| Level | Lines | Notes |
|---|---|---|
| Clauses, system and response separated | 533/539 (98.9%); effectively **539/539** | The 6 misses are `spec-consistency` r22–r27. Those are table rows with one cell besides the id, so my table flag missed their lead sentence. Parsed by their lead, they pass. |
| System is a short noun phrase or code span | 508/539 | The real smells among the rest: `work-queue#r23` "that command" (an anaphoric system) and `migration-tools#r15`/`r30` (two systems in one line). Others are long but fine ("the plugin's SessionStart hook"). |
| Trigger split into subject, event verb and qualifier | 486/539 | Uses a 30-verb list. The 53 misses are triggers whose verb is not in the list ("needs", "refuses", "hands back", "commits"). spaCy's root verb would take most of them. Not measured. |
| Trigger normalised to an event on a round of a named kind | 27 lines | All in `supervision`. This is where the event identity that matters lives. |
| Response split into conflict-relevant atoms | about 70 lines | transition to a status, keep the status, make no transition, start or start no round of a kind, exit with an error, run or run nothing |

**What parses mechanically:** the form (clause order, one `shall`, system, response). It is about 100% parseable
because the spec is written to a template.

**What does not:** the **identity** of events, objects and qualifiers. Examples:

- Is "applies nothing because…" a case of "ends having applied its drafts"?
- Is "answers … with an answer that asks for a change" disjoint from "accepts as it is"?

The PoC hand-codes about 12 qualifier atoms, 4 event implications and 7 disjointness facts (`req/facts.py`, `req/overlap.lp`).
That works well for the supervision round lifecycle and nowhere else. Extending it across all 19 capabilities is either
hand ontology work or a model extracting the atoms.

**Recommendation:** extract the structure with a deterministic parser, and normalise events and qualifiers with a
glossary-driven table that a person or the writer keeps. Haiku can propose entries for it. It should not be the parser.

## 2. Layer (b): EARS parts + clingo, the proof of concept

### 2.1 Facts schema

These facts are additions alongside `model_facts.py`'s current facts.

```
line(L, Cap, Kw).              system(L, S).            retired(L).     new(L).        % new = a request line
subject(L, Head).              kind(L, K).              event(L, E).    qual(L, Q).    % trigger parts
resp(L, Verb, Obj, Arg).       many_responses(L, N).    where_event(L).                 % response parts, per-line
```

- `Head` is the earliest glossary-ish head noun in the trigger outside code spans.
- `K` is the round kind from "of the kind `K`".
- `E` is one of `ends|gives|applies|formulates|drafts|finds|starts|started`.
- `Q` is one of `no_question, question, applied_drafts, unheld, change_list, no_change_list, nothing, fault, lines_not_in_spec, anew, raises, needs_run`.

### 2.2 The program (`req/overlap.lp`, 47 lines, abridged)

```prolog
implies(gives, ends). implies(applies, ends). implies(formulates, ends). implies(drafts, ends).
ev_rel(E,E) :- event(_,E).   ev_rel(E,F) :- implies(E,F).   ev_rel(F,E) :- implies(E,F).
ev_rel(E,F) :- implies(E,ends), implies(F,ends).            % two outcomes of one round may co-occur (open world)
disjoint(question,no_question). disjoint(change_list,no_change_list).
disjoint(fault,X) :- qual(_,X), X != fault.                 % a round that ends in a fault gives nothing else
sep(A,B) :- qual(A,X), qual(B,Y), disjoint(X,Y).
overlap(A,B) :- A < B, system(A,S), system(B,S), subject(A,H), subject(B,H), kind_ok(A,B),
                event(A,E), event(B,F), ev_rel(E,F), not sep(A,B).
clash(A,B,"transition vs keep status") :- resp(A,transition,O,_), resp(B,keep_status,O,_).   % + 3 more clash kinds
c1_conflict(A,B,Why) :- overlap(A,B), clash(A,B,Why), active(A), active(B).
c2_catchall(A,B) :- ov(A,B), event(A,ends), event(B,F), implies(F,ends), not same_resp(A,B), active(A), active(B),
                    qual_count(A,N), N <= 1.                 % "When a round ... ends" vs a specific new outcome
c3_widens(A,B)   :- overlap(A,B), same_resp(A,B).            % retired lines included: a new line re-states/widens one
c4_presupposes(A,B) :- resp(A,runs_nothing,_,_), system(A,S), system(B,S), B != A, resp(B,presupposes_run,_,_).
p1_where_event(L) :- where_event(L).                         % "Where" holding an event verb
```

**The design choice that matters:** overlap is **open world**. Two triggers overlap unless a declared disjointness
separates them. This is what makes catch-all triggers visible: the spec never says that "applies nothing" excludes
"ends having applied its drafts", so the solver assumes they can co-occur. That assumption is exactly the gate question
#11.

### 2.3 What it flags on the current spec (plus r140 from `git show 580ad083` and 3 original request wordings), `req/poc-output.txt`

| Rule | Flags | Known question pairs it hits | False or uninteresting positives |
|---|---|---|---|
| c1 conflict | 5 | r146 × r151 (start formulate vs start no formulate; #11/#16); r152 × r83 (keep status vs transition to `formulated`; #12/#15) | r118 × r119 (asks-for-a-change vs accepts: disjoint in English, unknown to the ontology); r69 × r86/r87 (the gate's catch-all "ends" vs the fault line: a real "which wins", already settled by r86 being an `If`) |
| c2 catch-all | 30 | r144/r145/r146 × r150/r151/r147 (#11, #16, #17); r83 × r149/r152/r153 (#12, #15); r92 × r148, r142 (#18) | r91 × … (keeping drafts is compatible with anything); r101 × r77/r78/r118/r119 (subject mis-normalised); r69/r85 × r117. About 14/30 true. |
| c3 widens | 9 | r140 (retired) × r150 (#10) | r47 × r48, r154 × r155 (one trigger split into two responses, which is correct style). Restrict c3 to pairs where one line is `new`. |
| c4 presupposes | 4 | r32 × r7 (wall time; #4) | r32 × r33 ("marked not run"), r32 × r34 (verify from the run `work run` gave: consistent). Misses r6 and r12 (#5, #3), because their system is "the reviewer", not "the branch reviewer". A system-alias table fixes it. |
| p1 Where-for-event | 1 | q23 line 5, the original "**Where** the branch reviewer finds…" (#2) | 0, after excluding "gives" (a delegation or config "gives" is a state) |
| p2 two responses | 32 | q23 line 1 (it was split into r154/r155) | Most are "…, naming X, and leave every file as it was", which `docs/capability-format.md:99-105`'s own failure template permits. **Misses** q18 line 4 / q19 line 3 "set `drafted`, its earlier drafts kept…" (#19): an absolute construction, no "and". |

### 2.4 Replay: each request against the spec as it stood when the request was raised

`req/replay.py` uses snapshots from `git show <commit>:spec/...` into `req/snap/`. The request lines are added as `new`.
Output: `req/replay-output.txt`.

| Request (raised at) | Flags on its lines | Hits in the question record |
|---|---|---|
| q14 (a1bc6f66) | 4 | q14 line 1 has two responses ("one set of commands … and one lifecycle"; #34 was about it). r91/r92/r96 × line 24: no question was recorded (FP). |
| q18 (7a68d57e) | 6 | **r80/r71/r114 × line 1**: exactly i40's dropped W-Q1 (#25). That question cost q19 and the whole of i41. **r92 × line 4**: W-Q4, "r92 writes a second proposal" (#27). |
| q19 (7d0ed73f) | 20 | r92 × lines 3/9 (#18). Lines 5/7 widen r80/r71, which q19 retired by name (correct: c3 needs "names it"). The rest are the q19 lines among themselves. |
| q22 (1e62ab81) | 5 | **r144/r145/r146 × line 3** (#11, and its re-asks #16); **r83 × line 1** (#12, re-ask #15); **line 3 widens retired r140** (#10) |
| q23 (33f4e145) | 7 | line 4 (r32) × r7 (#4); line 5 Where-for-event (#2); line 1 two responses. Misses r6 and r12 (#5, #3): system alias. |

**Score:** 10 of the 42 rows are flagged before the gate: #2, #4, #10, #11, #12, #15, #16, #18, #25, #27. Two of them
(#25, #27) were questions the gate **dropped**, which then cost a further request and initiative (sibling §3.3).

**Not flagged:**
- the closed output list r132 (#13, #17, #23, #26);
- `work show`/`work status` overlap (#33, #42);
- the missing status line (#22);
- r6 and r12 (#3, #5).

### 2.5 Limits, said plainly

- **Overfit risk.** I wrote the qualifier atoms and implications while knowing the target pairs. A fair test has two parts:
  1. freeze the ontology now;
  2. score it on the next 3–5 requests, blind.
- **Coverage.** The event ontology covers only the round lifecycle in `supervision`. Every other capability falls back to
  same-subject, same-verb matching, which says little. Growing it is ongoing work: one implication or disjointness fact
  per new outcome word. The writer could add these to a small table beside the glossary.
- **c2 is a "say which wins" prompt, not an error.** Its value is to put the colliding existing lines in front of the
  writer and the gate. It should be a warning that lists candidates, and never block.

## 3. Layer (a): English-structure clarity checks

`req/clarity.py` uses spaCy 3.8 with `en_core_web_sm` in a scratch venv. It runs offline once the model is installed, at
about 1 s per 100 lines. Code spans are replaced by a proper noun before parsing.

**Labels.** 11 request lines that drew a per-line question: q14 lines 1, 2, 9, 18, 20, 22; q18 line 4; q19 line 3; q23
lines 1, 2, 5. The other 38 lines of q14/q18/q19/q22/q23/q24 are unlabelled negatives. They are not certified clean.

| Check (INCOSE GtWR rule) | Spec lines flagged /539 | Request lines flagged | Hits on labelled lines | Did it flag the **cause** of the question? |
|---|---|---|---|---|
| passive with no agent (R2) | 162 | 8 | 0 | no |
| anaphora it/they/this as an argument (R24) | 246 | 21 | 6 | **no**. "it" in "the work-item it belongs to" (#8) is fine; "belongs" is the problem. |
| coordinated responses under `shall` (R18) | 42 | 2 | 2 | q23 line 1: yes, it was split, but its question was "exit code". q14 line 18: a parse error. |
| coordination ambiguity, N and N with a modifier (Chantree/Yang) | 83 | 9 | 5 | no. "a request or a message" was asked about for "message" being undefined, not for the attachment. |
| deep nesting, ≥4 subordinate clauses | 120 | 8 | 3 | no |
| vague words (R7, QuARS, Smella lexicon) | 22 | 2 | 1 | no ("whatever") |
| long, >45 words | 73 | 1 | 1 | no |
| nominalisations ≥3 | 12 | 0 | 0 | — |
| **implementation lexicon** (exit code, field, carrier, port, issue, GitHub, JSON …) | — | 9 | 4 | **yes**: #1 "exit code", #31 "carrier/port/issue/GitHub", #30 "fields of the contract's form" |
| **novel word** (noun or verb lemma in ≤2 lines of that spec and in no glossary term), against the snapshot | — | 17 | 6 | **partly**: "identity" (#32 allow list), "contract" (#30), "lifecycle"/"raise" (#34). **Missed** "message" (#36) and "belongs" (#8), because both words already appeared elsewhere in another sense. |

**Verdict on layer (a):**

- **The generic smells do not earn their place here.** This spec is long, dense, correct EARS. Passive voice and
  relative pronouns are the house style, so the base rates (30–46% of lines) bury the signal. None of the 42 questions
  is caused by passive voice, vagueness, length or nesting.
- **Two narrow lexicon checks do pay:** implementation words, and new words that are no glossary term. They need no
  parser beyond a lemmatiser, and spaCy is enough for that. They catch #1, #30, #31 and part of #32/#34.
- **"Is this term defined in the sense used"** (#8, #36) is beyond lexicons. It goes to layer (c).

## 4. Layer (c): a System-1 judge (Claude Haiku 5.5, `claude-haiku-5-5`)

**What it judges.** Two tasks. It never does free review.

1. **Per line** (every request line, and every line a draft adds or changes). The input is:
   - the line;
   - the glossary of `spec/index.md` (cached);
   - the rubric, which is the skill's red-flags table (cached).

   It returns JSON:
   ```json
   {"responses": 1, "keyword_fits_trigger": true, "suggested_keyword": null,
    "undefined_terms": [{"word": "message", "why": "no entry; used for something a carrier holds"}],
    "terms_used_off_sense": [], "implementation_detail": ["exit code"],
    "two_readings": [{"phrase": "...", "a": "...", "b": "..."}], "verdict": "fix", "confidence": 0.8}
   ```
2. **Per candidate pair**, and only the pairs layer (b) emits (c1–c4) or the pairs a closed list touches. The input is
   both lines, and the output is:
   ```json
   {"can_both_fire": "yes|no|unclear", "responses_compatible": "yes|no|unclear",
    "which_wins_said": true, "new_line_falls_outside_closed_list": false, "reason": "..."}
   ```
   This is where r118 × r119 is cleared ("asks for a change" and "accepts" are disjoint), where r32 × r6/r12 are caught
   (a reproduction needs a run), and where r132 × r147/r149 is caught (a new round outcome is not in r132's list).

**Order of the layers:**
1. Parser and lexicons, which are free.
2. clingo, which is free and finds candidates.
3. Haiku, only on the lines and pairs the first two emit, or all request lines.

The model gets no task that a rule can do.

**Cost.** Haiku 5.5 is $0.10 per million input tokens and $0.50 per million output tokens (cache reads are cheaper).

| Item | Tokens | Cost |
|---|---|---|
| One judgement: glossary (~4k) + rubric (~1k) + line(s) (~0.3k) in; ~250 out | ~5.3k in, ~250 out | about **$0.0007** |
| Whole spec, 539 lines | | about $0.40 |
| A typical request, 3–9 lines plus ~10–30 candidate pairs | | under $0.05 |

Latency is a few seconds. The cost is negligible next to one gate round trip.

**How to measure accuracy before trusting it:**

1. **Positives:** the 11 labelled per-line request lines (§3), and the set-level pairs of the 10 + 9 recorded collisions
   (r83 × r149/r152, r144–146 × r150/r151, r140 × r150, r92 × r148, r80/r71/r114 × q18 line 1, r32 × r6/r7/r12,
   r132 × r147/r149).
2. **Negatives:** the lines that passed integrate and gate without a question, from i39–i43 change lists. Also the 30
   ASP c2 pairs a person marks "compatible".
3. **Run on the request text as raised** (the `req/snap/` snapshots), not the final wording.
4. Report recall and precision per field. Repeat 3× to measure variance.
5. **Gate:** it goes into the workflow only if its recall on positives is at least 0.7 and its precision is at least 0.5.
   Otherwise it costs the person more reading than the questions it saves.
6. **Then score it blind** on the next 5 requests, against the questions the gate raises.

**Where it runs:**
- **`work request`**: advisory warnings printed. The command still refuses only on `ears()`.
- **The integrate round, after the writer's change list and before the gate**: the round gets the flags. It either
  drafts the retire-and-replace or names the "which wins" in the change list. This is the stage that saves the most.
- **`model check`**: c1–c4 as `w_` warnings, never blocking.

## 5. Tool survey

| Tool | What it checks | Usable here? | Why |
|---|---|---|---|
| **clingo** (Potassco) | Any rule over facts | **Yes. Already installed and in use** (`scripts/model_check.py:17-33`) | Set-level overlap and catch-all checks are about 40 rules over parsed facts. §2. |
| **spaCy 3.8** + `en_core_web_sm` | POS, dependencies, lemmas | Yes, offline in Python | Good for lemmas, verb extraction and coordinated verbs. The generic smells built on it are noise on this spec (§3). |
| **Stanza** (Stanford) | The same, more accurate, slower | Yes, offline; a ~400 MB model | No gain over spaCy for the checks that pay here |
| **benepar** | Constituency parse | Possible; it needs spaCy 3 + TF/torch | Would sharpen attachment ambiguity, which caused 0 recorded questions |
| **LanguageTool** (`language_tool_python`) | Grammar and style | Runs offline, but needs a Java server | Catches grammar, not requirement semantics. None of the 42 questions is grammatical. |
| **Vale / proselint / write-good** | Prose style; custom YAML word lists | Vale yes (Go binary) | A good host for the implementation and vague lexicons, but a 20-line Python check does the same inside `model` |
| **QuARS** (Lami, ISTI-CNR, 2004) | Lexical defects: vagueness, optionality, weakness, multiplicity, implicitness | Not as a tool (old Java, not packaged); its lexicons can be reused | Its "multiplicity" and "implicitness" overlap p2 and anaphora, which are noisy here |
| **Smella** (Femmer et al., JSS 2017) | ISO 29148 smells: subjective, loophole, open-ended, superlative, comparative, negative, vague pronoun, incomplete reference | Research prototype, not maintained | Reimplementable; results as §3: low causal yield |
| **Paska** (Veizaga et al., TSE 2024) | Smells plus recommendations, over the Rimay controlled language | Research artefact for a different CNL | Its idea, a smell with a suggested rewrite, fits the skill and the judge |
| **RETA / Arora et al.** (TSE 2015) | Conformance to Rupp and EARS templates, by chunking in GATE | Not needed | `model_parse.ears` already does EARS conformance; all 539 lines pass |
| **INCOSE GtWR v4 rules** (R1–R42) | Rules such as active voice, single thought, no pronouns, defined terms | As a rubric, yes. The implementations (QVscribe, The Reuse Company RQA, IBM RQA) are commercial and cloud-based. | Use R18 (one thought), R5/R6 (defined terms), R31 (no solution or implementation) and R27 (explicit conditions) in the skill and Haiku rubric |
| **NAI / anaphora and coordination ambiguity** (Yang, de Roeck et al. 2010–11; Chantree 2006; TAPHSIR, Ezzini et al., ICSE 2022) | Nocuous anaphora and coordination | Research code (TAPHSIR on SpanBERT) | Anaphora caused none of the 42 questions. Not worth it. |
| **FRET / FRETish** (NASA) | Structured English → past/future MTL; realizability and conflict checks | **No**, as a tool | Built for reactive Boolean signals and timing. Our responses are discrete workflow actions. Its scope/condition/component/response split is the same as §1's parse, and its realizability check is our c1 in temporal form. |
| **ARSENAL** (SRI) / **nl2spec** (LLM → LTL) | NL → temporal logic | No | Not available, or an LLM pipeline aimed at LTL; same mismatch as FRET |
| **EARS-CTRL** (Lúcio et al.) | EARS → controller synthesis | No | Same mismatch |

## 6. Recommended architecture, as candidate request lines (proposals only; the upstream owns wording)

1. **When** `model check` reads two Behaviour lines of one capability whose triggers name one event of one subject and
   no qualifier separates, and whose responses set different statuses or one starts what the other withholds,
   `model check` shall print them as a warning naming both ids.
2. **When** `model check` reads a Behaviour line whose trigger is that a round of a kind ends, with at most one
   qualifier, and another line whose trigger is a specific outcome of a round of that kind with a different response,
   `model check` shall print them as a warning naming both ids.
3. **When** `work request` is given a line that uses a word of the implementation list or a word that is neither a term
   nor used elsewhere in `spec/capabilities/`, `work request` shall print the word with the line as a warning.
4. **When** `work request` is given a line whose trigger overlaps an existing or retired line with the same response,
   and the line names neither, `work request` shall print the existing line's id as a warning.
5. **When** a round of the kind `integrate` ends with a change list, `work run` shall give the round of the kind `gate`
   the warnings `model check` prints for the drafted lines.
6. **Where** a judge model is configured, **when** `work request` is given a line, `work request` shall print the judge's
   verdict on the line's responses, keyword, terms and implementation detail as a warning.

**Build order:** 3 (lexicons; cheap; #1, #30, #31), then 1–2 with a frozen ontology (§2), then 4, then 5. Build 6 only after the §4 eval
passes.

**The ontology table** (event implications, disjoint qualifiers, system aliases) needs a home and an owner. A spec
glossary-like section is the natural place. Raising it is a question for the person.

## 7. What I could not determine

- **Haiku's actual accuracy.** I did not call the API. §4 is a design and a plan, not a measurement.
- **A blind score for layer (b).** The ontology was tuned on the record it is scored against. Only the next requests
  give an honest number.
- **The drafts behind q14–q23** (`runs/` integrate drafts). I ran the request lines and the spec snapshots, not the
  writer's intermediate drafts. I did not read i43 `runs/` or i44 at all.
- **Whether each flag would actually have stopped the question,** given the person's "no line overrides another" ruling
  (sibling §3.1). Flagging r83 × r152 tells the writer to retire and replace, or to name the exception, and which is
  allowed is the person's open decision.
- **Stanza or benepar,** which were not installed or tried. LanguageTool, Vale and the research tools were assessed from
  their published scope, not run.
