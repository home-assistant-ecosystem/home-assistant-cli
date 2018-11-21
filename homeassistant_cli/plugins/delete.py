"""Delete plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import urllib.parse
import webbrowser

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import (
    format_output, raw_format_output, req, req_raw)
import yaml


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
