# implement of w125

Work-item: .shop/work/i24-requests-and-the-context-loop/w125.md
Agent: bdd-implementer
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: f890f2f134c30ab6fe6c80036cfd0d3e207e7d7d
Worktree: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125
Branch: work/w125
Work-item branch: work/w125
Suite record: Suite: 760 passed, 13 failed at 15a08fa in 20 s; failing: tests/scenarios/test_batch_measurement.py::test_an_initiative_that_fulfils_no_request_is_measured_without_a_requests_origin, tests/scenarios/test_design_model_check.py::test_model_reads_the_repositorys_files_under_its_root[.shop/work/requests/q1.md-with --root naming that directory-include], tests/scenarios/test_batch_measurement.py::test_the_request_an_initiative_fulfils_is_given_as_origin_when_its_asker_is_asker[this bounded context-internal], tests/scenarios/test_batch_measurement.py::test_the_request_an_initiative_fulfils_is_given_as_origin_when_its_asker_is_asker[another bounded context-external], tests/scenarios/test_design_model_check.py::test_an_initiative_dated_after_20261023_that_fulfils_no_request_is_v16a, tests/scenarios/test_design_model_check.py::test_an_initiative_of_kind_job_or_jobpath_is_a_file_problem[job-path-prints], tests/scenarios/test_design_model_check.py::test_a_delivered_request_whose_initiative_is_not_done_is_v_d3, tests/scenarios/test_design_model_check.py::test_an_initiative_of_kind_job_or_jobpath_is_a_file_problem[capability-change-does not print], tests/scenarios/test_design_model_check.py::test_a_request_that_is_part_of_no_jobthread_and_cites_no_origin_is_v17, tests/scenarios/test_design_model_check.py::test_a_delivered_request_whose_resolution_names_a_requirement_the_spec_does_not_have_is_v3, tests/scenarios/test_design_model_check.py::test_a_request_not_of_the_form_work_request_writes_is_a_file_problem, tests/scenarios/test_design_model_check.py::test_an_initiative_of_kind_job_or_jobpath_is_a_file_problem[job-prints], tests/scenarios/test_work_queue.py::test_start_on_an_accepted_request_writes_a_proposed_capabilitychange_initiative_that_fulfils_it_sourced_from_its_origins_and_prints_its_id

Read (paths in your worktree):
- .shop/work/i24-requests-and-the-context-loop/w125.md
- spec/capabilities/supervision.md
- .shop/work/i24-requests-and-the-context-loop/runs/w125/1-research
- .shop/work/i24-requests-and-the-context-loop/runs/w125/2-plan

Run directory: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125/.shop/scratch/3-implement
Result file: /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125/.shop/scratch/3-implement/result.json

You start in your worktree, /tmp/work-run-i24-requests-and-the-context-loop-_5ujkx2k/w125: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write the result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings), so that a session that stops part-way still leaves a result, and one that does not claim the work done. Write your notes, plan, report or findings in the run directory.
