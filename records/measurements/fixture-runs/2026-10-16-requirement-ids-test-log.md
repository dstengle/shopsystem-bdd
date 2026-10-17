# Requirement ids: test log (0.19.0)

Branch `0.19.0-requirement-ids`, commits `9038634` to the release commit. Scripts: 307 tests, OK.

**The headless runs were made.** Task 7's self-run of the formulation text was blocked by the permission
classifier and is not among them: its feature files were formulated in-session (below). Task 9's fixture runs were
first denied the same way. The person then allowed the harness scripts with `/permissions` rules, and the runs
were made: 15 B runs and 4 A runs, each one headless `claude -p --model sonnet` session on a fresh fixture. B is
this branch at `8b61d65`, A is 0.18.0 at `e3c846d`. Results are under "Fixture run results".

## What changed

- Design model v3 in use: every Behaviour line `[r<n>]`, every scenario tagged `@r<n>`, retired ids in the
  capability's frontmatter, capability ids as IRIs under the context id.
- `scripts/model`: held scenarios are no acceptance-scenarios; a decisions ledger is read; `features tag` takes
  `r<n>`.
- `docs/capability-format.md`, `integrating-a-proposal`, `formulating-features`, `migrating-to-capabilities`
  (including "Adding Ids" for a repository already on capability files), the `capability-writer` and
  `feature-formulator` briefs.
- Five script capabilities formulated and bound: `analysis-tools`, `batch-measurement`, `slice-plan-tool`,
  `design-model-check`, `feature-file-tools`.
- Version 0.19.0, README, `spec/index.md`, initiative i3, observation
  `obs/2026-10-16-release-0.19.0-defects`.

## Formulating this repository's script capabilities in-session

Five `feature-formulator` agents were dispatched with the new brief, one per capability, drafts under
`.superpowers/spec-drafts/2026-10-16-script-capabilities/round-1/`. The brief was formulating-features' new text,
written out as the skill gives it. This exercises the brief and the agents, not the skill's end-to-end run:
`spec-round`, `model check` inside the round and the commit step were done by an implementer by hand.

