---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-15-collections-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-15
---

# Collections and comparisons in grammar 4 today: an adversarial review

An adversarial review, by a fresh agent, of a session's summary of what grammar 4 (plugin 0.34.1) can say about collections and comparisons. It was written before b267 and its neighbours were shaped. The person had already found one claim wrong: that "While a batch holds no item" says the batch is empty. Each claim was checked in `model parse --form`, and through `features generate --root` and `model logic --root`, on a throwaway copy of `spec/`. That copy had one capability per line, `cN` for claim N, with c13-c22 holding extra lines. The lines and the tools' outputs are in this record's folder.

## Finding beside the table: `model logic` is silent on a line it cannot translate

`model logic` printed `no findings` for c4 and c5. With `--json` it printed `{"findings": [], "exit": 0}`. A line that spec_lf_facts refuses goes into `ctx.refused` (`scripts/spec_context.py:100`), and only `features_generate.py:32` reads that list. So "no findings" can mean "not checked".

## The claims

| # | Claim | Verdict | Evidence | What is true |
|---|---|---|---|---|
| 1 | every in a response: "print a batch that holds every item whose status is `ready`" | misleading | `every [x5: item] status(x5) = \`ready\` scope in(x5, x4)`. Scenario c1: two ready items, no other item, Thens that the batch holds i1 and i2 | Every ready item in the world is in the printed batch, with no bound (it clashes with `batch_size`). The scenario cannot fail for a batch that holds every item, ready or not |
| 2 | membership in a condition: "While a batch holds an item" | correct, misleading | `while [x1: batch, x2: item] in(x2, x1)`, and the trigger has no `on:` | Some batch holds some item, not tied to the command. "on the batch" ties it |
| 3 | empty: "While a batch holds no item" | misleading | `not [x2: item] in(x2, x1)` is a "there is none" (¬∃). The form, check.lp (`rnone`, check.lp:203) and the Given "the batch b1 holds no item" agree | It means "holds no item", which is not "holds nothing": other kinds may be held, and "holds no thing" does not parse. "a batch" in a While is any batch, not the one the command runs on. "the number of items in the batch is `0`" (`count exactly 0`) also says it, once the batch is brought in first (c18) |
| 4 | only: "a batch that holds only items whose status is `ready`" | wrong | Parses. `features generate`: `refused: no translation of only over that` (spec_lf_facts' `only` takes an event scope). `model logic` skips it silently | Not usable. "print only items in the batch" generates, but its scenario (c15) has no non-member and asserts a print that "only" does not oblige |
| 5 | size bounded: "a batch that holds at most three items", "While a batch holds at least two items" | half wrong | Response: `refused: no translation of a count over that`, and logic skips it (also c14 "holds exactly three"). While: `count at least 2 ... scope in(x2, x1)` works (c6), but its scenario gives exactly two items and never one | A count in a condition bounds a collection. A count in a response over a relation is unusable. A count in a response over an act bounds only the number of things acted on |
| 6 | exact output: "print exactly three items" | misleading | `count exactly 3 [x5: item] scope print(...)`, with no tie to the batch. Scenario c7: three free items, no fourth | It says three items are printed, any items, nothing about the batch. The scenario cannot catch a fourth item printed |
| 7 | number as a value: "print the number of items in the batch" | correct | `number x5 of [x6: item] in(x6, x3)`. Scenario: two members, a Then of the number | As claimed. The Then is as strong as its handler |
| 8 | number compared: "the number of items in the batch is more than three" | correct | `count more than 3 [x3: item] in(x3, x1)`. Scenario: five items | As claimed. The boundary of three is never tested |
| 9 | every member meets: "... and every item in the batch is `ready`" | wrong in its scenario | The form is right. Scenario c10: i1 is in b1 with no status, and only i2 is `ready`, so its Givens break the While | The scenario is defective: spec_steps4_boxes gives the every box a fresh K and gives the "holds an item" K no status. Without the "holds an item" conjunct the line is refused (R2), and the empty batch is never tested |
| 10 | every member printed: "print every item in the batch" | correct, weak test | `every [x5: item] in(x5, x3) scope print`. Scenario c11: two members, no non-member | The scenario cannot fail for printing every item there is. "... and not print an item that the batch does not hold" (c16) brings in i3 and tests that it is not printed |
| 11 | two distinct: "print two items" | misleading | `distinct(x5, x4)` and no count box. Scenario c12: no Givens, Thens on i1 and i2, which no Given brings in | "two Ks" means at least two different things, while "one item" is `count exactly 1`. The scenario names undeclared instances (also c19) |
| 12 | a member against a fixed value: "the release of x is after `0.34.1`" | correct | `cmp(release(x1)) after \`0.34.1\`` | Only for a code listed in the entry's `Values:` |
| g | `features generate` correct for every, only and count | wrong | See 4, 5, 9 and 10, and c20 ("print one item": one item and no second). c17 ("a batch that holds no item whose status is not `ready`"): `refused: no translation of a negated restriction (not) on an object` | Only, and counts in a response over a relation, are refused. The every, only and exactly scenarios have no counter-example, and the scenario of every in a condition is wrong |

## The claimed failures

| Claim | Verdict | What is true |
|---|---|---|
| ordering ("print every item, ordered by score, in descending order") | correct | does not parse (known limit #14) |
| two values compared ("the release of a repository is after the release of the plugin") | correct | does not parse (limit #6) |
| "holds exactly the items whose status is `ready`" | correct, misleading | The same meaning is "holds every item whose status is `ready`" with "holds no item whose status is not `ready`". The second parses, but generate refuses it (c17) |
| "... and print no other item" | misleading | "... and not print an item that the batch does not hold" parses and generates a scenario that can fail (c16) |
| "While an item is in a batch" | misleading | "While an item in a batch is `ready`" (`in(x1, x2)`) or "While a batch holds an item" |
| "the first item", "the highest score" | correct | do not parse (limits #14, #3) |
| uniqueness ("an item twice") | unverified | `in` is a plain relation, and nothing counts multiplicity |
| "every item with its title" | correct | does not parse (limit #10) |
| b268 | unverified | It did not show up in these lines' scenarios |
| "a batch" made inside an every or count box cannot be "the batch" later | correct | Refused (R2). Bring the batch in before the box |
| "the number of items of a batch" | unverified | The parse did not return (stopped after about 3.5 min, likely in the hint search) |
| added: "zero" | | does not parse. Only the code `0` is read, and number words start at one |

## Use cases the summary missed

- Emptiness said with a count, "the number of items in the batch is `0`". It needs the batch brought in first, and its scenario only relies on the world being empty.
- Non-emptiness and exact size in a condition ("holds exactly one item"; "at most one" gives a scenario with no item).
- A While collection tied to the thing the command runs on ("on the batch"), without which a condition is about some collection anywhere.
- Exclusivity said as a negated act, the only form whose scenario brings in a non-member.
- `model logic`'s "no findings" on a line it never translated.
- A count compared with a parameter (`more than \`batch_size\``), which works.
- Membership at any depth (no closure), each X with its Y (#10), and aggregates (#3), all unsayable and in `grammar/language.md`'s known limits.
