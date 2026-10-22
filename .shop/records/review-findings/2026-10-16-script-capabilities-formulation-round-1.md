---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-capabilities-formulation-round-1
kind: review-finding
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement, capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools, bounded-context/missingmass.io/shopsystem/shopsystem-bdd]
date: 2026-10-16
---

# Script capabilities formulation, round 1: formulator replies

The feature-formulator's round-1 replies (coverage tables, questions on lines with two readings, cases no line mentions) for the script capabilities formulated on 2026-10-16: batch-measurement, design-model-check, feature-file-tools and slice-plan-tool (since removed from the spec, hence the bounded context). analysis-tools was drafted in this round too but left no reply file. Their questions were answered by rewording the lines, which round 2 formulated; the round's feature drafts are archived in archive/2026-10-16-script-capabilities-drafts-round-1.

Archived from git-ignored scratch; each file's text as it was.

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/batch-measurement.reply.md`

~~~~~~
# batch-measurement, round 1

Draft: /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/batch-measurement.feature

## Coverage

| id | line | scenario |
|---|---|---|
| r1 | "When `measure batch <archive file>` is run, `measure` writes one facts file for the batch running from the commit that added the archive file before it to the commit that added its own." | an archive file's batch runs from the archive commit before it to its own |
| r2 | "Where no archive file is given, `measure batch` measures the open batch, from the last archive commit to now, reading the living plan." | without an archive file the open batch is measured from the last archive commit to now |
| r3 | "Where `--from` or `--to` is given, as a commit or an ISO time, `measure batch` uses it in place of that end of the batch." | a given --<option> replaces that end of the batch (Outline) |
| r4 | "Where no `--out` is given, `measure batch` writes the facts to `docs/superpowers/measurements/<archive file's name>.json`." | without --out the facts go under measurements in the archive file's name |
| r5 | "If the archive file was not added by any commit, `measure batch` refuses, naming the file." | an archive file no commit added is refused |
| r6 | "If a transcript's shape is not known, `measure batch` refuses, naming the file and what was missing, and writes no facts file." | a transcript of an unknown shape is refused and no facts are written |
| r7 | "If the facts file exists and `--replace` is not given, `measure batch` refuses and leaves the file as it was." | an existing facts file is not written over without --replace |
| r8 | "If no dispatch is found inside the batch, `measure batch` refuses, naming the window it searched, and writes nothing." | a batch with no dispatch inside it is refused |
| r9 | "A subagent transcript that starts inside the batch is counted as a dispatch, and one that starts outside it is not." | a subagent transcript is a dispatch only when it starts inside the batch (Outline) |
| r10 | "A request's usage is counted once in the facts, however many transcript rows carry it, and its reasoning is counted inside its output, not beside it." | none: returned as a question |
| r11 | "The facts count a session's own requests inside the batch as the controller's when that session dispatched there." | a dispatching session's own requests are the controller's |
| r12 | "The facts attribute a dispatch to a slice or batch work by its description, failing that by the task or slice its prompt names, and otherwise count it as unattributed." | a dispatch is attributed by its description, then its prompt, else unattributed (Outline) |
| r13 | "The facts count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor." | a reviewer's findings are counted as it wrote them |
| r14 | "The facts give each commit to the implementer running when it was made, and count the files it touched as production, test or other." | a commit goes to the implementer running when it was made |
| r15 | "The facts give each slice its Lands line from the archive file, or the living plan for the open batch, beside the files its dispatches touched." | each slice's Lands line sits beside the files its dispatches touched (Outline) |
| r16 | "The facts give the tasks the batch plan held when it was added and the tasks it held at the batch's end, the plan's hand-back entries and its suite record." | the facts give the plan's tasks at both ends, its hand-backs and suite record |
| r17 | "The facts hold no prompt, reply or tool content." | the facts hold no prompt, reply or tool content |
| r18 | "When `measure show <file>` is run, `measure` prints the facts file as tables." | show prints a facts file as tables |
| r19 | "When `measure compare <a> <b>` is run, `measure` prints the two facts files side by side." | compare prints two facts files side by side |
| r20 | "If `measure show` is given a file that is not a facts file `measure` wrote, `measure` refuses, naming the file." | show refuses a file measure did not write as facts |
| r21 | "If no archive file is given, no `--plan` is given and the repository holds no `docs/superpowers/plans/*-slices.md` or several, `measure batch` refuses, saying to name the living plan with `--plan`." | the open batch needs --plan when the living plan cannot be found (Outline) |
| r22 | "If no archive file was added before the batch's end and no `--from` is given, `measure batch` refuses, saying to give the batch's start with `--from`." | a batch with no archive before it needs --from (Outline) |
| r23 | "If `--from` or `--to` is neither a commit nor an ISO time, `measure batch` refuses, naming what it was given." | a --<option> that is neither a commit nor an ISO time is refused (Outline) |
| r24 | "If `--repo`, default the current directory, is not inside a git repository, or a git command `measure batch` runs fails, `measure` refuses with git's error." | git's failures are refused with git's error (Outline) |
| r25 | "Where no archive file is given, `measure batch` names the batch `--name`, default `open`, and without `--out` writes the facts to `docs/superpowers/measurements/<name>.json`." | the open batch is named by --name, default open (Outline) |
| r26 | "Where no archive file is given, the open batch starts at the last commit that added a file under `--archive-dir`, default `docs/superpowers/plans/archive`." | the open batch starts at the last commit that added a file under the archive directory (Outline) |
| r27 | "The facts hold the archive file's slices and every other slice a dispatch is attributed to, and for the open batch only the slices a dispatch is attributed to." | the facts hold the slices the batch planned and the slices dispatches were attributed to (Outline) |
| r28 | "The facts count, as ambiguous, the commits made while more than one implementer was running." | a commit made while two implementers ran is counted as ambiguous |
| r29 | "If no dispatch names a ledger and no `--tasks` is given, or the batch plan is in no commit, the facts leave tasks uncounted and hold a note saying why, and `measure batch` writes the note on stderr." | tasks are left uncounted with a note when the batch plan cannot be had (Outline) |
| r30 | "When `measure batch` has written the facts, it prints one line naming the file, the number of dispatches and slices, and the window." | a written batch is reported in one line |
| r31 | "The facts give each dispatch the closing status its reply states, and count replies that close BLOCKED, PARTIAL or NEEDS_CONTEXT as not done." | a reply closing <status> is counted as not done (Outline) |
| r32 | "The facts record the plugin and harness versions the transcripts name, and the batch's window as times and, where known, commits." | the facts record the versions the transcripts name and the window |
| r33 | "Where the batch starts at a commit, the facts give the files and lines changed from it to the batch's end commit, or to HEAD when the end is not a commit." | a batch starting at a commit gives the files and lines changed to its end (Outline) |
| r34 | "The facts count the dispatches given more than one prompt as resumed, the share of building time from the first branch review on with scouts left out, and the mean and summed starting context of the dispatches." | none: returned as a question |
| r35 | "When `measure show` is run, `measure` prints the repository, batch, window, plugin and harness versions and suite record, then the summary, roles and slices tables, the dispatches not done or not attributed, each hand-back and each note." | show prints the header, the tables, the exceptions, the hand-backs and the notes |
| r36 | "When `measure compare` is run, `measure` prints each summary figure and the output, new input, cache read and agent minutes per slice of both files, each file headed by its batch and plugin versions, with the ratio of the second to the first." | compare prints both files' figures with the ratio of the second to the first |
| r37 | "If `measure compare` is given a file that is not a facts file `measure` wrote, or `measure show` or `measure compare` a file it cannot read as JSON, `measure` refuses, naming the file." | a file measure cannot read as its facts is refused (Outline) |
| r38 | "If `measure` refuses, it says why on stderr and exits 1." | a refusal says why on stderr and exits 1 |

