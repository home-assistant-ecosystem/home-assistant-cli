"""Constants used by Home Assistant CLI (hass-cli)."""
PACKAGE_NAME = 'homeassistant_cli'

__version__ = '0.3.0'

REQUIRED_PYTHON_VER = (3, 5, 3)

AUTO_SERVER = 'auto'
DEFAULT_SERVER = 'http://localhost:8123'
DEFAULT_HASSIO_SERVER = 'http://hassio/homeassistant'
DEFAULT_TIMEOUT = 5
DEFAULT_OUTPUT = 'json'  # TODO: Have default be human table relevant output

COLUMNS_DEFAULT = [('ALL', '*')]
COLUMNS_ENTITIES = [
    ('ENTITY', 'entity_id'),
    ('DESCRIPTION', 'attributes.friendly_name'),
    ('STATE', 'state'),
]
COLUMNS_SERVICES = [('DOMAIN', 'domain'), ("SERVICE", "domain.services[*]")]
