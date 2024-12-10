#!/usr/bin/env python3
# Copyright 2024 Canonical
# See LICENSE file for licensing details.

"""Tester charm for Observability things."""

import ops
from ops.model import ActiveStatus

from typing import Any


class TesterCharm(ops.CharmBase):
    """Tester charm that doesn't do anything."""

    def __init__(self, *args: Any):
        """Initialize the tester charm."""
        super().__init__(*args)
        self.unit.status = ActiveStatus()
