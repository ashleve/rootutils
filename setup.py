from setuptools import find_packages, setup

from pyrootutils import __version__

with open("README.md") as f:
    long_description = f.read()


setup(
    name="pyrootutils",
    version=__version__,
    license="MIT",
    description="Simple package for easy project root setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ashleve/pyrootutils",
    author="ashleve",
    author_email="ashlevegalaxy@gmail.com",
    packages=find_packages(),
    python_requires=">=3.7.0",
    include_package_data=True,
    install_requires=["python-dotenv"],
    tests_require=["pytest"],
)
