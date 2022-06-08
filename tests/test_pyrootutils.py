import os
import sys
from pathlib import Path

import pytest

from pyrootutils import find_root, set_root, setup_root


def test_pyrootutils():
    assert find_root
    assert set_root
    assert setup_root


def test_find_root():
    path = find_root()
    assert path.exists()

    path = find_root("")
    assert path.exists()

    path = find_root(".")
    assert path.exists()

    path = find_root(__file__)
    assert path.exists()

    path = find_root(str(__file__))
    assert path.exists()

    path = find_root(Path(__file__))
    assert path.exists()

    path = find_root(__file__, ".git")
    assert path.exists()

    path = find_root(__file__, indicator=[".setup.cfg", "setup.py", "LICENSE"])
    assert path.exists()

    with pytest.raises(FileNotFoundError):
        path = find_root(__file__, indicator="abc")

    with pytest.raises(FileNotFoundError):
        path = find_root(__file__, indicator=["abc", "def", "fgh"])

    with pytest.raises(FileNotFoundError):
        path = find_root(Path(__file__).parent.parent.parent)

    with pytest.raises(TypeError):
        path = find_root([])

    with pytest.raises(TypeError):
        path = find_root("", ["abs", "def", 42])


def test_set_root():

    path = find_root(__file__)
    assert path.exists()

    os.chdir(path.parent)
    assert os.getcwd() != str(path)

    assert "PROJECT_ROOT" not in os.environ

    set_root(path, project_root_env_var=True, dotenv=False, pythonpath=False, cwd=False)
    assert "PROJECT_ROOT" in os.environ
    assert os.environ["PROJECT_ROOT"] == str(path)
    assert os.getcwd() != str(path)

    set_root(path, project_root_env_var=True, dotenv=True, pythonpath=True, cwd=True)
    assert os.getcwd() == str(path)
    assert str(path) in sys.path


def test_setup_root():
    path = setup_root(__file__)
    assert path.exists()
