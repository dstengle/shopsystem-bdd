# Proposal: predictable batches, and analysis tools in place of grep and hand probes

From a kb session, 2026-10-10 to 2026-10-11, for a shopsystem-bdd session to brainstorm into a design and release.
The person asked for it after three and a half batches of kb's K2 release (shopsystem-kb, worktree
`shopsystem-kb-main`, branches `batch32-kb-v2-identity` to `batch35-placeholders`) ran under 0.11.0. Their words:
the changes get done, it takes longer than they would like, and they can live with that if the work is predictable
and of high quality. They want every improvement made in the plugin, none only in kb. Everything below is a
proposal; how each is worded in the skills, agents and scripts is the shopsystem-bdd session's.

Where the evidence is: the ledgers under `shopsystem-kb-main/.superpowers/sdd/2026-10-10-kb-batch32-implementation/`,
`…batch33…` and `2026-10-11-kb-batch34-implementation/` (`progress.md`: every hand-back, ruling and review reply),
the scouts' notes under `.superpowers/scout/`, and the living plan's log and archives
(`docs/superpowers/plans/2026-09-24-kb-slices.md`, `archive/…-batch32.md` to `-batch34.md`). Token figures are the
agents' own usage reports summed by the controller; times are commit timestamps.

## What happened

Twenty slices in about four hours: 157 to 160, 160.1 to 165.1, 165.2 to 165.6.

| | tokens | share |
|---|---|---|
| implementers | about 3.0M | 49% |
| reviewers | about 1.8M | 28% |
| scouts | about 1.4M | 23% |

- **Wall-clock.** About 60% building slices, about 37% closing batches (branch review, fix wave, re-review). Pace
  per slice was about 8 minutes, the same as kb's batch 31 under 0.10.0; slices are smaller now, so there are more
  of them, and they run one after another.
- **Against slice 156.** That slice (0.10.0, one implementer) changed about 3,050 lines in 75 files for 425k tokens
  in 36 minutes. Batch 33 (0.11.0) changed about 3,100 lines in 44 files for about 1.7M implementer tokens, 3.1M
  with its reviews and scouts, in about 105 minutes. The two are not like for like (156 was mostly mechanical
  migration, batch 33 was design-heavy and grew mid-batch), but per file touched 156 cost about 6k tokens and batch
  33 about 39k. What was wrong with 156 was risk, one diff too large to review, not cost.
- **A floor per dispatch.** The smallest dispatches (a two-field contract step, a test split, a scoped re-review)
  cost 30k to 40k tokens each before doing anything: CLAUDE.md, the brief, the reports before it. Across about 70
  dispatches that floor is an estimated 2.3M tokens, over a third of the total.
- **Batches grew.** Batch 33 was planned as 7 tasks and ran 11. Batch 34 did not exist until batch 33's review
  found a regression. Slice sizes measured by search were floors that the work passed: slice 160.1 was counted at 3
  production modules and landed in 6, the import slice at 2 and landed in 5.

No agent ran over about 165k tokens, no implementer lost its place, every hand-back was a real plan defect, and the
reviews found real defects (a race, a regression, two contract gaps). 0.11.0 did what it set out to do. The request
is about what it costs and what it cannot see.

## Three things the workflow cannot see

### 1. Nobody traces a decision's consequences through the code

The capability writer and the feature formulator cannot see the code, by design. Slicing counts where a slice
lands by search. Between "the line is approved" and "the slices are cut" nothing asks: what else in the code
assumes the old thing?

kb's decision "an artifact keeps the version of its type it conforms to" also meant that reads, stored links, the
export and the import had to go through that version. Each was found late and separately:

- slice 162's task review: reads of such an artifact were refused, and a type's change silently rewrote its links
  (dropping a link that guarded its target from removal);
- slice 165's task review: a type another type's version reads could be removed, after which the store's own
  check failed;
- batch 33's branch review: an exported store no longer imported readably (a regression against batch 32).

Each finding cost a spec change, a scout, new slices and a re-plan in the middle of a batch. The branch reviewer
found the whole class in one table, "every place in `src/` that still reads an artifact through its type's latest
version". That table, made at planning time, would have put all four into the batch plan.

