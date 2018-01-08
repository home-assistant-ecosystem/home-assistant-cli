"""State plugin for Home Assistant CLI (hass-cli)."""
import json

import click

from homeassistant_cli.cli import pass_context
from homeassistant_cli.helper import timestamp


@click.command('list')
@click.option('--action', '-a',
              type=click.Choice(['set', 'get', 'remove']),
              help='The action to perform.')
@click.option('--entity', '-e',
              type=click.STRING, help='The entity to work with.')
@click.option('--new_state', '-s', help='The new state of the entity.')
@click.option('--attributes', type=click.STRING,
              help='The attributes of the entity.')
@pass_context
def cli(ctx, entity, action, new_state, attributes):
    """Get, set or remove the state of entity."""
    import homeassistant.remote as remote

    if action == 'get':
        state = remote.get_state(ctx.api, entity)
        ctx.log('State of %s is %s', entity, state.state)

    if action == 'set':
        remote.set_state(ctx.api, entity, new_state,
                         attributes=json.loads(attributes))
        ctx.log('State of %s set to %s', entity, new_state)

    if action == 'remove':
        remote.remove_state(ctx.api, entity)
        ctx.log('Entitiy %s removed', entity)

    ctx.vlog('Entity: %s, Execute: %s', entity, timestamp())
