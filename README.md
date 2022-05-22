# pyrootutils

[![Tests](https://github.com/ashleve/pyrootutils/actions/workflows/tests.yaml/badge.svg)](https://github.com/ashleve/pyrootutils/actions/workflows/tests.yaml)

A simple python package to solve all your problems with pythonpath, working directory, file paths, module imports and environment variables.

## Why pyrootutils?

**Problem:** I would like to be able to:

- Run my python scripts from anywhere
- Always import python modules relatively to the project root directory
- Always access files relatively to the project root so I don't have to specify a series of `../` to get to the data
- Always have access to environment variables from `.env` file without having to load them manually
- Have all the above benefits in notebooks even if they're nested in subdirectories

**Solution:** The `pyrootutils` package provides a flexible way to setup the python project with a simple one-liner. It finds the project root based on the location of specified file name, e.g. `.project-root` or `.git`.

The package is tiny and continuosly maintained, so you can use it without worrying it gets deprecated in the future.

## Setup

```python
pip install pyrootutils
```

## Usage

```python
import pyrootutils


# find absolute root path (searches for directory containing .project-root file)
# search starts from current file and recursively goes over parent directories
# returns pathlib object
path = pyrootutils.get_root(search_from=__file__, indicator=".project-root")

# find absolute root path (searches for directory containing any of the files on the list)
path = pyrootutils.get_root(search_from=__file__, indicator=[".git", "setup.cfg"])

# take advantage of the pathlib syntax
data_dir = path / "data"
assert data_dir.exists(), f"path doesn't exist: {data_dir}"

# set root directory
pyrootutils.set_root(
    path=path # path to the root directory
    pythonpath=True, # add root directory to the PYTHONPATH (helps with imports)
    cwd=True, # set current working directory to the root directory (helps with filepaths)
    project_root_env_var=True, # set the PROJECT_ROOT environment variable to root directory
    dotenv=True, # load environment variables from .env if exists in root directory
)
```

```python
import pyrootutils


# combines get_root() and set_root() into one method
root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=".git" # indicator of the root directory
    pythonpath=True,
    cwd=True,
    project_root_env_var=True,
    dotenv=True,
)
```

## Inspirations

This package is heavily inspired by:

https://github.com/chendaniely/pyprojroot

https://github.com/pashminacameron/py-repo-root

https://github.com/EduardKononov/from-root

https://github.com/eddieantonio/project-paths
