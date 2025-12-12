# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

"""Unit tests for silly calculator using BDD."""

from pytest_bdd import given, parsers, scenario, then, when


class SillyCalculator:
    """A silly calculator for demonstration purposes."""

    def __init__(self):
        """Initialize the calculator."""
        self.result = 0

    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        self.result = a + b
        return self.result


@scenario("../features/silly_calculator.feature", "Add two numbers")
def test_add_two_numbers():
    """Test the addition scenario from the feature file."""
    pass


@given("I have a calculator")
def calculator():
    """Create a calculator instance."""
    return SillyCalculator()


@when(parsers.parse("I add {a:d} and {b:d}"))
def add_numbers(calculator, a, b):
    """Add two numbers using the calculator."""
    calculator.add(a, b)


@then(parsers.parse("the result should be {expected:d}"))
def check_result(calculator, expected):
    """Verify the result matches the expected value."""
    assert calculator.result == expected
