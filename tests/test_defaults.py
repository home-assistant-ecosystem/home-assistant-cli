"""Tests file for Home Assistant CLI (hass-cli)."""
import os
from typing import Dict, Optional
from unittest import mock

import pytest
import requests_mock

import homeassistant_cli.cli as cli

HASSIO_SERVER_FALLBACK = "http://hassio/homeassistant"
HASS_SERVER = "http://localhost:8123"


@pytest.mark.parametrize(
    "description,env,expected_server,expected_resolved_server,\
    expected_token,expected_password",
    [
        (
            "No env set, all should be defaults",
            {},
            'auto',
            HASS_SERVER,
            None,
            None,
        ),
        (
            "If only HASSIO_TOKEN, use default hassio",
            {'HASSIO_TOKEN': 'supersecret'},
            'auto',
            HASSIO_SERVER_FALLBACK,
            "supersecret",
            None,
        ),
        (
            "Honor HASS_SERVER together with HASSIO_TOKEN",
            {
                'HASSIO_TOKEN': 'supersecret',
                'HASS_SERVER': 'http://localhost:63333',
            },
            "http://localhost:63333",
            "http://localhost:63333",
            "supersecret",
            None,
        ),
        (
            "HASS_TOKEN should win over HASIO_TOKEN",
            {'HASSIO_TOKEN': 'supersecret', 'HASS_TOKEN': 'I Win!'},
            'auto',
            HASS_SERVER,
            'I Win!',
            None,
        ),
        (
            "HASS_PASSWORD should be honored",
            {'HASS_PASSWORD': 'supersecret'},
            'auto',
            HASS_SERVER,
            None,
            'supersecret',
        ),
    ],
)
def test_defaults(
    description: str,
    env: Dict[str, str],
    expected_resolved_server,
    expected_server: str,
    expected_token: Optional[str],
    expected_password: Optional[str],
) -> None:
    """Test defaults applied correctly for server, token and password."""
    mockenv = mock.patch.dict(os.environ, env)

    try:
        mockenv.start()
        with requests_mock.mock() as mockhttp:
            expserver = "{}/api/discovery_info".format(
                expected_resolved_server
            )
            mockhttp.get(
                expserver, json={"name": "mock response"}, status_code=200
            )
            ctx = cli.cli.make_context('hass-cli', ['--timeout', '1', 'info'])
            with ctx:  # type: ignore
                cli.cli.invoke(ctx)

            cfg = ctx.obj

            assert cfg.server == expected_server
            assert cfg.resolve_server() == expected_resolved_server
            assert cfg.token == expected_token

            assert mockhttp.call_count == 1

            assert mockhttp.request_history[0].url.startswith(
                expected_resolved_server
            )

            if expected_token:
                auth = mockhttp.request_history[0].headers["Authorization"]
                assert auth == "Bearer " + expected_token
            elif expected_password:
                password = mockhttp.request_history[0].headers["x-ha-access"]
                assert password == expected_password
            else:
                assert (
                    "Authorization" not in mockhttp.request_history[0].headers
                )
                assert "x-ha-access" not in mockhttp.request_history[0].headers

    finally:
        mockenv.stop()
