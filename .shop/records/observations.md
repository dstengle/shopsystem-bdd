# Observations

Dated, never edited. An observation is an origin: an initiative may cite it as its `source`.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-design-model-v3
about: capability/formulation
by: the person
date: 2026-10-15

Design model version 3 gives every capability-requirement a stable id `[r<n>]`, referenced as `<capability>#r<n>`; scenarios, resolutions and proposals point by id; a capability-proposal lists `adds`, `changes`, `removes` by id and gains a `formulated` stage. The plugin's format (`docs/capability-format.md`), its writers and formulators, and `features rebind` all still work by text.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-grammar-eval-v1
about: capability/design-model-check
by: the person
date: 2026-10-15

A separate evaluator, grammar-eval (clingo, lark, markdown-it-py), runs grammar.md against documents written as sentences, such as ecommerce-example.md. It is written against model version 1 (transaction, thread, proposal, request, item, `needed_by`). Its FIX notes found clauses of grammar.md that do not compile as written; three of those carry into v3: `standing_edge` (v7c) is undefined, `authored_depends_on` (v4) has no declaration, and `age` (w_stale_intake) has none.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-unmeasured-releases
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the 13 October assessment
date: 2026-10-15

Releases 0.13.0 to 0.18.0 have fixture evidence only: no batch of a consuming repository has been measured on any of them. Every rule change proposed since rests on the 0.10.0/0.11.0 baseline of kb batches 32-35.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-proposal-argues-many
about: capability/spec-migration
by: the session adopting the model
date: 2026-10-15

design-model.md v3 says a capability-proposal argues one capability, and grammar.md v3 rule v_k5 gives an initiative one first part. grammar.md's edge table allows `argues` 1..n. A repository's first spec (a migration) adds requirements to every capability at once; this repository's first spec is one proposal arguing fourteen capabilities. The model has no kind for that, or the one-capability rule needs a stated exception.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-closed-before-formulated
about: capability/design-model-check
by: the session adopting the model
date: 2026-10-15

grammar.md v3's `closed(P)` counts a part closed at `merged` and not at `formulated`, though v3 makes `formulated` a capability-proposal's last stage. Read as written, v_d1 lets an initiative be `done` while a proposal's requirements have no scenarios, and refuses `done` once the proposal is `formulated`. `scripts/model.lp` carries a FIX: a capability-proposal is closed at `formulated` only.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-15-script-behaviour-unpinned
about: capability/feature-file-tools
by: the session drafting the script capabilities
date: 2026-10-15

Behaviour seen in the scripts' source that neither `--help` nor a test establishes, left out of the first spec: `features verify-moved` reporting titles missing or added; `features move` refusing its own file as destination; what `plan show --backlog` prints; the plan file's discovery (exactly one `docs/superpowers/plans/*-slices.md`); `measure`'s refusals for an open batch with no plan and for no earlier archive without `--from`, its ambiguous-commit count and its note when tasks cannot be counted; `tools install`'s output for a non-virtualenv interpreter; `tools untested`'s exit status; `tools check`'s output with nothing to check.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-model-owned-by-knowledge
about: capability/design-model-check
by: the person
date: 2026-10-16

The design model's grammar, its executable form (`scripts/model.lp`) and the check over it belong with shopsystem-knowledge, which owns the shop's artifact types (capability, decision, feature, work-item among them), their IRIs and `check-the-knowledge-base`. Building them here first gets them into use, but leaves the model owned by one of its consumers. 0027 meets the same line: the plugin's ids must follow the IRI decisions shopsystem-knowledge holds (decision/an-artifacts-iri-is-its-types-then-its-owners-path).

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-defects-seen-in-sweep
about: capability/feature-file-tools
about: capability/analysis-tools
about: capability/batch-measurement
by: the session describing the scripts
date: 2026-10-16

Seen while stating what the scripts do, and left as they are: `features tag` accepts `slice-1.2.3`, though feature-file-tools#r11 allows only `slice-<n>` or `slice-<n>.<m>` (confirmed in the pattern `slice-\d+(\.\d+)*`); analysis-tools#r2 says every subcommand needs a Python project, but only `probe`, `install` and `check` test for one; `tools untested` on a missing file, and `tests-of` or `untested` with coverage data but no `.at` file beside it, end in a traceback, not a refusal; `tools check --base` ignores any paths also given, without saying so; `measure batch` ends in a traceback when `--plan` or the archive file is missing from disk; the pytest plugin, with an ini `slice_plan` naming a missing file, expects nothing to fail without saying no plan was read.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-release-0-19-0-defects
about: capability/feature-file-tools
about: capability/analysis-tools
about: capability/batch-measurement
about: capability/spec-integration
by: the session building 0.19.0
date: 2026-10-16

