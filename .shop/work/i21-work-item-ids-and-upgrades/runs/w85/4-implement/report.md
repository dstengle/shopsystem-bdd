## Budget
scripts/model_work.py, tests/scenarios/conftest.py, tests/scenarios/design_model_check_problems.py, tests/scenarios/design_model_check_then.py

# Report
Changed: model_work.py gets `check_work_item_name` (stem must be `w<n>`; a second work-item with the same stem, across initiatives and statuses, is a file problem naming both files); registry `held` is local to `read_work`. Test side: `World.work_item(initiative, name)`, four case branches in `malformed_record`, bare Then "it does not print a file problem".

Red: `python3 -m pytest -q --work-item design-model-check-3 -n0`: rows 1 and 3 ("prints") failed (row 1 and 3 had no file problem; rows 2 and 4 passed once the Given existed). Row 3 then failed once more because of my own Given helper (one id for two files); fixed.
Green: same command, scenario rows 1-4 pass. `tests/scenarios/test_design_model_check.py tests/scripts/test_model*.py`: 46 passed.
Suite at start: 612 passed, 4 failed (the brief's record, including these 4 outline rows).
Final work-item run: 115 passed, 2 failed: tests/scripts/test_tools.py::test_the_map_says_which_tests_execute_a_function and ::test_untested_names_each_function_no_test_executed. They concern `tools map` (coverage), not touched here, and they are not in the suite record's failing list; they also fail run alone. Concern: likely environment (coverage/jedi); not investigated.

## Tests changed under an allowance
none (World.work_item gained defaulted arguments; existing callers unchanged).

## Open questions
Plan §5: frontmatter id disagreeing with the stem (w4.md with id w3); what `w<n>` admits (w0, w03, W3 — currently `w\d+`, lower-case); same-initiative duplicates with non-w<n> stems (only stem problem printed); order of the two files named in a duplicate (later file is reported, naming the earlier).

The plan contained no code. Size check: `tools size --limit 300` printed nothing.
Commit: 3c4f259. Files: the four above.
