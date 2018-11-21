"""Location plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req, format_output

@click.command('info')
@pass_context
def cli(ctx):
    """Get basic info from Home Assistant using /api/discovery_info."""

    click.echo(format_output(ctx, req(ctx, "get", "discovery_info")))

