"""Collection of translators for Bluma components."""

from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator

from .components import messages


class BulmaTranslator(HTML5Translator):  # noqa: D101
    def visit_admonition(self, element, name=""):
        messages.visit_admonition(self, element, name)

    def depart_admonition(self, element=None):
        messages.depart_admonition(self, element)


def setup(app: Sphinx):  # noqa: D103
    app.set_translator("html", BulmaTranslator)
    app.set_translator("dirhtml", BulmaTranslator)
    app.setup_extension("atsphinx.bulma.components.messages")
