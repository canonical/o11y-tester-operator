#!/usr/bin/env python3
"""Conftest file for integration tests."""
# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import asyncio
import functools
import json
import logging
import os
from collections import defaultdict
from datetime import datetime

import pytest
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

store = defaultdict(str)


def timed_memoizer(func):
    """Cache the result of a function."""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        fname = func.__qualname__
        logger.info("Started: %s" % fname)
        start_time = datetime.now()
        if fname in store.keys():
            ret = store[fname]
        else:
            logger.info("Return for {} not cached".format(fname))
            ret = await func(*args, **kwargs)
            store[fname] = ret
        logger.info("Finished: {} in: {} seconds".format(fname, datetime.now() - start_time))
        return ret

    return wrapper


@pytest.fixture(scope="module")
@timed_memoizer
async def charm(ops_test: OpsTest) -> str:
    """Charm used for integration testing."""
    if charm_file := os.environ.get("CHARM_PATH"):
        return str(charm_file)

    charm = await ops_test.build_charm(".")
    assert charm
    return str(charm)


@pytest.fixture(scope="module")
async def cos_deployed(ops_test: OpsTest):
    """Deploy COS to the test model via the observability-stack Terraform module.

    Reads OBS_STACK_PATH from the environment (defaults to "observability-stack") to find the
    checked-out observability-stack repository. Deploys COS in monolithic topology with seaweedfs
    as the storage backend, then waits until all COS applications reach active status.
    """
    assert ops_test.model is not None

    obs_stack_path = os.environ.get("OBS_STACK_PATH", "observability-stack")
    tf_dir = os.path.join(obs_stack_path, "terraform", "cos-dev")
    model_name = ops_test.model_name

    # Resolve the model UUID via the juju CLI (same approach as the deploy-cos workflow)
    proc = await asyncio.create_subprocess_exec(
        "juju", "show-model", model_name, "--format", "json",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    assert proc.returncode == 0, f"juju show-model failed: {stderr.decode()}"
    model_uuid = json.loads(stdout)[model_name]["model-uuid"]

    logger.info("Deploying COS to model %s (uuid=%s) via Terraform", model_name, model_uuid)

    proc = await asyncio.create_subprocess_exec("terraform", "init", cwd=tf_dir)
    assert (await proc.wait()) == 0, "terraform init failed"

    proc = await asyncio.create_subprocess_exec(
        "terraform", "apply", "-auto-approve",
        f"-var=model_uuid={model_uuid}",
        "-var=topology=monolithic",
        "-var=storage_backend=seaweedfs",
        cwd=tf_dir,
    )
    assert (await proc.wait()) == 0, "terraform apply failed"

    logger.info("Waiting for all COS applications to reach active status (timeout: 30m)")
    proc = await asyncio.create_subprocess_exec(
        "juju", "wait-for", "model", model_name,
        "--timeout", "30m",
        "--query", "forEach(applications, app => app.status == \"active\")",
    )
    assert (await proc.wait()) == 0, "COS failed to reach active state within 30 minutes"

    logger.info("COS is active in model %s", model_name)
    yield model_name
