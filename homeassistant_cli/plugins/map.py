"""Map plugin for Home Assistant CLI (hass-cli)."""
import webbrowser

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req

OSM_URL = 'https://www.openstreetmap.org'
ZOOM = 17


@click.command('map')
@pass_context
def cli(ctx):
    """Print the current location on a map."""
    response = req(ctx, 'get', 'config')

    url = '{0}/?mlat={2}&mlon={3}#map={1}/{2}/{3}'.format(
        OSM_URL, ZOOM, response.get('latitude'), response.get('longitude'))
    webbrowser.open_new_tab(url)
