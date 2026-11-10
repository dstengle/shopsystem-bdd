# analysis-tools: every live line with its intended reading (b240)

## r36
Retires: r1. From: b154 r36, the option in the trigger's code (`option-set-to`). Audit: fine.

```reading
When the person runs `tools probe` with the `--python` option set to a Python interpreter, `tools` shall print the Python interpreter.
shall [x1: agent the person (constant), x2: command `tools probe` (parameter), x3: option `--python` (parameter), x5: tool `tools` (constant)]
  when [x4: Python interpreter]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    print(e2, subject: x5, object: x4)
```

## r37
Retires: r2. From: b154 r37. Audit: distortion, fixed with `exists` and the interpreter named by its path (`named`), not a proper noun in a file system; without `--python`, so r36 does not overlap. Known limit: #14 (the first match of four interpreters, each case said with existence).

```reading
While the `.venv/bin/python` Python interpreter exists, when the person runs `tools probe` without the `--python` option, `tools` shall print the `.venv/bin/python` Python interpreter.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: agent the person (constant), x3: command `tools probe` (parameter), x4: option `--python` (parameter), x5: tool `tools` (constant)]
  while
    exists(x1)
  when
    run(e1, subject: x2, object: x3, without: x4)
  response
    print(e2, subject: x5, object: x1)
```

## r38
Retires: r3. From: b154 r38. Audit: distortion, fixed as r37. Known limit: #14.

```reading
While the `venv/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print the `venv/bin/python` Python interpreter.
shall [x1: Python interpreter `venv/bin/python` (parameter), x2: Python interpreter `.venv/bin/python` (parameter), x3: agent the person (constant), x4: command `tools probe` (parameter), x5: option `--python` (parameter), x6: tool `tools` (constant)]
  while
    exists(x1)
    not
      exists(x2)
  when
    run(e1, subject: x3, object: x4, without: x5)
  response
    print(e2, subject: x6, object: x1)
```

## r39
Retires: r4. From: b154 r39. Audit: distortion, fixed as r37 (without `--python`: no overlap with r36). Known limit: #14.

```reading
While the `$VIRTUAL_ENV/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print the `$VIRTUAL_ENV/bin/python` Python interpreter.
shall [x1: Python interpreter `$VIRTUAL_ENV/bin/python` (parameter), x2: Python interpreter `.venv/bin/python` (parameter), x3: Python interpreter `venv/bin/python` (parameter), x4: agent the person (constant), x5: command `tools probe` (parameter), x6: option `--python` (parameter), x7: tool `tools` (constant)]
  while
    exists(x1)
    not
      exists(x2)
    not
      exists(x3)
  when
    run(e1, subject: x4, object: x5, without: x6)
  response
    print(e2, subject: x7, object: x1)
```

## r40
Retires: r5. From: b154 r40. Audit: distortion, fixed as r37; the running interpreter said as "a Python interpreter that executes the `scripts/tools` file", not a proper noun. Known limit: #14.

```reading
While the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist and the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print a Python interpreter that executes the `scripts/tools` file.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: Python interpreter `venv/bin/python` (parameter), x3: Python interpreter `$VIRTUAL_ENV/bin/python` (parameter), x4: agent the person (constant), x5: command `tools probe` (parameter), x6: option `--python` (parameter), x7: tool `tools` (constant), x9: file `scripts/tools` (parameter)]
  while
    not
      exists(x1)
    not
      exists(x2)
    not
      exists(x3)
  when
    run(e1, subject: x4, object: x5, without: x6)
  response [x8: Python interpreter]
    execute(subject: x8, object: x9)
    print(e2, subject: x7, object: x8)
```

