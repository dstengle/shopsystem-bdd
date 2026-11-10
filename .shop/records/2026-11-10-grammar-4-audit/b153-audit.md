# Audit: can grammar 4 say requests' lines? (b153)

Scope: the 44 grammar-4 lines on b153 (r59-r102). Between them they replace the 44 retired lines of requests. r8 was
retired with no successor, and r7 was split into r61 and r102. No other item has added grammar-4 lines to requests,
and spec/ on main still holds the codified-1 lines. I laid b153 over a copy of spec/ (`backlog_lines.lay_onto`) and
put all 44 lines through `model parse --form --capability requests`. All 44 parse. I also parsed 23 alternative
wordings to see which faults a rewording alone would fix. The evidence column of `audit.tsv` says which ones I
checked.

## Counts

| verdict | lines |
|---|---|
| fine | 18 (r64-r68, r70, r71, r73-r75, r78, r85, r91-r94, r97, r98) |
| distortion | 16 (r59, r61-r63, r69, r79, r81, r82, r87-r90, r96, r99, r101, r102) |
| coined | 10 (r60, r72, r76, r77, r80, r83, r84, r86, r95, r100) |
| unsayable | 0 as written. The meaning of r80 and r83 ("every line settled") has no form, and it is hidden behind the coined verb *block* |

The fine lines are mostly simple ones: a status moved into While, "set the status of the request to `v`", "close the
issue of the request", and the short refusal. The coined adjectives received and sent are gone. In their place are
two plain relation verbs and the indexical: "addresses / originates from this bounded context". This is the
structure the person asked for, and it fixes b118's r16 and r18/r49 faults.

## Missing constructs (lines)

| construct | lines |
|---|---|
| Conformance (CONFORMS): the comment form, the upstream's requirement grammar, an ask's body | 8: r76, r77, r86, r95, r100 (*field block*), r82 (*has no logical form*), r87, r101 (ask dropped) |
| An option with its argument, or several options, in the trigger | 5: r59, r61, r62, r82, r102. Flags glued into the code also appear in r97-r101 |
| A defined adjective (settled, closed; call 13 unbuilt) or a value list ("is `accepted`, `refused` or `withdrawn`") | 4: r79, r84, r96, r99 |
| A universal over a disjunction ("every line proposed in the request is settled") | 2: r80, r83 |
| A negated response over an attribute ("not change the side"); *keep* stands in | 2: r80, r96 |
| A universal in a condition's object ("rejects every commit"), git as the agent | 3: r88-r90 |
| The image of a relation under "not" in a response: the parse accepts it, but features generate has no Then for it | 2: r89, r90 |
| A chain of "of" and "no" over the upstream entry's `github:` (hidden in *host*) | 3: r72, r87, r101 |
| An issue's open state | 2: r87, r101 |
| A negated restriction on an object ("an observation that no request and no initiative cites") | 1: r69 |
| *every* with existential import | 1: r81 |
| Setting an attribute to the value the command was given | 1: r63 |
| A negated option list ("with none of `--source`, `--thread`, `--raised-for`") | 1: r60 |
| An entry of the other side's part (*foreign entry*) | 1: r95 |

## Worst examples

- **r80 / r83, *block*.** "no request line blocks the request" stands for "every request line proposed in the
  request is accepted, refused or withdrawn". The gloss holds the whole condition: proposed in, no outcome, or an
  outcome other than three values. *block* is a state verb, so model logic cannot see inside it (b153's notes say
  so). This is the anti-goal in its plainest form, and it comes back three months after *settled*. No grammar-4 form
  says "every line settled". I checked "every ... is `accepted` or the request line is ..." (refused: no antecedent
  outside the every box), "no request line that is not `accepted`" and a value list. None parses.
- **The *field block* family (r76, r77, r86, r95, r100).** "a comment ... has a field block" reads like structure.
  But the gloss of *field block* puts the meaning in the glossary: "whose fields parse as the comment form, which a
  comment ... with a block that does not parse lacks". The person's own rewrite of r33 was "does not conform to the
  comment schema" (design 4.1), and "conform" does not parse.
- **r63, *assign*.** "assign the line outcome of a request line proposed in the request". By R1 the request line is
  a new referent of the response: the form says `work outcome` creates a request line. The coined verb also hides
  that the value is the command's argument.
- **r81.** The conjunct "a request line ... is `refused`" was dropped. No reading rule gives *every* existential
  import, so the line now refuses an open request that has no lines.
- **r96 and r99.** These list the status values in place of *closed*, and use *keep* (role-boundaries' "a session
  leaves a thing as it was", an opaque event, not `nochange`) in place of "not change". r99 still states less than
  the behaviour, as phase 3 noted.
- **r87 / r101.** "an issue that no request has" drops "open" and "whose body is an ask", so any issue of the host
  wakes the watch.
- **r88-r90.** "this repository rejects a commit" is existential, where the meaning is "every commit". *reject*
  stands in for git as the agent.

## Fixable by rewording alone (checked with `model parse`)

- **r61 + r102**: "runs `work request` with `--source` and `--thread`" parses, with both options as option
  referents. No split and no glued code are needed. r7's "or `--raised-for`" still needs two lines, or an "or"
  between the options.
- **r76**: "the request does not hold the comment" parses, as r86 already says it. *lack* (second sense) can go.
- **r81**: putting back "a request line proposed in the request is `refused` and" parses.
- **r84**: r79's form ("is not `accepted` and ... not `refused` and ... not `withdrawn`") parses as a refusal
  condition, which removes *block* from r84. It is still a value-list distortion.
- **r99**: the real condition parses: "no request that originates from this bounded context is `awaiting-upstream`
  and no request that addresses this bounded context is `awaiting-asker`". (A fuller form would add the "does not
  address / originate" negations.)
- **r97-r101**: "runs `work watch` with `--forward`" parses. The glued flags can become option referents.
- **r89 / r90**: "not close the issue of the request" parses, but features generate has no Then for it. The fix
  is in the generator, not the wording.

The other faults need grammar or vocabulary:

- CONFORMS.
- The defined adjectives of call 13, or value lists.
- A universal over a disjunction.
- A negated response on an attribute (the glossary's *change* takes only a file).
- An option together with its argument and an "on" object (refused when written together).
- A *cites* sense with a request as subject (r69).
- An argument-valued set (r63).
- *every* in a condition's object.
