"""Generate dummy JSON data from a template JSON file (structure-preserving)."""

import random
import string
import uuid
from datetime import datetime, timedelta

_NAME_POOL = ["Kim Minjun", "Lee Seoyeon", "Park Jihoon", "Choi Yuna", "Jung Doyoon"]
_CITY_POOL = ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju"]
_DOMAIN_POOL = ["example.com", "test.com", "sample.org"]


def _random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _random_by_key(key):
    """Try to infer a realistic dummy value from the field name. Returns None if no rule matches."""
    lower_key = key.lower()

    if "email" in lower_key:
        return f"{_random_string(6)}@{random.choice(_DOMAIN_POOL)}"
    if lower_key == "id" or lower_key.endswith("_id") or lower_key.endswith("id"):
        return str(uuid.uuid4())
    if "name" in lower_key:
        return random.choice(_NAME_POOL)
    if "phone" in lower_key:
        return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    if "city" in lower_key:
        return random.choice(_CITY_POOL)
    if "zipcode" in lower_key or "zip" in lower_key:
        return str(random.randint(10000, 99999))
    if "url" in lower_key:
        return f"https://{random.choice(_DOMAIN_POOL)}/{_random_string(5)}"
    if "date" in lower_key or lower_key.endswith("_at"):
        base = datetime(2024, 1, 1)
        offset = timedelta(days=random.randint(0, 700), seconds=random.randint(0, 86400))
        return (base + offset).isoformat()

    return None


def _random_by_type(value, key=""):
    if isinstance(value, bool):
        return random.choice([True, False])
    if isinstance(value, int):
        magnitude = max(abs(value), 10)
        return random.randint(0, magnitude * 2)
    if isinstance(value, float):
        magnitude = max(abs(value), 10.0)
        return round(random.uniform(0, magnitude * 2), 2)
    if isinstance(value, str):
        inferred = _random_by_key(key)
        return inferred if inferred is not None else _random_string(len(value) or 8)
    if value is None:
        return None
    raise TypeError(f"Unsupported template value type for key '{key}': {type(value)}")


def generate_from_template(template):
    """Recursively build one dummy record that mirrors the structure of `template`."""
    if isinstance(template, dict):
        return {key: generate_from_template(value) if isinstance(value, (dict, list))
                 else _random_by_type(value, key)
                 for key, value in template.items()}

    if isinstance(template, list):
        if not template:
            return []
        element_template = template[0]
        count = random.randint(1, 3)
        return [generate_from_template(element_template) for _ in range(count)]

    return _random_by_type(template)


def generate_records(template, count=1):
    """Generate `count` dummy records from a template dict/list."""
    return [generate_from_template(template) for _ in range(count)]
