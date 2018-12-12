"""Edit plugin for Home Assistant CLI (hass-cli)."""
import json as json_
import logging
import shlex
from typing import Any, Dict, cast, no_type_check  # NOQA

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import raw_format_output, req_raw
import yaml

_LOGGING = logging.getLogger(__name__)


@click.group('edit', hidden=True)
@pass_context
def cli(ctx):
    """Edit entities."""
    _LOGGING.warning(
        "'edit' is deprecated use 'entity edit' or 'event fire' instead."
    )


@cli.command()
@no_type_check
@click.argument(
    'entity', required=True, autocompletion=autocompletion.entities
)
@click.argument('newstate', required=False)
@click.option(
    '--attributes', help="Comma separated key/value pairs to use as attributes"
)
@click.option(
    '--json',
    help="Raw JSON state to use for setting. Overrides any other"
    "state values provided.",
)
@click.option(
    '--merge',
    is_flag=True,
    default=False,
    help="If set and the entity exists the state and attributes will"
    "be merged into the state rather than overwrite.",
    show_default=True,
)
@pass_context
def state(ctx: Configuration, entity, newstate, attributes, merge, json):
    """Edit state from Home Assistant."""
    if json:
        response = req_raw(ctx, 'post', 'states/{}'.format(entity), json)
    elif newstate or attributes:
        wanted_state = {}  # type: Dict[str, Any]
        existing_state = None

        response = req_raw(ctx, 'get', 'states/{}'.format(entity))

        if response.ok:
            click.echo("Existing state found for {}".format(entity))
            existing_state = response.json()
            if merge:
                wanted_state = existing_state
        else:
            click.echo("No existing state found for '{}'".format(entity))

        if attributes:
            lexer = shlex.shlex(attributes, posix=True)
            lexer.whitespace_split = True
            lexer.whitespace = ','
            attributes_dict = cast(
                Dict[str, str], dict(pair.split('=', 1) for pair in lexer)
            )

            newattr = wanted_state.get('attributes', {})
            newattr.update(attributes_dict)
            wanted_state['attributes'] = newattr

        if newstate:
            wanted_state['state'] = newstate
        else:
            if not existing_state:
                raise ValueError("No new or existing state provided.")
            wanted_state['state'] = existing_state['state']

        newjson = raw_format_output('json', wanted_state)

        response = req_raw(ctx, 'post', 'states/{}'.format(entity), newjson)
    else:
        existing = req_raw(ctx, 'get', 'states/{}'.format(entity)).json()

        existing = raw_format_output(ctx.output, existing)
        new = click.edit(existing, extension='.{}'.format(ctx.output))

        if new is not None:
            click.echo("Updating '{}'".format(entity))
            if ctx.output == 'yaml':
                new = json_.dumps(yaml.load(new))
            response = req_raw(ctx, 'post', 'states/{}'.format(entity), new)
        else:
            click.echo("No edits/changes.")


@cli.command('event')
@no_type_check
@click.argument('event', required=True, autocompletion=autocompletion.events)
@click.option(
    '--json',
    help="Raw JSON state to use for event. Overrides any other state"
    "values provided.",
)
@pass_context
def eventcmd(ctx: Configuration, event, json):
    """Edit/fire event in Home Assistant."""
    if json:
        click.echo("Fire {}".format(event))
        response = req_raw(ctx, 'post', 'events/{}'.format(event), json)
        response.raise_for_status()
    else:
        existing = raw_format_output(ctx.output, {})
        new = click.edit(existing, extension='.{}'.format(ctx.output))

        if new is not None:
            click.echo("Fire {}".format(event))
            if ctx.output == 'yaml':
                new = json_.dumps(yaml.load(new))
            response = req_raw(ctx, 'post', 'events/{}'.format(event), new)
            response.raise_for_status()
        else:
            click.echo("No edits/changes.")
