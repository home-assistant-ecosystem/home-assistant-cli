"""Tests for Home Assistant Operating System plugin (ha.py)."""

import json

import requests_mock
from click.testing import CliRunner

import homeassistant_cli.cli as cli


def test_os_update_already_latest() -> None:
    """Test os update when already on latest version."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/",
            json={"message": "API running."},
            status_code=200,
        )
        mock.get(
            "http://localhost:8123/api/hassio/os/info",
            json={
                "result": "ok",
                "data": {"version": "12.0", "version_latest": "12.0"},
            },
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["ha", "os", "update"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Already running the latest release" in result.output


def test_os_update_needs_update() -> None:
    """Test os update when newer version available."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/",
            json={"message": "API running."},
            status_code=200,
        )
        mock.get(
            "http://localhost:8123/api/hassio/os/info",
            json={
                "result": "ok",
                "data": {"version": "11.0", "version_latest": "12.0"},
            },
            status_code=200,
        )
        mock.post(
            "http://localhost:8123/api/hassio/os/update",
            json={"result": "ok", "data": {}},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["ha", "os", "update"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Already running the latest release" not in result.output


def test_core_update_already_latest() -> None:
    """Test core update when already on latest version."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/",
            json={"message": "API running."},
            status_code=200,
        )
        mock.get(
            "http://localhost:8123/api/hassio/core/info",
            json={
                "result": "ok",
                "data": {"version": "2024.4.0", "version_latest": "2024.4.0"},
            },
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["ha", "core", "update"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Already running the latest release" in result.output


def test_core_update_needs_update() -> None:
    """Test core update when newer version available."""
    with requests_mock.Mocker() as mock:
        mock.get(
            "http://localhost:8123/api/",
            json={"message": "API running."},
            status_code=200,
        )
        mock.get(
            "http://localhost:8123/api/hassio/core/info",
            json={
                "result": "ok",
                "data": {"version": "2024.3.0", "version_latest": "2024.4.0"},
            },
            status_code=200,
        )
        mock.post(
            "http://localhost:8123/api/hassio/core/update",
            json={"result": "ok", "data": {}},
            status_code=200,
        )

        runner = CliRunner()
        result = runner.invoke(
            cli.cli,
            ["ha", "core", "update"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0
        assert "Already running the latest release" not in result.output
