"""Generate dummy JSON data from a template JSON file (structure-preserving).

The template can be any JSON structure produced by the real console app -
it does not need to match the bundled `templates/sample_user.json` example.
Field types are auto-inferred from the template's Python types and field
names, and can be explicitly overridden per field via a hints file
(see `dummy_data_generator.hints`).
"""

import random

from .type_registry import generate_by_type, infer_type_from_key


def _child_path(path, key):
    return f"{path}.{key}" if path else key


def _array_item_path(path):
    return f"{path}[]"


def _random_by_type(value, key=""):
    if isinstance(value, bool):
        return generate_by_type("bool")
    if isinstance(value, int):
        magnitude = max(abs(value), 10)
        return generate_by_type("int_range", min=0, max=magnitude * 2)
    if isinstance(value, float):
        magnitude = max(abs(value), 10.0)
        return generate_by_type("float_range", min=0.0, max=magnitude * 2)
    if isinstance(value, str):
        inferred_type = infer_type_from_key(key)
        if inferred_type is not None:
            return generate_by_type(inferred_type)
        return generate_by_type("string", length=len(value) or 8)
    if value is None:
        return None
    raise TypeError(f"Unsupported template value type for key '{key}': {type(value)}")


def _generate_leaf(value, key, path, hints):
    hint = hints.get(path)
    if hint is not None:
        type_name = hint["type"] if isinstance(hint, dict) else hint
        params = {k: v for k, v in hint.items() if k != "type"} if isinstance(hint, dict) else {}
        return generate_by_type(type_name, **params)

    return _random_by_type(value, key)


def generate_from_template(template, hints=None, path=""):
    """Recursively build one dummy record that mirrors the structure of `template`.

    `hints` maps a dot/`[]` field path (see `dummy_data_generator.hints`) to an
    explicit type override, taking precedence over auto-inference.
    """
    hints = hints or {}

    if isinstance(template, dict):
        result = {}
        for key, value in template.items():
            key_path = _child_path(path, key)
            if isinstance(value, (dict, list)):
                result[key] = generate_from_template(value, hints, key_path)
            else:
                result[key] = _generate_leaf(value, key, key_path, hints)
        return result

    if isinstance(template, list):
        if not template:
            return []
        element_template = template[0]
        item_path = _array_item_path(path)
        count = random.randint(1, 3)
        return [generate_from_template(element_template, hints, item_path) for _ in range(count)]

    return _generate_leaf(template, "", path, hints)


def generate_records(template, count=1, hints=None):
    """Generate `count` dummy records from a template dict/list."""
    return [generate_from_template(template, hints=hints) for _ in range(count)]
