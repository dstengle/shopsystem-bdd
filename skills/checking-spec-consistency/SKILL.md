---
name: checking-spec-consistency
description: Use when the person asks to check the spec's consistency, its terms or its glossary, or whether its lines and scenarios say the same thing, in a repository with spec/ capability files with [r<n>] ids. Also use when the person asks to fix what such a check found (fix mode). Run on demand only; integration and formulation rounds do not run it.
---

# Checking Spec Consistency

## Overview

A bounded context's spec should agree with itself: one word means one thing, one thing has one word, a line has one reading, and a scenario says what its line says. This skill checks that and, in fix mode, walks the person through the fixes. `model check` judges the words the glossary avoids (`v_t1` (a word the glossary avoids), `v_t2` (a term has two entries), `v_t3` (an avoided word is a term)); a blind `shopsystem-bdd:spec-checker` agent judges meaning, one dispatch for each capability and one for the whole context.

The skill runs when the person asks for it, never otherwise. Integration and formulation rounds do not run it, and no other skill invokes it.

The glossary's form, term ids and `v_t*` rules are in `docs/capability-format.md` in this plugin, "Glossary". Scripts: `<this skill's base directory>/../../scripts/`. `scripts/model check` takes no path or other argument: it reads all of `spec/` and `features/`. It shows the first ten rows of each rule and then `... and <n> more`, so this skill runs it as `scripts/model check --limit 100000`: `--limit` is an option, not a path, and with it every row is shown.

The session reads only `spec/`, `features/`, its drafts path and the agents' replies and findings files, never the source or the step definitions. Running one scenario by name, as formulating-features does to deprecate it, is a run, not a reading.

**Report mode** is the default: it ends with one findings file and changes nothing else. **Fix mode** runs only when the person asks for it, on the findings of a check.

A repository whose Behaviour lines have no `[r<n>]` ids is migrated to ids first (migrating-to-capabilities, "Adding Ids").

## The Check

Both modes start here. Choose the drafts path `.shop/scratch/drafts/<date>-consistency/`; the check is `round-1/`.

1. **State the count.** Count the capability files under `spec/capabilities/`. Before anything else, tell the person: "This check runs `model check`, then dispatches <n + 1> spec-checkers: one for each of the <n> capabilities and one for the whole context." Then note `git status --porcelain`.
2. **Run `scripts/model check --limit 100000`**, with no other argument, and keep its output as `<drafts path>/round-1/model-check.txt`. Its `v_t1`, `v_t2` and `v_t3` rows are findings; rows of any other rule are not this check's findings. Exit 2 with a message that names clingo and `pip install clingo` means clingo is missing: the findings file says that `v_t*` was not checked, and the check goes on. Any other exit 2 is a failed run: stop and report it.
3. **Dispatch** the spec-checkers, all in one message so they run together: the capability brief once for each capability, the context brief once. Describe each `consistency: check <capability>`, and the context's `consistency: check whole context`. Give them no other paths.
4. **Wait for your agents.** Their finishing is not certain to wake you, and a turn ended while one runs leaves the check unfinished. After dispatching, wait in one shell command for every reply file to exist, looking every few seconds, for up to nine minutes; run it again if it times out with agents still working. Do nothing else meanwhile, and do not end your turn. An agent with no reply file after two waits is dispatched again, once; after that, the check stops and names it.
5. **Check the porcelain.** `git status --porcelain` matches the porcelain noted in step 1, but for entries under the drafts path: an agent that wrote outside it goes back with those files removed.
6. **Write the findings file**, `<drafts path>/findings.md`, from `model-check.txt` and the agents' findings files, in this order:
   - `## Terms`: one `### <word> / <word>` heading per term cluster, the words one thing goes by or the thing one word names, with every finding about them: the `v_t*` rows of its words, one word used for two things, two words used for one thing, a thing with no glossary entry.
   - `## Lines with two readings`: each line, quoted, with its two readings.
   - `## Lines in the wrong pattern`: each line, quoted, with the EARS pattern it uses and the one what starts its behaviour asks for.
   - `## Other drift`: each scenario whose wording drifts from its line, and anything else.

   A drift finding about a word goes under that word's term cluster. Number the findings `F1`, `F2` and on, across the file. Each finding names its ids (`capability/<name>#r<n>`, `features/<name>.feature:<title>`, `term/<term>`) and quotes the words. Two agents' findings about one thing are one finding.

**Report mode ends here.** Reply to the person with the findings file's path and the count in each group. Nothing outside the drafts path changes and nothing is committed. If `.gitignore` lacks `.shop/scratch/`, say so and leave it.

## Fix Mode

