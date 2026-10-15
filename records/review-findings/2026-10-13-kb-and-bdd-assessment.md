---
id: review-finding/2026-10-13-kb-and-bdd-assessment
kind: review-finding
about: shopsystem-bdd
date: 2026-10-13
---

# kb and shopsystem-bdd: the spec, the work, and the cost

Date: 2026-10-13
Read: shopsystem-bdd at 0.18.0 (e3c846d), shopsystem-kb at 0.9.0 (2eed357),
plus the four kb batch facts files (32–35) kept in the plugin repo. Every
number below is from those files or from git; none is estimated.

## Summary

The spec layer works. `spec/capabilities/*.md` is the format we settled in
September — EARS lines, `rests_on`, `Not yet` with triggers — and on kb it
holds 21 capabilities, 361 scenarios, 154 decisions, 31 ADRs, and a suite
at 1603 passed with zero expected failures. Spec commits name their
motivation. That part answers "what is this meant to do" well.

The three things you asked about are each a gap in a different layer:

| ask | state | where the gap is |
|---|---|---|
| current vs intended state | the spec describes the present and nothing marks it as such; the future lives in a request file, 97 delegation rulings and a 160-line backlog | `spec/index.md` has no "now / next"; approved-but-unbuilt was handled by branches and a revert, not by the spec |
| what work is going on and why | a slice reaches its capability in three hops by scenario *title*; 93 of 276 slices are enabling slices tied to a `Check:`, not to any line; reports, findings and scout notes are git-ignored | nothing in the build layer names a capability |
| efficiency | closing (review + fix) is 38–44% of agent time while 7 of 17 task reviews came back clean; the controller session reads up to 55% of a batch's cache tokens; `Lands:` was wrong in 15 of 23 slices; no batch has been measured on any of the last six plugin versions | the rulebook grew by scar, and the loop that was meant to prune it hasn't closed since 0.12.0 |

The structural finding is the one you half-named in your message: the
workflow has been built the way your product-ops system was. 1,348 lines of
instruction, 86 rationalization rows, 51 red flags, each added after one
batch or one fixture run showed a problem, and no rule has been removed.
The plugin measures itself (0.12.0) but doesn't specify itself: its "spec"
is ten dated design notes and a changelog. Section 4 is the recommendation
that follows from that; sections 1–3 are the specific fixes, and 6 is an
order to take them in.

---

## 1. The specification: current and intended state

### What works

- A capability file is a complete statement of present behaviour. Lines are
  present tense, observable, one scenario each. `Not yet` is the only
  "unbuilt" marker, and every entry has a promotion trigger.
- `decisions.md` is append-only, 154 entries, 23 with `revisit_when`, 31
  with `supersedes`, every one with a `source`. The contract's version
  history is readable as a chain: `contract-v1` → `published-contract-v1`
  → `-in-0-6-0` → `-in-0-7-0` → `contract-v2` → `published-contract-v2`.
- 27 of 42 spec commits say "lines approved <date> under the person's
  delegation"; 7 cite a review, 6 a formulation question, 3 a request, 4 a
  design note. The motivation-on-commit convention is in place.
- ADRs are the person's decisions (0022–0031 all end "The user's
  decision"); `decisions.md` is everything a line rests on, the
  controller's rulings included. That division is right and stated in
  `adrs/README.md`.

### Gaps

**Nothing says the spec is the present.** On the `v0.9.0` tag every line is
built, but a reader learns that from `git tag`, the living plan's "No slice
is open", and `tests/slices.py`'s xfail rule in `CLAUDE.md`. The 0.8.0
release had to *revert* 24 files of approved K2/K3 lines from `main`
because main's code didn't hold them: the spec and the code travelled
together on a branch, which is consistent, but the convention is nowhere
written.

**`Order of building` is finished work in future tense.** "Three changes
follow, built in order … Then, for portable knowledge: K1 … K2 … K3" — all
shipped. And "every kb scenario cites the shop-knowledge scenario that
needs it" — 0 of 361 scenarios do (and per September, they shouldn't).

