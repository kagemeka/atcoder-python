#!/bin/bash

get_current_file_directory() {
    file_abs_path="$(readlink -f "${BASH_SOURCE[0]}")"
    directory_path="$(dirname "${file_abs_path}")"
    echo "${directory_path}"
}

root=$(dirname "$(get_current_file_directory)")

poetry run python "$root"/scripts/generate_sphinx_docs_headers.py
