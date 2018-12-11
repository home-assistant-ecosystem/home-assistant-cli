"""Delete plugin for Home Assistant CLI (hass-cli)."""
import logging
from typing import no_type_check

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import req_raw

_LOGGING = logging.getLogger(__name__)


@click.group('delete', hidden=True)
@pass_context
def cli(ctx) -> None:
    """Delete entities."""
    _LOGGING.warning("`delete` is deprecated, use `entity delete`")


@cli.command()
@no_type_check
@click.argument(
    'entity', required=True, autocompletion=autocompletion.entities
)
@pass_context
def state(ctx: Configuration, entity) -> None:
    """Delete state from Home Assistant."""
    response = req_raw(ctx, 'delete', 'states/{}'.format(entity))
    click.echo(str(response))
