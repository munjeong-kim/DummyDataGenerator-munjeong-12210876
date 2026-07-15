"""CLI entrypoint: read a local JSON template and write generated dummy JSON data."""

import argparse
import json
import random
from pathlib import Path

from dummy_data_generator import generate_records


def parse_args():
    parser = argparse.ArgumentParser(description="Generate dummy JSON data from a JSON template.")
    parser.add_argument("--template", required=True, help="Path to the template JSON file")
    parser.add_argument("--count", type=int, default=1, help="Number of dummy records to generate")
    parser.add_argument("--output", default="output/dummy_data.json", help="Path to write the generated JSON")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    template_path = Path(args.template)
    template = json.loads(template_path.read_text(encoding="utf-8"))

    records = generate_records(template, count=args.count)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Generated {args.count} record(s) from '{template_path}' -> '{output_path}'")


if __name__ == "__main__":
    main()
