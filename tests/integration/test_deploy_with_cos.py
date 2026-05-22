"""Integration test: deploy o11y-tester alongside a running COS deployment."""

import os
from typing import Dict

import pytest
import yaml
from pytest_operator.plugin import OpsTest

pytestmark = pytest.mark.skipif(
    "OBS_STACK_PATH" not in os.environ,
    reason="OBS_STACK_PATH not set; skip (run via tox -e cos-integration)",
)


def _charm_resources(metadata_file: str = "charmcraft.yaml") -> Dict[str, str]:
    with open(metadata_file, "r") as file:
        metadata = yaml.safe_load(file)
    return {res: data["upstream-source"] for res, data in metadata["resources"].items()}


async def test_deploy_alongside_cos(ops_test: OpsTest, charm: str, cos_deployed: str):
    """Deploy the tester charm in the same model as a running COS and verify it becomes active.

    The cos_deployed fixture (from conftest.py) deploys the full COS stack to the test model
    before this test runs. This test then deploys the tester charm into that same model and
    asserts it reaches active status, confirming the two deployments can coexist.
    """
    assert ops_test.model is not None
    await ops_test.model.deploy(charm, "o11y-tester", resources=_charm_resources())
    await ops_test.model.wait_for_idle(apps=["o11y-tester"], status="active", timeout=300)