## r41
Retires: r6. From: b154 r41 (r6's negated half, b118). Audit: distortion, fixed as r37. Known limit: #14.

```reading
While the `.venv/bin/python` Python interpreter exists and the `venv/bin/python` Python interpreter exists, when the person runs `tools probe` without the `--python` option, `tools` shall not print the `venv/bin/python` Python interpreter.
shall [x1: Python interpreter `.venv/bin/python` (parameter), x2: Python interpreter `venv/bin/python` (parameter), x3: agent the person (constant), x4: command `tools probe` (parameter), x5: option `--python` (parameter), x6: tool `tools` (constant)]
  while
    exists(x1)
    exists(x2)
  when
    run(e1, subject: x3, object: x4, without: x5)
  response
    not
      print(e2, subject: x6, object: x2)
```

## r7
Kept. Audit: fine.

```reading
While no analysis tool is `missing`, when the person runs `tools probe`, `tools` shall print every analysis tool and exit successfully.
shall [x2: agent the person (constant), x3: command `tools probe` (parameter), x4: tool `tools` (constant)]
  while
    not [x1: analysis tool]
      presence(x1) = `missing`
  when
    run(e1, subject: x2, object: x3)
  response
    every [x5: analysis tool]
      scope
        print(e2, subject: x4, object: x5)
    exit(e3, subject: x4, successfully)
```

## r8
Kept. Audit: fine ("exit with an error" where something is missing, not a refusal).

```reading
While an analysis tool is `missing`, when the person runs `tools probe`, `tools` shall exit with an error naming the analysis tool.
shall [x2: agent the person (constant), x3: command `tools probe` (parameter), x4: tool `tools` (constant)]
  while [x1: analysis tool]
    presence(x1) = `missing`
  when
    run(e1, subject: x2, object: x3)
  response
    exit(e2, subject: x4, with an error naming: x1)
```

## r42
Retires: r9. From: b154 r42. Audit: coined, the gloss of log line held each analysis tool; the line now prints every analysis tool. That the tools are in the one line is output layout (#18), which the line cannot say ("one log line that lists every analysis tool" parses, but has no step: every in a relative clause on an object).

```reading
When the person runs `tools probe` with the `--log` option, `tools` shall print one log line and every analysis tool.
shall [x1: agent the person (constant), x2: command `tools probe` (parameter), x3: option `--log` (parameter), x4: tool `tools` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response
    count exactly 1 [x5: log line]
      scope
        print(e2, subject: x4, object: x5)
    every [x6: analysis tool]
      scope
        print(e3, subject: x4, object: x6)
```

## r43
Retires: r10. From: b154 r43. Audit: distortion, fixed by section 5 (`This:` on Python interpreter: "the environment of the Python interpreter", the one `tools` runs with, not the dot-venv interpreter).

```reading
While the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install every analysis tool whose presence is `missing` and change no dependency file.
shall [x1: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x2: agent the person (constant), x3: command `tools install` (parameter), x4: tool `tools` (constant)]
  while
    environment(x1) = `virtualenv`
  when
    run(e1, subject: x2, object: x3)
  response
    every [x5: analysis tool]
      presence(x5) = `missing`
      scope
        install(e2, subject: x4, object: x5)
    not [x6: dependency file]
      change(e3, subject: x4, object: x6)
```

## r44
Retires: r11. From: b154 r44. Audit: coined, fixed by section 5 (a plain verb pin: "the version of `ruff` that the plugin pins", not the noun pinned version; `This:` on Python interpreter).

```reading
While `ruff` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install the version of `ruff` that the plugin pins.
shall [x1: analysis tool `ruff` (constant), x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: command `tools install` (parameter), x5: tool `tools` (constant), x7: thing the plugin (constant)]
  while
    presence(x1) = `missing`
    environment(x2) = `virtualenv`
  when
    run(e1, subject: x3, object: x4)
  response [x6: version]
    of(x6, x1)
    pin(subject: x7, object: x6)
    install(e2, subject: x5, object: x6)
```

## r45
Retires: r12. From: b154 r45. Audit: distortion, fixed by section 5 (`This:` on Python interpreter).

```reading
While an analysis tool is `missing` and the environment of the Python interpreter is `system`, if the person runs `tools install`, then `tools` shall refuse the command and name the analysis tool.
shall [x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: command `tools install` (parameter), x5: tool `tools` (constant)]
  while [x1: analysis tool]
    presence(x1) = `missing`
    environment(x2) = `system`
  if
    run(e1, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r46
Retires: r13. From: b154 r46. Audit: distortion, fixed by section 5 (`This:` on Python interpreter); "the pip command that failed" is said by `uninstallable`.

```reading
While an analysis tool is `uninstallable` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall print the pip command of the analysis tool and exit with an error naming the analysis tool.
shall [x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: command `tools install` (parameter), x5: tool `tools` (constant)]
  while [x1: analysis tool]
    presence(x1) = `uninstallable`
    environment(x2) = `virtualenv`
  when
    run(e1, subject: x3, object: x4)
  response [x6: pip command]
    of(x6, x1)
    print(e2, subject: x5, object: x6)
    exit(e3, subject: x5, with an error naming: x1)
```

## r47
Retires: r14. From: b154 r47. Audit: distortion, fixed with a state verb fail ("a test fails"), not an attribute outcome.

```reading
While a test fails, when the person runs `tools map`, `tools` shall make a coverage map and exit successfully.
shall [x2: agent the person (constant), x3: command `tools map` (parameter), x4: tool `tools` (constant)]
  while [x1: test]
    fail(subject: x1)
  when
    run(e1, subject: x2, object: x3)
  response [x5: coverage map]
    make(e2, subject: x4, object: x5)
    exit(e3, subject: x4, successfully)
```

## r48
Retires: r15. From: b154 r48. Audit: distortion, fixed with `exists` ("a coverage map exists", not "this repository holds").

```reading
While a coverage map exists, when the person runs `tools map`, `tools` shall replace the coverage map.
shall [x2: agent the person (constant), x3: command `tools map` (parameter), x4: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when
    run(e1, subject: x2, object: x3)
  response
    replace(e2, subject: x4, object: x1)
```

## r49
Retires: r16. From: b154 r49. Audit: distortion, fixed with `number-of` ("the number of tests in the coverage map", not run count) and the option in the trigger's code.

```reading
When the person runs `tools map` with the `--json` option, `tools` shall make a coverage map and print the commit of the coverage map and the number of tests in the coverage map.
shall [x1: agent the person (constant), x2: command `tools map` (parameter), x3: option `--json` (parameter), x4: tool `tools` (constant)]
  when
    run(e1, subject: x1, object: x2, with: x3)
  response [x5: coverage map, x6: commit, x7: number]
    make(e2, subject: x4, object: x5)
    of(x6, x5)
    print(e3, subject: x4, object: x6)
    number x7 of [x8: test]
      in(x8, x5)
    print(e4, subject: x4, object: x7)
```

## r50
Retires: r17. From: b154 r50. Audit: distortion, fixed with `number-of` ("the number of tests that execute the function", not test count) and `exists`.

```reading
While a coverage map exists, when the person runs `tools tests-of` on a function, `tools` shall print every test that executes the function, the number of tests that execute the function and the commit of the coverage map.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x5: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x4: function]
    run(e1, subject: x2, object: x3, on: x4)
  response [x7: number, x9: commit]
    every [x6: test]
      execute(subject: x6, object: x4)
      scope
        print(e2, subject: x5, object: x6)
    number x7 of [x8: test]
      execute(subject: x8, object: x4)
    print(e3, subject: x5, object: x7)
    of(x9, x1)
    print(e4, subject: x5, object: x9)
```

## r51
Retires: r18. From: b154 r51. Audit: unsayable (each file with its own count, a distribution); the line prints each Python file, with `exists` and the option in the trigger's code.

```reading
While a coverage map exists, when the person runs `tools tests-of` with the `--by-file` option on a function, `tools` shall print every Python file that holds a test that executes the function.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x4: option `--by-file` (parameter), x6: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x5: function]
    run(e1, subject: x2, object: x3, with: x4, on: x5)
  response
    every [x7: Python file, x8: test]
      execute(subject: x8, object: x5)
      in(x8, x7)
      scope
        print(e2, subject: x6, object: x7)
```

## r52
Retires: r19. From: b154 r52. Audit: distortion, fixed with `exists`; "says that no test executed it" is reported content, which the line cannot say: it prints the commit of the coverage map.

```reading
While a coverage map exists, when the person runs `tools tests-of` on a function that no test executes, `tools` shall print the commit of the coverage map and exit successfully.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x6: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x4: function]
    not [x5: test]
      execute(subject: x5, object: x4)
    run(e1, subject: x2, object: x3, on: x4)
  response [x7: commit]
    of(x7, x1)
    print(e2, subject: x6, object: x7)
    exit(e3, subject: x6, successfully)
