"""Raw plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


def _report(ctx, cmd, method, response) -> None:

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

    method = "/api/hassio/" + method
    response = api.restapi(ctx, httpmethod, method)

    _report(ctx, httpmethod, method, response)


@click.group('hassio')
@pass_context
def cli(ctx: Configuration):
    """Hass.io commands (if available)."""
    ctx.auto_output("data")


@cli.group('supervisor')
@pass_context
def supervisor(ctx: Configuration):
    """Hass.io supervisor commands."""
    ctx.auto_output("data")


@supervisor.command()
@pass_context
def info(ctx: Configuration):
    """Hass.io supervisor info."""
    _handle(ctx, 'supervisor/info')


@supervisor.command()
@pass_context
def logs(ctx: Configuration):
    """Hass.io supervisor logs."""
    _handle(ctx, 'supervisor/logs')


@supervisor.command()
@pass_context
def reload(ctx: Configuration):
    """Hass.io supervisor reload."""
    _handle(ctx, 'supervisor/reload', 'post')


@cli.group('host')
@pass_context
def host(ctx: Configuration):
    """Hass.io Host commands."""
    ctx.auto_output('data')


@host.command('logs')
@pass_context
def hostlogs(ctx: Configuration):
    """Hass.io host logs."""
    _handle(ctx, 'host/info')


@host.command()
@pass_context
def reboot(ctx: Configuration):
    """Hass.io host reboot."""
    _handle(ctx, 'host/reboot', 'post')


@host.command('reload')
@pass_context
def hostreload(ctx: Configuration):
    """Hass.io host reload."""
    _handle(ctx, 'host/reload', 'post')


@host.command()
@pass_context
def shutdown(ctx: Configuration):
    """Hass.io host shutdown."""
    _handle(ctx, 'host/shutdown', 'post')
