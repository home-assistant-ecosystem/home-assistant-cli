"""Discovery plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output


@click.command('discover')
@click.option(
    '--raw', is_flag=True, help="Include raw data found during scan."
)
@pass_context
def cli(ctx: Configuration, raw):
    """Discovery for the local network."""
    from netdisco.discovery import NetworkDiscovery

    click.echo("Running discovery on network (might take a while)...")
    netdiscovery = NetworkDiscovery()
    netdiscovery.scan()

    for device in netdiscovery.discover():
        info = netdiscovery.get_info(device)
        click.echo("{}:\n{}".format(device, format_output(ctx, info)))

    if raw:
        click.echo("Raw data:")
        netdiscovery.print_raw_data()

    netdiscovery.stop()
