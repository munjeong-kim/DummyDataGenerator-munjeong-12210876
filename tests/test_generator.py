import unittest

from dummy_data_generator import generate_records


TEMPLATE = {
    "id": 1,
    "name": "Hong Gildong",
    "email": "hong@example.com",
    "age": 28,
    "is_active": True,
    "score": 87.5,
    "tags": ["admin"],
    "address": {"city": "Seoul", "zipcode": "12345"},
}


class GenerateRecordsTest(unittest.TestCase):
    def test_generates_requested_count(self):
        records = generate_records(TEMPLATE, count=5)
        self.assertEqual(len(records), 5)

    def test_preserves_keys_and_types(self):
        record = generate_records(TEMPLATE, count=1)[0]

        self.assertEqual(set(record.keys()), set(TEMPLATE.keys()))
        self.assertIsInstance(record["id"], int)
        self.assertIsInstance(record["name"], str)
        self.assertIsInstance(record["email"], str)
        self.assertIn("@", record["email"])
        self.assertIsInstance(record["age"], int)
        self.assertIsInstance(record["is_active"], bool)
        self.assertIsInstance(record["score"], float)
        self.assertIsInstance(record["tags"], list)
        self.assertIsInstance(record["address"], dict)
        self.assertEqual(set(record["address"].keys()), set(TEMPLATE["address"].keys()))

    def test_empty_list_template_stays_empty(self):
        record = generate_records({"items": []}, count=1)[0]
        self.assertEqual(record["items"], [])

    def test_flexible_template_structure_unrelated_to_sample(self):
        custom_template = {
            "product_id": 100,
            "variants": [{"sku": "ABC-1", "in_stock": True}],
            "metadata": {"created_at": "2026-01-01T00:00:00", "notes": "n/a"},
        }
        record = generate_records(custom_template, count=1)[0]

        self.assertEqual(set(record.keys()), set(custom_template.keys()))
        self.assertIsInstance(record["variants"], list)
        for variant in record["variants"]:
            self.assertEqual(set(variant.keys()), {"sku", "in_stock"})
            self.assertIsInstance(variant["sku"], str)
            self.assertIsInstance(variant["in_stock"], bool)
        self.assertEqual(set(record["metadata"].keys()), {"created_at", "notes"})


class HintsOverrideTest(unittest.TestCase):
    def test_hint_overrides_type_even_for_int_template_value(self):
        hints = {"id": {"type": "uuid"}}
        record = generate_records({"id": 1}, count=1, hints=hints)[0]
        self.assertIsInstance(record["id"], str)
        self.assertEqual(len(record["id"]), 36)  # canonical uuid4 string length

    def test_hint_int_range_is_respected(self):
        hints = {"age": {"type": "int_range", "min": 18, "max": 20}}
        records = generate_records({"age": 99}, count=20, hints=hints)
        ages = {record["age"] for record in records}
        self.assertTrue(ages.issubset({18, 19, 20}))

    def test_hint_enum_is_respected(self):
        hints = {"role": {"type": "enum", "values": ["admin", "user"]}}
        records = generate_records({"role": "whatever"}, count=20, hints=hints)
        roles = {record["role"] for record in records}
        self.assertTrue(roles.issubset({"admin", "user"}))

    def test_hint_path_for_nested_field(self):
        hints = {"address.city": {"type": "enum", "values": ["Jeju"]}}
        template = {"address": {"city": "Seoul"}}
        record = generate_records(template, count=1, hints=hints)[0]
        self.assertEqual(record["address"]["city"], "Jeju")

    def test_hint_path_for_array_items(self):
        hints = {"tags[]": {"type": "enum", "values": ["vip"]}}
        template = {"tags": ["admin"]}
        records = generate_records(template, count=5, hints=hints)
        for record in records:
            self.assertTrue(all(tag == "vip" for tag in record["tags"]))


if __name__ == "__main__":
    unittest.main()
