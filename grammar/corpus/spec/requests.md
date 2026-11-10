# requests: every live line with its intended reading (b240)

## r59
Retires: r2. From: b153 r59. Audit: distortion, fixed by "runs `work request` with the `--raised-for` option set to a request" (an option with its argument).

```reading
When the person runs `work request` with the `--raised-for` option set to a request, `work` shall write a request raised for the request.
shall [x1: agent the person (constant), x2: command `work request` (parameter), x3: option `--raised-for` (parameter), x5: tool `work` (constant)]
  when [x4: request]
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response [x6: request]
    raised for(x6, x4)
    write(e2, subject: x5, object: x6)
```

## r60
Retires: r6, r8. From: b153 r60. Audit: coined, fixed by "without the `--source`, `--thread` and `--raised-for` options" (an option not given); "has no origin" and the noun origin gone, and it names `--thread`, which the refusal names with and without an upstream (r8 adds nothing to it).

```reading
If the person runs `work request` without the `--source`, `--thread` and `--raised-for` options, then `work` shall refuse the command and name `--thread`.
shall [x1: agent the person (constant), x2: command `work request` (parameter), x3: option `--source` (parameter), x4: option `--thread` (parameter), x5: option `--raised-for` (parameter), x6: tool `work` (constant)]
  if
    run(e1, subject: x1, object: x2, without: x3, without: x4, without: x5)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r61
Retires: r7 (with r102). From: b153 r61. Audit: distortion, fixed by section 5 ("with the `--source` and `--thread` options", the options of one run).

```reading
While this bounded context holds an upstream entry, if the person runs `work request` with the `--source` and `--thread` options, then `work` shall refuse the command and name `--source`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work request` (parameter), x5: option `--source` (parameter), x6: option `--thread` (parameter), x7: tool `work` (constant)]
  while [x2: upstream entry]
    in(x2, x1)
  if
    run(e1, subject: x3, object: x4, with: x5, with: x6)
  response
    refuse(e2, subject: x7, object: x4)
    name(e3, subject: x7, object: x5)
```

## r62
Retires: r9. From: b153 r62. Audit: distortion, fixed by "with the `--from` option set to a text" (an option with its argument).

