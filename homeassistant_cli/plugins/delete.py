"""Delete plugin for Home Assistant CLI (hass-cli)."""
import logging

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import req_raw

_LOGGING = logging.getLogger(__name__)


@click.group('delete', hidden=True)
@pass_context
def cli(ctx):
    """Delete entities."""
    _LOGGING.warning("`delete` is deprecated, use `entity delete`")


@cli.command()
@click.argument(
    'entity', required='true', autocompletion=autocompletion.entities
)
@pass_context
def state(ctx, entity):
    """Delete state from Home Assistant."""
    response = req_raw(ctx, 'delete', 'states/{}'.format(entity))
    click.echo(response)
