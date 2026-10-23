ARG PYTHON_IMAGE=python:3.14-slim@sha256:ce40764625a4ff50df3548277632e7f96c4e77fe75fa848aae9885476e7df5a4

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
