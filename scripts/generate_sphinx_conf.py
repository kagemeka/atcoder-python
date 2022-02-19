import argparse

CONTENT = """\
import os
import sys


def find_docs_root() -> str:
    filepath = os.path.abspath(__file__)
    path_chunks = filepath.split(os.path.sep)
    while path_chunks[-1] != "docs":
        path_chunks.pop()
    return os.path.sep.join(path_chunks)


sys.path.append(find_docs_root())
from _sphinx_conf import *
from _rtd_conf import *
"""


def _generate(sphinx_docs_path: str) -> None:
    with open(f"{sphinx_docs_path}/conf.py", mode="w") as f:
        f.write(CONTENT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sphinx-docs-path",
        type=str,
        default=None,
        required=True,
    )
    args = parser.parse_args()
    _generate(args.sphinx_docs_path)
