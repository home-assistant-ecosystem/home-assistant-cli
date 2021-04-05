"""Constants used by Home Assistant components.

Copy of recent homeassistant.const to make hass-cli run
without installing Home Assistant itself.
"""
# Home Assistant WS constants

# Websocket API
WS_TYPE_DEVICE_REGISTRY_LIST = "config/device_registry/list"
WS_TYPE_AREA_REGISTRY_LIST = "config/area_registry/list"
WS_TYPE_AREA_REGISTRY_CREATE = "config/area_registry/create"
WS_TYPE_AREA_REGISTRY_DELETE = "config/area_registry/delete"
WS_TYPE_AREA_REGISTRY_UPDATE = "config/area_registry/update"
WS_TYPE_DEVICE_REGISTRY_UPDATE = "config/device_registry/update"
WS_TYPE_ENTITY_REGISTRY_LIST = "config/entity_registry/list"
WS_TYPE_ENTITY_REGISTRY_GET = "config/entity_registry/get"
WS_TYPE_ENTITY_REGISTRY_UPDATE = "config/entity_registry/update"
WS_TYPE_ENTITY_REGISTRY_REGISTRY = "config/entity_registry/remove"

###############################################################################
# Home Assistant constants

# Format for platform files
PLATFORM_FORMAT = "{platform}.{domain}"

# Can be used to specify a catch all when registering state or event listeners.
MATCH_ALL = "*"

# Entity target all constant
ENTITY_MATCH_NONE = "none"
ENTITY_MATCH_ALL = "all"

# If no name is specified
DEVICE_DEFAULT_NAME = "Unnamed Device"

# Sun events
SUN_EVENT_SUNSET = "sunset"
SUN_EVENT_SUNRISE = "sunrise"

