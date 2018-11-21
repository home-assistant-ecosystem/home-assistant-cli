#!/usr/bin/env python3
"""Setup script for Home Assistant CLI."""
from datetime import datetime as dt
from setuptools import setup, find_packages

import homeassistant_cli.const as hass_cli_const


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
    PROJECT_GITHUB_USERNAME, PROJECT_GITHUB_REPOSITORY)
GITHUB_URL = 'https://github.com/{}'.format(GITHUB_PATH)

DOWNLOAD_URL = '{}/archive/{}.zip'.format(GITHUB_URL, hass_cli_const.__version__)
PROJECT_URLS = {
    'Bug Reports': '{}/issues'.format(GITHUB_URL),
    'Dev Docs': 'https://developers.home-assistant.io/',
    'Discord': 'https://discordapp.com/invite/c5DvZ4e',
    'Forum': 'https://community.home-assistant.io/',
}

PACKAGES = find_packages(exclude=['tests', 'tests.*'])

REQUIRES = [
    'click',
    'homeassistant',
    'netdisco',
    'tabulate',
    'jsonpath-rw'
]

MIN_PY_VERSION = '.'.join(map(str, hass_cli_const.REQUIRED_PYTHON_VER))

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
    python_requires='>={}'.format(MIN_PY_VERSION),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'hass-cli = homeassistant_cli.cli:cli'
        ]
    },
)
