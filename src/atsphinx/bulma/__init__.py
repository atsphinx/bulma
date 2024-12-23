"""Bluma using suite for Sphinx.."""

from sphinx.application import Sphinx

__version__ = "0.0.0"


def setup(app: Sphinx):  # noqa: D103
    app.setup_extension("atsphinx.bulma.translator")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
