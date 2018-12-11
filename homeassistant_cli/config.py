"""Configuration for Home Assistant CLI (hass-cli)."""
import sys
from typing import Any, Optional

import click
import homeassistant_cli.const as const


class Configuration:
    """The configuration context for the Home Assistant CLI."""

    def __init__(self) -> None:
        """Initialize the configuration."""
        self.verbose = False  # type: bool
        self.server = const.DEFAULT_SERVER  # type: str
        self.output = const.DEFAULT_OUTPUT  # type: str
        self.token = None  # type: Optional[str]
        self.insecure = False  # type: bool
        self.timeout = const.DEFAULT_TIMEOUT  # type: int
        self.debug = False  # type: bool
        self.showexceptions = False  # type: bool

    def echo(self, msg: str, *args: Optional[Any]) -> None:
        """Put content message to stdout."""
        self.log(msg, *args)

    def log(  # pylint: disable=no-self-use
        self, msg: str, *args: Optional[str]
    ) -> None:  # pylint: disable=no-self-use
        """Log a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg: str, *args: Optional[str]) -> None:
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
