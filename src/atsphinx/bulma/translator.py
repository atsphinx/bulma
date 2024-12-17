"""Collection of translators for Bluma components."""

from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator

from .components import messages


class BulmaTranslator(HTML5Translator):  # noqa: D101
    visit_admonition = messages.visit_admonition
    depart_admonition = messages.depart_admonition


def setup(app: Sphinx):  # noqa: D103
    app.set_translator("html", BulmaTranslator)
    app.set_translator("dirhtml", BulmaTranslator)
    pass