# #### CONFIG ####
CONF_ABOVE = "above"
CONF_ACCESS_TOKEN = "access_token"
CONF_ADDRESS = "address"
CONF_AFTER = "after"
CONF_ALIAS = "alias"
CONF_ALLOWLIST_EXTERNAL_URLS = "allowlist_external_urls"
CONF_API_KEY = "api_key"
CONF_API_TOKEN = "api_token"
CONF_API_VERSION = "api_version"
CONF_ARMING_TIME = "arming_time"
CONF_AT = "at"
CONF_ATTRIBUTE = "attribute"
CONF_AUTH_MFA_MODULES = "auth_mfa_modules"
CONF_AUTH_PROVIDERS = "auth_providers"
CONF_AUTHENTICATION = "authentication"
CONF_BASE = "base"
CONF_BEFORE = "before"
CONF_BELOW = "below"
CONF_BINARY_SENSORS = "binary_sensors"
CONF_BRIGHTNESS = "brightness"
CONF_BROADCAST_ADDRESS = "broadcast_address"
CONF_BROADCAST_PORT = "broadcast_port"
CONF_CHOOSE = "choose"
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_CODE = "code"
CONF_COLOR_TEMP = "color_temp"
CONF_COMMAND = "command"
CONF_COMMAND_CLOSE = "command_close"
CONF_COMMAND_OFF = "command_off"
CONF_COMMAND_ON = "command_on"
CONF_COMMAND_OPEN = "command_open"
CONF_COMMAND_STATE = "command_state"
CONF_COMMAND_STOP = "command_stop"
CONF_CONDITION = "condition"
CONF_CONDITIONS = "conditions"
CONF_CONTINUE_ON_TIMEOUT = "continue_on_timeout"
CONF_COUNT = "count"
CONF_COVERS = "covers"
CONF_CURRENCY = "currency"
CONF_CUSTOMIZE = "customize"
CONF_CUSTOMIZE_DOMAIN = "customize_domain"
CONF_CUSTOMIZE_GLOB = "customize_glob"
CONF_DEFAULT = "default"
CONF_DELAY = "delay"
CONF_DELAY_TIME = "delay_time"
CONF_DESCRIPTION = "description"
CONF_DEVICE = "device"
CONF_DEVICES = "devices"
CONF_DEVICE_CLASS = "device_class"
CONF_DEVICE_ID = "device_id"
CONF_DISARM_AFTER_TRIGGER = "disarm_after_trigger"
CONF_DISCOVERY = "discovery"
CONF_DISKS = "disks"
CONF_DISPLAY_CURRENCY = "display_currency"
CONF_DISPLAY_OPTIONS = "display_options"
CONF_DOMAIN = "domain"
CONF_DOMAINS = "domains"
CONF_EFFECT = "effect"
CONF_ELEVATION = "elevation"
CONF_EMAIL = "email"
CONF_ENTITIES = "entities"
CONF_ENTITY_ID = "entity_id"
CONF_ENTITY_NAMESPACE = "entity_namespace"
CONF_ENTITY_PICTURE_TEMPLATE = "entity_picture_template"
CONF_EVENT = "event"
CONF_EVENT_DATA = "event_data"
CONF_EVENT_DATA_TEMPLATE = "event_data_template"
CONF_EXCLUDE = "exclude"
CONF_EXTERNAL_URL = "external_url"
CONF_FILENAME = "filename"
CONF_FILE_PATH = "file_path"
CONF_FOR = "for"
CONF_FORCE_UPDATE = "force_update"
CONF_FRIENDLY_NAME = "friendly_name"
CONF_FRIENDLY_NAME_TEMPLATE = "friendly_name_template"
CONF_HEADERS = "headers"
CONF_HOST = "host"
CONF_HOSTS = "hosts"
CONF_HS = "hs"
CONF_ICON = "icon"
CONF_ICON_TEMPLATE = "icon_template"
CONF_ID = "id"
CONF_INCLUDE = "include"
CONF_INTERNAL_URL = "internal_url"
CONF_IP_ADDRESS = "ip_address"
CONF_LATITUDE = "latitude"
CONF_LEGACY_TEMPLATES = "legacy_templates"
CONF_LIGHTS = "lights"
CONF_LONGITUDE = "longitude"
CONF_MAC = "mac"
CONF_MAXIMUM = "maximum"
CONF_MEDIA_DIRS = "media_dirs"
CONF_METHOD = "method"
CONF_MINIMUM = "minimum"
CONF_MODE = "mode"
CONF_MONITORED_CONDITIONS = "monitored_conditions"
CONF_MONITORED_VARIABLES = "monitored_variables"
CONF_NAME = "name"
CONF_OFFSET = "offset"
CONF_OPTIMISTIC = "optimistic"
CONF_PACKAGES = "packages"
CONF_PARAMS = "params"
CONF_PASSWORD = "password"
CONF_PATH = "path"
CONF_PAYLOAD = "payload"
CONF_PAYLOAD_OFF = "payload_off"
CONF_PAYLOAD_ON = "payload_on"
CONF_PENDING_TIME = "pending_time"
CONF_PIN = "pin"
CONF_PLATFORM = "platform"
CONF_PORT = "port"
CONF_PREFIX = "prefix"
CONF_PROFILE_NAME = "profile_name"
CONF_PROTOCOL = "protocol"
CONF_PROXY_SSL = "proxy_ssl"
CONF_QUOTE = "quote"
CONF_RADIUS = "radius"
CONF_RECIPIENT = "recipient"
CONF_REGION = "region"
CONF_REPEAT = "repeat"
CONF_RESOURCE = "resource"
CONF_RESOURCES = "resources"
CONF_RESOURCE_TEMPLATE = "resource_template"
CONF_RGB = "rgb"
CONF_ROOM = "room"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_SCENE = "scene"
CONF_SELECTOR = "selector"
CONF_SENDER = "sender"
CONF_SENSORS = "sensors"
CONF_SENSOR_TYPE = "sensor_type"
CONF_SEQUENCE = "sequence"
CONF_SERVICE = "service"
CONF_SERVICE_DATA = "data"
CONF_SERVICE_TEMPLATE = "service_template"
CONF_SHOW_ON_MAP = "show_on_map"
CONF_SLAVE = "slave"
CONF_SOURCE = "source"
CONF_SSL = "ssl"
CONF_STATE = "state"
CONF_STATE_TEMPLATE = "state_template"
CONF_STRUCTURE = "structure"
CONF_SWITCHES = "switches"
CONF_TARGET = "target"
CONF_TEMPERATURE_UNIT = "temperature_unit"
CONF_TIMEOUT = "timeout"
CONF_TIME_ZONE = "time_zone"
CONF_TOKEN = "token"
CONF_TRIGGER_TIME = "trigger_time"
CONF_TTL = "ttl"
CONF_TYPE = "type"
CONF_UNIQUE_ID = "unique_id"
CONF_UNIT_OF_MEASUREMENT = "unit_of_measurement"
CONF_UNIT_SYSTEM = "unit_system"
CONF_UNTIL = "until"
CONF_URL = "url"
CONF_USERNAME = "username"
CONF_VALUE_TEMPLATE = "value_template"
CONF_VARIABLES = "variables"
CONF_VERIFY_SSL = "verify_ssl"
CONF_WAIT_FOR_TRIGGER = "wait_for_trigger"
CONF_WAIT_TEMPLATE = "wait_template"
CONF_WEBHOOK_ID = "webhook_id"
CONF_WEEKDAY = "weekday"
CONF_WHILE = "while"
CONF_WHITELIST = "whitelist"
CONF_ALLOWLIST_EXTERNAL_DIRS = "allowlist_external_dirs"
LEGACY_CONF_WHITELIST_EXTERNAL_DIRS = "whitelist_external_dirs"
CONF_WHITE_VALUE = "white_value"
CONF_XY = "xy"
CONF_ZONE = "zone"