## Questions

- r10: "A request's usage is counted once in the facts, however many transcript rows carry it, and its reasoning is counted inside its output, not beside it."
  - Reading 1: the transcript's output figure already includes reasoning, so the facts' output is that figure and reasoning is not added to it (a request reporting output 100 and reasoning 40 counts 100).
  - Reading 2: reasoning is reported apart from output and the facts add it into output rather than keeping it as a separate figure (the same request counts 140).
- r34: "The facts count the dispatches given more than one prompt as resumed, the share of building time from the first branch review on with scouts left out, and the mean and summed starting context of the dispatches."
  - Reading 1: the share is the part of the batch's building time (scouts' time excluded from both the part and the whole) that falls from the first branch review's start onward.
  - Reading 2: the share is the time from the first branch review on, scouts excluded only from that part, over all building time including scouts; and "building time" may mean wall-clock time or summed agent minutes, which the line does not settle either.

## Cases no line mentions

- A commit made while no implementer was running (r14 gives it to "the implementer running"; r28 covers more than one).
- A dispatch whose reply states no closing status, or one other than BLOCKED, PARTIAL or NEEDS_CONTEXT: is it done (r31)?
- A session with requests inside the batch that dispatched nothing there: are its requests counted at all (r11)?
- A subagent transcript that starts inside the batch and runs past its end: are its requests after the end counted (r9)?
- A reviewer's reply that states no count of Minor (r13).
- A dispatch description that names both a slice and batch work, or two slices (r12).
- `--from` later than `--to`, or `--to` before the batch's start.
- `--plan` or `--name` given together with an archive file.
- An archive file given that is not under `--archive-dir`.
- `--out` naming a directory that does not exist.
- A transcript of unknown shape and no dispatch in the batch both at once: which refusal wins (r6, r8)?
- `measure compare` where a slice is in only one file, or the first file's figure is 0, so the ratio has no value (r36).
- A dispatch touching files that are not in its slice's Lands line, or a Lands line naming files no dispatch touched: does anything mark the difference (r15)?
- `--replace` given when no facts file exists (r7).
- `--tasks` naming a plan that cannot be read (r29 names only a missing ledger or a plan in no commit).
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/design-model-check.reply.md`

~~~~~~
## Coverage

| id | line | scenario |
|---|---|---|
| r19 | "`model` reads, under `--root` (default the current directory), `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, `decisions/*.md`, `work/<initiative>/*.md`, `records/observations.md` and any other Markdown under `records/` whose frontmatter has an `id`." | model reads the repository's files under its root (Outline) |
| r20 | "A scenario names a requirement by a tag `@r<n>`, its own or its feature's, in the feature file its capability is `formulated_as`, or `features/<capability name>.feature` when it gives none." | a scenario names a requirement by its tag in its capability's feature file (Outline) |
| r21 | "A reference written `<name>#r<n>` is read as a requirement of the capability `<name>` in the bounded context." | a reference written name#r<n> is that capability's requirement |
| r22 | "**If** a list names a reference that is not `<capability>#r<n>` or `<capability>#behaviour/r<n>`, or a range `#r<a>-r<b>` with a greater than b, `model check` reports it as unresolved." | a reference in neither requirement form, or a reversed range, is unresolved (Outline) |
| r23 | "**If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c." | none: question 1 |
| r24 | "**If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by` or `depends_on` names nothing, or nothing of the kind it needs, in the repository, `model check` reports it as unresolved." | a frontmatter reference to nothing, or to the wrong kind, is unresolved (Outline) |
| r25 | "**If** `spec/index.md` is missing or has no `id`, a capability's `id` is not `<context>/<file name>`, a capability has no `## Behaviour` section, or its `retired` lists an entry not written `r<n>`, `model check` reports a file problem naming the file." | a malformed index or capability file is a file problem (Outline) |
| r26 | "**If** a feature file is no capability's `formulated_as`, or two of its scenarios share a title, `model check` reports a file problem naming the file." | none: question 2 |
| r27 | "**If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, a priority is not a number or a date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file." | none: question 3 |
| r28 | "**If** a work-item accepts a requirement no scenario names yet, `model check` reports a file problem naming the work-item's file." | a work-item accepting a requirement no scenario names is a file problem |
| r29 | "**If** a decision has no `id`, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds, `model check` reports a file problem." | a malformed decision, record or frontmatter is a file problem (Outline) |
| r30 | "**If** `model check` finds a file problem, it prints each and exits 1." | file problems are each printed and fail the check |
| r31 | "**When** `model check` ends without `--json`, it prints the counts of violations, warnings, unresolved references and file problems." | the check ends with the four counts |
| r32 | "**Where** `--limit <n>` is given, default 10, `model check` prints at most n rows of each violated relation and how many more there are." | rows of a violated relation are limited, saying how many more there are (Outline) |
| r33 | "**Where** `--json` is given, `model check` prints the violations, warnings, unresolved references and file problems as one JSON object, with the same exit status." | with --json the check's findings are one JSON object (Outline) |
| r34 | "**If** an initiative that is not a capability-change has more than one part directly under it, `model check` reports it under v_k5, while a capability-change initiative may hold several capability-proposals." | only a capability-change initiative may hold several parts directly (Outline) |
| r35 | "**If** a capability-proposal argues more than one capability, `model check` reports it under v_k6." | a proposal arguing two capabilities is refused |
| r36 | "A capability-proposal at `formulated` counts as closed when `model check` decides whether an initiative may be done." | an initiative may be done when its proposal is formulated |
| r37 | "**When** `model decisions --check` finds `spec/decisions.md` is what `model decisions` would write, it says the file is current and exits 0." | a current decisions index passes the check |
| r38 | "**When** `model decisions` is run, it prints the file it wrote, and a decision file with no `id` is left out of the index." | writing the decisions index names the file and leaves out decisions with no id |
| r39 | "**If** `model why` is given an argument that is not a requirement reference, it says why and exits 2." | why refuses an argument that is not a requirement reference |
| r40 | "**If** no capability has the requirement `model why` names, it says so in place of the requirement's text and still lists the proposals that name it." | why on a requirement no capability has still lists its proposals |
| r41 | "**When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date, and one that only removes it leaves `model why` exiting 1." | none: question 4 |
| r42 | "A reference written `<capability>#behaviour/r<n>`, the requirement as a part in shopsystem-knowledge's IRI form, names the same requirement as `<capability>#r<n>`." | the behaviour/ form of a reference names the same requirement |
| r43 | "**Where** the bounded context's id is a path such as `<owner>/<product>/<context name>`, a capability written `<context name>/<name>` is read as `<context id>/<name>`, and the context name alone as the bounded context." | a path-shaped context id may be written by its context name (Outline) |
| r44 | "A scenario tagged `@holding` is not read as an acceptance-scenario, whatever `@r<n>` tag it carries." | a held scenario names no requirement |
| r45 | "**Where** a repository has no `decisions/` directory, `model` reads each `## decision/<slug>` heading of `spec/decisions.md` as a design-decision." | without a decisions directory the index's headings are the decisions |

