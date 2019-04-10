"""Auto-completion for Home Assistant CLI (hass-cli)."""

import click
from click._bashcomplete import get_completion_script

from homeassistant_cli.cli import pass_context


@click.group('completion')
@pass_context
def cli(ctx):
    """Output shell completion code for the specified shell (bash or zsh)."""


def dump_script(shell: str) -> None:
    """Dump the script content."""
    # todo resolve actual script name in case user aliased it
    prog_name = "hass-cli"
    cvar = '_%s_COMPLETE' % (prog_name.replace('-', '_')).upper()

    click.echo(get_completion_script(prog_name, cvar, shell))


@cli.command()
@pass_context
def bash(ctx):
    """Output shell completion code for bash."""
    dump_script("bash")


@cli.command()
@pass_context
def zsh(ctx):
    """Output shell completion code for zsh."""
    dump_script("zsh")
