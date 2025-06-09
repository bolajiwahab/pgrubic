#!/bin/bash

set -euo pipefail

# tools/ensure_up_to_date_docs.sh

if git diff --quiet -- docs/ && [ -z "$(git ls-files --others --exclude-standard docs/)" ]; then
    echo "Documentation are up to date."
    exit 0
else
    echo "Documentations are not up to date. Ensure docs are rebuilt."
    echo "Run 'tox -e docbuild' and commit the changes."
    exit 1
fi
