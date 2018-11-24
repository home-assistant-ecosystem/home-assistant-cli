"""Config plugin for Home Assistant CLI (hass-cli)."""
import click
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import format_output, req


@click.command('config')
@pass_context
def cli(ctx):
    """Get basic info from Home Assistant using /api/config."""
    click.echo(format_output(ctx, req(ctx, 'get', 'config')))
