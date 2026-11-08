# Requirement CNLs with formal and temporal semantics, and their path to tests and monitors

Phase 1 of the b112 research. Strand: the requirement languages of formal methods and requirements engineering (NASA FRET,
EARS and its formalisations, the property specification patterns, Rimay, SpeAR, the MASTeR templates, Stimulus, work
that generates BDD scenarios), and how each one reaches tests and runtime monitors. The last two sections compare them
with this repository, mostly hypothesis 3 (time) and the owner's verification routes.

Sources are cited inline and listed at the end. Where I could read only an abstract or a secondary source, the text says
so. The formulas in LTL that follow FRET or Dwyer examples are my own renderings of the published meanings. They are not
copied from the papers.

## 1. The short answer

- **Every mature requirement CNL with formal semantics puts time in fixed fields, not in the vocabulary.** FRETish has
  `scope` (an interval of modes), `condition` (a trigger, read as an edge or as a level), and `timing` (immediately,
  next, within N, for N, until, eventually, always, never). EARS has its keyword clauses (While, When, If-then, Where).
  The Dwyer patterns give a pattern plus a scope (globally, before Q, after Q, between Q and R, after Q until R). This
  repository has EARS's clauses but no timing field and no scope. The meaning of "only after" and "always running" has
  nowhere to live, so it ends up in coined adjectives or in prose.
- **FRET is the closest model for this repository's goals.** One structured sentence gives a formula. The semantics is
  composed from three fields, 160 keys in classic FRET. From that one formula FRET generates test cases (FLIP coverage,
  model checking), contracts for model checkers (CoCoSpec/Kind 2), a realizability check, and runtime monitors through
  Ogma and Copilot. **The monitors use the past-time form of each formula.** A past-time formula needs only the current
  sample plus a few history bits, so it can be checked by sampling a running system.
- **Past time is cheap and fits a two-state checker. Future time is not cheap.** "Only after", "once", "since" and
  "previously" compile to history fluents that one event sets. That is exactly the shape of the repository's
  `set(...)` facts, so a precedence rule ("a method receives a request only after the server processes it") can become
  a state invariant over a history fluent without adding traces to `check.lp`. True liveness ("eventually") cannot be
  refuted on a finite trace. Every practical monitor tool bounds it ("within N"), and so should this repository's
  monitored lines.
- **The owner's example of liveness is safety.** "A background task is always running" is G(running), an invariant
  checked at every sample. A real liveness line is "every request is eventually checked". In the form "within 30 s" it
  becomes a bounded response, which a monitor can check.
- **Tests and monitors split cleanly by pattern.** An effect rule (a trigger and a response at the next state) is a
  scenario. Invariants and bounded responses are monitors, or checks after every scenario. This repository already does
  the second for U4, U8 and U11 in `tests/scenarios/vocab.py`. Precedence rules are monitors with history, or invariants
  over a history fluent.

## 2. NASA FRET and FRETish

**What it is.** FRET (Formal Requirements Elicitation Tool), from NASA Ames, lets a user write requirements in FRETish,
a restricted English. For each requirement it shows the formula, a natural-language explanation of the semantics, and a
timing diagram ([FRET repository][fret-gh]; [user manual][fret-manual]). The key paper is Giannakopoulou, Pressburger,
Mavridou & Schumann, *Automated formalization of structured natural language requirements*, Information and Software
Technology 137, 2021. Its predecessor is *Generation of formal requirements from structured natural language*, REFSQ
2020.

**Sentence structure.** A requirement has up to six fields (seven in probabilistic FRET):
`[scope] [condition] component shall [timing] response`. Component, shall and response are mandatory
([writingReqs][fret-fields]).

| Field | Options |
|---|---|
| scope | none (global); `in M` (also `during`, `when in`, `while`); `not in M` (also `except in`, `unless in`); `before M`; `after M`; `only in`, `only before`, `only after` (the response must *not* hold outside the interval) |
| condition | *regular*, `upon C` (also `when`, `where`, `if`): fires at the moment C **becomes** true (false to true). *Holding*, `whenever C`: fires at every point where C is true |
| component | the system element the requirement constrains |
| timing | `immediately`, `at the next timepoint`, `eventually` (the default), `always`, `never`, `within N`, `for N`, `after N`, `until S`, `before S`, `finally` |
| response | a boolean expression the component satisfies (`satisfy p`) |

