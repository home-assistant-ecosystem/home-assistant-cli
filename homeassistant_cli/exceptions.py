"""The exceptions used by Home Assistant CLI."""


class HomeAssistantCliError(Exception):
    """General Home Assistant CLI exception occurred."""


class UnsafeTemplateError(HomeAssistantCliError):
    """Template contains unsafe operations."""
