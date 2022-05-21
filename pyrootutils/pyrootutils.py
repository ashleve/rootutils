from pathlib import Path
from typing import Iterable, Union


class ProjectRootNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def _pyrootutils_recursive_search(path: str, indicator: Union[str, Iterable[str]]) -> Path:
    pass


def get_root(search_from: str, indicator: Union[str, Iterable[str]] = ".project-root") -> Path:
    pass


def set_root(
    path: str,
    pythonpath: bool = True,
    cwd: bool = True,
    project_root_env_var: bool = True,
    dotenv: bool = True,
):
    pass


def setup_root(
    search_from: str,
    indicator: Union[str, Iterable[str]] = ".project-root",
    pythonpath: bool = True,
    cwd: bool = True,
    project_root_env_var: bool = True,
    dotenv: bool = True,
):
    """Combines `get_root()` and `set_root()` into one method."""
    path = get_root(search_from, indicator)
    set_root(path, pythonpath, cwd, project_root_env_var, dotenv)
    return path


def get_from_root(
    search_from: str,
    indicator: Union[str, Iterable[str]] = ".project-root",
    filepath: str = "",
) -> Path:
    pass