# #### EVENTS ####
EVENT_CALL_SERVICE = "call_service"
EVENT_COMPONENT_LOADED = "component_loaded"
EVENT_CORE_CONFIG_UPDATE = "core_config_updated"
EVENT_HOMEASSISTANT_CLOSE = "homeassistant_close"
EVENT_HOMEASSISTANT_START = "homeassistant_start"
EVENT_HOMEASSISTANT_STARTED = "homeassistant_started"
EVENT_HOMEASSISTANT_STOP = "homeassistant_stop"
EVENT_HOMEASSISTANT_FINAL_WRITE = "homeassistant_final_write"
EVENT_LOGBOOK_ENTRY = "logbook_entry"
EVENT_SERVICE_REGISTERED = "service_registered"
EVENT_SERVICE_REMOVED = "service_removed"
EVENT_STATE_CHANGED = "state_changed"
EVENT_THEMES_UPDATED = "themes_updated"
EVENT_TIMER_OUT_OF_SYNC = "timer_out_of_sync"
EVENT_TIME_CHANGED = "time_changed"


# #### DEVICE CLASSES ####
DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_CO = "carbon_monoxide"
DEVICE_CLASS_CO2 = "carbon_dioxide"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_ILLUMINANCE = "illuminance"
DEVICE_CLASS_SIGNAL_STRENGTH = "signal_strength"
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_TIMESTAMP = "timestamp"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_POWER = "power"
DEVICE_CLASS_CURRENT = "current"
DEVICE_CLASS_ENERGY = "energy"
DEVICE_CLASS_POWER_FACTOR = "power_factor"
DEVICE_CLASS_VOLTAGE = "voltage"

# #### STATES ####
STATE_ON = "on"
STATE_OFF = "off"
STATE_HOME = "home"
STATE_NOT_HOME = "not_home"
STATE_UNKNOWN = "unknown"
STATE_OPEN = "open"
STATE_OPENING = "opening"
STATE_CLOSED = "closed"
STATE_CLOSING = "closing"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_IDLE = "idle"
STATE_STANDBY = "standby"
STATE_ALARM_DISARMED = "disarmed"
STATE_ALARM_ARMED_HOME = "armed_home"
STATE_ALARM_ARMED_AWAY = "armed_away"
STATE_ALARM_ARMED_NIGHT = "armed_night"
STATE_ALARM_ARMED_CUSTOM_BYPASS = "armed_custom_bypass"
STATE_ALARM_PENDING = "pending"
STATE_ALARM_ARMING = "arming"
STATE_ALARM_DISARMING = "disarming"
STATE_ALARM_TRIGGERED = "triggered"
STATE_LOCKED = "locked"
STATE_UNLOCKED = "unlocked"
STATE_UNAVAILABLE = "unavailable"
STATE_OK = "ok"
STATE_PROBLEM = "problem"

# #### STATE AND EVENT ATTRIBUTES ####
# Attribution
ATTR_ATTRIBUTION = "attribution"

# Credentials
ATTR_CREDENTIALS = "credentials"

# Contains time-related attributes
ATTR_NOW = "now"
ATTR_DATE = "date"
ATTR_TIME = "time"
ATTR_SECONDS = "seconds"

# Contains domain, service for a SERVICE_CALL event
ATTR_DOMAIN = "domain"
ATTR_SERVICE = "service"
ATTR_SERVICE_DATA = "service_data"

# IDs
ATTR_ID = "id"

# Name
ATTR_NAME = "name"

