"""Configuration for Home Assistant CLI (hass-cli)."""
import logging
import os
import sys
from typing import Any, Dict, Optional, cast  # noqa: F401

import click
import homeassistant_cli.const as const
from requests import Session  # noqa: ignore
import zeroconf

_LOGGING = logging.getLogger(__name__)


class _ZeroconfListener:
    def __init__(self) -> None:
        self.services = {}  # type: Dict[str, zeroconf.ServiceInfo]

    def remove_service(
        self, _zeroconf: zeroconf.Zeroconf, _type: str, name: str
    ) -> None:
        """Remove service."""
        self.services[name] = None

    def add_service(
        self, _zeroconf: zeroconf.Zeroconf, _type: str, name: str
    ) -> None:
        """Add service."""
        self.services[name] = _zeroconf.get_service_info(_type, name)


def _locate_ha() -> Optional[str]:

    _zeroconf = zeroconf.Zeroconf()
    listener = _ZeroconfListener()
    zeroconf.ServiceBrowser(_zeroconf, "_home-assistant._tcp.local.", listener)
    try:
        import time

        retries = 0
        while not listener.services and retries < 5:
            _LOGGING.info(
                "Trying to locate Home Assistant on\
                local network..."
            )
            time.sleep(0.5)
            retries = retries + 1
    finally:
        _zeroconf.close()

    if listener.services:
        if len(listener.services) > 1:
            _LOGGING.warning(
                "Found multiple Home Assistants at %s",
                ", ".join(listener.services),
            )
            _LOGGING.warning("Use --server to explicitly specify one.")
            return None

        _, service = listener.services.popitem()
        base_url = service.properties[b'base_url'].decode('utf-8')
        _LOGGING.info("Found and using %s as server", base_url)
        return cast(str, base_url)

    _LOGGING.warning(
        "Found no Home Assistant on\
        local network. Using defaults."
    )
    return None


def resolve_server(ctx: Any) -> str:  # noqa: F821
    """Resolve server if not already done.

    if server is `auto` try and resolve it
    """
    # to work around bug in click that hands out
    # non-Configuration context objects.
    if not hasattr(ctx, "resolved_server"):
        ctx.resolved_server = None

    if not ctx.resolved_server:

        if ctx.server == "auto":

            if "HASSIO_TOKEN" in os.environ and "HASS_TOKEN" not in os.environ:
                ctx.resolved_server = const.DEFAULT_HASSIO_SERVER
            else:
                if not ctx.resolved_server and "pytest" in sys.modules:
                    ctx.resolved_server = const.DEFAULT_SERVER
                else:
                    ctx.resolved_server = _locate_ha()
                    if not ctx.resolved_server:
                        sys.exit(3)
        else:
            ctx.resolved_server = ctx.server

        if not ctx.resolved_server:
            ctx.resolved_server = const.DEFAULT_SERVER

    return cast(str, ctx.resolved_server)


class Configuration:
    """The configuration context for the Home Assistant CLI."""

    def __init__(self) -> None:
        """Initialize the configuration."""
        self.verbose = False  # type: bool
        self.server = const.AUTO_SERVER  # type: str
        self.resolved_server = None  # type: Optional[str]
        self.output = const.DEFAULT_OUTPUT  # type: str
        self.token = None  # type: Optional[str]
        self.password = None  # type: Optional[str]
        self.insecure = False  # type: bool
        self.timeout = const.DEFAULT_TIMEOUT  # type: int
        self.debug = False  # type: bool
        self.showexceptions = False  # type: bool
        self.session = None  # type: Optional[Session]
        self.cert = None  # type: Optional[str]

    def echo(self, msg: str, *args: Optional[Any]) -> None:
        """Put content message to stdout."""
        self.log(msg, *args)

    def log(  # pylint: disable=no-self-use
        self, msg: str, *args: Optional[str]
    ) -> None:  # pylint: disable=no-self-use
        """Log a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg: str, *args: Optional[str]) -> None:
        """Log a message only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

    def __repr__(self) -> str:
        """Return the representation of the Configuration."""
        view = {
            "server": self.server,
            "access-token": 'yes' if self.token is not None else 'no',
            "api-password": 'yes' if self.password is not None else 'no',
            "insecure": self.insecure,
            "output": self.output,
            "verbose": self.verbose,
        }

        return "<Configuration({})".format(view)

    def resolve_server(self) -> str:
        """Return resolved server (after resolving if needed)."""
        return resolve_server(self)
