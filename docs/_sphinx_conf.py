# https://www.sphinx-doc.org/en/master/usage/configuration.html

import enum
import typing

import sphinx_theme_pd

project = "AtCoder"
author = "Hiroshi Tsuyuki <kagemeka1@gmail.com>"
copyright = f"2022, {author}"


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",  # enable numpy/google documentation styles.
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
# relative to conf.py


language = "en"
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language


exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# relative to source directory.


# https://sphinx-themes.org/#themes
class _HtmlTheme(enum.Enum):
    ALABASTER = "alabaster"
    FURO = "furo"
    SPHINX_RTD_THEME = "sphinx_rtd_theme"
    PYTHON_DOCS_THEME = "python_docs_theme"
    SPHINX_THEME_PD = "sphinx_theme_pd"
    SPHINX_BOOK_THEME = "sphinx_book_theme"
    PYDATA_SPHINX_THEME = "pydata_sphinx_theme"


html_theme = _HtmlTheme.FURO.value

html_theme_path: typing.List[str] = [
    sphinx_theme_pd.get_html_theme_path(),
]
# relative to conf.py

html_static_path = ["_static"]
# relative to conf.py


todo_include_todos = True
