# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from pallets_sphinx_themes import ProjectLink

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'ratbag-emu'
copyright = '2020, Filipe Laíns'
author = 'Filipe Laíns'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
    'pallets_sphinx_themes',
    'recommonmark',
]

# TODO: Use m2r to include the README.md instead of recommonmark. Currently waiting for a m2r release.

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    'hid-tools': ('https://pkgbuild.com/~ffy00/documentation/hid-tools/', None)
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'flask'

html_context = {
    "project_links": [
        ProjectLink("Source Code", "https://github.com/libratbag/ratbag-emu/"),
        ProjectLink("Issue Tracker", "https://github.com/libratbag/ratbag-emu/issues/"),
        ProjectLink("libratbag project", "https://github.com/libratbag/libratbag"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