```reading
If the person runs `work request` with the `--from` option set to a text that does not identify this bounded context, then `work` shall refuse the command and name the text.
shall [x1: agent the person (constant), x2: command `work request` (parameter), x3: option `--from` (parameter), x5: bounded context "the bounded context whose repository the command runs in" (indexical), x6: tool `work` (constant)]
  if [x4: text]
    not
      identify(subject: x4, object: x5)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r63
Retires: r14. From: b153 r63. Audit: distortion; assign gone and the request line given before the response (R1). Known limit: #8 (an attribute set to the value the command is given): the line says the `accepted` case, `work outcome accepted`.

```reading
While a request is `open`, when the person runs `work outcome accepted` on a request line proposed in the request, `work` shall set the line outcome of the request line to `accepted` and commit the request.
shall [x2: agent the person (constant), x3: command `work outcome accepted` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    status(x1) = `open`
  when [x4: request line]
    proposed in(x4, x1)
    run(e1, subject: x2, object: x3, on: x4)
  response
    initiates(e2, subject: x5, line outcome(x4) = `accepted`)
    commit(e3, subject: x5, object: x1)
```

## r64
Retires: r15. From: b153 r64. Audit: fine.

```reading
While a request is `awaiting-asker`, if the person runs `work outcome` on the request, then `work` shall refuse the command and name the request.
shall [x2: agent the person (constant), x3: command `work outcome` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `awaiting-asker`
  if
    run(e1, subject: x2, object: x3, on: x1)
  response
    refuse(e2, subject: x4, object: x3)
    name(e3, subject: x4, object: x1)
```

## r65
Retires: r16. From: b153 r65. Audit: fine.

```reading
While a request is `open` and the request does not address this bounded context, if the person runs `work outcome` on the request, then `work` shall refuse the command and name the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work outcome` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    status(x1) = `open`
    not
      address(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r66
Retires: r17. From: b153 r66. Audit: fine.

```reading
While a request is `open`, when the person runs `work ask` on the request, `work` shall write a question and commit the request.
shall [x2: agent the person (constant), x3: command `work ask` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `open`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: question]
    write(e2, subject: x4, object: x5)
    commit(e3, subject: x4, object: x1)
```

## r67
Retires: r18. From: b153 r67. Audit: fine.

```reading
While a request is `awaiting-asker` and the request originates from this bounded context, when the person runs `work reply` on the request, `work` shall write an answer and commit the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work reply` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    status(x1) = `awaiting-asker`
    originate(subject: x1, from: x2)
  when
    run(e1, subject: x3, object: x4, on: x1)
  response [x6: answer]
    write(e2, subject: x5, object: x6)
    commit(e3, subject: x5, object: x1)
```

## r68
Retires: r24. From: b153 r68. Audit: fine.

```reading
While a request is not `accepted`, if the person runs `work resolve` on the request, then `work` shall refuse the command and name the status of the request.
shall [x2: agent the person (constant), x3: command `work resolve` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    not
      status(x1) = `accepted`
  if
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: status]
    refuse(e2, subject: x4, object: x3)
    status(x1) = x5
    name(e3, subject: x4, object: x5)
```

## r69
Retires: r25. From: b153 r69. Audit: distortion, fixed by "every observation that no request and no initiative cite" (a negated restriction on an object); lack and citation gone.

```reading
When the person runs `work list`, `work` shall print every request, the status of every request and every observation that no request and no initiative cite.
shall [x1: agent the person (constant), x2: command `work list` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response
    every [x4: request]
      scope
        print(e2, subject: x3, object: x4)
    every [x5: request]
      scope [x6: status]
        status(x5) = x6
        print(e3, subject: x3, object: x6)
    every [x7: observation]
      not [x8: request]
        cite#3(subject: x8, object: x7)
      not [x9: initiative]
        cite#3(subject: x9, object: x7)
      scope
        print(e4, subject: x3, object: x7)
```

## r70
Retires: r26. From: b153 r70. Audit: fine.

```reading
When the person runs `work show` on a request, `work` shall print the status of the request and every request line proposed in the request.
shall [x1: agent the person (constant), x2: command `work show` (parameter), x4: tool `work` (constant)]
  when [x3: request]
    run(e1, subject: x1, object: x2, on: x3)
  response [x5: status]
    status(x3) = x5
    print(e2, subject: x4, object: x5)
    every [x6: request line]
      proposed in(x6, x3)
      scope
        print(e3, subject: x4, object: x6)
```

## r71
Retires: r27. From: b153 r71. Audit: fine.

```reading
When the person runs `work request`, `work` shall post an issue, write a request whose status is `open` and commit the request.
shall [x1: agent the person (constant), x2: command `work request` (parameter), x3: tool `work` (constant)]
  when
    run(e1, subject: x1, object: x2)
  response [x4: issue, x5: request]
    post(e2, subject: x3, object: x4)
    status(x5) = `open`
    write(e3, subject: x3, object: x5)
    commit(e4, subject: x3, object: x5)
```

## r72
Retires: r28. From: b153 r72. Audit: coined, fixed by "with the `--to` option set to a bounded context that has no GitHub repository"; host gone.

```reading
If the person runs `work request` with the `--to` option set to a bounded context that has no GitHub repository, then `work` shall refuse the command and name the bounded context.
shall [x1: agent the person (constant), x2: command `work request` (parameter), x3: option `--to` (parameter), x6: tool `work` (constant)]
  if [x4: bounded context]
    not [x5: GitHub repository]
      of(x5, x4)
    argument(x3, x4)
    run(e1, subject: x1, object: x2, with: x3)
  response
    refuse(e2, subject: x6, object: x2)
    name(e3, subject: x6, object: x4)
```

## r73
Retires: r29. From: b153 r73. Audit: fine.

```reading
While a request is `open`, when a session runs `work offer` on the request, `work` shall post a comment, set the status of the request to `awaiting-asker` and commit the request.
shall [x3: command `work offer` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `open`
  when [x2: session]
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: comment]
    post(e2, subject: x4, object: x5)
    initiates(e3, subject: x4, status(x1) = `awaiting-asker`)
    commit(e4, subject: x4, object: x1)
```

## r74
Retires: r30. From: b153 r74. Audit: fine.

```reading
While a request is `awaiting-asker`, when the person runs `work fits` on the request, `work` shall set the status of the request to `delivered`, write a resolution, post a comment, close the issue of the request and commit the request.
shall [x2: agent the person (constant), x3: command `work fits` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `awaiting-asker`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: resolution, x6: comment, x7: issue]
    initiates(e2, subject: x4, status(x1) = `delivered`)
    write(e3, subject: x4, object: x5)
    post(e4, subject: x4, object: x6)
    of(x7, x1)
    close(e5, subject: x4, object: x7)
    commit(e6, subject: x4, object: x1)
```

## r75
Retires: r31. From: b153 r75. Audit: fine.

```reading
While a request is `awaiting-asker`, when the person runs `work propose` on the request, `work` shall write a request line and commit the request.
shall [x2: agent the person (constant), x3: command `work propose` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `awaiting-asker`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: request line]
    write(e2, subject: x4, object: x5)
    commit(e3, subject: x4, object: x1)
```

## r76
Retires: r32. From: b153 r76. Audit: coined, fixed by "conforms to the comment form" (conformance) and section 5 ("the request does not hold the comment"); field block and lack gone.

```reading
While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and print every request.
shall [x3: artifact the comment form (constant), x5: command `work sync` (parameter), x6: tool `work` (constant)]
  while [x1: comment, x2: request]
    on(x1, x2)
    conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    run(e1, subject: x4, object: x5)
  response
    write(e2, subject: x6, object: x1)
    every [x7: request]
      scope
        print(e3, subject: x6, object: x7)
```

## r77
Retires: r33. From: b153 r77. Audit: coined, fixed by "does not conform to the comment form" (conformance).

```reading
While a comment on a request does not conform to the comment form, when a session runs `work sync`, `work` shall print the comment and not write the comment.
shall [x3: artifact the comment form (constant), x5: command `work sync` (parameter), x6: tool `work` (constant)]
  while [x1: comment, x2: request]
    on(x1, x2)
    not
      conforms(x1, x3)
  when [x4: session]
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x1)
    not
      write(e3, subject: x6, object: x1)
```

## r78
Retires: r34. From: b153 r78. Audit: fine.

```reading
While a request is `awaiting-asker`, when the person runs `work turn` on the request, `work` shall set the status of the request to `awaiting-upstream`, set the side of the request to `upstream` and post a comment.
shall [x2: agent the person (constant), x3: command `work turn` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `awaiting-asker`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: comment]
    initiates(e2, subject: x4, status(x1) = `awaiting-upstream`)
    initiates(e3, subject: x4, side(x1) = `upstream`)
    post(e4, subject: x4, object: x5)
```

## r79
Retires: r35. From: b153 r79. Audit: distortion, fixed by "is not `accepted`, `refused` or `withdrawn`" (a value set).

```reading
While a request is `open` and a request line proposed in the request is not `accepted`, `refused` or `withdrawn`, when the person runs `work turn` on the request, `work` shall set the status of the request to `awaiting-asker` and post a comment.
shall [x3: agent the person (constant), x4: command `work turn` (parameter), x5: tool `work` (constant)]
  while [x1: request, x2: request line]
    status(x1) = `open`
    proposed in(x2, x1)
    not
      line outcome(x2) = `accepted`
    not
      line outcome(x2) = `refused`
    not
      line outcome(x2) = `withdrawn`
  when
    run(e1, subject: x3, object: x4, on: x1)
  response [x6: comment]
    initiates(e2, subject: x5, status(x1) = `awaiting-asker`)
    post(e3, subject: x5, object: x6)
```

## r80
Retires: r36. From: b153 r80. Audit: coined, fixed by "every request line proposed in the request is one of `accepted`, `refused` or `withdrawn`" (a value set under every); block gone. Known limit: #8 ("keep the side of the request" for not changing it).

```reading
While a request is `open` and a request line proposed in the request is `accepted` and every request line proposed in the request is one of `accepted`, `refused` or `withdrawn`, when the person runs `work turn` on the request, `work` shall post a comment and keep the side of the request.
shall [x4: agent the person (constant), x5: command `work turn` (parameter), x6: tool `work` (constant)]
  while [x1: request, x2: request line]
    status(x1) = `open`
    proposed in(x2, x1)
    line outcome(x2) = `accepted`
    every [x3: request line]
      proposed in(x3, x1)
      scope
        or
          case
            line outcome(x3) = `accepted`
          case
            line outcome(x3) = `refused`
          case
            line outcome(x3) = `withdrawn`
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: comment, x8: side]
    post(e2, subject: x6, object: x7)
    side(x1) = x8
    keep(e3, subject: x6, object: x8)
```

## r81
Retires: r37. From: b153 r81. Audit: distortion, fixed by section 5 (the dropped conjunct "a request line proposed in the request is `refused`" restored).

```reading
While a request is `open` and a request line proposed in the request is `refused` and every request line proposed in the request is `refused`, when the person runs `work turn` on the request, `work` shall set the status of the request to `refused`, post a comment and close the issue of the request.
shall [x4: agent the person (constant), x5: command `work turn` (parameter), x6: tool `work` (constant)]
  while [x1: request, x2: request line]
    status(x1) = `open`
    proposed in(x2, x1)
    line outcome(x2) = `refused`
    every [x3: request line]
      proposed in(x3, x1)
      scope
        line outcome(x3) = `refused`
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: comment, x8: issue]
    initiates(e2, subject: x6, status(x1) = `refused`)
    post(e3, subject: x6, object: x7)
    of(x8, x1)
    close(e4, subject: x6, object: x8)
```

## r82
Retires: r38. From: b153 r82. Audit: distortion, fixed by "does not conform to the requirement grammar of this bounded context" (conformance); logical form gone. `work outcome accepted` keeps the command's argument in its code, as r63 does.

```reading
While a request line does not conform to the requirement grammar of this bounded context, if a session runs `work outcome accepted` on the request line, then `work` shall refuse the command and name the request line.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x5: command `work outcome accepted` (parameter), x6: tool `work` (constant)]
  while [x1: request line, x3: requirement grammar]
    of(x3, x2)
    not
      conforms(x1, x3)
  if [x4: session]
    run(e1, subject: x4, object: x5, on: x1)
  response
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x1)
```

## r83
Retires: r39. From: b153 r83. Audit: coined, fixed as r80 (a value set under every); block gone.

```reading
While a request is `open` and a request line proposed in the request is `accepted` and every request line proposed in the request is one of `accepted`, `refused` or `withdrawn`, when the person runs `work accept` on the request, `work` shall set the status of the request to `accepted`, write an item whose status is `shaped`, post a comment and commit the request.
shall [x4: agent the person (constant), x5: command `work accept` (parameter), x6: tool `work` (constant)]
  while [x1: request, x2: request line]
    status(x1) = `open`
    proposed in(x2, x1)
    line outcome(x2) = `accepted`
    every [x3: request line]
      proposed in(x3, x1)
      scope
        or
          case
            line outcome(x3) = `accepted`
          case
            line outcome(x3) = `refused`
          case
            line outcome(x3) = `withdrawn`
  when
    run(e1, subject: x4, object: x5, on: x1)
  response [x7: item, x8: comment]
    initiates(e2, subject: x6, status(x1) = `accepted`)
    status(x7) = `shaped`
    write(e3, subject: x6, object: x7)
    post(e4, subject: x6, object: x8)
    commit(e5, subject: x6, object: x1)
```

## r84
Retires: r40. From: b153 r84. Audit: coined, fixed by section 5 (r79's form, as a value set); block gone.

```reading
While a request line proposed in a request is not `accepted`, `refused` or `withdrawn`, if the person runs `work accept` on the request, then `work` shall refuse the command and name the request line.
shall [x3: agent the person (constant), x4: command `work accept` (parameter), x5: tool `work` (constant)]
  while [x1: request line, x2: request]
    proposed in(x1, x2)
    not
      line outcome(x1) = `accepted`
    not
      line outcome(x1) = `refused`
    not
      line outcome(x1) = `withdrawn`
  if
    run(e1, subject: x3, object: x4, on: x2)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r85
Retires: r41. From: b153 r85. Audit: fine.

```reading
While a request is `accepted`, when the person runs `work resolve` on the request, `work` shall set the status of the request to `delivered`, write a resolution, set the side of the request to `asker`, post a comment, close the issue of the request and commit the request.
shall [x2: agent the person (constant), x3: command `work resolve` (parameter), x4: tool `work` (constant)]
  while [x1: request]
    status(x1) = `accepted`
  when
    run(e1, subject: x2, object: x3, on: x1)
  response [x5: resolution, x6: comment, x7: issue]
    initiates(e2, subject: x4, status(x1) = `delivered`)
    write(e3, subject: x4, object: x5)
    initiates(e4, subject: x4, side(x1) = `asker`)
    post(e5, subject: x4, object: x6)
    of(x7, x1)
    close(e6, subject: x4, object: x7)
    commit(e7, subject: x4, object: x1)
```

## r86
Retires: r44. From: b153 r86. Audit: coined, fixed by "conforms to the comment form" (conformance); field block gone.

```reading
While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work watch`, `work` shall print the comment, exit successfully and not write the comment.
shall [x3: artifact the comment form (constant), x5: command `work watch` (parameter), x6: tool `work` (constant)]
  while [x1: comment, x2: request]
    on(x1, x2)
    conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    run(e1, subject: x4, object: x5)
  response
    print(e2, subject: x6, object: x1)
    exit(e3, subject: x6, successfully)
    not
      write(e4, subject: x6, object: x1)
```

## r87
Retires: r43. From: b153 r87. Audit: distortion, fixed by "an issue in the GitHub repository of this bounded context is `open` and the issue conforms to the comment form" (the open state and the form restored); host gone.

```reading
While an issue in the GitHub repository of this bounded context is `open` and the issue conforms to the comment form and no request has the issue, when a session runs `work watch`, `work` shall print the issue and exit successfully.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x4: artifact the comment form (constant), x7: command `work watch` (parameter), x8: tool `work` (constant)]
  while [x1: issue, x3: GitHub repository]
    of(x3, x2)
    in(x1, x3)
    status(x1) = `open`
    conforms(x1, x4)
    not [x5: request]
      of(x1, x5)
  when [x6: session]
    run(e1, subject: x6, object: x7)
  response
    print(e2, subject: x8, object: x1)
    exit(e3, subject: x8, successfully)
```

## r88
Retires: r45. From: b153 r88. Audit: distortion, fixed by "rejects the commit", the commit the command makes (the run's own thing, This: of commit), not some commit.

```reading
While this repository rejects the commit, if the person runs `work request`, then `work` shall refuse the command, name this repository and not post an issue.
shall [x1: repository "the repository the command runs in" (indexical), x2: commit "the commit the command makes" (indexical), x3: agent the person (constant), x4: command `work request` (parameter), x5: tool `work` (constant)]
  while
    reject#2(subject: x1, object: x2)
  if
    run(e1, subject: x3, object: x4)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
    not [x6: issue]
      post(e4, subject: x5, object: x6)
```

## r89
Retires: r46. From: b153 r89. Audit: distortion, fixed by section 5 ("not close the issue of the request") and "rejects the commit" (the run's own thing).

```reading
While this repository rejects the commit and a request is `open`, if the person runs `work turn` on the request, then `work` shall refuse the command, name this repository, not post a comment and not close the issue of the request.
shall [x1: repository "the repository the command runs in" (indexical), x2: commit "the commit the command makes" (indexical), x4: agent the person (constant), x5: command `work turn` (parameter), x6: tool `work` (constant)]
  while [x3: request]
    reject#2(subject: x1, object: x2)
    status(x3) = `open`
  if
    run(e1, subject: x4, object: x5, on: x3)
  response [x8: issue]
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x1)
    not [x7: comment]
      post(e4, subject: x6, object: x7)
    of(x8, x3)
    not
      close(e5, subject: x6, object: x8)
```

## r90
Retires: r47. From: b153 r90. Audit: distortion, fixed by section 5 ("not close the issue of the request") and "rejects the commit" (the run's own thing).

```reading
While this repository rejects the commit and a request is `awaiting-asker`, if the person runs `work fits` on the request, then `work` shall refuse the command, name this repository, not post a comment and not close the issue of the request.
shall [x1: repository "the repository the command runs in" (indexical), x2: commit "the commit the command makes" (indexical), x4: agent the person (constant), x5: command `work fits` (parameter), x6: tool `work` (constant)]
  while [x3: request]
    reject#2(subject: x1, object: x2)
    status(x3) = `awaiting-asker`
  if
    run(e1, subject: x4, object: x5, on: x3)
  response [x8: issue]
    refuse(e2, subject: x6, object: x5)
    name(e3, subject: x6, object: x1)
    not [x7: comment]
      post(e4, subject: x6, object: x7)
    of(x8, x3)
    not
      close(e5, subject: x6, object: x8)
```

## r91
Retires: r49. From: b153 r91. Audit: fine.

```reading
While a request addresses this bounded context and the request does not originate from this bounded context, if the person runs `work reply` on the request, then `work` shall refuse the command and name the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work reply` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    address(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r92
Retires: r50. From: b153 r92. Audit: fine.

```reading
While a request addresses this bounded context and the request does not originate from this bounded context and the request is `awaiting-asker`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work turn` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    address(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
    status(x1) = `awaiting-asker`
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r93
Retires: r51. From: b153 r93. Audit: fine.

```reading
While a request originates from this bounded context and the request does not address this bounded context and the request is `open`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work turn` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    originate(subject: x1, from: x2)
    not
      address(subject: x1, object: x2)
    status(x1) = `open`
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r94
Retires: r48. From: b153 r94. Audit: fine.

```reading
While a request originates from this bounded context and the request does not address this bounded context and the request is `awaiting-upstream`, if the person runs `work turn` on the request, then `work` shall refuse the command and name the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work turn` (parameter), x5: tool `work` (constant)]
  while [x1: request]
    originate(subject: x1, from: x2)
    not
      address(subject: x1, object: x2)
    status(x1) = `awaiting-upstream`
  if
    run(e1, subject: x3, object: x4, on: x1)
  response
    refuse(e2, subject: x5, object: x4)
    name(e3, subject: x5, object: x1)
```

## r95
Retires: r52 (with r103). From: b153 r95. Audit: coined, fixed by conformance and the side of the comment and of its entry, one line a side; field block and foreign entry gone.

```reading
While a comment on a request conforms to the comment form and the side of the comment is `asker` and the comment holds an entry whose side is `upstream` and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and not write the entry.
shall [x3: artifact the comment form (constant), x6: command `work sync` (parameter), x7: tool `work` (constant)]
  while [x1: comment, x2: request, x4: entry]
    on(x1, x2)
    conforms(x1, x3)
    side(x1) = `asker`
    side(x4) = `upstream`
    in(x4, x1)
    not
      in(x1, x2)
  when [x5: session]
    run(e1, subject: x5, object: x6)
  response
    write(e2, subject: x7, object: x1)
    not
      write(e3, subject: x7, object: x4)
```

## r96
Retires: r53. From: b153 r96. Audit: distortion, fixed by "is one of `delivered`, `refused` or `withdrawn`" (a value set) and r53's comment and its write restored. Known limit: #8 ("keep" for not changing the status and the side).

```reading
While a request is one of `delivered`, `refused` or `withdrawn` and a comment on the request conforms to the comment form and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and keep the status of the request and the side of the request.
shall [x3: artifact the comment form (constant), x5: command `work sync` (parameter), x6: tool `work` (constant)]
  while [x1: request, x2: comment]
    or
      case
        status(x1) = `delivered`
      case
        status(x1) = `refused`
      case
        status(x1) = `withdrawn`
    on(x2, x1)
    conforms(x2, x3)
    not
      in(x2, x1)
  when [x4: session]
    run(e1, subject: x4, object: x5)
  response [x7: status, x8: side]
    write(e2, subject: x6, object: x2)
    status(x1) = x7
    keep(e3, subject: x6, object: x7)
    side(x1) = x8
    keep(e4, subject: x6, object: x8)
```

## r97
Retires: r54. From: b153 r97. Audit: fine; section 5's option ("with the `--hook` option").

```reading
While a request originates from this bounded context and the request does not address this bounded context and the request is `awaiting-upstream`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall print the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the SessionStart hook (constant), x4: command `work watch` (parameter), x5: option `--hook` (parameter), x6: tool `work` (constant)]
  while [x1: request]
    originate(subject: x1, from: x2)
    not
      address(subject: x1, object: x2)
    status(x1) = `awaiting-upstream`
  when
    run(e1, subject: x3, object: x4, with: x5)
  response
    print(e2, subject: x6, object: x1)
```

## r98
Retires: r55. From: b153 r98. Audit: fine; section 5's option ("with the `--hook` option").

```reading
While a request addresses this bounded context and the request does not originate from this bounded context and the request is `awaiting-asker`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall print the request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the SessionStart hook (constant), x4: command `work watch` (parameter), x5: option `--hook` (parameter), x6: tool `work` (constant)]
  while [x1: request]
    address(subject: x1, object: x2)
    not
      originate(subject: x1, from: x2)
    status(x1) = `awaiting-asker`
  when
    run(e1, subject: x3, object: x4, with: x5)
  response
    print(e2, subject: x6, object: x1)
```

## r99
Retires: r56. From: b153 r99. Audit: distortion, fixed by section 5 (the real waiting condition) and the option ("with the `--hook` option").

```reading
While no request that originates from this bounded context is `awaiting-upstream` and no request that addresses this bounded context is `awaiting-asker`, when the SessionStart hook runs `work watch` with the `--hook` option, `work` shall exit successfully and not print a request.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x4: agent the SessionStart hook (constant), x5: command `work watch` (parameter), x6: option `--hook` (parameter), x7: tool `work` (constant)]
  while
    not [x1: request]
      originate(subject: x1, from: x2)
      status(x1) = `awaiting-upstream`
    not [x3: request]
      address(subject: x3, object: x2)
      status(x3) = `awaiting-asker`
  when
    run(e1, subject: x4, object: x5, with: x6)
  response
    exit(e2, subject: x7, successfully)
    not [x8: request]
      print(e3, subject: x7, object: x8)
```

## r100
Retires: r57. From: b153 r100. Audit: coined, fixed by conformance and section 5's option ("with the `--forward` option"); field block gone.

```reading
While a comment on a request conforms to the comment form and the request does not hold the comment, when a session runs `work watch` with the `--forward` option, `work` shall print the comment, exit successfully and not write the comment.
shall [x3: artifact the comment form (constant), x5: command `work watch` (parameter), x6: option `--forward` (parameter), x7: tool `work` (constant)]
  while [x1: comment, x2: request]
    on(x1, x2)
    conforms(x1, x3)
    not
      in(x1, x2)
  when [x4: session]
    run(e1, subject: x4, object: x5, with: x6)
  response
    print(e2, subject: x7, object: x1)
    exit(e3, subject: x7, successfully)
    not
      write(e4, subject: x7, object: x1)
```

## r101
Retires: r58. From: b153 r101. Audit: distortion, fixed as r87 and by section 5's option ("with the `--forward` option").

```reading
While an issue in the GitHub repository of this bounded context is `open` and the issue conforms to the comment form and no request has the issue, when a session runs `work watch` with the `--forward` option, `work` shall print the issue and exit successfully.
shall [x2: bounded context "the bounded context whose repository the command runs in" (indexical), x4: artifact the comment form (constant), x7: command `work watch` (parameter), x8: option `--forward` (parameter), x9: tool `work` (constant)]
  while [x1: issue, x3: GitHub repository]
    of(x3, x2)
    in(x1, x3)
    status(x1) = `open`
    conforms(x1, x4)
    not [x5: request]
      of(x1, x5)
  when [x6: session]
    run(e1, subject: x6, object: x7, with: x8)
  response
    print(e2, subject: x9, object: x1)
    exit(e3, subject: x9, successfully)
```

## r102
Retires: r7 (with r61). From: b153 r102. Audit: distortion, fixed by section 5 ("with the `--source` and `--raised-for` options").

```reading
While this bounded context holds an upstream entry, if the person runs `work request` with the `--source` and `--raised-for` options, then `work` shall refuse the command and name `--source`.
shall [x1: bounded context "the bounded context whose repository the command runs in" (indexical), x3: agent the person (constant), x4: command `work request` (parameter), x5: option `--source` (parameter), x6: option `--raised-for` (parameter), x7: tool `work` (constant)]
  while [x2: upstream entry]
    in(x2, x1)
  if
    run(e1, subject: x3, object: x4, with: x5, with: x6)
  response
    refuse(e2, subject: x7, object: x4)
    name(e3, subject: x7, object: x5)
```

## r103
Retires: r52 (with r95). From: b153 r95. Audit: coined, fixed as r95, the other side.

```reading
While a comment on a request conforms to the comment form and the side of the comment is `upstream` and the comment holds an entry whose side is `asker` and the request does not hold the comment, when a session runs `work sync`, `work` shall write the comment and not write the entry.
shall [x3: artifact the comment form (constant), x6: command `work sync` (parameter), x7: tool `work` (constant)]
  while [x1: comment, x2: request, x4: entry]
    on(x1, x2)
    conforms(x1, x3)
    side(x1) = `upstream`
    side(x4) = `asker`
    in(x4, x1)
    not
      in(x1, x2)
  when [x5: session]
    run(e1, subject: x5, object: x6)
  response
    write(e2, subject: x7, object: x1)
    not
      write(e3, subject: x7, object: x4)
```
