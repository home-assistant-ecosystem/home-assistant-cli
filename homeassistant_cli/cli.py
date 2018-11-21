"""Configuration plugin for Home Assistant CLI (hass-cli)."""
import os
import sys

import click

from homeassistant_cli.const import DEFAULT_SERVER, DEFAULT_TIMEOUT, PACKAGE_NAME, __version__
from homeassistant_cli.config import Configuration
from homeassistant_cli.helper import debug_requests_on

CONTEXT_SETTINGS = dict(auto_envvar_prefix='HOMEASSISTANT')

pass_context = click.make_pass_decorator(Configuration, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'plugins'))


class HomeAssistantCli(click.MultiCommand):
    """The Home Assistant Command-line."""

    def list_commands(self, ctx):
        """List all command available as plugin."""
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                rv.append(filename[:-3])
        rv.sort()
        
        return rv

    def get_command(self, ctx, name):
        """Import the commands of the plugins."""
        try:
            mod = __import__('{}.plugins.{}'.format(PACKAGE_NAME, name),
                             None, None, ['cli'])
        except ImportError as ie:
            ## todo: print out issue of loading plugins ?
            return
        return mod.cli


@click.command(cls=HomeAssistantCli, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option('--server', '-s',
              help='The server URL of Home Assistant instance.', default=DEFAULT_SERVER, show_default=True, envvar="HASS_SERVER")
@click.option('--token', 
              help='The Bearer token for Home Assistant instance.', envvar="HASS_TOKEN")
@click.option('--timeout',
              help='Timeout for network operations.', default=DEFAULT_TIMEOUT)
@click.option('--output', '-o',
              help="Output format", type=click.Choice(['json', 'yaml']), default="json", show_default=True )
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--debug', is_flag=True, default=False,
              help='Enables debug mode.')
@pass_context
def cli(ctx, verbose, server, token, output, timeout, debug):
    """A command line interface for Home Assistant."""
    
    ctx.verbose = verbose
    ctx.server = server
    ctx.token = token
    ctx.timeout = timeout
    ctx.output = output 
    ctx.debug = debug

    if debug:
        debug_requests_on()