**The future has no home.** What's next lives in: the request file (fully
consumed), the delegation file's 47 open spec questions, the backlog's 5
open `RELEASE GATE` lines and 3 `FOR THE PERSON` lines, and 41 `QUESTION
FOR THE SPEC` log entries. Nobody arriving cold would find them.

**Version is a parenthetical.** "(until v1 `Write`)", "`Export` is an rpc of
`kb.v2`" — a line's version appears only where a name changed. No line says
when it arrived or which request brought it.

### Recommendations

1. **A state header on `spec/index.md`**, four lines: the release, the
   contract package, the suite record, and the convention — "every
   Behaviour line on `main` is built; what is approved and unbuilt lives on
   its release branch with its code, and under `Not yet` here." That's the
   whole fix for "what does it do now."
2. **`Order of building` becomes history or goes.** What it holds is the
   September partnership story and three finished phases. Move it to a
   `docs/history.md` or cut it to one paragraph; the live order belongs in
   the plan.
3. **A `## Next` section**, kept short, in the living plan's head (not the
   spec): the open requests, the release gates waiting on the person, and
   the one or two capabilities the next batch touches. It is the answer to
   "what is being built this week and why," and it's currently
   reconstructable only from four files.
4. **Triage the backlog out of the living plan.** 160 bullets of review
   findings is not a plan; it's where findings go to be forgotten. Split:
   spec questions → one short `FOR THE PERSON` list; hardening with repro →
   `docs/backlog.md`, out of the plan; stale → drop. The living plan then
   holds open slices, the log since the last archive, and `Next`.
5. **Don't mark lines with status or version.** That's the ledger kb
   explicitly deferred (`a-scenario-status-ledger-can-wait`), and the
   branch convention plus the xfail plugin already carry it. A `since:`
   per line would be the start of the overweight spec.

---

## 2. The work and its relation to the spec

### What's visible today

| artifact | shows | tied to the spec by |
|---|---|---|
| feature file | scenarios, `@slice-n`, `@holding` | `# formulated from`; title restates the line (text) |
| living plan | open slices, status, `Lands:`, unknowns, log | slice → scenario titles → feature → capability, three hops by text |
| batch plan | tasks, decisions citing line or ledger, tests the decisions break | decision ids; scenario titles; (batch 33 quoted lines verbatim, batch 39 stopped) |
| archive | green slices and the batch's log | slice numbers |
| facts file | cost per dispatch, by slice | slice numbers |
| reports, findings, scout notes | the reasoning of each dispatch | **git-ignored; gone after the batch** |

Enabling slices — 93 of 276 — carry a `Check:` and no scenario, so a test
seam, a module split, a migrate or contract slice has no path to the line
that caused it. The scout's notes that say which modules a slice changes
are discarded; the plan keeps the count. `measure` attributes by slice, so
"what did the export capability cost" is unanswerable.

### The delegation finding

In two days (10-10, 10-11) the controller took 97 rulings and raised 47
spec questions the person had not seen, and wrote Behaviour lines "under
the person's delegation" on the small-change path. The single human gate
on lines is sound, but at that volume it's being passed line by line in a
log the person reads afterwards. The delegation file was the right
instinct, done by hand once.

### Recommendations

6. **One field on a slice: `Capability:`.** Capability slices name theirs;
   enabling slices name the capability slice they enable (`For: slice
   171`). That one field gives the archive, the facts file and `measure`
   the join to the spec, and makes "the export capability cost N tokens
   over 4 batches" a query.
7. **Keep the findings files.** The branch review's findings and each
   task review's are small; archive them beside the batch's plan instead
   of ignoring them. They're the only record of *why* a backlog line
   exists, and the backlog is where defects currently go to lose their
   context.
8. **The spec delta is the archive's first section.** When a batch closes,
   the lines added, changed and removed under delegation — a list, with
   the ruling each rests on — goes at the head of the archive file. The
   delegation file is that, done once by hand; make it what `plan archive`
   writes. Then the gate is per batch as a reviewable list, not per line
   in a log.
