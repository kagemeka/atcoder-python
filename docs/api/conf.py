import os
import sys


def find_docs_root() -> str:
    filepath = os.path.abspath(__file__)
    path_chunks = filepath.split(os.path.sep)
    while path_chunks[-1] != "docs":
        path_chunks.pop()
    return os.path.sep.join(path_chunks)


sys.path.append(find_docs_root())
from _rtd_conf import *
from _sphinx_conf import *
