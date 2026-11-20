---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/toolchain
title: Toolchain
narrator: the person
group: service
area: analysis
specifies: service toolchain
language: codified-2
retired: []
unbuilt: []
---

# Toolchain

## Purpose
The analysis tools and the Python interpreter they run with: probed and installed.

## Behaviour

### [g1] A probe with a Python interpreter gives that interpreter
Restates: analysis-tools#r1@0.29.
- [r1] When the person probes the toolchain with a Python interpreter, the toolchain service shall return the Python
  interpreter.

### [g2] A probe finds the `.venv` interpreter first
Restates: analysis-tools#r1@0.29.
- [r2] While the `.venv/bin/python` Python interpreter exists, when the person probes the toolchain without a Python
  interpreter, the toolchain service shall return the `.venv/bin/python` Python interpreter.

### [g3] A probe finds the `venv` interpreter when there is no `.venv` one
Restates: analysis-tools#r1@0.29.
- [r3] While the `venv/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not
  exist, when the person probes the toolchain without a Python interpreter, the toolchain service shall return the
  `venv/bin/python` Python interpreter.

### [g4] A probe finds the active virtualenv's interpreter when there is no local one
Restates: analysis-tools#r1@0.29.
- [r4] While the `$VIRTUAL_ENV/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does
  not exist and the `venv/bin/python` Python interpreter does not exist, when the person probes the toolchain without a
  Python interpreter, the toolchain service shall return the `$VIRTUAL_ENV/bin/python` Python interpreter.

### [g5] A probe falls back to the interpreter that executes the tools
Restates: analysis-tools#r1@0.29.
- [r5] While the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does
  not exist and the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist, when the person probes the toolchain
  without a Python interpreter, the toolchain service shall return a Python interpreter that executes the
  `scripts/tools` file.

### [g6] A probe does not give the `venv` interpreter beside a `.venv` one
Restates: analysis-tools#r1@0.29.
- [r6] While the `.venv/bin/python` Python interpreter exists and the `venv/bin/python` Python interpreter exists, when
  the person probes the toolchain without a Python interpreter, the toolchain service shall not return the
  `venv/bin/python` Python interpreter.

### [g7] A probe with no missing analysis tool gives every analysis tool
Restates: analysis-tools#r3@0.29.
- [r7] While no analysis tool is `missing`, when the person probes the toolchain, the toolchain service shall return
  every analysis tool and complete the request.

### [g8] A probe with a missing analysis tool fails naming it
Restates: analysis-tools#r3@0.29.
- [r8] While an analysis tool is `missing`, when the person probes the toolchain, the toolchain service shall fail the
  check and name the analysis tool.

### [g9] A probe with the log gives one log line and every analysis tool
Restates: analysis-tools#r4@0.29.
- [r9] When the person probes the toolchain with the log, the toolchain service shall return one log line and every
  analysis tool.

### [g10] An install in a virtualenv installs every missing analysis tool and changes no dependency file
Restates: analysis-tools#r5@0.29.
- [r10] While the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the
  toolchain service shall install every analysis tool whose presence is `missing` and change no dependency file.
```given
the dependency file `requirements.txt` holds "pytest"
```

### [g11] An install installs the version of `ruff` the plugin pins
Restates: analysis-tools#r58@0.29.
- [r11] While `ruff` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person
  installs the toolchain, the toolchain service shall install the version of `ruff` that the plugin pins.

### [g12] An install outside a virtualenv is refused
Restates: analysis-tools#r6@0.29.
- [r12] While an analysis tool is `missing` and the environment of the Python interpreter is `system`, if the person
  installs the toolchain, then the toolchain service shall refuse the request and name the analysis tool.

### [g13] An install of an uninstallable analysis tool gives its pip command and is refused
Restates: analysis-tools#r7@0.29.
- [r13] While an analysis tool is `uninstallable` and the environment of the Python interpreter is `virtualenv`, if the
  person installs the toolchain, then the toolchain service shall return the pip command of the analysis tool, refuse
  the request and name the analysis tool.

### [g14] A function is not traced while `coverage` is missing
Restates: analysis-tools#r17@0.29.
- [r14] While `coverage` is `missing`, if the person traces a function, then the code analysis service shall refuse the
  request and name `coverage`.

### [g15] An identifier is not located while `jedi` is missing
Restates: analysis-tools#r17@0.29.
- [r15] While `jedi` is `missing`, if the person locates an identifier, then the code analysis service shall refuse the
  request and name `jedi`.

### [g16] An install in a virtualenv installs a missing `gf-rgl`
- [r16] While `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person
  installs the toolchain, the toolchain service shall install `gf-rgl`.

### [g17] A probe gives `gf-rgl`
- [r17] When the person probes the toolchain, the toolchain service shall return `gf-rgl`.

### [g18] An install in a repository with no Python file installs `gf-rgl`
- [r18] While no Python file exists and `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the toolchain service shall install `gf-rgl` and complete the request.

### [g19] A probe in a repository with no Python file gives `gf-rgl`
- [r19] While no Python file exists, when the person probes the toolchain, the toolchain service shall return `gf-rgl` and complete the request.

