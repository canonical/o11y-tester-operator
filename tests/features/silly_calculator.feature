# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

Feature: Silly Calculator
  As a silly mathematician
  I want to perform silly calculations
  So that I can test BDD with pytest-bdd

  Scenario: Add two numbers
    Given I have a calculator
    When I add 5 and 3
    Then the result should be 8

  Scenario: Multiply two numbers
    Given I have a calculator
    When I multiply 4 and 7
    Then the result should be 28
