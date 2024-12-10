"""Caching of formatted files."""

import os
import typing
import hashlib
import pathlib
import tempfile

import msgpack

import pgrubic
from pgrubic import PACKAGE_NAME
from pgrubic.core import config

CACHE_FILE_NAME_LENGTH: typing.Final[int] = 20

CACHE_DIR_ENVIRONMENT_VARIABLE: typing.Final[str] = f"{PACKAGE_NAME.upper()}_CACHE_DIR"

DEFAULT_CACHE_DIR: typing.Final[str] = ".pgrubic_cache"


class FileData(typing.NamedTuple):
    """Representation of file data."""

    size: int
    last_modified_time: float
    hashed_content: str


class Cache:
    """Caching of formatted files."""

    def __init__(
        self,
        *,
        config: config.Config,
    ) -> None:
        """Initialize variables."""
        self.config = config
        if (
            os.getenv(CACHE_DIR_ENVIRONMENT_VARIABLE)
            and str(self.config.cache_dir) == DEFAULT_CACHE_DIR
        ):
            self.config.cache_dir = pathlib.Path(
                os.environ[CACHE_DIR_ENVIRONMENT_VARIABLE],
            )

        self.cache_dir = config.cache_dir.resolve() / pgrubic.__version__
        self.cache_file = (
            self.cache_dir
            / hashlib.sha256(b"formatter.cache").hexdigest()[:CACHE_FILE_NAME_LENGTH]
        )

    def _read(self) -> dict[str, FileData]:
        """Read the cache file if it exists."""
        if not self.cache_file.exists():
            return {}

        with self.cache_file.open("rb") as f:
            cache: dict[str, tuple[int, float, str]] = msgpack.unpack(f)
            return {
                k: FileData(size=v[0], last_modified_time=v[1], hashed_content=v[2])
                for k, v in cache.items()
            }

    def _hash_digest(self, source: pathlib.Path) -> str:
        """Return hash digest of the content of source and config."""
        hasher = hashlib.sha256()
        hasher.update(source.read_bytes())
        hasher.update(msgpack.packb(self.config.format.__repr__()))
        return hasher.hexdigest()

    def _get_file_data(self, source: pathlib.Path) -> FileData:
        """Return file data for source."""
        file_stat = source.stat()
        hashed_content = self._hash_digest(source)
        return FileData(
            size=file_stat.st_size,
            last_modified_time=file_stat.st_mtime,
            hashed_content=hashed_content,
        )

    def _need_to_be_formatted(self, source: pathlib.Path) -> bool:
        """Check if source needs to be formatted."""
        cache = self._read()
        resolved_source = source.resolve()
        cached_version = cache.get(str(resolved_source))
        if not cached_version:
            return True

        source_stat = resolved_source.stat()

        if source_stat.st_size != cached_version.size:
            return True

        if source_stat.st_mtime != cached_version.last_modified_time:
            return True

        new_file_hash = self._hash_digest(resolved_source)
        return new_file_hash != cached_version.hashed_content

    def filter_sources(self, sources: tuple[pathlib.Path, ...]) -> set[pathlib.Path]:
        """Return sources that need to be formatted."""
        sources_to_be_formatted: set[pathlib.Path] = set()
        for source in sources:
            if self._need_to_be_formatted(source):
                sources_to_be_formatted.add(source)

        return sources_to_be_formatted

    def write(self, sources: tuple[pathlib.Path, ...]) -> None:
        """Generate the cache data for sources and write a new cache file."""
        file_data: dict[str, FileData] = {
            str(source.resolve()): self._get_file_data(source) for source in sources
        }

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            dir=str(self.cache_file.parent),
            delete=False,
        ) as tf:
            data: dict[str, tuple[int, float, str]] = {
                k: (v.size, v.last_modified_time, v.hashed_content)
                for k, v in file_data.items()
            }
            msgpack.pack(data, tf)

        pathlib.Path.replace(pathlib.Path(tf.name), self.cache_file)
