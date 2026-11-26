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

  @g14 @r14
  Scenario: A job whose statement's situation holds a comma is declared
    Given the job statement `j2` holds "When a change is wanted, reviewed and agreed, the developer wants it specified, so they can build it."
    And a job statement j2
    And the job statement j2 conforms to the job statement form
    And a job j1
    When the person declares the job j1 with the job statement j2
    Then this product holds the job j1
    And the product service keeps the job j1
    And the product service completes this request
