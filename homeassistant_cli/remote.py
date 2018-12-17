"""
Basic api to access remote instance of Home Assistant.

If a connection error occurs while communicating with the API a
HomeAssistantCliError will be raised.

"""
from datetime import datetime
import enum
import json
import logging
from typing import Any, Dict, Optional, cast
import urllib.parse

from homeassistant_cli.config import Configuration, resolve_server
from homeassistant_cli.exceptions import HomeAssistantCliError
import homeassistant_cli.hassconst as hass
import requests

_LOGGER = logging.getLogger(__name__)

# copied from aiohttp.hdrs
CONTENT_TYPE = 'Content-Type'
METH_DELETE = 'DELETE'
METH_GET = 'GET'
METH_POST = 'POST'


class APIStatus(enum.Enum):
    """Representation of an API status."""

    OK = "ok"
    INVALID_PASSWORD = "invalid_password"
    CANNOT_CONNECT = "cannot_connect"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        """Return the state."""
        return self.value  # type: ignore


def restapi(
    ctx: Configuration, method: str, path: str, data: Optional[Dict] = None
) -> requests.Response:
    """Make a call to the Home Assistant REST API."""
    if data is None:
        data_str = None
    else:
        data_str = json.dumps(data, cls=JSONEncoder)

    if not ctx.session:
        ctx.session = requests.Session()
        ctx.session.verify = not ctx.insecure
        if ctx.cert:
            ctx.session.cert = ctx.cert

        _LOGGER.debug(
            "Session: verify(%s), cert(%s)",
            ctx.session.verify,
            ctx.session.cert,
        )

    headers = {CONTENT_TYPE: hass.CONTENT_TYPE_JSON}  # type: Dict[str, Any]

    if ctx.token:
        headers["Authorization"] = "Bearer {}".format(ctx.token)
    if ctx.password:
        headers["x-ha-access"] = ctx.password

    url = urllib.parse.urljoin(resolve_server(ctx) + path, "")

    try:
        if method == METH_GET:
            return requests.get(url, params=data_str, headers=headers)

        return requests.request(method, url, data=data_str, headers=headers)

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
        if hasattr(o, "as_dict"):
            return o.as_dict()

        return json.JSONEncoder.default(self, o)


def validate_api(ctx: Configuration) -> APIStatus:
    """Make a call to validate API."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API)

        if req.status_code == 200:
            return APIStatus.OK

        if req.status_code == 401:
            return APIStatus.INVALID_PASSWORD

        return APIStatus.UNKNOWN

    except HomeAssistantCliError:
        return APIStatus.CANNOT_CONNECT


def get_info(ctx: Configuration) -> Dict[str, Any]:
    """Get basic info about the Homeassistant instance."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_DISCOVERY_INFO)

        req.raise_for_status()

        return (
            cast(Dict[str, Any], req.json()) if req.status_code == 200 else {}
        )

    except (HomeAssistantCliError, ValueError):
        raise HomeAssistantCliError("Unexpected error retriving info")
        # ValueError if req.json() can't parse the json


def get_events(ctx: Configuration) -> Dict[str, Any]:
    """Return all events."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_EVENTS)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting events: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())

    raise HomeAssistantCliError(
        "Error while getting all events: {}".format(req.text)
    )


def get_history(
    ctx: Configuration, entity: Optional[str] = None
) -> Dict[str, Any]:
    """Return History."""
    try:
        method = hass.URL_API_HISTORY
        if entity:
            method = "{}?filter_entity_id={}".format(
                hass.URL_API_HISTORY, entity
            )

        req = restapi(ctx, METH_GET, method)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting history: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())

    raise HomeAssistantCliError(
        "Error while getting all events: {}".format(req.text)
    )


def get_states(ctx: Configuration) -> Dict[str, Any]:
    """Return all states."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_STATES)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting state: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())

    raise HomeAssistantCliError(
        "Error while getting all states: {}".format(req.text)
    )


def get_raw_error_log(ctx: Configuration) -> str:
    """Return the error log."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_ERROR_LOG)
        req.raise_for_status()
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting error log: {}".format(ex)
        )

    return req.text


def get_config(ctx: Configuration) -> Dict[str, Any]:
    """Return the runing config."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_CONFIG)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting config: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, str], req.json())

    raise HomeAssistantCliError(
        "Error while getting all config: {}".format(req.text)
    )


