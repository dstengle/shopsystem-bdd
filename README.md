# shopsystem-bdd
Claude Code plugin for the shopsystem harness: a behaviour-driven workflow
that replaces test-driven development with a single spec of capability
files, Gherkin feature files paired with them as the contract, thin vertical
slicing, and one human gate on the spec's Behaviour lines.

Skills: `integrating-a-proposal`, `formulating-features`,
`slicing-into-increments`, `bdd-red-green`, `migrating-to-capabilities`,
`analyzing-a-batch`, `checking-spec-consistency`.
Agents: `capability-writer`, `feature-formulator`, `initiative-round`, `code-scout`,
`bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`,
`architecture-reviewer`, `spec-checker`.
Format: `docs/capability-format.md`.
Spec: `spec/index.md` and `spec/capabilities/`, with decisions under `decisions/`
(index: `spec/decisions.md`), work under `work/`, and history and evidence under
`records/` — the layout of the design model in `docs/design-model/` (version 3).
Check it with `python3 scripts/model check`.
Earlier design notes: `records/archive/design-notes/`. Test logs:
`records/measurements/fixture-runs/`.

## Requires

The [superpowers](https://github.com/obra/superpowers) plugin, 6.4.0 or
later, declared as the dependency `superpowers@claude-plugins-official` in
`.claude-plugin/plugin.json` (the marketplace suffix is required: a bare name
is resolved against this plugin's own marketplace and reported missing, and
the object form of a dependency rejects a suffixed name, so it is a string). Claude Code
refuses to load this plugin when superpowers is not installed (a
`dependency-unsatisfied` load error). As of Claude Code on 2026-09-22 version
constraints on dependencies are not enforced, so the minimum version here is
documentation. The skills assume the rest of
the superpowers pipeline around them:

- `superpowers:brainstorming` produces an approved note, a proposal that
  `integrating-a-proposal` merges into `spec/`; `formulating-features` reads
  `spec/`, never the note.
- `slicing-into-increments` invokes `superpowers:writing-plans` to turn
  slices into tasks.
- `superpowers:executing-plans` or `superpowers:subagent-driven-development`
  runs those tasks, with `bdd-red-green` firing where they would otherwise
  fire `superpowers:test-driven-development`. formulating-features, slicing and bdd-red-green state that
  they supersede test-driven-development when both apply.

## Models

The `feature-formulator` agent pins `model: opus`, so formulation runs on
Opus whatever the session runs on; verified by the subagent turns in a
Sonnet session. A skill's own turns run on the session's model: a `model:`
field in SKILL.md did not change a session's model when the skill was
invoked by the model rather than by a slash command, so the skills carry
none. Launch a headless formulation, slicing, or planning session with
`--model opus` and an execution session with `--model sonnet`;
subagent-driven-development puts implementers on Sonnet and reviewers on
Opus by its own rules, and `bdd-red-green` pins nothing.

## Install

```
claude plugin marketplace add dstengle/shopsystem-bdd
claude plugin install shopsystem-bdd@shopsystem-bdd
```

While developing, `claude --plugin-dir <path to this checkout>` loads the
working copy instead.

## Sized to the change (0.9.0)

0.9.0 makes the workflow's cost follow the size and risk of a change. Measured on shopsystem-kb, about half of a batch's agent time went to running the full pipeline around one-line changes, re-reviewing small tasks, and a two-minute suite run many times a slice.

- **A small-change path.** At most two Behaviour lines in existing capabilities, no contract change, nothing unknown: the controller writes the lines and their scenarios itself, from the spec alone. The gate on the lines stays. Anything larger takes the full path (`integrating-a-proposal`, `formulating-features`).
- **Review by risk.** Each planned task carries `Review:` and `Model:` lines. Concurrency, the published contract, data integrity and moving stored data get a per-task review on Opus; everything else, refactors and small slices included, is reviewed once at the batch's end and implemented on Sonnet (`slicing-into-increments`).
- **Findings triaged.** Correctness and data loss are fixed now; hardening goes to the plan's backlog with its reproduction, and is cut only when the person asks or it bites; polish is fixed when cheap (`slicing-into-increments`, both reviewers).
- **A line every call must keep is one scenario per reason,** with one representative call; a table-driven test checks every call goes through the boundary (`formulating-features`).
- **The architecture review folds into the branch review,** which now checks shape against `CLAUDE.md` and coupling every batch. `architecture-reviewer` runs only on request.
- **A short living plan.** A batch's green slices and log move to `docs/superpowers/plans/archive/` when its branch review is done.
- **A fast suite.** `bdd-red-green` runs the slice's marker during red-green and the whole suite once per slice, and asks for a parallel suite (`pytest-xdist`) that drives commands in-process.

## Fewer runs, fewer round trips (0.10.0)

0.10.0 removes the repeated work a 0.9.0 session showed: a suite run about 34 times at 100-206 s each, a dependency read instead of probed, splits and defects bounced between agents, and a controller context of half a million tokens.

- **The suite fast first.** Slicing records the suite's wall time in its `Suite:` log line and checks whether it runs in parallel and drives commands in-process. A suite over 60 s that fails either property, with no reason in `CLAUDE.md`, gets an enabling slice cut first in the batch (`slicing-into-increments`). The branch reviewer reports the wall time beside its summary.
- **A suite record per commit.** `Suite: <N> passed, <M> failed at <hash> in <seconds> s` holds while nothing outside `docs/superpowers/plans/` differs between its commit, `HEAD` and the working tree. Whoever finds a record that holds uses it instead of running again. The implementer drops the run at the start and runs the whole suite once, before the slice's last commit; the branch reviewer runs it once at the batch's head. Plans carry no run protocol (`bdd-red-green`, `bdd-implementer`, both reviewers).
- **Probes at the pin.** A slice whose Needs names something a dependency provides carries a probe, a command run against the installed version, with its result in the plan's log. A failing probe marks the slice `blocked: awaiting <dependency>` and logs the request. Reading the dependency's spec is not a probe, and a capability file is read whole, never by range (`slicing-into-increments`).
- **Rule-decided splits and behaviour defects.** When a module would cross a size limit and the repository's rules say where the code goes, the implementer splits it and records that in the checkpoint; it hands back only when no rule decides. Behaviour that contradicts a Behaviour line or a capability's Purpose is Important, covered by a scenario or not, never Minor (`bdd-implementer`, both reviewers).
- **Drafts to files, and a fresh session.** `capability-writer` and `feature-formulator` write drafts under `.superpowers/spec-drafts/<run>/round-<n>/`, one directory per dispatch, applied in order, and reply with the change list and paths. The controller checks every file written is under that path before the gate. Slicing recommends executing the plan in a new session that reads the plan file, not the one that integrated, formulated and sliced.

## Small slices, steps and fresh agents (0.11.0)

0.11.0 measures a slice's size before the work and holds it during the work. On shopsystem-kb one slice passed every test of slicing and then ran as one implementer over 72 files and 426k tokens; its review had to be split, and it removed the tests that covered a regression two of the plan's decisions caused together. Design: `records/archive/design-notes/2026-10-10-small-slices-and-steps-design.md`.

- **Small, a fourth test.** A slice lands in at most 8 production and 4 test modules, counting the migration it forces. Each slice carries `Lands: <p> production, <t> test`. For a slice that changes a form existing code depends on, the count is a probe, logged; `plan` refuses a slice over the budget (`slicing-into-increments`).
- **Expand, migrate, contract.** A breaking change is cut as the new form beside the old, callers moved a group to a slice behind a test seam, the capability slices, then the old form removed, each with the suite and a search for its check (`slicing-into-increments`).
- **A scout reads; the planner plans.** `code-scout`, on Haiku, runs the Lands probe and each task's research and writes notes to `.superpowers/scout/`. The planning session reads the notes, not the source.
- **Tests the decisions break.** Each task lists the existing tests its decisions make impossible to keep and what the plan decides for each. An implementer may change what a test asserts only when it is listed; any other test it would have to remove, loosen, skip or rewrite is a stop, `BLOCKED` with the test named (`bdd-implementer`, `bdd-red-green`). Both reviewers list every removed or weakened test, and one no task lists is Important.
- **Steps.** (0.13.0: only where an order must be seen.) A task over about 5 files is written as ordered Steps, each with its own check and files, each run by a fresh implementer from the task's one report file. A step ends with the whole suite run once. One dispatch touches at most 15 files: before any edit an implementer writes a `Dispatch budget` at the head of its report, naming the files it will touch and the files it leaves, and when files are left it stops at a green commit and replies `PARTIAL`; a fresh implementer continues from the report (0.11.1: the written budget held in 13 of 14 runs, where a rule to count and stop held in one of five).
- **Fresh agents, a thin controller.** Review findings go to a file and then to a fresh implementer; no agent is resumed. The controller passes paths and reads short replies, not diffs, reports or source. A large diff is reviewed by area, in parallel.
- **Lanes.** Tasks the planner marks `Lane:` (disjoint files, neither needing the other) may run at once, each lane in its own worktree, branch and virtualenv. The controller merges one at a time, runs the suite after each merge and writes the plan's checkpoints itself, from each lane's reply.

These rules reach a controller through the plan: the hand-off has writing-plans copy them into the plan's Global Constraints.

## Measuring a batch (0.12.0)

0.12.0 changes no rule. It makes a batch measurable, so that a change to the workflow is tried on a real batch and kept or dropped by what the numbers show. Design: `records/archive/design-notes/2026-10-11-measuring-a-batch-design.md`.

- **`scripts/measure batch <archive file>`** reads the session transcripts Claude Code keeps for the repository and its worktrees, the archive `plan archive` wrote, the batch plan and git, and writes one facts file under `docs/superpowers/measurements/`. No agent runs. For every dispatch: role, model, slice, kind, time, requests, tokens (output, new input, cache read), the context it started with and its peak, how it closed, and the files its commits touched. For the batch: tasks planned against tasks run, hand-backs, reviews that came back clean, `Lands:` against files touched, and the share of time spent closing. The controller session is a role of its own.
- **`measure show`** prints a facts file as tables; **`measure compare <a> <b>`** sets two batches side by side.
- **The controller measures at the close.** The plan's execution rules have it run `measure batch` after `plan archive` and commit the facts, and have every dispatch's description start `slice <n>: <kind>` or `batch <name>: `, so each agent's cost is attributed.
- **`analyzing-a-batch`** turns the facts into a report, in the repository that ran the batch: the tables, a comparison with an earlier batch, a judgement of each hand-back's cause and of where each defect was found against where it could have been, and candidates to try. Every number is the script's; the report words no rule. It is brought to this repository as a request.
- **An experiment is a release.** One change to the workflow per version; a batch run on it; `measure compare` against the batch before. The facts record the plugin version they ran on.

The transcripts are Claude Code's own files and not a published format: `measure` refuses a shape it does not know instead of guessing. On shopsystem-kb's batches 32 to 35 it reproduced the figures a session had summed by hand, and showed two it could not: the controller's cache reads (26M to 31M tokens a batch, more than the implementers' in batch 33) and the context each dispatch starts with (29k for an implementer, 15k for a reviewer or a scout).

