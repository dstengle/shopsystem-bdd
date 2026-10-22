---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-17-ids-integrate-gate-texts
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
date: 2026-10-17
---

# Integrate fixture runs: the gate texts (B and T)

Gate texts exported from integrate fixture runs, kept by the controller to check the harness's gate scorer: `b-integrate-1.md` and `b-integrate-3.md` from the 0.19.0 B runs (2026-10-16), `t-integrate-1.md`, `t-integrate-2.md` and `t-integrate-2-late.md` from the type-first reruns (2026-10-17). In T-integrate-2 the last message answered a late background notification (`t-integrate-2-late.md`), so the gate is the message before it; that and the differing gate layouts led to the scorer fixes reported in `2026-10-16-requirement-ids-test-log.md`.

Archived from git-ignored scratch; each file's text as it was.

## `/home/vscode/scratch/shopsystem-bdd/ids/gates/b-integrate-1.md`

~~~~~~
# Gate: lending design, round 1

I've written nothing to `spec/`. The drafts are under `.superpowers/spec-drafts/2026-10-16-lending-design/round-1/`.

## Added: `lend-books` (new capability)
- **[r1]** When the reader lends a book the shelf holds to a named friend, the shelf records that friend as having the book.
- **[r2]** If the reader lends a book that is already lent, the shelf refuses the lend because the book is out.
- **[r3]** If the reader lends a book the shelf does not hold, the shelf refuses the lend because the book is not held.
- **[r4]** When the reader takes a lent book back, the shelf records the book as on the shelf again.
- **[r5]** If the reader takes back a book that is not lent, the shelf refuses because the book is not out.
- **[r6]** When the reader asks who has a book that is lent, the shelf answers with the friend's name.
- **[r7]** While a book is lent, the shelf still holds it.

## Added: `keep-items`
- **[r6]** If the reader adds a book whose title is empty, the shelf refuses the add because the title is empty.
- **[r7]** When the reader removes a book the shelf holds, the shelf no longer holds it.

## Changed: `keep-items`
- **[r3]**
  - Was: When the reader asks how many books there are, the shelf answers with the number of books it holds.
  - Now: When the reader asks how many books there are, the shelf answers with the number of books it holds that are not lent.

## Removed: `keep-items`
- **[r4]** When the reader asks for the title of a book by its id, the shelf answers with the title.
  - r4 is retired.
  - Its scenario in `features/keep-items.feature` loses its line, so formulation removes or holds it.

## Not lines (for information)
- **Implementation (`lend-books`):** the friend's name is kept beside the book in the same file, and names are compared without regard to case.
- **Not yet:**
  - `lend-books` "Due dates".
  - `keep-items` "Removing a lent book". It replaces "Removing a book", which r7 covers.
  - Neither has a trigger in the note.
- **Ledger:** `decision/lending-not-a-library` (no due dates, no fines).
- **Cut sentences:** 3.

## Questions
1. **Friend limit.** The note says "A friend should not hold too many books at once" but gives no bound and no reason.
   - If there is a bound N: `[r8]` If the reader lends a book to a friend who already has N books, the shelf refuses the lend because the friend has too many books.
   - If it is only a hope: a Not yet entry "A limit on books per friend", with a trigger.
   - What is N, what reason does the refusal name, and is it a rule or a hope?
2. **Asking who has a book that is not lent.**
   - If refused: `[r8]` If the reader asks who has a book that is not lent, the shelf refuses because the book is not out.
   - If answered: `[r8]` When the reader asks who has a book that is not lent, the shelf answers that no friend has it.
   - Or no line.
3. **Case of names.**
   - (a) A storage detail only, as drafted.
   - (b) `[r8]` Where two friends' names differ only in case, the shelf treats them as the same friend.
   - Should r6 also read "...answers with the friend's name as given when the book was lent"?
4. **Removing a lent book.** What trigger promotes the Not yet entry? Until then, is it refused? If so: `[r8]` If the reader removes a book that is lent, the shelf refuses the removal because the book is out.
5. **Due dates.** What trigger promotes the Not yet entry? Or does it come out, leaving the ledger entry as the only record?
6. **Removing a book the shelf does not hold.** The note is silent. If refused: `[r8]` If the reader removes a book the shelf does not hold, the shelf refuses the removal because the book is not held.
7. **Empty title.** Is a whitespace-only title empty? If yes, `keep-items` `[r6]` becomes: If the reader adds a book whose title is empty or only whitespace, the shelf refuses the add because the title is empty.
8. **Where the count change lives.**
   - Keep it in `keep-items` r3 as drafted. `keep-items` then mentions lending.
   - Or leave `keep-items` r3 as it was and add to `lend-books` `[r8]` When the reader asks how many books there are, the shelf does not count a book that is lent.
   - "Holds" is used in two senses: r7 in `lend-books` ("the shelf still holds it") and `keep-items` r3 ("holds that are not lent"). The answer here can settle the wording.

