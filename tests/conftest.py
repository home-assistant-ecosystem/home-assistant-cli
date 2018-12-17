"""conftest.py loads all fixtures found in fixtures/.

Each file are made available as follows:

Given a file named: `mydata.json`
it will be available as:

mydata_text - str with the raw text
mydata      - Dict with the content parsed from json
"""

import json
import os

import pkg_resources
import pytest

FIXTURES_PATH = pkg_resources.resource_filename(__name__, 'fixtures/')


def generate_fixture(content):
    """Generate the individual fixtures."""
    pass  # pylint: disable=unnecessary-pass

    @pytest.fixture(scope='module')
    def my_fixture():
        return content

    return my_fixture


def _inject_fixture(name, someparam):
    globals()[name] = generate_fixture(someparam)


def _all_fixtures():
    for fname in os.listdir(FIXTURES_PATH):
        name, _ = os.path.splitext(fname)

        with open(FIXTURES_PATH + fname) as file:
            content = file.read()

        _inject_fixture(name + "_text", content)
        _inject_fixture(name, json.loads(content))


_all_fixtures()
