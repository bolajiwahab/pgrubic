# Stage 1: Build
FROM python:3.12-slim AS build

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip tox

COPY src ./src

COPY pyproject.toml ./

RUN tox -e build-dist

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

COPY --from=build /app/dist/pgrubic-*.whl ./

RUN pip install --no-cache-dir --upgrade pip pgrubic-*.whl

# Switch to /sql working directory as default bind mount location.
# User can bind mount to /sql and not have to specify the full file path in the command:
# e.g. docker run --rm -it -v $PWD:/sql pgrubic-test:latest lint test.sql

WORKDIR /sql

# Switch to non-root user.
USER 5000

ENTRYPOINT ["pgrubic"]

CMD ["--help"]