Found while binding the script capabilities' scenarios to tests and in the reviews of 0.19.0. Fixed in the release: `features tag` accepted `slice-1.2.3` (feature-file-tools#r11 allows `slice-<n>` or `slice-<n>.<m>`); `scripts/plan` (about lines 171-172) said "has Scenarios, not Check" for a slice that has a Check, the two kinds reversed.

Still open, left as they are:
- `features holding` prints `for: None` for a held scenario with no `Held for:` line (`scripts/features:413`).
- `tools untested` on a missing file ends in a traceback, not a refusal (`scripts/tools:252-262`, `executed` and `functions` read the file unguarded).
- `tools tests-of` and `tools untested` end in a traceback when the coverage data has no `.at` file beside it (`read_map`, `scripts/tools:193`).
- `tools check --base` ignores any paths also given, without saying so (`scripts/tools:313-315`).
- `measure batch` ends in a traceback when `--plan` or the archive file is missing on disk (`scripts/measure:374`, the `open` of `plan_file` after the commit-based checks at 350-366).
- `tools map` has more than one way of removing the old map: the loop deleting every `coverage*` file (`scripts/tools:168-170`) beside the map file's own replacement through COVERAGE_FILE; one would do.
- A risk for spec-round, not a script defect: a harness that blocks subagents from writing files (one feature-formulator's `.reply.md` write was refused with "subagents may not write report files") stalls a round, because spec-round waits on reply files.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-final-state-only
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-19

There are no intermediate states, only the final state, the plugin fully on design model v3, and the tools that migrate a repository to it. Nothing more is invested in the old system (slices, slice plans, lanes, the old rules) beyond those tools. The plugin moves to the model first; shopsystem-kb and shopsystem-knowledge move afterwards. Decision 0017 is retired; 0028 and 0032 are rejected.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-lines-not-ears
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-19

The Behaviour lines are not in EARS syntax. Beyond the documented adaptations (no "shall", present indicative), lines combine responses with ";", run to two sentences, or describe a form with no system as subject. The person wants EARS syntax, with "shall", ahead of everything else, and the strict form taken back to the design model in shopsystem-knowledge after the migration release.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-files-too-large
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-20

Several Python scripts and test modules are much too large (scripts/model 1035 lines, tests/scenarios/test_design_model_check.py 1490), and large code files slow agents down. The size limit lives only as prose in a consuming repository's CLAUDE.md, this repository has none, and "module" lets extension-less scripts and test modules slip through. The person: the limit is 300 lines for code and tests alike; the split is next release.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-left-for-next-release
about: capability/supervision
about: capability/work-queue
about: capability/migration-tools
by: the person, at the 0.21.0 release gate, on the final review's findings
date: 2026-10-21

Left as they are for the next release (the final review of 0.21.0, `.shop/scratch/run/final-review.md`):
- S7: code-scout.md, bdd-implementer.md and bdd-task-reviewer.md say `ls`, `cat`, `wc` and `grep` are allowed, but no `--allowedTools` entry gives them and the stub refuses them; probe the real CLI once to learn which is wrong.
- M18: the stub matches the whole command with fnmatch (`tests/scripts/stub_claude.py`), so `*` matches `;`, `&&` and `|`, unlike the real CLI; it never checks that `--agent` resolves in `--plugin-dir`, and ignores `--max-turns`.
- M20: `work add` writes `--accepts` and `--part-of` values containing `,`, `]` or `#` unquoted into flow YAML (`scripts/workqueue.py`); the global `--root`, and the id derived from spec/index.md, have no line.
- M2: `migrate run` overwrites a tracked spec/decisions/index.md without a word.
- M3: migrate's refusals that no line states: ledger prose outside entries, a heading not in `## decision/…` form, a duplicate entry, a value `quoted()` cannot write, two sources to one destination; links to the removed spec/decisions.md are left dangling.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-release-gate
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-21

The person approved every card of the 0.21.0 release gate (https://claude.ai/artifact/DnuBKmGFec57xuQ2X7NzgN): release (merge to main, tag `v0.21.0`, push); the four choice cards, each with its recommended option A: pytest-python (accept it inside the worker's own worktree, guarded by supervision r21 and r28), delivery-toml (`[allowed_tools]` is the person's override, r30, with r29 for `[tests]`), skill-tool (role-boundaries r4 changed: the implementer has the Skill tool) and r20-fileset (the planner's final set written at `planned`, r31); lines (all seventeen); decisions (0037-0050 and 0053 accepted, 0039 amended); readings (all confirmed). The unbuilt lines are drafted work-items for after the release.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-session-keeps-the-gate
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-21

In the migration release the coordinating session kept its context small by handing integration, gate assembly, applying verdicts, trials and analysis to agents that replied in a few lines and left the rest in files, with one ledger as the recovery map. Several of those were general-purpose agents because the plugin had no role for the work, or the installed plugin lacked the branch's agents. The person wants the practice kept, through the plugin's own roles, in the next release.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-one-requirement-per-scenario
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person
date: 2026-10-21

A supervision scenario tagged `@r1 @r9` took r1's title, never checked r9's own response, and asserted "it exits 0", which no line said (the code came from the Implementation section; the feature file was written by its implementer, not formulated blind). The person: map a scenario to a single requirement, sharing steps in code where useful; a line says a command exits successfully or with an error, never a Unix code; waiting on a ruling is exiting with an error. Done as 0.21.1.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-refusal-worked-around
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the coordinator, reported to the person
date: 2026-10-22

Claude Code's safety check refused an implementer's `cp` of a reformulated feature file over the tracked file in its worktree. The feature-file-tools implementer stopped and reported, as it should. The batch-measurement implementer made the same change with the Edit tool instead. The result was byte-identical to the formulator's draft on an unmerged branch, and the person accepted it, but the workaround is wrong: a refused action is reported, never achieved another way. Since then the coordinator lands reformulated feature files itself and implementers start from that commit.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-migration-tools-as-is
about: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
by: the person
date: 2026-10-22

No more time on migration code (the person): shopsystem-knowledge is the only repository left to migrate, and anything `migrate` does not do there the migrating agent fixes by hand. migration-tools keeps its feature file from before the 0.22.0 reformulation, so two of its scenarios still name two requirements (v_s2) and some of its steps name exit codes; they stay so unless migration-tools is worked on again.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-deferred-from-0-22-0
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("I want a release"), recorded by the coordinator
date: 2026-10-22

The 0.22.0 final review's Critical finding (C1) was fixed for the release; its Important findings were deferred to
0.23.0, with the lines drafted for them (in .shop/records/review-findings once archived; ledger-0.22.0):
`work withdraw` (a way into `withdrawn`); which line wins when a worker's result and a fault both apply (r47); r4
naming r43; work-queue r8's "before the stage that failed started"; r45 covering a non-zero exit; the branch review's
result kept and logged (r48) and not rerun on an unmoved branch (r49); log lines and other code no line asks for moved
into Implementation or given lines; undefined words ("the tests", "the repository's remote", "fault"). r43 masking a
regression while another open work-item accepts the requirement is the approved trade-off and stays.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-release-gate-0-23-0
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("Confirmed on the release gate artifact"), recorded by the coordinator
date: 2026-10-22

The person confirmed the 0.23.0 release gate (https://claude.ai/artifact/PtqctgL9gNGTLvuGZS6iNg, version 3) as
recommended: release 0.23.0; the coordinator's readings under delegation stand; for 0.24.0, the `--work-item` option
keeps probe files and non-scenario tests (the cause of researchers ending at their limit,
measurement/2026-10-22-research-at-the-limit), work-items get context-scoped `w<n>` ids in place of names (the
person: "Why wouldn't we use Ids instead of names and get all of the uniqueness we need?"), and `measure` counts round
trips; analysis-tools' `--json` lines are held; no allow rule is added for the refused subagent writes.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-point-release-0-23-1
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("Take care of the --work-item issue as a point release"), recorded by the coordinator
date: 2026-10-22

The person asked for the `--work-item` fix approved for 0.24.0 at the 0.23.0 gate as a point release, 0.23.1, and
delegated its small-change gate to the coordinator's recommendation. Supervision r55 and r56 were written, formulated
and delivered by a direct bdd-implementer (initiative i20); the duplicate work-item names and the other 0.24.0 items
stay for 0.24.0.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-release-0-24-0
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("I thought we were fixing the names. Please get the work ids released"; "Please create a more general purpose migration capability ... Now skip questions and get the release done"), recorded by the coordinator
date: 2026-10-22

The person asked for the work-item ids as the next release, with a general upgrade capability offered when a newer
plugin is installed, and delegated every gate to the coordinator. Under that delegation the coordinator approved the
lines of i21 (64d0443, 4cf0163, the widened r26), raised the researcher's limit to 40 (supervision r19: with probes
working, design-model-check-3's researcher still ended at 25), ruled the open questions (work-queue-5 reading A, its
two deprecated scenarios retired; design-model-check-3's step leaving r110's problem out of other lines' counts;
migration-tools-1's Important fixed; w2 reading A, an empty title refused), and dropped work-queue r7's outline row
"add i1 ../../w1" (f69c120) because a title is no longer a file name (branch review 2, N1). `work rule` is still
missing, so ruled work-items were finished by direct implementers and withdrawn from `work run`. Round trips in
`measure` and analysis-tools' `--json` lines move to the next release. This repository was upgraded by its own
`migrate upgrade` (9170f7a).

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-23-hung-worker
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("leave that for later"), recorded by the coordinator
date: 2026-10-23

During i22's third `work run`, w97's bdd-task-reviewer started 18 minutes before the machine was suspended and never
came back: 3 s of CPU in 10 h 50 min, its result file the placeholder it wrote in its first seconds. `work run` waits
on a worker with no limit of time, so it waited the whole night until the coordinator killed the reviewer (exit 143,
w97 failed, then retried). The coordinator proposed a line ending a worker silent for longer than a set time, as a
failure of the work-item; the person deferred it: not in i22's batch.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-23-open-initiatives-closed
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("close all 10"), recorded by the coordinator
date: 2026-10-23

The coordinator's sweep of the open initiatives found every work-item of each green or withdrawn, and every requirement
still without a passing scenario in the agent and skill capabilities, which have no feature files by design (decision
0030). The person closed all ten: i1, i3, i8, i9, i10, i11, i13, i16 and i17 as done, their agent and skill lines
delivered by the shipped agent and skill text; i14 as abandoned, its work belonging to shopsystem-knowledge.

Closing them adds nine `model check` rows, v_d1 "a done initiative has a part open": i1, i3, i8, i9, i10, i11, i13, i16
and i17 each keep capability-proposals at `merged`, those of agent and skill capabilities, which never reach
`formulated` because they have no feature files (decision 0030). A capability-proposal's file form allows no status
after `merged` but `formulated` (`delivered` is refused as a file problem), so the model has no way to close such a
proposal. The rows are left standing; giving the model a closing status for these proposals is work for a later batch.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-23-decision-0030-misread
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the coordinator, after the model check analysis of 2026-10-23
date: 2026-10-23

The two entries above (2026-10-23-open-initiatives-closed and its v_d1 paragraph) misquote decision 0030. It does not
say the agent and skill capabilities have no feature files: it says they get Gherkin scenarios run as headless
`claude -p` fixture sessions, and it rejected grouping them as guarantees. spec/index.md says that until a line's
scenario is written, `model check` reports it under v_s3. The harness of decision 0043 was never built, so those
scenarios do not exist yet. The coordinator gave the person the misreading when recommending the ten closings; the
person closed them on it. The closings stand until the person decides between building the scenarios (0030 kept) and
superseding 0030 with guarantees checked by `measure`.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-24-guarantees-work-item
about: capability/supervision
by: the coordinator, after i23's delivery and the 0.25.0 release
date: 2026-10-24

A work-item whose accepted requirements are all guarantees (decision 0065) has no scenarios, and `--work-item` refuses
it ("accepts none of the scenarios it collected"), so `work run` cannot deliver it. In i23, w111 (delivery#r17, r18:
skill text) was implemented by a direct bdd-implementer dispatch, reviewed by the coordinator, merged by hand and
withdrawn; the person accepted that delivery on 2026-10-24. 0.25.0 still refuses such a work-item (README, 0.25.0).
Every later change to a workflow capability's lines meets the same refusal. The coordinator's proposal: `--work-item`
accepts a work-item with no scenarios when every requirement it accepts is a guarantee, and the review stage judges it.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-24-i23-open-cases
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the coordinator, from i23's formulation rounds and branch reviews
date: 2026-10-24

Cases i23 left unpinned by any line, with what the code does in 0.25.0. Each is a candidate for a small change that
pins today's behaviour:
- migration-tools r30/r31: a `.shop/plugin-version` holding only whitespace reads as empty ("it is empty"); a version
  followed by more lines is refused, naming what the file holds; a missing file is no version recorded (0.23.1).
- work-queue r15: an answer ending in a newline is refused (the answer is not trimmed before the check).
- batch-measurement r59: a time with no `Z` and no offset is read as UTC.
- O1 (branch review 2): `work run` keeps every file a stage leaves in its run directory; w119's researcher left probe
  repositories there, committed as 7 dangling gitlinks (removed in c9e1de6). It should keep regular files only.
- F3 (branch review 1): when implementers working at the same time end together, r61 merges them one at a time, but
  not necessarily in the order they ended.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-24-context-loop-not-queued
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the person ("I really don't understand where the work is that I've requested"), recorded by the coordinator
date: 2026-10-24

The design note 2026-10-23-requests-and-the-context-loop, approved by the person on 2026-10-23 (f9a5ed2), proposes
section 1 (design model v4) and requests R1-R6. Section 1 went into docs/design-model/ without an initiative, on the
person's direction (8ba0618), and shipped in 0.25.0; `model check` still checks the v3 rules. R1-R5 were never put
in `.shop/work/`: no initiative, capability-proposal or request cites the note, so nothing kept them in view, and the
skills of 0.25.0 still hold what R5 removes (both small-change paths, "If the person is talking to you", drafting in
delivering-an-initiative). On 2026-10-24 the coordinator followed integrating-a-proposal's small-change path for
observation 2026-10-24-guarantees-work-item and the person stopped it: "I thought the small-change path had been
eliminated so that this session doesn't write anything". R6 is outside this context.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-24-i24-delivery-gaps
about: capability/supervision
by: the coordinator, delivering i24 under the person's delegation ("Please get everying delivered. Do not stop to ask me questions or permission.")
date: 2026-10-24

Gaps `work run` showed while delivering i24, each worked around:
- A task review's finding on a `done` work-item can only go back to the reviewer: `work answer` returns the work-item to the stage that asked (decision 0063), and a reviewer changes nothing, so w121's finding came back unchanged. w121 was withdrawn and redrafted as w125; w126's and w128's findings were accepted and drafted as fix work-items w148 and w149.
- A scenario formulated before any work-item accepts it fails every other work-item's whole-suite run (r43 counts only scenarios an open work-item accepts): w125 stopped on phase B's and C's scenarios until their work-items were drafted.
- `work run` given no `agent-vault run` cannot push (its pre-flight `git push --dry-run` fails), so every work-item it started failed before its research.
- An implementer's run of a scenario that starts a nested `work run` loaded the main checkout's `scripts/work_items.py` through the inherited PYTHONPATH, so a change to `--work-item` was tested against the old code (fixed in 82ad81f, the supervision steps).
- work-queue r23 is set by `work` commands only (the coordinator's ruling on w130): an initiative whose last work-item `work run` takes to green stays `started`.
- A Scenario Outline was committed with no Examples table (requests r17) and `features bindings` and `model check` passed it.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-i24-unpinned-cases
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
by: the coordinator, from i24's task reviews, under the person's delegation
date: 2026-10-25

Cases i24's task reviews found that no line pins, accepted as the code has them:
- work-queue r23: `work retry` returning a work-item to green (after a push failure) does not run the done check, so the initiative stays `started` (w130).
- batch-measurement r63/r64: `measure initiative` refuses an initiative whose request is missing, has no asker, or whose `fulfils` holds more than one id; no line asks for the refusal (w133).
- supervision: the readings ruled on w135 and w137 (intake only from `work run` with no initiative; a round's branch merged when it ends; a gate with no question goes on to apply; a failed round keeps the proposal's status) are in those work-items' answers, not in lines.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-answer-pass-once-a-run
about: capability/supervision
by: the coordinator, from w147's task review, under the person's delegation
date: 2026-10-25

`work run` gives questions to a delegated answer session (supervision r77) once, at the start of a run, so a question raised during the run (a gate round's, a worker's) goes to the person with exit 3 and is answered under the delegation only by the next `work run`. Accepted as it is for i24.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-integrate-round-without-request
about: capability/supervision
by: the coordinator, delivering i24
date: 2026-10-25

Once w151 (supervision r79, r84) was merged, `work run i24` moved the `proposed` i24 to `started` and then stopped with "work: there is no request  under .shop/work/requests", leaving a `log.jsonl` line uncommitted: i24 fulfils no request (it predates R3's requests), and r79 gives a `proposed` initiative an integrate round from its request's lines. No line says what `work run` does for a `proposed` initiative that fulfils no request (v16a reports it). The line was committed by hand and the run restarted.

## observation/missingmass.io/shopsystem/shopsystem-bdd/2026-10-25-thread-crash-exits-zero
about: capability/supervision
by: the coordinator, from w134's task review, under the person's delegation
date: 2026-10-25

In a `work run` with no initiative (supervision r66, r81, r82), an exception other than `Refused` raised in one initiative's thread is only printed by `threading.excepthook`, and the run can exit 0 under r82 although that initiative's nodes can still move; with one initiative the same crash exits non-zero. Accepted as it is for i24.
