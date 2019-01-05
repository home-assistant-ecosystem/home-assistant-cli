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
    ctx: Configuration, args: List, incomplete: str
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
        ("presto", "Formatted as PrestoDB cli"),
        ("psql", "Formatted as Postgres psql cli"),
        ("rst", "reStructuredText"),
        ("mediawiki", "Media Wiki as used in Wikpedia"),
        ("moinmoin", "MoinMain Wiki"),
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
