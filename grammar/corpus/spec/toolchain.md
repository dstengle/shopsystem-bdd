# toolchain: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: analysis-tools#r36, reworded in request words (0.38.0).

```reading
When the person probes the toolchain with a Python interpreter, the toolchain service shall return the Python interpreter.
shall [x1: agent the person (constant), x2: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant)]
  when [x3: Python interpreter]
    request(e1, toolchain.probe, subject: x1, object: x2)
    param(e1, Python interpreter, x3)
  response
    return(e2, subject: x4, object: x3)
```

## r2
From: analysis-tools#r37, reworded in request words (0.38.0).

```reading
While the `.venv/bin/python` Python interpreter exists, when the person probes the toolchain without a Python interpreter, the toolchain service shall return the `.venv/bin/python` Python interpreter.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: agent the person (constant), x3: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant)]
  while
    exists(x1)
  when
    request(e1, toolchain.probe, subject: x2, object: x3)
    noparam(e1, Python interpreter)
  response
    return(e2, subject: x4, object: x1)
```

## r3
From: analysis-tools#r38, reworded in request words (0.38.0).

```reading
While the `venv/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist, when the person probes the toolchain without a Python interpreter, the toolchain service shall return the `venv/bin/python` Python interpreter.
shall [x1: Python interpreter `venv/bin/python` (parameter), x2: Python interpreter `.venv/bin/python` (parameter), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant)]
  while
    exists(x1)
    not
      exists(x2)
  when
    request(e1, toolchain.probe, subject: x3, object: x4)
    noparam(e1, Python interpreter)
  response
    return(e2, subject: x5, object: x1)
```

## r4
From: analysis-tools#r39, reworded in request words (0.38.0).

```reading
While the `$VIRTUAL_ENV/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist, when the person probes the toolchain without a Python interpreter, the toolchain service shall return the `$VIRTUAL_ENV/bin/python` Python interpreter.
shall [x1: Python interpreter `$VIRTUAL_ENV/bin/python` (parameter), x2: Python interpreter `.venv/bin/python` (parameter), x3: Python interpreter `venv/bin/python` (parameter), x4: agent the person (constant), x5: toolchain "the toolchain of this repository" (indexical), x6: service the toolchain service (constant)]
  while
    exists(x1)
    not
      exists(x2)
    not
      exists(x3)
  when
    request(e1, toolchain.probe, subject: x4, object: x5)
    noparam(e1, Python interpreter)
  response
    return(e2, subject: x6, object: x1)
```

## r5
From: analysis-tools#r40, reworded in request words (0.38.0).

```reading
While the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist and the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist, when the person probes the toolchain without a Python interpreter, the toolchain service shall return a Python interpreter that executes the `scripts/tools` file.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: Python interpreter `venv/bin/python` (parameter), x3: Python interpreter `$VIRTUAL_ENV/bin/python` (parameter), x4: agent the person (constant), x5: toolchain "the toolchain of this repository" (indexical), x6: service the toolchain service (constant), x8: file `scripts/tools` (parameter)]
  while
    not
      exists(x1)
    not
      exists(x2)
    not
      exists(x3)
  when
    request(e1, toolchain.probe, subject: x4, object: x5)
    noparam(e1, Python interpreter)
  response [x7: Python interpreter]
    execute(subject: x7, object: x8)
    return(e2, subject: x6, object: x7)
```

## r6
From: analysis-tools#r41, reworded in request words (0.38.0).

```reading
While the `.venv/bin/python` Python interpreter exists and the `venv/bin/python` Python interpreter exists, when the person probes the toolchain without a Python interpreter, the toolchain service shall not return the `venv/bin/python` Python interpreter.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: Python interpreter `venv/bin/python` (parameter), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant)]
  while
    exists(x1)
    exists(x2)
  when
    request(e1, toolchain.probe, subject: x3, object: x4)
    noparam(e1, Python interpreter)
  response
    not
      return(e2, subject: x5, object: x2)
```

## r7
From: analysis-tools#r7, reworded in request words (0.38.0).

```reading
While no analysis tool is `missing`, when the person probes the toolchain, the toolchain service shall return every analysis tool and complete the request.
shall [x2: agent the person (constant), x3: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not [x1: analysis tool]
      presence(x1) = `missing`
  when
    request(e1, toolchain.probe, subject: x2, object: x3)
  response
    every [x5: analysis tool]
      scope
        return(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```

## r8
From: analysis-tools#r8, reworded in request words (0.38.0).

```reading
While an analysis tool is `missing`, when the person probes the toolchain, the toolchain service shall fail the check and name the analysis tool.
shall [x2: agent the person (constant), x3: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant), x5: check "the check the trigger makes" (indexical)]
  while [x1: analysis tool]
    presence(x1) = `missing`
  when
    request(e1, toolchain.probe, subject: x2, object: x3)
  response
    fail(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r9
From: analysis-tools#r42, reworded in request words (0.38.0).

```reading
When the person probes the toolchain with the log, the toolchain service shall return one log line and every analysis tool.
shall [x1: agent the person (constant), x2: toolchain "the toolchain of this repository" (indexical), x3: service the toolchain service (constant)]
  when
    request(e1, toolchain.probe, subject: x1, object: x2)
    param(e1, log, on)
  response
    count exactly 1 [x4: log line]
      scope
        return(e2, subject: x3, object: x4)
    every [x5: analysis tool]
      scope
        return(e3, subject: x3, object: x5)