```

## r53
Retires: r20. From: b154 r53. Audit: distortion, fixed as r50, with the option in the trigger's code.

```reading
While a coverage map exists, when the person runs `tools tests-of` with the `--json` option on a function, `tools` shall print every test that executes the function, the number of tests that execute the function and the commit of the coverage map.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x4: option `--json` (parameter), x6: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x5: function]
    run(e1, subject: x2, object: x3, with: x4, on: x5)
  response [x8: number, x10: commit]
    every [x7: test]
      execute(subject: x7, object: x5)
      scope
        print(e2, subject: x6, object: x7)
    number x8 of [x9: test]
      execute(subject: x9, object: x5)
    print(e3, subject: x6, object: x8)
    of(x10, x1)
    print(e4, subject: x6, object: x10)
```

## r54
Retires: r21. From: b154 r54. Audit: distortion, fixed by section 5 (refuse a name: "an identifier that no Python file defines", as r59 does, not "a function that no Python file has").

```reading
While a coverage map exists, if the person runs `tools tests-of` on an identifier that no Python file defines, then `tools` shall refuse the command and name the identifier.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x6: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  if [x4: identifier]
    not [x5: Python file]
      define(subject: x5, object: x4)
    run(e1, subject: x2, object: x3, on: x4)
  response
    refuse(e2, subject: x6, object: x3)
    name(e3, subject: x6, object: x4)
