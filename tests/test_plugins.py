"""Tests file for Home Assistant CLI (hass-cli)."""

from typing import List

from homeassistant_cli.cli import HomeAssistantCli, cli
import pytest

DFEAULT_PLUGINS = [
    'completion',
    'config',
    'delete',
    'discover',
    'edit',
    'entity',
    'event',
    'get',
    'info',
    'map',
    'raw',
    'template',
    'toggle',
]
DFEAULT_PLUGINS.sort()


@pytest.fixture(name="defaultplugins_sorted")
def defaultplugins_fixture() -> List[str]:
    """Return the exepcted default list of plugins"""
    return DFEAULT_PLUGINS


def test_commands_match_expected(defaultplugins_sorted) -> None:
    """Test plugin discovery."""

    hac = HomeAssistantCli()

    ctx = cli.make_context('hass-cli', ['info'])

    cmds = hac.list_commands(ctx)

    cmds.sort()

    assert cmds == defaultplugins_sorted


@pytest.mark.parametrize("plugin", DFEAULT_PLUGINS)
def test_commands_loads(plugin) -> None:
    """Test plugin discovery."""

    hac = HomeAssistantCli()

    ctx = cli.make_context('hass-cli', ['info'])

    cmd = hac.get_command(ctx, plugin)

    assert cmd