def get_state(ctx: Configuration, entity_id: str) -> Optional[Dict[str, Any]]:
    """Get entity state. If ok, return dictionary with state.

    If no entity found return None - otherwise excepton raised
    with details.
    """
    try:
        req = restapi(
            ctx, METH_GET, hass.URL_API_STATES_ENTITY.format(entity_id)
        )
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting state: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())
    if req.status_code == 404:
        return None

    raise HomeAssistantCliError(
        "Error while getting Entity {}: {}".format(entity_id, req.text)
    )


def remove_state(ctx: Configuration, entity_id: str) -> bool:
    """Call API to remove state for entity_id.

    If success return True, if could not find the entity return False.
    Otherwise raise exception with details.
    """
    try:
        req = restapi(
            ctx, METH_DELETE, hass.URL_API_STATES_ENTITY.format(entity_id)
        )

        if req.status_code == 200:
            return True
        if req.status_code == 404:
            return False
    except HomeAssistantCliError:
        raise HomeAssistantCliError("Unexpected error removing state")

    raise HomeAssistantCliError(
        "Error removing state: {} - {}".format(req.status_code, req.text)
    )


def set_state(
    ctx: Configuration, entity_id: str, data: Dict
) -> Dict[str, Any]:
    """Set/update state for entity id."""
    try:
        req = restapi(
            ctx, METH_POST, hass.URL_API_STATES_ENTITY.format(entity_id), data
        )
    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError(
            "Error updating state for entity {}: {}".format(
                entity_id, exception
            )
        )

    if req.status_code not in (200, 201):
        raise HomeAssistantCliError(
            "Error changing state for entity {}: {} - {}".format(
                entity_id, req.status_code, req.text
            )
        )
    else:
        return cast(Dict[str, Any], req.json())


def render_template(ctx: Configuration, template: str, variables: Dict) -> str:
    """Render template."""
    data = {"template": template, "variables": variables}

    try:
        req = restapi(ctx, METH_POST, hass.URL_API_TEMPLATE, data)
    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError(
            "Error applying template: {}".format(exception)
        )

    if req.status_code not in (200, 201):
        raise HomeAssistantCliError(
            "Error applying template: {} - {}".format(
                req.status_code, req.text
            )
        )
    else:
        return req.text


def get_event_listeners(ctx: Configuration) -> Dict:
    """List of events that is being listened for."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_EVENTS)

        return req.json() if req.status_code == 200 else {}  # type: ignore

    except (HomeAssistantCliError, ValueError):
        # ValueError if req.json() can't parse the json
        _LOGGER.exception("Unexpected result retrieving event listeners")

        return {}


def fire_event(
    ctx: Configuration, event_type: str, data: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Fire an event at remote API."""
    try:
        req = restapi(
            ctx, METH_POST, hass.URL_API_EVENTS_EVENT.format(event_type), data
        )

        if req.status_code != 200:
            _LOGGER.error(
                "Error firing event: %d - %s", req.status_code, req.text
            )

        return cast(Dict[str, Any], req.json())

    except HomeAssistantCliError as exception:
        raise HomeAssistantCliError("Error firing event: {}".format(exception))


def call_service(
    ctx: Configuration,
    domain: str,
    service: str,
    service_data: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Call a service."""
    try:
        req = restapi(
            ctx,
            METH_POST,
            hass.URL_API_SERVICES_SERVICE.format(domain, service),
            service_data,
        )
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError("Error calling service: {}".format(ex))

    if req.status_code != 200:
        raise HomeAssistantCliError(
            "Error calling service: {} - {}".format(req.status_code, req.text)
        )

    return cast(Dict[str, Any], req.json())


def get_services(ctx: Configuration,) -> Dict[str, Any]:
    """Get list of services."""
    try:
        req = restapi(ctx, METH_GET, hass.URL_API_SERVICES)
    except HomeAssistantCliError as ex:
        raise HomeAssistantCliError(
            "Unexpected error getting services: {}".format(ex)
        )

    if req.status_code == 200:
        return cast(Dict[str, Any], req.json())

    raise HomeAssistantCliError(
        "Error while getting all services: {}".format(req.text)
    )
