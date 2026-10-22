# Structured output for query commands (0.23.0, part 2)

Source: the person, during 0.22.0: a query command's result should be structured output that can be checked
explicitly; JSON is not required. The person approved this scope on 2026-10-22 and delegated the drafting decisions
to the coordinator's recommendations; each reading below is listed on the release gate.

## The decision

A new decision supersedes 0055 (exits-are-successful-or-errors) and keeps all of it, adding: a query command
answers in its output, and its exit says only whether it could answer. A query that finds nothing has answered: it
prints an empty result and exits successfully. It exits with an error only when it cannot answer (a missing map, a
missing tool, an argument it cannot read). Where `--json` is given, a query command prints its whole result as one
JSON object, and without it prints text as today, so the skills that read the text keep working.

`--json` is chosen over a `--format` option because `model check --json` (design-model-check r33) already gives
this repository its form, and JSON is the one structured form needed.

## The query commands

Each of these gets one line: where `--json` is given, the command prints its result as one JSON object. The keys
are Implementation.

- `tools tests-of` (the tests, their count, the map's commit), `tools untested` (the functions, their count, the
  map's commit), `tools refs` (the references and the summary), `tools map` (the map's commit and test count);
- `features list` (the scenarios, file and title each), `features deprecated` (each deprecated scenario, what it is
  deprecated for and its replacement), `features bindings` (the bindings it found wrong or, with `--unbound`, the
  scenarios bound by no test or by two);
- `model why` (the requirement's text and the proposals that trace it), `model rules` (each rule's code, label and
  kind);
- `work show` (each work-item with its initiative and status).

## Exits that change

Under the decision, these lines no longer exit with an error on an empty answer; they exit successfully, printing
the empty result:

- analysis-tools r11: no test in the map executed the target of `tools tests-of` (a file with no function by that
  name stays an error: the target cannot be read);
- feature-file-tools r7: `features list` matches no scenario;
- design-model-check r17: no capability-proposal adds or changes the requirement given to `model why`.
