"""Entity plugin for Home Assistant CLI (hass-cli)."""

import logging
import re
import sys

import click

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.const as const
import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration

_LOGGING = logging.getLogger(__name__)


@click.group("entity")
@pass_context
def cli(ctx):
    """Get info on entities from Home Assistant."""


@cli.command("list")
@click.argument("entity_filter", default=".*", required=False)
@pass_context
def listcmd(ctx: Configuration, entity_filter: str):
    """List all entities from Home Assistant."""
    ctx.auto_output("table")

    areas = api.get_areas(ctx)

    entities = api.get_entities(ctx)

    result = []  # type: List[Dict]
    if entity_filter == ".*":
        result = entities
    else:
        entity_filter_regex = re.compile(entity_filter)  # type: Pattern

        for entity in entities:
            if entity_filter_regex.search(entity["entity_id"]):
                result.append(entity)

    for entity in entities:
        area = next((a for a in areas if a["area_id"] == entity["area_id"]), None)
        if area:
            entity["area_name"] = area["name"]

    cols = [
        ("ENTITY_ID", "entity_id"),
        ("NAME", "name"),
        ("DEVICE_ID", "device_id"),
        ("PLATFORM", "platform"),
        ("AREA", "area_name"),
        ("CONFIG_ENTRY_ID", "config_entry_id"),
        ("DISABLED_BY", "disabled_by"),
    ]

    ctx.echo(
        helper.format_output(ctx, result, columns=ctx.columns if ctx.columns else cols)
    )


@cli.command("assign")
@click.argument(
    "area_id_or_name",
    required=True,
    shell_complete=autocompletion.areas,  # type: ignore
)
@click.argument("names", nargs=-1, required=False)
@click.option("--match", help="Expression used to find entities matching that name")
@pass_context
def assign(
    ctx: Configuration,
    area_id_or_name,
    names: list[str],
    match: str | None = None,
):
    """Update area on one or more entities.

    NAMES - one or more name or id (Optional)
    """
    ctx.auto_output("data")

    entities = api.get_entities(ctx)

    result = []  # type: List[Dict]

    area = api.find_area(ctx, area_id_or_name)
    if not area:
        _LOGGING.error("Could not find area with id or name: %s", area_id_or_name)
        sys.exit(1)

    if match:
        if match == ".*":
            result = entities
        else:
            entity_filter_regex = re.compile(match)  # type: Pattern

            for entity in entities:
                if entity_filter_regex.search(entity["name"]):
                    result.append(entity)

    for id_or_name in names:
        entity = next(
            (x for x in entities if x["entity_id"] == id_or_name),
            None,  # type: ignore
        )
        if not entity:
            entity = next(
                (x for x in entities if x["name"] == id_or_name),
                None,  # type: ignore
            )
        if not entity:
            _LOGGING.error("Could not find entity with id or name: %s", id_or_name)
            sys.exit(1)
        result.append(entity)

    for entity in result:
        output = api.assign_entity_area(ctx, entity["entity_id"], area["area_id"])
        if output["success"]:
            ctx.echo(
                "Successfully assigned '{}' to '{}'".format(
                    area["name"], entity["entity_id"]
                )
            )
        else:
            _LOGGING.error(
                "Failed to assign '%s' to '%s'",
                area["name"],
                entity["entity_id"],
            )

            ctx.echo(str(output))


@cli.command("rename")
@click.argument(
    "old_id",
    required=True,
    shell_complete=autocompletion.entities,  # type: ignore
)
@click.option("--name", required=False)
@click.argument(
    "new_id",
    required=False,
    shell_complete=autocompletion.entities,  # type: ignore
)
@pass_context
def rename(ctx, old_id, new_id, name):
    """Rename a entity."""
    ctx.auto_output("data")

    if not new_id and not name:
        _LOGGING.error("Need to at least specify either a new id or new name")
        sys.exit(1)

    entity = api.get_entity(ctx, old_id)
    if not entity:
        _LOGGING.error("Could not find entity with ID: %s", old_id)
        sys.exit(1)

    result = api.rename_entity(ctx, old_id, new_id, name)

    ctx.echo(
        helper.format_output(
            ctx,
            [result],
            columns=ctx.columns if ctx.columns else const.COLUMNS_DEFAULT,
        )
    )


@cli.command("delete")
@click.argument(
    "entity_id",
    required=True,
    shell_complete=autocompletion.entities,  # type: ignore
)
@click.option(
    "--confirm",
    is_flag=True,
    default=False,
    help="Confirm deletion without prompting",
)
@pass_context
def delete(ctx: Configuration, entity_id: str, confirm: bool) -> None:
    """Delete an entity.

    ENTITY_ID - the entity_id of the entity to delete
    """
    ctx.auto_output("data")

    entity = api.get_entity(ctx, entity_id)
    if not entity:
        _LOGGING.error("Could not find entity with ID: %s", entity_id)
        sys.exit(1)

    if not confirm:
        click.confirm(
            f"Are you sure you want to delete '{entity_id}'?",
            abort=True,
        )

    result = api.delete_entity(ctx, entity_id)

    if result.get("success"):
        ctx.echo(f"Successfully deleted entity '{entity_id}'")
    else:
        _LOGGING.error("Failed to delete entity: %s", entity_id)
        ctx.echo(str(result))
