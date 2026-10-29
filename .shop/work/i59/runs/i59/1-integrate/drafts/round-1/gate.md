## Change list

The note's sentences, quoted in full; each row names the one it comes from.
- L1: "The plugin's commands, `work`, `measure`, `features`, `model`, `tools` and `migrate`, shall give their output as one JSON object on stdout by default."
- L2: "**When** a command of the plugin refuses, finds a fault, finds a check failing or has a question for the person, the command shall exit 0 and give what it found and why in its JSON output."
- L3: "**If** a command of the plugin crashes on an error it does not handle, then the command shall exit 1."
- L4: "The plugin's agents shall return their output as structured JSON."
- A1: "Every command gives one JSON object by default, a command that prints text (the SessionStart hook, features showing Gherkin, model rules) with that text inside a field; each command's JSON shape is named in its contract (the person, 2026-10-28)"
- A2: "All commands: every command exits 0 but on a crash, check-like ones included; work run and the suite read an ok field of the JSON in place of the exit code, and the approved lines that rely on exit codes are retired (the person, 2026-10-28)"
- A3: "The reply an agent gives its caller becomes JSON, in one shape for all agents: outcome, summary, files, questions; result.json is JSON already (the person, 2026-10-28)"

### supervision
added | supervision | r188 | `work run` shall give its output as one JSON object on stdout. | L1
added | supervision | r189 | The JSON object that `work run` gives shall hold the field `ok`. | A1
added | supervision | r190 | **When** `work run` ends without crashing on an error it does not handle, `work run` shall exit successfully. | A2
added | supervision | r191 | **If** `work run` crashes on an error it does not handle, **then** `work run` shall exit with an error. | L3
added | supervision | r207 | **When** `work run` refuses, `work run` shall give `ok` false in its JSON object, saying why. | L2
added | supervision | r208 | **When** `work run` runs a check that a work-item names, `work run` shall take the check as failing unless the JSON object the check gives holds `ok` true. | A2
added | supervision | r192 | **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall give `ok` true in its JSON object, with each work-item's status. | A2
added | supervision | r193 | **When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall give `ok` false in its JSON object, with the request and its open questions. | L2
added | supervision | r194 | **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall give `ok` false in its JSON object, with each work-item's status and each open question. | L2
added | supervision | r195 | **When** no work-item can make a transition and a work-item is `failed`, `work run` shall give `ok` false in its JSON object, with each work-item's status and each fault. | L2
added | supervision | r196 | **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and one such node is `awaiting-answer` or `failed`, `work run` shall give `ok` false in its JSON object, with the status of each initiative it took. | L2
added | supervision | r197 | **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed` and no request whose asker is this context is in the asker's turn, `work run` shall give `ok` true in its JSON object, with the status of each initiative it took. | A2
added | supervision | r198 | **If** the push after the branch review's commit fails, **then** `work run` shall end, giving `ok` false in its JSON object and saying why. | L2
added | supervision | r199 | **If** `work run` cannot start the delivery it was asked for, **then** `work run` shall end, giving `ok` false in its JSON object and saying why, and change nothing. | L2
added | supervision | r200 | **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall end, giving `ok` false in its JSON object and naming the round. | L2
added | supervision | r201 | **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and end, giving `ok` false in its JSON object and naming the capability. | L2
added | supervision | r202 | **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, **then** `work run` shall end, giving `ok` false in its JSON object and naming the round and how it ended. | L2
added | supervision | r203 | **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, **then** `work run` shall take the initiative's other nodes through their transitions before it ends. | A2
added | supervision | r204 | **When** `work run` transitions a work-item to `failed`, `work run` shall end, giving `ok` false in its JSON object and naming the work-item and its fault. | L2
added | supervision | r205 | **If** the main checkout's `.shop/work/` has uncommitted changes when `work run` starts, **then** `work run` shall end, giving `ok` false in its JSON object and naming them, and change nothing. | L2
added | supervision | r206 | **If** the push verification before the branch review fails, **then** `work run` shall end, giving `ok` false in its JSON object and saying why, and start no branch review. | L2
removed | supervision | r9 | **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. | A2
removed | supervision | r101 | **When** `work run` ends while a request kept in this context whose asker is this context is in the asker's turn, `work run` shall exit with an error, printing the request with its open questions. | A2
removed | supervision | r32 | **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question. | A2
removed | supervision | r52 | **When** no work-item can make a transition and a work-item is `failed`, `work run` shall exit with an error, printing each work-item's status and each fault. | A2
removed | supervision | r81 | **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and one such node is `awaiting-answer` or `failed`, `work run` shall exit with an error, printing the status of each initiative it took. | A2
removed | supervision | r82 | **When** `work run` was started with no initiative, no node of an initiative it took can make a transition and none is `awaiting-answer` or `failed` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing the status of each initiative it took. | A2
removed | supervision | r53 | **If** the push after the branch review's commit fails, then `work run` shall exit with an error, saying why. | A2
removed | supervision | r10 | **If** `work run` cannot start the delivery it was asked for, then `work run` shall exit with an error, say why, and change nothing. | A2
removed | supervision | r96 | **If** a round of the kind `integrate` that `work run` started ends without a change list, **then** `work run` shall exit with an error, naming the round. | A2
removed | supervision | r107 | **If** a change list that `work run` reads names a capability that neither `spec/capabilities/` nor the round's drafts have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability. | A2
removed | supervision | r88 | **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall exit with an error, naming the round and how it ended. | A2
removed | supervision | r115 | **If** a round of any kind that `work run` started for a capability-proposal or an initiative ends in an error or at its turn limit, or leaves no result `work run` can read, then `work run` shall take the initiative's other nodes through their transitions before it exits with an error. | A2
removed | supervision | r40 | **When** `work run` transitions a work-item to `failed`, `work run` shall exit with an error, naming the work-item and its fault. | A2
removed | supervision | r46 | **If** the main checkout's `.shop/work/` has uncommitted changes when `work run` starts, then `work run` shall exit with an error, naming them, and change nothing. | A2
removed | supervision | r51 | **If** the push verification before the branch review fails, then `work run` shall exit with an error, saying why, and start no branch review. | A2

### work-queue
added | work-queue | r51 | `work` shall give its output as one JSON object on stdout. | L1
added | work-queue | r52 | The JSON object that `work` gives shall hold the field `ok`. | A1
added | work-queue | r53 | **When** `work` does what it was asked, `work` shall give `ok` true in its JSON object. | A2
added | work-queue | r54 | **When** `work` ends without crashing on an error it does not handle, `work` shall exit successfully. | A2
added | work-queue | r55 | **If** `work` crashes on an error it does not handle, **then** `work` shall exit with an error. | L3
added | work-queue | r50 | **If** `work` cannot do what it was asked, **then** `work` shall give `ok` false in its JSON object, saying why, and change nothing. | L2
added | work-queue | r56 | **If** the line given to `work note` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, **then** `work` shall give `ok` false in its JSON object, saying that a note is one line, and change nothing. | L2
added | work-queue | r57 | **If** `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, **then** `work` shall give `ok` false in its JSON object, saying that the answer must say which, and change nothing. | L2
added | work-queue | r58 | **If** the answer given to `work answer` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, **then** `work` shall give `ok` false in its JSON object, saying that an answer is one line, and change nothing. | L2
removed | work-queue | r7 | **If** `work` cannot do what it was asked, then `work` shall exit with an error, say why, and change nothing. | A2
removed | work-queue | r21 | **If** the line given to `work note` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, then `work` shall exit with an error, saying that a note is one line, and change nothing. | A2
removed | work-queue | r28 | **If** `work answer <work-item> <answer>` is run without the flag saying whether the answer asks for a change or accepts the work-item as it is on an `awaiting-answer` work-item whose question a reviewer asked, then `work` shall exit with an error, saying that the answer must say which, and change nothing. | A2
removed | work-queue | r15 | **If** the answer given to `work answer` has in it one of Unicode's mandatory line breaks, U+000A (LF), U+000B (VT), U+000C (FF), U+000D (CR), U+0085 (NEL), U+2028 or U+2029, then `work` shall exit with an error, saying that an answer is one line, and change nothing. | A2
removed | work-queue | r35 | **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object. | L1
removed | work-queue | r38 | **Where** `--json` is given, `work show` shall print its result as one JSON object. | L1