Fix mode works through a findings file, in four steps, in this order. It takes the findings file of a check this session ran, or one the person names; with neither, it runs The Check first. Before step 1 the working tree is clean of other work, or fix mode stops and says so; if `.gitignore` lacks `.shop/scratch/`, add it and commit that line alone. A finding's state is written beside it in the findings file as it is settled: `applied <commit>`, `rejected` or `deferred`.

Steps 1 to 3 each begin by running `scripts/model check --limit 100000` and keeping its output as `<drafts path>/fix/step-<k>-before.txt`, and each ends by running it again and comparing the rows with that kept run: a row in both was there before and is not the step's. Report to the person, before the next step, the rows that went and the rows that came. The commits inside a step are guarded by the checks the skill they go through runs before each commit; this closing run reports, and it is the next step's kept run. A new row the step made that its skill does not expect is fixed before the next step begins. Where `model check` exits 2 with a message that names clingo and `pip install clingo`, clingo is missing: say so, and the skills a step goes through check by hand, as each says. Any other exit 2 is a failed run: stop and report it.

1. **Terms.** One term cluster at a time. Propose a glossary entry in the form `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, with its id `term/<term>`. The term is the word the glossary already has for the thing; where it has none, the word most of the lines use. `Not:` lists the cluster's other words. Where one word is used for two things, propose two entries, one for each thing: at most one of them keeps the shared word, the other thing's lines take a new word, and the shared word goes after `Not:` in the entry that does not keep it. Before showing a proposal, run `grep -rniwE '<word>s?' spec/capabilities` for each word after its `Not:`, so the proposal lists every line that uses it. With the entry, show each line that would change to apply it. Ids are kept: a changed line keeps its id. The entry and its line changes go through integrating-a-proposal, as one gate pass for the term:
   - At most two lines change: its small-change path, and the proposal is that path's gate. Write the changed lines yourself, from `spec/` alone, and show each in full with its id and what it was. The person's yes to the proposal is the gate's yes. Then apply, check and commit as that path says, the commit naming the term and each id it changes.
   - More than two lines change: its full path. The proposal shows each line's id and the words that would change. The person's yes to it is not a gate pass: it chooses the entry the note has, and initiative-round's gate is the term's one gate pass. Write the note `<drafts path>/fix/term-<term>.md`: the entry the person approved, with the date, and one sentence for each line change ("In `capability/<name>#r<n>`, <word> becomes <term>."). Dispatch `initiative-round` with the job `integrate` and that note, as integrating-a-proposal's "Who Does What" says; its gate text is the term's one gate pass, and the person's yes to it goes to a `initiative-round` with the job `apply`.

   In a repository that keeps `.shop/work/`, the term and its line changes ride with a capability-proposal that lists `term/<term>` (integrating-a-proposal, "Terms"). The person may give another word or another definition: the proposal changes and is shown again. A `v_t2` or `v_t3` row is settled by changing the glossary entries it names, through the same gate pass. A `v_t*` row is never rejected or deferred: the proposal for its cluster settles it. A cluster whose entry is in the glossary already and whose lines need no change has no gate pass: its scenarios follow in step 2. Any other cluster the person declines is `rejected`, or `deferred` when they say later. Integrating-a-proposal's hand-off to formulation is step 2 of this skill.
2. **Scenarios follow.** Every scenario a `v_t1` row of this step's kept run names is reworded to its line through formulating-features' small-change path ("The Small-Change Path"), with no further approval: the line and the term are approved. Where clingo is missing, they are the scenarios `grep -rniwE '<word>s?' features` finds for each word after a `Not:`, those tagged `@deprecated` left out. Write the reworded scenarios yourself, from the line and the glossary, and splice, deprecate, rebind, check and commit as that path says, the commit containing the feature files and the test files `rebind` changed. A rewording that changes only a title is rebound and goes no further. One that changes a step's text is a changed scenario, as that path says, for a work-item to turn green. Tell the person which scenarios changed their steps.
3. **One at a time.** First the lines with two readings, then the lines in the wrong pattern, then the other drift, one finding to the person at a time, each answered before the next is asked.
   - **A line with two readings.** Ask one question: the line, quoted with its id, and its two readings, each with the line it would give. The answer is integrated through integrating-a-proposal's question path: when it changes at most two lines, its small-change path, the lines written by you from the answer and shown at its gate; otherwise a `initiative-round` with the job `integrate`, the question, its readings and the person's answer in their words, whose writer gets the question brief, and on the person's yes to its gate text a `initiative-round` with the job `apply`, as that skill's "Who Does What" says. Either path ends in its gate, its commit and its hand-off to formulation.
   - **A line in the wrong pattern.** Ask one question: the line, quoted with its id, the pattern it uses, and the line it would be in the pattern its trigger asks for. The answer goes through the same path as a line with two readings; a pattern change keeps the line's meaning, and its scenario is reworded only where its wording differs from the new line.
   - **Other drift.** Ask which side is right: the line, quoted with its id, and the scenario's words, quoted with its title. The line is right: the scenario is reworded to its line through formulating-features' small-change path, with no further approval. The scenario is right: the line changes through integrating-a-proposal's small-change path, at its gate. Neither, or not now: the finding is `deferred`.

   A finding the person says to leave is `rejected`. A `deferred` finding, from this step or step 1, is recorded as an observation: appended to `.shop/records/observations.md` in the form of the entries there (`## observation/<context id>/<date>-consistency-<F<n>>`, then `about:` the capability, `by: the person`, `date:`, and the finding in one paragraph with its ids), and that file is committed alone, `observation: consistency findings`, before step 4. Its state in the findings file says `deferred, observation <its id>`.
