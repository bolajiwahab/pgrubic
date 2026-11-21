#!/bin/bash

set -euo pipefail

# tools/release_preview.sh
#
# Shows the version, tag and changelog entry the next release would create from the
# current checkout, without changing anything.

cd -- "$(dirname -- "$0")/.."

uv run --locked --no-build --only-group tooling tox -qq -e release-preview