## Rules adjusted (0.13.0)

0.13.0 adjusts the rules of 0.11.0 that the kb baseline shows costing more than they return. Each change names the number in a batch's facts that should move. Design: `records/archive/design-notes/2026-10-11-rules-adjusted-design.md`.

- **Two allowances for unlisted tests.** An implementer may change a test's setup, with no assertion, expected value or parametrize case touched, and may rewrite a test this batch wrote (first committed after the task's `Batch base:`) that pinned an interim state. It lists each in its report, and both reviewers check each row against the diff. Changing what any other test asserts is still `BLOCKED` (`bdd-implementer`, `bdd-red-green`, both reviewers). Watch: hand-backs a batch.
- **Steps where an order must be seen.** A task has Steps only when a contract field, a stored layout, a port or a seam must be green alone first. Otherwise it is one dispatch, whatever its file count (`slicing-into-increments`). Watch: dispatches per slice.
- **The implementer has no Skill tool.** `bdd-red-green` reaches it through its `skills` field; the tool only brought the listing of every installed skill into each dispatch. Watch: the implementers' mean starting context.
- **Steps-only slices.** The scout marks each scenario `steps only` or `behaviour`; a task that is all steps runs on Sonnet with a batch-end review. Sizes are probed one batch ahead, not for the whole release. Lanes are marked where file lists are disjoint, never planned for.
- **The controller** writes one line a slice and stops at a batch's close, so the next batch starts in a new session. Watch: the controller's cache read and peak context.

