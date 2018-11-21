"""Delete plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse
import yaml
import click
import json as json_

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req, req_raw, raw_format_output, format_output
import homeassistant_cli.autocompletion as autocompletion


@click.group('delete')
@pass_context
def cli(ctx):
    """Delete entities."""

@cli.command()
@click.argument('entity', required="true", autocompletion=autocompletion.entities)
@pass_context
def state(ctx, entity):
    """Delete state from Home Assistant."""
    response = req_raw(ctx,"delete", "states/{}".format(entity))
    click.echo(response)
    

