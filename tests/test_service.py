"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import requests_mock

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration


def test_service_list(default_services) -> None:
    """Test services can be listed."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/services",
            json=default_services,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "service", "list"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 12


def test_service_filter(default_services) -> None:
    """Test services can be listed."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/services",
            json=default_services,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "service", "list", "homeassistant\\..*config.*"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 2


def test_service_completion(default_services) -> None:
    """Test completion for services with filter."""
    with requests_mock.Mocker() as mock:
        mock.get(
            'http://localhost:8123/api/services',
            json=default_services,
            status_code=200,
        )

        cfg = Configuration()

        result = autocompletion.services(
            cfg, ["service", "call"], "light.turn"
        )
        assert len(result) == 2

        resultdict = dict(result)

        assert "light.turn_on" in resultdict
        assert "light.turn_off" in resultdict


def test_service_call(default_services) -> None:
    """Test basic call of a service."""
    with requests_mock.Mocker() as mock:

        post = mock.post(
            "http://localhost:8123/api/services/homeassistant/restart",
            json={"result": "bogus"},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "service", "call", "homeassistant.restart"],
            catch_exceptions=False,
        )

        assert result.exit_code == 0

        assert post.call_count == 1
