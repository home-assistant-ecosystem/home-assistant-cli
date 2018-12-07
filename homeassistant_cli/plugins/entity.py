"""Location plugin for Home Assistant CLI (hass-cli)."""

import json as json_
import logging
import shlex

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import format_output, raw_format_output
import homeassistant_cli.remote as api
import yaml

_LOGGING = logging.getLogger(__name__)


@click.group('entity')
@pass_context
def cli(ctx):
    """Get info and operate on entities from Home Assistant."""


@cli.command()
@click.argument(
    'entity', required=True, autocompletion=autocompletion.entities
)
@pass_context
def get(ctx, entity):
    """Get/read entity state from Home Assistant."""
    _LOGGING.info(format_output(ctx, api.get_state(ctx, entity)))


@cli.command()
@click.argument(
    'entity', required='true', autocompletion=autocompletion.entities
)
@pass_context
def delete(ctx, entity):
    """Delete entity from Home Assistant."""

    deleted = api.remove_state(ctx, entity)

    if deleted:
        _LOGGING.info("Entity %s deleted.", entity)
    else:
        _LOGGING.info("Entity %s not found.", entity)


@cli.command()
@pass_context
def list(ctx):
    """List all state from Home Assistant."""
    _LOGGING.info(format_output(ctx, api.get_states(ctx)))


@cli.command()
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
def edit(ctx, entity, newstate, attributes, merge, json):
    """Edit entity state from Home Assistant."""
    if json:
        _LOGGING.debug(
            "json found overriding/creating new state for entity %s", entity
        )
        wanted_state = json_.loads(json)
    elif newstate or attributes:
        wanted_state = {}
        existing_state = api.get_state(ctx, entity)

        if existing_state:
            click.echo("Existing state found for {}".format(entity))
            if merge:
                wanted_state = existing_state
        else:
            _LOGGING.info("No existing state found for '{}'".format(entity))

        if attributes:
            lexer = shlex.shlex(attributes, posix=True)
            lexer.whitespace_split = True
            lexer.whitespace = ','
            attributes_dict = dict(pair.split('=', 1) for pair in lexer)

            newattr = wanted_state.get('attributes', {})
            newattr.update(attributes_dict)
            # this is not hornoring merge!
            wanted_state['attributes'] = newattr

        if newstate:
            wanted_state['state'] = newstate
        else:
            if not existing_state:
                raise ValueError("No new or existing state provided.")
            wanted_state['state'] = existing_state['state']

    else:
        existing = api.get_state(ctx, entity)
        existing = raw_format_output(ctx.output, existing)
        new = click.edit(existing, extension='.{}'.format(ctx.output))

        if new is not None:
            _LOGGING.info("Updating '{}'".format(entity))
            if ctx.output == 'yaml':
                wanted_state = yaml.load(new)
            if ctx.output == 'json':
                wanted_state = json_.loads(new)

            api.set_state(ctx, entity, wanted_state)
        else:
            _LOGGING.info("No edits/changes returned from editor.")
            return

    _LOGGING.debug("wanted: %s", str(wanted_state))
    result = api.set_state(ctx, entity, wanted_state)
    _LOGGING.info("Entity %s updated succesfully", entity)
    _LOGGING.debug("Updated to: %s", result)


@cli.command()
@click.argument(
    'entities', nargs=-1, required=True, autocompletion=autocompletion.entities
)
@pass_context
def toggle(ctx, entities):
    """Toggle state for one or more entities in Home Assistant."""
    for entity in entities:
        data = {'entity_id': entity}
        _LOGGING.info("Toggling {}".format(entity))
        result = api.call_service(ctx, 'homeassistant', 'toggle', data)

        _LOGGING.debug(format_output(ctx, result))
        _LOGGING.info("%s entities reported to be toggled", len(result))
