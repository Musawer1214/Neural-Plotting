#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: bash ../tikzmake.sh <basename>" >&2
    exit 1
fi

name="$1"
python_bin="${PYTHON_BIN:-python}"

if ! command -v "$python_bin" >/dev/null 2>&1; then
    echo "Python executable not found: $python_bin" >&2
    exit 1
fi

"$python_bin" "${name}.py"
pdflatex -interaction=nonstopmode -halt-on-error "${name}.tex"

rm -f "${name}.aux" "${name}.log" "${name}.vscodeLog"

if [[ "${TIKZMAKE_CLEAN_TEX:-0}" == "1" ]]; then
    rm -f "${name}.tex"
fi

if [[ "$OSTYPE" == "darwin"* ]] && command -v open >/dev/null 2>&1; then
    open "${name}.pdf"
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${name}.pdf"
fi
