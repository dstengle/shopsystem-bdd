# Audit: grammar 4 over backlog and batches (b158)

Sources: b158's `## Requirements` (backlog r22-r39 and batches r20-r33 reworded, with the lines it keeps: backlog r5, r6
and r15; batches r4, r9, r11, r14 and r15), laid with `backlog_lines.lay` over a scratch copy of `spec/`. I also used
phase 3's d.tsv candidates and d.md's hard lines. All 40 lines parse with `model parse --capability <cap> --form`
(forms in `forms/`). So none of the verdicts below rests on a parse failure. Each comes from reading the logical form
against what the original line meant.

## Counts

| verdict | backlog (21) | batches (19) | total |
|---|---|---|---|
| fine | 14 | 13 | 27 |
| distortion | 4 | 5 | 9 |
| unsayable | 3 | 1 | 4 |
| coined | 0 | 0 | 0 |

No coined adjective is left. tasked, tracking, unpushable, silent, blocked, passing and uncited have all become
structure. The meaning that is still hidden now sits in verb glosses (pick, propose) and in what the new structure
leaves out, not in adjectives.

## Missing constructs (lines each)

| construct | lines | where |
|---|---|---|
| identity or distinctness of two referents ("another item", "not in the same batch") | 4 | backlog r26; batches r20, r22, r32 |
| "the K" naming the earlier of two Ks of one kind (R2 always binds the latest) | 2 | backlog r26; batches r22 |
| "for each X, its Y" (distributive anaphora) | 2 | backlog r6; batches r4 |
| argument binding ("set the value to the one given") | 1 | backlog r25 |
| bounded time ("no answer within the push timeout") | 1 | backlog r37 (operational timing is deferred to b127) |
| the command's own later event in a condition (the push `work idea` makes) | 1 | backlog r36 |
| "no K" restricting an object ("a pull request with no commit of the item") | 1 | batches r25 (b237) |
| an adjunct in a frame ("remove X from Y") | 1 | batches r30 |
| two referents' attributes compared (an upstream branch "of another name") | 1 | backlog r39 |
| ordered choice ("up to batch_size, in rank order") | 1 | batches r20 |
| "one K" used where it is meant | 1 | backlog r27 |
| a set of values ("an item that is `idea`, `shaped`, `ready` or `needs-input`") | 6 fine lines | backlog r28-r33: one rule each over four values and over two |

## Worst examples

1. **backlog r6 and batches r4 parse to ill-formed forms.** In "print every item, the title of the item, ..." the
   `every` box scopes only `print(x4)`. The `of(x5, x4)`, `status(x4) = ...` and the other prints sit outside the box,
   where x4 is unbound. batches r4 does the same with `status(x6)` after "every task of the batch". language.md's R2
   says a referent made inside an `every` box gives nothing to a later "the K", so both lines should be refused. This is
   a parser fault as well as a gap in the language: they are "kept, parsing unchanged", and they carry a meaning the
   form does not have.
2. **batches r20.** "pick the item" takes the place of r1's "set the status of the item to `in-batch`", and only
   pick's gloss now says that. The meaning moved into the glossary, which is the anti-goal. blocked's "not in the same
   batch" and the pick's exception ("unless what blocks it is picked first") are gone, and so is batch_size. On top of
   that, "has no dependency on an item whose status is not `delivered`" stops `model logic` (b238).
3. **batches r22 and backlog r26.** "the item" cannot name the first of the two items, because R2 binds it to the
   undelivered one. The lines go around this: "shall not pick an item that has the dependency" and "print the
   dependency and every item that has the dependency". b158's notes already say that no definite rewording holds.
4. **batches r32.** The group's point is *another* item's passing scenario, but the form allows the task's own item.
   The b118 fault that r31 (the old r18) fixed is still present in its sibling.
5. **backlog r37.** silent hid the push timeout, and the reword drops it. "A remote answers no push" reads "never
   answers any push", which is a different state from "no answer within 60 s".
6. **backlog r36.** "While a remote rejects a push" means any remote and any push. The meaning is the push this
   command makes to its branch's remote.

## Fixable by rewording alone (with a glossary edit at most)

- **backlog r27:** "print one JSON object", with the option written as "with the `--json` option" (call 4, and
  design 4.3).
- **batches r20:** add the response "set the status of the item to `in-batch`" and trim pick's gloss. This fixes the
  hidden state change. The exceptions and batch_size still need constructs.
- **batches r30:** give remove a second frame (`agent removes text from git branch`) and say "remove the requirement
  from the git branch". "propose" could become "a requirement of the item" through an `of` row, so a common verb no
  longer carries a relation.
- **backlog r36:** in part. The remote can be bound with a row or the indexical ("the remote of this repository").
  The push being the command's own needs a construct.
- **batches r9:** fine as a line, but merge's gloss contradicts its frame. That needs a glossary fix.

These need a construct, not a rewording:

- distinctness and identity (4 lines);
- naming an earlier referent of the same kind (2);
- "for each X, its Y" (2), together with the parser's R2 fault;
- argument binding (1);
- bounded time (1);
- "no K" on an object (1);
- comparing attributes (1);
- ordered choice (1).

## Fine, with notes

- **backlog r28-r33:** six lines for two rules. A set of values would merge them without bending anything.
- **batches r21:** "passes the readiness bar" names the bar as an artifact (`This:`) and reads as conformance, which
  design 6.2 allows. It is borderline, since the bar's checks are listed only in its gloss.
- **backlog r38:** "git branch" exists only to avoid a kind named branch (v_t12). It is a workaround, not a fault.
- **batches r31:** correct, but only because R2 binds "the item" to the latest one (the `needs-input` item). It is
  fragile if the conditions are put in another order.
