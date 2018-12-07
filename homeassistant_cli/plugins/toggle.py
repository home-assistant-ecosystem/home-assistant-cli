"""Location plugin for Home Assistant CLI (hass-cli)."""
import json
import logging

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import format_output, req_raw

_LOGGING = logging.getLogger(__name__)


@click.group('toggle', hidden=True)
@pass_context
def cli(ctx):
    """Generic toggle of state/switches from Home Assistant."""
    _LOGGING.warning("`toggle` is deprecated, use `entity toggle` instead.")


@cli.command()
@click.argument(
    'entities', nargs=-1, required=True, autocompletion=autocompletion.entities
)
@pass_context
def state(ctx, entities):
    """Toggle state from Home Assistant."""
    for entity in entities:
        data = {'entity_id': entity}
        click.echo("Toggling {}".format(entity))
        response = req_raw(
            ctx, 'post', 'services/homeassistant/toggle', json.dumps(data)
        )
        if response.ok:
            result = response.json()
            click.echo(format_output(ctx, response.json()))
            click.echo(
                "{} entities reported to be toggled".format(len(result))
            )