- Requirement lines per capability, each with a scenario tagged to it (from the capability files and the feature files' distinct `@r<n>` tags): analysis-tools 35, batch-measurement 38, slice-plan-tool 38, design-model-check 45, feature-file-tools 51; 207 in all.
- The formulators returned 14 questions between them (analysis-tools r1, r14; batch-measurement r10, r34;
  slice-plan-tool r8, r10, r23; design-model-check r23, r26, r27, r41; feature-file-tools r3, r4, r14). The lines
  were drafted from the 0.18.0 code and admitted two readings.
- The questions were answered from the code, not by the person: each line was reworded to state what the code does
  (14 rewordings, commit `d4090e3`), then a second round formulated them (14 of 14, no questions). Four lines
  changed meaning against the draft, because the code did not do what the draft said: r1, r3, r26 and r41.
- After review, four scenarios were fixed where they asserted more than the code does, only the affected steps,
  and one line (analysis-tools r16, import-linter run over no paths) was reworded at binding. These rewordings are
  listed for the gate: the person sees them there, and may reject any.
- One formulator, analysis-tools, could not write its `.reply.md`: the harness refused ("subagents may not write
  report files"). The drafts were written. `spec-round` waits in one shell command for every reply file, so a
  harness that blocks them stalls the round. Recorded as a risk in the observation, not changed.
- Untagged scenarios: none. Coverage after formulation was checked by `model check`.

## Binding

Each scenario is bound to the unittest test whose docstring is its title; scenarios are tagged `@r<n>`, titles are
free. 307 tests. A mutation check per subtask: each new test passed on its first run (the code already did it) and
was then failed by a scratch mutation of the script, restored afterwards.

| subtask | script | mutation checks |
|---|---|---|
| 8a | `scripts/model`, `model.lp` | each new test failed by a mutation; r41 first survived (dates in id order) and its data was changed |
| 8b | `scripts/features`, `slice_expectations.py` | 21 mutations caught |
| 8c | `scripts/plan` | 34 mutations caught; two survive (porcelain-only, the title check has no scenario) |
| 8d | `scripts/measure` | in the subtask report |
| 8e | `scripts/tools` | about 35 caught; two redundant map mechanisms (old-map removal, `--cov-append`) mask each other and survive |

Code defects found and fixed:

- `features tag slice-1.2.3` was accepted, though feature-file-tools r11 allows `slice-<n>` or `slice-<n>.<m>`.
- `scripts/plan` reported a slice that has a Check as "has Scenarios, not Check": the message was reversed.

Open defects are in `obs/2026-10-16-release-0.19.0-defects`.

## The fixture harness

Built and self-tested in `/home/vscode/scratch/shopsystem-bdd/ids/` (`make_ids.py`, `score.py`, `run.sh`,
`run-all.sh`, `selftest.sh`, `selftest.out`). Five cases: `integrate` (to the gate), `apply` (approved drafts
applied and committed alone), `formulate` (with clingo), `noclingo` (clingo hidden by a `PYTHONPATH` directory;
the run must say model check did not run), `migrate` (adding ids to a repository on capability files).
`run-all.sh` runs three B runs per case (the branch) and two A runs of integrate and formulate (0.18.0, cost only).

The self-test needs no model. Fresh fixtures fail every check a run has to achieve; a hand-made correct result
passes every check (ok lines in selftest.out: integrate 7, apply 7, formulate 8, noclingo 7, migrate 12); mutation cases (a renumbered
line, an apply message that names the wrong lines, an unformulated lend-items, a v_s3 left, the index id not
changed, spec and features in two commits) each fail the check meant for them (some fail others too: the stale index id also fails `model check` and the one-commit check). Two rounds of review
of the harness fixed: a correct same-line gate misread, the missing index id and one-commit checks, and prompts
that hinted the checks.

Command: `/home/vscode/scratch/shopsystem-bdd/ids/run-all.sh`, allowed by the person's `/permissions` rules.
Results: scores in `scores-final.txt`, costs in `costs-final.txt` in the same directory, scored with B's model at
`8b61d65`. Three B runs of each case; two A runs each of integrate and formulate. The A fixtures already carry
ids, so A was scored with B's checks and counted for cost only.

## Fixture run results

One table per case: each check, then ok or FAIL for B runs 1, 2 and 3.

**integrate** (to the gate)

| check | 1 | 2 | 3 |
|---|---|---|---|
| the gate text is the reply | ok | ok | ok |
| the gate shows keep-items' two added lines with ids | ok | ok | ok |
| the added lines are r6 and r7, never r3 | ok | ok | ok |
| the changed count line keeps r3 | ok | ok | ok |
| the gate shows keep-items' removed title-by-id line as r4 | ok | ok | ok |
| the gate shows the new capability's lines with ids r1-r6 | ok | ok | ok |
| spec/ unchanged | ok | ok | ok |

**apply** (approved drafts applied and committed alone)

| check | 1 | 2 | 3 |
|---|---|---|---|
| spec/ committed alone | ok | ok | ok |
| the commit message adds keep-items#r6, #r7, changes keep-items#r3 and removes keep-items#r4 | ok | ok | ok |
| the apply committed without restoring spec/ | ok | ok | ok |
| no line renumbered | ok | ok | ok |
| the removed line is gone, its id r4 in retired, r5 kept | ok | ok | ok |
| model check reports the removed line's scenario (v_s1 and unresolved), and it did not block the commit | ok | ok | ok |
| the drafts applied as written | ok | ok | ok |

**formulate** (with clingo)

| check | 1 | 2 | 3 |
|---|---|---|---|
| features committed | ok | ok | ok |
| every scenario not @holding has one @r<n> tag | ok | ok | ok |
| lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7 | ok | ok | ok |
| model check: no v_s1, no v_s2 | ok | ok | ok |
| model check: no v_s3 for keep-items or lend-items | ok | ok | ok |
| the removed line's scenario (keep-items r4) is removed or held | ok | ok | ok |
| the held count scenario keeps @r3 and @holding | ok | ok | ok |
| suite passes | ok | ok | ok |

**noclingo** (clingo hidden)

| check | 1 | 2 | 3 |
|---|---|---|---|
| features committed | ok | ok | ok |
| every scenario not @holding has one @r<n> tag | ok | ok | ok |
| lend-items has scenarios @r1-@r6, keep-items new ones @r3, @r6, @r7 | ok | ok | ok |
| the removed line's scenario (keep-items r4) is removed or held | ok | ok | ok |
| the held count scenario keeps @r3 and @holding | ok | ok | ok |
| suite passes | ok | ok | ok |
| the reply says model check did not run | ok | ok | ok |

**migrate** (adding ids to a repository on capability files)

| check | 1 | 2 | 3 |
|---|---|---|---|
| every line has [r<n>] from r1 in order | ok | ok | ok |
| line text otherwise unchanged | ok | ok | ok |
| capability id is <context>/keep-items, retired: [] | ok | ok | ok |
| spec/index.md's id is the context id | ok | ok | ok |
| every scenario not @holding has one @r<n> tag | ok | ok | ok |
| no @r on a Feature: line | ok | ok | ok |
| the outline tagged once | ok | ok | ok |
| the held scenario keeps @holding and takes no @r<n> | ok | ok | ok |
| features count --by-tag equals the baseline's but for r tags | ok | ok | ok |
| the suite's summary unchanged | ok | ok | ok |
| model check exits 0 (no v15a, v_s1, v_s2, v_s3, file problem) | ok | ok | ok |
| spec/ and features/ committed in one commit | ok | **FAIL** | ok |

### The one B failure

B-migrate-2 committed spec/ and features/ in two commits, `d57aa99` (spec/capabilities/keep-items.md and
spec/index.md, 'requirement ids, 4 lines numbered') and `25ab91b` (features/keep-items.feature, '... 4 scenarios
tagged'). It took Adding Ids' new-line commit path, though there was no new line. This is a wording ambiguity in
the skill, seen in 1 of 3 runs. Every other check of that run passed, `model check` included.

### A (0.18.0) under B's checks

- A-integrate: 2 of 2 all ok (7 of 7 each). 0.18.0 already kept ids that were present.
- A-formulate: 0 of 2 covered every line (6 ok, 2 FAIL each). Each missed the same two checks.
  - A-formulate-1: lend-items had scenarios r1, r2, r3, r5, r6, so `missingmass.io/demo/shelf/lend-items#r4` has no scenario (v_s3).
  - A-formulate-2: lend-items had r1, r2, r3, r4, r6, keep-items r1, r2, r3, r6, so `missingmass.io/demo/shelf/keep-items#r7` and `missingmass.io/demo/shelf/lend-items#r5` have none (v_s3).

## Cost

Mean per case, from `costs-final.txt` (three runs per B case, two per A case).

| case | B cost | B wall | A cost | A wall |
|---|---|---|---|---|
| integrate | $0.53 | 111 s | $0.50 | 105 s |
| apply | $0.20 | 32 s | | |
| formulate | $0.57 | 257 s (94 s without the long run) | $0.64 | 335 s (111 s without the long run) |
| noclingo | $0.57 | 110 s | | |
| migrate | $0.16 | 24 s | | |

Formulate had one long wall time in each version: B-formulate-1 583 s and A-formulate-2 558 s. Its cost was
in line with the others ($0.59 and $0.65), so the time went to waiting, not to work. The means above give both
with the long run and without it. A was not run on apply, noclingo or migrate.

## What the first runs showed

- The scorer was fixed four times on real gates: ids in the gate's Questions section were read as lines; the
  cost counted one result event where there are two; a new capability named `lend-books` was not the hard-coded
  name; the gate was parsed by layout, which a correct gate in another layout failed. The last fix parses the gate
  without regard to layout. B-integrate-1 to 3 were rescored after it, all ok. The harness self-test did not
  find these; real model output did.
- In `-p` mode the session waits for its background spec-round and answers afterwards. The two result events in the
  cost lines (`num_turns summed ... over 2 results`) show it.

## What the reviews caught

- **Commit-then-check order** (integrating-a-proposal step 4): the plan committed `spec/` and then ran
  `model check`; spec-integration r16 says check first. The order is apply, check, commit.
- **`model check` given paths**: the skills passed paths; the script reads the whole repository and takes none.
- **Failures not scoped to the round**: in a repository not yet on ids every scenario is `v_s1` and every line
  `v15a`, so a literal follower could never pass. Both skills now judge what the round added.
- **A removal deadlock**: a scenario placed under no line could never clear `v_s1`; an answer now leads to a new
  line or to holding it for removal.
- **A missing id in `spec/index.md`**: Adding Ids never wrote the context id there, so `model check` reported a
  file problem. Found by the harness; fixed in `4afdeda`.
- **First migration untagged**: spec-migration's lines and the skill did not tag scenarios on a first migration;
  r4, r5, r6 and r11 now allow the new `@r<n>` tags, and r11 says "nothing else in a scenario changes".
- **Hold without rebind**: a hold changes the title, so its test needs `features rebind`; the skill now says so.

## Not tested

- Task 7's self-run of the formulation text on this repository (blocked; formulated in-session instead).
- A real batch in a consuming repository, kb or shopsystem-knowledge, measured with `scripts/measure`.
- A question round-trip after ids: a formulation question going back to integration and returning as a round.
- The skills run end to end on this repository: `spec-round` with `model check` inside the round.
- Decisions as files in consuming repositories, which is not in this release.
- A harness that blocks subagents from writing reply files.

## Fix note

Added with the fixture runs: the results, cost and first-runs sections, and the opening, harness and Not tested text that said the runs were not made.

Corrected after review: the harness's ok counts are taken from selftest.out; "exactly" dropped from the mutation sentence; the unsupported "186 lines" replaced by counts of requirement lines per capability.

## Type-first ids (2026-10-17)

### What changed

- The convention: ids are `<kind>/<owner>/<product>/<context>/<name>` with the design model's kind names; short forms
  `<kind>/<name>` inside a context, and `<name>` where the field fixes the kind. Old forms are refused.
- Decision 0027 is rewritten; spec lines are reworded (r43: bare names only where the code accepts them).
- The model resolver: type-first ids, short forms, kind-named capabilities, a file-name check, and r45 reads
  `design-decision` headings.
- The teaching text: Adding Ids steps 2 and 4, and the type-first wording in the skills.
- This repository is renamed to type-first ids (a migration; no content changed).
- `revisit_signal` is a reference, read in short form.

### Reruns

Plugin B was a detached worktree of the branch at `1a7b92a`.

| Case | Run | Result | Cost |
|---|---|---|---|
| T-integrate | 1 | ok 7/7 | $0.58, 119 s |
| T-integrate | 2 | ok 7/7 | $0.53, 104 s |
| T-integrate | 3 | ok 7/7 | $0.48, 105 s |
| T-migrate | 1 | ok 13/13 | $0.18 |
| T-migrate | 2 | ok 13/13 | $0.16 |
| T-migrate | 3 | ok 13/13 | $0.18 |

Integrate passed 3/3 at 7/7 and migrate 3/3 at 13/13. In T-integrate-2 the last message answers a late background
notification, so the gate is the message before it. The one-commit check, which failed once in the 0.19.0 runs,
passed 3/3. The migrate checks now include the index id `bounded-context/missingmass.io/demo/shelf`, type-first
capability ids, and `decision/` rewritten.

### Scorer fixes

1. A bold label with trailing text is read as a label.
2. The gate is read from the last message holding `[rN]` under a label.

### kb clone trial 2

A fresh clone of shopsystem-kb at `2eed357`, git identity set on the clone.

- Session 1 ($2.09, 14 turns): numbered 371 lines, ids type-first, index `bounded-context/missingmass.io/shopsystem/kb`,
  `decision/` to `design-decision/` throughout `spec/` (154 ledger headings, 0 left). It stopped at the gate with two
  questions: a scenario fitting two lines in hand-over-content, and an outline fitting r1 and r2 in
  name-what-is-asked-for. The first trial had placed every scenario.
- The controller answered for the trial only (reading A, A: the session's recommendations, on a throwaway clone) and
  resumed. Session 2 ($2.24, 11 turns) tagged all 361 and committed `a52b712`.
- Verified by the controller: `model check` with clingo gave 10 `v_s3` only (the same 10 lines as trial 1), 0
  unresolved, 0 file problems; the suite 1603 passed, equal to the baseline; the feature diff is only `@r` tags. The
  duplicate title across two files was again tagged by hand (fix 2, `--file`, is in 0.20.0).
- Cost: $4.33 in all.

### Not tested

- A real kb migration. The trial ran on a throwaway clone with the gate answered by the controller.
- `decision/` references outside `spec/` in consuming repositories (CLAUDE.md, docs/), which the skill leaves alone.
