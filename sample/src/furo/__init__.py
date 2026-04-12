#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.application import Sphinx


def setup(app: Sphinx):
    """Entrypoint as Sphinx extension."""
    from sphinx.util import logging

    logging.getLogger(__name__).debug("Hello world")
    return {
        "version": "0.0.0",
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
