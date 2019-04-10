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
    ctx.auto_output('table')


COLUMNS_DETAILS = [
    ("VERSION", "version"),
    ("CONFIG", "config_dir"),
    ("TZ", "time_zone"),
    ("LOCATION", "location_name"),
    ("LONGITUDE", "longitude"),
    ("LATITUDE", "latitude"),
    ("ELEVATION", "elevation"),
    ("TZ", "time_zone"),
    ("UNITS", "unit_system"),
]


@cli.command()
@pass_context
def full(ctx: Configuration):
    """Get full details on the configuration from Home Assistant."""
    click.echo(
        format_output(
            ctx,
            [api.get_config(ctx)],
            columns=ctx.columns if ctx.columns else COLUMNS_DETAILS,
        )
    )


@cli.command()
@pass_context
def components(ctx: Configuration):
    """Get loaded components from Home Assistant."""
    click.echo(
        format_output(
            ctx,
            api.get_config(ctx)['components'],
            columns=ctx.columns if ctx.columns else [('COMPONENT', '$')],
        )
    )


@cli.command()
@pass_context
def whitelist_dirs(ctx: Configuration):
    """Get the whitelisted directories from Home Assistant."""
    click.echo(
        format_output(
            ctx,
            api.get_config(ctx)['whitelist_external_dirs'],
            columns=ctx.columns if ctx.columns else [('DIRECTORY', '$')],
        )
    )


@cli.command()
@pass_context
def release(ctx: Configuration):
    """Get the release of Home Assistant."""
    click.echo(
        format_output(
            ctx,
            [api.get_config(ctx)['version']],
            columns=ctx.columns if ctx.columns else [('VERSION', '$')],
        )
    )
