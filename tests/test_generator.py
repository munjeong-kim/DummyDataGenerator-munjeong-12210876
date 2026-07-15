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


if __name__ == "__main__":
    unittest.main()
