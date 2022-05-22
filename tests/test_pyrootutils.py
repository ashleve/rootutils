import os
import sys
from pathlib import Path

import pytest

from pyrootutils import get_root, set_root, setup_root


def test_pyrootutils():
    assert get_root
    assert set_root
    assert setup_root


def test_get_root():
    path = get_root(__file__)
    assert path.exists()

    path = get_root(str(__file__))
    assert path.exists()

    path = get_root(Path(__file__))
    assert path.exists()

    path = get_root(__file__, ".git")
    assert path.exists()

    path = get_root(__file__, indicator=[".setup.cfg", "setup.py", "LICENSE"])
    assert path.exists()

    path = get_root("")
    assert path.exists()

    path = get_root(".")
    assert path.exists()

    with pytest.raises(FileNotFoundError):
        path = get_root(__file__, indicator="abc")

    with pytest.raises(FileNotFoundError):
        path = get_root(__file__, indicator=["abc", "def", "fgh"])

    with pytest.raises(FileNotFoundError):
        path = get_root(Path(__file__).parent.parent.parent)

    with pytest.raises(TypeError):
        path = get_root([])

    with pytest.raises(TypeError):
        path = get_root("", ["abs", "def", 42])


def test_set_root():

    path = get_root(__file__)
    assert path.exists()

    os.chdir(path.parent)
    assert os.getcwd() != str(path)

    with pytest.raises(Exception):
        set_root(path, pythonpath=False, cwd=False, project_root_env_var=False, dotenv=False)

    assert "PROJECT_ROOT" not in os.environ

    set_root(path, pythonpath=False, cwd=False, project_root_env_var=True, dotenv=False)
    assert "PROJECT_ROOT" in os.environ
    assert os.environ["PROJECT_ROOT"] == str(path)
    assert os.getcwd() != str(path)

    set_root(path, pythonpath=True, cwd=True, project_root_env_var=True, dotenv=True)
    assert os.getcwd() == str(path)
    assert str(path) in sys.path


def test_setup_root():
    path = setup_root(__file__)
    assert path.exists()
