"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration
import requests_mock


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
            cli.cli, ["service", "list"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 25


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
            ["service", "list", "homeassistant\\.turn.*"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert len(data['homeassistant']['services']) == 2


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
            cfg, "service call", "homeassistant.turn"
        )
        assert len(result) == 2

        resultdict = dict(result)

        assert "homeassistant.turn_on" in resultdict


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
            ["service", "call", "homeassistant.restart"],
            catch_exceptions=False,
        )

        assert result.exit_code == 0

        assert post.call_count == 1
