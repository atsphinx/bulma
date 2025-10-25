"""Entrypoint of theme."""

from pathlib import Path
from typing import Union

from bs4 import BeautifulSoup, Tag
from docutils import nodes
from sphinx.application import Sphinx

from ... import __version__
from ...components.navbar import register_root_toctree_dict

here = Path(__file__).parent


def rebuild_toc(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: Union[nodes.document, None],
):
    """Generate new toc content html from original toc.

    New toc has 'menu-list' property in 'class' attribute
    to enable style of Buluma's list.
    """
    if "toc" not in context:
        return
    soup = BeautifulSoup(context["toc"], "html.parser")
    toc_ul = soup.find("ul")
    if isinstance(toc_ul, Tag):
        toc_ul.attrs.setdefault("class", [])
        if isinstance(toc_ul.attrs["class"], str):
            toc_ul.attrs["class"] = [toc_ul.attrs["class"]]
        toc_ul.attrs["class"].append("menu-list")
    context["toc_for_bulma"] = str(soup)


def setup(app: Sphinx):  # noqa: D103
    app.add_html_theme("bulma-basic", str(here))
    app.connect("html-page-context", register_root_toctree_dict)
    app.connect("html-page-context", rebuild_toc)
    app.setup_extension("atsphinx.bulma")
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
