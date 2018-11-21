"""Location plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req, req_raw, format_output

import homeassistant_cli.autocompletion as autocompletion


@click.group('toggle')
@pass_context
def cli(ctx):
    """toggle data from Home Assistant"""

@cli.command()
@click.argument('entities', nargs=-1, required=True, autocompletion=autocompletion.entities)
@pass_context
def state(ctx, entities):
    """toggle state from Home Assistant"""
    for entity in entities:
            import json
            data = {
                "entity_id" : entity
            }
            click.echo("Toggling {}".format(entity))
            response = req_raw(ctx,"post", "services/homeassistant/toggle", json.dumps(data))
            if response.ok:
                result = response.json()
                click.echo(format_output(ctx,response.json()))
                click.echo("{} entities reported to be toggled".format(len(result)))
                