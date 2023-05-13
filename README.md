# rootutils

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Tests](https://github.com/ashleve/rootutils/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/ashleve/rootutils/actions/workflows/test.yml)
[![Codecov](https://codecov.io/gh/ashleve/rootutils/branch/main/graph/badge.svg)](https://codecov.io/gh/ashleve/rootutils)
[![Build](https://github.com/ashleve/rootutils/actions/workflows/publish_package.yml/badge.svg)](https://github.com/ashleve/rootutils/actions/workflows/publish_package.yml)
[![Issues](https://img.shields.io/github/issues/ashleve/rootutils)](https://github.com/ashleve/rootutils/issues)
[![License](https://img.shields.io/github/license/ashleve/rootutils)](https://github.com/ashleve/rootutils/blob/main/LICENSE)
[![Release](https://img.shields.io/pypi/v/rootutils)](pypi.org/project/rootutils/1.0.5/)
[![PyPi](https://img.shields.io/pypi/dm/rootutils)](pypi.org/project/rootutils/1.0.5/)

A simple python package to solve all your problems with pythonpath, working directory, file paths, module imports and environment variables.

## Why rootutils?

**Problem:** I would like to be able to:

- Run my python scripts from anywhere
- Always import python modules relatively to the project root directory
- Always access files relatively to the project root so I don't have to specify a series of `../` to get to the data
- Always have access to environment variables from `.env` file without having to load them manually
- Have all the above benefits in notebooks even if they're nested in subdirectories

**Solution:** The `rootutils` package provides a flexible way to setup the python project with a simple one-liner. It finds the project root based on the location of specified file name, e.g. `.project-root` or `.git`.

The package is tiny and continuosly maintained.

## Setup

```bash
pip install rootutils
```

## Usage

```python
import rootutils

# find absolute root path (searches for directory containing .project-root file)
# search starts from current file and recursively goes over parent directories
# returns pathlib object
path = rootutils.find_root(search_from=__file__, indicator=".project-root")

# find absolute root path (searches for directory containing any of the files on the list)
path = rootutils.find_root(search_from=__file__, indicator=[".git", "setup.cfg"])

# take advantage of the pathlib syntax
data_dir = path / "data"
assert data_dir.exists(), f"path doesn't exist: {data_dir}"

# set root directory
rootutils.set_root(
    path=path # path to the root directory
    project_root_env_var=True, # set the PROJECT_ROOT environment variable to root directory
    dotenv=True, # load environment variables from .env if exists in root directory
    pythonpath=True, # add root directory to the PYTHONPATH (helps with imports)
    cwd=True, # change current working directory to the root directory (helps with filepaths)
)
```

Simplest usage with one-liner (combines `find_root()` and `set_root()` into one method):
```python
import rootutils
root = rootutils.setup_root(__file__, dotenv=True, pythonpath=True, cwd=False)
```

## Defaults

Default root indicators (used when you don't specify `indicator` arg):

```python
[".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"]
```

## Autoroot

`autoroot` is an experimental package that reduces `rootutils` to single import, without the need to execute any setup calls. This means just the act of importing this dependency (`import autorootcwd`) causes execution of recurrent search for `.project-root` file.

Installation:
```bash
pip install autoroot autorootcwd
```

This adds root folder to pythonpath, sets PROJECT_ROOT env var, and loads variables from `.env`:
```python
import autoroot # root setup, do not delete
```

This also changes working directory to root:
```python
import autorootcwd # root setup, do not delete
```

Autoroot exist for convenience and speed. For example, it's faster to just add `import autorootcwd` at the beginning when creating new notebook.

Package page: https://github.com/ashleve/autoroot

## Inspirations

This package is heavily inspired by:

https://github.com/chendaniely/pyprojroot

https://github.com/pashminacameron/py-repo-root

https://github.com/EduardKononov/from-root
