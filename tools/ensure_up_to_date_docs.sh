#!/bin/bash

# checks/ensure_docs_built.sh
if git status -s src/pgrubic/rules/ | grep -qE '^(A|D)' && ! git status -s docs/ | grep -qE '^(A|D)'; then
#    git diff --name-status HEAD~1 HEAD -- docs/ | grep -E '^(A|D)'
    echo "Documentations are not up to date. Ensure docs are built."
    echo "Run 'tox -e docbuild' and commit the changes."
    exit 1
else
    echo "Documentation are up to date."
    exit 0
fi
