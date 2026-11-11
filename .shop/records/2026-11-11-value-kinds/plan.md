# Value kinds (b257) Plan

**Goal:** an attribute says whether its values are adjectives or nouns, and the short form "X is `v`" reads only
where it is good English: an adjective value (`shaped`, `ready`, `in-batch`). A noun value (`idea`, a tier, a
release) or a verb-phrase one (`needs-input`, `fix now`) is said in the full form, "the status of the item is
`idea`" or "an item whose status is `idea`". Generated Gherkin is always the full form, for every value: "Given the
status of the item i1 is `idea`", so whoever binds a step reads the attribute in the step and never looks it up
(the person, quote-24 and quote-25; `.shop/backlog/b257.md`).

**Branch:** `plan-value-kinds` from `origin/main`, worktree `.shop/worktrees/plan-value-kinds`; one implementer,
test first, then one reviewer of the branch. The item's status is closed by the main session after the merge.

## 1. The declaration

An attribute entry gives its values in one or both of two fields:

```
- **status** (attribute of item): Values (adjective): `shaped`, `ready`, `in-batch`, `delivered`, `refused`, `withdrawn`. Values (noun): `idea`, `needs-input`.
- **tier** (attribute of design-decision): Values (noun): `check`, `requirement`, `judgement`.
```

- `Values (adjective):` lists the values that read after "is" as an adjective or a participle.
- `Values (noun):` lists every other value: a noun, a verb phrase, a code (a release's `1.0.0`). A value that does
  not read as an adjective after "is" is declared a noun.
- One attribute may give both; the values are the two lists in order (an `Order: as listed.` reads the adjectives
  first, then the nouns). An ordered-by-number attribute's codes no entry lists are of its noun list's kind when it
  gives one.
- A plain `Values:` is a value list of no declared kind (below). An entry gives either `Values:` or the declared
  fields, not both (v_t4 names it).

The reader is spec_lexicon (each `Term` gains the kind of each value); `model lexicon` prints each value with its
kind.

## 2. An undeclared value kind: today's behaviour, with a warning

A value of a plain `Values:` reads as it did in 4.0: the short form is accepted. `model check` warns
`w_value_kind` ("an attribute does not say whether its values are adjectives or nouns") for each such attribute.
So every line that parses under 4.0 parses under 4.1 until its context declares a value a noun; nothing a consumer
has is refused by the upgrade alone. That is why the release is a minor one (section 7).

## 3. The refusal and its hint

The short form of a noun value is refused after the parse (the line has its one tree; the guard reads it), in the
one place a line is read (spec_language's `parse`, which `model parse`, `model check`, `model logic`, the readiness
bar and `work outcome` share). The short form is any of the grammar's `<t>_<K>_Is` ("an item is `idea`", "is not"),
`<t>_<K>_IsOneOf` and `<t>_<K>_IsNoneOf` ("an item is one of `idea` or `shaped`": refused when any value it names
is a noun) and `<t>_<K>_IsCode` (a code of an attribute whose values are nouns). The refusal names the value, the
attribute and the full form:

```
refused: `idea` is a noun, a value of the status of an item: "an item is `idea`" does not read; write "the status of the item is `idea`" or "an item whose status is `idea`"
```

`model parse` prints it as it prints any refusal; the hint (prefix, near words) is not given, since the line parses.

## 4. The construct catalogue

`attribute-is` keeps the full form only, "the <attribute> of <np> is <value>" (`<t>_IsOf`); a new entry
`adjective-value`, "<np> is <value>, of a value declared an adjective" (`<t>_<K>_Is`), with the refusal in its
label. `attribute-code` and `value-set` say their short form takes an adjective value. The catalogue's context
(`grammar/corpus/constructs/`) declares its attributes; the core-4 corpus (`grammar/corpus/core-4.txt`, its
fixture context) gains a noun-valued attribute and the refused short forms with their reasons.
`grammar/language.md` gains a section on values: adjective and noun, the two forms and the refusal.

## 5. The lines of this repository

Every attribute of the glossary and the capabilities is declared (the nouns: the item's `idea` and `needs-input`, a
request line's `question`, sides, stage kinds, groups, languages, results' outcomes, provenance, tiers, triage,
releases, environments, routes' kinds, parts of speech, headings, aspects; the rest adjectives). A scan of every live
line's tree finds 78 lines with a short form, 17 of them with a noun or verb-phrase value, each reworded to the full
form with "the status of an item is `idea`" in place of "an item is `idea`" (its logical form unchanged), a new id
each, the old one retired, its corpus block first:

- backlog r23, r24, r28, r29, r30, r31 (`idea`, `needs-input`)
- batches r27, r33 (`needs-input`)
- decision-tiers r14, r15, r16, r17 (the tiers), r23 (a route's kind)
- pr-review r4 (`judgement`), r13, r14, r15 (`fix now`)

The other 61 use adjective values and stay as they are. Generated Gherkin changes for every value step (the full
form), so every feature is regenerated and every handler that reads a value step's text is moved onto the step's
subject (the `Call` of a value step gains the owner's words as its `subject`).

## 6. Docs and skills

The README's example line becomes "While the status of an item is `idea`, when ...", with a sentence that each
attribute's values are declared adjectives or nouns in the glossary; `docs/writing-requirements.md` (the entry table,
`Values:`, the two forms), `docs/reference/capability-file.md` (the entry fields and the example), the docs whose
Gherkin examples show "the item i1 is `idea`" (README, docs/index.md, docs/concepts.md, docs/how-it-works.md,
capability-file.md), and the skills that teach values (shaping-items, raising-a-request, taking-in-a-request: the
two forms and the refusal's fix).

## 7. The release: 4.1.0

Nothing that parses under 4.0.0 is refused under 4.1.0 unless its attribute declares the value a noun, which no
consumer's spec does before it is changed; an undeclared attribute only warns. The generated Gherkin's wording of a
value step changes (a `features generate --check` fails until the feature is regenerated, as after any change of the
generator), and the plugin's handlers bind by the step's template, kind and attribute, which do not change. So the
release is 4.1.0: README and CHANGELOG, `.claude-plugin/plugin.json`, `.shop/plugin-version`, migration-tools' lines on
the plugin's release (r62, r63, r64 reworded to `4.1.0`, new ids, `4.1.0` a value of the releases) and a 4.1.0
upgrade step "value kinds", which reports only, as 4.0.0's did: each attribute with an undeclared value kind and each
line that uses its short form, by file and id, for a session to declare and to reword the noun ones; a new line of
migration-tools says it.

## 8. The gate

The suite (`timeout 1500 python3 -m pytest -q -n 8`), `model check`, `model logic`, `features generate --check`,
`features vocab --check`, the corpus and docs tests, `model constructs --check`, `tools size --limit 300` and
`tools check`; pushed.