### design-model-check
added | design-model-check | r125 | `model` shall give its output as one JSON object on stdout. | L1
added | design-model-check | r126 | The JSON object that `model` gives shall hold the field `ok`. | A1
added | design-model-check | r127 | **When** `model` does what it was asked and finds no violation, unresolved reference or file problem and no decisions index that is not current, `model` shall give `ok` true in its JSON object. | A2
added | design-model-check | r128 | **When** `model` ends without crashing on an error it does not handle, `model` shall exit successfully. | A2
added | design-model-check | r129 | **If** `model` crashes on an error it does not handle, **then** `model` shall exit with an error. | L3
added | design-model-check | r138 | **If** `model` cannot do what it was asked, **then** `model` shall give `ok` false in its JSON object, saying why, and change nothing. | L2
added | design-model-check | r130 | **If** `model check` finds a violation, an unresolved reference or a file problem, **then** `model check` shall give each in its JSON object, a violated relation by its grammar.md code and plain label with its rows, with `ok` false. | L2
added | design-model-check | r131 | **When** `model check` finds warnings, `model check` shall give in its JSON object each warning relation with its plain label and its count, with no effect on its `ok`. | A2
added | design-model-check | r132 | The JSON object that `model check` gives shall hold its violations, warnings, unresolved references and file problems, each code mapped to its plain label. | A1
added | design-model-check | r133 | **If** no interpreter has clingo, **then** `model check` shall give `ok` false in its JSON object, naming each interpreter it tried and the command that installs clingo. | L2
added | design-model-check | r139 | **When** `model facts` is run, `model facts` shall give inside a field of its JSON object the facts read, one a line in clingo's syntax, using only the standard library. | A1
added | design-model-check | r134 | **If** `model decisions --check` finds `spec/decisions/index.md` is not what `model decisions` would write, **then** `model decisions` shall say so in its JSON object with `ok` false, writing nothing. | L2
added | design-model-check | r135 | The JSON object that `model why` gives shall hold the requirement's text and the capability-proposals that trace it. | A1
added | design-model-check | r136 | **When** `model rules` is run, `model rules` shall give in its JSON object each rule's code, plain label and kind, the violations first and then the warnings. | A1
added | design-model-check | r137 | **When** `model rules` is run, `model rules` shall give inside a field of its JSON object the text of each rule's code and plain label, one a line. | A1
removed | design-model-check | r2 | **If** `model check` finds a violation, an unresolved reference or a file problem, then `model check` shall print each, a violated relation by its grammar.md code and plain label with its rows, and exit with an error. | A2
removed | design-model-check | r11 | **When** `model check` finds warnings, `model check` shall print each warning relation with its plain label and its count, with no effect on whether it exits successfully. | A2
removed | design-model-check | r33 | **Where** `--json` is given, `model check` shall print its violations, warnings, unresolved references and file problems as one JSON object, each code mapped to its plain label, exiting as it would without `--json`. | L1
removed | design-model-check | r12 | **If** no interpreter has clingo, then `model check` shall exit with an error, naming each interpreter it tried and the command that installs clingo. | A2
removed | design-model-check | r15 | **If** `model decisions --check` finds `spec/decisions/index.md` is not what `model decisions` would write, then `model decisions` shall say so and exit with an error, writing nothing. | A2
removed | design-model-check | r108 | **Where** `--json` is given, `model why` shall print its result, the requirement's text and the capability-proposals that trace it, as one JSON object. | L1
removed | design-model-check | r65 | **When** `model rules` is run, `model rules` shall print each rule's code and plain label, one a line, the violations first and then the warnings, and exit successfully. | A1
removed | design-model-check | r109 | **Where** `--json` is given, `model rules` shall print its result, each rule's code, plain label and kind, as one JSON object. | L1
removed | design-model-check | r105 | **If** `model` cannot do what it was asked, then `model` shall exit with an error, say why, and change nothing. | A2
removed | design-model-check | r13 | **When** `model facts` is run, `model facts` shall print the facts read, one a line in clingo's syntax, using only the standard library. | A1