## Questions

1. r23: "**If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c."
   - Reading A: "has" means the requirement is in the capability's Behaviour now. A proposal that removes r3 is then unresolved once r3 has been taken out of Behaviour and listed as retired, so every integrated removal is reported.
   - Reading B: for a removal, "has" also counts the capability's `retired` list. Removing an id the capability lists as retired resolves, and only removing an id that is in neither Behaviour nor `retired` is unresolved.
2. r26: "**If** a feature file is no capability's `formulated_as`, or two of its scenarios share a title, `model check` reports a file problem naming the file."
   - Reading A: only an explicit `formulated_as` counts, so `features/thing.feature` for a capability `thing` with no `formulated_as` is a file problem.
   - Reading B: the default r20 gives (`features/<capability name>.feature` when a capability names none) counts as that capability's `formulated_as`, so that file is not a file problem.
3. r27: "**If** a work directory has no `initiative.md`, ... `model check` reports a file problem naming the file."
   - Reading A: for a work directory with no `initiative.md`, the problem names the missing file, `work/<initiative>/initiative.md`.
   - Reading B: the problem names the work directory, `work/<initiative>/`, because there is no file to name.
4. r41: "... and one that only removes it leaves `model why` exiting 1."
   - Reading A: `model why` exits 1 when every capability-proposal that names the requirement only removes it, which is r17's case extended to removals. If one proposal adds it and a later one removes it, `model why` exits 0.
   - Reading B: `model why` exits 1 whenever any proposal naming the requirement only removes it, even if other proposals add or change it.

