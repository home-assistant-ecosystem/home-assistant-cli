"""Map plugin for Home Assistant CLI (hass-cli)."""
import webbrowser

import click
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.remote as api

OSM_URL = 'https://www.openstreetmap.org'
ZOOM = 17


@click.command('map')
@pass_context
def cli(ctx: Configuration) -> None:
    """Print the current location on a map."""
    response = api.get_config(ctx)

    if response:
        url = '{0}/?mlat={2}&mlon={3}#map={1}/{2}/{3}'.format(
            OSM_URL, ZOOM, response.get('latitude'), response.get('longitude')
        )
        webbrowser.open_new_tab(url)