The scope and condition semantics are taken from the description of classic FRETish in Mavridou et al., *Automated
formalization of probabilistic requirements from structured natural language*, arXiv 2512.15788 ([html][fret-prob]). The
manual adds temporal predicates for conditions and responses: `persisted(n,p)`, `occurred(n,p)`, `persists`, `occurs`,
`prevOcc`, `nextOcc`, `preBool`.

**Examples.**

- "In flight mode the battery shall always satisfy voltage > 9" (the manual): scope `in flight`, timing `always`. My
  rendering: G(flight → voltage > 9).
- "whenever idealConditions SensorSelection shall immediately satisfy q_hat = q" (arXiv 2512.15788, requirement
  P-001): a holding condition with immediate timing, template key `[null, holding, null, immediately]`.
- A ROS 2 example in Perez, Mavridou et al. 2022 ([arXiv 2209.14030][ros]): the condition
  `persisted(10, current_consumption > cc_t & wind_speed > ws_t)`, the timing `within 10 seconds`, and the response
  `current_consumption <= cc_t`.

**Semantics.** FRETish is given a formal semantics in Real-Time Graphic Interval Logic. FRET emits, for every
requirement, future-time metric LTL over finite traces, past-time metric LTL (both in SMV syntax), and PCTL for the
probabilistic variant ([semantics overview][fret-sem]). The translation is compositional. The timing field gives a
formula, which is then restricted to the scope's intervals (through SALT). The condition decides whether the formula is
anchored at each rising edge or at each point. Conrad, Titolo, Giannakopoulou, Pressburger and Dutle gave a denotational
semantics and a mechanised proof that the generated formulas agree with it: *A compositional proof framework for
FRETish requirements*, CPP 2022 ([pdf][fret-cpp]).

**Modes and states.** States enter FRET in two ways. A *mode* is a named boolean expression that the scope fields cut
into intervals ("in landing mode"), and several separate intervals are allowed. A *condition* is a boolean over
variables. The regular/holding split is FRET's answer to the state-versus-event question. `upon C` turns the state C
into an event (its rising edge). `whenever C` keeps it as a level. There is no separate event vocabulary: an event is
always the edge of a boolean.

**Tests.** FRET generates test cases with the FLIP coverage criterion. For each atomic proposition of a requirement's
LTL formula, it produces one test obligation: the formula extended so that the proposition's own effect is exposed. A
model checker then solves the obligations: NuSMV on the finite-trace future-time formulas (Boolean components only,
default length 4), or Kind 2 on the past-time ones. A test is a finite trace with a value for each variable at each step
([testgen manual][fret-testgen]). This descends from the unique-first-cause coverage of Whalen, Rajan, Heimdahl & Miller,
*Coverage metrics for requirements-based testing*, ISSTA 2006. That lineage is my inference: the manual names FLIP but I
did not confirm the line of descent.

**Model checkers and realizability.** FRET exports CoCoSpec contracts for CoCoSim/Kind 2 on Simulink models, checks
realizability with JKind or Kind 2, and checks consistency between requirements. Case studies include Mavridou et al.,
*The ten Lockheed Martin cyber-physical challenges: formalized, analyzed, and explained*, RE 2020 ([NTRS][lm10]), and
Luckcuck, Farrell, Sheridan & Monahan, *FRETting about requirements: formalised requirements for an aircraft engine
controller*, REFSQ 2022 ([arXiv 2112.04251][fretting]).

**Runtime monitors (Ogma, Copilot).** Ogma reads FRET's component specification, which carries the *past-time* MTL
formulas, and writes Copilot monitor specifications. Copilot, a Haskell stream DSL, compiles them to hard real-time C99
with constant memory. Ogma can also wrap the monitors as NASA cFS applications or ROS 2 packages. Sources: Perez,
Mavridou, Pressburger, Goodloe & Giannakopoulou, *Automated translation of natural language requirements to runtime
monitors*, TACAS 2022 ([Springer][tacas22]); Perez et al., *Monitoring ROS2: from requirements to autonomous robots*,
2022 ([arXiv 2209.14030][ros]); the [ogma-cli][ogma] package.

How the sampling works: the host program writes the latest value of each input variable into a global, then calls the
monitor's `step()`. A violation calls a handler (in ROS 2, a message on a topic `copilot/handler...`). The ROS 2 paper
notes that violation messages carry no values or timestamps, and that every monitor is re-run on every input. Neither
paper I read explains how a future-bounded response ("within 10 seconds") is turned into a past-time monitor. I believe
it is checked with a delay, as "if the trigger occurred 10 s ago, the response has occurred since", but I did not
confirm this.

