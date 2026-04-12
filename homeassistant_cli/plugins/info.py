"""Information plugin for Home Assistant CLI (hass-cli)."""

import logging
from typing import Any, Dict, List

import click

import homeassistant_cli.autocompletion as autocompletion
import homeassistant_cli.remote as api
from homeassistant_cli.cli import pass_context
from homeassistant_cli.config import Configuration, set_supervisor_server
from homeassistant_cli.const import __version__ as cli_version
from homeassistant_cli.helper import format_output, to_attributes

_LOGGING = logging.getLogger(__name__)


def redacted_output(token: str) -> str:
    """Redact the token for display."""
    return (
        token[:4] + "*" * (len(token) // 8 - 8) + token[-4:]
        if token and len(token) > 8
        else "***"
    )


@click.group("info")
@pass_context
def cli(ctx):
    """Display information about Home Assistant CLI."""


@cli.command()
@pass_context
def cli(ctx):
    """Show information about Home Assistant CLI."""
    information = {
        "Server URL": ctx.resolved_server if ctx.resolved_server else ctx.server,
        "Password": True if ctx.password else False,
        "Token": redacted_output(ctx.token),
        "Supervisor URL": set_supervisor_server(ctx),
        "Supervisor Token": redacted_output(ctx.supervisor_token),
        "Verbose": ctx.verbose,
        "Debug": ctx.debug,
        "Insecure": ctx.insecure,
        "Show Exceptions": ctx.showexceptions,
        "Timeout": ctx.timeout,
        "CLI version": cli_version,
    }

    click.echo(format_output(ctx, information))
