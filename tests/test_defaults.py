"""Tests file for Home Assistant CLI (hass-cli)."""
import os
from typing import Dict, Optional, no_type_check
from unittest import mock

import homeassistant_cli.cli as cli
import pytest

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
        ctx = cli.cli.make_context('hass-cli', ['--timeout', '1', 'info'])
        with ctx:
            try:
                cli.cli.invoke(ctx)
            except Exception:  # pylint: disable=broad-except
                pass

        cfg = ctx.obj

        assert cfg.server == expected_server
        assert cfg.token == expected_token
    finally:
        mockenv.stop()
