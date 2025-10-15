#!/usr/bin/env python3
"""Conftest file for integration tests."""
# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import functools
import logging
import os
from collections import defaultdict
from datetime import datetime

import jubilant
import pytest
from helpers import TfDirManager
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
def ca_model():
    keep_models: bool = os.environ.get("KEEP_MODELS") is not None
    with jubilant.temp_model(keep=keep_models) as juju:
        yield juju


@pytest.fixture(scope="module")
def cos_model():
    keep_models: bool = os.environ.get("KEEP_MODELS") is not None
    with jubilant.temp_model(keep=keep_models) as juju:
        yield juju


@pytest.fixture(scope="module")
def tf_manager(tmp_path_factory):
    base = tmp_path_factory.mktemp("terraform_base")
    return TfDirManager(base)
