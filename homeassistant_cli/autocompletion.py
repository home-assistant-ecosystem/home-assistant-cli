"""Details for the auto-completion."""
import os
from typing import Any, Dict, List, Tuple  # NOQA

from homeassistant_cli import const
from homeassistant_cli.config import Configuration, resolve_server
import homeassistant_cli.remote as api
from requests.exceptions import HTTPError


def _init_ctx(ctx: Configuration) -> None:
    """Initialize ctx."""
    # ctx is incomplete thus need to 'hack' around it
    # see bug https://github.com/pallets/click/issues/942
    if not hasattr(ctx, 'server'):
        ctx.server = os.environ.get('HASS_SERVER', const.AUTO_SERVER)

    if not hasattr(ctx, 'token'):
        ctx.token = os.environ.get('HASS_TOKEN', None)

    if not hasattr(ctx, 'password'):
        ctx.password = os.environ.get('HASS_PASSWORD', None)

    if not hasattr(ctx, 'timeout'):
        ctx.timeout = int(
            os.environ.get('HASS_TIMEOUT', str(const.DEFAULT_TIMEOUT))
        )

    if not hasattr(ctx, 'insecure'):
        ctx.insecure = False

    if not hasattr(ctx, 'session'):
        ctx.session = None

    if not hasattr(ctx, 'cert'):
        ctx.cert = None

    if not hasattr(ctx, 'resolved_server'):
        ctx.resolved_server = resolve_server(ctx)


def services(
    ctx: Configuration, args: str, incomplete: str
) -> List[Tuple[str, str]]:
    """Services."""
    _init_ctx(ctx)
    try:
        response = api.get_services(ctx)
    except HTTPError:
        response = {}

    completions = []  # type: List[Tuple[str, str]]
    if response:
        for domain in response:
            domain_name = domain['domain']  # type: ignore
            servicesdict = domain['services']  # type: ignore

            for service in servicesdict:
                completions.append(
                    (
                        "{}.{}".format(domain_name, service),
                        servicesdict[service]['description'],  # type: ignore
                    )
                )

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions


def entities(
    ctx: Configuration, args: str, incomplete: str
) -> List[Tuple[str, str]]:
    """Entities."""
    _init_ctx(ctx)
    try:
        response = api.get_states(ctx)
    except HTTPError:
        response = {}

    completions = []  # type List[Tuple[str, str]]

    if response:
        for entity in response:
            friendly_name = entity['attributes'].get(  # type: ignore
                'friendly_name', ''
            )
            completions.append(
                (entity['entity_id'], friendly_name)  # type: ignore
            )

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions


def events(
    ctx: Configuration, args: str, incomplete: str
) -> List[Tuple[str, str]]:
    """Events."""
    _init_ctx(ctx)
    try:
        response = api.get_events(ctx)
    except HTTPError:
        response = {}

    completions = []

    if response:
        for entity in response:
            completions.append((entity['event'], ''))  # type: ignore

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions
