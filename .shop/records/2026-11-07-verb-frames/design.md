# Verb frames: a controlled grammar built on basic English sentence structure (b82)

## Why

feed's latest-videos r2 parsed:

> While a channel is not subscribed, when a caller with the YouTube access of a viewer asks, `feed` shall not give a
> video from the channel.

Its tree (`WhileWhen (CondOne (c_subscribed_IsNot …)) (HappensI … e_ask) (… ShallNot … (Do e_give …))`) shows three
faults that a reader sees at once and the parser does not:

1. **"asks" has no object.** Asks for what, from whom? `HappensI` takes any event with no object.
2. **"give a video" has no recipient**, where r1 of the same capability says "give the caller every video" (`Do`
   against `DoTo`). Any event takes any number of objects.
3. **"a channel is not subscribed" has no subscriber.** `subscribed` is a one-place condition of channel whose gloss
   says "a channel *the viewer* subscribes to": a relation between viewer and channel, disguised as a property.

The person's position (quote-8 to quote-14):

- The glossary labels a verb as a verb. Leaving what a verb takes to a gloss "is shifting far too much responsibility
  to the glossary"; if a reader can tell the English is wrong, the parser can too.
- "Verbs require nouns, nouns define variables." A clause is a subject, a verb and the nouns the verb takes.
- The aim is a controlled natural language that yields unambiguous *and logical* statements: a line can be
  unambiguous and still give nothing to infer from.
- The base grammar starts from basic English grammar, restricted. It is a controlled grammar: what it does not allow
  is refused.
- Terms are labelled with their part of speech.
- "Reword everything, we are still in early alpha": no period where the old grammar is kept beside the new.

The person's rewrite of r2, as the target the grammar should accept:

> While a user is not subscribed to a channel, when a caller requests a video from the channel, `feed` shall not
> return the video.

## Goals

- Every term of a glossary names its part of speech, and every verb its **frame**: the kind of its subject, the kind
  of its object (or that it takes none), and the kind of its recipient where it takes one.
- The grammar builds clauses only from frames: a verb used without a noun its frame takes does not parse, and the
  refusal names the verb's term (r58, r59). A verb with no frame is refused by `model check` (r60).
- A condition (adjective) is one-place. A condition whose definition names another kind with "the" is a relation in
  disguise and is refused by `model check` (r61); it is written as a verb between the two kinds.
- `not` goes on a verb or a relation: "a user is not subscribed to a channel", "a user does not subscribe to a
  channel", "`feed` shall not return the video" all parse (r62).
- Each frame gives the facts `model logic` reasons with: subject, object and recipient are roles of one event fact,
  so a negated verb or relation is a fact the checker can contrast with the positive one.
- Every line of this repository's spec, its glossary, `grammar/corpus/` and its generated features are reworded to
  the new grammar in b82.
- Consumers get the change by `migrate upgrade` (below); they reword their own lines.

## Non-goals

- Word choice. "ask" against "request" is the glossary author's call; the grammar can require that a verb names what
  it takes, not that the verb is well chosen.
- feed's own spec: its universal requirement that every call carries a user's YouTube access, binding a caller to its
  user (a verb such as *caller acts for user*), and whether r2 is needed at all. feed rewords after it upgrades.
- "the X" with no antecedent, and nested noun phrases such as "a caller with the YouTube access of a viewer": the
  next cases to weigh against the readability bar, not settled here.
- Keeping the old grammar alongside the new.

## The how the person settled

- Part of speech on every term (quote-12).
- A verb's frame in the glossary, not in a gloss (quote-8).
- A clause is subject, verb and the nouns the verb takes; a verb alone only where the verb takes no object (quote-10,
  quote-11).
- Basic English, restricted; anything outside it refused (quote-13).
- Reword everything at once (quote-14).

## Calls made in the session (the person asleep; check these)

1. **The term entry.** The category in parentheses becomes the part of speech: `(noun)` for a kind, `(proper noun)`
   for an actor, `(adjective of <kind>)` for a condition, `(attribute of <kind>)` stays for an attribute with values,
   `(noun, exclusive)` / `(noun, counted by …)` for a resource, and `(verb)` for an event. A verb's entry carries its
   frame on a `Frame:` line in the sentence order it is read, the kinds as glossary terms:
   - `Frame: caller requests video.` (subject, object)
   - `Frame: feed returns video to caller.` (subject, object, recipient)
   - `Frame: session ends.` (no object)
   - `Frame: user subscribes to channel.` (a prepositional verb: the preposition is part of the verb)
   `Forms:` stays for irregular forms. The exact spelling is the builder's, as long as each term's part of speech and
   each verb's frame are read from the entry and nowhere else.
2. **One order for a recipient**: object, then "to" recipient ("return the video to the caller"). The double-object
   order ("give the caller a video") is refused, so a line has one way to say it.
3. **A passive with no agent is refused** where the verb's frame has a subject: "a channel is not subscribed" is the
   person's own example of the fault. The passive with its agent ("a channel that is subscribed to by a user") is not
   offered; the active clause is the one form. A verb whose frame has no object has no passive.
4. **Relation rows stay for prepositions** (`video | from | channel`): a noun-phrase modifier and an `is`-clause
   ("the video is from the channel", "… is not from …"). A relation row whose word is a verb ("has", "holds") becomes
   a verb with a frame.
5. **The generic verb funs go**: `Do`, `DoTo`, `Happens`, `HappensI`, `Undergoes` in `Req`, and `SDoes`, `SDoesNot`,
   `SDoesTo` in `Steps`, give way to typed funs generated per frame (as kinds and relation rows are typed today). The
   fixed verbs of the core (`print`, `exit successfully`, `exit with an error naming`, `change nothing`, `hold`, the
   person `runs` a command) stay as core funs, each with its own fixed frame.
6. **Release 3.0.0** with an upgrade step "verb frames" (below), since every consumer's glossary changes form.

## Behaviour (the item's lines, design-model-check)

- r58: `model parse` refuses an objectless requirement, naming the term.
- r59: `model parse` refuses a recipientless requirement, naming the term.
- r60: `model check` refuses a frameless verb term, naming the term.
- r61: `model check` refuses a relational condition, naming the term.
- r62: `model parse` parses a negating requirement.

r58 and r59 need the refusal to say why: GF alone stops at the token where a verb runs short. The builder makes the
refusal name the verb's term, for example by reading the verb's frame where the parse stopped, or by a lenient parse
whose post-parse guard names the missing role (as `spec_tree`'s guards do today).

## What changes (left to the builder, within the above)

- `spec_lexicon`: reads the part of speech and a verb's frame; v_t-codes for a frameless verb and a relational
  condition (`model check`, r60, r61).
- `spec_typed` (and its split, to stay under 300 lines): typed verb funs per frame for triggers, conditions, verb
  phrases and noun-phrase modifiers ("a video that a caller requests"), negated forms; `Lex` stops emitting an
  untyped `Event`.
- `grammar/Req.gf`, `ReqEng.gf`, `Steps.gf`, `StepsEng.gf`: the generic verb funs removed; the core verbs kept.
- `spec_facts`, `spec_logic_vocab`, `grammar/check.lp`: a verb fact with typed roles; negation of a verb or a relation.
- `spec_steps`, `features_vocab*`: steps worded from the new funs; `features generate` byte-stable over the result.
- `grammar/corpus/`: every sentence rewritten; `refused.txt` gains the three faults of feed's r2, each refused.
- **The rewording.** Every glossary entry relabelled, every capability's terms and lines reworded. A requirement is
  never edited in place (design-decision/requirements-retired-never-edited): a line whose text changes gets a new id,
  its old id goes to `retired:`, and its scenarios are regenerated. A line that parses unchanged keeps its id. The
  item's own lines r58-r62 are reworded the same way if the new grammar changes them.
- **The upgrade step "verb frames"** (`migrate_upgrade_*`, migration-tools): relabels each glossary entry's category
  to its part of speech where that is mechanical (kind, actor, condition, attribute, resource), and reports each verb
  that needs a frame, each relational condition, and each requirement that no longer parses, by file and id. It does
  not reword a line.
- README's 3.0.0 section, `.claude-plugin/plugin.json` 3.0.0, `migration-tools`' version given blocks, and this
  repository's `.shop/plugin-version`.
