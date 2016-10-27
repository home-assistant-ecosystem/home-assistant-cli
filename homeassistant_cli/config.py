"""Configuration for Home Assistant CLI (hass-cli)."""
import sys
import click
from homeassistant_cli.const import DEFAULT_HOST, DEFAULT_PORT

class Configuration(object):
    """The configuration context for the Home Assistant CLI."""

    def __init__(self):
        """Initialize the configuration."""
        self.verbose = False
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.password = None
        self.ssl = None

    def log(self, msg, *args):
        """Log a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Log a message only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def table(self, elements):
        """Create a table-like output."""
        from tabulate import tabulate
        click.echo(tabulate(elements))
