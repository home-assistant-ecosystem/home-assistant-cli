"""Details for the auto-completion."""
import os
from typing import Any, Dict, List, Tuple  # NOQA

from click.shell_completion import CompletionItem
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

    completions = []  # type List[CompletionItem]
    if response:
        for domain in response:
            domain_name = domain['domain']
            servicesdict = domain['services']

            for service in servicesdict:
                description = servicesdict[service].get('description', '')
                completions.append(
                    CompletionItem(
                        value=f"{domain_name}.{service}", help=description
                    )
                )

        # Sort by service name
        completions.sort(key=lambda x: x.value)

        return [c for c in completions if incomplete in c.value]

    return completions


def entities(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Entities."""
    _init_ctx(ctx)
    try:
        response = api.get_states(ctx)
    except HTTPError:
        response = []

    completions = []  # type List[CompletionItem]

    if response:
        for entity in response:
            state = entity.get('state', '')
            friendly_name = entity['attributes'].get('friendly_name', '')
            completions.append(
                CompletionItem(
                    value=entity['entity_id'],
                    help=f'{friendly_name} [{state}]',
                )
            )

        # Sort by entity_id
        completions.sort(key=lambda x: x.value)

        return [c for c in completions if incomplete in c.value]

    return completions


def events(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Events."""
    _init_ctx(ctx)
    try:
        response = api.get_events(ctx)
    except HTTPError:
        response = {}

    completions = []  # type List[CompletionItem]

    if response:
        for entity in response:
            completions.append(
                CompletionItem(value=entity['event'])  # type: ignore
            )

        # Sort by event name
        completions.sort(key=lambda x: x.value)

        return [c for c in completions if incomplete in c.value]

    return completions


def table_formats(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Table Formats."""
    _init_ctx(ctx)

    completions = [
        CompletionItem(
            value="plain",
            help="Plain tables, no pseudo-graphics to draw lines",
        ),
        CompletionItem(
            value="simple",
            help="Simple table with --- as header/footer (default)",
        ),
        CompletionItem(value="github", help="Github flavored Markdown table"),
        CompletionItem(
            value="grid", help="Formatted as Emacs 'table.el' package"
        ),
        CompletionItem(
            value="fancy_grid",
            help="Draws a fancy grid using box-drawing characters",
        ),
        CompletionItem(value="pipe", help="PHP Markdown Extra"),
        CompletionItem(value="orgtbl", help="org-mode table"),
        CompletionItem(value="jira", help="Atlassian Jira Markup"),
        CompletionItem(value="presto", help="Formatted as PrestoDB CLI"),
        CompletionItem(value="psql", help="Formatted as Postgres psql CLI"),
        CompletionItem(value="rst", help="reStructuredText"),
        CompletionItem(
            value="mediawiki", help="Media Wiki as used in Wikipedia"
        ),
        CompletionItem(value="moinmoin", help="MoinMoin Wiki"),
        CompletionItem(value="youtrack", help="Youtrack format"),
        CompletionItem(value="html", help="HTML Markup"),
        CompletionItem(
            value="latex", help="LaTeX markup, replacing special characters"
        ),
        CompletionItem(
            value="latex_raw",
            help="LaTeX markup, no replacing of special characters",
        ),
        CompletionItem(
            value="latex_booktabs",
            help="LaTex markup using spacing and style from `booktabs",
        ),
        CompletionItem(value="textile", help="Textile"),
        CompletionItem(value="tsv", help="Tab Separated Values"),
    ]

    completions.sort(key=lambda x: x.value)

    return [c for c in completions if incomplete in c.value]


def api_methods(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Auto completion for methods."""
    _init_ctx(ctx)

    from inspect import getmembers

    completions = []  # type List[CompletionItem]

    for name, value in getmembers(hassconst):
        if name.startswith('URL_API_'):
            CompletionItem(value=value, help=name[len('URL_API_') :])

    completions.sort(key=lambda x: x.value)

    return [c for c in completions if incomplete in c.value]


def wsapi_methods(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Auto completion for websocket methods."""
    _init_ctx(ctx)

    from inspect import getmembers

    completions = []  # type List[CompletionItem]

    for name, value in getmembers(hassconst):
        if name.startswith('WS_TYPE_'):
            completions.append(
                CompletionItem(value=value, help=name[len('WS_TYPE_') :])
            )

    completions.sort(key=lambda x: x.value)

    return [c for c in completions if incomplete in c.value]


def _quoteifneeded(val: str) -> str:
    """Add quotes if needed."""
    if val and ' ' in val:
        return '"{}"'.format(val)
    return val


def areas(
    ctx: Configuration, args: List, incomplete: str
) -> List[CompletionItem]:
    """Areas."""
    _init_ctx(ctx)
    allareas = api.get_areas(ctx)

    completions = []  # type List[Tuple[str, str]]

    if allareas:
        for area in allareas:
            completions.append(
                CompletionItem(_quoteifneeded(area['name']), area['area_id'])
            )

        completions.sort(key=lambda x: x.value)

        return [c for c in completions if incomplete in c.value]

    return completions
