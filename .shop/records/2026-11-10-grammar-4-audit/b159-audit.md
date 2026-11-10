# Audit: can grammar 4 say b159's lines? (decision-tiers, pr-review, intake, conversation, brainstorming)

Scope: 31 lines. That is b159's 28 grammar-4 rewordings (decision-tiers r13-r23, pr-review r10-r16, intake r10-r13,
conversation r5-r8, brainstorming r4, r5) plus the 3 lines kept unchanged (pr-review r1, r4; brainstorming r2). In
spec/ these five capabilities are still `codified-1`, and no other item has added grammar-4 lines to them. So I laid
b159 onto a copy of spec/ (`backlog_lines.lay_onto`) and ran `model parse --form` on every line. All 31 parse, each to
one logical form (forms.txt beside this file). Each verdict compares the form with the retired line, with the phase 3
candidate (a.tsv, b.tsv) and with what the share reports say the candidate could not say.

## Counts

| verdict | lines |
|---|---|
| fine | 17 |
| distortion | 10 |
| unsayable | 2 |
| coined | 2 |

By capability: pr-review 8 fine, 1 unsayable. decision-tiers 5 fine, 4 distortion, 2 coined. intake 4 distortion.
conversation 2 fine, 1 distortion, 1 unsayable. brainstorming 2 fine, 1 distortion.

## Missing constructs, with the number of lines each

| construct | lines | where |
|---|---|---|
| Coordinated values / value-set membership ("is not A, B or C", "is one of") | 3 | decision-tiers r13, r23; intake r10 |
| A negated argument in the trigger ("runs C without an option C requires") | 2 | decision-tiers r20, intake r13 |
| Attribute absence ("has no tier") | 1 | decision-tiers r13 |
| "For each X, its Y" in a response list ("every item with its title") | 1 | conversation r8 |
| Eventually / liveness (deferred to b127) | 1 | pr-review r1 |
| An outcome of the response's own act ("a test that fails when `model` runs it") | 1 | decision-tiers r17 |
| A definite singleton (`This:` or exactly one, for "the decisions index") | 1 | decision-tiers r19 |
| A verb whose gloss hides a condition and a second relation | 1 | decision-tiers r22 (verify) |
| A relation between two lines (counter-proposal), the owner of a reason, a location adjunct, a second object | 3 | intake r11, r12; conversation r6 |
| Roles the frame does not show (quote's words and message) | 1 | brainstorming r5 |

## The worst examples

- **decision-tiers r13** (untiered). The line reads: "While a design-decision is not `superseded` and the
  design-decision is not `rejected` and the design-decision is not `check` and the design-decision is not
  `requirement` and the design-decision is not `judgement`, ...". It lists five values because "has no tier" cannot
  be said. The meaning also changes. The Implementation calls a tier outside the three a file problem, not a
  `w_untiered`, but this line now warns on such a tier too. This is the phase 3 gap ("absence is not a value") left
  open and covered over with values.
- **decision-tiers r22** (unrouted). The verb `verify` is glossed "a design-decision that is not `superseded` or
  `rejected` names a route ... under its `verified_by` and a universal condition under its `rests_on`". That gloss
  holds a status condition and two field relations. This is the anti-goal "meaning hides in the glossary" in a
  verb's clothing. The line also puts the condition into the trigger's `on` slot ("runs `model check` on a universal
  condition"), which `model check` does not take. b188 forced this: a negated restriction on a response object has
  no translation.
- **decision-tiers r23** (misrouted). "the route list" is a proper noun of kind text whose gloss holds the four
  route values. The membership check runs against a list kept only in the glossary. `route` should be an attribute
  of design-decision with `Values:`.
- **conversation r8**. "print every item, every title of an item and every batch" makes three independent `every`
  boxes. The pairing of each item with its title, which is the whole point of the names table, is gone.
- **pr-review r1** (kept). Phase 3 found that the batch session dispatches the reviewer after `work batch brief`,
  and that a review follows publication eventually, not at the next step. Grammar 4 reads When as the next step and
  has no "eventually", so the kept line states an obligation the system does not meet.
- **decision-tiers r20 and intake r13**. "While `work decision` requires an argument that `work decision` does not
  have" makes the static row `argument | of | command` stand in for "not given on this command line". What a run was
  given belongs to the run, not to the command. The candidate's "runs C without ..." has no grammar-4 form, because
  only "with the X option" exists.

## Which distortions a rewording alone could fix

- **decision-tiers r19**: say "the decisions index" once the noun gets `This:` (or a necessity "exactly one"). This
  needs a glossary edit, not grammar.
- **intake r11**: add a verb `counter` (Frame: request line counters request line) so the new line is tied to the
  one it replaces. Say "post a comment on the issue of the request". Replace the participle row `proposed in` with a
  verb `propose` (the same frame b158 and pr-review use) or a preposition from call 14's set.
- **intake r12**: "write a reason for the request line", with a row, and a noun or sense that is not the CLI pack's
  error `reason`.
- **conversation r6**: "write a file in the git directory that names the session and the transcript of the session"
  (rows for location and transcript). Move the prompt hook's rule out of its gloss.
- **brainstorming r5**: give quote a frame with the words ("session quotes words of agent") or say "run `work quote`
  on the person's words". The gloss then stops adding roles.
- **decision-tiers r23** (coined): make `route` an attribute with `Values:`. The glossary plus a rewording do it if
  "a design-decision whose route is not one of its values" can be read, and today that hits the value-coordination
  gap.

These need grammar or logic work and cannot be fixed by rewording:

- value coordination and attribute absence: r13, intake r10
- a negated argument in the trigger: r20, intake r13
- "for each X its Y": conversation r8
- liveness (b127): pr-review r1
- the outcome of the response's own act: r17
- a negated restriction on a response's object (b188), behind r22's misplaced trigger

## Judgement

17 of 31 lines are fine. All of pr-review's rewords are fine except the kept r1: the noun-phrase constructs (of, no,
has, relative clauses, whose, only, every) did their job there, and the b118 faults are fixed. The trouble sits in
decision-tiers and intake, where two old coined adjectives (untiered, settled) became value lists, and two (unrouted,
misrouted) became a gloss-loaded verb and a gloss-held list. That is the "coined adjectives come back under another
name" anti-goal at a smaller scale. Only 2 lines are truly unsayable, and both are on constructs the design deferred
or never named ("for each X its Y" is not in sections 6-7).