### feature-file-tools
added | feature-file-tools | r63 | `features` shall give its output as one JSON object on stdout. | L1
added | feature-file-tools | r64 | The JSON object that `features` gives shall hold the field `ok`. | A1
added | feature-file-tools | r65 | **When** `features` neither refuses nor finds a verification failing, `features` shall give `ok` true in its JSON object. | A2
added | feature-file-tools | r66 | **When** `features` ends without crashing on an error it does not handle, `features` shall exit successfully. | A2
added | feature-file-tools | r67 | **If** `features` crashes on an error it does not handle, **then** `features` shall exit with an error. | L3
added | feature-file-tools | r73 | **When** `features` shows Gherkin text, `features` shall give the text inside a field of its JSON object. | A1
added | feature-file-tools | r68 | **If** `features` cannot do what it was asked, **then** `features` shall give `ok` false in its JSON object, saying why, and change nothing. | L2
added | feature-file-tools | r69 | **When** `features list` matches no scenario, `features` shall give no scenario in its JSON object, with `ok` true. | A2
added | feature-file-tools | r70 | **If** `features verify-moved` finds a scenario whose effective tags, description or steps differ between the two trees, a title used by more than one scenario in either tree, or a title in one tree and not the other, **then** `features verify-moved` shall name each in its JSON object, as changed (with what changed), duplicate, missing or added, with `ok` false. | L2
added | feature-file-tools | r71 | **If** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, **then** `features` shall give the module, line, title and feature of each in its JSON object, with `ok` false. | L2
added | feature-file-tools | r72 | **Where** `--unbound` is given, **if** a scenario in the feature files named after `--unbound` (with none named, every feature file under `--dir`) is bound by no `scenario(...)` or `scenarios(...)` call, or by more than one, **then** `features bindings` shall give its file and title, with the module and line of each call, in its JSON object, with `ok` false. | A2
removed | feature-file-tools | r46 | **If** `features` cannot do what it was asked, then `features` shall exit with an error, say why on stderr, and change nothing. | A2
removed | feature-file-tools | r7 | **Where** `--json` is not given, **when** `features list` matches no scenario, `features` shall print nothing and exit successfully. | L1
removed | feature-file-tools | r60 | **Where** `--json` is given, `features list` shall print its result, the scenarios with the file and title of each, as one JSON object. | L1
removed | feature-file-tools | r61 | **Where** `--json` is given, `features deprecated` shall print its result, each deprecated scenario with what it is deprecated for and its replacement, as one JSON object. | L1
removed | feature-file-tools | r62 | **Where** `--json` is given, `features bindings` shall print its result, the bindings it found wrong or, with `--unbound`, the scenarios bound by no test or by more than one, as one JSON object. | L1
removed | feature-file-tools | r17 | **If** `features verify-moved` finds a scenario whose effective tags, description or steps differ between the two trees, a title used by more than one scenario in either tree, or a title in one tree and not the other, then `features verify-moved` shall name each, as changed (with what changed), duplicate, missing or added, and exit with an error. | A2
removed | feature-file-tools | r25 | **If** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, then `features` shall print the module, line, title and feature of each, and exit with an error. | A2
removed | feature-file-tools | r58 | **Where** `--unbound` is given, **if** a scenario in the feature files named after `--unbound` (with none named, every feature file under `--dir`) is bound by no `scenario(...)` or `scenarios(...)` call, or by more than one, then `features bindings` shall print its file and title, with the module and line of each call, and exit with an error. | A2