I need an explicit yes or no on the lines above, and an answer to each question.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/gates/b-integrate-3.md`

~~~~~~
The integration round is done and nothing is written to `spec/`. Drafts are in `.superpowers/spec-drafts/2026-10-02-lending-design/round-1/`.

## Gate: lending-design, round 1

### lending (new capability, rests on keep-items)
Added:
- **[r1]** When the reader lends a book the shelf holds to a named friend, the shelf records that friend as having the book.
- **[r2]** If the reader lends a book that is already lent, the shelf refuses the lending because the book is out.
- **[r3]** If the reader lends a book the shelf does not hold, the shelf refuses the lending because the book is not held.
- **[r4]** When the reader takes a lent book back, the shelf records the book as on the shelf again.
- **[r5]** If the reader takes back a book that is not lent, the shelf refuses the taking back because the book is not out.
- **[r6]** When the reader asks who has a book that is lent, the shelf answers with the friend's name.
- **[r7]** While a book is lent, the shelf still holds it.

### keep-items
Changed:
- **[r3]** now: When the reader asks how many books there are, the shelf answers with the number of books on the shelf right now, not counting a book that is lent.
  was: When the reader asks how many books there are, the shelf answers with the number of books it holds.

Added:
- **[r6]** If the reader adds a book whose title is empty, the shelf refuses the add because the title is empty.
- **[r7]** When the reader removes a book the shelf holds, the shelf no longer holds it.

Removed (this deletes contract, and the id is retired):
- **[r4]** When the reader asks for the title of a book by its id, the shelf answers with the title.

Also drafted, with no Behaviour lines:
- A ledger entry, `decision/title-by-id-withdrawn`.
- The index composition.
- Lending's Implementation and Not yet sections.
- Removing "Removing a book" from keep-items' Not yet.

### Questions
1. **Friend limit.** The note says "A friend should not hold too many books at once" but gives no bound or reason.
   - If there is a bound N: lending [r8] "If the reader lends a book to a friend who already has N books, the shelf refuses the lending because the friend holds too many books." Also an index constraint "A friend holds at most N books at once."
   - If it is only an aspiration: cut it, or add Not yet "A limit on books per friend" with a trigger you name.
2. **Case in names.** Is "Names are compared without regard to case" (under How) implementation or a rule?
   - Implementation: it stays as it is.
   - Rule: lending [r8] "The shelf treats two friends' names that differ only in case as the same friend."
3. **Asking who has a book that is not lent.** The note doesn't say what happens.
   - Refusal: lending [r8] "If the reader asks who has a book that is not lent, the shelf refuses the question because the book is not out."
   - Answer: "When the reader asks who has a book that is not lent, the shelf answers that no one has it."
4. **Not yet triggers.** What signal should "Due dates" and "removing a lent book" each wait for? Until you give one, both read "Trigger: not stated".
5. **keep-items [r7] and lent books.** Should removal be limited to books that are not lent?
   - Yes: "When the reader removes a book the shelf holds that is not lent, the shelf no longer holds it."
   - No: [r7] stays as drafted.
6. **The changed count.** Should it stay as keep-items [r3] (as drafted)? Or move to lending as new [r8] "When the reader asks how many books there are, the shelf does not count a book that is lent." with keep-items r3 unchanged? Moving it would contradict r3, because a lent book is still held (lending r7).
7. **Empty title.** The note says it is refused "as a duplicate is". Should it be refused the same way but with its own reason (as drafted in [r6])? Or does an empty title count as a duplicate, which would change [r2] instead?
8. **Taking back.** Should taking back name a friend?
   - Yes: lending [r9] "If the reader takes back a lent book naming a friend who does not have it, the shelf refuses the taking back because that friend does not have the book."
   - No: nothing is written.

Two sentences from the note were cut and are not drafted as lines. The full gate text is in `round-1/gate.md`.

I need an explicit yes on the lines and an answer to each question before I do anything. Your answers go back to the writer as round 2, and I'll show you the result before anything is applied.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/gates/t-integrate-1.md`

~~~~~~
## Gate: lending design, round 1

Nothing has been written to `spec/`.

### lending (new capability)

