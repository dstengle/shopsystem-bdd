## Drafts

/tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/spec-integration.md
/tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/requests.md
/tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/spec-consistency.md
/tmp/work-run-i45-fukf4k_n/i45-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/index.md

(spec-integration: frontmatter and Behaviour; requests: Behaviour only, frontmatter unchanged; spec-consistency: frontmatter and Behaviour; index.md: the whole `## Glossary`. No decision file is drafted; see Q10.)

## Change list

Behaviour lines:

| change | capability | id | line | from the note |
|---|---|---|---|---|
| added | spec-integration | r47 | The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines. | Line 1: "The plugin shall give a skill for writing requirement lines to the `capability-writer` and to a session that writes a request's lines." |
| added | requests | r46 | **If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused. | Line 2: "**When** `work request` takes a line that names an implementation detail or a term the glossary does not define, `work request` shall refuse the line, naming the word and why." (written as `If ... then` because it is a refusal, as requests r2 is; "a term the glossary does not define" written as Q1's reading A) |
| added | spec-integration | r48 | **When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts. | Line 3: "**When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts." |
| added | spec-integration | r49 | The glossary shall define each event and each condition that a line's trigger names. | Line 4: "The glossary shall define each event and each condition that a line's trigger names." (as given; see Q6) |
| added | spec-integration | r50 | **When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking. | Line 5: "**When** a gate round finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking." |
| added | spec-integration | r51 | **When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading. | Line 6: "**When** a round of the kind `integrate` gives a question with readings, `initiative-round` shall draft the lines of each reading." |
| added | spec-integration | r52 | The plugin shall say, in the spec's format rules and in the `capability-writer`'s instructions, that a changed line is retired and its replacement given a new id. | Line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." (one system named, the plugin, for one "shall" and one subject) |
| removed | spec-integration | r13 | **When** a line is changed, `integrating-a-proposal` shall keep its id. | Line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." (see Q8) |
| added | spec-integration | r53 | **When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id. | Line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." (see Q8) |
| removed | spec-consistency | r5 | **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, ids kept, through one gate pass for the term. | Line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." (see Q8) |
| added | spec-consistency | r28 | **Where** fix mode is asked for, `checking-spec-consistency` shall first propose, for each term cluster, a glossary entry with its `Not:` words, and put it, with the line changes that apply it, each changed line retired and its replacement given a new id, through one gate pass for the term. | Line 7: "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id." (see Q8) |

Glossary terms (the note gives none of them; each is Q3, drafted as its reading A):

| change | term | entry | from the note |
|---|---|---|---|
| added | term/implementation-detail | - **implementation detail**: what a line says of how its system gives a response rather than what the narrator observes: the words of a message, an exit or status code, a field name, a table or a column. | Line 2: "...a line that names an implementation detail or a term the glossary does not define..." |
| added | term/overlapping-triggers | - **overlapping triggers**: the triggers or conditions of two lines of one system that can both hold at once, so that both lines respond. | Line 3: "...for overlapping triggers, conflicting responses and catch-all triggers before the gate round starts." |
| added | term/conflicting-responses | - **conflicting responses**: the responses of two lines with overlapping triggers that cannot both be given, such as two statuses for one node, or a refusal and a write of one file. | Line 3 (as above) |
| added | term/catch-all-trigger | - **catch-all trigger**: a trigger or condition of a line that holds for every event or every condition of its system, such as any failure at all, rather than for one event or condition it names. | Line 3 (as above) |
| added | term/convention | - **convention**: a rule of how the spec is written that `docs/capability-format.md` or a decision under `spec/decisions/` states. | Line 5: "...whose readings differ only in wording that a convention of the spec settles..." |

No entry has a `Not:` list (the note names no word to avoid), so none can be another term or appear in a line or scenario (v_t1, v_t3). None of the five terms is an existing term; "convention" appears elsewhere only in decision 0046's body, in the same sense.

## Decision files

None drafted. Decision numbers run to 0072, so a decision would be `spec/decisions/0073-<slug>.md` (not 0024, which is taken). See Q10.

## Questions

Q1 (requests r46; line 2). What does `work request` check for "an implementation detail or a term the glossary does not define"? ("A term the glossary does not define" can't be taken literally: by definition, a term is a glossary entry.)
- A (recommended; drafted): a word of a fixed list of implementation details, or a word that is neither a glossary term nor used in any Behaviour line under `spec/capabilities/`: "**If** a line given to `work request` names an implementation detail or uses a word that is neither a glossary term nor a word of a Behaviour line under `spec/capabilities/`, **then** `work request` shall refuse the line, naming the word and why it is refused." (Implementation would then list the words `work request` takes as implementation details.)
- B (stricter): any word of the line that is not a glossary term: "**If** a line given to `work request` names an implementation detail or uses a word that is not a glossary term, **then** `work request` shall refuse the line, naming the word and why it is refused." (Common words such as "line" and "file" are not terms, so nearly every line would be refused unless a list of ordinary words is exempt.)
- C: implementation details only, and the glossary is left to the gate: "**If** a line given to `work request` names an implementation detail, **then** `work request` shall refuse the line, naming the word and why it is refused."

Q2 (spec-integration r48; line 3). Checking "before the gate round starts" has no result anyone can see. What does the round do with a finding?
- A (recommended): give each finding, with the two ids, in the result and in the gate's questions; the round otherwise ends as it would: "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall give the finding, naming both lines' ids, in its result and in the gate's questions."
- B: send the finding back to the writer, who drafts again with the clash named or the old line retired and replaced, before the gate: "**When** a round of the kind `integrate` finds a drafted line whose trigger overlaps, whose response conflicts with, or whose trigger catches all of a line of `spec/`, `initiative-round` shall dispatch the `capability-writer` again with the finding before the gate round starts."
- Drafted: r48 as the request words it. A or B is added beside it, or replaces it under a new id.

Q3 (index.md Glossary; lines 2, 3, 5). Five words the lines depend on have no glossary entry: implementation detail, overlapping triggers, conflicting responses, catch-all trigger, convention.
- A (recommended; drafted): add the five entries in the change list above, with no `Not:` lists.
- B: add none. Then r46, r48 and r50 depend on undefined words, which spec-consistency r27 would report.

Q4 (spec-integration r50; line 5). Which conventions count as "a convention of the spec"?
- A (recommended; matches the drafted `convention` entry): a rule that `docs/capability-format.md` or a decision in `spec/decisions/` states. The line stays as drafted: "**When** a round of the kind `gate` finds a question whose readings differ only in wording that a convention of the spec settles, `initiative-round` shall take the reading the convention gives and note it in its result in place of asking."
- B: any Behaviour line as well. Same line; the entry becomes: "- **convention**: a rule of how the spec is written that `docs/capability-format.md`, a decision under `spec/decisions/` or a Behaviour line states."
- Clash to note: r50 settles some questions without asking, while r1 ("every question the note left open"), r3 ("answered every question") and r35 ("one question for each decision the person is asked to make") expect every question at the gate. Under either reading, r50's settled question isn't one the person is asked; say yes if that reading is right. Otherwise r35 would take an exception: "**When** `initiative-round` runs the kind `gate`, `initiative-round` shall give in its result one question for each decision the person is asked to make that no convention settles, each marking the recommended reading and giving the lines it concerns in full." (r35 retired, this line as r54.)

Q5 (spec-integration r47; line 1). What counts as "a session that writes a request's lines"?
- A (recommended; drafted as given): every session that writes a request's lines, including the person's session running `work request` and an integrate round giving lines of a request into an upstream (r44). The line stays as drafted.
- B: only the plugin's agents and rounds, not the person's own session: "The plugin shall give a skill for writing requirement lines to the `capability-writer` and to each of its rounds that gives the lines of a request."

Q6 (line 4; drafted as given as spec-integration r49). "The glossary shall define ..." puts the glossary in the system's place, and no round or skill does anything, so the line passes v_e1/v_e2 in form but nobody is responsible for it. Where does it go?
- A (recommended), under spec-integration: "**When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, `initiative-round` shall draft a glossary entry for it." (r49 retired before approval; this line as r49 in its place, since r49 is not yet approved.)
- B, under spec-consistency as a row of the `spec-checker`'s table: "| [r29] | an event or a condition that a line's trigger names and the glossary does not define |" (r49 not added to spec-integration).
- C: r49 as the request words it, under spec-integration (drafted).
- Overlap: spec-consistency r27 already finds "a word a line depends on that is neither a glossary term nor spelled out in the line". Line 4 is stricter: spelling a word out in the line is not enough.

Q7 (requests r46; line 2). Which glossary is used? `work request` runs in the asker's repository with no checkout of the upstream's (r28).
- A (recommended): the glossary of the upstream, the context asked, which a request proposes against: "...a word that is neither a term of the upstream's glossary nor a word of a Behaviour line under the upstream's `spec/capabilities/`...".
- B: the glossary of the repository `work request` runs in: "...a word that is neither a term of the glossary of the repository it is run in nor a word of a Behaviour line under its `spec/capabilities/`...".

Q8 (spec-integration r13, r53; spec-consistency r5, r28; line 7, "The spec's format rules and the `capability-writer`'s instructions shall say that a changed line is retired and its replacement given a new id."). r13 ("When a line is changed, `integrating-a-proposal` shall keep its id") and spec-consistency r5 ("..., ids kept, ...") say the opposite.
- A (recommended; drafted): retire r13 and r5. Add spec-integration r53 "**When** a line is changed, `integrating-a-proposal` shall retire the line and give its replacement a new id." and spec-consistency r28, which is r5 with "ids kept" replaced by "each changed line retired and its replacement given a new id". Add r52 (line 7).
- B: leave r13 and r5 and add r52 only. The spec then contradicts itself: r52 says changed lines are retired, while r13 and r5 say changed lines keep their ids.
- Left unchanged under either reading: formulation r1 and r13, which say "added or changed line". Under A, a changed line arrives as an added line, so they still read true.

Q9 (spec-integration r49; line 4). Do lines that already exist count? Most triggers in `spec/` name events with no glossary entry ("the person says yes", "a line is changed", "the pass starts").
- A (recommended): only lines drafted from now on: "**When** a round of the kind `integrate` drafts a line whose trigger names an event or a condition the glossary does not define, ..." (Q6 A's line).
- B: every line, existing ones included, which means glossary entries for every existing trigger before the line holds: r49 as drafted, and a work-item that adds the entries.

Q10 (decision; line 7). Line 7 reverses a rule `docs/capability-format.md` states ("A changed line keeps its id"), and decision 0031's Context relies on that rule. Should the reversal be a decision?
- A: yes. Draft `spec/decisions/0073-a-changed-line-is-retired.md` with summary "A changed Behaviour line is retired and its replacement given a new id; no line keeps its id when its words change.", date 2026-10-28, status proposed, source [request/q26, record/2026-10-28-requirement-checking], by "the request q26, line 7, accepted". spec-integration's `rests_on` then names design-decision/a-changed-line-is-retired.
- B (as expected by the dispatch; drafted): no decision. r52 and r53 are the rule, and `docs/capability-format.md` is changed by the work-item that delivers r52.

Q11 (clash; spec-integration r48 and r33, spec-consistency r21). Under the drafted `catch-all trigger` entry, the general failure line that `docs/capability-format.md` prescribes ("If <system> cannot do what it was asked, then ...", such as r33 and spec-consistency r21) is a catch-all trigger, so r48 would report it every round.
- A (recommended): the general failure line is not a finding: "**When** a round of the kind `integrate` has drafted its lines, `initiative-round` shall check them against the lines of `spec/` for overlapping triggers, conflicting responses and catch-all triggers other than a capability's general failure line before the gate round starts." (in place of r48, which is not yet approved)
- B: it is a finding every time: r48 as drafted.

Q12 (requests r46; line 2). Does "refuse the line" refuse the whole request? requests r2 refuses and changes nothing.
- A (recommended): the whole request is refused and nothing changes, as with r2: r46 ending "..., **then** `work request` shall refuse, naming the word and why it is refused, and change nothing."
- B: only the line is refused, and the other lines are written: r46 as drafted, and "**When** `work request` refuses a line, `work` shall write the request with its other lines." (as requests r47)

## Cut sentences

None. Each of the seven lines is a Behaviour line (line 7 gives three lines and two removals).
