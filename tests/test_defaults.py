"""Tests file for Home Assistant CLI (hass-cli)."""
import os
from typing import Dict, Optional, no_type_check
from unittest import mock

import homeassistant_cli.cli as cli
import pytest
import requests_mock

HASSIO_SERVER_FALLBACK = "http://hassio/homeassistant"
HASS_SERVER = "http://localhost:8123"


@no_type_check
@pytest.mark.parametrize(
    "description,env,expected_server,expected_token",
    [
        ("No env set, all should be defaults", {}, HASS_SERVER, None),
        (
            "If only HASSIO_TOKEN, use default hassio",
            {'HASSIO_TOKEN': 'supersecret'},
            HASSIO_SERVER_FALLBACK,
            "supersecret",
        ),
        (
            "Honor HASS_SERVER together with HASSIO_TOKEN",
            {
                'HASSIO_TOKEN': 'supersecret',
                'HASS_SERVER': 'http://localhost:999999',
            },
            "http://localhost:999999",
            "supersecret",
        ),
        (
            "HASS_TOKEN should win over HASIO_TOKEN",
            {'HASSIO_TOKEN': 'supersecret', 'HASS_TOKEN': 'I Win!'},
            HASS_SERVER,
            'I Win!',
        ),
    ],
)
def test_defaults(
    description: str,
    env: Dict[str, str],
    expected_server: str,
    expected_token: Optional[str],
) -> None:
    """Test defaults applied correctly for server and token."""
    mockenv = mock.patch.dict(os.environ, env)

    try:
        mockenv.start()
        with requests_mock.mock() as mockhttp:
            expserver = "{}/api/discovery_info".format(expected_server)
            mockhttp.get(
                expserver, json={"name": "mock response"}, status_code=200
            )
            ctx = cli.cli.make_context('hass-cli', ['--timeout', '1', 'info'])
            with ctx:
                cli.cli.invoke(ctx)

            cfg = ctx.obj

            assert cfg.server == expected_server
            assert cfg.token == expected_token

            assert mockhttp.call_count == 1

            assert mockhttp.request_history[0].url.startswith(expected_server)

            if expected_token:
                auth = mockhttp.request_history[0].headers["Authorization"]
                assert auth == "Bearer " + expected_token
            else:
                assert (
                    "Authorization" not in mockhttp.request_history[0].headers
                )

    finally:
        mockenv.stop()