## Cases no line mentions

- r19: a `*.feature` outside `features/`, or Markdown in `work/` deeper than `work/<initiative>/`. Neither is said to be read or ignored.
- r19: `--root` naming a directory that does not exist, or one with no `spec/`.
- r20: a scenario carrying two `@r<n>` tags, or a feature tag together with a different scenario tag.
- r22: a range `#r<a>-r<a>` (a equal to b).
- r24: which kind each of `under`, `for`, `blocked_by`, `depends_on` and `source` needs. The draft tests a wrong kind only for `argues`.
- r29: a frontmatter value written as a block when there is no frontmatter at all, and a file with unparseable frontmatter.
- r32: `--limit 0`, a negative or non-numeric limit, and what "how many more" prints when nothing is left out.
- r33: whether `--json` with the clingo package missing still prints JSON.
- r34: a capability-change initiative with several parts directly under it that are not capability-proposals.
- r36: whether other statuses count as closed, and what is reported when a done initiative has an open part.
- r38: whether a decision with no `id` written by `model decisions` is also reported, and what `model decisions --check` does with one.
- r39: what `model why` does with a well-formed reference to a capability that does not exist (r40 covers a missing requirement, not a missing capability).
- r40: the exit status when no capability has the requirement but a proposal adds it.
- r43: whether a capability's own `id` may be written `<context name>/<name>` and still satisfy r25.
- r45: a repository with both a `decisions/` directory and `## decision/<slug>` headings in `spec/decisions.md`.

## Drafts

- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/design-model-check.feature (only the new scenarios, each headed by a comment quoting its line; r1-r18 not repeated)
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/design-model-check.reply.md
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/feature-file-tools.reply.md`

~~~~~~
# feature-file-tools: round 1 reply

Drafts:
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/feature-file-tools.feature (new feature file, whole)
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/feature-file-tools.reply.md (this reply)

## Coverage

| id | line | scenario |
|---|---|---|
| r1 | "`features` reads every `*.feature` under `--dir` (default `features`), recursively, and text inside a docstring is never taken as a scenario, keyword or tag." | every feature file under the directory is read, and docstring text is not |
| r2 | "**If** a feature file holds a `Rule:` block, `features` refuses, naming the file." | a feature file with a Rule block is refused |
| r3 | "**If** an edit would leave its file invalid, `features` refuses the edit and leaves the file as it was." | none: returned as a question |
| r4 | "**When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and the total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags." | none: returned as a question |
| r5 | "**When** `features list --tag <tag>` is run, `features` prints the file and title of each scenario whose tags, its feature's and its Examples' included, hold that tag." | listing by tag includes the feature's and the Examples' tags |
| r6 | "**When** `features list --title <text>` is run, `features` prints the file and title of each scenario whose title contains the text." | listing by title finds every scenario whose title contains the text |
| r7 | "**If** `features list` matches no scenario, `features` prints nothing and exits 1." | listing that matches nothing prints nothing and fails |
| r8 | "**When** `features tag <title> <slice>` is run on a title exactly one file holds, `features` makes the scenario's first slice tag the new one, removes any further slice tags, and leaves its other tags and every other line unchanged." | retagging replaces the first slice tag and drops the others |
| r9 | "**Where** the scenario has no slice tag, **when** `features tag` is run, `features` adds the new slice tag to the scenario's last tag line, or on a tag line of its own above the scenario when it has none." | a scenario without a slice tag gets one (outline) |
| r10 | "**If** `features tag` is given a title no file holds, or one several files hold, `features` refuses, naming every file that holds it, and changes no file." | retagging a title that is not in exactly one file is refused (outline) |
| r11 | "**If** `features tag` is given a tag not written `slice-<n>`, `slice-<n>.<m>` or `r<n>`, `features` exits 2 as bad usage and changes no file." | retagging with a tag that is neither a slice nor a requirement tag is bad usage |
| r12 | "**When** `features move <title> --to <file>` is run, `features` removes the scenario's block from its file and appends it unchanged to the end of the destination file." | moving a scenario takes its block to the end of the destination |
| r13 | "**Where** `--inline-background` is given, **when** `features move` is run, `features` puts the source Background's steps before the moved scenario's first step." | moving with the Background inlined puts its steps first |
| r14 | "**Where** `--carry-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line above the moved scenario." | none: returned as a question |
| r15 | "**If** the destination of `features move` does not exist, `features` refuses and changes no file." | moving to a destination that does not exist is refused |
| r16 | "**When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` prints how many scenarios match and exits 0." | two trees alike scenario by scenario pass the move check |
| r17 | "**If** a scenario's effective tags, description or steps differ between the two trees, `features verify-moved` names the scenario and which of them changed, and exits 1." | a scenario that changed in the move is named with what changed (outline) |
| r18 | "**If** a title is held by more than one scenario in either tree, `features verify-moved` names the title as a duplicate and exits 1." | a title held twice in either tree is a duplicate (outline) |
| r19 | "**When** `features hold <title> --for <new title>` or `--for-removal` is run, `features` gives the scenario the tag `@holding`, \" (held)\" at the end of its title and a description line naming what it is held for, and changes nothing else in it, whether or not the replacement exists yet." | holding a scenario marks it held and records what for (outline) |
| r20 | "**If** `features hold` is given a scenario already tagged `@holding`, `features` refuses it." | holding a scenario already held is refused |
| r21 | "**When** `features holding` is run, `features` lists each held scenario with what it is held for and the slice tag its replacement carries, or says that no scenario has the replacement's title, or that the slice removing the behaviour retires it." | the holding list shows each held scenario and what will retire it (outline) |
| r22 | "**When** `features holding` is run and no scenario is held, `features` says none is held." | the holding list says when nothing is held |
| r23 | "**When** `features retire <title>` is run on a scenario tagged `@holding`, `features` removes that scenario's block and leaves the rest of the file as it was." | retiring a held scenario removes its block |
| r24 | "**If** `features retire` is given a scenario not tagged `@holding`, `features` refuses because it is not held, and leaves the file as it was." | retiring a scenario that is not held is refused |
| r25 | "**When** `features bindings` finds a `scenario(<feature>, \"<title>\")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, `features` reports the module, line, title and feature of each, and exits 1." | a binding that names no scenario is reported (outline) |
| r26 | "**When** `features bindings` finds every binding names a scenario, `features` says so and exits 0." | bindings that all name a scenario pass |
| r27 | "**If** a test module under `--tests` does not parse, `features bindings` and `features rebind` refuse, naming the module." | a test module that does not parse is refused (one reason, representative call bindings) |
| r28 | "**When** `features rebind <old> <new>` is run, `features` rewrites `<old>` to `<new>` in each binding call that names it, changes nothing else in the module, and prints how many bindings it rebound, zero included." | rebinding rewrites each binding of the old title and counts them (outline) |
| r29 | "**If** `features rebind` is given a new title that is no scenario in a feature file, `features` refuses and changes no test module." | rebinding to a title no scenario has is refused |
| r30 | "**When** `features plugin <directory>` is run, `features` writes `slice_expectations.py` into the directory and prints the line that registers it in the `conftest.py` beside it." | the plugin is written into the directory with its registration line |
| r31 | "**Where** `slice_expectations.py` is registered and one living plan is found, a test tagged to a slice the plan has as planned or blocked is expected to fail: its failure is reported as expected, its pass fails the run, and the run reports how many tests of which slices were expected to fail." | a test of a planned or blocked slice is expected to fail (outline) |
| r32 | "**Where** `slice_expectations.py` is registered, a test tagged to a slice that is in progress, green or no longer in the plan runs as it is." | a test of a slice under way, done or gone from the plan runs as it is (outline) |
| r33 | "**Where** `--slice <n>` is given to pytest, `slice_expectations.py` runs that slice's tests as they are." | naming a slice runs its tests as they are |
| r34 | "**Where** no one living plan is found, `slice_expectations.py` expects no test to fail and the run says so." | with no one living plan no test is expected to fail (outline) |
| r35 | "**If** `features move`, `features hold` or `features retire` is given a title no file holds, or one several files hold, `features` refuses, naming every file that holds it, and changes no file." | moving a title no file holds is refused; moving a title several files hold is refused (one scenario per reason, representative call move) |
| r36 | "**If** the destination of `features move` is the scenario's own file, `features` refuses and changes no file." | moving a scenario to its own file is refused |
| r37 | "**If** a title is in the `--from` tree and not the other, or in the other tree and not `--from`, `features verify-moved` names it as missing or as added, and exits 1." | a title in only one tree is missing or added (outline) |
| r38 | "`features list --tag` finds the tag whether it is given with its leading `@` or without." | a tag is found with or without its leading @ (outline) |
| r39 | "**When** `features hold` has held a scenario, `features` prints its file and its new title." | holding a scenario prints its file and new title |
| r40 | "**When** `features holding` finds a held scenario with no `Held for:` line, or whose replacement carries no slice tag, `features` says so on that scenario's line." | the holding list flags a held scenario it cannot place (outline) |
| r41 | "**If** `features rebind` is given a new title that several feature files hold, `features` refuses and changes no test module." | rebinding to a title several feature files hold is refused |
| r42 | "**If** a binding call names the old title of `features rebind` in a string written over several lines, `features` refuses, naming the module and line, and changes no test module." | rebinding a title written over several lines is refused |
| r43 | "**If** `features plugin` is given a path that is not a directory, `features` refuses and writes nothing." | writing the plugin to a path that is not a directory is refused |
| r44 | "**When** `features plugin` is run, `features` writes over any `slice_expectations.py` already in the directory, and reads no feature file." | writing the plugin replaces an existing one and reads no feature file |
| r45 | "**Where** the directory given to `features plugin` holds an `__init__.py`, the line `features plugin` prints imports `slice_expectations` relative to the package." | the registration line for a package imports relatively |
| r46 | "**If** `features` refuses a command or an edit, it says why on stderr and exits 1." | a refusal says why on stderr and fails (representative call retire) |
| r47 | "`slice_expectations.py` reads as the living plan the file the ini value `slice_plan` names under pytest's root directory, or else the one `docs/superpowers/plans/*-slices.md` under it, and finds none when there are none or several." | the living plan is the one slice_plan names, or else the one plan file (outline) |
| r48 | "**Where** `--slice` is given to pytest more than once, `slice_expectations.py` runs the tests of every slice named, each written `<n>` or `slice-<n>`, as they are." | naming several slices runs each one's tests as they are |
| r49 | "**Where** `slice_expectations.py` is registered, the run's header names the living plan it read, relative to the root directory, or says no one living plan was found." | the run's header names the living plan or says there is none (outline) |
| r50 | "**If** the ini value `slice_plan` names a file that does not exist, `slice_expectations.py` expects no test to fail, and the run's header names that file." | a slice_plan naming a missing file expects nothing to fail |
| r51 | "**When** `features tag <title> r<n>` is run on a title exactly one file holds, `features` makes `@r<n>` the scenario's one requirement tag, removing any other `@r<m>` tag it has, and leaves its other tags and every other line unchanged." | tagging with a requirement id makes it the scenario's one requirement tag |

