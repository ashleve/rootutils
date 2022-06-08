from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="pyrootutils",
    version="1.0.3",
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
    install_requires=["python-dotenv>=0.20.0"],
    tests_require=["pytest"],
)
