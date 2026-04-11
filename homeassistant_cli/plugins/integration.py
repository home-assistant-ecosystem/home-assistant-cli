"""Integrations (config entries) plugin for Home Assistant CLI (hass-cli)."""

import logging
import re
import sys

import click

import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration

_LOGGING = logging.getLogger(__name__)


@click.group("integration")
@pass_context
def cli(ctx):
    """Get info and operate on integrations (config entries) from Home Assistant."""


@cli.command("list")
@click.argument("integration_filter", default=".*", required=False)
@pass_context
def list_integrations(ctx: Configuration, integration_filter: str):
    """List all integrations (config entries) from Home Assistant.

    INTEGRATION_FILTER - optional regex to filter by domain or title
    """
    ctx.auto_output("table")

    entries = api.get_config_entries(ctx)

    result = []
    if integration_filter == ".*":
        result = entries
    else:
        filter_regex = re.compile(integration_filter, re.IGNORECASE)

        for entry in entries:
            if filter_regex.search(entry.get("domain", "")) or filter_regex.search(
                entry.get("title", "")
            ):
                result.append(entry)

    cols = [
        ("ENTRY_ID", "entry_id"),
        ("DOMAIN", "domain"),
        ("TITLE", "title"),
        ("STATE", "state"),
        ("DISABLED_BY", "disabled_by"),
    ]

    ctx.echo(
        helper.format_output(ctx, result, columns=ctx.columns if ctx.columns else cols)
    )


@cli.command("info")
@click.argument("entry_id", required=True)
@pass_context
def info(ctx: Configuration, entry_id: str):
    """Show detailed information about an integration.

    ENTRY_ID - the entry_id of the config entry
    """
    ctx.auto_output("data")

    entries = api.get_config_entries(ctx)

    # Find by entry_id or partial match
    entry = None
    for e in entries:
        if e.get("entry_id") == entry_id or e.get("entry_id", "").startswith(entry_id):
            entry = e
            break

    if not entry:
        _LOGGING.error("Could not find integration with entry_id: %s", entry_id)
        sys.exit(1)

    ctx.echo(helper.format_output(ctx, entry))


@cli.command("reload")
@click.argument("entry_id", required=True)
@pass_context
def reload(ctx: Configuration, entry_id: str):
    """Reload an integration.

    ENTRY_ID - the entry_id of the config entry to reload
    """
    ctx.auto_output("data")

    # Find full entry_id if partial match
    entries = api.get_config_entries(ctx)
    full_entry_id = None
    for e in entries:
        if e.get("entry_id") == entry_id or e.get("entry_id", "").startswith(entry_id):
            full_entry_id = e.get("entry_id")
            break

    if not full_entry_id:
        _LOGGING.error("Could not find integration with entry_id: %s", entry_id)
        sys.exit(1)

    result = api.reload_config_entry(ctx, full_entry_id)

    if result.get("success"):
        ctx.echo(f"Successfully reloaded integration: {full_entry_id}")
    else:
        ctx.echo(helper.format_output(ctx, result))


@cli.command("delete")
@click.argument("entry_id", required=True)
@click.option(
    "--confirm",
    is_flag=True,
    default=False,
    help="Confirm deletion without prompting",
)
@pass_context
def delete(ctx: Configuration, entry_id: str, confirm: bool):
    """Delete an integration.

    ENTRY_ID - the entry_id of the config entry to delete
    """
    ctx.auto_output("data")

    # Find full entry_id if partial match
    entries = api.get_config_entries(ctx)
    entry = None
    for e in entries:
        if e.get("entry_id") == entry_id or e.get("entry_id", "").startswith(entry_id):
            entry = e
            break

    if not entry:
        _LOGGING.error("Could not find integration with entry_id: %s", entry_id)
        sys.exit(1)

    full_entry_id = entry.get("entry_id")
    domain = entry.get("domain", "unknown")
    title = entry.get("title", "unknown")

    if not confirm:
        click.confirm(
            f"Are you sure you want to delete '{domain}' ({title}) [{full_entry_id}]?",
            abort=True,
        )

    result = api.delete_config_entry(ctx, full_entry_id)

    if result.get("success"):
        ctx.echo(f"Successfully deleted integration: {domain} ({title})")
    else:
        ctx.echo(helper.format_output(ctx, result))


