"""Configuration plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse
from collections import namedtuple

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import timestamp

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
        ctx.log(format_config(config))
        ctx.vlog('Details of %s, Recieved: %s', ctx.host, timestamp())

    if location and not connect:
        url = '{0}/?mlat={2}&mlon={3}#map={1}/{2}/{3}'.format(
            OSM_URL, ZOOM, config.get('latitude'), config.get('longitude'))
        webbrowser.open_new_tab(url)

    if connect and not location:
        url = 'http://{}:{}'.format(ctx.host, ctx.port)
        webbrowser.open_new_tab(url)

def format_config(config):
    UnitSystem = namedtuple('UnitSystem', ['mass', 'volume', 'distance', 'temperature'])
    units = namedtuple('UnitSystem', config.get('unit_system').keys())(**config.get('unit_system'))
    format_arguments = {
            **config,
            'whitelist_external_dirs': ', '.join(config.get('whitelist_external_dirs')),
            'units': units,
            'components': ', '.join(sorted(config.get('components'))),
            }
    return """
Location name:                      {location_name}
Version:                            {version}
Location:                           {latitude}°, {longitude}°
Elevation:                          {elevation}{units.length}
Timezone:                           {time_zone}
Whitelisted external directories:   {whitelist_external_dirs}
Config dir:                         {config_dir}
Units:
    Mass:                           {units.mass}
    Volume:                         {units.volume}
    Distance:                       {units.length}
    Temperature:                    {units.temperature}
Components:                         {components}
    """.strip().format(**format_arguments)
