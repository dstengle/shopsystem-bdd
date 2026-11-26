# contract-registry: every live line with its intended reading

## r1
From: b636 r1.

```reading
When the specification service deposits a contract, the contract registry service shall complete the request.
shall [x1: service the specification service (constant), x3: service the contract registry service (constant), x4: request "the request the trigger makes" (indexical)]
  when [x2: contract]
    request(e1, contract registry.deposit, subject: x1, object: x2)
  response
    complete(e2, subject: x3, object: x4)
```

## r2
From: b636 r2.

```reading
When the specification service retrieves a contract, the contract registry service shall return the contract.
shall [x1: service the specification service (constant), x3: service the contract registry service (constant)]
  when [x2: contract]
    request(e1, contract registry.retrieve, subject: x1, object: x2)
  response
    return(e2, subject: x3, object: x2)
```

## r3
From: b636 r3.

```reading
If the specification service retrieves a contract with a version that no contract has, then the contract registry service shall refuse the request and name the version.
shall [x1: service the specification service (constant), x5: service the contract registry service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: contract, x3: version]
    not [x4: contract]
      of(x3, x4)
    request(e1, contract registry.retrieve, subject: x1, object: x2)
    param(e1, version, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r4
From: b735 r4.

```reading
When the specification service registers a contract for an adapter spec, the contract registry service shall complete the request.
shall [x1: service the specification service (constant), x4: service the contract registry service (constant), x5: request "the request the trigger makes" (indexical)]
  when [x2: contract, x3: adapter spec]
    request(e1, contract registry.register, subject: x1, object: x2, for: x3)
  response
    complete(e2, subject: x4, object: x5)
```

