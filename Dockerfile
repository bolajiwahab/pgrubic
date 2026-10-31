ARG PYTHON_IMAGE=python:3.15-alpine@sha256:20a82dbc2783112ddb91d1534603f802d222a3e63e593cd002eb2ac534e70211

FROM ${PYTHON_IMAGE} AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.6@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock README.md LICENSE ./

# Cache runtime dependencies separately from application source changes.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-install-project

COPY src ./src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-default-groups --no-editable --compile-bytecode

FROM ${PYTHON_IMAGE} AS runtime

RUN apk del curl && python -m pip uninstall --yes pip \
    # GitPython uses the Git executable to respect .gitignore in mounted projects.
    && apk add --no-cache 'git~2.54' \
    && git config --system --add safe.directory /sql

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
