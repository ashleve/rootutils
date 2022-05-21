from pathlib import Path
from typing import Iterable, Union


class ProjectRootNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def _pyrootutils_recursive_search(path: str, indicator: Union[str, Iterable[str]]) -> Path:
    pass


def get_root():
    pass


def set_root():
    pass


def setup_root():
    pass


def get_from_root():
    pass