4. **End.** Run `scripts/model check --limit 100000`, with no other argument. Fix mode ends when every finding in the findings file is `applied`, `rejected` or `deferred` and this run reports no `v_t1`, `v_t2` or `v_t3` row. A `v_t*` row still there goes back to step 1 as a cluster of its own, and steps 2 to 4 follow it again. Where `model check` exits 2 with a message that names clingo and `pip install clingo`, clingo is missing: check each word after a `Not:` by hand (`grep -rniwE '<word>s?' spec/capabilities features`, leaving out scenarios tagged `@deprecated`), and say so in the reply. Any other exit 2 is a failed run: stop and report it. Reply to the person with the commits, the count of findings applied, rejected and deferred, and each scenario whose steps changed.

## The Capability Brief

Send this to each agent verbatim, with the names and paths filled in.

```
Check spec/capabilities/<NAME>.md against features/<NAME>.feature.
You may read those two files and spec/index.md. Nothing else: not docs/,
not the source, not the step definitions.

Judge each Behaviour line against the scenario that has its @r<n> tag.
A scenario tagged @deprecated formulates no line: leave it out. A scenario
may have several @r<n> tags: judge it against each line it names. Find:
- wrong pattern: a line whose EARS pattern does not fit what starts its
  behaviour (a response to a command or an event is When ..., a refusal or
  fault is If ... then, behaviour that lasts for a period is While, one that
  depends on configuration is Where, and only what is true with no trigger at
  all has none);
- drift: a scenario whose wording differs from its line: it names a thing
  by another word, adds or drops a condition, or pins an outcome the line
  does not state;
- two readings: a line that admits two readings.
Use spec/index.md's Glossary for what its terms mean. Decide nothing: never
say which side is right, never pick a reading, never rewrite a line or a
scenario.

Write your findings to <DRAFTS PATH>/round-<N>/<NAME>.findings.md, and
nowhere else, one per finding: its kind (wrong pattern | drift | two readings); its ids
(capability/<NAME>#r<n>, features/<NAME>.feature:<scenario title>); the
words, quoted; for wrong pattern, the pattern the line uses and the one its trigger asks for; for drift, one line saying what differs; for two readings,
the two readings, one line each. Write "none" when you find nothing.
Reply with the count of each kind and the findings file's path, nothing
else. Write that same reply, last of all, to
<DRAFTS PATH>/round-<N>/<NAME>.reply.md.
```

## The Context Brief

```
Check the language of this bounded context's spec.
You may read spec/index.md and every file under spec/capabilities/. Nothing
else: not features/, not docs/, not the source.

Read every Behaviour line and spec/index.md's Glossary. Find:
- one word for two things: a word the lines use for two different things;
- two words for one thing: two words the lines use for the same thing;
- a missing term: a thing several lines name that the Glossary has no
  entry for.
Decide nothing: never choose which word is the term, never rewrite a line or
an entry.

Write your findings to <DRAFTS PATH>/round-<N>/whole-context.findings.md,
and nowhere else, one per finding: its kind (one word for two things | two
words for one thing | missing term); the words; each line that uses them,
by its id (capability/<name>#r<n>) and quoted; any glossary entry they
concern, by its id (term/<term>). Write "none" when you find nothing. Reply
with the count of each kind and the findings file's path, nothing else.
Write that same reply, last of all, to
<DRAFTS PATH>/round-<N>/whole-context.reply.md.
```

## Red Flags

- A spec-checker dispatched before the person was told how many there will be
- The check run because an integration or formulation round finished, not because the person asked
- Report mode that edited `spec/`, `features/` or the glossary, or committed anything
- A finding without its ids
- A term's entry and its lines approved in two gate passes, or its lines changed before the person's yes
- A scenario reworded to a term before the terms were settled, or kept back for the person's approval
- Two findings asked in one question
- A `v_t*` row marked rejected or deferred
- `model check` given a path, or clingo called missing on an exit 2 whose message does not name it
