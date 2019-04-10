"""Map plugin for Home Assistant CLI (hass-cli)."""
import sys
import webbrowser

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.remote as api

OSM_URL = "https://www.openstreetmap.org/"
GOOGLE_URL = "https://www.google.com/maps/search/"
BING_URL = "https://www.bing.com/maps"
SERVICE = {
    'openstreetmap': OSM_URL + '?mlat={0}&mlon={1}#map=17/{0}/{1}',
    'google': GOOGLE_URL + '?api=1&query={0},{1}',
    'bing': BING_URL + '?v=2&cp={0}~{1}&lvl=17&sp=point.{0}_{1}_{2}',
}


@click.command('map')
@click.argument(  # type: ignore
    'entity', required=False, autocompletion=autocompletion.entities
)
@click.option(
    '--service', default='openstreetmap', type=click.Choice(SERVICE.keys())
)
@pass_context
def cli(ctx: Configuration, service: str, entity: str) -> None:
    """Show the location of the config or an entity on a map."""
    latitude = None
    longitude = None

    if entity:
        thing = entity
        data = api.get_state(ctx, entity)
        if data:
            attr = data.get('attributes', {})
            latitude = attr.get('latitude')
            longitude = attr.get('longitude')
            thing = attr.get('friendly_name', entity)
    else:
        thing = "configuration"
        response = api.get_config(ctx)
        if response:
            latitude = response.get('latitude')
            longitude = response.get('longitude')
            thing = response.get('location_name', thing)

    if latitude and longitude:
        urlpattern = SERVICE.get(service)
        import urllib.parse

        if urlpattern:
            url = urlpattern.format(
                latitude, longitude, urllib.parse.quote_plus(thing)
            )
            ctx.echo(
                "{} location is at {}, {}".format(thing, latitude, longitude)
            )
            webbrowser.open_new_tab(url)
        else:
            ctx.echo(
                "Could not find url pattern for service {}".format(service)
            )
    else:
        ctx.echo("No exact location info found in {}".format(thing))
        sys.exit(2)
