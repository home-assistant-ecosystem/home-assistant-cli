"""Info plugin for Home Assistant CLI (hass-cli)."""
import logging

import click
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.command('info')
@pass_context
def cli(ctx):
    """Get basic info from Home Assistant."""
    _LOGGING.info(format_output(ctx, api.get_info(ctx)))
