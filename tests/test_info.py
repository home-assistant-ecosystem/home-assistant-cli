"""Tests file for Home Assistant CLI (hass-cli)."""
import json
import yaml

from click.testing import CliRunner
import homeassistant_cli.cli as cli

import requests_mock

from requests.exceptions import ConnectionError

VALID_INFO = {"base_url": "http://192.168.1.156:8123",
              "location_name": "Home",
              "requires_api_password": "false",
              "version": "0.82.1"}


def ordered(obj):
    """Sort object recursively. Useful for comparing json/yaml dicts."""
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def test_info_without_server_running():
    runner = CliRunner()
    result = runner.invoke(cli.cli, ['--server',
                                     'http://donotexist.inf',
                                     'info'])
    assert result.exit_code == 1
    assert isinstance(result.exception, ConnectionError)


def test_info_json():
    with requests_mock.Mocker() as m:
        m.get('http://localhost:8123/api/discovery_info',
              json=VALID_INFO, status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, ['info'], catch_exceptions=False)
        assert result.exit_code == 0
        assert VALID_INFO == json.loads(result.output)


def test_info_yaml():
    with requests_mock.Mocker() as m:
        m.get('http://localhost:8123/api/discovery_info',
              json=VALID_INFO, status_code=200)

        runner = CliRunner()
        result = runner.invoke(cli.cli, ['info'], catch_exceptions=False)
        assert result.exit_code == 0
        assert VALID_INFO == yaml.load(result.output)