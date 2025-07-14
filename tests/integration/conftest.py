#!/usr/bin/env python3
"""Conftest file for integration tests."""
# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import functools
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pytest
from pytest_operator.plugin import OpsTest

logger = logging.getLogger(__name__)

store = defaultdict(str)

REPO_ROOT = Path(__file__).parent.parent.parent

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


@pytest.fixture(scope="session", autouse=True)
def dump_logs():
    yield
    logs = Path(REPO_ROOT)/".logs"
    logs.mkdir(exist_ok=True)
    (logs/'logfile.txt').write_text("something something")
