"""Configuration plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api


@click.group('config')
@pass_context
def cli(ctx):
    """Get configuration from a Home Assistant instance."""


@cli.command()
@pass_context
def full(ctx: Configuration):
    """Get the full configuration from Home Assistant."""
    click.echo(format_output(ctx, api.get_config(ctx)))


@cli.command()
@pass_context
def components(ctx: Configuration):
    """Get loaded components from Home Assistant."""
    click.echo(format_output(ctx, api.get_config(ctx)['components']))


@cli.command()
@pass_context
def whitelist_dirs(ctx: Configuration):
    """Get the whitelisted directories from Home Assistant."""
    click.echo(format_output(
        ctx, api.get_config(ctx)['whitelist_external_dirs']))
