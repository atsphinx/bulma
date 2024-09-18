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
html_theme = "bulma_basic"
html_theme_options = {
    "bulmaswatch": "flatly",
}
html_static_path = ["_static"]
