# **pgrubic**

[![pgrubic](https://img.shields.io/badge/pgrubic-purple.svg)](https://github.com/bolajiwahab/pgrubic/)
[![PyPI - Version](https://img.shields.io/pypi/v/pgrubic)](https://pypi.org/project/pgrubic/)
[![PyPI - Status](https://img.shields.io/pypi/status/pgrubic)](https://pypi.org/project/pgrubic/)
[![PyPI - License](https://img.shields.io/pypi/l/pgrubic)](https://github.com/bolajiwahab/pgrubic/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pgrubic)](https://pypi.org/project/pgrubic/)
[![CI](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/bolajiwahab/pgrubic/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/bolajiwahab/pgrubic/tree/python-coverage-comment-action-data)
[![DOC](https://github.com/bolajiwahab/pgrubic/actions/workflows/doc.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/doc.yml)
[![release](https://github.com/bolajiwahab/pgrubic/actions/workflows/release.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/release.yml)
[![PyPI Total Downloads](https://img.shields.io/pepy/dt/pgrubic)](https://pepy.tech/projects/pgrubic)
[![CodeQL](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/pgrubic?artifact_id=tar-gz)](https://socket.dev/pypi/package/pgrubic/overview/)
![Dependency Review](https://img.shields.io/badge/Dependency%20Review-enabled-deepgreen)

A PostgreSQL linter and formatter for schema migrations and design best practices.

## Features

- Over 100+ rules
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements)
- River style code formatting for DML statements
- Almost identical stying with **pg_dump** for DDL statements
- Python 3.12+ compatibility
- Automatic caching to avoid reformatting unchanged files
- Violations suppression, statement level, and file level

## Requirements

pgrubic is built upon the shoulders of:

- [pglast](https://github.com/lelit/pglast) - Python bindings to libpg_query
- [libpg_query](https://github.com/pganalyze/libpg_query) - PostgreSQL parser outside of the server environment