## Questions

- r3: "**If** an edit would leave its file invalid, `features` refuses the edit and leaves the file as it was."
  - Reading 1: invalid means Gherkin a Gherkin parser would reject (for example a scenario with no steps, or a step before any Scenario:).
  - Reading 2: invalid means a file `features` itself would refuse or misread (for example one holding a `Rule:` block, an unclosed docstring, or two scenarios with one title).
  - (Under either reading the line names no edit that could produce such a file, so a scenario needs one named.)
- r4: "**When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and the total, ..."
  - Reading 1: "the total" is the number of all scenarios in the files, untagged ones included.
  - Reading 2: "the total" is the number of scenarios carrying at least one tag (or the sum of the per-tag counts, which differs when a scenario carries several tags).
- r14: "**Where** `--carry-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line above the moved scenario."
  - Reading 1: the carried tags go on a new tag line of their own above the moved scenario, whatever tag lines it already has.
  - Reading 2: the carried tags join the moved scenario's existing (last) tag line, and stand on a new line only when it has none.

## Cases no line mentions

- `features list --tag` on a Scenario Outline with several Examples rows: listed once, or once per row (r4 counts per row; r5 says "each scenario").
- `features list --title`: whether the text match is case-sensitive.
- `features tag <title> r<n>` on a scenario with no requirement tag: where the new `@r<n>` goes (r9 covers only slice tags).
- `features tag` with a requirement tag on a scenario whose tag line also holds slice tags: whether slice tags are touched (r51 says other tags unchanged; no case with zero `@r` tags).
- `features move --carry-feature-tags` when the destination already has every source feature tag: whether an empty tag line is written.
- `features move --inline-background` when the source has no Background, or the destination has its own Background.
- `features hold` given both `--for` and `--for-removal`, or neither.
- `features hold --for <title>` where the new title is the scenario's own title.
- `features rebind` where the old and new titles are equal, or the old title is bound under a feature other than the one holding the new title.
- `features verify-moved` when `--from` does not exist, or is the same tree as `--dir`.
- `features plugin` when the directory has no `conftest.py`, or its `conftest.py` already registers the plugin.
- `features plugin` given a path that does not exist (r43 says "not a directory"; whether a missing path is refused or created).
- `features` run with a `--dir` that does not exist, or holds no feature file.
- An unclosed docstring in a feature file.
- `slice_expectations.py`: a test tagged to two slices with different standings in the plan, a test with no slice tag, and a slice the plan lists with a status word other than planned, blocked, in progress or green.
- `--slice` naming a slice the plan does not have, or a value written neither `<n>` nor `slice-<n>`.
- `slice_plan` given as an absolute path, or one outside pytest's root directory.
- `slice_expectations.py` reporting expected failures when one living plan is found but no test is tagged to a waiting slice (whether the count of zero is reported).
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/slice-plan-tool.reply.md`

~~~~~~
## Coverage

| id | line | scenario |
|---|---|---|
| r1 | "If the plan is not valid — its title, slice order, section order, a slice's Kind, Status, Scenarios or Check lines — `plan` refuses every command, naming every problem, and leaves the file as it was." | an invalid plan refuses every command and names every problem |
| r2 | "If an edit would make the plan invalid, `plan` refuses it, naming every problem, and leaves the file as it was." | an edit that would break the plan is refused with every problem named |
| r3 | "When `plan check` is run on a valid plan, `plan` says it is ok and exits 0." | checking a valid plan says ok |
| r4 | "A section `plan` does not know is kept byte for byte through every edit." | a section plan does not know survives an edit untouched |
| r5 | "When `plan log <text>` or `plan backlog <text>` is run, `plan` appends `- <date> <text>` to the Log or Backlog section, the date being `--date` or today." | log and backlog entries are appended with a date (outline) |
| r6 | "Where the Backlog or Log section is missing, when a command needs it, `plan` creates it in its place in the section order." | a missing Log or Backlog section is created where it belongs (outline) |
| r7 | "When `plan status <n> <status>` is run, `plan` sets slice `<n>`'s Status and changes nothing else." | setting a slice's status changes only that status |
| r8 | "If `plan status` is given a status that is not planned, in progress or green with an optional note, or `blocked: <why>`, `plan` refuses and leaves the file as it was." | none: returned as a question |
| r9 | "If `plan status` names a slice the plan does not have, `plan` refuses." | setting the status of a slice the plan does not have is refused |
| r10 | "When `plan add-slice <n> <name>` is run, `plan` writes the slice in number order, dotted numbers sorting numerically, with Status planned." | none: returned as a question |
| r11 | "If `plan add-slice` gives a slice the wrong one of Scenarios and Check for its Kind, or a number the plan already has, `plan` refuses and leaves the file as it was." | adding a slice that does not fit is refused (outline) |
| r12 | "Where `plan add-slice` is given no `--lands`, `plan` writes the slice and says on stderr that it has no Lands line and how to set it; with `--lands` it writes the line and says nothing." | adding a slice with or without a Lands line (outline) |
| r13 | "If a slice's Lands line counts more than 8 production or 4 test modules, `plan` refuses, naming the slice, its Lands and the budget, whatever the command, and leaves the file as it was." | a slice over the module budget is refused whatever the command (outline) |
| r14 | "If a slice has more than one Lands line, or a Lands line written any other way than `- Lands: <p> production, <t> test`, `plan` refuses, naming the slice." | a slice with a badly written or repeated Lands line is refused (outline) |
| r15 | "A slice without a Lands line is valid." | a slice without a Lands line is valid |
| r16 | "When `plan lands <n> \"<p> production, <t> test\"` is run, `plan` sets slice `<n>`'s Lands line, replacing any it had." | setting a slice's Lands line replaces any it had (outline) |
| r17 | "When `plan show --open` is run, `plan` prints each slice that is not green with its name and status." | showing open slices lists every slice that is not green |
| r18 | "When `plan show --requests` is run, `plan` prints the Log's REQUEST entries." | showing requests lists the Log's REQUEST entries |
| r19 | "When `plan show --last-suite` is run, `plan` prints the Log's last `Suite:` entry." | showing the last suite record gives the Log's last Suite entry |
| r20 | "Where `--current` is given with `--last-suite`, `plan show` prints the record, then `current` and exits 0 when no path outside `docs/superpowers/plans/` has changed since the commit it names, or `stale:` with the reason and exits 1." | the current flag says whether the last suite record still holds (outline) |
| r21 | "If the suite record names a commit the repository does not have, `plan show --last-suite --current` says it is stale because of that commit and exits 1." | a suite record naming an unknown commit is stale |
| r22 | "If `--current` is given without `--last-suite`, `plan` exits 2 as bad usage." | the current flag without last-suite is bad usage |
| r23 | "When `plan archive <batch>` is run, `plan` writes the green slices and the whole Log to `archive/<plan name>-<batch>.md` beside the plan and removes those slices from the plan." | none: returned as a question |
| r24 | "When `plan archive` is run, `plan` leaves the Log holding the REQUEST, RE-FORMULATE and QUESTION FOR THE SPEC: entries with their continuation lines, one line naming the archive and the last `Suite:` entry, and that `Suite:` entry again, so `plan show --last-suite --current` still finds it." | archiving leaves the Log holding what is still owed and the suite record |
| r25 | "If the archive file exists or no slice is green, `plan archive` refuses." | archiving is refused when the archive exists or nothing is green (outline) |
| r26 | "`plan` works on the plan `--file` names, or else on the one `docs/superpowers/plans/*-slices.md` under the current directory." | plan works on the named file or the one plan in the current directory (outline) |
| r27 | "If no `--file` is given and the current directory holds no `docs/superpowers/plans/*-slices.md` or several, `plan` refuses every command, saying how many it found and to name the plan with `--file`." | without --file, no plan or several plans is refused (outline) |
| r28 | "If the plan file cannot be read, `plan` refuses, naming the file." | a plan file that cannot be read is refused |
| r29 | "When `plan show --backlog` is run, `plan` prints each Backlog entry with its continuation lines, and nothing when the Backlog is empty or missing." | showing the backlog prints each entry with its continuation lines (outline) |
| r30 | "When `plan show --requests` or `plan show --last-suite` without `--current` is run, `plan` prints each entry with its continuation lines." | showing requests or the last suite record keeps continuation lines (outline) |
| r31 | "If the Log has no `Suite:` entry, `plan show --last-suite` prints nothing and exits 0, and with `--current` `plan` refuses because there is no suite record." | a Log with no suite record (outline) |
| r32 | "If the suite record names no commit, `plan show --last-suite --current` says it is stale because the record names no commit, and exits 1." | a suite record naming no commit is stale |
| r33 | "When `plan show --last-suite --current` finds files changed, committed or not, outside `docs/superpowers/plans/` since the record's commit, the stale reason gives how many and names each." | the stale reason counts and names every changed file |
| r34 | "If `plan lands` names a slice the plan does not have, `plan` refuses and leaves the file as it was." | setting the Lands line of a slice the plan does not have is refused |
| r35 | "`plan` takes a slice as green, for `show --open` and `archive`, by the word before its Status's colon, so a Status of `green: <note>` is green." | a green status with a note counts as green (outline) |
| r36 | "When `plan archive` is run, `plan` creates the `archive/` directory beside the plan when it is missing, and the archive file begins with the plan's title." | archiving creates the archive directory and starts the file with the plan's title |
| r37 | "Where `--date` is given to `plan archive`, the Log's line naming the archive carries that date, and otherwise today's." | the Log's archive line carries the given date or today's (outline) |
| r38 | "If `plan` refuses a command or an edit, it says why on stderr and exits 1." | a refused command says why on stderr and exits 1 |