9. **Commit messages carry the slice and the capability.** Spec commits
   already name their motivation; code commits name a slice ("Slice 183
   step 2: …"). Add the capability to the checkpoint commit and the trace
   from `git blame` to a line is two hops, both by id.

---

## 3. Efficiency

### The numbers (kb batches 32–35, plugin 0.10.0/0.11.0)

| | 32 | 33 | 34 | 35 |
|---|---|---|---|---|
| slices / dispatches | 7 / 26 | 11 / 31 | 5 / 11 | 3 / 8 |
| wall span / agent-minutes | 180 / 112 | 105 / 135 | 51 / 50 | 35 / 37 |
| output / cache-read tokens | 0.79M / 115M | 0.86M / 75M | 0.26M / 33M | 0.23M / 29M |
| controller's share of cache reads | 23% | 42% | 55% | 53% |
| closing share of agent time (review + fix) | 20% | 38% | 42% | 44% |
| task reviews, clean | 5, 2 | 8, 4 | 1, 1 | 3, 1 |
| hand-backs | 0 | 2 | 1 | 1 |

What stands out:

- **The controller is the cost centre.** Its context went 412k → 585k
  across one session that ran four batches; by batch 34 it read more
  cache than every agent together. Batch 32's span (180 min) exceeds its
  agent-minutes (112) — the controller's own 96 turns at ~250–550k
  context are the wall-time cost. "One batch, one session" (0.13.0) is the
  fix, and it is asked, not structural.
- **Closing has grown to nearly half.** Per-task review on Opus is the
  largest line after implementation, and 7 of 17 came back clean. The
  branch review found Important issues all three times it ran.
- **Every hand-back was the test-listing rule catching its own omission**
  (4 of 4). The hand-back-to-formulation path — the design's original
  purpose — fired zero times in four batches. Zero tests were deleted,
  which is the rule's point and worth the 5–8 minutes each.
- **`Lands:` was exceeded in 15 of 23 slices** and cost ~790k tokens of
  sizing scouts. What actually bounded dispatches was the written
  dispatch budget (held 13 of 14) and Steps — not the number.
- **Policy didn't hold.** Implementers ran Opus 32 of 42 times against
  "Sonnet by default"; every implementer dispatch shows two prompts under
  a rule of fresh agents; 0 lanes ran.
- **Instruction dwarfs intent.** An implementer starts at 29k tokens, of
  which the brief is ~900. The rest is `bdd-implementer.md` +
  `bdd-red-green` + `CLAUDE.md`.
- **The loop hasn't closed.** 0.13 through 0.18 — six releases — have
  fixture evidence only. No kb batch has run on any of them with a facts
  file. The rule "one change per release, measured on a batch" is the
  best rule in the plugin and it hasn't been applied to itself.

### Token cost vs wall time

The two aren't in tension here; the same three things dominate both. The
serial chain per slice is scout → implement → review → fix → re-review;
removing the default task review cuts two to three serial dispatches per
slice and the Opus tokens they spend. The controller's turns are both the
largest cache-read share and the gap between span and agent-minutes.
Lanes, the one wall-time-only mechanism, never ran, and the planner is
told they're rare. Real parallelism that exists: scouts in one message,
reviews by area.

### Recommendations, in order of return

10. **Run one batch on 0.18.0 and measure it before changing anything.**
    Six versions of unmeasured rules is the biggest unknown in the system.
    The next batch is the baseline for everything below.
11. **Make the controller a per-batch agent.** 0.18.0 already found the
    pattern for the spec phase: `spec-round` runs one round and ends, so
    the gate-keeping session stays flat. Apply it to the build: a
    `batch-round` (or per-slice) agent that runs implement → review → fix
    and replies one line. The session the person talks to then holds the
    gate and the plan and nothing else. Watch: controller cache reads and
    peak context; span minus agent-minutes.
12. **Per-task review only on the named risks, and enforce it.** The rule
    already says contract, concurrency, data integrity, stored data; batch
    33 reviewed 8 of 11 tasks. Default to batch-end; keep the branch
    review, the fix wave, and the dry-run invariant. Watch: closing share,
    defects found at branch review that a task review would have caught.
13. **`Lands:` from a refusal to an estimate.** Log it, don't refuse on it;
    keep the dispatch budget and Steps, which held. Drop the sizing scouts
    for slices not in the next batch. Watch: tokens on scouts; max files
    per dispatch.
14. **Cut the instruction a dispatch carries.** Move the rationalization
    and red-flag tables out of the SKILL.md files into `docs/lessons.md`,
    not loaded at dispatch: they are notes for the author, each from one
    run, and a model reading 35 of them performs worse, not better. Keep
    the process steps and the stop conditions. Watch: starting context,
    hand-backs (should not rise).
15. **Enforce model policy in the dispatch, not the plan.** The `Model:`
    line is advice to a controller that ignored it 32 of 42 times. If
    Sonnet is the default, the agent definition is the place.

---

## 4. The shape of the problem

The plugin is the product-ops system again, in the "how" layer. Each
version answers one measured failure with a mechanism; mechanisms
accumulate; none is removed; the instruction mass is now ten times the
intent it carries. That is exactly what the September method was designed
to prevent in a spec, and the plugin has no spec in that form. Its
behaviour is specified in ten design notes and a changelog, and its
decisions have no `revisit_when`.

The recommendation is to give the workflow the same treatment kb got:

- **A `spec/` for the plugin**, capabilities by narrator — the person at
  the gate, the controller, the implementer, the reviewer, the scout —
  with Behaviour in EARS lines, `Implementation, may change` holding the
  mechanism, and `Not yet` with triggers. The README's version sections
  are the proposals; the design notes are their argument.
- **Every rule becomes a decision with `revisit_when`**, naming the
  measurement that would retire it. "Lands ≤ 8/4: revisit when the probe
  is wrong in more than half of slices" would already have fired.
  "Per-task review on Opus: revisit when more than half come back clean"
  would have fired in batch 33.
- **The rationalization tables are the `revisit_when` ledger**, not
  dispatch instructions. Each row was a scar; recorded as a decision with
  its trigger, it can be retired when the trigger fires the other way.
- **One change per release stays, with one addition: removals count.**
  The next six releases should each remove a rule and measure, the way
  0.9–0.12 each added one and measured.

This isn't a rewrite; the material is all there. It's the migration the
plugin already did for kb (`migrating-to-capabilities`), applied to
itself, and it would make "is this how I want work run" a question with
a measurable answer per rule rather than a feeling about the whole.

---

## 5. What to keep

These are earning their place and shouldn't be touched while the rest is
pruned:

- The spec/feature pairing by name, the gate on Behaviour lines, and
  `formulated from`.
- `hold`/`retire`/`bindings`/`rebind` and the slice-expectations plugin: a
  green suite between slices with planned work as expected failure.
- The suite record per commit.
- "Tests the decisions break" and the `BLOCKED` stop: four batches, zero
  deleted tests.
- No-code plans; decisions cited by line or ledger entry.
- `measure`, and the rule that an experiment is a release.
- The branch review and the dry-run invariant.
- ADRs as the person's decisions; `decisions.md` as the ledger; motivation
  on spec commits.
- The request file and the delegation file as forms — the latter should
  become what the archive writes (rec. 8).

---

## 6. Order

Each step is one batch and one measurement.

| step | do | measure |
|---|---|---|
| 1 | state header + `Next` on kb; backlog triaged (recs 1–4) | none needed; a cold read of `index.md` and the plan head |
| 2 | run the next kb batch on 0.18.0 unchanged; commit its facts | the baseline |
| 3 | per-batch controller agent (rec. 11) | controller cache share; span − agent-min |
| 4 | review by risk enforced; `Lands:` demoted (recs 12, 13) | closing share; scout tokens; defects at branch review |
| 5 | instruction out of dispatch; model policy in agents (recs 14, 15) | starting context; hand-backs; model actually used |
| 6 | `Capability:` on slices; findings archived; spec delta in the archive (recs 6–9) | a trace from a facts row to a line, by id |
| 7 | the plugin's own `spec/`, rules as decisions with `revisit_when` (§4) | the next removal has a trigger that fired |

Steps 1 and 6 are bookkeeping and can go in any batch. Steps 3–5 are the
efficiency work, one per batch so each has a number. Step 7 is what keeps
the next six versions from reproducing the last six.
