"""Delete plugin for Home Assistant CLI (hass-cli)."""
import click
import homeassistant_cli.autocompletion as autocompletion
from homeassistant_cli.cli import pass_context


@click.group('delete')
@pass_context
def cli(ctx):
    """Delete entities."""

@cli.command()
@click.argument('entity', required='true',
                autocompletion=autocompletion.entities)
@pass_context
def state(ctx, entity):
    """Delete state from Home Assistant."""
    response = req_raw(ctx, 'delete', 'states/{}'.format(entity))
    click.echo(response)
