ARG PYTHON_IMAGE=python:3.15-alpine@sha256:a0f2e268f2ce8f3709611a90054ec6a8ae31f6251f5896b8648b9bb99835e30a

FROM ${PYTHON_IMAGE} AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /usr/local/bin/uv

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
