"""Regression tests for raw and config-entry deletion."""

import json

import pytest
import requests_mock
from click.testing import CliRunner

import homeassistant_cli.cli as cli

ENTRY_URL = "http://localhost:8123/api/config/config_entries/entry"
ENTRY = {"entry_id": "helper-one", "domain": "template", "title": "Test sensor"}


@pytest.mark.parametrize("payload", [None, '{"force": true}', "-"])
def test_raw_delete_json(payload: str | None) -> None:
    """Send DELETE and preserve the JSON response and optional request body."""
    with requests_mock.Mocker() as request:
        request.delete(ENTRY_URL + "/helper-one", json={"require_restart": False})
        args = [
            "-o",
            "json",
            "raw",
            "delete",
            "/api/config/config_entries/entry/helper-one",
        ]
        if payload is not None:
            args += ["--json", payload]
        result = CliRunner().invoke(cli.cli, args, input='{"force": true}')
        assert result.exit_code == 0, result.output
        assert json.loads(result.output) == {"require_restart": False}
        assert request.last_request.method == "DELETE"
        if payload is not None:
            assert request.last_request.json() == {"force": True}
        else:
            assert not request.last_request.body


@pytest.mark.parametrize("status,text", [(204, ""), (200, "Deleted")])
def test_raw_delete_non_json(status: int, text: str) -> None:
    """Accept successful empty and plain-text responses."""
    with requests_mock.Mocker() as request:
        request.delete(ENTRY_URL + "/helper-one", status_code=status, text=text)
        result = CliRunner().invoke(
            cli.cli, ["raw", "delete", "/api/config/config_entries/entry/helper-one"]
        )
        assert result.exit_code == 0, result.output
        assert result.output.strip() == text


@pytest.mark.parametrize("status", [401, 403, 404, 500])
def test_raw_delete_http_error(status: int) -> None:
    """HTTP failures must not look successful to scripts."""
    with requests_mock.Mocker() as request:
        request.delete(ENTRY_URL + "/helper-one", status_code=status)
        result = CliRunner().invoke(
            cli.cli, ["raw", "delete", "/api/config/config_entries/entry/helper-one"]
        )
        assert result.exit_code == 1
        assert request.call_count == 1


def test_raw_delete_invalid_json() -> None:
    """Reject an invalid body before sending a deletion request."""
    with requests_mock.Mocker() as request:
        result = CliRunner().invoke(
            cli.cli, ["raw", "delete", "/api/anything", "--json", "{"]
        )
        assert result.exit_code != 0
        assert request.call_count == 0


def test_integration_delete_ambiguous() -> None:
    """Never select the first of multiple prefix matches for deletion."""
    with requests_mock.Mocker() as request:
        request.get(ENTRY_URL, json=[ENTRY, {**ENTRY, "entry_id": "helper-two"}])
        result = CliRunner().invoke(
            cli.cli, ["integration", "delete", "helper-", "--confirm"]
        )
        assert result.exit_code == 1
        assert "ambiguous" in result.output.lower()
        assert [item.method for item in request.request_history] == ["GET"]


def test_integration_delete_empty_id() -> None:
    """An empty ID must not select an entry, even when only one exists."""
    with requests_mock.Mocker() as request:
        request.get(ENTRY_URL, json=[ENTRY])
        result = CliRunner().invoke(cli.cli, ["integration", "delete", "", "--confirm"])
        assert result.exit_code == 1
        assert "must not be empty" in result.output
        assert request.call_count == 0


@pytest.mark.parametrize("entry_id", ["helper-one", "helper-on"])
def test_integration_delete_exact_or_unique(entry_id: str) -> None:
    """Prefer an exact ID over an earlier prefix match; accept unique prefixes."""
    with requests_mock.Mocker() as request:
        entries = [ENTRY]
        if entry_id == "helper-one":
            entries.insert(0, {**ENTRY, "entry_id": "helper-one-longer"})
        request.get(ENTRY_URL, json=entries)
        request.delete(ENTRY_URL + "/helper-one", json={"require_restart": False})
        result = CliRunner().invoke(
            cli.cli, ["integration", "delete", entry_id, "--confirm"]
        )
        assert result.exit_code == 0, result.output
        assert "Successfully deleted" in result.output
        assert request.last_request.url == ENTRY_URL + "/helper-one"


def test_integration_delete_missing() -> None:
    """A missing entry must not cause any DELETE request."""
    with requests_mock.Mocker() as request:
        request.get(ENTRY_URL, json=[ENTRY])
        result = CliRunner().invoke(
            cli.cli, ["integration", "delete", "missing", "--confirm"]
        )
        assert result.exit_code == 1
        assert request.call_count == 1


def test_integration_delete_cancelled() -> None:
    """Declining the existing confirmation must not send DELETE."""
    with requests_mock.Mocker() as request:
        request.get(ENTRY_URL, json=[ENTRY])
        result = CliRunner().invoke(
            cli.cli, ["integration", "delete", "helper-one"], input="n\n"
        )
        assert result.exit_code == 1
        assert request.call_count == 1


@pytest.mark.parametrize("status", [403, 404, 500])
def test_integration_delete_server_failure(status: int) -> None:
    """A server failure, including a concurrent removal, must exit nonzero."""
    with requests_mock.Mocker() as request:
        request.get(ENTRY_URL, json=[ENTRY])
        request.delete(ENTRY_URL + "/helper-one", status_code=status)
        result = CliRunner().invoke(
            cli.cli, ["integration", "delete", "helper-one", "--confirm"]
        )
        assert result.exit_code == 1
        assert "Successfully deleted" not in result.output
        assert request.last_request.method == "DELETE"
