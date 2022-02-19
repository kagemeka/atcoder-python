import os

import yaml

CFD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(f"{CFD}/..")
RTD_YAML_PATH = f"{ROOT}/.readthedocs.yaml"


def get_sphinx_docs_directory() -> str:
    with open(RTD_YAML_PATH, mode="r") as f:
        content = yaml.safe_load(f)
    conf_path = content.get("sphinx").get("configuration")
    docs_path = os.path.abspath(os.path.join(ROOT, os.path.dirname(conf_path)))
    return docs_path
