# Plan of w165: requests#r19, `work request --delegation`

## 1. What goes green

- **requests#r19**: scenario "request with --delegation writes the delegation given in the request"
  (`features/requests.feature`, `@r19`; `tests/scenarios/test_requests.py::test_request_with_delegation_writes_the_delegation_given_in_the_request`).
  Why it is red today (notes §1, §2): two steps have no definition, "the upstream keeps one new request" and
  "its delegation is "<text>"", and behind them the When fails anyway: the `request` subparser of `scripts/work` does
  not know `--delegation`, so argparse refuses with an error exit and keeps no request (probe A).

No deprecated scenario is retired; the work-item has no Retires section and no Rulings.

## 2. Where the change lands

The researcher's file set, unchanged:

- `scripts/work`: the `request` subparser gains an optional `--delegation` option; `cmd_request` passes it on to
  `workqueue_request.request`.
- `scripts/workqueue_request.py`: `request()` takes an optional delegation and, when one is given, writes a
  `delegation` field in the request's frontmatter, in the same text that is checked and committed now (one write,
  one `committed` call).
- `tests/scenarios/requests_write_steps.py`: defines the two missing steps, "the upstream keeps one new request"
  (exactly one request kept under the upstream, the short form of the existing longer step) and
  "its delegation is "<text>"" (the kept request's delegation, read back and decoded, equals the text).

No file is added or removed by a decision below. All three files are well under the 300-line limit (notes §7).

## 3. Decisions

1. **The delegation is written as the frontmatter field `delegation`, as one JSON-quoted string** (the text encoded
   as a JSON string, so a quote, a backslash or a newline in it stays on one line). Rests on requests#r19 ("write the
   delegation in the request") and the capability's Implementation ("`--delegation` is written as the frontmatter
   field `delegation`"); the quoted form is the one the existing reader, `supervise_answers.py`'s
   `Answers.delegation`, decodes (notes §3, row 1), and the one the supervision steps already write by hand. A raw
   value would break that reader on a quote and break the file on a newline (frontmatter ends at a line `---`).
2. **No `delegation` field at all when the option is not given.** Rests on requests#r1 (the request r1 writes is
   unchanged; probe B's frontmatter stays as it is) and r19 being a **Where** line (only where the option is given).
3. **The delegation goes through the same `request()` path**: after every existing refusal (r2, r3, missing lines
   file) and inside the one commit. Rests on requests#r2/r3 ("change nothing" on refusal) and requests#r12 (the
   change is committed); design-decision/requests-written-through-work (the asker's part is written by `work`
   only, `work request` only, requests#r4).
4. **The step "its delegation is" reads the stored field and decodes it as `Answers.delegation` does** (JSON when
   quoted), not through `model_parse.scalar`, which strips quotes without unescaping (notes §3, row 2). Rests on the
   scenario's purpose line ("as they were given") and requests#r19.
5. **Exit**: success, as the scenario's "it exits successfully" says; no exit code is named in the scenario
   (design-decision/exits-are-successful-or-errors).

## 4. Tests the decisions break

None. Verified from the notes (§4, by search, no coverage map): no test asserts that `--delegation` is refused; no
test calls `workqueue_request.request` as a function (the request tests run `work` as a subprocess with unchanged
arguments, so `test_requests.py` keeps passing); `supervision_delegation_steps.py` writes the same JSON-quoted
`delegation:` form by hand and is untouched; `design_model_check_requests.py` writes no delegation and `model
check` ignores an extra key (probe E). Decision 2 keeps every request written without the option byte-for-byte as
today, so the existing request steps' frontmatter checks hold.

## 5. Open cases

For the implementer to name in the report, not to choose here:

- `--delegation ""`: an empty delegation; would be stored as an empty quoted string, which `Answers.delegation`
  reads as no delegation (notes §2).
- `--delegation` given twice: argparse's default keeps the last; the scenarios are silent.
- A delegation with a newline, `"` or `\`: decision 1 keeps it on one line; no scenario checks the round trip.
- `model`'s frontmatter reader does not unescape a quoted value, so `model` and `work run` would read such text
  differently; `model` does not use the field today.
