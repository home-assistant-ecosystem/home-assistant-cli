"""Tests file for Home Assistant CLI (hass-cli)."""
import json
from typing import Any

from click.testing import CliRunner
import requests_mock

import homeassistant_cli.cli as cli
from homeassistant_cli.exceptions import HomeAssistantCliError
import homeassistant_cli.yaml as yaml

VALID_INFO = {
    "base_url": "http://192.168.1.156:8123",
    "location_name": "Home",
    "requires_api_password": "false",
    "version": "0.82.1",
}


def ordered(obj: Any):
    """Sort object recursively. Useful for comparing JSON/YAML dicts."""
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)

    return obj


def test_info_without_server_running() -> None:
    """Test proper failure when server not running."""
    runner = CliRunner()
    result = runner.invoke(
        cli.cli, ['--server', 'http://donotexist.inf', 'info']
    )
    assert result.exit_code == 1
    assert isinstance(result.exception, HomeAssistantCliError)
    assert str(result.exception) == "Unexpected error retrieving information"


def test_info_json() -> None:
    """Test info reads properly with JSON."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/discovery_info',
            json=VALID_INFO,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ['--output=json', 'info'], catch_exceptions=False
        )
        assert result.exit_code == 0
        assert [VALID_INFO] == json.loads(result.output)


def test_info_unauth() -> None:
    """Test info reads properly with JSON."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/discovery_info',
            json={},
            status_code=401,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ['--output=json', 'info'], catch_exceptions=True
        )
        assert result.exit_code != 0


def test_info_yaml() -> None:
    """Test info reads properly with YAML."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/discovery_info',
            json=VALID_INFO,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ['--output=yaml', 'info'], catch_exceptions=False
        )
        assert result.exit_code == 0
        assert [VALID_INFO] == yaml.loadyaml(yaml.yaml(), result.output)
