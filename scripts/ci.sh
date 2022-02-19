#!/bin/bash

get_current_file_directory() {
    file_abs_path="$(readlink -f "${BASH_SOURCE[0]}")"
    directory_path="$(dirname "${file_abs_path}")"
    echo "${directory_path}"
}

root=$(dirname "$(get_current_file_directory)")

"$root"/scripts/update_env.sh
"$root"/scripts/chmod_exec.sh
"$root"/scripts/precommit.sh
"$root"/scripts/format.sh
"$root"/scripts/lint.sh
"$root"/scripts/testing.sh
# "$root"/scripts/generate_sphinx_docs_headers.sh
# "$root"/scripts/build_sphinx_docs.sh
