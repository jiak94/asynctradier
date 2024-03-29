# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys

project = "asynctradier"
copyright = "2024, Jiakuan Li"
author = "Jiakuan Li"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, os.path.abspath(".."))
apidoc_module_dir = "../asynctradier"
apidoc_output_dir = "python_apis"
apidoc_excluded_paths = ["tests"]
apidoc_separate_modules = True
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinxcontrib.apidoc",
    "sphinx.ext.viewcode",
    "m2r2",
]
# autodoc_mock_imports = ["asynctradier"]
source_suffix = [".rst", ".md"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = [sphinx_rtd_theme.get_html_theme_path()]
master_doc = "index"
