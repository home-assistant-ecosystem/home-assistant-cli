"""Dashboard plugin for Home Assistant CLI (hass-cli)."""

import logging
import sys

import click
from ruamel.yaml import YAML

import homeassistant_cli.helper as helper
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration

_LOGGING = logging.getLogger(__name__)

COLUMNS = [
    ("URL PATH", "url_path"),
    ("TITLE", "title"),
    ("MODE", "mode"),
    ("SIDEBAR", "show_in_sidebar"),
    ("ICON", "icon"),
]


@click.group("dashboard")
@pass_context
def cli(ctx: Configuration) -> None:
    """Get info and manage dashboards from Home Assistant."""


@cli.command("list")
@pass_context
def listcmd(ctx: Configuration) -> None:
    """List all dashboards."""
    ctx.auto_output("table")
    dashboards = api.get_dashboards(ctx)
    ctx.echo(
        helper.format_output(
            ctx, dashboards, columns=ctx.columns if ctx.columns else COLUMNS
        )
    )


@cli.command("get")
@click.argument("url_path", default="", required=False)
@pass_context
def get(ctx: Configuration, url_path: str) -> None:
    """Get a dashboard config.

    URL_PATH - optional url_path of a named dashboard (omit for default)
    """
    ctx.auto_output("json")
    config = api.get_dashboard_config(ctx, url_path)
    ctx.echo(helper.format_output(ctx, config))


@cli.command("set")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument("url_path", default="", required=False)
@pass_context
def set_cmd(ctx: Configuration, filename: str, url_path: str) -> None:
    """Set a dashboard config from a YAML or JSON file.

    FILENAME - path to the config file
    URL_PATH - optional url_path of a named dashboard (omit for default)
    """
    yaml = YAML()
    try:
        with open(filename) as f:
            config = yaml.load(f)
    except Exception as err:
        _LOGGING.error("Failed to read %s: %s", filename, err)
        sys.exit(1)

    api.save_dashboard_config(ctx, dict(config), url_path)
    _LOGGING.info("Dashboard uploaded successfully")
