## Budget

- scripts/work
- scripts/workqueue_request.py
- tests/scenarios/requests_write_steps.py

## Report

Changed: `work request` takes `--delegation`; `request()` writes it as JSON-quoted frontmatter `delegation` in the same commit (absent when not given); two steps defined in requests_write_steps.py.

Red: `python3 -m pytest -q -n 0 <r19 node id>` failed: argparse "unrecognized arguments: --delegation ..." so no request kept (steps defined first, so the failure was the Then on the kept request).

Green: `python3 -m pytest -q --work-item w165` 143 passed, 1 skipped; tests/scenarios/test_requests.py passed.

Suite at start: 849 passed, 1 failed (the r19 scenario), plus the expected failures in the brief.

Size: `tools size --limit 300` printed nothing.

## Tests changed under an allowance

none

## Open questions

`--delegation ""` stored as an empty string (the reader treats it as none); `--delegation` twice keeps the last; model's reader does not unescape quoted values.

The plan contained no code.

## Outside the file set

none

Commit: 6a4244bb. Files: scripts/work, scripts/workqueue_request.py, tests/scenarios/requests_write_steps.py.
