"""CLI entrypoint: read a local JSON template and write generated dummy JSON data."""

import argparse
import json
import random
from pathlib import Path

from dummy_data_generator import default_hints_path, generate_records, load_hints


def parse_args():
    parser = argparse.ArgumentParser(description="Generate dummy JSON data from a JSON template.")
    parser.add_argument("--template", required=True, help="Path to the template JSON file")
    parser.add_argument("--count", type=int, default=1, help="Number of dummy records to generate")
    parser.add_argument("--output", default="output/dummy_data.json", help="Path to write the generated JSON")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible output")
    parser.add_argument(
        "--hints",
        default=None,
        help="Path to a hints JSON file with per-field type overrides "
        "(defaults to '<template>_hints.json' next to the template, if present)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    template_path = Path(args.template)
    template = json.loads(template_path.read_text(encoding="utf-8"))

    hints_path = Path(args.hints) if args.hints else default_hints_path(template_path)
    hints = load_hints(hints_path)

    records = generate_records(template, count=args.count, hints=hints)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    hints_note = f" with hints from '{hints_path}'" if hints else ""
    print(f"Generated {args.count} record(s) from '{template_path}'{hints_note} -> '{output_path}'")


if __name__ == "__main__":
    main()
