"""Yaml utility for hass-cli."""

from typing import Any, Optional, cast

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


def yaml() -> YAML:
    """Return default YAML parser."""
    yamlp = YAML(typ='safe', pure=True)
    yamlp.preserve_quotes = True
    yamlp.default_flow_style = False
    return yamlp


def loadyaml(yamlp: YAML, source: str) -> Any:
    """Load YAML."""
    return yamlp.load(source)


def dumpyaml(
    yamlp: YAML, data: Any, stream: Any = None, **kw: Any
) -> Optional[str]:
    """Dump YAML to string."""
    inefficient = False
    if stream is None:
        inefficient = True
        stream = StringIO()
    # overriding here to get dumping to
    # not sort keys.
    yamlp = YAML()
    yamlp.indent(mapping=4, sequence=6, offset=3)
    # yamlp.compact(seq_seq=False, seq_map=False)
    yamlp.dump(data, stream, **kw)
    if inefficient:
        return cast(str, stream.getvalue())
    return None
