# o11y-tester

This repository is used to test the Observability team's [workflows](https://github.com/canonical/observability) before they are used across all other repos.

## Testing

This project uses pytest for testing, including support for BDD (Behavior-Driven Development) using pytest-bdd.

### BDD Feature Files

Feature files are located in `tests/features/` and use Gherkin syntax to describe test scenarios. These feature files can be implemented by both unit tests and integration tests, with each test type implementing different scenarios from the same feature file.
