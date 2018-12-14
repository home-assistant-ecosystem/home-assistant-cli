"""Location plugin for Home Assistant CLI (hass-cli)."""
import logging

import click
from homeassistant_cli.cli import pass_context
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('system')
@pass_context
def cli(ctx):
    """System details and operations for Home Assistant."""


@cli.command()
@pass_context
def log(ctx):
    """Get errors from Home Assistant."""
    click.echo(api.get_raw_error_log(ctx))
