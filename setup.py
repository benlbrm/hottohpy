import setuptools
import os
import codecs
import re

# Method for retrieving the version is taken from the setup.py of pip itself:
# https://github.com/pypa/pip/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hottohpy",
    version=find_version("src/hottohpy", "__init__.py"),
    author="benlbrm",
    author_email="web@lebruman.fr",
    description="Python lib to control Hottoh based stove Devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benlbrm/hottohpy",
    project_urls={
        "Bug Tracker": "https://github.com/benlbrm/hottohpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Home Automation',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
