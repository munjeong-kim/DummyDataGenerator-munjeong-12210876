"""Registry of named value generators used both for auto-inference and explicit hints.

To add a new supported type: write a function `_gen_xxx(**params) -> value` and
register it in TYPE_REGISTRY under the name developers will use in a hints file.
"""

import random
import string
import uuid
from datetime import datetime, timedelta

_NAME_POOL = ["Kim Minjun", "Lee Seoyeon", "Park Jihoon", "Choi Yuna", "Jung Doyoon"]
_CITY_POOL = ["Seoul", "Busan", "Incheon", "Daegu", "Gwangju"]
_DOMAIN_POOL = ["example.com", "test.com", "sample.org"]


def _random_string(length=8):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _gen_email(**_params):
    return f"{_random_string(6)}@{random.choice(_DOMAIN_POOL)}"


def _gen_name(**_params):
    return random.choice(_NAME_POOL)


def _gen_phone(**_params):
    return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"


def _gen_city(**_params):
    return random.choice(_CITY_POOL)


def _gen_zipcode(**_params):
    return str(random.randint(10000, 99999))


def _gen_url(**_params):
    return f"https://{random.choice(_DOMAIN_POOL)}/{_random_string(5)}"


def _gen_date(**_params):
    base = datetime(2024, 1, 1)
    offset = timedelta(days=random.randint(0, 700), seconds=random.randint(0, 86400))
    return (base + offset).isoformat()


def _gen_uuid(**_params):
    return str(uuid.uuid4())


def _gen_string(length=8, **_params):
    return _random_string(length)


def _gen_int_range(min=0, max=1000, **_params):
    return random.randint(min, max)


def _gen_float_range(min=0.0, max=1000.0, **_params):
    return round(random.uniform(min, max), 2)


def _gen_bool(**_params):
    return random.choice([True, False])


def _gen_enum(values=None, **_params):
    if not values:
        raise ValueError("The 'enum' type requires a non-empty 'values' list in its hint")
    return random.choice(values)


TYPE_REGISTRY = {
    "email": _gen_email,
    "name": _gen_name,
    "phone": _gen_phone,
    "city": _gen_city,
    "zipcode": _gen_zipcode,
    "url": _gen_url,
    "date": _gen_date,
    "uuid": _gen_uuid,
    "string": _gen_string,
    "int_range": _gen_int_range,
    "float_range": _gen_float_range,
    "bool": _gen_bool,
    "enum": _gen_enum,
}


def generate_by_type(type_name, **params):
    try:
        generator = TYPE_REGISTRY[type_name]
    except KeyError:
        supported = ", ".join(sorted(TYPE_REGISTRY))
        raise ValueError(f"Unknown hint type '{type_name}'. Supported types: {supported}")
    return generator(**params)


KEY_PATTERN_TYPES = [
    ("email", "email"),
    ("name", "name"),
    ("phone", "phone"),
    ("city", "city"),
    ("zipcode", "zipcode"),
    ("zip", "zipcode"),
    ("url", "url"),
    ("date", "date"),
]


def infer_type_from_key(key):
    """Best-effort type guess from a field name. Returns None if nothing matches."""
    lower_key = key.lower()

    if lower_key == "id" or lower_key.endswith("_id") or lower_key.endswith("id"):
        return "uuid"
    for pattern, type_name in KEY_PATTERN_TYPES:
        if pattern in lower_key:
            return type_name
    if lower_key.endswith("_at"):
        return "date"

    return None
