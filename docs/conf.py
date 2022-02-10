import atcoder

project = "atcoder-api"
copyright = "2022, kagemeka"
author = "kagemeka"
version = atcoder.__version__
release = atcoder.__version__
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
]
templates_path = ["_templates"]
language = "en"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "tests",
    "./**/tests/",
    "./**/_test.py",
]
html_theme = "furo"
html_static_path = ["_static"]
todo_include_todos = True
