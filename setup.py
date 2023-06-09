# stdlib
import codecs
import os
import re

# pypi
from setuptools import find_packages
from setuptools import setup

# ==============================================================================


HERE = os.path.abspath(os.path.dirname(__file__))
long_description = description = "some extensions for bleach"
with open(os.path.join(HERE, "README.md")) as fp:
    long_description = fp.read()

install_requires = ["bleach>=3.2.1,<5"]
tests_require = ["pytest>=3.0.0"]
testing_extras = (
    install_requires
    + tests_require
    + [
        "pytest-wholenodeid",
        "flake8",
        "mypy",
        "tox",
        "types-bleach<5",
    ]
)


def get_version():
    fn = os.path.join("src", "bleach_extras", "__init__.py")
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = codecs.open(fn, mode="r", encoding="utf-8").read()
    return re.search(vsre, version_file, re.M).group(1)


setup(
    name="bleach_extras",
    version=get_version(),
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="http://github.com/jvanasco/bleach_extras",
    license="MIT License",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    keywords="bleach html-sanitizing",
    test_suite="tests",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    package_data={"bleach_extras": ["py.typed"]},
    include_package_data=True,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
    ],
)
