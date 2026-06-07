"""Standard tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from io import StringIO

    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    "html",
    confoverrides={
        "html_theme": "bulma-basic",
        "html_theme_options": {
            "bulmaswatch": "light",
        },
    },
)
def test__fallback_bulmaswatch(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    opts: dict = app.config.html_theme_options
    assert "version" in opts["bulmaswatch"]
    assert opts["bulmaswatch"]["version"] == "0.8.1"


@pytest.mark.sphinx(
    "html",
    confoverrides={
        "html_theme": "bulma-basic",
        "html_theme_options": {
            "logo_description": "Hello!",
        },
    },
)
def test__fallback_logo(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    opts: dict = app.config.html_theme_options
    assert isinstance(opts["logo"], dict)
    assert "classes" in opts["logo"]


@pytest.mark.sphinx(
    "html",
    confoverrides={
        "html_theme": "bulma-basic",
        "html_theme_options": {
            "navbar_search": True,
        },
    },
)
def test__fallback_navbar(app: SphinxTestApp, status: StringIO, warning: StringIO):
    app.build()
    opts: dict = app.config.html_theme_options
    assert isinstance(opts["navbar"], dict)
    assert opts["navbar"]["search"] is True
    assert "links" in opts["navbar"]