### 2. Re-formulation un-tests behaviour that still exists

When a release re-words scenarios, the old scenarios' bindings and step definitions go (kb's slice 154 removed 38),
and the re-worded scenarios are tagged to future slices. The behaviour still exists; nothing tests it until its
slice arrives. Three effects, all observed:

- **A regression with no red.** Batch 34's slice 165.5 re-keyed the import's files. The plan guarded it with "a
  test that breaks is `BLOCKED`". Every scenario of the import's skip analysis was tagged slice 184 and unbound, so
  no test could break; `kb import --skip-errors` went from landing what it could to refusing outright, and only the
  branch review's own probe noticed.
- **A module that stops collecting.** Merging one re-formulated scenario title at the start of batch 35 made
  `tests/test_remove_an_artifact.py` fail to collect (32 errors), because its `@scenario` binding named the old
  title. The slice that binds the new one was two tasks away.
- **Ninety expected failures.** The suite has run at "N passed, about 90 failed" for the whole release. "No new
  failure" is checked by each implementer comparing lists of failing names, often by stashing its change and running
  the suite twice. One implementer's record mis-stated which scenarios failed and the controller had to verify it
  later.

### 3. Reviews are the defect detector, and they work by hand

What the reviewers found, they mostly found by writing probes: a store exported, imported and read back; two
changes held at a gate and released in each order; a set that changes a type twice; a listing assertion that
compared `[] == []`. These are properties of the system that hold for every change, re-derived by the most
expensive agent each batch, and gone when its scratch directory is removed. The same reviewers also spend their
attention on what a tool decides in a second: a module over its size limit, a function with no caller left, a broad
`except`, a row of the module map against the imports.

## What 0.11.0's own rules cost

- **Three of four hand-backs were listing omissions.** Slices 161, 163 and 165.3 each stopped on a test the task's
  "Tests the decisions break" had not named. In two the only change needed was to a test's setup, with no assertion
  touched; in one the tests had been written one slice earlier, in the same batch, to pin an interim state the plan
  itself asked for. Each stop cost a plan amendment and a fresh dispatch, five to eight minutes. The rule is right
  for a test that guards shipped behaviour; it makes no difference between that and these.
- **Steps reload the same context.** Slice 161 ran as four fresh implementers, about 350k tokens. Steps earned their
  cost where a contract or stored-layout change had to land first and be seen green alone; elsewhere each step paid
  the floor again.
- **Seven per-task reviews came back clean** (157, 158, 160.1, 161, 163.2, 163.3, 165.3), about 480k tokens. The
  reviews that found something were on concurrency, the landing transaction and the contract. Both branch reviews
  found defects no task review had. "Data integrity" as a trigger for `Review: per-task` selects nearly every slice
  of a store.
