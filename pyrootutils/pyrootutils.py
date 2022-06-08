import os
import sys
from pathlib import Path
from typing import Iterable, Optional, Union

from dotenv import load_dotenv


def _pyrootutils_recursive_search(path: Path, indicators: Iterable[str]) -> Optional[Path]:
    """Recursively search for files from the `indicators` list, starting from given path.

    Args:
        path (Path): starting folder path.
        indicators (Iterable[str]): list of filenames to search for.

    Raises:
        FileNotFoundError: if root is not found.

    Returns:
        Optional[Path]: path to folder containing at list one of the files from the list.
    """
    for file in indicators:
        found = list(path.glob(file))
        if len(found) > 0:
            return path

    if path.parent == path:
        return None

    return _pyrootutils_recursive_search(path.parent, indicators)


def find_root(
    search_from: Union[str, Path] = ".",
    indicator: Union[str, Iterable[str]] = (
        ".project-root",
        "setup.cfg",
        "setup.py",
        ".git",
        "pyproject.toml",
    ),
) -> Path:
    """Recursively searches for project root indicator(s), starting from given path.

    Args:
        search_from (str): path to folder to start search from.
        indicator (Union[str, Iterable[str]], optional): _description_. Defaults to ".project-root".

    Raises:
        TypeError: if any input type is incorrect.
        FileNotFoundError: if root is not found.

    Returns:
        Path: path to project root.
    """
    if not isinstance(search_from, (str, Path)):
        raise TypeError("search_from must be either a string or pathlib object.")

    search_from = Path(search_from).resolve()

    if isinstance(indicator, str):
        indicator = [indicator]

    if not search_from.exists():
        raise FileNotFoundError("search_from path does not exist.")

    if not hasattr(indicator, "__iter__") or not all(isinstance(i, str) for i in indicator):
        raise TypeError("indicator must be a string or list of strings.")

    path = _pyrootutils_recursive_search(search_from, indicator)

    if not path or not path.exists():
        raise FileNotFoundError(f"Project root directory not found. Indicators: {indicator}")

    return path


def set_root(
    path: Union[str, Path],
    project_root_env_var: bool = True,
    dotenv: bool = True,
    pythonpath: bool = False,
    cwd: bool = False,
) -> None:
    """Set given path as a project root.

    Args:
        path (Union[str, Path]): project root path.
        project_root_env_var (bool, optional): whether to set PROJECT_ROOT environment variable to project root.
        dotenv (bool, optional): whether to load .env file from project root.
        pythonpath (bool, optional): whether to add project root to pythonpath.
        cwd (bool, optional): whether to set current working directory to project root.

    Raises:
        FileNotFoundError: if root path does not exist.

    Returns:
        None
    """
    path = str(path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Project root path does not exist: {path}")

    if project_root_env_var:
        os.environ["PROJECT_ROOT"] = path

    if dotenv:
        load_dotenv(os.path.join(path, ".env"))

    if pythonpath:
        sys.path.insert(0, path)

    if cwd:
        os.chdir(path)


def setup_root(
    search_from: Union[str, Path],
    indicator: Union[str, Iterable[str]] = (
        ".project-root",
        "setup.cfg",
        "setup.py",
        ".git",
        "pyproject.toml",
    ),
    project_root_env_var: bool = True,
    dotenv: bool = True,
    pythonpath: bool = False,
    cwd: bool = False,
) -> Path:
    """Combines `get_root()` and `set_root()` into one method.

    Args:
        search_from (str): path to folder to start search from.
        indicator (Union[str, Iterable[str]], optional): Project root indicator(s). Defaults to ".project-root".
        project_root_env_var (bool, optional): whether to set PROJECT_ROOT environment variable to project root.
        dotenv (bool, optional): whether to load .env file from project root.
        pythonpath (bool, optional): whether to add project root to pythonpath.
        cwd (bool, optional): whether to set current working directory to project root.

    Returns:
        Path: path to project root.
    """
    path = find_root(search_from, indicator)
    set_root(
        path=path,
        project_root_env_var=project_root_env_var,
        dotenv=dotenv,
        pythonpath=pythonpath,
        cwd=cwd,
    )
    return path
