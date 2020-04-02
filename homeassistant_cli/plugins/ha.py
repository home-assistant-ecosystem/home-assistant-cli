"""Home Assistant (former Hass.io) plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging
from typing import Any, Dict, List, cast  # noqa: F401

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('ha')
@pass_context
def cli(ctx: Configuration):
    """Home Assistant (former Hass.io) commands."""
    ctx.auto_output("data")


def _report(ctx, cmd, method, response) -> None:
    """Create a report."""
    response.raise_for_status()

    if response.ok:
        try:
            ctx.echo(format_output(ctx, response.json()))
        except json_.decoder.JSONDecodeError:
            _LOGGING.debug("Response could not be parsed as JSON")
            ctx.echo(response.text)
    else:
        _LOGGING.warning(
            "%s: <No output returned from %s %s>",
            response.status_code,
            cmd,
            method,
        )


def _handle(ctx, method, httpmethod='get') -> None:
    """Handle the data."""
    method = "/api/hassio/" + method
    response = api.restapi(ctx, httpmethod, method)
    api.restapi(ctx, httpmethod, method)

    _report(ctx, httpmethod, method, response)


@cli.group('supervisor')
@pass_context
def supervisor(ctx: Configuration):
    """Home Assistant supervisor commands."""
    ctx.auto_output("data")


@supervisor.command()
@pass_context
def ping(ctx: Configuration):
    """Home Assistant supervisor ping."""
    _handle(ctx, 'supervisor/ping')


@supervisor.command()
@pass_context
def info(ctx: Configuration):
    """Home Assistant supervisor info."""
    _handle(ctx, 'supervisor/info')


@supervisor.command()
@pass_context
def update(ctx: Configuration):
    """Home Assistant supervisor update."""
    _handle(ctx, 'supervisor/update', 'post')


@supervisor.command('options')
@pass_context
def supervisor_options(ctx: Configuration):
    """Home Assistant supervisor options."""
    _handle(ctx, 'supervisor/options', 'post')


@supervisor.command('reload')
@pass_context
def supervisor_reload(ctx: Configuration):
    """Home Assistant supervisor reload."""
    _handle(ctx, 'supervisor/reload', 'post')


@supervisor.command()
@pass_context
def logs(ctx: Configuration):
    """Home Assistant supervisor logs."""
    _handle(ctx, 'supervisor/logs')


@supervisor.command()
@pass_context
def repair(ctx: Configuration):
    """Home Assistant supervisor repair."""
    _handle(ctx, 'supervisor/repair')


@cli.group('snapshot')
@pass_context
def snapshot(ctx: Configuration):
    """Home Assistant snapshot commands."""
    ctx.auto_output('data')


@snapshot.command('reload')
@pass_context
def snapshot_reload(ctx: Configuration):
    """Home Assistant snapshots reload."""
    _handle(ctx, 'snapshots/reload', 'post')


@snapshot.command()
@pass_context
def shutdown(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, 'host/shutdown', 'post')


@cli.group('host')
@pass_context
def host(ctx: Configuration):
    """Home Assistant host commands."""
    ctx.auto_output('data')


@host.command()
@pass_context
def reboot(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, 'host/reboot', 'post')


@host.command('reload')
@pass_context
def host_reload(ctx: Configuration):
    """Home Assistant host reload."""
    _handle(ctx, 'host/reload', 'post')


@host.command()
@pass_context
def shutdown(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, 'host/shutdown', 'post')


@host.command()
@pass_context
def info(ctx: Configuration):
    """Home Assistant host shutdown."""
    _handle(ctx, 'host/info')


@host.command()
@pass_context
def options(ctx: Configuration):
    """Home Assistant options shutdown."""
    _handle(ctx, 'host/options', 'post')


@host.command()
@pass_context
def services(ctx: Configuration):
    """Home Assistant host reboot."""
    _handle(ctx, 'host/services')


@cli.group('os')
@pass_context
def os(ctx: Configuration):
    """Home Assistant os commands."""
    ctx.auto_output('data')


@os.command()
@pass_context
def info(ctx: Configuration):
    """Home Assistant os info."""
    _handle(ctx, 'os/info')


# @os.command()
# @pass_context
# def update(ctx: Configuration):
#     """Home Assistant os update."""
#     _handle(ctx, 'os/update', 'post')

@cli.group('hardware')
@pass_context
def hardware(ctx: Configuration):
    """Home Assistant hardware info."""
    ctx.auto_output('data')


@hardware.command()
@pass_context
def audio(ctx: Configuration):
    """Home Assistant hardware audio."""
    _handle(ctx, 'hardware/audio')


@hardware.command()
@pass_context
def trigger(ctx: Configuration):
    """Home Assistant hardware trigger."""
    _handle(ctx, 'hardware/tripper')


@cli.group('addons')
@pass_context
def addons(ctx: Configuration):
    """Home Assistant addons commands."""
    ctx.auto_output('data')


@addons.command()
@pass_context
def all(ctx: Configuration):
    """Home Assistant addons info."""
    _handle(ctx, 'addons')


@addons.command()
@pass_context
def reload(ctx: Configuration):
    """Home Assistant addons reload."""
    _handle(ctx, 'addons/reload', 'post')


@cli.group('core')
@pass_context
def core(ctx: Configuration):
    """Home Assistant core commands."""
    ctx.auto_output('data')


@core.command()
@pass_context
def info(ctx: Configuration):
    """Home Assistant core info."""
    _handle(ctx, 'core/info')


@core.command()
@pass_context
def update(ctx: Configuration):
    """Home Assistant core update."""
    _handle(ctx, 'core/update')


@core.command()
@pass_context
def logs(ctx: Configuration):
    """Home Assistant core logs."""
    _handle(ctx, 'core/logs')


@core.command()
@pass_context
def restart(ctx: Configuration):
    """Home Assistant core restart."""
    _handle(ctx, 'core/restart', 'post')


@core.command()
@pass_context
def check(ctx: Configuration):
    """Home Assistant core check."""
    _handle(ctx, 'core/check', 'post')


@core.command()
@pass_context
def start(ctx: Configuration):
    """Home Assistant core start."""
    _handle(ctx, 'core/start', 'post')


@core.command()
@pass_context
def stop(ctx: Configuration):
    """Home Assistant core stop."""
    _handle(ctx, 'core/stop', 'post')


@core.command()
@pass_context
def rebuild(ctx: Configuration):
    """Home Assistant core rebuild."""
    _handle(ctx, 'core/rebuild', 'post')


@core.command()
@pass_context
def options(ctx: Configuration):
    """Home Assistant core options."""
    _handle(ctx, 'core/options', 'post')


@core.command()
@pass_context
def websocket(ctx: Configuration):
    """Home Assistant core websocket."""
    _handle(ctx, 'core/websocket')


@core.command()
@pass_context
def stats(ctx: Configuration):
    """Home Assistant core stats."""
    _handle(ctx, 'core/stats')
