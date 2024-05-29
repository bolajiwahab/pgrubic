"""Load config from a file."""
import configparser
import os
import pathlib
import typing

file_path = pathlib.Path(__file__).resolve().parent

file_name: pathlib.Path = pathlib.Path(file_path) / ".pgshield"
def read_config_file(file_name: os.PathLike[str]) -> dict[str, str]:
    """Read config file from a file."""
    kw: dict[str, typing.Any] = {}
    config = configparser.ConfigParser(delimiters="=", **kw)

    config.read(file_name)

    return dict(config.items("pgshield"))