**Added**
- **[r1]** When the reader lends a book the shelf holds to a named friend, the shelf records that friend as having the book.
  - Note: "The reader lends a book the shelf holds to a named friend, and the shelf records that friend as having the book."
- **[r2]** If the reader lends a book that is already lent, the shelf refuses the lend because the book is out.
  - Note: "Lending a book that is already lent is refused, because the book is out."
- **[r3]** If the reader lends a book the shelf does not hold, the shelf refuses the lend because it is not held.
  - Note: "Lending a book the shelf does not hold is refused, because it is not held."
- **[r4]** When the reader takes a lent book back, the shelf records it as on the shelf again.
  - Note: "The reader takes a lent book back, and the shelf records it as on the shelf again; ..."
- **[r5]** If the reader takes back a book that is not lent, the shelf refuses the return because it is not out.
  - Note: "...taking back a book that is not lent is refused, because it is not out."
- **[r6]** When the reader asks who has a lent book, the shelf answers with the friend's name.
  - Note: "The reader can ask who has a book that is lent, and is told the friend's name."
- **[r7]** While a book is lent, the shelf still holds it.
  - Note: "A lent book stays on the shelf's list: lending does not remove it."

### keep-items

**Changed**
- **[r3]** When the reader asks how many books there are, the shelf answers with the number of books it holds that are not lent.
  - It was "...the number of books it holds."
  - Note: "But the count the reader asks for should be of the books on the shelf right now, so a lent book is not counted."

**Added**
- **[r6]** If the reader adds a book whose title is empty, the shelf refuses the add because the title is empty.
  - Note: "Adding a book whose title is empty is refused, as a duplicate is, because the title is empty."
- **[r7]** When the reader removes a book the shelf holds, the shelf no longer holds it.
  - Note: "the reader can remove a book the shelf holds, after which the shelf no longer holds it"

**Removed** (its id is retired)
- **[r4]** When the reader asks for the title of a book by its id, the shelf answers with the title.
  - Note: "The reader no longer asks for a book's title by its id: that question goes."

### Other changes
- keep-items "Not yet": "Removing a book." is replaced by "Removing a lent book."
- lending "Not yet": "Due dates." is added.
- lending Implementation: the friend's name is kept beside the book, and names are compared case-insensitively.
- There are no ledger entries.
- One sentence was cut as framing: "Two things change about keeping books."

### Questions
Each question shows the line its answer would add.

1. **Friend limit.** The note says "A friend should not hold too many books at once" but gives no bound. With a bound N, the line would be:
   - **[lending r8]** If the reader lends a book to a friend who already has N books, the shelf refuses the lend because the friend has too many books.
   - Otherwise it is cut, or it becomes a "Not yet" entry with a trigger.
2. **Case in names.** The note says "Names are compared without regard to case."
   - (a) Implementation only, as drafted.
   - (b) A rule: **[lending r8]** The shelf treats friends' names that differ only in case as the same friend.
   - Do titles also compare without regard to case? If so: **[keep-items r8]** If the reader adds a book whose title differs only in case from one the shelf holds, the shelf refuses the add because it is a duplicate.
3. **Due dates.** The Purpose says "no due dates", but "Not yet" lists "Due dates." Are they ruled out, so the "Not yet" entry is dropped? Or deferred, so the Purpose is softened and the entry gets a trigger?
4. **Removing a lent book.** What is the trigger for "Removing a lent book"? Or decide it now as a refusal: **[keep-items r8]** If the reader removes a book that is lent, the shelf refuses the removal because the book is out.
5. **Removing an unheld book.** The note doesn't say what happens. If refused: **[keep-items, next free id]** If the reader removes a book the shelf does not hold, the shelf refuses the removal because it is not held.
6. **Asking who has an unlent book.** The note doesn't say. If refused: **[lending, next free id]** If the reader asks who has a book that is not lent, the shelf refuses because it is not out.
7. **Empty friend name.** The note doesn't say. If refused: **[lending, next free id]** If the reader lends a book to a friend whose name is empty, the shelf refuses the lend because the name is empty.
8. **Whitespace-only titles.** Do they count as empty? If so, keep-items r6 would read "...whose title is empty or only whitespace, ... because the title is empty."
9. **Lent books and holding.** Please confirm the keep-items r3 count is books held minus lent ones, as drafted. A lent book is still held (lending r7), so adding its title again is still a duplicate. Or say if a lent book should stop counting as held everywhere.

Please answer the questions and say yes or no to the lines above. Your answers go to a second round, and I apply nothing until you approve the lines.

