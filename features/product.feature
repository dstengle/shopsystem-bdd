# generated from spec/capabilities/product.md by features generate; do not edit
Feature: Product
  Narrator: the person

  @g1 @r1
  Scenario: The product is declared with its id and purpose
    Given a product p1
    And an id i1
    And a purpose p2
    When the person declares the product p1 with the id i1 and the purpose p2
    Then the product service keeps the product p1
    And the product service completes this request

  @g2 @r2
  Scenario: An actor of the product is declared
    Given a product actor p1
    When the person declares the product actor p1
    Then this product holds the product actor p1
    And the product service keeps the product actor p1
    And the product service completes this request

  @g3 @r3
  Scenario: A job to be done is declared with its actors and statement
    Given a job j1
    And an id i1
    And a product actor p1
    And a job statement j2
    When the person declares the job j1 with the id i1 and the product actor p1 and the job statement j2
    Then this product holds the job j1
    And the product service keeps the job j1
    And the product service completes this request

  @g4 @r4
  Scenario: A job whose statement is not of the job statement form is refused
    Given a job statement j2
    And the job statement j2 does not conform to the job statement form
    And a job j1
    When the person declares the job j1 with the job statement j2
    Then the product service refuses this request
    And the product service names the job statement j2

  @g5 @r5
  Scenario: A job whose actor is not the product's is refused
    Given a product actor p1
    And this product does not hold the product actor p1
    And a job j1
    When the person declares the job j1 with the product actor p1
    Then the product service refuses this request
    And the product service names the product actor p1

  @g6 @r6
  Scenario: A job that needs a job the product does not hold is refused
    Given a need n1
    And this product does not hold the need n1
    And a job j1
    When the person declares the job j1 with the need n1
    Then the product service refuses this request
    And the product service names the need n1

  @g7 @r7
  Scenario: A job whose needs close a cycle is refused
    Given a need n1
    And a job j1
    And the need n1 depends on the job j1
    When the person declares the job j1 with the need n1
    Then the product service refuses this request
    And the product service names the need n1

  @g8 @r8
  Scenario: A product declared again keeps the product's details
    Given a product detail p1
    And this product holds the product detail p1
    And a product p2
    And an id i1
    And a purpose p3
    When the person declares the product p2 with the id i1 and the purpose p3
    Then the product p2 holds the product detail p1
    And the product service keeps the product detail p1
    And the product service completes this request

  @g9 @r9
  Scenario: A product actor declared keeps the product's details
    Given a product detail p1
    And this product holds the product detail p1
    And a product actor p2
    When the person declares the product actor p2
    Then this product holds the product detail p1
    And the product service keeps the product detail p1
    And the product service completes this request

  @g10 @r10
  Scenario: A job declared keeps the product's details
    Given a product detail p1
    And this product holds the product detail p1
    And a job j1
    And an id i1
    And a product actor p2
    And a job statement j2
    When the person declares the job j1 with the id i1 and the product actor p2 and the job statement j2
    Then this product holds the product detail p1
    And the product service keeps the product detail p1
    And the product service completes this request

  @g11 @r11
  Scenario: A product not of the product form is not declared again
    Given this product does not conform to the product form
    And a product p1
    And an id i1
    And a purpose p2
    When the person declares the product p1 with the id i1 and the purpose p2
    Then the product service refuses this request
    And the product service names this product

  @g12 @r12
  Scenario: No product actor is declared in a product not of the product form
    Given this product does not conform to the product form
    And a product actor p1
    When the person declares the product actor p1
    Then the product service refuses this request
    And the product service names this product

  @g13 @r13
  Scenario: No job is declared in a product not of the product form
    Given this product does not conform to the product form
    And a job j1
    And an id i1
    And a product actor p1
    And a job statement j2
    When the person declares the job j1 with the id i1 and the product actor p1 and the job statement j2
    Then the product service refuses this request
    And the product service names this product

  @g15 @r15
  Scenario: A subdomain is declared with its id, type and jobs
    Given a subdomain s1
    And an id i1
    And a subdomain type s2
    And a job j1
    When the person declares the subdomain s1 with the id i1 and the subdomain type s2 and the job j1
    Then this product holds the subdomain s1
    And the product service keeps the subdomain s1
    And the product service completes this request

  @g16 @r16
  Scenario: A subdomain of a type outside the subdomain type form is refused
    Given a subdomain type s2
    And the subdomain type s2 does not conform to the subdomain type form
    And a subdomain s1
    When the person declares the subdomain s1 with the subdomain type s2
    Then the product service refuses this request
    And the product service names the subdomain type s2

  @g17 @r17
  Scenario: A subdomain serving a job the product does not hold is refused
    Given a job j1
    And this product does not hold the job j1
    And a subdomain s1
    When the person declares the subdomain s1 with the job j1
    Then the product service refuses this request
    And the product service names the job j1

  @g19 @r19
  Scenario: A third-party provider is declared as a bounded context no shop keeps
    Given a bounded context b1
    And an id i1
    And a subdomain s1
    When the person declares the bounded context b1 with the id i1 and the subdomain s1 and without a shop
    Then this product holds the bounded context b1
    And the product service keeps the bounded context b1
    And the product service completes this request

  @g20 @r20
  Scenario: A bounded context whose id lies outside the product is refused
    Given an id i2
    And this product has the id i2
    And an id i1
    And the id i2 does not cover the id i1
    And a bounded context b1
    When the person declares the bounded context b1 with the id i1
    Then the product service refuses this request
    And the product service names the id i2

  @g21 @r21
  Scenario: A bounded context addressing a subdomain the product does not hold is refused
    Given a subdomain s1
    And this product does not hold the subdomain s1
    And a bounded context b1
    When the person declares the bounded context b1 with the subdomain s1
    Then the product service refuses this request
    And the product service names the subdomain s1

  @g22 @r22
  Scenario: A job is assigned to the bounded context that serves it
    Given a job j1
    And a bounded context b1
    When the person assigns the job j1 to the bounded context b1
    Then the bounded context b1 holds the job j1
    And the product service keeps the job j1
    And the product service completes this request

  @g23 @r23
  Scenario: A job assigned to a bounded context is not assigned again
    Given a job j1
    And a bounded context b1
    And the bounded context b1 holds the job j1
    And a bounded context b2
    When the person assigns the job j1 to the bounded context b2
    Then the product service refuses this request
    And the product service names the job j1

  @g24 @r24
  Scenario: A product actor is mapped to the actor a bounded context calls it by
    Given a product actor p1
    And a bounded context b1
    And an actor a1
    When the person maps the product actor p1 with the bounded context b1 and the actor a1
    Then the bounded context b1 holds the product actor p1
    And the product service keeps the product actor p1
    And the product service completes this request

  @g25 @r25
  Scenario: A product actor the product does not hold is not mapped
    Given a product actor p1
    And this product does not hold the product actor p1
    When the person maps the product actor p1
    Then the product service refuses this request
    And the product service names the product actor p1

  @g26 @r26
  Scenario: A job's trace holds the requirements of the groups that serve it
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    When the person traces the job j1
    Then the product service returns the requirement r2

  @g27 @r27
  Scenario: A job's trace holds the requirements that govern the operations its requirements use
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a requirement r3
    And the requirement r3 governs the operation o1
    When the person traces the job j1
    Then the product service returns the requirement r3

  @g28 @r28
  Scenario: A job's trace holds the adapter specs that realise the port lines it reaches
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And a requirement id r3
    And the port line p1 has the requirement id r3
    And an adapter spec a1
    And the adapter spec a1 realises the requirement id r3
    When the person traces the job j1
    Then the product service returns the adapter spec a1

  @g29 @r29
  Scenario: A job's trace holds the traces of the jobs it needs
    Given a requirement group r1
    And a need n1
    And the requirement group r1 serves the need n1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And a job j1
    And the job j1 needs the need n1
    When the person traces the job j1
    Then the product service returns the requirement r2

  @g30 @r30
  Scenario: A job that no requirement group serves is not traced
    Given a job j1
    And no requirement group serves the job j1
    When the person traces the job j1
    Then the product service refuses this request
    And the product service names the job j1

  @g31 @r31
  Scenario: A job whose trace makes a port request no line awaits is coordinated by a port request
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And no property of the operation o1 refers to an operation
    And no requirement handles an operation outcome of the operation o1
    When the person traces the job j1
    Then the coordination of the job j1 is `port request`
    And the product service returns the job j1

  @g32 @r32
  Scenario: A job whose trace awaits a port's reply in a lifecycle is coordinated by a long-running process
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And an operation outcome o2
    And the operation o1 has the operation outcome o2
    And a requirement r3
    And the requirement r3 handles the operation outcome o2
    And an operation o3
    And a transition t1
    And the operation o3 performs the transition t1
    And the requirement r3 uses the operation o3
    When the person traces the job j1
    Then the coordination of the job j1 is `long-running process`
    And the product service returns the job j1

  @g33 @r33
  Scenario: A job whose trace makes compensated requests of two ports is coordinated by a saga
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And a driven port d1
    And the driven port d1 holds the operation o1
    And a property p1
    And an operation o2
    And the property p1 refers to the operation o2
    And the operation o1 has the property p1
    And the requirement r2 uses the operation o1
    And an operation o3
    And the driven port d1 holds the operation o3
    And the operation o3 has the property p1
    And the requirement r2 uses the operation o3
    When the person traces the job j1
    Then the coordination of the job j1 is `saga`
    And the product service returns the job j1

  @g34 @r34
  Scenario: A bounded context a shop keeps is declared in the product the shop has
    Given a product p1
    And a shop s1
    And the shop s1 has the product p1
    And a bounded context b1
    And an id i1
    And a subdomain s2
    When the person declares the bounded context b1 with the id i1 and the subdomain s2 and the shop s1
    Then the product p1 holds the bounded context b1
    And the product service keeps the bounded context b1
    And the product service completes this request

  @g35 @r35
  Scenario: A trace follows each provider operation an adapter spec uses
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And a requirement id r3
    And the port line p1 has the requirement id r3
    And an adapter spec a1
    And the adapter spec a1 realises the requirement id r3
    And an operation o2
    And the operation o1 uses the operation o2
    And a requirement r4
    And the requirement r4 governs the operation o2
    And a contract c1
    And the contract c1 holds the requirement r4
    And the adapter spec a1 holds the contract c1
    When the person traces the job j1
    Then the product service returns the requirement r4

  @g36 @r36
  Scenario: A trace keeps a provider's requirement whose id is a local requirement's
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    And an operation o1
    And the requirement r2 uses the operation o1
    And a port line p1
    And the port line p1 governs the operation o1
    And a requirement id r3
    And the port line p1 has the requirement id r3
    And an adapter spec a1
    And the adapter spec a1 realises the requirement id r3
    And an operation o2
    And the operation o1 uses the operation o2
    And a requirement r4
    And the requirement r4 governs the operation o2
    And a contract c1
    And the contract c1 holds the requirement r4
    And the adapter spec a1 holds the contract c1
    And the requirement r4 has the requirement id r3
    When the person traces the job j1
    Then the product service returns the requirement r4

  @g37 @r37
  Scenario: A bounded context whose id is out of the context id form is not declared
    Given an id i1
    And the id i1 does not conform to the context id form
    And a bounded context b1
    When the person declares the bounded context b1 with the id i1
    Then the product service refuses this request
    And the product service names the id i1

  @g38 @r38
  Scenario: A job is not assigned to a bounded context whose id is out of the context id form
    Given an id i1
    And a bounded context b1
    And the bounded context b1 has the id i1
    And the id i1 does not conform to the context id form
    And a job j1
    When the person assigns the job j1 to the bounded context b1
    Then the product service refuses this request
    And the product service names the id i1

  @g39 @r39
  Scenario: A job assigned to a bounded context the product does not hold is refused
    Given a bounded context b1
    And this product does not hold the bounded context b1
    And a job j1
    When the person assigns the job j1 to the bounded context b1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g41 @r41
  Scenario: A product actor is not mapped in a bounded context whose id is out of the context id form
    Given an id i1
    And a bounded context b1
    And the bounded context b1 has the id i1
    And the id i1 does not conform to the context id form
    And a product actor p1
    And an actor a1
    When the person maps the product actor p1 with the bounded context b1 and the actor a1
    Then the product service refuses this request
    And the product service names the id i1

  @g42 @r42
  Scenario: A job whose statement mentions an actor the product does not hold is refused
    Given a product actor p1
    And this product does not hold the product actor p1
    And a job statement j2
    And the job statement j2 mentions the product actor p1
    And a job j1
    When the person declares the job j1 with the job statement j2
    Then the product service refuses this request
    And the product service names the product actor p1

  @g44 @r44
  Scenario: A job whose statement's situation is one word is declared
    Given the job statement `j2` holds "When x, the developer wants y, so they can z."
    And a job statement j2
    And the job statement j2 conforms to the job statement form
    And a job j1
    And a product actor p1
    When the person declares the job j1 with the product actor p1 and the job statement j2
    Then this product holds the job j1
    And the product service keeps the job j1
    And the product service completes this request

  @g45 @r45
  Scenario: A product actor a bounded context maps is not dropped
    Given a product actor p1
    And a bounded context b1
    And the bounded context b1 holds the product actor p1
    When the person drops the product actor p1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g46 @r46
  Scenario: A subdomain is dropped from the product
    Given a subdomain s1
    When the person drops the subdomain s1
    Then this product does not hold the subdomain s1
    And the product service does not keep the subdomain s1
    And the product service completes this request

  @g47 @r47
  Scenario: A subdomain a bounded context addresses is not dropped
    Given a bounded context b1
    And a subdomain s1
    And the bounded context b1 addresses the subdomain s1
    When the person drops the subdomain s1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g48 @r48
  Scenario: A bounded context is dropped from the product
    Given a bounded context b1
    When the person drops the bounded context b1
    Then this product does not hold the bounded context b1
    And the product service does not keep the bounded context b1
    And the product service completes this request

  @g49 @r49
  Scenario: A bounded context that holds a job is not dropped
    Given a job j1
    And a bounded context b1
    And the bounded context b1 holds the job j1
    When the person drops the bounded context b1
    Then the product service refuses this request
    And the product service names the job j1

  @g50 @r50
  Scenario: A job is unassigned from a bounded context
    Given a job j1
    And a bounded context b1
    When the person unassigns the job j1 from the bounded context b1
    Then the bounded context b1 does not hold the job j1
    And the product service does not keep the job j1
    And the product service completes this request

  @g51 @r51
  Scenario: A job a bounded context does not hold is not unassigned from it
    Given a job j1
    And a bounded context b1
    And the bounded context b1 does not hold the job j1
    When the person unassigns the job j1 from the bounded context b1
    Then the product service refuses this request
    And the product service names the job j1

  @g52 @r52
  Scenario: A job is dropped from the product
    Given a job j1
    When the person drops the job j1
    Then this product does not hold the job j1
    And the product service does not keep the job j1
    And the product service completes this request

  @g53 @r53
  Scenario: A job another job needs is not dropped
    Given a job j1
    And a need n1
    And the job j1 needs the need n1
    When the person drops the need n1
    Then the product service refuses this request
    And the product service names the job j1

  @g54 @r54
  Scenario: A job a bounded context holds is not dropped
    Given a job j1
    And a bounded context b1
    And the bounded context b1 holds the job j1
    When the person drops the job j1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g55 @r55
  Scenario: A job a subdomain serves is not dropped
    Given a subdomain s1
    And a job j1
    And the subdomain s1 serves the job j1
    When the person drops the job j1
    Then the product service refuses this request
    And the product service names the subdomain s1

  @g56 @r56
  Scenario: A product actor is dropped from the product
    Given a product actor p1
    When the person drops the product actor p1
    Then this product does not hold the product actor p1
    And the product service does not keep the product actor p1
    And the product service completes this request

  @g57 @r57
  Scenario: A product actor a job has is not dropped
    Given a product actor p1
    And a job j1
    And the job j1 has the product actor p1
    When the person drops the product actor p1
    Then the product service refuses this request
    And the product service names the job j1

  @g58 @r58
  Scenario: A job's trace for an item holds the requirements of the item's groups that serve it
    Given a requirement group r1
    And an item i1
    And the item i1 holds the requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And a requirement r2
    And the requirement group r1 has the requirement r2
    When the person traces the job j1 with the item i1
    Then the product service returns the requirement r2

  @g59 @r59
  Scenario: A job the product does not hold is not assigned
    Given a job j1
    And this product does not hold the job j1
    And a bounded context b1
    When the person assigns the job j1 to the bounded context b1
    Then the product service refuses this request
    And the product service names the job j1

  @g60 @r60
  Scenario: A job whose statement mentions another actor of the product than the job's is refused
    Given a product actor p1
    And this product holds the product actor p1
    And a product actor p2
    And this product holds the product actor p2
    And a job statement j2
    And the job statement j2 mentions the product actor p2
    And a job j1
    When the person declares the job j1 with the product actor p1 and the job statement j2
    Then the product service refuses this request
    And the product service names the job statement j2

  @g61 @r61
  Scenario: A product actor of the product is not mapped to an actor the domain model does not hold
    Given a product actor p1
    And this product holds the product actor p1
    And an actor a1
    And this domain model does not hold the actor a1
    When the person maps the product actor p1 with this bounded context and the actor a1
    Then the product service refuses this request
    And the product service names the actor a1

  @g62 @r62
  Scenario: A job declared without a product actor is refused
    Given a job j1
    And a job statement j2
    When the person declares the job j1 with the job statement j2 and without a product actor
    Then the product service refuses this request

  @g63 @r63
  Scenario: A bounded context whose id is out of the context id form is not dropped
    Given an id i1
    And a bounded context b1
    And the bounded context b1 has the id i1
    And the id i1 does not conform to the context id form
    When the person drops the bounded context b1
    Then the product service refuses this request
    And the product service names the id i1

  @g64 @r64
  Scenario: A job the product does not hold is not dropped
    Given a job j1
    And this product does not hold the job j1
    When the person drops the job j1
    Then the product service refuses this request
    And the product service names the job j1

  @g65 @r65
  Scenario: A product actor the product does not hold is not dropped
    Given a product actor p1
    And this product does not hold the product actor p1
    When the person drops the product actor p1
    Then the product service refuses this request
    And the product service names the product actor p1

  @g66 @r66
  Scenario: A subdomain the product does not hold is not dropped
    Given a subdomain s1
    And this product does not hold the subdomain s1
    When the person drops the subdomain s1
    Then the product service refuses this request
    And the product service names the subdomain s1

  @g67 @r67
  Scenario: A bounded context the product does not hold is not dropped
    Given a bounded context b1
    And this product does not hold the bounded context b1
    When the person drops the bounded context b1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g68 @r68
  Scenario: A job only an item's groups serve is traced with the item
    Given a requirement group r1
    And a job j1
    And the requirement group r1 serves the job j1
    And an item i1
    And the item i1 holds the requirement group r1
    And no capability has a requirement group that serves the job j1
    When the person traces the job j1 without an item
    Then the product service refuses this request
    And the product service names the item i1

  @g69 @r69
  Scenario: A product actor is not mapped in a bounded context the product does not hold
    Given a product actor p1
    And this product holds the product actor p1
    And a bounded context b1
    And this product does not hold the bounded context b1
    And an actor a1
    When the person maps the product actor p1 with the bounded context b1 and the actor a1
    Then the product service refuses this request
    And the product service names the bounded context b1

  @g70 @r70
  Scenario: A product declared again with another id is refused
    Given an id i1
    And this product has the id i1
    And an id i2
    And this product does not have the id i2
    And a product p1
    When the person declares the product p1 with the id i2
    Then the product service refuses this request
    And the product service names the id i2

  @g71 @r71
  Scenario: A product whose id is out of the product id form is refused
    Given an id i1
    And the id i1 does not conform to the product id form
    And a product p1
    When the person declares the product p1 with the id i1
    Then the product service refuses this request
    And the product service names the id i1

  @g72 @r72
  Scenario: A product actor out of the product actor form is refused
    Given a product actor p1
    And the product actor p1 does not conform to the product actor form
    When the person declares the product actor p1
    Then the product service refuses this request
    And the product service names the product actor p1

  @g73 @r73
  Scenario: A subdomain whose id is out of the subdomain id form is refused
    Given an id i1
    And the id i1 does not conform to the subdomain id form
    And a subdomain s1
    When the person declares the subdomain s1 with the id i1
    Then the product service refuses this request
    And the product service names the id i1

  @g74 @r74
  Scenario: A product actor is not declared before the product has an id
    Given this product has no id
    And a product actor p1
    When the person declares the product actor p1
    Then the product service refuses this request
    And the product service names this product
