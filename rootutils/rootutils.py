import os
import sys
from pathlib import Path
from typing import Iterable, Optional, Union

from dotenv import load_dotenv


def _rootutils_recursive_search(path: Path, indicators: Iterable[str]) -> Optional[Path]:
    """Recursively search for files from the `indicators` list, starting from given path.

    Args:
        path (Path): Starting folder path.
        indicators (Iterable[str]): List of filenames to search for.

    Returns:
        Optional[Path]: Path to folder containing at list one of the files from the list.
    """
    for file in indicators:
        found = list(path.glob(file))
        if len(found) > 0:
            return path

    if path.parent == path:
        return None

    return _rootutils_recursive_search(path.parent, indicators)


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
        search_from (str): Path to folder or file to start search from.
        indicator (Union[str, Iterable[str]], optional): List of filenames to search for. Finding at least one on these files indicates the project root.

    Raises:
        TypeError: If any input type is incorrect.
        FileNotFoundError: If root is not found.

    Returns:
        Path: Path to project root.
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

    path = _rootutils_recursive_search(search_from, indicator)

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
        path (Union[str, Path]): Project root path.
        project_root_env_var (bool, optional): Whether to set PROJECT_ROOT environment variable.
        dotenv (bool, optional): Whether to load `.env` file from project root.
        pythonpath (bool, optional): Whether to add project root to pythonpath.
        cwd (bool, optional): Whether to set current working directory to project root.

    Raises:
        FileNotFoundError: If root path does not exist.

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

    Recursively searches for files from the `indicators` list, starting from given path.

    Args:
        search_from (str): Path to file or folder to start search from.
        indicator (Union[str, Iterable[str]], optional): List of filenames to search for. Finding at least one on these files indicates the project root.
        project_root_env_var (bool, optional): Whether to set PROJECT_ROOT environment variable.
        dotenv (bool, optional): Whether to load `.env` file from project root.
        pythonpath (bool, optional): Whether to add project root to pythonpath.
        cwd (bool, optional): Whether to set current working directory to project root.

    Raises:
        TypeError: If any input type is incorrect.
        FileNotFoundError: If root is not found.

    Returns:
        Path: Path to project root.
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


def autosetup(
    indicator=".project-root",
    project_root_env_var=True,
    dotenv=True,
    pythonpath=True,
    cwd=False,
) -> Path:
    """Experimental method for less friction. Automatically inferrs `search_from` path."""

    # this line finds the absolute path of the original python script that is being run
    startfile = os.path.abspath(sys.argv[0])

    # if we are in notebook or pytest, just use current working directory
    if startfile.endswith("ipykernel_launcher.py") or startfile.endswith("pytest"):
        startfile = os.getcwd()

    # convert to Path object
    startfile = Path(startfile)

    # this line recursively searches for ".project-root" file
    # starting from folder containing the entry python script and going up until it finds it
    path = setup_root(
        search_from=startfile,
        indicator=indicator,
        project_root_env_var=project_root_env_var,
        dotenv=dotenv,
        pythonpath=pythonpath,
        cwd=cwd,
    )

    return path