### analysis-tools (draft not written: a hook refused the path; rows as drafted)
added | analysis-tools | r59 | `tools` shall give its output as one JSON object on stdout. | L1
added | analysis-tools | r60 | The JSON object that `tools` gives shall hold the field `ok`. | A1
added | analysis-tools | r61 | **When** `tools` neither refuses nor finds a tool missing, a lint finding or a file over the size limit, `tools` shall give `ok` true in its JSON object. | A2
added | analysis-tools | r62 | **When** `tools` ends without crashing on an error it does not handle, `tools` shall exit successfully. | A2
added | analysis-tools | r63 | **If** `tools` crashes on an error it does not handle, **then** `tools` shall exit with an error. | L3
added | analysis-tools | r64 | **If** `tools` cannot do what it was asked, **then** `tools` shall give `ok` false in its JSON object, saying why, and change nothing. | L2
added | analysis-tools | r65 | **If** a tool that `tools check`, `tools tests-of`, `tools untested` or `tools refs` needs is missing, **then** `tools` shall name it in its JSON object as missing rather than skip it, with `ok` false. | L2
added | analysis-tools | r66 | **When** `tools probe` is run, `tools` shall give in its JSON object each tool with its version, or as missing with what it is for, then the interpreter's path and whether it came from `--python`, the project's virtualenv or neither. | A1
added | analysis-tools | r67 | **If** `tools probe` finds a tool missing, **then** `tools probe` shall give `ok` false in its JSON object. | L2
added | analysis-tools | r68 | **When** `tools probe --log` is run, `tools` shall give inside a field of its JSON object one line, `Probe: tools -> ...`, naming every tool with its version or `missing`, for a researcher's notes. | A1
added | analysis-tools | r69 | **If** `tools install` has a missing tool to install and the interpreter is not a virtualenv, **then** `tools` shall install nothing and say so in its JSON object for each missing tool, with `ok` false. | L2
added | analysis-tools | r70 | **If** a tool is still missing after `tools install`, **then** `tools` shall give in its JSON object the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, with `ok` false. | L2
added | analysis-tools | r71 | **When** `tools map` is run, `tools` shall give in its JSON object the map's commit and its test count. | A1
added | analysis-tools | r72 | **If** the file given to `tools tests-of` has no function by the name given, **then** `tools` shall give `ok` false in its JSON object, saying the target cannot be read. | L2
added | analysis-tools | r73 | **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given, or in their place the Python files changed since `--base` and not deleted, and, where the project has import contracts, import-linter over the project, giving each one's findings under its own heading. | A2
added | analysis-tools | r74 | **If** a tool that `tools check` runs finds something, **then** `tools check` shall give `ok` false in its JSON object. | L2
added | analysis-tools | r75 | **If** any tracked Python file is over the size limit, **then** `tools size` shall give `ok` false in its JSON object. | L2
removed | analysis-tools | r49 | **If** `tools` cannot do what it was asked, then `tools` shall exit with an error, say why, and change nothing. | A2
removed | analysis-tools | r17 | **If** a tool that `tools check`, `tools tests-of`, `tools untested` or `tools refs` needs is missing, then `tools` shall name it as missing rather than skip it, and exit with an error. | A2
removed | analysis-tools | r3 | **When** `tools probe` is run, `tools` shall print each tool with its version, or as missing with what it is for, then the interpreter's path and whether it came from `--python`, the project's virtualenv or neither, and exit with an error when any tool is missing. | A2
removed | analysis-tools | r4 | **When** `tools probe --log` is run, `tools` shall print one line, `Probe: tools -> ...`, naming every tool with its version or `missing`, for a researcher's notes. | A1
removed | analysis-tools | r6 | **If** `tools install` has a missing tool to install and the interpreter is not a virtualenv, then `tools` shall install nothing, say so for each missing tool, and exit with an error. | A2
removed | analysis-tools | r7 | **If** a tool is still missing after `tools install`, then `tools` shall print the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exit with an error. | A2
removed | analysis-tools | r56 | **Where** `--json` is given, `tools map` shall print its result, the map's commit and its test count, as one JSON object. | L1
removed | analysis-tools | r53 | **Where** `--json` is given, `tools tests-of` shall print its result, the tests, their count and the map's commit, as one JSON object. | L1
removed | analysis-tools | r54 | **Where** `--json` is given, `tools untested` shall print its result, the functions, their count and the map's commit, as one JSON object. | L1
removed | analysis-tools | r55 | **Where** `--json` is given, `tools refs` shall print its result, the references and the summary, as one JSON object. | L1
removed | analysis-tools | r57 | **If** the file given to `tools tests-of` has no function by the name given, then `tools` shall exit with an error, saying the target cannot be read. | A2
removed | analysis-tools | r16 | **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given, or in their place the Python files changed since `--base` and not deleted, and, where the project has import contracts, import-linter over the project, each under its own heading, and exit with an error when any finds something. | A2
removed | analysis-tools | r51 | **If** any tracked Python file is over the size limit, then `tools size` shall exit with an error. | A2