**Why past time for monitors.** A past-time LTL formula can be checked by a monitor that keeps one bit per subformula
from the previous step: Havelund & Roşu, *Synthesizing monitors for safety properties*, TACAS 2002. Future-time
liveness has no finite bad prefix. Bauer, Leucker & Schallhart's three-valued LTL3 (*Runtime verification for LTL and
TLTL*, TOSEM 2011) gives such a formula the verdict "inconclusive" for ever. Bounded timing (`within N`) turns liveness
into safety, and that is why FRET's monitorable requirements are bounded.

## 3. EARS and its formalisations

**EARS itself.** Mavin, Wilkinson, Harwood & Novak, *Easy Approach to Requirements Syntax (EARS)*, RE 2009; Mavin &
Wilkinson, *Big Ears (the return of Easy Approach to Requirements Syntax)*, RE 2010. The patterns, with the examples on
the official page ([alistairmavin.com/ears][ears]):

| Pattern | Template | Example (verbatim) |
|---|---|---|
| Ubiquitous | The <system> shall <response> | "The mobile phone shall have a mass of less than XX grams." |
| State-driven | While <precondition(s)>, the <system> shall … | "While there is no card in the ATM, the ATM shall display "insert card to begin"." |
| Event-driven | When <trigger>, the <system> shall … | "When "mute" is selected, the laptop shall suppress all audio output." |
| Optional feature | Where <feature is included>, … | "Where the car has a sunroof, the car shall have a sunroof control panel on the driver door." |
| Unwanted behaviour | If <trigger>, then the <system> shall … | "If an invalid credit card number is entered, then the website shall display "please re-enter credit card details"." |
| Complex | While …, when …, the <system> shall … | "While the aircraft is on ground, when reverse thrust is commanded, the engine control system shall enable reverse thrust." |

EARS's own guidance: the clauses always appear in the same order (it calls this order "temporal logic"). A requirement
has zero or many preconditions, zero or one trigger, one system name, and one or many responses. The subject is always
"the <system name>". A state-driven requirement is active for as long as its state holds. An event-driven one responds
when its trigger occurs.

What EARS does not give: timing (no "within"), ordering between events, scopes ("before"/"after"), quantification over
the system's objects, and any semantics beyond that informal reading. The official page lists no limitations. It says
EARS "gently constrains" text. These limits are therefore my reading, supported by the existence of T-EARS (below),
which was created to add timing.

The informal meanings carry over to formulas directly. *While C, S shall R* with no trigger is G(C → R): an invariant
over the interval of C. It is not a response to a trigger. *When T, S shall R* is G(T → X R) or G(T → F R), and EARS
does not say which. The difference matters for this repository, below.

**EARS-CTRL.** Lúcio, Rahman, Cheng & Mavin, *Just formal enough? Automated analysis of EARS requirements*, NFM 2017.
EARS sentences are written in a projectional editor (MPS) over a glossary of controller terms, translated to LTL, and
handed to a controller synthesis tool. The tool checks realizability and synthesises a controller, shown as a dataflow
diagram. Also Lúcio & Iqbal, *Formalizing EARS – first impressions*, EARS workshop 2018, which explores the EARS-to-LTL
translation in practice. I read only the abstracts and fortiss listings ([fortiss][earsctrl]), so I cannot quote the
translation table.

**T-EARS (Timed EARS) and passive testing.** Flemström, Enoiu, Afzal, Sundmark, Gustafsson & Kobetski, *From natural
language requirements to passive test cases using guarded assertions*, QRS 2018 ([MDU][tears18]). T-EARS adds timing
keywords such as "within". A requirement becomes a *guarded assertion*: a guard says when the system is in a testable
state, and an assertion says the response expected while it is. These are evaluated *passively* over logs of a running
system. They are not driven by a test. A 2025 industrial study at Volvo CE (Nicaj, Flemström, Enoiu & Afzal, ICTSS 2025,
[listing][tears25]) reports that most functional requirements could be written as guarded assertions and checked on
logs. This is the closest published analogue to the owner's "runtime monitors that sample the running system": a
requirement checked against recorded traces rather than exercised by a scenario.

**EARS to event calculus in ASP.** Hall, Varanasi, Fiedor, Arias, Basu, Li, Bhatt, Driscoll, Salazar & Gupta,
*Knowledge-assisted reasoning of model-augmented system requirements with event calculus and goal-directed answer set
programming*, HCVS 2021, EPTCS 344 ([arXiv 2109.04634][ec]). This is the nearest relative of this repository's own
pipeline. EARS-style requirements become event calculus in s(CASP), an answer set programming system with constraints.
The mapping is:

