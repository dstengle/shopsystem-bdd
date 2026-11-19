---
id: vocabulary/missingmass.io/shopsystem/shopsystem-bdd/analysis
area: analysis
---

# The words of analysis

## Terms

- **Python interpreter** (noun) → object Python interpreter. The Python `tools` runs the analysis tools with: the one `--python` gives, else the first of `.venv/bin/python`, `venv/bin/python` and `$VIRTUAL_ENV/bin/python` under the current directory that exists, else the one that executes `scripts/tools`. This: the Python interpreter `tools` runs the analysis tools with.
- **analysis tool** (noun) → object analysis tool. A package `tools` probes and installs.
- **pip command** (noun) → object pip command. The command `<interpreter> -m pip install <package>` that `tools install` runs for one analysis tool.
- **coverage map** (noun) → object coverage map. What `tools map` writes under `.shop/scratch/tools/coverage`, made at one commit. This: the coverage map of this repository.
- **reference** (noun) → object reference. A use of a name the project defines, written `path:line`.
- **finding** (noun) → object finding. What ruff, vulture or import-linter reports.
- **heading** (noun) → object heading. The line `== <tool> ==` `tools check` prints above an analysis tool's findings.
- **log line** (noun) → object log line. The one line `tools probe --log` prints for a researcher's notes, `Probe: tools -> ` and each analysis tool with its presence.
- **size limit** (noun) → object size limit. The number of lines `tools size` allows a Python file.
- **dependency file** (noun) → object dependency file. A file that lists a project's dependencies (`pyproject.toml`, `requirements.txt`, ...).
- **test module** (noun) → object test module. A Python file under the directory `--tests` names (default `tests`), with its bindings.
- **subdirectory** (noun) → object subdirectory. A directory under the directory `--dir` names.
- **docstring** (noun) → object docstring. The text of a step between two lines of `"""` or of three backticks, in a feature file.
- **requirement tag** (noun) → object requirement tag. A tag `@r<n>` of a scenario, which names a requirement of its group.
- **scenario line** (noun) → object scenario line. A line that starts `Scenario:`.
- **scenario outline** (noun) → object scenario outline. A Scenario Outline of a feature file, with its Examples tables.
- **examples row** (noun) → object examples row. One row of values of an Examples table of a scenario outline.
- **rule block** (noun) → object rule block. A `Rule:` block of a feature file.
- **scenario title** (noun) → object scenario title. The text after `Scenario:` that names a scenario.
- **replacement** (noun) → object replacement. The scenario that a scenario tagged `@deprecated` names after `Deprecated for:`.
- **binding** (noun) → object binding. A `scenario(<feature>, "<title>")` or `scenarios(<path>, ...)` call of a test module.
- **scenarios call** (noun) → object scenarios call. A `scenarios(<path>, ...)` call of a test module.
- **search text** (noun) → object search text. The text `features list` is given with its `--title` option, which the scenario titles it prints contain.
- **`ruff`** (proper noun) → object ruff. The linter ruff.
- **`vulture`** (proper noun) → object vulture. The dead-code finder vulture.
- **`coverage`** (proper noun) → object coverage. Coverage.py, which `tools map` runs the tests under.
- **`jedi`** (proper noun) → object jedi. The static analyser jedi, which `tools refs` reads the code with.
- **`gf-rgl`** (proper noun) → object gf-rgl. GF's resource grammar library.
- **environment** (attribute) → attribute Python interpreter.environment. Whether pip installs into a virtualenv.
- **virtualenv** (noun) → value Python interpreter.environment virtualenv.
- **system** (noun) → value Python interpreter.environment system.
- **presence** (attribute) → attribute analysis tool.presence. Whether the interpreter has the tool, and whether pip can install it.
- **installed** (adjective) → value analysis tool.presence installed.
- **missing** (adjective) → value analysis tool.presence missing.
- **uninstallable** (adjective) → value analysis tool.presence uninstallable.
- **define** (verb, state) → relation Python file.defines. A Python file binds a name at its top level or in a class. Forms: defines, defined. Frame: <Python file> defines <identifier>.
- **exceed** (verb, state) → relation Python file.exceeds. A Python file has more lines than a size limit. Forms: exceeds, exceeded. Frame: <Python file> exceeds <size limit>.
- **bind** (verb, state) → relation binding.binds. A binding names a scenario, by its title or by its feature file, so that a test runs the scenario. Forms: binds, bound. Frame: <binding> binds <scenario>.
- **toolchain** (noun) → object toolchain. The analysis tools and grammar tools this repository's checks run with. This: the toolchain of this repository.
- **probe** (verb, action) → operation toolchain.probe. Forms: probes, probed. Frame: <actor> probes <toolchain>.
- **install** (verb, action) → operation toolchain.install. Forms: installs, installed. Frame: <actor> installs <toolchain>. Frame: <actor> installs <analysis tool>. Frame: <actor> installs <version>.
- **map** (verb, action) → operation code analysis.map. Forms: maps, mapped. Frame: <actor> maps <repository>.
- **trace** (verb, action) → operation code analysis.trace. Forms: traces, traced. Frame: <actor> traces <identifier>.
- **screen** (verb, action) → operation code analysis.screen. Forms: screens, screened. Frame: <actor> screens <Python file>.
- **locate** (verb, action) → operation code analysis.locate. Forms: locates, located. Frame: <actor> locates <identifier>.
- **lint** (verb, action) → operation code analysis.lint. Forms: lints, linted. Frame: <actor> lints <file>.
- **size** (verb, action) → operation code analysis.size. Forms: sizes, sized. Frame: <actor> sizes <repository>.
- **the toolchain service** (proper noun) → service toolchain.
- **the code analysis service** (proper noun) → service code analysis.
- **revision** (attribute) → attribute coverage map.revision. The revision of this repository a coverage map was made at.
- **search** (verb, action) → operation feature reading.search. Forms: searches, searched. Frame: <actor> searches <repository>.
- **count** (verb, action) → operation feature reading.count. Forms: counts, counted. Frame: <actor> counts <feature file>.
- **scan** (verb, action) → operation feature reading.scan. Forms: scans, scanned. Frame: <actor> scans <repository>.
- **vet** (verb, action) → operation feature reading.vet. Forms: vets, vetted. Frame: <actor> vets <repository>.
- **the feature reading service** (proper noun) → service feature reading.