### migration-tools
added | migration-tools | r37 | `migrate` shall give its output as one JSON object on stdout. | L1
added | migration-tools | r38 | The JSON object that `migrate` gives shall hold the field `ok`. | A1
added | migration-tools | r39 | **When** `migrate` does what it was asked, `migrate` shall give `ok` true in its JSON object. | A2
added | migration-tools | r40 | **When** `migrate` ends without crashing on an error it does not handle, `migrate` shall exit successfully. | A2
added | migration-tools | r41 | **If** `migrate` crashes on an error it does not handle, **then** `migrate` shall exit with an error. | L3
added | migration-tools | r45 | **When** `migrate` refuses, `migrate` shall give `ok` false in its JSON object, saying why. | L2
added | migration-tools | r42 | **If** `migrate` cannot make every change it was asked to, **then** `migrate` shall name in its JSON object each change it could not make, with `ok` false, and change no file. | L2
added | migration-tools | r44 | **When** the plugin's SessionStart hook runs `migrate`, `migrate` shall give the text the hook tells the session inside a field of its JSON object. | A1
added | migration-tools | r43 | **If** `.shop/plugin-version` holds no version, **then** `migrate status` and `migrate upgrade` shall give `ok` false in their JSON object, saying that the file holds no version and naming, for an empty file, that the file is empty and, for a file with other text in it, what it holds, and change nothing. | L2
removed | migration-tools | r7 | **If** `migrate` cannot make every change it was asked to, then `migrate` shall exit with an error, naming each change it could not make, and change no file. | A2
removed | migration-tools | r30 | **If** `.shop/plugin-version` holds no version, then `migrate status` and `migrate upgrade` shall exit with an error, saying that the file holds no version and naming, for an empty file, that the file is empty and, for a file with other text in it, what it holds, and change nothing. | A2

