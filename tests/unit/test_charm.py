# Copyright 2024 Zeus
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

from ops import testing

from charm import CharmTestCharm


def test_config_changed_valid_cannot_connect():
    """Test a config-changed event when the config is valid but the container cannot be reached.

    We expect to end up in MaintenanceStatus waiting for the deferred event to
    be retried.
    """
    # Arrange:
    ctx = testing.Context(CharmTestCharm)
    container = testing.Container("agent", can_connect=False)
    state_in = testing.State(containers={container}, config={"log-level": "debug"})

    # Act:
    state_out = ctx.run(ctx.on.config_changed(), state_in)

    # Assert:
    assert isinstance(state_out.unit_status, testing.MaintenanceStatus)


def test_config_changed_invalid():
    """Test a config-changed event when the config is invalid."""
    # Arrange:
    ctx = testing.Context(CharmTestCharm)
    container = testing.Container("agent", can_connect=True)
    invalid_level = "foobar"
    state_in = testing.State(containers={container}, config={"log-level": invalid_level})

    # Act:
    state_out = ctx.run(ctx.on.config_changed(), state_in)

    # Assert:
    assert isinstance(state_out.unit_status, testing.BlockedStatus)
    assert invalid_level in state_out.unit_status.message
