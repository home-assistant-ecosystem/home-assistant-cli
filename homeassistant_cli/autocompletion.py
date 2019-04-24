"""Details for the auto-completion."""
import os
from typing import Any, Dict, List, Tuple  # NOQA

from requests.exceptions import HTTPError

from homeassistant_cli import const, hassconst
from homeassistant_cli.config import Configuration, resolve_server
import homeassistant_cli.remote as api


def _init_ctx(ctx: Configuration) -> None:
    """Initialize ctx."""
    # ctx is incomplete thus need to 'hack' around it
    # see bug https://github.com/pallets/click/issues/942
    if not hasattr(ctx, 'server'):
        ctx.server = os.environ.get('HASS_SERVER', const.AUTO_SERVER)

    if not hasattr(ctx, 'token'):
        ctx.token = os.environ.get(
            'HASS_TOKEN', os.environ.get('HASSIO_TOKEN', None)
        )

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
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Services."""
    _init_ctx(ctx)
    try:
        response = api.get_services(ctx)
    except HTTPError:
        response = []

    completions = []  # type: List[Tuple[str, str]]
    if response:
        for domain in response:
            domain_name = domain['domain']
            servicesdict = domain['services']

            for service in servicesdict:
                completions.append(
                    (
                        "{}.{}".format(domain_name, service),
                        servicesdict[service]['description'],
                    )
                )

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions


def entities(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Entities."""
    _init_ctx(ctx)
    try:
        response = api.get_states(ctx)
    except HTTPError:
        response = []

    completions = []  # type List[Tuple[str, str]]

    if response:
        for entity in response:
            friendly_name = entity['attributes'].get('friendly_name', '')
            completions.append((entity['entity_id'], friendly_name))

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions


def events(
    ctx: Configuration, args: List, incomplete: str
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


def table_formats(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Table Formats."""
    _init_ctx(ctx)

    completions = [
        ("plain", "Plain tables, no pseudo-graphics to draw lines"),
        ("simple", "Simple table with --- as header/footer (default)"),
        ("github", "Github flavored Markdown table"),
        ("grid", "Formatted as Emacs 'table.el' package"),
        ("fancy_grid", "Draws a fancy grid using box-drawing characters"),
        ("pipe", "PHP Markdown Extra"),
        ("orgtbl", "org-mode table"),
        ("jira", "Atlassian Jira Markup"),
        ("presto", "Formatted as PrestoDB CLI"),
        ("psql", "Formatted as Postgres psql CLI"),
        ("rst", "reStructuredText"),
        ("mediawiki", "Media Wiki as used in Wikipedia"),
        ("moinmoin", "MoinMoin Wiki"),
        ("youtrack", "Youtrack format"),
        ("html", "HTML Markup"),
        ("latex", "LaTeX markup, replacing special characters"),
        ("latex_raw", "LaTeX markup, no replacing of special characters"),
        (
            "latex_booktabs",
            "LaTex markup using spacing and style from `booktabs",
        ),
        ("textile", "Textile"),
        ("tsv", "Tab Separated Values"),
    ]

    completions.sort()

    return [c for c in completions if incomplete in c[0]]


def api_methods(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Auto completion for methods."""
    _init_ctx(ctx)

    from inspect import getmembers

    completions = []
    for name, value in getmembers(hassconst):
        if name.startswith('URL_API_'):
            completions.append((value, name[len('URL_API_'):]))

    completions.sort()

    return [c for c in completions if incomplete in c[0]]


def _quoteifneeded(val: str) -> str:
    """Add quotes if needed."""
    if val and ' ' in val:
        return '"{}"'.format(val)
    return val


def areas(
    ctx: Configuration, args: List, incomplete: str
) -> List[Tuple[str, str]]:
    """Areas."""
    _init_ctx(ctx)
    allareas = api.get_areas(ctx)

    completions = []  # type List[Tuple[str, str]]

    if allareas:
        for area in allareas:
            completions.append((_quoteifneeded(area['name']), area['area_id']))

        completions.sort()

        return [c for c in completions if incomplete in c[0]]

    return completions