1. each object state is a fluent;
2. the WHEN trigger becomes `happens(Event,T)`;
3. the response becomes `initiates`/`terminates`, with a `holdsAt` qualifier for every WHILE precondition;
4. a durative change ("while the door is opening, the door position shall increase at most 5 degrees per second")
   becomes a `trajectory` predicate.

Example requirement (from the paper): "While the aircraft is on-ground, when the requested door position becomes open,
the door control system shall change the state of the cargo door from closed to open within 10 secs." It is encoded
with `initiates(pilot_requests_door_to_open, door_state(open), T) :- holdsAt(aircraft_state(on_ground), T).` and a
time-bounded `happens` whose bound is a constraint (`T2 #=< T1+10`). The paper says IF maps exactly like WHEN; IF
differs only in naming off-nominal events. "Upon initialization" becomes `initiallyP`. Because the encoding has
time points, s(CASP) can simulate runs from initial conditions and find gaps with abductive queries. Note the word
"becomes": like FRET's `upon`, it turns a state into an event.

## 4. Specification patterns

**Dwyer, Avrunin & Corbett**, *Patterns in property specifications for finite-state verification*, ICSE 1999. Their
survey of about 500 real specifications found that a handful of patterns covered almost all of them. Each pattern
combines with a scope.

| Pattern | Structured English (PSP style) | LTL, global scope |
|---|---|---|
| Absence | it is never the case that P holds | G ¬P |
| Universality | it is always the case that P holds | G P |
| Existence | P eventually holds | F P |
| Bounded existence | P holds at most k times | … |
| Precedence | if P holds, then S previously held ("S precedes P") | ¬P W S |
| Response | if P holds, then in response S eventually holds | G(P → F S) |
| Chain precedence / response | sequences of the above | … |

The scopes are: globally, before R, after Q, between Q and R, and after Q until R. A scope is the interval over which
the pattern must hold. Response is the most common pattern in their data, then universality and absence.

**Konrad & Cheng**, *Real-time specification patterns*, ICSE 2005, add metric versions: minimum and maximum duration,
bounded recurrence, bounded response ("if P holds then S holds after at most c time units"), bounded invariance. They
also give a structured English grammar that generates sentences such as "Globally, it is always the case that if P
holds, then S holds after at most c time units." **Autili, Grunske, Lumpe, Pelliccione & Tang**, *Aligning qualitative,
real-time, and probabilistic property specification patterns using a structured English grammar*, IEEE TSE 41(7), 2015,
unify the three catalogues under one grammar (the PSPWizard tool), with mappings to LTL, MTL, TCTL and PCTL. A related
catalogue ([arXiv 2211.03817][rtcat]) generates observer automata and TCTL for UPPAAL.

This is the shape of a CNL whose semantics comes from structure. The grammar has a scope clause, a pattern clause and a
time bound, and the formula is fixed per (scope, pattern) pair. FRET's 160 template keys are the same idea.

**The owner's categories mapped onto the patterns:**

| Owner's category | Example (owner's or this repository's) | Pattern | Formula (sketch) | Verification route |
|---|---|---|---|---|
| Effect rule | "When the person runs `work outcome` on a request that is `open`, `work` shall write a line outcome" (requests r14) | Response with *next* timing (a Hoare triple) | G(open(q) ∧ run(outcome,q) → X written(o)) | Gherkin scenario: one trigger, its post-state |
| Structural / ordering rule | "a method receives a request only after the server processes it" | Precedence | ¬receive W processed, or past-time G(receive → O processed) | Monitor with one history bit; or an invariant over a fluent `processed`; or a check over logs |
| State invariant | "a list has items or is empty"; U7 "A worker shall change only files in its worktree" | Universality / absence, global or in a scope | G(items>0 ∨ empty); G ¬(change(f) ∧ f∉tree) | Check after every scenario (as U4/U8/U11 now), a static check, or a monitor |
| Transition rule | "the server checks every request" | Response (liveness), or bounded response | G(arrive(r) → F checked(r)); bounded: G(arrive(r) → F≤30s checked(r)) | Unbounded: judgement or a bounded rewrite. Bounded: a monitor |
| Liveness | "a background task is always running" | **Universality**, a safety property, despite the name | G running(task) | Monitor sampling `running`. Real liveness is "… is eventually restarted" (response) |

Two remarks. "Always running" is safety, and a monitor can refute it at the first sample where the task is down. The
owner's word "liveness" fits "every request is eventually checked" better, and that line cannot be refuted on a finite
run unless it is bounded. Second, the structural rule's "only after" is the Dwyer *precedence* pattern. It needs past
time but **no future**, so it is monitorable, and section 7 argues it is checkable with the existing two states.

