"""Tests for the integration plugin."""

import json
from unittest import mock

import requests_mock
from click.testing import CliRunner

import homeassistant_cli.cli as cli

# Sample config entries data
SAMPLE_CONFIG_ENTRIES = [
    {
        "entry_id": "01JS6FQ9VD5A1CR30KE4F4MWXG",
        "domain": "hue",
        "title": "Philips Hue",
        "state": "loaded",
        "disabled_by": None,
    },
    {
        "entry_id": "02AB7GR0WE6B2DS41LF5G5NXYH",
        "domain": "mqtt",
        "title": "MQTT Broker",
        "state": "loaded",
        "disabled_by": None,
    },
    {
        "entry_id": "03CD8HS1XF7C3ET52MG6H6OYZI",
        "domain": "zwave_js",
        "title": "Z-Wave JS",
        "state": "not_loaded",
        "disabled_by": "user",
    },
]


def test_integration_list() -> None:
    """Test listing all integrations."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 3


def test_integration_list_with_filter() -> None:
    """Test listing integrations with a filter."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list", "hue"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]["domain"] == "hue"


def test_integration_list_filter_by_title() -> None:
    """Test listing integrations filtered by title."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list", "Philips"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]["title"] == "Philips Hue"


def test_integration_info() -> None:
    """Test getting info for a specific integration."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "info", "01JS6FQ9VD5A1CR30KE4F4MWXG"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["domain"] == "hue"
        assert data["title"] == "Philips Hue"


def test_integration_info_partial_match() -> None:
    """Test getting info with partial entry_id match."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "info", "01JS6"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["entry_id"] == "01JS6FQ9VD5A1CR30KE4F4MWXG"


def test_integration_reload_success() -> None:
    """Test reloading an integration successfully."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )
        mock_req.post(
            "http://localhost:8123/api/config/config_entries/entry/01JS6FQ9VD5A1CR30KE4F4MWXG/reload",
            json={"require_restart": False},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["integration", "reload", "01JS6FQ9VD5A1CR30KE4F4MWXG"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Successfully reloaded" in result.output


def test_integration_reload_partial_id() -> None:
    """Test reloading an integration with partial entry_id."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )
        mock_req.post(
            "http://localhost:8123/api/config/config_entries/entry/01JS6FQ9VD5A1CR30KE4F4MWXG/reload",
            json={"require_restart": False},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["integration", "reload", "01JS6"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Successfully reloaded" in result.output


def test_integration_delete_with_confirm() -> None:
    """Test deleting an integration with --confirm flag."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )
        mock_req.delete(
            "http://localhost:8123/api/config/config_entries/entry/01JS6FQ9VD5A1CR30KE4F4MWXG",
            json={"require_restart": False},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["integration", "delete", "01JS6FQ9VD5A1CR30KE4F4MWXG", "--confirm"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Successfully deleted" in result.output


def test_integration_disable() -> None:
    """Test disabling an integration."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        with mock.patch(
            "homeassistant_cli.remote.wsapi",
            return_value={"success": True, "result": {"require_restart": False}},
        ):
            runner = CliRunner()
            result = runner.invoke(
                cli.cli,
                ["integration", "disable", "01JS6FQ9VD5A1CR30KE4F4MWXG"],
                catch_exceptions=False,
            )
            assert result.exit_code == 0
            assert "Successfully disabled" in result.output


def test_integration_enable() -> None:
    """Test enabling a disabled integration."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        with mock.patch(
            "homeassistant_cli.remote.wsapi",
            return_value={"success": True, "result": {"require_restart": False}},
        ):
            runner = CliRunner()
            result = runner.invoke(
                cli.cli,
                ["integration", "enable", "03CD8HS1XF7C3ET52MG6H6OYZI"],
                catch_exceptions=False,
            )
            assert result.exit_code == 0
            assert "Successfully enabled" in result.output


def test_integration_list_disabled() -> None:
    """Test listing only disabled integrations."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list-disabled"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]["domain"] == "zwave_js"
        assert data[0]["disabled_by"] == "user"


def test_integration_list_loaded() -> None:
    """Test listing only loaded integrations."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list-loaded"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 2
        assert all(entry["state"] == "loaded" for entry in data)


def test_integration_list_unloaded() -> None:
    """Test listing only unloaded integrations."""
    with requests_mock.Mocker() as mock_req:
        mock_req.get(
            "http://localhost:8123/api/config/config_entries/entry",
            json=SAMPLE_CONFIG_ENTRIES,
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["--output=json", "integration", "list-unloaded"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]["state"] == "not_loaded"
