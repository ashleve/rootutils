from pathlib import Path

from pyrootutils import get_root, set_root, setup_root


def test_pyrootutils():
    assert get_root
    assert set_root
    assert setup_root

    path = get_root(__file__)
    assert path.exists()

    path = get_root(Path(__file__))
    assert path.exists()


def test_set_root():
    path = get_root(__file__)
    assert path.exists()

    set_root(path, pythonpath=False, cwd=False, project_root_env_var=True, dotenv=False)

    path = str(path)
    set_root(path, pythonpath=False, cwd=False, project_root_env_var=True, dotenv=False)


def test_setup_root():
    path = setup_root(__file__)
    assert path.exists()