## 5. Other requirement CNLs and requirements-to-test work

**Rimay** (Veizaga, Alférez, Torre, Sabetzadeh & Briand, *On systematically building a controlled natural language for
functional requirements*, Empirical Software Engineering 26, 2021; preprint [arXiv 2005.01355][rimay]). Rimay was built
by qualitative analysis of 15 financial-domain SRSs (3,215 statements), not by design from logic. It covered 88% (405
of 460) of the statements in four unseen SRSs. As I recall it, the grammar is EARS-like: an optional condition
(when/if/while, before/after), an actor, a modal verb, and a system response built from about a dozen verb classes. It
has no formal semantics; its value is coverage and smell detection. I could not extract its examples from the PDF, so I
give none. Treat the description of its structure as unverified. The same group (Alférez et al., *Bridging the gap
between requirements modeling and behavior-driven development*, MODELS 2019, [UL listing][bddgap]) generates Gherkin
acceptance criteria from UML requirement models. That is the one academic requirements-to-Gherkin line I found that is
not LLM-based.

**SpeAR** (Fifarek, Wagner, Hoffman, Rodes, Aiello & Davis, *SpeAR v2.0: formalized past LTL specification and
analysis of requirements*, NFM 2017; [repository][spear]). AFRL's language: requirements relate monitored (input)
variables to controlled (output) variables in a structured but formal syntax with **past-time** LTL operators
(`previously`, `historically`, `since`, `triggers`). They are compiled to Lustre synchronous observers and analysed with
JKind for consistency, realizability, and logical entailment ("do the requirements imply this property?"). The choice
of past time, as in FRET's monitor path, keeps every property an observer over a finite history.

**MASTeR templates** (SOPHIST: Rupp et al., *Requirements-Engineering und -Management*, Hanser; the English *MASTeR*
booklets). This is from my own knowledge; I did not fetch a source. The template is
`[condition] THE SYSTEM {SHALL | SHOULD | WILL} {<process verb> | PROVIDE <whom> WITH THE ABILITY TO <verb> | BE ABLE TO <verb>} <object> [details]`.
It has separate templates for function, property, environment and condition, and the condition template has event,
logical and time variants. Its relevance here is modality: shall (legally binding), should (desired), will (future
intent). It also distinguishes "the system <verbs>" (autonomous), "provides the ability to" (user interaction), and "is
able to" (interface).

**Stimulus** (Argosim, now Dassault Systèmes). Requirements are written in a template language with temporal
connectives ("when … then … during …", "… shall be true within …"). The tool *simulates the requirements themselves*,
with no implementation: it produces random traces that satisfy all the requirements together, so an engineer sees
under-specification and conflicts, and it derives test observers from them. Source: Jeannet & Gaucher, *Debugging
embedded systems requirements with STIMULUS: an automotive case-study*, ERTS 2016. I cite this from memory and did not
re-fetch it, so check the exact title.

**Requirements to BDD.** Beyond Alférez et al., the recent work is LLM generation of Gherkin from free text (for
example [arXiv 2603.04729][llmbdd], comparing GPT-4, Claude 3 and Gemini), plus vendor tools (Conformiq SmartGen,
SpiraTest). I found **no** paper that generates Gherkin deterministically from a requirement CNL's formal semantics, as
this repository does. FRET's test generation is the formal counterpart. Its tests are traces of variable values, not
Given/When/Then text, and it covers each proposition (FLIP), while this repository writes one scenario per group.

## 6. How these languages handle the hard parts

| Concern | FRET | EARS | Dwyer / Konrad-Cheng | SpeAR | EARS→EC (s(CASP)) | This repository |
|---|---|---|---|---|---|---|
| States vs events | an event is the rising edge of a boolean (`upon`); a state is a level (`whenever`, a mode) | When (event), While (state); informal | P, Q, R are propositions; events are edges | variables; `previously` | fluents with `holdsAt`; `happens` | trigger = verb/`runs` event; While = conditions in state 0 |
| Durative process ("while X runs") | scope `in M` (several intervals); timing `for N`, `until S` | While (informal) | scopes between Q and R; durations | `historically`, `since` | `trajectory`; fluents over intervals | none; While is read only at the trigger's instant |
| Ordering ("only after") | `only after M`; `prevOcc`, `occurred` | none | precedence, chain patterns | `since`, `previously` | time-point constraints | none |
| Invariants | timing `always` / `never`, any scope | ubiquitous; While without When | universality / absence | relations over all steps | constraints over all T | ubiquitous lines and U*; a check against untriggered lines at state 1 |
| Bounded response | `within N`, `after N` | none (T-EARS adds "within") | bounded response | via counters | `#=<` constraints | none |
| Modality | shall only (probability in P-FRET) | shall | n/a | n/a | n/a | shall / shall not |
| Tested by | FLIP test traces (model checker) | — | — | entailment checks | simulation, abduction | Gherkin per group |
| Monitored by | Copilot via Ogma (past-time MTL) | T-EARS on logs | observer automata | Lustre observers | — | U4/U8/U11 checked after each scenario |

