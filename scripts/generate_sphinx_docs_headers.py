import os
import shutil
import sys

sys.path.append(".")
from scripts._docs_util import ROOT, get_sphinx_docs_directory

SPHINX_DOCS_HEADER = "AtCoder"


def _remove_current_docs(docs_path: str) -> None:
    try:
        shutil.rmtree(docs_path)
    except Exception as e:
        pass
    finally:
        pass


def _generate_conf(docs_path: str) -> None:
    from scripts.generate_sphinx_conf import _generate

    _generate(docs_path)


def sphinx_apidoc(src_path: str, docs_path: str) -> None:
    print(f"{src_path}/")
    command = " ".join(
        [
            "poetry run sphinx-apidoc",
            "-d 2",
            f"-H {SPHINX_DOCS_HEADER}",
            "--follow-links",
            "--full",
            "--separate",
            f"-o {docs_path}",
            "-s rst",
            f"{src_path}",
            f"{src_path}/**/*_test.py",
            f"{src_path}/**/tests/",
            f"{src_path}/**/test_*.py",
            f"{src_path}/**/_test_*.py",
        ]
    )
    os.system(command)
    # full options
    # https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html


def generate() -> None:
    docs_path = get_sphinx_docs_directory()
    _remove_current_docs(docs_path)
    sphinx_apidoc(f"{ROOT}/src", docs_path)
    _generate_conf(docs_path)


if __name__ == "__main__":
    generate()
