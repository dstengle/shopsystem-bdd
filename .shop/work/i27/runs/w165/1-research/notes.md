# Research of w165: requests#r19, `work request --delegation`

Tools: `scripts/tools` ran (`/home/vscode/shopsystem-bdd/scripts`). No coverage map exists (`tools: no map`), so no
`tests-of` or `untested` answers; every test list below is `by search`. `tools refs workqueue_request.request` gave 0
references, which I do not trust (the caller is `scripts/work:64`, found by search). `tools size --limit 300` printed
nothing: no tracked Python file is over 300 lines.

Accepted scenario: `features/requests.feature`: "request with --delegation writes the delegation given in the request"
(`@r19`), node id `tests/scenarios/test_requests.py::test_request_with_delegation_writes_the_delegation_given_in_the_request`.

## 1. Why the scenario is red today

Command: `python3 -m pytest -q "tests/scenarios/test_requests.py::test_request_with_delegation_writes_the_delegation_given_in_the_request"` (run)

Fails with `StepDefinitionNotFoundError: Then "the upstream keeps one new request"`, line 28 of the feature. Two steps
are undefined:
- `the upstream keeps one new request` (line 28). `tests/scenarios/requests_write_steps.py:48` defines only the longer
  form, "... , whose status is open and whose turn is the upstream's".
- `its delegation is "<text>"` (line 29). No step definition anywhere in `tests/`.

The When (line 27) is defined (`requests_write_steps.py`, `the_asker_runs`), and it runs `work request ... --delegation`.
Probe A shows what that When gets today: argparse refuses the option (exit 2, `unrecognized arguments: --delegation ...`),
so no request is written (see section 2).

Code missing, by file and function:
- `scripts/work`, the `request` subparser (lines 121-126): no `--delegation` option.
- `scripts/work`, `cmd_request` (lines 63-65): does not pass a delegation.
- `scripts/workqueue_request.py`, `request()` (line 68): no delegation parameter; the frontmatter template (lines 86-88)
  has no `delegation:` line.
- `tests/scenarios/requests_write_steps.py`: two step definitions missing (above).

## 2. What the system answers today

Probes are in `.shop/scratch/w165-1-research/probe_delegation.py` and `probe_model.py`. Each run with
`python3 -m pytest -q -s <path> -n 0` (run).

Probe A, `work request "Show the queue" --from ctx-a --lines lines.md --source o1 --delegation "answer any question on line 2"` (run):
exit 2; stderr `work: error: unrecognized arguments: --delegation answer any question on line 2`; no `q1.md` kept.

Probe B, control, same without `--delegation` (run): exit 0, prints `q1`; `q1.md` frontmatter is `id`, `kind`, `asker: ctx-a`,
`source: [o1]`, `status: open`, `turn: upstream`. The commit is `work request: q1` (read of `b_control/.git/logs/HEAD`, r12).

Probe C, `--thread t1 --delegation=answer any question on line 2` (run): exit 2, unrecognized argument; nothing kept.

Probe D, `--delegation a --delegation b` (run): exit 2, unrecognized arguments; nothing kept.
The `--delegation ""` case was not run (the same argparse refusal is expected, read).

Probe E, a hand-written `q1.md` with a `delegation:` line, read by the existing readers (run):
- `scripts/model --root <dir> check --json`: returns `v17` ("a request that is part of no job-thread and cites no origin")
  with or without the delegation line (control file c_control_no_delegation gives the same). The `v17` comes from the
  scratch repo having no observation `o1`, not from the delegation. So a `delegation:` line does not change `model check`.
- `scripts/work show`: prints `q1 open upstream` with or without the line.

Read, not run: `scripts/model_requests.py:request_form` (lines 43-63) rejects no unknown frontmatter key, so a
`delegation` key is harmless to `model`. `scripts/workqueue.py:requests` (line 113) reads only `kind`, `status`, `turn`,
`source`.

Nearest cases the scenarios do not give (read, not yet runnable because the option does not exist):
- `--delegation ""`: would write an empty field. `supervise_answers.py:Answers.delegation` (line 46) returns `None`
  for an empty value, so no question is answered.
