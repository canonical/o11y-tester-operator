"""Basic integration test for the charm."""

import yaml
from typing import Dict
from pytest_operator.plugin import OpsTest


def _charm_resources(metadata_file="charmcraft.yaml") -> Dict[str, str]:
    with open(metadata_file, "r") as file:
        metadata = yaml.safe_load(file)
    resources = {}
    for res, data in metadata["resources"].items():
        resources[res] = data["upstream-source"]
    return resources


async def test_build_and_deploy(ops_test: OpsTest, charm: str):
    """Deploy the charm."""
    assert ops_test.model is not None
    await ops_test.model.deploy(charm, "o11y-tester", resources=_charm_resources())
    await ops_test.model.wait_for_idle(apps=["o11y-tester"], status="active")
