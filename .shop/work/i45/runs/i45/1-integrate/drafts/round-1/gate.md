# Gate: q26, round 1

Drafts: `.shop/scratch/1-integrate/drafts/round-1/spec/`. No decision file is drafted (see Q10).

## spec-integration (adds r47–r53, removes r13; r13 goes to `retired`)

Added:
- [r47] The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. (q26 line 1)
- [r48] **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts. (line 3; see Q2, Q11)
- [r49] The glossary shall define each event and each condition that a line's trigger names. (line 4 as given; see Q6, Q9)
- [r50] **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. (line 5; see Q4)
- [r51] **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. (line 6)
- [r52] The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. (line 7)
- [r53] **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. (line 7; see Q8)

Removed:
- [r13] **When** a line is changed, `integrating-a-proposal` shall keep its id. (line 7; see Q8)

## requests (adds r46)

- [r46] **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. (line 2, "When ... shall refuse" written as `If ... then` like r2; Q1 reading A, see Q1, Q7, Q12)

## spec-consistency (adds r28, removes r5; r5 goes to `retired`)

Added:
- [r28] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, each changed line retired and its replacement given a new id, through one gate pass for the term. (line 7; see Q8)

Removed, what it was:
- [r5] **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term.

## Glossary (adds, none has a `Not:`; the request gives none of the terms, see Q3)

- `term/implementation-detail`: - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column.
- `term/overlapping-triggers`: - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond.
- `term/conflicting-responses`: - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file.
- `term/catch-all-trigger`: - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names.
- `term/convention`: - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states.

## Decisions

None drafted.

## Questions (each marks a recommended reading; the drafted lines are reading A unless said)

**Q1 (requests r46, line 2).** What does `work request` check for "an implementation detail or a term the glossary does not define"?
- A (recommended, drafted): a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in a Behaviour line under `spec/capabilities/`: r46 as above.
- B (stricter): any word that is not a glossary term: "**If** a line given to `work request` names an implementation detail or uses a word that is not a glossary term, **then** `work request` shall refuse the line, naming the word and why it is refused." (nearly every line refused unless ordinary words are exempt)
- C: implementation details only: "**If** a line given to `work request` names an implementation detail, **then** `work request` shall refuse the line, naming the word and why it is refused."

**Q2 (spec-integration r48, line 3).** The check has no visible result. What does the round do with a finding?
- A (recommended): "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions."
- B: "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall dispatch the `capability-writer` again with the finding before the gate round starts."
- r48 as the request words it is drafted; A or B is added beside it or replaces it under a new id.

**Q3 (glossary; lines 2, 3, 5).** Five words the lines depend on have no entry.
- A (recommended, drafted): add the five entries above.
- B: add none; r46, r48 and r50 then depend on undefined words (spec-consistency r27).

**Q4 (spec-integration r50, line 5).** What counts as "a convention of the spec"?
- A (recommended, drafted with the `convention` entry): a rule `docs/capability-format.md` or a decision in `spec/decisions/` states.
- B: also any Behaviour line; the entry becomes "- **convention**: a rule of how the spec is written that `docs/capability-format.md`, a decision under `spec/decisions/` or a Behaviour line states."
- Clash: r50 settles a question without asking, while r1, r3 and r35 expect every question at the gate. A question r50 settles is not one the person is asked, so no change is drafted. If that is wrong, r35 takes an exception: "**When** `initiative-round` runs the kind `gate`, `initiative-round` shall give in its result one question for each decision the person is asked to make that no convention settles, each marking the recommended reading and giving the lines it concerns in full." (r35 retired, this line as r54).

**Q5 (spec-integration r47, line 1).** What counts as "a session that writes a request's lines"?
- A (recommended, drafted): every such session, the person's running `work request` and an integrate round giving lines into an upstream (r44) included.
- B: only the plugin's agents and rounds: "The plugin shall give a skill for writing requirement lines to the `capability-writer` and to each of its rounds that gives the lines of a request."

**Q6 (line 4, drafted as spec-integration r49).** "The glossary shall define..." names the glossary as the system, so no round or skill is responsible for it. Where does it go?
- A (recommended): under spec-integration, as "**When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it." (in place of r49)
- B: a row of the `spec-checker`'s table in spec-consistency: "| [r29] | an event or a condition that a line's trigger names and the glossary does not define |" (no r49)
- C: r49 as the request words it (drafted).
- Overlap: spec-consistency r27 already finds a word a line depends on that is neither a term nor spelled out; line 4 is stricter.

**Q7 (requests r46).** Which glossary does `work request` use, since it runs in the asker's repository with no checkout of the upstream's (r28)?
- A (recommended): the upstream's glossary and the upstream's `spec/capabilities/`: "...a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`..."
- B: the glossary and `spec/capabilities/` of the repository it runs in.

**Q8 (spec-integration r13, r53; spec-consistency r5, r28; line 7).** r13 ("keep its id") and spec-consistency r5 ("ids kept") say the opposite of line 7.
- A (recommended, drafted): retire r13 and r5; add r52, r53 and r28.
- B: leave r13 and r5 and add r52 only; the spec then contradicts itself.
- Unchanged under either reading: formulation r1 and r13 ("added or changed line"), which still read true under A.

**Q9 (spec-integration r49; line 4).** Do existing lines count? Most existing triggers name events with no entry.
- A (recommended): only lines drafted from now on (Q6 A's line).
- B: every line, existing ones included: r49 as drafted, and a work-item that adds the entries.

**Q10 (decision; line 7).** Line 7 reverses a rule `docs/capability-format.md` states, which decision 0031's Context relies on. A decision?
- A: yes: draft `spec/decisions/0073-a-changed-line-is-retired.md` (summary "A changed Behaviour line is retired and its replacement given a new id; no line keeps its id when its words change.", date 2026-10-28, status proposed, source [request/q26, record/2026-10-28-requirement-checking], by "the request q26, line 7, accepted"), and spec-integration's `rests_on` names it.
- B (drafted): no decision; r52 and r53 are the rule.

**Q11 (r48 and r33, spec-consistency r21).** Under the `catch-all trigger` entry, the general failure line ("If <system> cannot do what it was asked, then ...") is a catch-all trigger, so r48 would report it every round.
- A (recommended): it is not a finding: "**When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts." (in place of r48)
- B: it is a finding every time: r48 as drafted.

**Q12 (requests r46).** Does "refuse the line" refuse the whole request?
- A (recommended): yes, as r2: "..., **then** `work request` shall refuse, naming the word and why it is refused, and change nothing."
- B: only the line; the other lines are written: r46 as drafted, and "**When** `work request` refuses a line, `work` shall write the request with its other lines."

## Cut sentences

None.
