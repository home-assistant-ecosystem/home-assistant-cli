"""Entity plugin for Home Assistant CLI (hass-cli)."""
import logging
import re
import sys
from typing import Any, Dict, List, Pattern  # noqa

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.const as const
import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('entity')
@pass_context
def cli(ctx):
    """Get info on entities from Home Assistant."""


@cli.command('list')
@click.argument('entityfilter', default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, entityfilter: str):
    """List all entities from Home Assistant."""
    ctx.auto_output("table")

    entities = api.get_entities(ctx)

    result = []  # type: List[Dict]
    if entityfilter == ".*":
        result = entities
    else:
        entityfilterre = re.compile(entityfilter)  # type: Pattern

        for entity in entities:
            if entityfilterre.search(entity['entity_id']):
                result.append(entity)

    cols = [
        ('ENTITY_ID', 'entity_id'),
        ('NAME', 'name'),
        ('DEVICE_ID', 'device_id'),
        ('PLATFORM', 'platform'),
        ('CONFIG_ENTRY_ID', 'config_entry_id'),
        ('DISABLED_BY', 'disabled_by'),
    ]

    ctx.echo(
        helper.format_output(
            ctx, result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('rename')
@click.argument(  # type: ignore
    'oldid', required=True, autocompletion=autocompletion.entities
)
@click.option('--name', required=False)
@click.argument(  # type: ignore
    'newid', required=False, autocompletion=autocompletion.entities
)
@pass_context
def rename(ctx, oldid, newid, name):
    """Rename a entity."""
    ctx.auto_output("data")

    if not newid and not name:
        _LOGGING.error("Need to at least specify either a new id or new name")
        sys.exit(1)

    entity = api.get_entity(ctx, oldid)
    if not entity:
        _LOGGING.error("Could not find entity with ID: %s", oldid)
        sys.exit(1)

    result = api.rename_entity(ctx, oldid, newid, name)

    ctx.echo(
        helper.format_output(
            ctx,
            [result],
            columns=ctx.columns if ctx.columns else const.COLUMNS_DEFAULT,
        )
    )
