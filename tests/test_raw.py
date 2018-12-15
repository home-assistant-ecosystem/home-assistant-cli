"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import homeassistant_cli.cli as cli
import requests_mock


def test_raw_get() -> None:
    """Test raw."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/anything",
            json={"message": "success"},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["raw", "get", "/api/anything"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['message'] == 'success'


def test_raw_post() -> None:
    """Test raw."""
    with requests_mock.Mocker() as mock:
        mock.post(
            "http://localhost:8123/api/anything",
            json={"message": "success"},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli, ["raw", "post", "/api/anything"], catch_exceptions=False
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['message'] == 'success'