Drafts are under `.superpowers/spec-drafts/2026-10-02-lending-design/round-1/`, and the full gate text is in `gate.md` there.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/gates/t-integrate-2.md`

~~~~~~
Here is the gate text from the integration round. Nothing has been applied to `spec/`.

## lending (new capability, rests on keep-items)

**Added**
- [r1] When the reader lends a book the shelf holds to a named friend, the shelf records that friend as having the book.
- [r2] If the reader lends a book that is already lent, the shelf refuses the lend because the book is out.
- [r3] If the reader lends a book the shelf does not hold, the shelf refuses the lend because the book is not held.
- [r4] When the reader takes a lent book back, the shelf records the book as on the shelf again.
- [r5] If the reader takes back a book that is not lent, the shelf refuses because the book is not out.
- [r6] When the reader asks who has a book that is lent, the shelf answers with the friend's name.
- [r7] While a book is lent, the shelf still holds it.

## keep-items

**Added**
- [r6] If the reader adds a book whose title is empty, the shelf refuses the add because the title is empty.
- [r7] When the reader removes a book the shelf holds, the shelf no longer holds it.

**Changed**
- [r3] now: When the reader asks how many books there are, the shelf answers with the number of books it holds that are not lent.
  was: When the reader asks how many books there are, the shelf answers with the number of books it holds.

**Removed** (deletes contract, and id r4 is retired)
- [r4] When the reader asks for the title of a book by its id, the shelf answers with the title.

A ledger entry is also drafted: `design-decision/lent-books-held-not-counted`, dated 2026-10-02. The round also cut 2 sentences of the note.

## Questions

1. **Friend limit** ("A friend should not hold too many books at once"). The note gives no bound and no response.
   - If it is a rule, what is N? Lending [r8] would be "If the reader lends a book to a friend who already has N books, the shelf refuses the lend because the friend holds too many books."
   - If it is only intent, the sentence is cut and no line is added.
2. **Name comparison** ("Names are compared without regard to case").
   - If a reader can observe it, lending [r9] would be "Where friends' names differ only in case, the shelf treats them as the same friend."
   - If not, it stays an Implementation line, as drafted.
3. **Asking who has a book that is not lent** (the note doesn't say).
   - If refused, lending [r8] would be "If the reader asks who has a book that is not lent, the shelf refuses because the book is not out."
   - If it answers, the line would be "When the reader asks who has a book that is not lent, the shelf answers that the book is on the shelf."
4. **Lending without a friend's name** (the note doesn't say).
   - If refused, lending [r8] would be "If the reader lends a book without naming a friend, the shelf refuses the lend because no friend is named."
   - If not, there is no line.
5. **Removing a book the shelf does not hold** (the note doesn't say).
   - If refused, keep-items [r8] would be "If the reader removes a book the shelf does not hold, the shelf refuses the removal because the book is not held."
   - If not, there is no line.
6. **Removing a lent book** (the note says "left for later").
   - If refused in the meantime, keep-items [r8] would be "If the reader removes a book that is lent, the shelf refuses the removal because the book is out."
   - If unspecified, there is no line and it stays Not yet. What promotes it out of Not yet?
7. **Due dates** (Not yet). What promotes them? The note gives no signal.
8. **Empty title.** Does a title of only spaces count as empty?
   - If yes, keep-items r6 becomes "If the reader adds a book whose title is empty or only spaces, the shelf refuses the add because the title is empty."
   - If no, r6 stays as drafted.
9. **Where the count rule lives.**
   - As drafted, keep-items r3 changes, so keep-items refers to lent books while lending rests on keep-items.
   - The other reading leaves keep-items r3 unchanged and adds lending [r8]: "While a book is lent, the shelf leaves it out when the reader asks how many books there are."

Please give a yes or no on the lines above and an answer to each question. Your answers go to a second round, and nothing is applied to `spec/` until you approve.

The full gate text is at `.superpowers/spec-drafts/2026-10-02-lending-design/round-1/gate.md`.
~~~~~~

## `/home/vscode/scratch/shopsystem-bdd/ids/gates/t-integrate-2-late.md`

~~~~~~
That was a notification from the writer sub-agent that ran inside the integration round. It isn't a message from you, so I haven't treated it as an answer or an approval.

It repeats the same lines and the same nine questions I showed you above, with the same ids and wording. It adds two details:
- **Sentences not turned into lines:** the "Two things change about keeping books." sentence and the note's title, date and status lines are cut.
- **`index.md` draft:** lending is added to composition, order of building and testing.

Nothing has been applied to `spec/` and nothing has been committed. I'm waiting for your yes or no on the lines and your answers to questions 1–9.
~~~~~~
