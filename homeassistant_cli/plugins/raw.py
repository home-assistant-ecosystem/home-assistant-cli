"""Location plugin for Home Assistant CLI (hass-cli)."""
import webbrowser
import urllib.parse

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req, req_raw, format_output

@click.group('raw')
@pass_context
def cli(ctx):
    """call raw api (advanced)"""

@cli.command()
@click.argument("method")
@pass_context
def get(ctx, method):
    """do a GET against api/<method>"""
    
    click.echo(format_output(ctx,req(ctx, "get", method)))
    
@cli.command()
@click.argument("method")
@click.option('--json')
@pass_context
def post(ctx, method,json):
    """do a POST against api/<method>"""

    click.echo(format_output(ctx,req(ctx, "post", method,json)))
    