Held, each with the measurement that would decide it: resuming an implementer in place of a fresh one, narrower triggers for `Review: per-task`, a budget by kind of change, and one research scout a batch.

## A green suite (0.14.0)

0.14.0 keeps the suite passing between slices, and keeps behaviour tested until a slice changes it. Design: `records/archive/design-notes/2026-10-11-green-suite-design.md`.

- **A scenario that passes today is held, not removed.** When a line is re-worded or removed, formulation keeps the old scenario in the feature file, tagged `@holding` with " (held)" on its title, its steps unchanged, so it still passes. Slicing gives it a slice that retires it, the task lists it under `Retires:`, and the implementer removes it with `features retire` in the commit that turns its replacement green (`formulating-features`, `slicing-into-increments`, `bdd-red-green`).
- **A changed title never stops a module collecting.** `features bindings` reports every `scenario(…, "<title>")` call that names no scenario; `features rebind` rewrites the title in those calls. Formulation runs both before it commits.

## Analysis tools, a consequence sweep and invariants (0.15.0)

0.15.0 gives the workflow tools in place of text search and hand probes. Design: `records/archive/design-notes/2026-10-11-analysis-tools-design.md`.

- **`scripts/tools`.** `probe` looks for the project's analysis tools in its own virtualenv (for Python: coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter, hypothesis); `install` installs what is missing there and edits no dependency file; anything still missing is told to the person in plain words, with what the workflow does without it, and logged in the plan. `map` runs the suite once under coverage with a context per test; `tests-of <file>:<function>` and `untested` answer from it; `refs <name>` gives exact references; `check` runs the lint, dead-code and import-contract tools for the reviewers.
- **The scout uses them before it searches,** and its notes say of each count whether it came from `refs`, `tests-of` or a search. "Tests the decisions break" starts from the tests that execute the changed code, where that is a list short enough to read; on kb, code on every call's path is executed by two thirds of the suite, and there the scout says so and searches.
- **A consequence sweep.** Before a batch's slices are final, each decision that replaces something the code assumes is traced by a scout: every place that still embodies the old assumption, with the tests that execute it. Slicing gives every row a slice, a question for the spec, or a deferral logged with its price.
- **A guard names its test.** A task says "a test that breaks is a stop" only by naming the passing test that executes the behaviour; where none does, the task writes it first.
- **Invariants.** A project lists under `## Invariants` in its `CLAUDE.md` what must hold after any change, each with its test; slicing cuts the missing ones as an early enabling slice. A reviewer's probe that finds a defect is handed on as a test to keep, and one that checks such a property is proposed as an invariant.

