# -*- coding: utf-8 -*-
#
# PV ICE documentation build configuration file, April 2020
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

import sys
import os

"""
# Mock modules so RTD works
try:
    from mock import Mock as MagicMock
except ImportError:
    from unittest.mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return Mock()

MOCK_MODULES = []
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)
"""
import pandas as pd
pd.show_versions()

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../sphinxext'))
sys.path.insert(0, os.path.abspath('../../../'))




# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
#    'IPython.sphinxext.ipython_directive',
#    'IPython.sphinxext.ipython_console_highlighting',
    'sphinx.ext.doctest',
    #'autoapi.extension',
    'sphinx.ext.todo'
]
   


# Document Python Code
#autodoc_mock_imports = ['bs4', 'requests']
#autoapi_type = 'python'
#autoapi_dirs = '../../../PV_ICE'

napoleon_use_rtype = False  # group rtype on same line together with return

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'PV ICE'
copyright = '2020, NREL'
author = 'Silvana Ayala, Heather Mirletz'
release = '0.1.0'
version = '0.1.0'  

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version.
# The full version, including alpha/beta/rc tags.

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['whatsnew/*', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

autosummary_generate = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# on_rtd is whether we are on readthedocs.org

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'PV_ICEdoc'

# A workaround for the responsive tables always having annoying scrollbars.
def setup(app):
    app.add_css_file("no_scrollbars.css")
    #app.add_stylesheet("no_scrollbars.css")

    
"""    
# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('index', 'PV_ICE.tex', u'PV_ICE\\_Python Documentation',
   u'NREL, github contributors', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True
"""
# extlinks alias
extlinks = {'issue': ('https://github.com/NREL/PV_ICE/issues/%s', 'GH'),
            'pull': ('https://github.com/NREL/PV_ICE/pull/%s', 'GH'),
            'wiki': ('https://github.com/NREL/PV_ICE/wiki/%s', 'wiki '),
            'doi': ('http://dx.doi.org/%s', 'DOI: '),
            'ghuser': ('https://github.com/%s', '@')}
"""
# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'PV_ICE', u'PV_ICE Documentation',
     [u'NREL, github contributors'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'PV_ICE', u'PV_ICE Documentation',
   u'NREL, github contributors', 'PV_ICE', 'One line description of project.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.7/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
}

nbsphinx_allow_errors = True

ipython_warning_is_error = False
"""
