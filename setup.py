from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="pyrootutils",
    version="0.0.0",
    license="MIT",
    description="A simple python package to solve all of your problems with pythonpath, working directory, file paths and module imports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ashleve",
    author_email="ashlevegalaxy@gmail.com",
    url="https://github.com/ashleve/pyrootutils",
    packages=find_packages(),
    python_requires=">=3.7.0",
    install_requires=["python-dotenv"],
    tests_require=["pytest"],
)
