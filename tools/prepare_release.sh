#!/bin/bash

set -euo pipefail

# tools/prepare_release.sh

git checkout -B Release
git pull --rebase origin main
tox -e prepare-release
git push origin Release --force
