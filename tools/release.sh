#!/bin/bash

set -euo pipefail

# tools/release.sh
#
# Bumps the version and changelog on the default branch, then pushes the release commit
# and its tag, which starts the release workflow.

cd -- "$(dirname -- "$0")/.."

if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
    echo "Commit or stash your changes before preparing a release." >&2
    exit 1
fi

git remote set-head origin --auto >/dev/null
branch=$(git symbolic-ref --short refs/remotes/origin/HEAD)
branch=${branch#origin/}

git switch "${branch}"
git pull --ff-only --tags origin "${branch}"
uv run --locked --no-build --only-group tooling tox -e prepare-release
git push --atomic --follow-tags origin "${branch}"
