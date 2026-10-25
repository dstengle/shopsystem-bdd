## Budget
tests/scenarios/supervision_integrate_steps.py

## Changes
Continuation: the earlier commits (0bd4ae49 and before) already made w181's scenarios pass. The merge failed on the r92 scenario (w167's), because its fixture named capability `other`, which r107 (w181) now rejects as unknown. The Given step `integrate_with_changes` now also writes and commits spec/capabilities/other.md.

## Runs
- Suite record: 879 passed, 2 failed at 0bd4ae49 (the r92 scenario and the gate "no question" scenario, since accepted by w184).
- Red: the r92 scenario failed at supervision_integrate_steps.py:146 ("named other, which neither spec/capabilities/ nor its drafts have"), expected: r107 is in force.
- Green: `--work-item w167` 2 passed; `--work-item w181` 148 passed, 1 skipped; tests/scenarios/test_supervision.py 6 passed.
- tools size --limit 300: prints nothing.

## Tests changed under an allowance
- tests/scenarios/supervision_integrate_steps.py, integrate_with_changes (the r92 scenario's Given): setup. It adds a spec/capabilities/other.md, with no assertion changed.

## Open questions
none

## Other
The plan contained no code that I pasted. Files changed: the one above. No concerns.
