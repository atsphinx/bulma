"""Translator for messages (from admonition)."""

from docutils import nodes
from sphinx.locale import admonitionlabels
from sphinx.writers.html5 import HTML5Translator

MESSAGE_CLASSES = {
    # docutils admonition's types
    "attention": "is-warning",
    "caution": "is-warning",
    "danger": "is-danger",
    "error": "is-danger",
    "hint": "is-info",
    "important": "is-info",
    "note": "is-info",
    "tip": "is-info",
    "warning": "is-warning",
    # Sphinx extra admonitions
    "Todo": "is-link",
}
"""Mapping for admonition types and bulma color names.

:ref: https://www.docutils.org/docs/ref/rst/directives.html#specific-admonitions
"""


def visit_admonition(self: HTML5Translator, node: nodes.admonition, name: str = ""):  # noqa: D103
    if isinstance(node.children[0], nodes.title):
        msg_title = node.pop(0).astext()
        msg_class = MESSAGE_CLASSES.get(msg_title, "")
    else:
        msg_title = admonitionlabels[name]
        msg_class = MESSAGE_CLASSES.get(name, "")
    self.body.append(f'<article class="message {msg_class}">')
    self.body.append(f"""
      <div class="message-header">
        <p>{msg_title}</p>
      </div>
    """)
    self.body.append('  <div class="message-body">')


def depart_admonition(self: HTML5Translator, node: nodes.admonition):  # noqa: D103
    self.body.append("  </div>")
    self.body.append("</article>")