# Contains one string or a list of strings, each being an entity id
ATTR_ENTITY_ID = "entity_id"

# Contains one string or a list of strings, each being an area id
ATTR_AREA_ID = "area_id"

# Contains one string, the device ID
ATTR_DEVICE_ID = "device_id"

# String with a friendly name for the entity
ATTR_FRIENDLY_NAME = "friendly_name"

# A picture to represent entity
ATTR_ENTITY_PICTURE = "entity_picture"

# Icon to use in the frontend
ATTR_ICON = "icon"

# The unit of measurement if applicable
ATTR_UNIT_OF_MEASUREMENT = "unit_of_measurement"

CONF_UNIT_SYSTEM_METRIC: str = "metric"
CONF_UNIT_SYSTEM_IMPERIAL: str = "imperial"

# Electrical attributes
ATTR_VOLTAGE = "voltage"

# Location of the device/sensor
ATTR_LOCATION = "location"

ATTR_MODE = "mode"

ATTR_BATTERY_CHARGING = "battery_charging"
ATTR_BATTERY_LEVEL = "battery_level"
ATTR_WAKEUP = "wake_up_interval"

# For devices which support a code attribute
ATTR_CODE = "code"
ATTR_CODE_FORMAT = "code_format"

# For calling a device specific command
ATTR_COMMAND = "command"

# For devices which support an armed state
ATTR_ARMED = "device_armed"

# For devices which support a locked state
ATTR_LOCKED = "locked"

# For sensors that support 'tripping', eg. motion and door sensors
ATTR_TRIPPED = "device_tripped"

# For sensors that support 'tripping' this holds the most recent
# time the device was tripped
ATTR_LAST_TRIP_TIME = "last_tripped_time"

# For all entity's, this hold whether or not it should be hidden
ATTR_HIDDEN = "hidden"

# Location of the entity
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"

# Accuracy of location in meters
ATTR_GPS_ACCURACY = "gps_accuracy"

# If state is assumed
ATTR_ASSUMED_STATE = "assumed_state"
ATTR_STATE = "state"

ATTR_EDITABLE = "editable"
ATTR_OPTION = "option"

# The entity has been restored with restore state
ATTR_RESTORED = "restored"

# Bitfield of supported component features for the entity
ATTR_SUPPORTED_FEATURES = "supported_features"

# Class of device within its domain
ATTR_DEVICE_CLASS = "device_class"

# Temperature attribute
ATTR_TEMPERATURE = "temperature"

# #### UNITS OF MEASUREMENT ####
# Power units
POWER_WATT = "W"
POWER_KILO_WATT = "kW"

# Voltage units
VOLT = "V"

# Energy units
ENERGY_WATT_HOUR = "Wh"
ENERGY_KILO_WATT_HOUR = "kWh"

# Electrical units
ELECTRICAL_CURRENT_AMPERE = "A"
ELECTRICAL_VOLT_AMPERE = "VA"

# Degree units
DEGREE = "°"

# Currency units
CURRENCY_EURO = "€"
CURRENCY_DOLLAR = "$"
CURRENCY_CENT = "¢"

# Temperature units
TEMP_CELSIUS = "°C"
TEMP_FAHRENHEIT = "°F"
TEMP_KELVIN = "K"

# Time units
TIME_MICROSECONDS = "μs"
TIME_MILLISECONDS = "ms"
TIME_SECONDS = "s"
TIME_MINUTES = "min"
TIME_HOURS = "h"
TIME_DAYS = "d"
TIME_WEEKS = "w"
TIME_MONTHS = "m"
TIME_YEARS = "y"

# Length units
LENGTH_MILLIMETERS: str = "mm"
LENGTH_CENTIMETERS: str = "cm"
LENGTH_METERS: str = "m"
LENGTH_KILOMETERS: str = "km"

LENGTH_INCHES: str = "in"
LENGTH_FEET: str = "ft"
LENGTH_YARD: str = "yd"
LENGTH_MILES: str = "mi"

# Frequency units
FREQUENCY_HERTZ = "Hz"
FREQUENCY_GIGAHERTZ = "GHz"

# Pressure units
PRESSURE_PA: str = "Pa"
PRESSURE_HPA: str = "hPa"
PRESSURE_BAR: str = "bar"
PRESSURE_MBAR: str = "mbar"
PRESSURE_INHG: str = "inHg"
PRESSURE_PSI: str = "psi"

