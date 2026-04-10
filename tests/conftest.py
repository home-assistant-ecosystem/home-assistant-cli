"""conftest.py loads all fixtures found in fixtures/.

Each file are made available as follows:

Given a file named: `mydata.json`
it will be available as:

mydata_text - str with the raw text
mydata      - Dict with the content parsed from json
"""

import json
import os
from pathlib import Path

import click_log.core as logcore
import pytest

FIXTURES_PATH = Path(__file__).parent / "fixtures"


logcore.basic_config()


# Environment variables that should be cleared during tests
HASS_ENV_VARS = [
    "HASS_SERVER",
    "HASS_TOKEN",
    "HASS_PASSWORD",
    "HASSIO_TOKEN",
]


@pytest.fixture(autouse=True)
def clean_hass_env(monkeypatch):
    """Clear Home Assistant environment variables for test isolation."""
    for var in HASS_ENV_VARS:
        monkeypatch.delenv(var, raising=False)


def generate_fixture(content: str):
    """Generate the individual fixtures."""
    pass  # pylint: disable=unnecessary-pass

    @pytest.fixture(scope="module")
    def my_fixture():
        return content

    return my_fixture


def _inject_fixture(name: str, someparam: str):
    globals()[name] = generate_fixture(someparam)


def _all_fixtures():
    for fname in os.listdir(FIXTURES_PATH):
        name, ext = os.path.splitext(fname)

        with open(FIXTURES_PATH / fname) as file:
            content = file.read()

        _inject_fixture(name + "_text", content)
        if ext == ".json":
            _inject_fixture(name, json.loads(content))


_all_fixtures()  # type: ignore
