#!/usr/bin/python3
"""Setup script for Home Assistant CLI."""
import codecs
from datetime import datetime as dt
import os
import re
import subprocess

from setuptools import find_packages, setup

# shared consts using approach suggested at
# https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package


def read(*parts):
    """Read file from current directory."""
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as infofile:
        return infofile.read()


def find_version(*file_paths):
    """Locate version info to share between const.py and setup.py."""
    version_file = read(*file_paths)  # type: ignore
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_git_commit_datetime() -> str:
    """Return timestamp from last commit."""
    try:
        commit_timestamp = subprocess.check_output(
            "git show -s --format=%ct", shell=True, stderr=subprocess.STDOUT
        )
        datetime_object = dt.fromtimestamp(int(commit_timestamp))
        return "{:%Y%m%d%H%M%S}".format(datetime_object)
    except subprocess.CalledProcessError as cpe:
        print(cpe.output)
        return "00000000000000"


__VERSION__ = find_version("homeassistant_cli", "const.py")  # type: ignore
# Append a suffix to the version for dev builds
if 'dev' in __VERSION__:
    __VERSION__ = '{v}{s}'.format(v=__VERSION__, s=get_git_commit_datetime())

REQUIRED_PYTHON_VER = (3, 6, 0)


PROJECT_NAME = 'Home Assistant CLI'
PROJECT_PACKAGE_NAME = 'homeassistant-cli'
PROJECT_LICENSE = 'Apache License 2.0'
PROJECT_AUTHOR = 'The Home Assistant CLI Authors'
PROJECT_COPYRIGHT = ' 2018-{}, {}'.format(dt.now().year, PROJECT_AUTHOR)
PROJECT_URL = 'https://github.com/home-assistant/home-assistant-cli/'
PROJECT_EMAIL = 'hello@home-assistant.io'

PROJECT_GITHUB_USERNAME = 'home-assistant'
PROJECT_GITHUB_REPOSITORY = 'home-assistant-cli'

PYPI_URL = 'https://pypi.python.org/pypi/{}'.format(PROJECT_PACKAGE_NAME)
GITHUB_PATH = '{}/{}'.format(
    PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY
)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

DOWNLOAD_URL = '{}/archive/{}.zip'.format(GITHUB_URL, __VERSION__)
PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL),
    'Dev Docs': 'https://developers.home-assistant.io/',
    'Discord': 'https://discordapp.com/invite/c5DvZ4e',
    'Forum': 'https://community.home-assistant.io/',
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'aiohttp>=3.5.4,<4',
    'click-log>=0.3.2,<0.4',
    'click>=7.0,<8',
    'dateparser>=0.7.1,<0.8',
    'jinja2>=2.10',
    'jsonpath-rw>=1.4.0,<2',
    'netdisco>=2.6.0,<3',
    'regex>=2019.08.19',
    'ruamel.yaml>=0.16.5,<0.17',
    'requests>=2.22.0,<3',
    'tabulate>=0.8.3,<0.9',
]

# Should be as close to Home Assistant dev/master as possible
TESTS_REQUIRE = [
    "black>=19.10b0,<20;python_version>'3.6'",
    'codecov>=2.0.15,<3',
    'coveralls>=1.2.0,<2',
    'flake8>=3.7.7,<4',
    'flake8-docstrings>=1.3.0,<2',
    'mock-open>=1.3.1,<1.4',
    'mypy>=0.710,<0.800',
    'pydocstyle>=4.0.0,<5',
    'pylint>=2.3.1,<2.4',
    'pytest>=5.1.2,<6',
    'pytest-cov>=2.6.1,<3',
    'pytest-sugar>=0.9.2,<0.10',
    'pytest-timeout>=1.3.3,<1.4',
    'requests_mock>=1.6.0,<2',
    'twine>=1.13.0,<2',
    'wheel>=0.33.1,<0.40',  # Otherwise setup.py bdist_wheel does not work
]

MIN_PY_VERSION = '.'.join(map(str, REQUIRED_PYTHON_VER))

# Allow you to run pip0 install .[test] to get test dependencies included
EXTRAS_REQUIRE = {'test': TESTS_REQUIRE}

setup(
    name=PROJECT_PACKAGE_NAME,
    version=__VERSION__,
    url=PROJECT_URL,
    download_url=DOWNLOAD_URL,
    project_urls=PROJECT_URLS,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRE,
    extras_require=EXTRAS_REQUIRE,
    python_requires='>={}'.format(MIN_PY_VERSION),
    test_suite='tests',
    entry_points={'console_scripts': ['hass-cli = homeassistant_cli.cli:run']},
)