```

## r55
Retires: r22. From: b154 r55. Audit: distortion, fixed with `exists` ("no coverage map exists").

```reading
While no coverage map exists, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `tools map`.
shall [x2: agent the person (constant), x3: command `tools tests-of` (parameter), x5: tool `tools` (constant), x6: thing `tools map` (parameter)]
  while
    not [x1: coverage map]
      exists(x1)
  if [x4: function]
    run(e1, subject: x2, object: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x3)
    name(e3, subject: x5, object: x6)
```

## r56
Retires: r23. From: b154 r56. Audit: distortion, fixed by phase 12 ("every function of the Python file that no test executes", not the one function of the trigger); the number of those functions is left out: "the number of Ks that no K Vs" parses but has no step yet.

```reading
While a coverage map exists, when the person runs `tools untested` on a Python file, `tools` shall print every function of the Python file that no test executes and the commit of the coverage map and exit successfully.
shall [x2: agent the person (constant), x3: command `tools untested` (parameter), x5: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x4: Python file]
    run(e1, subject: x2, object: x3, on: x4)
  response [x8: commit]
    every [x6: function]
      of(x6, x4)
      not [x7: test]
        execute(subject: x7, object: x6)
      scope
        print(e2, subject: x5, object: x6)
    of(x8, x1)
    print(e3, subject: x5, object: x8)
    exit(e4, subject: x5, successfully)
