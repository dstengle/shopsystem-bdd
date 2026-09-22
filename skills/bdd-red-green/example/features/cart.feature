Feature: Shopping cart
  So that customers can buy several things in one order, a customer can
  collect products in a cart and see what they will pay.

  @assumes-customers-buy-multiple-units
  Scenario: Add a product to an empty cart
    Given an empty cart
    And a product "Widget" priced 9.99
    When the customer adds 2 "Widget" to the cart
    Then the cart holds 2 "Widget"
    And the cart total is 19.98
