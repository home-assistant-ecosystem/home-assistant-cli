#!/usr/bin/env python3
"""Setup script for Home Assistant CLI."""
from datetime import datetime as dt

import homeassistant_cli.const as hass_cli_const
from setuptools import find_packages, setup

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

DOWNLOAD_URL = '{}/archive/{}.zip'.format(
    GITHUB_URL, hass_cli_const.__version__
)
PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL),
    'Dev Docs': 'https://developers.home-assistant.io/',
    'Discord': 'https://discordapp.com/invite/c5DvZ4e',
    'Forum': 'https://community.home-assistant.io/',
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'requests==2.20.1',
    'pyyaml>=3.13,<4',
    'netdisco==2.2.0',
    'click==7.0',
    'click-log==0.3.2',
    'tabulate==0.8.2',
    'idna==2.5',
    'jsonpath-rw==1.4.0',
    'jinja2>=2.10',
]

# should be as close to homeassistant dev/master as possible
TESTS_REQUIRE = [
    'coveralls==1.2.0',
    'flake8-docstrings==1.3.0',
    'flake8==3.6.0',
    'mock-open==1.3.1',
    'mypy==0.650',
    'pydocstyle==2.1.1',
    'pylint==2.1.1',
    'pytest-cov==2.6.0',
    'pytest-sugar==0.9.2',
    'pytest-timeout==1.3.2',
    'pytest==4.0.0',
    'requests_mock==1.5.2',
    "black==18.9b0;python_version>'3.6'",
    'wheel==0.32.3',  # otherwise setup.py bdist_wheel does not work
]

MIN_PY_VERSION = '.'.join(map(str, hass_cli_const.REQUIRED_PYTHON_VER))

# allow you to run pip3 install .[test] to get
# test dependencies included.
EXTRAS_REQUIRE = {'test': TESTS_REQUIRE}

setup(
    name=PROJECT_PACKAGE_NAME,
    version=hass_cli_const.__version__,
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