### batch-measurement
added | batch-measurement | r68 | `measure` shall give its output as one JSON object on stdout. | L1
added | batch-measurement | r69 | The JSON object that `measure` gives shall hold the field `ok`. | A1
added | batch-measurement | r70 | **When** `measure` does what it was asked, `measure` shall give `ok` true in its JSON object. | A2
added | batch-measurement | r71 | **When** `measure` ends without crashing on an error it does not handle, `measure` shall exit successfully. | A2
added | batch-measurement | r72 | **If** `measure` crashes on an error it does not handle, **then** `measure` shall exit with an error. | L3
added | batch-measurement | r73 | **If** `measure` refuses, **then** `measure` shall give `ok` false in its JSON object, with the reason it refuses. | L2
added | batch-measurement | r74 | **When** `measure show` or `measure compare` is run, `measure` shall give the text of its tables inside a field of its JSON object. | A1
removed | batch-measurement | r50 | **If** `measure` refuses, **then** `measure` shall exit with an error. | A2

### delivery
added | delivery | r23 | **When** `work run` exits, `delivering-an-initiative` shall show the person each work-item's status and each open question, as `work run` gives them in its JSON object. | A2
removed | delivery | r6 | **When** `work run` exits, `delivering-an-initiative` shall show the person each work-item's status and each open question, as `work run` printed them. | A2

### role-boundaries
added | role-boundaries | r8 | The plugin's agent definitions shall have every session started as one of them reply to the session or script that started it with one JSON object giving its outcome, its summary, the files it names and its questions. | L4; A3

### Glossary
changed | term/check | - **check**: a command a work-item names in place of scenarios, whose JSON output holding `ok` true shows its work complete. Not: criterion. (old: - **check**: a command a work-item names in place of scenarios, whose exit code 0 shows its work complete. Not: criterion.) | A2

### Other drafted sections (no Behaviour rows)
- spec/index.md `## Testing`: the suite fails when `features bindings --unbound`'s JSON object holds `ok` false (A2).
- The Implementation sections of supervision, work-queue, design-model-check, feature-file-tools, migration-tools (and analysis-tools, not written) replace the exit-code lists with "Exit code 0, and 1 only on a crash on an error the command does not handle; `ok` is a JSON boolean", and repoint "refused under r7/r46/r49" and "r10's exit"/"r101:" to r50/r68/r64, r199 and r193.
- Frontmatter: each changed capability rests on design-decision/commands-and-agents-answer-in-json instead of exits-are-successful-or-errors / query-commands-answer-in-their-output, with its retired ids added.

### Decision files
spec/decisions/0074-commands-and-agents-answer-in-json.md | Every command of the plugin gives one JSON object on stdout, holding `ok` and the fields its capability names, and exits successfully but on a crash on an error it does not handle; every agent replies to its caller with one JSON object of one shape: outcome, summary, files, questions. | source: [request/q25, design-decision/query-commands-answer-in-their-output, design-decision/exits-are-successful-or-errors] | by: "the person, 2026-10-28, accepting q25's lines and answering its questions" | supersedes both decisions named in source.

## Questions

