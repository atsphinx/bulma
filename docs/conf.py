"""Configuration for documents."""

from atsphinx.bulma import __version__ as version

# -- Project information
project = "atsphinx-bulma"
copyright = "2024, Kazuya Takei"
author = "Kazuya Takei"
release = version

# -- General configuration
extensions = [
    "sphinx.ext.todo",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output
html_theme = "bulma-basic"
html_theme_options = {
    "color_mode": "light",
    "bulmaswatch": "pulse",
    "sidebar_position": "right",
    "navbar_icons": [
        {
            "label": "",
            "icon": "fa-brands fa-solid fa-github fa-2x",
            "url": "https://github.com/atsphinx/bulma",
        }
    ],
}
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_title = f"{project} v{release}"
html_static_path = ["_static"]
html_sidebars = {
    "**": [
        "sidebar/searchbox.html",
        "sidebar/localtoc.html",
        "navigation.html",
    ]
}

# -- Options for extensions
# sphinx.ext.todo
todo_include_todos = True
