"""Discovery plugin for Home Assistant CLI (hass-cli)."""
import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import timestamp

@click.command('discovery')
@pass_context
def cli(ctx):
    """Discovery for the local network."""
    from netdisco.discovery import NetworkDiscovery

    netdiscovery = NetworkDiscovery()
    netdiscovery.scan()

    for device in netdiscovery.discover():
        print(device, netdiscovery.get_info(device))

    netdiscovery.stop()

    ctx.vlog('Discovery executed: %s',  timestamp())
