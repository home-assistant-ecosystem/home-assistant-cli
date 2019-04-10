"""Tests file for Home Assistant CLI (hass-cli)."""
import json

from click.testing import CliRunner
import requests_mock

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration


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
            cli.cli,
            ["--output=json", "raw", "get", "/api/anything"],
            catch_exceptions=False,
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
            cli.cli,
            ["--output=json", "raw", "post", "/api/anything"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data['message'] == 'success'


def test_apimethod_completion(default_services) -> None:
    """Test completion for raw API methods."""
    cfg = Configuration()

    result = autocompletion.api_methods(cfg, ["raw", "get"], "/api/disc")
    assert len(result) == 1

    resultdict = dict(result)

    assert "/api/discovery_info" in resultdict