```

## r57
Retires: r24. From: b154 r57. Audit: distortion, fixed as r56, with the option in the trigger's code.

```reading
While a coverage map exists, when the person runs `tools untested` with the `--json` option on a Python file, `tools` shall print every function of the Python file that no test executes and the commit of the coverage map.
shall [x2: agent the person (constant), x3: command `tools untested` (parameter), x4: option `--json` (parameter), x6: tool `tools` (constant)]
  while [x1: coverage map]
    exists(x1)
  when [x5: Python file]
    run(e1, subject: x2, object: x3, with: x4, on: x5)
  response [x9: commit]
    every [x7: function]
      of(x7, x5)
      not [x8: test]
        execute(subject: x8, object: x7)
      scope
        print(e2, subject: x6, object: x7)
    of(x9, x1)
    print(e3, subject: x6, object: x9)
```

## r58
Retires: r25. From: b154 r58. Audit: distortion, fixed with `number-of` ("the number of references to the identifier", not reference count).

```reading
When the person runs `tools refs` on an identifier that a Python file defines, `tools` shall print every reference to the identifier and the number of references to the identifier and exit successfully.
shall [x1: agent the person (constant), x2: command `tools refs` (parameter), x5: tool `tools` (constant)]
  when [x3: identifier, x4: Python file]
    define(subject: x4, object: x3)
    run(e1, subject: x1, object: x2, on: x3)
  response [x7: number]
    every [x6: reference]
      to(x6, x3)
      scope
        print(e2, subject: x5, object: x6)
    number x7 of [x8: reference]
      to(x8, x3)
    print(e3, subject: x5, object: x7)
    exit(e4, subject: x5, successfully)
```

## r68
Retires: r26. From: b154 r58 with the `--json` option. Audit: distortion, fixed by section 5 (a `tools refs --json` line: r26 had been retired with no successor).

```reading
When the person runs `tools refs` with the `--json` option on an identifier that a Python file defines, `tools` shall print every reference to the identifier and the number of references to the identifier.
shall [x1: agent the person (constant), x2: command `tools refs` (parameter), x3: option `--json` (parameter), x6: tool `tools` (constant)]
  when [x4: identifier, x5: Python file]
    define(subject: x5, object: x4)
    run(e1, subject: x1, object: x2, with: x3, on: x4)
  response [x8: number]
    every [x7: reference]
      to(x7, x4)
      scope
        print(e2, subject: x6, object: x7)
    number x8 of [x9: reference]
      to(x9, x4)
    print(e3, subject: x6, object: x8)
```

## r59
Retires: r27. From: b154 r59. Audit: fine.

```reading
If the person runs `tools refs` on an identifier that no Python file defines, then `tools` shall refuse the command and name the identifier.
shall [x1: agent the person (constant), x2: command `tools refs` (parameter), x5: tool `tools` (constant)]
  if [x3: identifier]
    not [x4: Python file]
      define(subject: x4, object: x3)
    run(e1, subject: x1, object: x2, on: x3)
  response
    refuse(e2, subject: x5, object: x2)
    name(e3, subject: x5, object: x3)
```

## r60
Retires: r28. From: b154 r60. Audit: distortion ("under" the heading is output layout, #18, which the line cannot say).

```reading
While a file holds a finding of an analysis tool, when the person runs `tools check` on the file, `tools` shall print the heading of the analysis tool and the finding and exit with an error naming the finding.
shall [x4: agent the person (constant), x5: command `tools check` (parameter), x6: tool `tools` (constant)]
  while [x1: file, x2: finding, x3: analysis tool]
    of(x2, x3)
    in(x2, x1)
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: heading]
    of(x7, x3)
    print(e2, subject: x6, object: x7)
    print(e3, subject: x6, object: x2)
    exit(e4, subject: x6, with an error naming: x2)
