"""Location plugin for Home Assistant CLI (hass-cli)."""

import json as json_
import logging
import re
from typing import Any, Dict, List, Pattern  # noqa

import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.const as const
import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api
import yaml

_LOGGING = logging.getLogger(__name__)


@click.group('entity')
@pass_context
def cli(ctx):
    """Get info and operate on entities from Home Assistant."""


@cli.command()
@click.argument(  # type: ignore
    'entity', required=True, autocompletion=autocompletion.entities
)
@pass_context
def get(ctx: Configuration, entity):
    """Get/read entity state from Home Assistant."""
    state = api.get_state(ctx, entity)

    if state:
        ctx.echo(helper.format_output(ctx, state, const.COLUMNS_ENTITIES))
    else:
        _LOGGING.error("Entity with id: '%s' not found.", entity)


@cli.command()
@click.argument(  # type: ignore
    'entity', required=True, autocompletion=autocompletion.entities
)
@pass_context
def delete(ctx: Configuration, entity):
    """Delete entity from Home Assistant."""
    deleted = api.remove_state(ctx, entity)

    if deleted:
        ctx.echo("Entity %s deleted.", entity)
    else:
        ctx.echo("Entity %s not found.", entity)


@cli.command('list')
@click.argument('entityfilter', default=".*", required=False)
@pass_context
def listcmd(ctx, entityfilter):
    """List all state from Home Assistant."""
    states = api.get_states(ctx)

    result = []  # type: List[Dict]
    if entityfilter == ".*":
        result = states
    else:
        entityfilterre = re.compile(entityfilter)  # type: Pattern

        for entity in states:
            if entityfilterre.search(entity['entity_id']):
                result.append(entity)

    ctx.echo(helper.format_output(ctx, result, columns=const.COLUMNS_ENTITIES))


@cli.command()
@click.argument(  # type: ignore
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
def edit(ctx: Configuration, entity, newstate, attributes, merge, json):
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
            ctx.echo("Existing state found for %s", entity)
            if merge:
                wanted_state = existing_state
        else:
            ctx.echo("No existing state found for '%s'", entity)

        if attributes:
            attributes_dict = helper.to_attributes(attributes)

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
        if existing:
            existingraw = helper.raw_format_output(ctx.output, existing)
        else:
            existingraw = helper.raw_format_output(ctx.output, {})

        new = click.edit(existingraw, extension='.{}'.format(ctx.output))

        if new is not None:
            ctx.echo("Updating '%s'", entity)
            if ctx.output == 'yaml':
                wanted_state = yaml.load(new)
            if ctx.output == 'json':
                wanted_state = json_.loads(new)

            api.set_state(ctx, entity, wanted_state)
        else:
            ctx.echo("No edits/changes returned from editor.")
            return

    _LOGGING.debug("wanted: %s", str(wanted_state))
    result = api.set_state(ctx, entity, wanted_state)
    ctx.echo("Entity %s updated succesfully", entity)
    _LOGGING.debug("Updated to: %s", result)


def _report(ctx: Configuration, result: Dict[str, Any], action: str):
    ctx.echo(helper.format_output(ctx, result, columns=const.COLUMNS_ENTITIES))
    if ctx.verbose:
        ctx.echo("%s entities reported to be %s", len(result), action)


@cli.command()
@click.argument(  # type: ignore
    'entities', nargs=-1, required=True, autocompletion=autocompletion.entities
)
@pass_context
def toggle(ctx: Configuration, entities):
    """Toggle state for one or more entities in Home Assistant."""
    for entity in entities:
        data = {'entity_id': entity}
        _LOGGING.debug("Toggling %s", entity)
        result = api.call_service(ctx, 'homeassistant', 'toggle', data)

        _report(ctx, result, "toggled")


@cli.command('turn_off')
@click.argument(  # type: ignore
    'entities', nargs=-1, required=True, autocompletion=autocompletion.entities
)
@pass_context
def off_cmd(ctx: Configuration, entities):
    """Turn entity off."""
    for entity in entities:
        data = {'entity_id': entity}
        _LOGGING.debug("Toggling %s", entity)
        result = api.call_service(ctx, 'homeassistant', 'turn_off', data)

        _report(ctx, result, "turned off")


@cli.command('turn_on')
@click.argument(  # type: ignore
    'entities', nargs=-1, required=True, autocompletion=autocompletion.entities
)
@pass_context
def on_cmd(ctx: Configuration, entities):
    """Turn entity on."""
    for entity in entities:
        data = {'entity_id': entity}
        _LOGGING.debug("Toggling %s", entity)
        result = api.call_service(ctx, 'homeassistant', 'turn_on', data)

        _report(ctx, result, "turned on")


@cli.command()
@click.argument(  # type: ignore
    'entity', required=False, autocompletion=autocompletion.entities
)
@pass_context
def history(ctx: Configuration, entity: str):
    """List history from Home Assistant."""
    click.echo(
        helper.format_output(
            ctx,
            api.get_history(ctx, entity)[0],
            columns=const.COLUMNS_ENTITIES,
        )
    )
