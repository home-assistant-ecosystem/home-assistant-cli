"""System plugin for Home Assistant CLI (hass-cli)."""

import logging

import click

import homeassistant_cli.const as const
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output

_LOGGING = logging.getLogger(__name__)


@click.group("system")
@pass_context
def cli(ctx):
    """System details and operations for Home Assistant."""


@cli.command()
@pass_context
def log(ctx):
    """Get errors from Home Assistant."""
    click.echo(api.get_raw_error_log(ctx))


@cli.command()
@pass_context
def health(ctx: Configuration):
    """Get system health from Home Assistant."""
    info = api.get_health(ctx)

    ctx.echo(
        format_output(
            ctx,
            [info],
            columns=ctx.columns if ctx.columns else const.COLUMNS_DEFAULT,
        )
    )
