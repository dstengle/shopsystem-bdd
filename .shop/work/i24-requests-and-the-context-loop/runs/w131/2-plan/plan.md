# Plan of w131: model reads requests, their file form, and an initiative of kind job

Work-item `.shop/work/i24-requests-and-the-context-loop/w131.md`, under design-model-check, accepts r19, r112, r118.
From the research notes `runs/w131/1-research/notes.md`.

## 1. What goes green

- **design-model-check#r19**, "model reads the repository's files under its root" (outline, 14 rows). Red today
  because the row `.shop/work/requests/q1.md ... include` hits a KeyError in the step data's files-read table
  (`tests/scenarios/design_model_check_reading.py`, which has no entry or marker for a request). Behind that,
  `Model.read` has no request reader, and `read_work` treats `.shop/work/requests/` as an initiative folder. The
  other 13 rows pass.
- **design-model-check#r112**, "a request not of the form `work request` writes is a file problem". Red because the
  Givens "a request in .shop/work/requests/q1.md with no asker" and "... that `work request` wrote" are not defined.
  Today's code also prints only `.shop/work/requests: no initiative.md`, which names no request file.
- **design-model-check#r118**, "an initiative of kind job or job-path is a file problem" (3 rows). Red because the
  Given "a repository with an initiative in .shop/work/i1/initiative.md of kind <kind>" is not defined, and
  `read_work` writes the `ikind` fact for any kind without a file problem. The capability-change row already gets
  what it expects from today's code.
- **Retired**: "model reads the repository's files under its root (deprecated)",
  `features/design-model-check.feature` lines 126-149. It passes today. It is removed along with its 14 test cases.

## 2. Where the change lands

- `scripts/model_work.py`: `read_work` skips the `requests/` directory when it collects initiative folders. This
  also fixes defect D1, where an empty `requests/` was refused with "no initiative.md". An initiative whose kind
  is `job` or `job-path` gets a file problem that names its `initiative.md` (r118).
- `scripts/model_facts.py`: `request` joins `KINDS`, so `request/<context path>/q<n>` ids are read with their kind.
  `Model.read` calls the new request reader. The file has 25 lines of room, so only the call and the kind go here.
- `scripts/model_requests.py` (new): reads `.shop/work/requests/*.md` as requests. It checks their form (decision
  D2) and emits the node fact and the status fact. It reuses the part reading's id, status and folded-block checks
  (notes section 5).
- `CLAUDE.md`: a module-map row for `scripts/model_requests.py`, the reading of requests by `model`.
- `scripts/model`: the header/help text (lines 35-38) that says it reads no other layout, so that it names
  `.shop/work/requests/*.md` among what is read.
