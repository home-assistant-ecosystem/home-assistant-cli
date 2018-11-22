"""Details for the auto-completion."""
import os

from homeassistant_cli.helper import (
    debug_requests_on, format_output, req, req_raw)
from requests.exceptions import HTTPError


def _init_ctx(ctx):
    """Initialize ctx."""
    # ctx is incomplete thus need to 'hack' around it
    # see bug https://github.com/pallets/click/issues/942
    if not hasattr(ctx, 'server'):
        ctx.server = os.environ.get('HASS_SERVER', const.DEFAULT_SERVER)

    if not hasattr(ctx, 'token'):
        ctx.token = os.environ.get('HASS_TOKEN')

    if not hasattr(ctx, "timeout"):
        ctx.timeout = os.environ.get('HASS_TIMEOUT', const.DEFAULT_TIMEOUT)


def entities(ctx, args, incomplete):
    """Entities."""
    _init_ctx(ctx)
    try:
        response = req(ctx, "get", "states")
    except HTTPError:
        response = None

    entities = []

    if response is not None:
        for entity in response:
            entities.append((entity["entity_id"], ''))

        entities.sort()

        return [c for c in entities if incomplete in c[0]]
    else:
        return entities


def events(ctx, args, incomplete):
    """Events."""
    _init_ctx(ctx)
    try:
        response = req(ctx, "get", "events")
    except HTTPError:
        response = None

    entities = []

    if x is not None:
        for entity in response:
            entities.append((entity["event"], ''))

        entities.sort()

        return [c for c in entities if incomplete in c[0]]
    else:
        return entities
