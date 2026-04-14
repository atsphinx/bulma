"""Configuration for documents."""

import sys
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import StringList

from atsphinx.bulma import __version__ as version

# -- Project information
project = "atsphinx-bulma using sphinx-themes.org"
copyright = "2025, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for i18n
gettext_compact = False
locale_dirs = ["_locales"]

# -- Options for HTML output
html_logo = "https://attakei.net/_static/images/icon-attakei@2x.png"
html_theme = "bulma-basic"
html_theme_options = {
    "color_mode": "light",
    "bulmaswatch": "pulse",
    "logo_description": "This is documentation of atsphinx-bulma.",
    "navbar_icons": [
        {
            "label": "",
            "icon": "fa-brands fa-solid fa-github fa-2x",
            "url": "https://github.com/atsphinx/bulma",
        }
    ],
    "navbar_search": True,
    "navbar_show_hidden_toctree": True,
    "layout": {
        "index": [
            {"type": "space", "size": 1},
            {"type": "main", "size": 10},
            {"type": "space", "size": 1},
        ],
        "**": [
            {"type": "main", "size": 10},
            {"type": "sidebar", "size": 2},
        ],
    },
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
    "custom.css",
]
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_sidebars = {
    "**": [
        "sidebar/logo.html",
        "sidebar/line.html",
        "sidebar/localtoc.html",
    ],
}


todo_include_todos = True


# ------
# From https://github.com/sphinx-themes/sphinx-themes.org/blob/master/src/templates/conf.template.py
# ------
sys.path.append(
    str(Path(__file__).parent / "sphinx-themes" / "sample-docs" / "kitchen-sink")
)
extlinks = {
    "pypi": ("https://pypi.org/project/%s/", "%s"),
}

rst_prolog = """
.. |theme_package| replace:: atsphinx-bulma
.. |theme_pypi_link| replace:: :pypi:`atsphinx-bulma`
.. |theme_name| replace:: bulma-basic
.. |theme_display| replace:: Bulma
.. |theme_documentation_message| replace:: You can find this theme's documentation at https://atsphinx.github.io/bulma/.
"""

theme_configuration = ""


class ThemeConfigurationDirective(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        container = nodes.literal_block()
        translated_content = StringList(theme_configuration.splitlines(keepends=False))
        self.state.nested_parse(translated_content, 0, container)
        return [container]


class ThemeInstallDirective(Directive):
    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self):
        container = nodes.literal_block()
        translated_content = StringList(["$ pip install {{ theme.pypi_package }}"])
        self.state.nested_parse(translated_content, 0, container)
        return [container]


def setup(app):
    app.add_directive("theme-configuration", ThemeConfigurationDirective)
    app.add_directive("theme-install", ThemeInstallDirective)
