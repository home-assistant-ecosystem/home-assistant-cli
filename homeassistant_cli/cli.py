"""Configuration plugin for Home Assistant CLI (hass-cli)."""
import os
import sys

import click
import homeassistant.remote as remote

from homeassistant_cli.config import Configuration
from homeassistant_cli.const import PACKAGE_NAME, __version__

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
        except ImportError:
            return
        return mod.cli


@click.command(cls=HomeAssistantCli, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
@click.option('--host', '-h',
              help='The IP address of Home Assistant instance.')
@click.option('--port', '-o',
              help='The port the Home Assistant instance listens on.')
@click.option('--password', '-p', hide_input=True,
              help='The API password of Home Assistant instance.')
@click.option('--ssl', '-s', is_flag=True,
              help='Enables SSL connection.')
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')

@pass_context
def cli(ctx, verbose, host, password, ssl, port):
    """A command line interface for Home Assistant."""
    import requests

    ctx.verbose = verbose
    ctx.password = password
    ctx.ssl = ssl
    if host is not None:
        ctx.host = host
    if port is not None:
        ctx.port = port        
    ctx.api = remote.API(ctx.host, ctx.password, ctx.port, ctx.ssl)
    if str(remote.validate_api(ctx.api)) == 'invalid_password':
        ctx.log("Your API password for %s was not provided or is wrong. "
                "Use '--password/-p'", ctx.host)
        sys.exit(1)

if __name__  == '__main__':
    cli()
