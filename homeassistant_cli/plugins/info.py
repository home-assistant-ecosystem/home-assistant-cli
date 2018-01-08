"""Location plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import json_output, timestamp, req
from homeassistant_cli.const import DEFAULT_PORT

OSM_URL = 'https://www.openstreetmap.org'
ZOOM = 17


@click.command('info')
@click.option('--location', '-l', is_flag=True)
@click.option('--connect', '-c', is_flag=True)
@pass_context
def cli(ctx, location, connect):
    """Get configuration details."""
    import homeassistant.remote as remote
    config = remote.get_config(ctx.api)

    if not location and not connect:
        ctx.log(json_output(config))
        ctx.vlog('Details of %s, Recieved: %s', ctx.host, timestamp())

    if location and not connect:
        url = '{0}/?mlat={2}&mlon={3}#map={1}/{2}/{3}'.format(
            OSM_URL, ZOOM, config.get('latitude'), config.get('longitude'))
        webbrowser.open_new_tab(url)

    if connect and not location:
        url = 'http://{}:{}'.format(ctx.host, DEFAULT_PORT)
        webbrowser.open_new_tab(url)