```

## r10
From: analysis-tools#r43, reworded in request words (0.38.0).

```reading
While the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the toolchain service shall install every analysis tool whose presence is `missing` and change no dependency file.
shall [x1: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x2: agent the person (constant), x3: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant)]
  while
    environment(x1) = `virtualenv`
  when
    request(e1, toolchain.install, subject: x2, object: x3)
  response
    every [x5: analysis tool]
      presence(x5) = `missing`
      scope
        install(e2, subject: x4, object: x5)
    not [x6: dependency file]
      change(e3, subject: x4, object: x6)
```

## r11
From: analysis-tools#r44, reworded in request words (0.38.0).

```reading
While `ruff` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the toolchain service shall install the version of `ruff` that the plugin pins.
shall [x1: analysis tool `ruff` (constant), x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant), x7: plugin "the plugin the request is made with" (indexical)]
  while
    presence(x1) = `missing`
    environment(x2) = `virtualenv`
  when
    request(e1, toolchain.install, subject: x3, object: x4)
  response [x6: version]
    of(x6, x1)
    pin(subject: x7, object: x6)
    install(e2, subject: x5, object: x6)
```

## r12
From: analysis-tools#r45, reworded in request words (0.38.0).

```reading
While an analysis tool is `missing` and the environment of the Python interpreter is `system`, if the person installs the toolchain, then the toolchain service shall refuse the request and name the analysis tool.
shall [x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant), x6: request "the request the trigger makes" (indexical)]
  while [x1: analysis tool]
    presence(x1) = `missing`
    environment(x2) = `system`
  if
    request(e1, toolchain.install, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x1)
```

## r13
From: analysis-tools#r46, reworded in request words (0.38.0).

```reading
While an analysis tool is `uninstallable` and the environment of the Python interpreter is `virtualenv`, if the person installs the toolchain, then the toolchain service shall return the pip command of the analysis tool, refuse the request and name the analysis tool.
shall [x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant), x7: request "the request the trigger makes" (indexical)]
  while [x1: analysis tool]
    presence(x1) = `uninstallable`
    environment(x2) = `virtualenv`
  if
    request(e1, toolchain.install, subject: x3, object: x4)
  response [x6: pip command]
    of(x6, x1)
    return(e2, subject: x5, object: x6)
    refuse(e3, subject: x5, object: x7)
    name(e4, subject: x5, object: x1)
```

## r14
From: analysis-tools#r62, reworded in request words (0.38.0).

```reading
While `coverage` is `missing`, if the person traces a function, then the code analysis service shall refuse the request and name `coverage`.
shall [x1: analysis tool `coverage` (constant), x2: agent the person (constant), x4: service the code analysis service (constant), x5: request "the request the trigger makes" (indexical)]
  while
    presence(x1) = `missing`
  if [x3: function]
    request(e1, code analysis.trace, subject: x2, object: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r15
From: analysis-tools#r63, reworded in request words (0.38.0).

```reading
While `jedi` is `missing`, if the person locates an identifier, then the code analysis service shall refuse the request and name `jedi`.
shall [x1: analysis tool `jedi` (constant), x2: agent the person (constant), x4: service the code analysis service (constant), x5: request "the request the trigger makes" (indexical)]
  while
    presence(x1) = `missing`
  if [x3: identifier]
    request(e1, code analysis.locate, subject: x2, object: x3)
  response
    refuse(e2, subject: x4, object: x5)
    name(e3, subject: x4, object: x1)
```

## r16
From: analysis-tools#r66, reworded in request words (0.38.0).

```reading
While `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the toolchain service shall install `gf-rgl`.
shall [x1: analysis tool `gf-rgl` (constant), x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: toolchain "the toolchain of this repository" (indexical), x5: service the toolchain service (constant)]
  while
    presence(x1) = `missing`
    environment(x2) = `virtualenv`
  when
    request(e1, toolchain.install, subject: x3, object: x4)
  response
    install(e2, subject: x5, object: x1)
```

## r17
From: analysis-tools#r67, reworded in request words (0.38.0).

```reading
When the person probes the toolchain, the toolchain service shall return `gf-rgl`.
shall [x1: agent the person (constant), x2: toolchain "the toolchain of this repository" (indexical), x3: service the toolchain service (constant), x4: analysis tool `gf-rgl` (constant)]
  when
    request(e1, toolchain.probe, subject: x1, object: x2)
  response
    return(e2, subject: x3, object: x4)
```

## r18
From: b388 r18.

```reading
While no Python file exists and `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person installs the toolchain, the toolchain service shall install `gf-rgl` and complete the request.
shall [x2: analysis tool `gf-rgl` (constant), x3: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x4: agent the person (constant), x5: toolchain "the toolchain of this repository" (indexical), x6: service the toolchain service (constant), x7: request "the request the trigger makes" (indexical)]
  while
    not [x1: Python file]
      exists(x1)
    presence(x2) = `missing`
    environment(x3) = `virtualenv`
  when
    request(e1, toolchain.install, subject: x4, object: x5)
  response
    install(e2, subject: x6, object: x2)
    complete(e3, subject: x6, object: x7)
```

## r19
From: b388 r19.

```reading
While no Python file exists, when the person probes the toolchain, the toolchain service shall return `gf-rgl` and complete the request.
shall [x2: agent the person (constant), x3: toolchain "the toolchain of this repository" (indexical), x4: service the toolchain service (constant), x5: analysis tool `gf-rgl` (constant), x6: request "the request the trigger makes" (indexical)]
  while
    not [x1: Python file]
      exists(x1)
  when
    request(e1, toolchain.probe, subject: x2, object: x3)
  response
    return(e2, subject: x4, object: x5)
    complete(e3, subject: x4, object: x6)
```