## Questions

- r8: "If `plan status` is given a status that is not planned, in progress or green with an optional note, or `blocked: <why>`, `plan` refuses and leaves the file as it was."
  - Reading A: only green may carry a note, so `planned: <note>` and `in progress: <note>` are refused.
  - Reading B: the optional note goes with any of planned, in progress and green, so `planned: <note>` is accepted.
- r10: "When `plan add-slice <n> <name>` is run, `plan` writes the slice in number order, dotted numbers sorting numerically, with Status planned."
  - Reading A: each part of a dotted number is compared as a whole number, so 2.10 comes after 2.9.
  - Reading B: a dotted number is compared as a decimal number, so 2.10 (that is, 2.1) comes before 2.9.
- r23: "When `plan archive <batch>` is run, `plan` writes the green slices and the whole Log to `archive/<plan name>-<batch>.md` beside the plan and removes those slices from the plan."
  - Reading A: `<plan name>` is the plan's file name without `.md`, so `2026-10-01-cart-slices.md` archives to `archive/2026-10-01-cart-slices-<batch>.md`.
  - Reading B: `<plan name>` is the file name without its `-slices.md` ending, so it archives to `archive/2026-10-01-cart-<batch>.md`.

## Cases no line mentions

- r22 says bad usage exits 2, and r38 says every refusal exits 1. No line says whether bad usage counts as a refusal under r38, or whether bad usage writes to stderr.
- `plan archive` when the Log has no `Suite:` entry: no line says what the line naming the archive and the last `Suite:` entry holds then.
- `plan archive` when the plan has no Log section: no line says whether the archive gets an empty Log or whether a Log is created.
- `plan show` with no option, or with several of `--open`, `--requests`, `--backlog` and `--last-suite` together.
- An unknown command, or a known command with a missing argument (for example `plan status 2` with no status).
- A `--date` value that is not a date.
- A slice number that is not a number, given to `add-slice`, `status` or `lands`.
- `plan lands` given an argument not in the form `<p> production, <t> test`. r2 or r14 might cover it, but no line says.
- `plan lands` with counts over the budget: r13 covers it as a refusal, but no line says whether the refusal is made before anything is written.
- `plan show --last-suite --current` run outside a git repository.
- `plan show --open` when every slice is green: whether it prints nothing and exits 0.
- `plan log` or `plan backlog` text that spans several lines: whether it becomes continuation lines.
- Where `plan archive` leaves the slices that are not green, and in what order.
- r6 names no command that "needs" the section beyond `log` and `backlog`. Whether `archive` creates a missing Log is not stated.
- What a REQUEST entry looks like in the Log (a prefix, a word anywhere in the entry) is not stated in Behaviour.

## Drafts

- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/slice-plan-tool.feature
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/slice-plan-tool.reply.md
~~~~~~