# Volume units
VOLUME_LITERS: str = "L"
VOLUME_MILLILITERS: str = "mL"
VOLUME_CUBIC_METERS = "m³"
VOLUME_CUBIC_FEET = "ft³"

VOLUME_GALLONS: str = "gal"
VOLUME_FLUID_OUNCE: str = "fl. oz."

# Volume Flow Rate units
VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR = "m³/h"
VOLUME_FLOW_RATE_CUBIC_FEET_PER_MINUTE = "ft³/m"

# Area units
AREA_SQUARE_METERS = "m²"

# Mass units
MASS_GRAMS: str = "g"
MASS_KILOGRAMS: str = "kg"
MASS_MILLIGRAMS = "mg"
MASS_MICROGRAMS = "µg"

MASS_OUNCES: str = "oz"
MASS_POUNDS: str = "lb"

# Conductivity units
CONDUCTIVITY: str = "µS/cm"

# Light units
LIGHT_LUX: str = "lx"

# UV Index units
UV_INDEX: str = "UV index"

# Percentage units
PERCENTAGE = "%"

# Irradiation units
IRRADIATION_WATTS_PER_SQUARE_METER = "W/m²"

# Precipitation units
PRECIPITATION_MILLIMETERS_PER_HOUR = "mm/h"

# Concentration units
CONCENTRATION_MICROGRAMS_PER_CUBIC_METER = "µg/m³"
CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER = "mg/m³"
CONCENTRATION_PARTS_PER_CUBIC_METER = "p/m³"
CONCENTRATION_PARTS_PER_MILLION = "ppm"
CONCENTRATION_PARTS_PER_BILLION = "ppb"

# Speed units
SPEED_MILLIMETERS_PER_DAY = "mm/d"
SPEED_INCHES_PER_DAY = "in/d"
SPEED_METERS_PER_SECOND = "m/s"
SPEED_INCHES_PER_HOUR = "in/h"
SPEED_KILOMETERS_PER_HOUR = "km/h"
SPEED_MILES_PER_HOUR = "mph"

# Signal_strength units
SIGNAL_STRENGTH_DECIBELS = "dB"
SIGNAL_STRENGTH_DECIBELS_MILLIWATT = "dBm"

# Data units
DATA_BITS = "bit"
DATA_KILOBITS = "kbit"
DATA_MEGABITS = "Mbit"
DATA_GIGABITS = "Gbit"
DATA_BYTES = "B"
DATA_KILOBYTES = "kB"
DATA_MEGABYTES = "MB"
DATA_GIGABYTES = "GB"
DATA_TERABYTES = "TB"
DATA_PETABYTES = "PB"
DATA_EXABYTES = "EB"
DATA_ZETTABYTES = "ZB"
DATA_YOTTABYTES = "YB"
DATA_KIBIBYTES = "KiB"
DATA_MEBIBYTES = "MiB"
DATA_GIBIBYTES = "GiB"
DATA_TEBIBYTES = "TiB"
DATA_PEBIBYTES = "PiB"
DATA_EXBIBYTES = "EiB"
DATA_ZEBIBYTES = "ZiB"
DATA_YOBIBYTES = "YiB"
DATA_RATE_BITS_PER_SECOND = "bit/s"
DATA_RATE_KILOBITS_PER_SECOND = "kbit/s"
DATA_RATE_MEGABITS_PER_SECOND = "Mbit/s"
DATA_RATE_GIGABITS_PER_SECOND = "Gbit/s"
DATA_RATE_BYTES_PER_SECOND = "B/s"
DATA_RATE_KILOBYTES_PER_SECOND = "kB/s"
DATA_RATE_MEGABYTES_PER_SECOND = "MB/s"
DATA_RATE_GIGABYTES_PER_SECOND = "GB/s"
DATA_RATE_KIBIBYTES_PER_SECOND = "KiB/s"
DATA_RATE_MEBIBYTES_PER_SECOND = "MiB/s"
DATA_RATE_GIBIBYTES_PER_SECOND = "GiB/s"

# #### SERVICES ####
SERVICE_HOMEASSISTANT_STOP = "stop"
SERVICE_HOMEASSISTANT_RESTART = "restart"

SERVICE_TURN_ON = "turn_on"
SERVICE_TURN_OFF = "turn_off"
SERVICE_TOGGLE = "toggle"
SERVICE_RELOAD = "reload"