## 7. Compared with this repository

**What the repository has.** `grammar/Req.gf` gives the six EARS forms and their combinations (Ubiq, When, While,
Where, IfThen, WhileWhen, WhereWhen, WhereWhile, WhileIf, WhereIf), with `shall` and `shall not` responses. Triggers are
events: a verb's frame ("a session writes a file"), `Runs`, `IsRun`. Conditions are atoms over the pre-state.
`grammar/check.lp` reads each pair of requirements over **two states**. State 0 is the pre-state, where the trigger
happens. State 1 is state 0 plus the triggered side's `set`s. An untriggered requirement paired with a triggered one is
read at state 1. "If" requirements are exceptions that win over the others on their trigger. `scripts/spec_steps.py`
reads the same facts into Givens (the While conditions and the pre-state), one When (the trigger) and Thens (the
responses and sets). `features/requests.feature` shows the result, for example r14's scenario "Given a request q1 that
is `open` / When the person runs `work outcome` on the request q1 / Then `work` writes a line outcome".

In pattern terms, every triggered line is a **response with next timing** over a single step: a Hoare triple. That is
FRET's `upon C, S shall at the next timepoint satisfy R` with no scope. The checker and the generator agree on that
reading, and for this repository's own subject (CLI commands that run to completion) it is mostly the right one. A
command's "response" is its effect at exit.

**Hypothesis 3 (time) is confirmed in shape, with a narrower remedy than it suggests.**

1. *No edge/level distinction, but no need for one yet.* The repository's triggers are already events (verbs), never
   states becoming true. Where a state change must trigger something (feed's "a video becomes available", say), FRET
   and the EC paper both use "becomes". This is one fixed structure, `Becomes : NP -> Cond -> Trig`, read as
   "¬C at state 0, C at state 1, of the trigger's own side". It is not a coined adjective.

2. *While means "at the trigger's instant", not "throughout".* In EARS and FRET, *While C, S shall R* without a trigger
   is G(C → R): R holds for as long as C does, which is an invariant over an interval. The repository's While clause is
   read only in state 0 of one trigger. For WhileWhen lines that is the same as FRET's
   `in C upon T shall next R`. For a **While-only** line (state-driven, no trigger) the repository has no reading
   except as an untriggered side at state 1. That line is an invariant, and its route is a check or a monitor, never a
   scenario. The generator should say so rather than build one.

3. *Ordering needs past time only, and past time compiles to fluents.* "A method receives a request only after the
   server processes it" is precedence: G(receive(r) → O processed(r)). A past-time operator is a history variable
   updated at each step (Havelund & Roşu). Here it is a fluent `processed(r)` that the processing event `set`s and
   nothing unsets. The rule then becomes a state invariant over it: "While a request is not processed, a method shall
   not receive the request." That is checkable in the existing two-state `check.lp`, testable as a scenario (Given
   not processed / When receive is attempted / Then refused), and monitorable with one bit. Concretely:
   - a grammar structure `… only after <event clause>` that writes the fluent and the guard;
   - spec_facts adds a `set` of the history fluent to every line whose response is that event.

   No trace semantics is needed. SpeAR and FRET's monitor path both stay within past time for this reason.

4. *Durations, "eventually" and "within N" are where two states truly fall short.* "Within 30 s", "for N", "until S"
   and "eventually" need either a metric trace or a monitor. A monitor is the sensible place, and these lines' routes
   are runtime monitors. The grammar would need a timing slot (FRET's field, with a small fixed set of values:
   immediately, within <duration>, always, never, until <clause>). `check.lp` could treat any timing other than
   "immediately" as opaque for clash-finding, as it treats prose conditions now (L6), and leave it to the monitor.

5. *Durative processes ("while a batch is building", "while the watch runs").* A process is a mode in FRET's sense: an
   interval between a start event and an end event. The pattern literature calls this the "between Q and R" scope. In
   fluents it is `building` set by `work batch start` and unset by `work batch review`. The repository already
   represents this as an attribute value (a batch that is `building`), so durative processes are modelled; what is
   missing is the reading of a While-only line over the interval.