```

## r61
Retires: r29. From: b154 r61. Audit: fine.

```reading
While `vulture` is `missing`, when the person runs `tools check`, `tools` shall exit with an error naming `vulture`.
shall [x1: analysis tool `vulture` (constant), x2: agent the person (constant), x3: command `tools check` (parameter), x4: tool `tools` (constant)]
  while
    presence(x1) = `missing`
  when
    run(e1, subject: x2, object: x3)
  response
    exit(e2, subject: x4, with an error naming: x1)
```

## r62
Retires: r30. From: b154 r62. Audit: fine.

```reading
While `coverage` is `missing`, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `coverage` and `tools install`.
shall [x1: analysis tool `coverage` (constant), x2: agent the person (constant), x3: command `tools tests-of` (parameter), x5: tool `tools` (constant), x6: thing `tools install` (parameter)]
  while
    presence(x1) = `missing`
  if [x4: function]
    run(e1, subject: x2, object: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x3)
    name(e3, subject: x5, object: x1)
    name(e4, subject: x5, object: x6)
```

## r63
Retires: r31. From: b154 r63. Audit: fine.

```reading
While `jedi` is `missing`, if the person runs `tools refs` on an identifier, then `tools` shall refuse the command and name `jedi` and `tools install`.
shall [x1: analysis tool `jedi` (constant), x2: agent the person (constant), x3: command `tools refs` (parameter), x5: tool `tools` (constant), x6: thing `tools install` (parameter)]
  while
    presence(x1) = `missing`
  if [x4: identifier]
    run(e1, subject: x2, object: x3, on: x4)
  response
    refuse(e2, subject: x5, object: x3)
    name(e3, subject: x5, object: x1)
    name(e4, subject: x5, object: x6)
```

## r64
Retires: r32. From: b154 r64. Audit: distortion, fixed with the option and its argument in the trigger's code (`option-set-to`); exceed is a plain verb with its frame.

```reading
While a Python file exceeds a size limit, when the person runs `tools size` with the `--limit` option set to the size limit, `tools` shall print the Python file and exit with an error naming the Python file.
shall [x3: agent the person (constant), x4: command `tools size` (parameter), x5: option `--limit` (parameter), x6: tool `tools` (constant)]
  while [x1: Python file, x2: size limit]
    exceed(subject: x1, object: x2)
  when
    argument(x5, x2)
    run(e1, subject: x3, object: x4, with: x5)
  response
    print(e2, subject: x6, object: x1)
    exit(e3, subject: x6, with an error naming: x1)
```

## r65
Retires: r33. From: b154 r65. Audit: unsayable (a default value), the default named in the line as the `300` size limit, with `--limit` not given.

```reading
While no Python file exceeds the `300` size limit, when the person runs `tools size` without the `--limit` option, `tools` shall exit successfully.
shall [x2: size limit `300` (parameter), x3: agent the person (constant), x4: command `tools size` (parameter), x5: option `--limit` (parameter), x6: tool `tools` (constant)]
  while
    not [x1: Python file]
      exceed(subject: x1, object: x2)
  when
    run(e1, subject: x3, object: x4, without: x5)
  response
    exit(e2, subject: x6, successfully)
```

## r66
Retires: r34. From: b154 r66. Audit: distortion, fixed by section 5 (`This:` on Python interpreter).

```reading
While `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install `gf-rgl`.
shall [x1: analysis tool `gf-rgl` (constant), x2: Python interpreter "the Python interpreter `tools` runs the analysis tools with" (indexical), x3: agent the person (constant), x4: command `tools install` (parameter), x5: tool `tools` (constant)]
  while
    presence(x1) = `missing`
    environment(x2) = `virtualenv`
  when
    run(e1, subject: x3, object: x4)
  response
    install(e2, subject: x5, object: x1)
```

## r67
Retires: r35. From: b154 r67. Audit: fine.

```reading
When the person runs `tools probe`, `tools` shall print `gf-rgl`.
shall [x1: agent the person (constant), x2: command `tools probe` (parameter), x3: tool `tools` (constant), x4: analysis tool `gf-rgl` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    print(e2, subject: x3, object: x4)
```
