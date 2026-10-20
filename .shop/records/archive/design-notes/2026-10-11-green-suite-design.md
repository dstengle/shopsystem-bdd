---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-green-suite-design
kind: decision-argument
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Green Suite Design

Date: 2026-10-11
Status: Written while the person was away, at their instruction; not read by them. Unreleased, on branch
`0.14.0-green-suite`, stacked on 0.13.0.
Release: 0.14.0
Request: `docs/superpowers/requests/2026-10-11-predictable-batches-and-analysis-tools.md`, section C
Baseline: `docs/superpowers/testing/2026-10-11-kb-baseline/`

## Purpose

Between slices the suite passes, and a failure means something broke. Behaviour that is still in the code stays
tested until a slice makes it untrue.

## Evidence

- kb's suite ran the whole release at "N passed, about 90 failed". Every suite record in the baseline carries a
  failing list ("the scenarios tagged slice-161 onward, and test_the_rule_names…"), and "nothing new fails" was a
  comparison of names, made by each implementer.
- Re-wording a scenario whose slice is in the future removed its test: slice 165.5 turned `kb import
  --skip-errors` from landing what it could to refusing, with no test red, because the import's scenarios were
  tagged slice 184 and unbound.
- One re-titled scenario merged at the start of batch 35 stopped `tests/test_remove_an_artifact.py` collecting, 32
  errors, because a `@scenario` binding named the old title.
- kb binds most scenarios by title, `@scenario(FEATURE, "<title>")`, in 13 test modules.

## Changes

### 1. Scenarios of unbuilt slices are expected to fail, strictly

New `scripts/slice_expectations.py`, a pytest plugin; `scripts/features plugin <directory>` writes it into a
repository and says how its conftest registers it.

- A test carrying the marker `slice-<n>` is marked `xfail(strict=True)` while the living plan gives slice n the
  Status `planned` or `blocked`. pytest-bdd makes the marker from the `@slice-<n>` tag; a plain test that waits
  for a slice takes the same marker.
- A slice that is `in progress`, `green`, or gone from the plan with its batch's archive is run as it is.
- `--slice <n>` names a slice being built: its tests are run as they are. The implementer gives it on every run of
  its slice, so red is red and green is green, and gives it or sets the Status green for the run that makes the
  record.
- A test of an unbuilt slice that passes fails the suite, `XPASS(strict)`: something built it early, or it does not
  test what its tag says. That is bdd-red-green's first stop condition, seen suite-wide.
- The suite record becomes `Suite: <N> passed, <M> failed, <X> expected at <hash> in <s> s`. M is 0 between slices.
- Slicing checks for it as it checks the suite is fast: a record whose failures are scenarios of unbuilt slices, in
  a project with no `--slice` option, makes the plugin the batch's first enabling slice.

The plugin reads the plan's `## Slice <n>:` heads and `- Status:` lines itself, so it needs nothing from the
plugin's directory at run time. It is a copy in the repository; `features plugin` writes it again.

### 2. A scenario that passes today is held, not removed

`scripts/features`: `hold`, `retire`, `holding`. `skills/formulating-features`, step 4.

- When a line is re-worded or removed and its scenario passes today, formulation holds the old scenario where it
  is, in the feature file: it gains the tag `@holding`, " (held)" at the end of its title, and a description line
  `Held for: <the title that replaces it>` or `Held for: removal`. Its steps do not change, so its step definitions
  still bind and it still passes. The new scenario is spliced in after it.
- Whether it passes is a run of that one scenario, not a reading. A scenario that fails or was never bound is
  replaced or removed as before.
- A held scenario formulates no line and is left out of the one-to-one coverage check.
- `features holding` lists each held scenario, what it is held for, and the slice tag its replacement carries.
  Slicing gives every one a slice that retires it: the slice of its replacement, or for a removal the slice that
  removes the behaviour, cut as an enabling slice when none does.
- A task carries `Retires:`. The implementer runs `features retire "<title> (held)"` in the commit that turns the
  replacement green, and removes the binding and the step definitions nothing else uses. `retire` refuses a
  scenario not tagged `@holding`. This is the one change an implementer makes to a feature file.

The request asked whether a held copy lives in the feature file or beside it. In the file: its binding and its
steps need no new path, and one command each holds and retires it.

### 3. A changed title never breaks collection

`scripts/features`: `bindings`, `rebind`.

- `features bindings` reads the test modules and reports every `scenario(<feature>, "<title>")` call whose title no
  feature file has. Formulation runs it before it commits; the branch reviewer runs it.
- `features rebind "<old>" "<new>"` rewrites the title in those calls and nothing else. Formulation uses it when it
  holds a scenario (to the held title) and when it re-titles one that never passed.
- Formulation commits the feature files and the rebound test files together.

### 4. The rest follows

- `bdd-red-green`: runs carry `--slice <n>`; the record's form; `features retire` as the one feature-file change;
  `XPASS(strict)` among the stop conditions.
- `bdd-implementer`: the same, briefly.
- `bdd-task-reviewer`: a feature file changed other than by a listed retirement is Critical.
- `bdd-branch-reviewer`: feature files change by formulated scenarios, slice tags, and holds and listed
  retirements; `features holding` and `features bindings` are run; a held scenario whose replacement's slice is
  green is a finding.

## Not yet

- **"A guard needs a test behind it."** The request's fourth point under C: a task may say "a test that breaks is
  `BLOCKED`" about a behaviour only when a passing test executes it. That needs the coverage map, and comes with
  the analysis tools in 0.15.0.
- **Languages and runners other than pytest.** The plugin is pytest's. `bindings` and `rebind` read Python.
- **A binding whose title is not a plain string in the call**, or whose scenarios are bound by
  `scenarios("<file>")`: the first is not read; the second needs no rebinding, since it binds whatever is there.

## What should move

On a batch of kb run on this version, in the facts and the plan: every suite record `0 failed` at a slice's
checkpoint; no hand-back and no finding of the kind "regression with no red" (a behaviour changed while its
scenario was unbound); no collection error in a record.

## Verification

- **Scripts:** unit tests for `hold`, `retire`, `holding`, `bindings`, `rebind`, and for the pytest plugin run
  under a real pytest: a planned slice expected, an early pass failing, a blocked slice, an archived one, `--slice`,
  no plan.
- **Against pytest-bdd:** the plugin registered in a generated project; a held scenario still bound and passing;
  retire.
- **Formulation,** headless on a fixture (`/home/vscode/scratch/shopsystem-bdd/green/`): one line re-worded and one
  removed, both scenarios passing and bound by title. Before: the old scenarios are replaced and removed, and the
  test module stops collecting. After: both held and rebound, the suite passes, `features bindings` is clean.