## Research that runs the system (0.16.0)

0.16.0 has the plan written from what the system does today, found by running it. Design: `records/archive/design-notes/2026-10-11-research-probes-design.md`.

- **The scout probes.** Task research drives the system through its real entry point, in a scratch directory and never on the checkout's data: the Givens and Whens of the slice's scenarios against today's code, and the nearest cases they do not state. Each probe is recorded with its command and what came back, marked `run`; what was only concluded from the code is marked `read`. A defect a probe finds is reported and triaged like a review's finding.
- **A path that leaves a stage out.** When a slice adds a way through the system that skips a stage, the research lists every refusal and effect that stage alone produces, and the task's decisions say what the new path does about each.
- **Sizes and zeros.** The research gives the line count and room of every module on the change's path. `Lands: 0 production` stands only on a probe that was run. One scout a task, never one a batch.
- **A dry run agrees with the real run.** Where a system has both for one operation, the batch keeps one randomized test that they give the same answer, and the branch reviewer runs it.
- **Fix rounds end.** After the fix wave's re-review, another round is run only for data left invalid, the system's own fault on input, or a write that lands where a refusal belongs. Everything else is a backlog line.

## Effort where the work is searching (0.17.0)

About a third of what the agents write is reasoning: on shopsystem-kb, 29% of the implementers' output tokens, 39% and 44% of the reviewers', and 64% of the scouts'. Every agent ran at medium effort.