- `tests/scenarios/design_model_check_reading.py`: the files-read table gains the `.shop/work/requests/q1.md` row
  and its marker (the request's node fact, decision D1).
- `tests/scenarios/design_model_check_requests.py` (new): the Givens of r112 and r118.
  `design_model_check_problems.py` is at 300 lines and takes nothing more.
- `tests/scenarios/test_design_model_check.py`: imports the new step module.
- `features/design-model-check.feature`: the deprecated r19 outline is removed, as the work-item's Retires
  section says. Nothing else in features/ changes.

Removed from the researcher's set: `scripts/model.lp`. Decision D4 leaves `v_k1` and `v_k2` alone.

## 3. Decisions

- **D1. r19's marker is the request's `node` fact of kind `request`**, with id `request/<context path>/q<n>`. This
  rests on design-model-check#r19, #r43 (a node written `<kind>/<context path>/<name>`),
  design-decision/references-are-ids, and the id form in the requests capability's Implementation. The asker,
  part_of and source facts that v17, v_d1 and v_d3 need are left to the work-items of r114, r115 and r119. This
  reader emits node and status only.
- **D2. "The form `work request` writes" is what requests#r1 says `work request` writes, spelled as requests'
  Implementation spells it.** A request file is of the form when all of the following hold:
  - its `id` is `request/<context path>/<file name>` and the file name is `q<n>.md`;
  - `kind` is `request`;
  - `asker` is present and not empty;
  - it has `part_of` or `source`;
  - `status` is in the request lifecycle (D3);
  - `turn` is `asker` or `upstream`;
  - it has a `## Lines` section;
  - any other `##` section is one of `## Outcomes`, `## Questions`, `## Answers`, `## Resolution`. These are the
    upstream's or later parts, so they are not required at first writing.

  A file that fails any of these gets one file problem naming the file. The folded or literal block refusal of
  #r29 applies too.

  This rests on design-model-check#r112, which names capability/requests as the authority, and on requests#r1:
  "an open request with ... its lines, the asker, the origins ... or the job-thread, and the turn". The Outcomes,
  Questions, Answers and Resolution sections are written by later commands (requests#r5), so a just-written
  request lacks them and is still of the form.

  The value of `asker` (a context id, `internal` or the product level) is not checked beyond being present. The
  Implementation does not spell the product level, and the scenario pins only absence. The researcher's reading B
  (asker alone) is narrower than r112's pointer to the requests form, so it is not taken.
- **D3. The request lifecycle is `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `refused`,
  `delivered`**, entered where the part statuses are kept. This rests on requests#r1 (open), #r17, #r18, #r8, #r9
  and #r11 (delivered). `withdrawn` is not in it: withdrawing a request is in requests' Not yet.
- **D4. `v_k1` and `v_k2` in `scripts/model.lp` stay as they are.** No accepted requirement or ruling removes
  them, and removing them would change what `model rules` prints (#r65). r118 needs only the file problem. The
  `ikind` fact is still written for a job or job-path initiative, as today.
- **D5. The `requests/` directory is never an initiative folder**, whether it is empty or not. This rests on
  design-model-check#r19, which reads `.shop/work/<initiative>/*.md` and `.shop/work/requests/*.md` as distinct
  paths.
- **D6. The "that `work request` wrote" fixture is built to D2's form**, since `work request` is not built yet.
  The fixture has id, kind request, an asker, a `source` naming an observation that exists in the fixture, status
  `open`, turn `upstream`, and a `## Lines` section with one line. This rests on requests#r1 and the
  Implementation. The "with no asker" fixture is the same file without `asker`.

## 4. Tests the decisions break

- `tests/scenarios/test_design_model_check.py::test_model_reads_the_repositorys_files_under_its_root_deprecated`
  (14 cases) is removed with its scenario. The work-item retires it, and its table lacks the requests row that
  r19 now has.
- None other. By the notes' search (no tools map exists):
  - no test makes a `.shop/work/requests/` directory (only migrate's tests mention requests);
  - no test uses an initiative of kind job or job-path (`kind=` in tests is capability-change or defect);
  - no test or feature names `v_k1` or `v_k2`;
  - `design_model_check_problems.py:84` "there is no initiative.md" concerns `i1`, not `requests/`;
  - `tests/scripts/test_model_output.py:19` counts file problems on a fixture with no requests directory;
  - `tests/scripts/test_model_reading.py` and `tests/scripts/test_model.py` use neither.

  D3 adds a lifecycle and D2 adds checks only for request files, which no existing fixture has.

## 5. Open cases

- A `.md` file under `.shop/work/requests/` whose name is not `q<n>.md`: under D2 it is a file problem. The
  wording of that problem is the implementer's to name.
- A subdirectory or non-Markdown file under `.shop/work/requests/`: the scenarios are silent. The implementer
  says what happens (ignored, as r19 reads only `*.md` there).
- A request with both `part_of` and `source`: D2 needs one or the other, and the scenarios do not say whether
  both is a problem.
- Two request files with one id: whether the existing one-id-two-kinds or duplicate-id checks cover it.
- A job or job-path initiative that also breaks `v_k1`/`v_k2`: the violation may print beside the file problem.
  The implementer names what the r118 rows show.
- The text of the file problem for a job or job-path initiative, and whether it names the kind.
- How `scripts/workqueue.py` `find` resolves `q1` to `requests/q1.md` (notes section 3) is not touched here. It
  belongs to the requests capability's work-items.
