import os
import sys

sys.path.append(".")
from scripts._docs_util import ROOT, get_sphinx_docs_directory


def build() -> None:
    docs_path = get_sphinx_docs_directory()
    make_base = f"poetry run make --directory={docs_path}"
    command = " ".join(
        [
            f"{make_base} clean &&",
            f"{make_base} html",
        ]
    )
    os.system(command)


if __name__ == "__main__":
    build()