- **The scout runs at low effort** (`effort: low` in `agents/code-scout.md`). On the same model and fixtures its output fell by about a third and its time with it, with the same parts in its notes and the same places found on kb.
- **`measure` records effort and reasoning.** Each dispatch has the effort it ran at and its reasoning tokens, which are part of its output tokens; `measure show` gives both by role.

Not changed: the implementer and the reviewers. A steps-only task on Sonnet reasons for a few hundred tokens at any setting, and a reviewer's reasoning is what finds defects.

## A controller for each spec round (0.18.0)

In shopsystem-knowledge's batch 19 the session that integrated and formulated a note read 30M tokens from cache, eleven times what its writers and formulators read together. It held the brainstorm (181k of context before integration began), and every writer and formulator that finished cost it another turn at that size: 53 turns for three formulation rounds.

- **`spec-round`** (since renamed `initiative-round`), a new agent, runs one round and ends with it: an integration round (it dispatches the `capability-writer` and checks the change list), the applying of approved drafts, or a formulation round (it dispatches the `feature-formulator`s, checks coverage, holds, splices and commits). It waits for its agents by a reply file each writes last.
- **The session the person talks to keeps the gate and nothing else.** `integrating-a-proposal` and `formulating-features` each begin with who does what: that session dispatches a fresh `initiative-round` for each round, shows the person the lines and questions that come back, and passes their answers to the next round. It opens no draft and dispatches no writer.
- **A new session for a note that was brainstormed here** is recommended before integration starts.
- **`measure`** attributes a dispatch whose description starts `spec` and gives the three spec agents the kind `spec`, so the 22 unattributed dispatches of batch 19 would have been counted.

With a controller holding 270k: formulating six capabilities read 1.8M tokens from cache in all against 5.4M, and integrating a note 0.8M against 1.6M. The round costs about 6k more output tokens each time, and in a session that holds little it saves nothing.

## Requirement ids (0.19.0)

Every Behaviour line carries a stable id, `[r<n>]`, and every scenario names its line by the tag `@r<n>`
(design model v3). A new line takes the next free id, a changed line keeps its id, a removed line's id is
retired in the capability's frontmatter and never reused. The gate shows ids and the spec commit names them.
Ids are type-first, following shopsystem-knowledge's IRIs: `<kind>/<owner>/<product>/<context>/<name>`, with the design
model's kind names (`capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration`). Inside a context the short forms
`<kind>/<name>` and, where the field fixes the kind, `<name>` are read. Adding Ids also rewrites `decision/` to `design-decision/`.
`scripts/model check` checks ids and coverage where clingo is installed. A repository already on capability
files is migrated with migrating-to-capabilities' "Adding ids". The release's fixture runs (15 B, 4 A) are recorded in the test log:
`records/measurements/fixture-runs/2026-10-16-requirement-ids-test-log.md`.

## A ubiquitous language (0.20.0)

A context's words are now checked, not only its lines. The glossary entries in `spec/index.md` are terms (`term/<name>`), each with the words it avoids (`Not:`), and `scripts/model check` reports a line or scenario that uses an avoided word (`v_t1`), a term with two entries (`v_t2`) and a term that avoids a term of its own glossary (`v_t3`).

- **`checking-spec-consistency`** and the **`spec-checker`** agent judge a spec against itself, blind to the code: one capability's lines against its scenarios, and every line against the glossary. Report mode writes findings and changes nothing; fix mode takes the person's answers, changes the spec and its scenarios, and commits each with the ids and terms it names. The integration and formulation skills teach the glossary terms.
- **`model` finds clingo behind a virtualenv**: run from a virtualenv without clingo, `check` tries the other `python3` interpreters on the PATH (and `SHOPSYSTEM_MODEL_PYTHON`), and says what it tried when none holds clingo.
- **`features` takes `--file`**: `tag`, `hold`, `retire`, `move` and `rebind` can be limited to one feature file, so a title that appears in two files is no longer tagged by hand.

