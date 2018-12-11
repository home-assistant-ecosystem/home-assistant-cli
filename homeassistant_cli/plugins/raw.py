"""Raw plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging

import click
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('raw')
@pass_context
def cli(ctx):
    """Call the raw API (advanced)."""


@cli.command()
@click.argument('method')
@pass_context
def get(ctx: Configuration, method):
    """Do a GET request against api/<method>."""
    response = api.restapi(ctx, 'get', method)

    if response.text:
        try:
            ctx.echo(
                "%s: %s",
                response.status_code,
                format_output(ctx, response.json()),
            )
        except json_.decoder.JSONDecodeError:
            ctx.echo("%s: %s", response.status_code, response.text)
    else:
        _LOGGING.warning(
            "%s: <No output returned from GET %s>",
            response.status_code,
            method,
        )


@cli.command()
@click.argument('method')
@click.option('--json')
@pass_context
def post(ctx: Configuration, method, json):
    """Do a POST request against api/<method>."""
    if json:
        data = json_.loads(json)
    else:
        data = {}

    response = api.restapi(ctx, 'get', data)

    response.raise_for_status()

    if response.text:
        try:
            ctx.echo(
                "%s: %s",
                response.status_code,
                format_output(ctx, response.json()),
            )
        except json_.decoder.JSONDecodeError:
            ctx.echo("%s: %s", response.status_code, response.text)
    else:
        _LOGGING.warning(
            "%s: <No output returned from POST %s>",
            response.status_code,
            method,
        )
