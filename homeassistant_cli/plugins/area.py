"""Area (registry) plugin for Home Assistant CLI (hass-cli)."""
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


@click.group('area')
@pass_context
def cli(ctx):
    """Get info and operate on areas from Home Assistant (EXPERIMENTAL)."""


@cli.command('list')
@click.argument('areafilter', default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, areafilter: str):
    """List all areas from Home Assistant."""
    ctx.auto_output("table")

    areas = api.get_areas(ctx)

    result = []  # type: List[Dict]
    if areafilter == ".*":
        result = areas
    else:
        areafilterre = re.compile(areafilter)  # type: Pattern

        for device in areas:
            if areafilterre.search(device['name']):
                result.append(device)

    cols = [('ID', 'area_id'), ('NAME', 'name')]

    ctx.echo(
        helper.format_output(
            ctx, result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('create')
@click.argument('names', nargs=-1, required=True)
@pass_context
def create(ctx, names):
    """Create an area.

    NAMES - one or more area names to create
    """
    ctx.auto_output("data")

    for name in names:
        result = api.create_area(ctx, name)

        ctx.echo(
            helper.format_output(
                ctx,
                [result],
                columns=ctx.columns if ctx.columns else const.COLUMNS_DEFAULT,
            )
        )


@cli.command('delete')
@click.argument(  # type: ignore
    'names', nargs=-1, required=True, autocompletion=autocompletion.areas
)
@pass_context
def delete(ctx, names):
    """Delete an area.

    NAMES - one or more area names or id to delete
    """
    ctx.auto_output("data")
    excode = 0

    for name in names:
        area = api.find_area(ctx, name)
        if not area:
            _LOGGING.error("Could not find area with id or name: %s", name)
            excode = 1
        else:
            result = api.delete_area(ctx, area['area_id'])

            ctx.echo(
                helper.format_output(
                    ctx,
                    [result],
                    columns=ctx.columns
                    if ctx.columns
                    else const.COLUMNS_DEFAULT,
                )
            )

    if excode != 0:
        sys.exit(excode)


@cli.command('rename')
@click.argument(  # type: ignore
    'oldname', required=True, autocompletion=autocompletion.areas
)
@click.argument('newname', required=True)
@pass_context
def rename(ctx, oldname, newname):
    """Rename an area."""
    ctx.auto_output("data")

    area = api.find_area(ctx, oldname)
    if not area:
        _LOGGING.error("Could not find area with id or name: %s", oldname)
        sys.exit(1)

    result = api.rename_area(ctx, area['area_id'], newname)

    ctx.echo(
        helper.format_output(
            ctx,
            [result],
            columns=ctx.columns if ctx.columns else const.COLUMNS_DEFAULT,
        )
    )