An existing `## Glossary` whose bullets are in another form gives a file problem per bullet: rewrite them to the form (this repository's own already fit).

Fixture runs on a seeded shelf spec (a planted `volume` for `book`, a scenario answering with titles where its line says the number, a line with no bound): report mode 3/3 and fix mode 3/3, $0.29 a report run and $0.42 to $0.54 a fix run. A report-mode run on a clone of shopsystem-kb found 77 findings for $3.28, among them the trial's three known issues. The runs, the scorer fix and what is not tested are in `records/measurements/fixture-runs/2026-10-17-ubiquitous-language-test-log.md`.

## Scripts

Python 3, in `scripts/`. They take the dependencies they need (design-decision/plugin-takes-the-dependencies-it-needs): clingo for `model check` (`python3 -m pip install clingo`), and pytest and pytest-bdd for the scenarios as they move to pytest-bdd step definitions (initiative i11). `--help` is the contract; tests: `python3 -m pytest`.

- `scripts/features`: count, list, tag, move and verify-moved for feature files, without the test runner; hold, retire and holding for scenarios kept while they still pass; bindings and rebind for the titles test modules bind.
- `scripts/measure`: write, show and compare a batch's facts, from the session transcripts, the plan and git.
- `scripts/tools`: probe and install the project's analysis tools, and use them through one interface: `map`, `tests-of`, `untested`, `refs`, `check`.
- `scripts/model`: read a bounded context's spec, feature files, decisions, work and records as the facts of the design model's grammar (`facts`), check them against `scripts/model.lp` with clingo (`check`), write the decisions index (`decisions`), and trace a requirement to why it exists (`why`). Only `check` needs a package: `python3 -m pip install clingo`.
- `scripts/plan`: edit and read the living slice plan (log, status, slices, backlog, archive, `show`), keeping its sections and order valid and refusing a slice whose `Lands:` is over the budget (`plan lands` sets it).

## One spec per context; the gate is on Behaviour lines

From 0.8.0 a bounded context has one spec: `spec/index.md`, the decision ledger `spec/decisions.md`, and `spec/capabilities/<name>.md`, each capability formulated as `features/<name>.feature`. The format is `docs/capability-format.md`.

- A brainstorming note is a proposal. `integrating-a-proposal` has the `capability-writer` agent (blind to the code; it reads `spec/`, `features/` and `docs/`, and writes only drafts under `.superpowers/spec-drafts/`) merge it into `spec/`, and stops at the one human gate: the added, changed and removed Behaviour lines and the questions the note left open. It never starts a second spec.
- `formulating-features` writes one scenario per approved line and needs no second approval. A line with two readings gets no scenario; its question goes to the person and the answer back through integration. This replaces 0.6.0's settled/deciding sort.
- Slicing cuts stack slices from the bounds in `spec/index.md`; its `QUESTION FOR THE SPEC:` lines end in a capability line or a ledger entry.
- `migrating-to-capabilities` moves a repository with notes and approved features onto `spec/`: capabilities grouped by behaviour, not by the old files; scenarios moved verbatim; test bindings follow the step definitions, which are never edited; the suite, the passing tests and every slice-tag count equal before and after. On a copy of shopsystem-kb: 171 scenarios from 16 features into 20 capabilities, 265 passed before and after, all 89 slice-tag counts equal.

A consuming repository's `CLAUDE.md` can say: "Brainstorming reads `spec/` first. Its note proposes changes to `spec/`, which integrating-a-proposal merges; it never starts a second spec."

## Plans carry no code; approval is for decisions

From 0.6.0 the planner plans and the implementer implements. `slicing-into-increments` hands writing-plans a constraint: no code blocks, file contents or diffs in the plan; each task says which scenarios go green, why they are red today, where the change lands by the project's `CLAUDE.md`, what the spec left open and how it was decided, which steps and fixtures to reuse, and the verification commands with counts taken from the tags. Nothing is built in a scratch copy first and no plan is replayed. Under `bdd-red-green` the implementer writes the code after the red run; a task that carries code is not pasted.

When execution runs under `superpowers:subagent-driven-development`, the controller dispatches by the plan's Global Constraints (from 0.11.0 they carry the execution rules: by step, paths in and short replies out, fresh fix rounds, lanes). Implementers work from intent under `bdd-red-green` and hand back on its stop conditions; "cannot verify" fails a review rather than passing it; main is pushed when the batch is green and reviewed.

0.6.0's settled/deciding sort of scenarios is replaced in 0.8.0 by the gate on Behaviour lines (above). The principle stands: the person approves decisions, not transcription.

## Agents: rules held by tools, not by asking

From 0.7.0 the plugin gives each role in the workflow an agent whose tools are exactly the role's. A controller running `superpowers:subagent-driven-development` dispatches these types instead of `general-purpose`.

| agent | tools | model | for |
|---|---|---|---|
| `shopsystem-bdd:capability-writer` | Read, Glob, Grep, Write | opus | integrating a note into `spec/`, and a repository's first `spec/`, blind to the code; writes only under `.superpowers/spec-drafts/` |
| `shopsystem-bdd:feature-formulator` | Read, Glob, Grep, Write | opus | writing feature files from the spec, blind to the code; writes only under `.superpowers/spec-drafts/` |
| `shopsystem-bdd:initiative-round` | Read, Glob, Grep, Bash, Write, Edit, Agent | sonnet | one round of spec work for the session that keeps the gate: an integration round, the applying of approved drafts, or a formulation round; dispatches only the two agents above |
| `shopsystem-bdd:spec-checker` | Read, Glob, Grep, Write | sonnet | judging a spec against itself, blind to the code: one capability's lines against its scenarios, or every line against the glossary; dispatched by `checking-spec-consistency`; writes only its findings file |
| `shopsystem-bdd:code-scout` | Read, Glob, Grep, Bash, Write | haiku | the Lands probe at slicing and a task's research at planning; writes only its notes under `.superpowers/scout/` |
| `shopsystem-bdd:bdd-implementer` | Read, Edit, Write, Glob, Grep, Bash | sonnet | one task of a no-code plan, one step of it, or one fix round, `bdd-red-green` preloaded |
| `shopsystem-bdd:bdd-task-reviewer` | Read, Glob, Grep, Bash, Write | opus | a task's review, whole or one area of it, and the scoped re-review of a fix round; writes only its findings file |
| `shopsystem-bdd:bdd-branch-reviewer` | Read, Glob, Grep, Bash, Write | opus | the whole-branch review at the end of a batch, or one area of it, shape and coupling included; writes only its findings file |
| `shopsystem-bdd:architecture-reviewer` | Read, Glob, Grep, Bash, Write | opus | an architecture review when the person asks for one (the branch review checks shape and coupling every batch from 0.9.0) |

What the tools make structural:
- **One agent can start another, and only for one purpose.** `initiative-round` has the Agent tool, to dispatch the `capability-writer` and the `feature-formulator` of its round; that it dispatches nothing else is asked, not enforced. No other agent has the tool, so an implementer cannot spawn helpers or its own reviewer, and a reviewer cannot ask for a second opinion.
- **No reviewer has the Edit tool.** Each has Write for one file, its report or its findings, which is asked and not enforced (below).
- **The implementer always has `bdd-red-green` in its context.** It is loaded through the `skills` field, and from 0.13.0 it has no Skill tool to load anything else.

What stays a request:
- **Bash is still available.** Reviewers need it to run the suite, so "no commit, no push, no tag" is still asked, not enforced.
- **Write is not limited to one path.** The task reviewer, the scout and the spec agents are asked to write only their one file. Bash could already write files, so Write gives the reviewer and the scout no power they lacked.
- **Command restrictions don't carry over from a plugin.** A plugin agent's `hooks` and `permissionMode` are ignored, and a tool entry with a specifier such as `Bash(git push *)` removes Bash altogether.
- **The fuller guarantee needs repository settings.** It is `permissions.deny` in the repository's `.claude/settings.json`, which binds the controller too, so the controller's own push must then run where those rules do not apply.

`model` is a default: a dispatch that names a model overrides it, as the controller does for the final review on the most capable model.