- **Several slices were step definitions only** (159, 160's first step, 161's and 163's last steps, and by the
  scout's reading all of 167 and 168): an earlier slice had built the behaviour. They ran one at a time on the most
  capable model.
- **Sizing far ahead went stale.** One pass sized slices 157 to 185 (about 790k tokens). The notes for 166 to 185
  assumed a storage design that batch 33 then built differently, and batches 34 and 35 were researched again.
- **The budget counts modules.** A 75-file mechanical rename behind a seam is cheap and needs little judgement; a
  5-file change to the landing transaction is neither. Module count prices them the wrong way round.
- **No lane ran.** In 20 slices every pair shared a production module or a test file. Reviews and planning ran
  beside implementation; implementation itself was serial.

## Proposals

### A. Tools: probe, install, report, and use them before grep

A new script (say `scripts/tools`, beside `plan` and `features`) that every workflow run starts with:

1. **Probe.** For the project's language, detect each tool below in the project's own environment (for Python, its
   virtualenv) and print one line per tool: present with its version, or missing.
2. **Install.** For each missing tool, try to install it into that environment as a development tool, without
   editing the project's dependency files. Whether a project then records the tools as development dependencies is
   that project's enabling slice, not the plugin's doing.
3. **Report.** If any is still missing, say so to the person in plain words before work starts: which tool, what
   it is for, what the workflow does without it, and the command that failed with its error. Never go on silently
   without one. Log the result in the plan (`Probe: tools -> …`), so a later session and every agent can read what
   is available.
4. **Degrade openly.** An agent that falls back to text search because a tool is missing says so in its notes or
   report, so a count made by search is never mistaken for one made by analysis.

The tools, by what they replace (Python names; the script should hold the equivalent set per language it supports
and say plainly when it supports none for a project's language):

| need | tool (Python) | replaces |
|---|---|---|
| which tests execute a function; which code no passing test executes | `coverage` with per-test contexts (`pytest-cov --cov-context=test`), run as its own command, not in the fast suite | the scout's search for "tests the decisions break"; the guard "a test that breaks is BLOCKED" where no test exists |
| exact references, callers and transitive reach | `pyright` (or `jedi`) | grep for a name; "the count is a floor" |
| structural search | `ast-grep` or `semgrep` | patterns grep cannot say: calls that rely on a default argument, a broad `except`, a raw request field read outside the conversion module |
| the module map's "never holds" column as checked contracts | `import-linter` | the reviewers' reading of imports against CLAUDE.md |
| lint, line length, unused imports | `ruff` | review minors |
| code with no caller left | `vulture` | three review findings after removals |
| properties over random sequences of calls | `hypothesis` (stateful) | the reviewers' hand probes |
| assertions that assert nothing | `mutmut` (or `cosmic-ray`), on a slice's changed lines only | "went green on step definitions alone", vacuous assertions found by review five times |
| only the tests a change reaches | `pytest-testmon` | running the whole suite to compare two lists |

Agents and what each should use:

- **code-scout**: references and call reach for "where the change lands"; the coverage map for "tests the decisions
  break" and for "which of this code does no passing test execute"; structural search for the consequence sweep
  (B below). Its notes say which tool gave each count.
- **bdd-implementer**: the coverage map to confirm its red test reaches the code it is about to change; mutation on
  its changed lines before it reports a scenario green that it never saw red on a Then line.
- **bdd-task-reviewer and bdd-branch-reviewer**: the lint, dead-code, size and import-contract checks as commands
  whose output they read, in place of looking; their attention goes to behaviour.

### B. A consequence sweep between integration and slicing

For each decision a batch applies, before its slices are cut: one scout asked "what in the code and tests embodies
the old assumption?", answered with the tools in A (references to the functions that read the old form, structural
search for the old pattern, the tests that execute them). Its output is a table like the branch reviewer's: place,
what it does today, what the decision makes of it, which slice owns it or that none does. A place no slice owns
becomes a slice, a line for the spec, or a logged deferral with its price (what breaks meanwhile, with a
reproduction), before execution starts. slicing-into-increments would own it; the plan carries the table's rows that
are deferred.

### C. Re-formulation keeps behaviour tested

- **Keep the old binding until the new one is bound.** When a scenario is re-worded and its slice is in the future,
  the behaviour it described is either unchanged until that slice (then the old scenario's steps stay bound to a
  held copy of the old text, marked as holding, and are retired by the slice that binds the new one), or it is
  already gone (then its removal belongs to the slice that removed it). formulating-features and slicing would
  decide which per scenario; "its steps go now and its replacement comes later" is not an option.
- **A changed title never breaks collection.** Merging feature files must leave every test module collecting: a
  binding whose scenario was re-titled is rebound in the same commit, by the `features` script if it can.
- **The suite is green between slices.** A scenario tagged to a slice not yet built is an expected failure,
  strictly: marked by its slice tag (the `features` script can generate the marker, or a conftest hook can read the
  tags and the plan's statuses), so the suite passes, an unexpected failure is red, and a scenario that starts
  passing before its slice is also flagged. The suite record becomes "N passed, M expected to fail, 0 failed", and
  nobody compares lists of names.
- **A guard needs a test behind it.** A task may say "a test that breaks is `BLOCKED`" about some behaviour only if
  the coverage map shows a passing test executing it; otherwise the task first writes the holding test.

### D. Invariants as tests, and probes that are kept

- A project states a handful of invariants once (for kb: every held artifact reads at every level; the store's
  check never answers with the store's own fault; export, import, export gives the same bytes; a refused set writes
  nothing), as stateful property tests that run in the suite. The plugin's part: slicing cuts them as an early
  enabling slice of a release, bdd-red-green treats a property's failure as a red like any other, and CLAUDE.md
  gains a place for them.
- A reviewer's probe that finds a defect is handed to the fix round as a test to keep, and a probe that exercises a
  property for every change is proposed as an invariant, not deleted with the scratch directory.

### E. The rules of 0.11.0, adjusted

1. **"Tests the decisions break", with two standing allowances.** An implementer may change an existing test's
   setup, with no assertion changed, where the task's decisions require it, and may rewrite a test written earlier
   in the same batch that pinned an interim state; it lists each in its report, and the reviewer checks the list.
   Changing what any other test asserts stays a hand-back. The coverage map (A) makes the list itself more complete.
2. **Steps where an order must be seen, not by file count.** A task gets Steps when a contract, stored-layout or
   port change must land and be green alone before what uses it, or when it is over the budget and was cut as
   expand, migrate, contract. Otherwise one dispatch, which may reply `PARTIAL` (0.11.1's budget).
3. **A continuation keeps its context where the harness allows.** Resuming the implementer that replied `PARTIAL` or
   finished a step costs nothing to reload; a fresh one is for a different model or a stuck agent.
4. **A smaller packet per dispatch.** The brief carries what its task needs of CLAUDE.md (the rows of the modules it
   names, the rules it must keep) and of earlier reports (the public names they introduced), so an implementer or
   reviewer reads one file, not the map and three reports. The floor per dispatch is the largest single cost.
5. **`Review: per-task` by risk of the change, not by what the project is.** Per-task for a change to concurrency,
   to a transaction that lands data, or to the published contract; every other task is reviewed by the branch
   review, which is told to read those diffs with a task review's care. The branch review stays as it is: it found
   what task reviews missed in every batch.
6. **Step-definition slices are bundled and cheap.** When the scout's red run shows a slice's scenarios need steps
   only, slicing bundles them with their neighbours in the same feature and the plan gives them the cheaper model.
   If a scenario then is red on behaviour, that is a hand-back, as now.
7. **Budget by kind of change.** Keep the count, and add the kind: mechanical migration behind a seam (a search
   says what moves, no judgement per file) may run large in one agent with a search for its check; a change to
   concurrency, landing or the contract stays small whatever its count.
8. **Research one batch ahead.** Size and research the next batch, and at most the one after; a release's later
   slices keep their one-line Unknown until the batch before them closes. One research scout per batch, and a
   scout per task only for a slice that changes a form other code depends on.
9. **Lanes are rare; say so.** The plan should not be shaped in hope of them. Where the scout's file lists show two
   tasks disjoint, mark them; otherwise parallelism is reviews, scouts and the next batch's planning beside the
   implementer, which is where it actually came from.
10. **The controller reports by slice.** One line to the person when a slice goes green or a decision is taken, not
    one per agent notification; every notification costs a turn that re-reads the session.

## What to measure

So the next release can be compared with this one: tokens and wall-clock per slice by role; dispatches per slice;
hand-backs and their cause (listing omission, real conflict); tasks planned against tasks run per batch; defects
found by task review, by branch review, and after a batch closed; and the share of a batch spent closing it. The
`plan` script's log already holds most of the timestamps; the agents' usage figures would need recording in the
ledger or the log as they arrive.

## What this request does not ask

- No change to the one human gate, to scenarios written without sight of the code, or to red before green.
- No tool run inside the fast suite that would slow it: the coverage map, mutation and the import contracts are
  their own commands.
- Nothing installed into a project's dependency files by the plugin.

## Open questions for the shopsystem-bdd session

- Which languages the tools script supports at first, and what it says for the rest.
- Whether expected-failure marking lives in the `features` script (generated markers) or in a conftest the plugin
  provides, and how it reads the plan's statuses.
- How the consequence sweep's table is reviewed: by the person at the gate, or by the planner alone.
- Whether a held copy of an old scenario lives in the feature file (tagged as holding) or beside it.
- Whether kb should be re-run on one batch under the new rules as the plugin's own test, as slice 156 was for
  0.11.0.
