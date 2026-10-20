---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-green-suite-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Green suite: test log (0.14.0)

Spec: `docs/superpowers/specs/2026-10-11-green-suite-design.md`.

## Scripts

`python3 -m unittest discover -s tests/scripts`: 84 OK, 14 new in `test_features.py`.

- `hold`, `retire`, `holding`: a held scenario differs from the original by its tag, " (held)" and the `Held for:`
  line and by nothing else; a scenario with no tags; one held already refused; a replacement not yet written shown
  as such by `holding`; `retire` refusing a scenario not tagged `@holding` and leaving the file as it was.
- `bindings`, `rebind`: a title given as a string and a feature given as a module constant; a binding that names a
  title of another feature file; the title rewritten and no other byte of the test module changed; a module that
  does not parse refused by name.
- The pytest plugin, under a real pytest: a `planned` slice's test `xfailed`; a `blocked` slice's test that passes
  failing as `[XPASS(strict)] slice 4.1 is blocked`; `in progress`, archived and untagged tests run as they are;
  `--slice`, given twice and with the `slice-` prefix; no plan found, said in the summary.

Against pytest-bdd, in a generated project whose `tests/` is a package: registered with
`from .slice_expectations import *` in `tests/conftest.py`; the suite `3 passed, 1 xfailed`; with `--slice 3`,
`1 failed, 3 passed`; a held scenario still bound through `scenarios()` and passing with its `Held for:` line.

The first registration tried, `pytest_plugins = ["slice_expectations"]`, failed to import in that layout. `features
plugin` now prints the import line for the directory it wrote into, with or without `__init__.py`.

## Formulation: a re-worded line and a removed one

Fixture `/home/vscode/scratch/shopsystem-bdd/green/` (`make_green.py`, `run.sh`): a capability with three lines,
three scenarios bound by `@scenario(FEATURE, "<title>")`, all passing. The last commit re-words the slug line and
removes the line about emptying the shelf. Headless, Sonnet: use formulating-features' small-change path, commit,
stop.

| | feature file | suite after | `features bindings` |
|---|---|---|---|
| 0.13.0, 2 runs | the slug scenario replaced, the emptying scenario removed | `1 error`: the module does not collect | 2 bindings name no scenario |
| 0.14.0, 3 runs | both old scenarios held, the new one after the first | `3 passed` | clean |

Every 0.14.0 run made the same change: two `hold`s, two `rebind`s, the feature file and `tests/test_keep_items.py`
in one commit (16 and 4 lines). `features holding` then gives the slug scenario as held for its replacement, "no
slice yet", and the emptying scenario as held for removal.

## The implementer: `--slice`, and a retirement

From one of those results: the plugin registered, the replacement tagged `@slice-3` and bound, slice 3 planned,
and a brief with `Retires:` naming the held slug scenario. The suite at the start: `3 passed, 1 xfailed`. Two runs.

Both: the change and the retirement in one commit (`features retire`, the held scenario's binding removed with
it), then the checkpoint; `--slice 3` on the runs; the suite `3 passed`, the record `Suite: 3 passed, 0 failed at
<hash>`; `features bindings` clean; the scenario held for removal untouched.

## Not tested

- Slicing giving a held scenario a slice, a `Retires:` line written by a planner, and the enabling slice that
  installs the plugin.
- Both reviewers' new lines (a feature file changed other than by a listed retirement; a held scenario left after
  its replacement's slice went green).
- A scenario outline held, and a scenario held twice over (re-worded again before its slice).
- The plugin on kb. kb's conftest registers the slice markers itself and its failing list includes one plain test,
  which would need its slice's marker.