**The owner's verification routes against the literature.**

- *Scenarios "only for what is not already entailed".* FRET's FLIP and SpeAR's entailment checks both ask whether a
  property follows from the others, and both use a model checker. The repository's ASP checker could do the same for
  untimed lines, once invariants are premises: is a scenario's Then entailed by the invariants plus the effect rules?
- *Runtime monitors that sample.* The FRET → Ogma → Copilot path is the reference design. Monitors take past-time
  formulas; inputs are sampled variables; a step function runs per sample; a violation calls a handler. T-EARS's
  passive testing over logs is the lighter variant, and fits a CLI-and-git system well: the "samples" are command runs,
  commits and issue comments, which are already logged. **The repository has a seed of this**:
  `tests/scenarios/vocab.py` checks U11, U4 and U8 after every generated scenario. That is a monitor sampled at the end
  of each scenario. A `verified_by: monitor` route on a decision could generalise it: the invariant compiled to a check
  run at each sample point (each command's exit in tests, each hook or `work watch` wake in use).
- *Which requirements need which route.* The patterns answer it mechanically:

  | Pattern | Route |
  |---|---|
  | Response with next timing | scenario |
  | Universality / absence, and bounded response | monitor or check |
  | Precedence | invariant over a history fluent (scenario plus monitor) |
  | Unbounded liveness | judgement, until it is bounded |

  This supports the owner's view that the route lives on a decision. It also suggests the route can be *proposed*
  from the line's pattern, and confirmed by the decision.
- *Modality.* None of FRET, EARS or SpeAR has "may" or a necessity/obligation split. MASTeR's shall/should/will and
  SBVR's necessity/obligation are the sources for hypothesis 4. FRET's `only in` / `only after` scopes do cover
  "only", which the repository has only for noun phrases (`Only : NP -> NP`).

**Hypothesis 1 (semantics fun by fun).** FRET's semantics is composed from three orthogonal fields into one of 160
templates, proved correct once (CPP 2022). The repository's translation is written per fun in `spec_facts.py`.
Splitting a line into fixed slots (scope or While; trigger with edge/level; timing; response) and giving each slot one
meaning would make the semantics a small table, as in FRET and Dwyer. That table could then be documented, tested and
proved, rather than spread across translators.

**Where the repository is ahead.** None of these systems has a typed domain vocabulary with verb frames, relations and
kind hierarchies feeding the grammar. FRET's responses are raw boolean expressions over variables. EARS's are free
text. Nor does any of them generate readable Given/When/Then. The repository's agent-explicit subjects and frames are
richer than FRET's single `component`, and its ASP checker searches for clashes much as FRET's realizability check
does. The gap is time, not vocabulary.

## 8. Uncertain or unverified

- I did not read the full texts of the FRET IST 2021 and TACAS 2022 papers, of EARS-CTRL, of Rimay or of Stimulus. Their
  details come from the FRET documentation, arXiv 2512.15788, arXiv 2209.14030, abstracts, or my own knowledge, as
  marked.
- How Ogma monitors a future-bounded response (`within N`) with past-time formulas is my inference.
- That FLIP descends from unique-first-cause coverage is my inference.
- The Dwyer and Konrad-Cheng structured English is quoted from memory of the PSP catalogue, and the LTL is my
  rendering.

## Sources

- [fret-gh]: https://github.com/NASA-SW-VnV/fret
- [fret-manual]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/userManual.md
- [fret-fields]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/user-interface/writingReqs.md
- [fret-sem]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/semantics/semanticsOverview.md
- [fret-testgen]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/exports/testgenManual.md
- [fret-prob]: Mavridou et al., *Automated formalization of probabilistic requirements from structured natural language*, https://arxiv.org/html/2512.15788v1
- [fret-cpp]: Conrad et al., *A compositional proof framework for FRETish requirements*, CPP 2022, https://shemesh.larc.nasa.gov/people/amd/publications/CPP2022-Comp-Framework-FRETish.pdf
- Giannakopoulou, Pressburger, Mavridou, Schumann, *Automated formalization of structured natural language requirements*, IST 137, 2021.
- [lm10]: Mavridou et al., RE 2020, https://ntrs.nasa.gov/api/citations/20205000433/downloads/RE2020__CaseStudyPaperFinalVersion%20(10).pdf
- [fretting]: Luckcuck et al., REFSQ 2022, https://arxiv.org/pdf/2112.04251
- [tacas22]: Perez et al., TACAS 2022, https://link.springer.com/chapter/10.1007/978-3-030-99524-9_21 (NASA TM: https://ntrs.nasa.gov/citations/20220000049)
- [ros]: Perez, Mavridou, Pressburger, Will, Martin, *Monitoring ROS2*, https://arxiv.org/abs/2209.14030
- [ogma]: https://hackage.haskell.org/package/ogma-cli
- Havelund & Roşu, *Synthesizing monitors for safety properties*, TACAS 2002. Bauer, Leucker & Schallhart, *Runtime verification for LTL and TLTL*, ACM TOSEM 20(4), 2011.
- Whalen, Rajan, Heimdahl & Miller, *Coverage metrics for requirements-based testing*, ISSTA 2006.
- [ears]: https://alistairmavin.com/ears/ ; Mavin et al., RE 2009; Mavin & Wilkinson, RE 2010.
- [earsctrl]: Lúcio, Rahman, Cheng & Mavin, NFM 2017, https://www.fortiss.org/en/results/scientific-publications/details/just-formal-enough-automated-analysis-of-ears-requirements
- [tears18]: Flemström et al., QRS 2018, https://www.es.mdu.se/publications/5132-From_Natural_Language_Requirements_to_Passive_Test_Cases_using_Guarded_Assertions
- [tears25]: Nicaj et al., ICTSS 2025, https://conf.researchr.org/details/ictss-2025/ictss-2025-general-track/21/Passive-Testing-of-Vehicular-Embedded-Systems-An-Industrial-Case-Study-with-T-EARS-a
- [ec]: Hall et al., HCVS 2021, https://arxiv.org/abs/2109.04634
- Dwyer, Avrunin & Corbett, ICSE 1999; Konrad & Cheng, ICSE 2005; Autili et al., IEEE TSE 41(7), 2015.
- [rtcat]: https://ar5iv.arxiv.org/html/2211.03817
- [rimay]: Veizaga et al., https://arxiv.org/abs/2005.01355 (EMSE 2021)
- [bddgap]: Alférez et al., https://pure.ul.ie/en/publications/bridging-the-gap-between-requirements-modeling-and-behavior-drive/
- [spear]: Fifarek et al., NFM 2017, https://github.com/lgwagner/spear
- [llmbdd]: https://arxiv.org/abs/2603.04729
- Rupp et al. (SOPHIST), MASTeR templates; Jeannet & Gaucher, STIMULUS, ERTS 2016 (from memory).

[fret-gh]: https://github.com/NASA-SW-VnV/fret
[fret-manual]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/userManual.md
[fret-fields]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/user-interface/writingReqs.md
[fret-sem]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/semantics/semanticsOverview.md
[fret-testgen]: https://github.com/NASA-SW-VnV/fret/blob/master/fret-electron/docs/_media/exports/testgenManual.md
[fret-prob]: https://arxiv.org/html/2512.15788v1
[fret-cpp]: https://shemesh.larc.nasa.gov/people/amd/publications/CPP2022-Comp-Framework-FRETish.pdf
[lm10]: https://ntrs.nasa.gov/api/citations/20205000433/downloads/RE2020__CaseStudyPaperFinalVersion%20(10).pdf
[fretting]: https://arxiv.org/pdf/2112.04251
[tacas22]: https://link.springer.com/chapter/10.1007/978-3-030-99524-9_21
[ros]: https://arxiv.org/abs/2209.14030
[ogma]: https://hackage.haskell.org/package/ogma-cli
[ears]: https://alistairmavin.com/ears/
[earsctrl]: https://www.fortiss.org/en/results/scientific-publications/details/just-formal-enough-automated-analysis-of-ears-requirements
[tears18]: https://www.es.mdu.se/publications/5132-From_Natural_Language_Requirements_to_Passive_Test_Cases_using_Guarded_Assertions
[tears25]: https://conf.researchr.org/details/ictss-2025/ictss-2025-general-track/21/Passive-Testing-of-Vehicular-Embedded-Systems-An-Industrial-Case-Study-with-T-EARS-a
[ec]: https://arxiv.org/abs/2109.04634
[rtcat]: https://ar5iv.arxiv.org/html/2211.03817
[rimay]: https://arxiv.org/abs/2005.01355
[bddgap]: https://pure.ul.ie/en/publications/bridging-the-gap-between-requirements-modeling-and-behavior-drive/
[spear]: https://github.com/lgwagner/spear
[llmbdd]: https://arxiv.org/abs/2603.04729
