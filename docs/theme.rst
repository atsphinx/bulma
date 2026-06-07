===========
Using theme
===========

Overview
========

This provides theme to display contents designed by Bulma.

Requirements
============

This does not have extra requirements.
You can use soon after install atsphinx-bulma.

Usage
=====

.. code-block:: python
   :caption: conf.py

   html_theme = "bulma-basic"

Full options
============

There are full defined options and default values.

.. literalinclude:: ../src/atsphinx/bulma/themes/bulma_basic/theme.toml
   :language: toml
   :lines: 12-

Details
=======

``navbar.links``
----------------

``navbar.icons``
----------------

``layout``
----------

You can manage layout of content layer by configure ``layout`` in ``html_theme_options``.

.. todo:: TBD

.. code-block:: json

   {
     "**": [
       {
         "type": "sidebar",
         "size": 2
       },
       {
         "type": "main",
         "size": 8
       },
       {
         "type": "space",
         "size": 2
       },
     ]
   }

Example
=======

This is settings of this document.

.. literalinclude:: conf.py
   :language: python
   :lines: 36-64
