"""Entrypoint of theme."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging

from ... import __version__
from ...components import menu
from ...components.navbar import register_root_toctree_dict

if TYPE_CHECKING:
    from typing import Any


here = Path(__file__).parent
logger = logging.getLogger(__name__)


def append_styling_filters(app: Sphinx):
    """Append custom filters to update content for enabling Bulma styles."""
    if hasattr(app.builder, "templates"):
        app.builder.templates.environment.filters["set_menu_list"] = menu.append_style


def select_layout(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict[str, Any],
    doctree: nodes.document | None = None,
):
    """Pick layout of target page."""
    # TODO: Test it!!
    DEFAULT_LAYOUT = {
        "**": [
            {"type": "sidebar", "size": 2},
            {"type": "main", "size": 10},
        ]
    }
    layouts = app.config.html_theme_options.get("layout", DEFAULT_LAYOUT)
    for key, settings in layouts.items():
        regex = re.compile(fnmatch.translate(key))
        if regex.match(pagename):
            context["bulma_layout"] = settings
            break


class LinkProperty(TypedDict):
    """Properties of ``theme_options["navbar"]["links"][]``."""

    title: str
    """Title text of link."""
    url: str
    """URL to go."""


class IconProperty(TypedDict):
    """Properties of ``theme_options["navbar"]["icons"][]``."""

    icon: str
    """Font awesome class to render icon."""
    label: str
    """Label text of icon."""
    url: str
    """URL to go."""


class LayoutProperty(TypedDict):
    """Columns property."""

    type: str
    size: int


class BulmaswatchOptions(TypedDict):
    """Part of options for using Bulmaswatch."""

    theme: str | bool | None
    """Color theme."""
    version: str
    """Version test of Bulmaswatch."""


class LogoOptions(TypedDict):
    """Part of options for logo component."""

    classes: str
    """Css classes for logo container."""

    description: str
    """Descriptin text for logo."""


class NavbarOptions(TypedDict):
    """Part of options for navbar component."""

    links: list[LinkProperty]
    search: bool
    icons: list[IconProperty]
    show_hidden_toctree: bool


class ThemeOptions(TypedDict):
    """Options for theme."""

    bulma_version: str
    bulmaswatch: BulmaswatchOptions | str | None
    color_mode: str
    logo: LogoOptions
    navbar: NavbarOptions
    show_theme_credit: bool
    layout: dict[str, list[LayoutProperty]]
    # Deprecated properties
    bulmaswatch_version: str
    logo_class: str
    logo_description: str
    navbar_links: list[str]
    navbar_search: bool
    navbar_icons: list[IconProperty]
    navbar_show_hidden_toctree: bool


def build_theme_options(app: Sphinx):
    """Regenerate application's ``html_theme_options``.

    This function has two roles:

    * Add default values into nested properties.
    * Inject values from deprecated properties.
    """
    if app.builder.format != "html":
        return
    config = app.config
    if config.html_theme != "bulma-basic":
        return
    user_opts: ThemeOptions = config.html_theme_options
    opts: ThemeOptions = app.builder.theme._options.copy()
    deprecated = set()

    # bulmaswatch
    if isinstance(user_opts.get("bulmaswatch", None), str):
        opts["bulmaswatch"]["theme"] = user_opts["bulmaswatch"]
        deprecated.add("bulmaswatch")
    if "bulmaswatch_version" in user_opts:
        opts["bulmaswatch"]["version"] = user_opts["bulmaswatch_version"]
        deprecated.add("bulmaswatch_version")
    # logo
    user_opts.setdefault("logo", opts["logo"])
    if user_opts.get("logo_class", None) is not None:
        user_opts["logo"]["classes"] = user_opts["logo_class"]
        deprecated.add("logo_class")
    if user_opts.get("logo_description", None) is not None:
        user_opts["logo"]["description"] = user_opts["logo_description"]
        deprecated.add("logo_description")
    opts["logo"] = user_opts["logo"]
    # navbar
    user_opts.setdefault("navbar", opts["navbar"])
    for k in {"links", "search", "icons", "show_hidden_toctree"}:
        key = f"navbar_{k}"
        if user_opts.get(key, None) is not None:
            user_opts["navbar"][k] = user_opts[key]
            deprecated.add(key)
    opts["navbar"] = user_opts["navbar"]

    if deprecated:
        logger.warning(
            f"conf.py uses deprecated values in 'html_theme_options'. migrate them: {', '.join(deprecated)}"
        )

    # Remap
    config.html_theme_options = opts


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("builder-inited", append_styling_filters)
    app.connect("builder-inited", build_theme_options)
    app.connect("html-page-context", register_root_toctree_dict)
    app.connect("html-page-context", select_layout)
    app.setup_extension("atsphinx.bulma")
    app.setup_extension("atsphinx.bulma.layout.hero")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
