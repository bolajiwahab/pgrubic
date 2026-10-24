ARG PYTHON_IMAGE=python:3.14-slim@sha256:ce40764625a4ff50df3548277632e7f96c4e77fe75fa848aae9885476e7df5a4

FROM ${PYTHON_IMAGE} AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.5@sha256:32a7bb39b496babbd997b0a39a4d66c126bdaf5661b302bf6f06abda8deca6ff /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md LICENSE ./

# Cache runtime dependencies separately from application source changes.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-editable --compile-bytecode

FROM ${PYTHON_IMAGE} AS runtime

# GitPython uses the Git executable to respect .gitignore in mounted projects.
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && git config --system --add safe.directory /sql \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

# Verify the installed CLI and cache its startup imports before dropping privileges.
RUN pgrubic --help > /dev/null

# Switch to /sql working directory as default bind mount location.
# User can bind mount to /sql and not have to specify the full file path in the command:
# e.g. docker run --rm -it -v $PWD:/sql pgrubic:latest lint test.sql

WORKDIR /sql

ENV PYTHONUNBUFFERED=1

# Use an explicit non-root user and group; no login account is needed.
USER 10001:10001

ENTRYPOINT ["pgrubic"]

CMD ["--help"]