@cli.command("disable")
@click.argument("entry_id", required=True)
@pass_context
def disable(ctx: Configuration, entry_id: str):
    """Disable an integration.

    ENTRY_ID - the entry_id of the config entry to disable
    """
    ctx.auto_output("data")

    # Find full entry_id if partial match
    entries = api.get_config_entries(ctx)
    entry = None
    for e in entries:
        if e.get("entry_id") == entry_id or e.get("entry_id", "").startswith(entry_id):
            entry = e
            break

    if not entry:
        _LOGGING.error("Could not find integration with entry_id: %s", entry_id)
        sys.exit(1)

    full_entry_id = entry.get("entry_id")
    result = api.disable_config_entry(ctx, full_entry_id, "user")

    if result.get("success"):
        ctx.echo(f"Successfully disabled integration: {full_entry_id}")
    else:
        ctx.echo(helper.format_output(ctx, result))


@cli.command("enable")
@click.argument("entry_id", required=True)
@pass_context
def enable(ctx: Configuration, entry_id: str):
    """Enable a disabled integration.

    ENTRY_ID - the entry_id of the config entry to enable
    """
    ctx.auto_output("data")

    # Find full entry_id if partial match
    entries = api.get_config_entries(ctx)
    entry = None
    for e in entries:
        if e.get("entry_id") == entry_id or e.get("entry_id", "").startswith(entry_id):
            entry = e
            break

    if not entry:
        _LOGGING.error("Could not find integration with entry_id: %s", entry_id)
        sys.exit(1)

    full_entry_id = entry.get("entry_id")
    result = api.disable_config_entry(ctx, full_entry_id, None)

    if result.get("success"):
        ctx.echo(f"Successfully enabled integration: {full_entry_id}")
    else:
        ctx.echo(helper.format_output(ctx, result))


@cli.command("list-disabled")
@pass_context
def list_disabled(ctx: Configuration):
    """List all disabled integrations (config entries) from Home Assistant."""
    ctx.auto_output("table")

    entries = api.get_config_entries(ctx)

    result = [entry for entry in entries if entry.get("disabled_by")]

    cols = [
        ("ENTRY_ID", "entry_id"),
        ("DOMAIN", "domain"),
        ("TITLE", "title"),
        ("DISABLED_BY", "disabled_by"),
    ]

    ctx.echo(
        helper.format_output(ctx, result, columns=ctx.columns if ctx.columns else cols)
    )

@cli.command("list-loaded")
@pass_context
def list_loaded(ctx: Configuration):
    """List all loaded integrations (config entries) from Home Assistant."""
    ctx.auto_output("table")

    entries = api.get_config_entries(ctx)

    result = [entry for entry in entries if entry.get("state") == "loaded"]

    cols = [
        ("ENTRY_ID", "entry_id"),
        ("DOMAIN", "domain"),
        ("TITLE", "title"),
        ("STATE", "state"),
    ]

    ctx.echo(
        helper.format_output(ctx, result, columns=ctx.columns if ctx.columns else cols)
    )


@cli.command("list-unloaded")
@pass_context
def list_unloaded(ctx: Configuration):
    """List all unloaded integrations (config entries) from Home Assistant."""
    ctx.auto_output("table")

    entries = api.get_config_entries(ctx)

    result = [entry for entry in entries if entry.get("state") != "loaded"]

    cols = [
        ("ENTRY_ID", "entry_id"),
        ("DOMAIN", "domain"),
        ("TITLE", "title"),
        ("STATE", "state"),
    ]

    ctx.echo(
        helper.format_output(ctx, result, columns=ctx.columns if ctx.columns else cols)
    )
