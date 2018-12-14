"""Helpers used by Home Assistant CLI (hass-cli)."""
import contextlib
from http.client import HTTPConnection
import json
import logging
import shlex
from typing import Any, Dict, Generator, List, Optional, cast

from homeassistant_cli.config import Configuration
import homeassistant_cli.const as const
from tabulate import tabulate
import yaml


def to_attributes(entry: str) -> Optional[Dict[str, str]]:
    """Convert list of key=value pairs to dictionary."""
    if not entry:
        return None

    lexer = shlex.shlex(entry, posix=True)
    lexer.whitespace_split = True
    lexer.whitespace = ','
    attributes_dict = {}  # type: Dict[str, str]
    attributes_dict = dict(
        pair.split('=', 1) for pair in lexer  # type: ignore
    )
    return attributes_dict


def raw_format_output(
    output: str, data: Dict[str, Any], columns: Optional[List] = None
) -> str:
    """Format the raw output."""
    if output == 'json':
        try:
            return json.dumps(data, indent=2, sort_keys=False)
        except ValueError:
            return str(data)
    elif output == 'yaml':
        try:
            return cast(str, yaml.safe_dump(data, default_flow_style=False))
        except ValueError:
            return str(data)
    elif output == 'table':
        from jsonpath_rw import parse

        if not columns:
            columns = const.COLUMNS_DEFAULT

        fmt = [(v[0], parse(v[1])) for v in columns]
        result = []
        headers = [v[0] for v in fmt]
        for item in data:
            row = []
            for fmtpair in fmt:
                val = [match.value for match in fmtpair[1].find(item)]
                row.append(", ".join(map(str, val)))

            result.append(row)
        return cast(str, tabulate(result, headers=headers))
    else:
        raise ValueError(
            "Output Format was {}, expected either 'json' or 'yaml'".format(
                output
            )
        )


def format_output(
    ctx: Configuration, data: Dict[str, Any], columns: Optional[List] = None
) -> str:
    """Format dict to defined output."""
    return raw_format_output(ctx.output, data, columns)


def debug_requests_on() -> None:
    """Switch on logging of the requests module."""
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def debug_requests_off() -> None:
    """Switch off logging of the requests module.

    Might have some side-effects.
    """
    HTTPConnection.set_debuglevel(cast(HTTPConnection, HTTPConnection), 1)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.WARNING)
    root_logger.handlers = []
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.WARNING)
    requests_log.propagate = False


@contextlib.contextmanager
def debug_requests() -> Generator:
    """Yieldable way to turn on debugs for requests.

    with debug_requests(): <do things>
    """
    debug_requests_on()
    yield
    debug_requests_off()
