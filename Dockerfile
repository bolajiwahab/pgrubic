ARG PYTHON_IMAGE=python:3.15-slim@sha256:044d5bd747976e21f8bc4d746c3479b19a84bb8ae6261b802acdd26b29036c93

FROM ${PYTHON_IMAGE}

WORKDIR /app

# Install uv.
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.13.5@sha256:32a7bb39b496babbd997b0a39a4d66c126bdaf5661b302bf6f06abda8deca6ff /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY src ./src

ENV UV_PROJECT_ENVIRONMENT=/usr/local
RUN uv sync --locked --no-editable --compile-bytecode

# Switch to /sql working directory as default bind mount location.
# User can bind mount to /sql and not have to specify the full file path in the command:
# e.g. docker run --rm -it -v $PWD:/sql pgrubic:latest lint test.sql

WORKDIR /sql

ENV PYTHONUNBUFFERED=1

# Switch to non-root user.
USER 10001

ENTRYPOINT ["pgrubic"]

CMD ["--help"]