1. supervision r193-r196: a `work run` that ends waiting on the person (a work-item `awaiting-answer`, a request in the asker's turn) gives (a) `ok` false, as drafted, the same as a fault; or (b) `ok` true, the status in its JSON object saying it waits, e.g. r194: "**When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall give `ok` true in its JSON object, with each work-item's status and each open question."
2. All command capabilities: the field `ok` is named in the Behaviour lines (as drafted, since A1 puts the shape in the contract), or the lines say "whether it did what it was asked" with `ok` named only in Implementation, e.g. "The JSON object that `work` gives shall hold whether `work` did what it was asked."
3. role-boundaries r8: the agents' reply shape stays in role-boundaries (as drafted), or goes to a new capability `agent-replies` (narrator: a session or script that started an agent, group guarantees) with "[r1] Every session started as one of the plugin's agents shall reply to the session or script that started it with one JSON object giving its outcome, its summary, the files it names and its questions."
4. Glossary, A3: is the reply a term? If yes: "- **reply**: the one JSON object a session started as an agent gives the session or script that started it: its outcome, its summary, the files it names and its questions. Not: return." And is the reply's outcome one of the words of the term `outcome`? If yes, `outcome` becomes "the one word a session's result or reply gives: ...".
5. `--json` after JSON is the default: (a) refused as an unknown option (Implementation: "`--json` is no longer an option; given, it is refused as bad usage"), or (b) accepted and ignored (Implementation: "`--json` is accepted and changes nothing").
6. A1 names three text commands (the SessionStart hook, features showing Gherkin, `model rules`). The drafts also put text inside a field for `model facts` (r139), `tools probe --log` (r68) and `measure show`/`compare` tables (r74). (a) Keep those three; or (b) take text only where A1 names it, retiring r139, r68 and r74 and keeping r13 and r4 of design-model-check and analysis-tools unretired. And do report commands (`model check`, `features list`, `work show`) also keep a text form in a field? If yes, design-model-check gets "**When** `model check` is run, `model check` shall give inside a field of its JSON object the text of what it finds, one relation's code, label and count above its rows."
7. Lines still saying "print" or "say so and exit successfully" (work-queue r34, r36, r37; design-model-check r1, r16, r17, r37; feature-file-tools r4, r5, r16, r26; analysis-tools r8, r9, r11, r13, r14, r50; migration-tools r18, r27; batch-measurement r44-r62) are kept, read under the new JSON-object lines (as drafted); or each is retired and redrafted as "shall give ... in its JSON object".
8. supervision r45 and r65 are kept: r45's "exits with an error" is a `claude -p` session's exit, and r65 is pytest's exit, neither a command of the plugin. If they are to be retired: r45 becomes "**If** a worker's session ends in an error or at its turn limit, or leaves output that holds no JSON result, **then** `work run` shall transition the work-item to `failed`, recording how the session ended."; r65 is retired with no replacement. r155 ("how it exited and its output") is kept too.
9. migration-tools r34: does the PreCompact hook's text also go inside a field? If yes: "**When** the plugin's PreCompact hook runs `migrate`, `migrate` shall give the text the hook tells the session inside a field of its JSON object."
10. feature-file-tools r73: no `features` command in spec/ shows Gherkin or a scenario. Which one does A1 mean? (a) keep r73 general, as drafted; (b) name the command, e.g. "**When** `features show <title>` is run, `features` shall give the scenario's Gherkin inside a field of its JSON object", which is a new command; (c) drop r73.
11. Not drafted, because no line of the note changes their behaviour: requests' Implementation says "refused under work-queue r7" (now r50) and it rests on exits-are-successful-or-errors; formulation rests on it and its Implementation says Then lines "say a command exits successfully or exits with an error". Redraft them: requests "refused under work-queue r50" resting on design-decision/commands-and-agents-answer-in-json; formulation "Then lines say whether a command gives `ok` true or false, and exits with an error only on a crash"? (docs/capability-format.md's "Exits in words" is outside spec/ and needs the same change.)
12. spec-integration: its Implementation has the capability-writer reply with the change list, questions, cut sentences and paths. Under A3's one shape, does the change list go (a) in a file named under `files` (the reply file), with the questions under `questions`, or (b) in `summary`?
13. delivery r13 ("ask it to reply in a few lines and leave the rest in files") is kept, the few lines read as the reply's summary; or it is retired for role-boundaries r8: "**When** `delivering-an-initiative` dispatches an agent, `delivering-an-initiative` shall read the dispatch's reply as one JSON object and leave the rest in files."
14. analysis-tools: a hook refused the draft's path (".../spec/capabilities/analysis-tools.md") twice as a "report file". Its rows are above; it needs writing by a round the hook allows, or the hook relaxed for drafts paths.
