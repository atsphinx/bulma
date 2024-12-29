"""Entrypoint of theme."""

from pathlib import Path

from sphinx.application import Sphinx

from ...components.navbar import register_root_toctree_dict

here = Path(__file__).parent


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("html-page-context", register_root_toctree_dict)
    app.setup_extension("atsphinx.bulma")