SERVICE_VOLUME_UP = "volume_up"
SERVICE_VOLUME_DOWN = "volume_down"
SERVICE_VOLUME_MUTE = "volume_mute"
SERVICE_VOLUME_SET = "volume_set"
SERVICE_MEDIA_PLAY_PAUSE = "media_play_pause"
SERVICE_MEDIA_PLAY = "media_play"
SERVICE_MEDIA_PAUSE = "media_pause"
SERVICE_MEDIA_STOP = "media_stop"
SERVICE_MEDIA_NEXT_TRACK = "media_next_track"
SERVICE_MEDIA_PREVIOUS_TRACK = "media_previous_track"
SERVICE_MEDIA_SEEK = "media_seek"
SERVICE_REPEAT_SET = "repeat_set"
SERVICE_SHUFFLE_SET = "shuffle_set"

SERVICE_ALARM_DISARM = "alarm_disarm"
SERVICE_ALARM_ARM_HOME = "alarm_arm_home"
SERVICE_ALARM_ARM_AWAY = "alarm_arm_away"
SERVICE_ALARM_ARM_NIGHT = "alarm_arm_night"
SERVICE_ALARM_ARM_CUSTOM_BYPASS = "alarm_arm_custom_bypass"
SERVICE_ALARM_TRIGGER = "alarm_trigger"


SERVICE_LOCK = "lock"
SERVICE_UNLOCK = "unlock"

SERVICE_OPEN = "open"
SERVICE_CLOSE = "close"

SERVICE_CLOSE_COVER = "close_cover"
SERVICE_CLOSE_COVER_TILT = "close_cover_tilt"
SERVICE_OPEN_COVER = "open_cover"
SERVICE_OPEN_COVER_TILT = "open_cover_tilt"
SERVICE_SET_COVER_POSITION = "set_cover_position"
SERVICE_SET_COVER_TILT_POSITION = "set_cover_tilt_position"
SERVICE_STOP_COVER = "stop_cover"
SERVICE_STOP_COVER_TILT = "stop_cover_tilt"
SERVICE_TOGGLE_COVER_TILT = "toggle_cover_tilt"

SERVICE_SELECT_OPTION = "select_option"

# #### API / REMOTE ####
SERVER_PORT = 8123

URL_ROOT = "/"
URL_API = "/api/"
URL_API_STREAM = "/api/stream"
URL_API_CONFIG = "/api/config"
URL_API_DISCOVERY_INFO = "/api/discovery_info"
URL_API_STATES = "/api/states"
URL_API_STATES_ENTITY = "/api/states/{}"
URL_API_EVENTS = "/api/events"
URL_API_EVENTS_EVENT = "/api/events/{}"
URL_API_SERVICES = "/api/services"
URL_API_SERVICES_SERVICE = "/api/services/{}/{}"
URL_API_COMPONENTS = "/api/components"
URL_API_ERROR_LOG = "/api/error_log"
URL_API_LOG_OUT = "/api/log_out"
URL_API_TEMPLATE = "/api/template"

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_ACCEPTED = 202
HTTP_MOVED_PERMANENTLY = 301
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_METHOD_NOT_ALLOWED = 405
HTTP_UNPROCESSABLE_ENTITY = 422
HTTP_TOO_MANY_REQUESTS = 429
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503

HTTP_BASIC_AUTHENTICATION = "basic"
HTTP_DIGEST_AUTHENTICATION = "digest"

HTTP_HEADER_X_REQUESTED_WITH = "X-Requested-With"

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_MULTIPART = "multipart/x-mixed-replace; boundary={}"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"

# The exit code to send to request a restart
RESTART_EXIT_CODE = 100

UNIT_NOT_RECOGNIZED_TEMPLATE: str = "{} is not a recognized {} unit."

LENGTH: str = "length"
MASS: str = "mass"
PRESSURE: str = "pressure"
VOLUME: str = "volume"
TEMPERATURE: str = "temperature"
SPEED_MS: str = "speed_ms"
ILLUMINANCE: str = "illuminance"

WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

# The degree of precision for platforms
PRECISION_WHOLE = 1
PRECISION_HALVES = 0.5
PRECISION_TENTHS = 0.1

# Static list of entities that will never be exposed to
# cloud, alexa, or google_home components
CLOUD_NEVER_EXPOSED_ENTITIES = ["group.all_locks"]

# The ID of the Home Assistant Cast App
CAST_APP_ID_HOMEASSISTANT = "B12CE3CA"
