"""Load config from a file."""
import os
import typing
import pathlib
import configparser

file_path = pathlib.Path(__file__).resolve().parent

file_name: pathlib.Path = pathlib.Path(file_path) / ".pgshield"

def load_config(file_name: os.PathLike[str]) -> dict[str, str]:
    """Read config file from a file."""
    config = configparser.ConfigParser(delimiters="=")

    try:
        config.read(file_name, encoding="utf-8")
    except configparser.DuplicateOptionError:
        config.read(file_name, encoding="utf-8")

    return dict(config.items("pgshield"))
