"""Configuration for Home Assistant CLI (hass-cli)."""
import sys

import click
from homeassistant_cli.const import DEFAULT_OUTPUT, DEFAULT_SERVER


class Configuration:
    """The configuration context for the Home Assistant CLI."""

    def __init__(self) -> None:
        """Initialize the configuration."""
        self.verbose = False
        self.server = DEFAULT_SERVER
        self.output = DEFAULT_OUTPUT
        self.token = None
        self.insecure = False

    def log(self, msg, *args):  # pylint: disable=no-self-use
        """Log a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Log a message only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def __repr__(self) -> str:
        """Return the representation of the Configuration."""
        view = {
            "server": self.server,
            "access-token": 'yes' if self.token is not None else 'no',
            "insecure": self.insecure,
            "output": self.output,
            "verbose": self.verbose,
        }

        return "<Configuration({})".format(view)
