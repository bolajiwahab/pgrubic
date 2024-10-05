#!/bin/bash

# checks/ensure_docs_built.sh
if git diff --cached --quiet -- docs/; then
#    git diff --name-status HEAD~1 HEAD -- docs/ | grep -E '^(A|D)'
    echo "Documentation are up to date."
    exit 0
else
    echo "Documentations are not up to date. Ensure docs are built."
    echo "Run 'tox -e docbuild' and commit the changes."
    exit 1
fi
