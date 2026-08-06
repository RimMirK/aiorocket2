import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

project = "aiorocket2"
author = "RimMirK"
release = "2.0.6"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_design",
]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "inherited-members": True,
}
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_title = "aiorocket2"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_logo = "../.github/logo+name-lt.png"
html_favicon = "../.github/logo_round.png"
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2563eb",
        "color-brand-content": "#1d4ed8",
    },
    "dark_css_variables": {
        "color-brand-primary": "#60a5fa",
        "color-brand-content": "#93c5fd",
    },
}

master_doc = "index"