- A delegation with `"` or `\`, or a newline: see section 3, row 1.

## 3. Old assumptions

No requirement changes an existing form here; r19 adds a field. The assumption that breaks is that no real request
carries `delegation`. Places that read the field:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_answers.py:Answers.delegation` (lines 34-46) | reads frontmatter `delegation` raw from `requests/q<n>.md`; `json.loads` when the value is wrapped in `"`; `None` when absent or empty | Now real requests carry it, so `work run` starts answer sessions for them. The writer must write the JSON-quoted form (`json.dumps`) or a `"` or `\` in the text breaks this reader. A newline breaks the file (frontmatter ends at `\n---`). | none by search for a real request; hand-written delegations in `tests/scenarios/supervision_delegation_steps.py` (by search) | search: `grep "delegation"` over `scripts/` |
| `scripts/model_parse.py:scalar` (line 83) | strips outer quotes, does not unescape | Reads a JSON-quoted delegation with `\"` still escaped, so `model` and `Answers.delegation` disagree on such text. `model` does not use the field today. | none by search | read |
| `scripts/model_requests.py:request_form` (lines 43-63) | checks required keys and sections; ignores other keys | none: an extra key is accepted (probe E) | `tests/scenarios/design_model_check_requests.py` (by search) | probe E, read |
| `scripts/workqueue.py:requests` (line 113) and `scripts/work:cmd_show` | read `kind`, `status`, `turn`, `source` | none: `delegation` not read | `tests/scenarios/requests_show_steps.py` (by search) | probe E (`work show`) |
| `scripts/work:cmd_request` (lines 63-65) and the parser (line 121-126) | passes `args.asker, args.lines, args.source, args.thread` only | must pass `args.delegation` too | `tests/scenarios/test_requests.py` via subprocess (coverage not measured) | read; probe A |
| `scripts/workqueue_request.py:request` (line 68) | writes the request text: no delegation field | must write `delegation:` (JSON-quoted), in the same `committed` call | `tests/scenarios/requests_steps.py`, `requests_write_steps.py` (by search) | read |
| `scripts/supervise_brief.py`, `supervise_rounds.py` (`accepted_lines`) | read lines and outcomes only | none | by search: `tests/scenarios/supervision_*` | read |

## 4. Tests the requirement makes impossible to keep

Searched (by search; no map): `grep` of `tests/` for `--delegation`, `unrecognized`, `workqueue_request.request`,
`cmd_request`, and `delegation`. Found:
- No test asserts that `--delegation` is refused. Nothing to break.
- No test calls `workqueue_request.request` as a function; the request tests run `work` as a subprocess. Their argument
  lists are unchanged, so `test_requests.py` (r1-r3, r4-r16) keeps passing if the option is added.
- `tests/scenarios/supervision_delegation_steps.py` and `test_supervision.py` write a `delegation:` line by hand
  (`'delegation: "%s"'`, line 19). They use the JSON-quoted form and keep passing.
- `tests/scenarios/design_model_check_requests.py` writes requests without `delegation`; keeps passing (probe E).
None that the requirement makes impossible to keep. What I verified: the quoted-form assumption (above) and that
`model check` ignores extra keys.

## 5. A step the work-item skips

The new path is not a separate path: `--delegation` has to go through `workqueue_request.request()`, the same function
that does every check and the commit. The steps the existing way takes, all in `request()`:
- refusal, no origin and no job-thread (`workqueue_request.py:74-75`): read; the scenario r3 is probed by the suite.
- refusal, missing lines file (lines 76-77): read.
- refusal, line not in strict form (lines 78-81): read.
- write under `.shop/work/requests/` with `mkdir` (lines 89-93), committed through `workqueue.committed` (line 94):
  probe B's `.git/logs/HEAD` shows the commit (run).
If the delegation is written by a second write, or after `committed`, its frontmatter would not be committed (r12).
Also a delegation is not checked for a newline (the request's title is not checked either; `workqueue.add` refuses a
newline in its title, `workqueue.py:82`), so a plan must make the writer one line, e.g. `json.dumps`.

## 6. Defects

None shown by the probes. Probe A-D are refusals of the missing option (the red itself), not a wrong acceptance.

## 7. The file set

Production:
- `scripts/work` (150 lines; room 150): add `--delegation` to the `request` subparser (line 126) and pass it in `cmd_request` (line 64). Found by search and read.
- `scripts/workqueue_request.py` (142 lines; room 158): `request()` takes the delegation and writes `delegation:` JSON-quoted in the frontmatter (lines 68, 86-88). Read.

Tests:
- `tests/scenarios/requests_write_steps.py` (108 lines; room 192): define `the upstream keeps one new request` and `its delegation is "<text>"`. Found by run (the undefined steps).

Not changed, on the path, read:
- `scripts/workqueue.py` (290; room 10): `committed`, `read`, `requests`.
- `scripts/model_parse.py` (271; room 29): frontmatter reader.
- `scripts/supervise_answers.py` (128; room 172): reads the field.
- `scripts/model_requests.py` (63; room 237): reads the request form.
- `tests/scenarios/requests_steps.py` (108; room 192): `sections`, `request_rel` used by the new steps.
- `tests/scenarios/test_requests.py` (9; room 291): binds the feature; no change.

Recorded by probes: scratch probes are in `.shop/scratch/w165-1-research/`, ignored by git (`git status --porcelain` is empty).
