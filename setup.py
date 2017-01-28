#!/usr/bin/env python3
"""Setup script for Home Assistant CLI."""
from setuptools import setup, find_packages

from homeassistant_cli.const import __version__, PACKAGE_NAME

PACKAGES = find_packages(exclude=['tests', 'tests.*'])
DOWNLOAD_URL = ('https://github.com/home-assistant/home-assistant-cli/archive/'
                '{}.zip'.format(__version__))
REQUIRES = [
    'click',
    'homeassistant',
    'netdisco',
    'tabulate',
]

setup(
    name=PACKAGE_NAME,
    version=__version__,
    license='Apache License 2.0',
    url='https://github.com/home-assistant/home-assistant-cli',
    download_url=DOWNLOAD_URL,
    author='Fabian Affolter',
    author_email='fabian@affolter-engineering.ch',
    description='Command-line tool for Home Assistant.',
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=REQUIRES,
    test_suite='tests',
    keywords=['home', 'automation'],
    entry_points={
        'console_scripts': [
            'hass-cli = homeassistant_cli.cli:cli'
        ]
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation'
    ],
)
