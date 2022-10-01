"""Raw plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging
from typing import Any, Dict, List, cast  # noqa: F401

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import format_output
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('raw')
@pass_context
def cli(ctx: Configuration):
    """Call the raw API (advanced)."""
    ctx.auto_output("data")


def _report(ctx, cmd, method, response) -> None:
    """Create a report."""
    response.raise_for_status()

    if response.ok:
        try:
            ctx.echo(format_output(ctx, response.json()))
        except json_.decoder.JSONDecodeError:
            _LOGGING.debug("Response could not be parsed as JSON")
            ctx.echo(response.text)
    else:
        _LOGGING.warning(
            "%s: <No output returned from %s %s>",
            response.status_code,
            cmd,
            method,
        )


@cli.command()
@click.argument(
    'method', shell_complete=autocompletion.api_methods  # type: ignore
)
@pass_context
def get(ctx: Configuration, method):
    """Do a GET request against api/<method>."""
    response = api.restapi(ctx, 'get', method)

    _report(ctx, "GET", method, response)


@cli.command()
@click.argument(
    'method', shell_complete=autocompletion.api_methods  # type: ignore
)
@click.option('--json')
@pass_context
def post(ctx: Configuration, method, json):
    """Do a POST request against api/<method>."""
    if json:
        data = json_.loads(json)
    else:
        data = {}

    response = api.restapi(ctx, 'post', method, data)

    _report(ctx, "GET", method, response)


@cli.command("ws")
@click.argument(
    'wstype', shell_complete=autocompletion.wsapi_methods  # type: ignore
)
@click.option('--json')
@pass_context
def websocket(ctx: Configuration, wstype, json):  # noqa: D301
    """Send a websocket request against /api/websocket.

    WSTYPE is name of websocket methods.

    \b
    --json is dictionary to pass in addition to the type.
           Example: --json='{ "area_id":"2c8bf93c8082492f99c989896962f207" }'
    """
    if json:
        data = json_.loads(json)
    else:
        data = {}

    frame = {'type': wstype}
    frame = {**frame, **data}  # merging data into frame

    response = cast(List[Dict[str, Any]], api.wsapi(ctx, frame))

    ctx.echo(format_output(ctx, response))
