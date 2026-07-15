"""Load optional per-field type hints that override auto-inference for a template."""

import json
from pathlib import Path


def default_hints_path(template_path):
    """Convention: `templates/foo.json` -> `templates/foo_hints.json`."""
    template_path = Path(template_path)
    return template_path.with_name(f"{template_path.stem}_hints.json")


def load_hints(hints_path):
    """Return the hints dict from `hints_path`, or {} if the path is None/missing."""
    if hints_path is None:
        return {}

    path = Path(hints_path)
    if not path.exists():
        return {}

    return json.loads(path.read_text(encoding="utf-8"))
