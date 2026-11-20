# **pgrubic**

[![Try it online](https://img.shields.io/badge/%F0%9F%9A%80%20Try%20it-online-2ea44f)](https://online.pgrubic.azellar.com)
[![PyPI - Version](https://img.shields.io/pypi/v/pgrubic)](https://pypi.org/project/pgrubic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pgrubic)](https://pypi.org/project/pgrubic/)
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![Windows](https://img.shields.io/badge/Windows-0078D4?logo=windows&logoColor=white)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![PyPI - License](https://img.shields.io/pypi/l/pgrubic)](https://github.com/bolajiwahab/pgrubic/blob/main/LICENSE)
[![PyPI Total Downloads](https://img.shields.io/pepy/dt/pgrubic)](https://pepy.tech/projects/pgrubic)
[![CI](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/bolajiwahab/pgrubic/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/bolajiwahab/pgrubic/tree/python-coverage-comment-action-data)
[![CodeQL](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql)
[![Trivy Security Scan](https://github.com/bolajiwahab/pgrubic/actions/workflows/trivy.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/trivy.yml)
[![Scan GitHub Actions](https://github.com/bolajiwahab/pgrubic/actions/workflows/zizmor.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/zizmor.yml)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/pgrubic?artifact_id=tar-gz)](https://socket.dev/pypi/package/pgrubic/overview/)

A PostgreSQL linter and formatter for schema migrations and design best practices.

## Features

- Over 100+ rules
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements)
- Linting of migrations embedded in PL/pgSQL functions and DO blocks
- River style code formatting for DML statements
- Almost identical styling with **pg_dump** for DDL statements
- Python 3.12+ compatibility
- Automatic caching to avoid reformatting unchanged files
- Violations suppression, statement level, and file level
- Can be used as a library in your own Python projects, not just as a CLI tool

## Requirements

pgrubic is built upon the shoulders of:

- [pglast](https://github.com/lelit/pglast) - Python bindings to libpg_query
- [libpg_query](https://github.com/pganalyze/libpg_query) - PostgreSQL parser outside of the server environment
