"""Edit plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import raw_format_output
import homeassistant_cli.remote as api
import yaml

_LOGGING = logging.getLogger(__name__)


@click.group('event')
@pass_context
def cli(ctx):
    """Interact with events."""


@cli.command()
@click.argument(  # type: ignore
    'event', required=True, autocompletion=autocompletion.events
)
@click.option(
    '--json',
    help="Raw JSON state to use for event. Overrides any other state"
    "values provided.",
)
@pass_context
def fire(ctx: Configuration, event, json):
    """Fire event in Home Assistant."""
    if json:
        click.echo("Fire {}".format(event))
        response = api.fire_event(ctx, event, json)
    else:
        existing = raw_format_output(ctx.output, {})
        new = click.edit(existing, extension='.{}'.format(ctx.output))

        if new:
            click.echo("Fire {}".format(event))
            if ctx.output == 'yaml':
                data = yaml.load(new)
            else:
                data = json_.loads(new)

            response = api.fire_event(ctx, event, data)
        else:
            click.echo("No edits/changes.")
            return

    if response:
        ctx.echo(raw_format_output(ctx.output, response))
