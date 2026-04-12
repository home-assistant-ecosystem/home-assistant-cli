"""Tests for template plugin."""

import os
import tempfile

import pytest
from jinja2.exceptions import SecurityError, UndefinedError

from homeassistant_cli.plugins.template import SAFE_ENV_VARS, render


def _render_template(content, data=None, strict=False):
    """Helper to render a template string via a temp file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".j2", delete=False, dir=tempfile.gettempdir()
    ) as temp_file:
        temp_file.write(content)
        temp_file.flush()
        path = temp_file.name
    try:
        return render(path, data or {}, strict=strict)
    finally:
        os.unlink(path)


# Safe template tests
def test_render_plain_text():
    """Plain text renders unchanged."""
    assert _render_template("hello world") == "hello world"


def test_render_variable():
    """Template variables are substituted."""
    output = _render_template("Hello {{ name }}!", {"name": "Alice"})
    assert output == "Hello Alice!"


def test_render_environ_allowed():
    """The environ global can read allowlisted environment variables."""
    os.environ["HASS_SERVER"] = "http://localhost:8123"
    try:
        output = _render_template("{{ environ('HASS_SERVER') }}")
        assert output == "http://localhost:8123"
    finally:
        del os.environ["HASS_SERVER"]


def test_render_environ_blocked_secret():
    """Secret env vars not in the allowlist are not accessible."""
    os.environ["HASS_TOKEN"] = "super_secret_token"
    try:
        output = _render_template(
            "{{ environ('HASS_TOKEN') or 'hidden' }}"
        )
        assert output == "hidden"
        assert "super_secret_token" not in output
    finally:
        del os.environ["HASS_TOKEN"]


def test_render_environ_blocked_supervisor_token():
    """HASS_SUPERVISOR_TOKEN is not accessible from templates."""
    os.environ["HASS_SUPERVISOR_TOKEN"] = "supervisor_secret"
    try:
        output = _render_template(
            "{{ environ('HASS_SUPERVISOR_TOKEN') or 'hidden' }}"
        )
        assert output == "hidden"
        assert "supervisor_secret" not in output
    finally:
        del os.environ["HASS_SUPERVISOR_TOKEN"]


def test_render_environ_missing():
    """Missing env var returns None (rendered as empty)."""
    output = _render_template(
        "{{ environ('HASS_NONEXISTENT_VAR_12345') or 'default' }}"
    )
    assert output == "default"


def test_safe_env_vars_no_secrets():
    """The allowlist does not contain any secret variables."""
    secret_vars = {"HASS_TOKEN", "HASS_SUPERVISOR_TOKEN", "HASS_PASSWORD"}
    assert SAFE_ENV_VARS.isdisjoint(secret_vars)


def test_render_strict_undefined():
    """Strict mode raises on undefined variables."""
    with pytest.raises(UndefinedError):
        _render_template("{{ undefined_var }}", strict=True)


# Sandbox security tests
def test_sandbox_blocks_globals_access():
    """Accessing __globals__ on environ is blocked."""
    output = _render_template("{{ environ.__globals__ }}")
    assert "builtins" not in output
    assert "__import__" not in output


def test_sandbox_blocks_builtins_via_globals():
    """Accessing __builtins__ via __globals__ is blocked."""
    with pytest.raises(SecurityError):
        _render_template("{% set b = environ.__globals__['__builtins__'] %}{{ b }}")


def test_sandbox_blocks_import():
    """Importing modules via __builtins__.__import__ is blocked."""
    with pytest.raises(SecurityError):
        _render_template(
            "{%- set b = environ.__globals__['__builtins__'] -%}"
            "{%- set os = b['__import__']('os') -%}"
            "{{ os.listdir('/') }}"
        )


def test_sandbox_blocks_os_system():
    """Executing os.system via template injection is blocked."""
    with pytest.raises(SecurityError):
        _render_template(
            "{%- set b = environ.__globals__['__builtins__'] -%}"
            "{%- set os = b['__import__']('os') -%}"
            "{%- set _ = os.system('echo pwned') -%}"
        )


def test_sandbox_blocks_subclass_traversal():
    """Traversing __subclasses__ is blocked."""
    with pytest.raises(SecurityError):
        _render_template("{{ ''.__class__.__mro__[4].__subclasses__() }}")


def test_sandbox_blocks_mro_traversal():
    """Traversing __class__.__mro__ to reach object base is blocked."""
    with pytest.raises(SecurityError):
        _render_template(
            "{{ ''.__class__.__mro__[4].__subclasses__()[4].__init__.__globals__ }}"
        )


def test_sandbox_blocks_file_open():
    """Opening files via builtins is blocked."""
    with pytest.raises(SecurityError):
        _render_template(
            "{%- set b = environ.__globals__['__builtins__'] -%}"
            "{%- set bio = b['__import__']('builtins') -%}"
            "{%- set f = bio.open('/etc/passwd') -%}"
            "{{ f.read() }}"
        )


def test_sandbox_blocks_reverse_shell():
    """Test reverse shell payload is blocked."""
    template = (
        "{%- set b   = environ.__globals__['__builtins__'] -%}"
        "{%- set os  = b['__import__']('os') -%}"
        "{%- set bio = b['__import__']('builtins') -%}"
        "{%- set _f  = bio.open('/tmp/test_shell.py', 'w') -%}"
        "{%- set _   = _f.write('print(\"pwned\")') -%}"
        "{%- set _   = _f.close() -%}"
        "{%- set _   = os.system('python /tmp/test_shell.py') -%}"
    )
    with pytest.raises(SecurityError):
        _render_template(template)
