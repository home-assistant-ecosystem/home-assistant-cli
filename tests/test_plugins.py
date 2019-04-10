"""Tests file for Home Assistant CLI (hass-cli)."""

from typing import List

import pytest

from homeassistant_cli.cli import HomeAssistantCli, cli

DFEAULT_PLUGINS = [
    'completion',
    'config',
    'discover',
    'state',
    'entity',
    'event',
    'info',
    'map',
    'raw',
    'service',
    'system',
    'template',
    'area',
    'device',
]
DFEAULT_PLUGINS.sort()


@pytest.fixture(name="defaultplugins_sorted")
def defaultplugins_fixture() -> List[str]:
    """Return the exepcted default list of plugins."""
    return DFEAULT_PLUGINS


def test_commands_match_expected(defaultplugins_sorted) -> None:
    """Test plugin discovery."""
    hac = HomeAssistantCli()

    ctx = cli.make_context('hass-cli', ['info'])

    cmds = hac.list_commands(ctx)

    cmds.sort()

    diff = set(cmds).difference(set(defaultplugins_sorted))

    assert not diff


@pytest.mark.parametrize("plugin", DFEAULT_PLUGINS)
def test_commands_loads(plugin) -> None:
    """Test plugin discovery."""
    hac = HomeAssistantCli()

    ctx = cli.make_context('hass-cli', ['info'])

    cmd = hac.get_command(ctx, plugin)

    assert cmd
