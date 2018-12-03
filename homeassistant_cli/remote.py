"""
Basic api to access remote instance of Home Assistant.

If a connection error occurs while communicating with the API a
HomeAssistantCliError will be raised.

"""
from datetime import datetime
import enum
import json
import logging
import urllib.parse

from typing import Optional, Dict, Any

from aiohttp.hdrs import METH_GET, METH_POST, METH_DELETE, CONTENT_TYPE
import requests

from homeassistant_cli.config import Configuration
from homeassistant_cli.exceptions import HomeAssistantCliError

from homeassistant.const import (
    URL_API, URL_API_DISCOVERY_INFO, URL_API_EVENTS, CONTENT_TYPE_JSON,
    URL_API_EVENTS_EVENT, URL_API_STATES_ENTITY)

_LOGGER = logging.getLogger(__name__)


class APIStatus(enum.Enum):
    """Representation of an API status."""

    OK = "ok"
    INVALID_PASSWORD = "invalid_password"
    CANNOT_CONNECT = "cannot_connect"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        """Return the state."""
        return self.value  # type: ignore


def restapi(ctx: Configuration, method: str, path: str,
            data: Dict = None) -> requests.Response:
    """Make a call to the Home Assistant REST API."""
    if data is None:
        data_str = None
    else:
        data_str = json.dumps(data, cls=JSONEncoder)

    headers = {CONTENT_TYPE: CONTENT_TYPE_JSON}
    if ctx.token is not None:
        headers['Authorization'] = 'Bearer: {}'.format(ctx.token)

    url = urllib.parse.urljoin(ctx.server, path)

    try:
        if method == METH_GET:
            return requests.get(
                url, params=data_str, timeout=ctx.timeout,
                headers=headers)

        return requests.request(
            method, url, data=data_str, timeout=ctx.timeout,
            headers=headers)

    except requests.exceptions.ConnectionError:
        raise HomeAssistantCliError("Error connecting to {}".format(url))

    except requests.exceptions.Timeout:
        error = "Timeout when talking to {}".format(url)
        _LOGGER.exception(error)
        raise HomeAssistantCliError(error)


class JSONEncoder(json.JSONEncoder):
    """JSONEncoder that supports Home Assistant objects."""

    # pylint: disable=method-hidden
    def default(self, o: Any) -> Any:
        """Convert Home Assistant objects.

        Hand other objects to the original method.
        """
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, set):
            return list(o)
        if hasattr(o, 'as_dict'):
            return o.as_dict()

        return json.JSONEncoder.default(self, o)


def validate_api(ctx: Configuration) -> APIStatus:
    """Make a call to validate API."""
    try:
        req = restapi(ctx, METH_GET, URL_API)

        if req.status_code == 200:
            return APIStatus.OK

        if req.status_code == 401:
            return APIStatus.INVALID_PASSWORD

        return APIStatus.UNKNOWN

    except HomeAssistantCliError:
        return APIStatus.CANNOT_CONNECT


def get_info(ctx: Configuration) -> Optional[Dict]:
    """Get basic info about the Homeassistant instance."""
    try:
        req = restapi(ctx, METH_GET, URL_API_DISCOVERY_INFO)

        return req.json() if req.status_code == 200 else {}  # type: ignore

    except (HomeAssistantCliError, ValueError):
        raise HomeAssistantCliError("Unexpected error retriving info")
        # ValueError if req.json() can't parse the json


def remove_state(ctx: Configuration, entity_id: str) -> Optional[Dict]:
    """Call API to remove state for entity_id."""
    try:
        req = restapi(ctx, METH_DELETE,
                      URL_API_STATES_ENTITY.format(entity_id))

        if req.status_code in (200, 404):
            return True
    except HomeAssistantCliError:
        raise HomeAssistantCliError("Unexpected error removing state")

    raise HomeAssistantCliError("Error removing state: %d - %s",
                                req.status_code, req.text)


def get_event_listeners(ctx: Configuration) -> Dict:
    """List of events that is being listened for."""
    try:
        req = restapi(ctx, METH_GET, URL_API_EVENTS)

        return req.json() if req.status_code == 200 else {}  # type: ignore

    except (HomeAssistantCliError, ValueError):
        # ValueError if req.json() can't parse the json
        _LOGGER.exception("Unexpected result retrieving event listeners")

        return {}


def fire_event(ctx: Configuration, event_type: str, data: Dict = None) -> None:
    """Fire an event at remote API."""
    try:
        req = restapi(ctx, METH_POST,
                      URL_API_EVENTS_EVENT.format(event_type), data)

        if req.status_code != 200:
            _LOGGER.error("Error firing event: %d - %s",
                          req.status_code, req.text)

    except HomeAssistantCliError:
        _LOGGER.exception("Error firing event")
