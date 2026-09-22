from decimal import Decimal

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from cart import Cart

scenarios("../features/cart.feature")


@pytest.fixture
def catalogue():
    return {}


@given("an empty cart", target_fixture="cart")
def empty_cart():
    return Cart()


@given(parsers.parse('a product "{name}" priced {price}'))
def product(catalogue, name, price):
    catalogue[name] = Decimal(price)


@when(parsers.parse('the customer adds {qty:d} "{name}" to the cart'))
def add_to_cart(cart, catalogue, qty, name):
    cart.add(name, catalogue[name], qty)


@then(parsers.parse('the cart holds {qty:d} "{name}"'))
def cart_holds(cart, qty, name):
    assert cart.quantity_of(name) == qty


@then(parsers.parse("the cart total is {total}"))
def cart_total(cart, total):
    assert cart.total() == Decimal(total)
