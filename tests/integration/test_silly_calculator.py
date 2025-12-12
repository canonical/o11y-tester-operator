# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests for silly calculator using BDD."""

from pytest_bdd import given, parsers, scenario, then, when


class SillyCalculator:
    """A silly calculator for demonstration purposes."""

    def __init__(self):
        """Initialize the calculator."""
        self.result = 0

    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers."""
        self.result = a * b
        return self.result


@scenario("../features/silly_calculator.feature", "Multiply two numbers")
def test_multiply_two_numbers():
    """Test the multiplication scenario from the feature file."""
    pass


@given("I have a calculator")
def calculator():
    """Create a calculator instance."""
    return SillyCalculator()


@when(parsers.parse("I multiply {a:d} and {b:d}"))
def multiply_numbers(calculator, a, b):
    """Multiply two numbers using the calculator."""
    calculator.multiply(a, b)


@then(parsers.parse("the result should be {expected:d}"))
def check_result(calculator, expected):
    """Verify the result matches the expected value."""
    assert calculator.result == expected
