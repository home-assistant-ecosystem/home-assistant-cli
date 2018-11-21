import os
import homeassistant_cli.const as const
from requests.exceptions import HTTPError
from homeassistant_cli.helper import req, req_raw, format_output,debug_requests_on

def _init_ctx(ctx):
    ## ctx is incomplete thus need to 'hack' arond it
    ## see bug https://github.com/pallets/click/issues/942
    if not hasattr(ctx, 'server'):
        ctx.server = os.environ.get('HASS_SERVER', const.DEFAULT_SERVER)
    
    if not hasattr(ctx, 'token'):
        ctx.token = os.environ.get('HASS_TOKEN')

    if not hasattr(ctx, "timeout"):
        ctx.timeout = os.environ.get('HASS_TIMEOUT', const.DEFAULT_TIMEOUT)

def entities(ctx, args, incomplete):
    _init_ctx(ctx)    
    try:
        x = req(ctx, "get", "states")
    except HTTPError:
        x = None

    entities = []

    if x is not None:
        for entity in x:
            entities.append((entity["entity_id"], ''))

        entities.sort()

        return [c for c in entities if incomplete in c[0]]
    else:
        return entities


def events(ctx, args, incomplete):
    _init_ctx(ctx)    
    try:
        x = req(ctx, "get", "events")
    except HTTPError:
        x = None

    entities = []

    if x is not None:
        for entity in x:
            entities.append((entity["event"], ''))

        entities.sort()

        return [c for c in entities if incomplete in c[0]]
    else:
        return entities