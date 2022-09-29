"""Device (registry) plugin for Home Assistant CLI (hass-cli)."""
import logging
import re
import sys
from typing import Any, Dict, List, Optional, Pattern  # noqa

import click

import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration
import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api

_LOGGING = logging.getLogger(__name__)


@click.group('device')
@pass_context
def cli(ctx):
    """Get info and operate on devices from Home Assistant (EXPERIMENTAL)."""


@cli.command('list')
@click.argument('devicefilter', default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, devicefilter: str):
    """List all devices from Home Assistant."""
    ctx.auto_output("table")

    areas = api.get_areas(ctx)

    devices = api.get_devices(ctx)

    result = []  # type: List[Dict]
    if devicefilter == ".*":
        result = devices
    else:
        devicefilterre = re.compile(devicefilter)  # type: Pattern

        for device in devices:
            if devicefilterre.search(device['name']):
                result.append(device)

    for device in devices:
        area = next(
            (a for a in areas if a['area_id'] == device['area_id']), None
        )
        if area:
            device['area_name'] = area['name']

    cols = [
        ('ID', 'id'),
        ('NAME', 'name'),
        ('MODEL', 'model'),
        ('MANUFACTURER', 'manufacturer'),
        ('AREA', 'area_name'),
    ]

    ctx.echo(
        helper.format_output(
            ctx, result, columns=ctx.columns if ctx.columns else cols
        )
    )


@cli.command('assign')
@click.argument(
    'area_id_or_name',
    required=True,
    shell_complete=autocompletion.areas,  # type: ignore
)
@click.argument('names', nargs=-1, required=False)
@click.option(
    '--match', help="Expression used to find devices matching that name"
)
@pass_context
def assign(
    ctx: Configuration,
    area_id_or_name,
    names: List[str],
    match: Optional[str] = None,
):
    """Update area on one or more devices.

    NAMES - one or more name or id (Optional)
    """
    ctx.auto_output("data")

    devices = api.get_devices(ctx)

    result = []  # type: List[Dict]

    area = api.find_area(ctx, area_id_or_name)
    if not area:
        _LOGGING.error(
            "Could not find area with id or name: %s", area_id_or_name
        )
        sys.exit(1)

    if match:
        if match == ".*":
            result = devices
        else:
            devicefilterre = re.compile(match)  # type: Pattern

            for device in devices:
                if devicefilterre.search(device['name']):
                    result.append(device)

    for id_or_name in names:
        device = next(
            (x for x in devices if x['id'] == id_or_name), None  # type: ignore
        )
        if not device:
            device = next(
                (x for x in devices if x['name'] == id_or_name),
                None,  # type: ignore
            )
        if not device:
            _LOGGING.error(
                "Could not find device with id or name: %s", id_or_name
            )
            sys.exit(1)
        result.append(device)

    for device in result:
        output = api.assign_area(ctx, device['id'], area['area_id'])
        if output['success']:
            ctx.echo(
                "Successfully assigned '{}' to '{}'".format(
                    area['name'], device['name']
                )
            )
        else:
            _LOGGING.error(
                "Failed to assign '%s' to '%s'", area['name'], device['name']
            )

            ctx.echo(str(output))


@cli.command('rename')
@click.argument('device_id_or_name', required=True)
@click.argument('new_name', required=True)
@pass_context
def rename(
    ctx: Configuration,
    device_id_or_name,
    new_name,
):
    """Update name of specified device."""
    ctx.auto_output("data")

    devices = api.get_devices(ctx)

    device = next(
        (x for x in devices if x['id'] == device_id_or_name),
        None,  # type: ignore
    )
    if not device:
        device = next(
            (x for x in devices if x['name'] == device_id_or_name),
            None,  # type: ignore
        )
    if not device:
        _LOGGING.error(
            "Could not find device with id or name: %s", device_id_or_name
        )
        sys.exit(1)

    output = api.rename_device(ctx, device['id'], new_name)
    if output['success']:
        ctx.echo(
            "Successfully renamed '{}' from {} to '{}'".format(
                device_id_or_name, device['name_by_user'], new_name
            )
        )
    else:
        _LOGGING.error(
            "Failed to rename '%s' to '%s'", device_id_or_name, new_name
        )

        ctx.echo(str(output))
