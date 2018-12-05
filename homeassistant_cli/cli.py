"""Configuration plugin for Home Assistant CLI (hass-cli)."""
import os
import sys
import logging

import click
import click_log
from homeassistant_cli.config import Configuration
from homeassistant_cli.const import (
    DEFAULT_SERVER, DEFAULT_HASSIO_SERVER,
    DEFAULT_TIMEOUT, PACKAGE_NAME, __version__)
from homeassistant_cli.helper import debug_requests_on


click_log.basic_config()

_LOGGER = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(auto_envvar_prefix='HOMEASSISTANT')

pass_context = click.make_pass_decorator(Configuration, ensure=True)
cmd_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'plugins'))


def run():
    """Custom run entry point.

    Wraps click for full control
    over exception handling in Click.
    """
    # a hack to see if exception details should be printed.
    exceptionflags = ['-v', '--verbose']
    verbose = [c for c in exceptionflags if c in sys.argv]

    try:
        # could use cli.invoke here to use the just created context
        # but then shell completion will not work. Thus calling
        # standalone mode to keep that working.
        result = cli.main(standalone_mode=False)
        if isinstance(result, int):
            sys.exit(result)

    # exception handling below is done to use logger
    # and mimick as close as possible what click would
    # do normally in its main()
    except click.ClickException as ex:
        ex.show()  # let Click handle its own errors
        sys.exit(ex.exit_code)
    except click.Abort:
        _LOGGER.fatal("Aborted!")
        sys.exit(1)
    except Exception as ex: # noqa: WO703
        if verbose:
            _LOGGER.exception(ex)
        else:
            _LOGGER.error("%s: %s", type(ex).__name__, ex)
            _LOGGER.info("Run with %s to see full exception info.",
                         " or ".join(exceptionflags))
        sys.exit(1)


class HomeAssistantCli(click.MultiCommand):
    """The Home Assistant Command-line."""

    def list_commands(self, ctx):
        """List all command available as plugin."""
        commands = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                commands.append(filename[:-3])
        commands.sort()

        return commands

    def get_command(self, ctx, cmd_name):
        """Import the commands of the plugins."""
        try:
            mod = __import__('{}.plugins.{}'.format(PACKAGE_NAME, cmd_name),
                             None, None, ['cli'])
        except ImportError:
            # todo: print out issue of loading plugins?
            return
        return mod.cli


def _default_server():
    if ("HASSIO_TOKEN" in os.environ and
            "HASS_TOKEN" not in os.environ):
                return DEFAULT_HASSIO_SERVER
    else:
        return DEFAULT_SERVER


def _default_token():
    return os.environ.get('HASS_TOKEN',
                          os.environ.get(
                              'HASSIO_TOKEN',
                              None
                          ))


@click.command(cls=HomeAssistantCli, context_settings=CONTEXT_SETTINGS)
@click_log.simple_verbosity_option(logging.getLogger(), "--loglevel", "-l")
@click.version_option(__version__)
@click.option('--server', '-s',
              help='The server URL of Home Assistant instance.',
              default=lambda: _default_server(), envvar='HASS_SERVER')
@click.option('--token',
              default=lambda: _default_token(),
              help='The Bearer token for Home Assistant instance.',
              envvar='HASS_TOKEN')
@click.option('--timeout',
              help='Timeout for network operations.', default=DEFAULT_TIMEOUT,
              show_default=True)
@click.option('--output', '-o',
              help="Output format", type=click.Choice(['json', 'yaml']),
              default='json', show_default=True)
@click.option('-v', '--verbose', is_flag=True,
              help='Enables verbose mode.')
@click.option('--insecure', is_flag=True, default=False,
              help=('Ignore SSL Certificates.'
                    ' Allow to connect to servers with'
                    ' self-signed certificates.'
                    ' Be careful!'))
@click.option('--debug', is_flag=True, default=False,
              help='Enables debug mode.')
@click.version_option()
@pass_context
def cli(ctx, verbose, server, token, output, timeout, debug, insecure):
    """Command line interface for Home Assistant."""
    ctx.verbose = verbose
    ctx.server = server
    ctx.token = token
    ctx.timeout = timeout
    ctx.output = output
    ctx.debug = debug
    ctx.insecure = insecure

    _LOGGER.debug("Using settings: %s", ctx)

    if debug:
        debug_requests_on()
