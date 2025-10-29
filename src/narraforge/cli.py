from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .loader.packs import load_packs
from .runtime.engine import RuntimeEngine
from .validator.core import Validator


def cmd_validate(args: argparse.Namespace) -> int:
    validator = Validator()
    report = validator.validate_paths(args.packs)
    for message in report.messages:
        print(f"[{message.level.upper()}] {message.location}: {message.message}")
    return 0 if report.ok() else 1


def cmd_inspect(args: argparse.Namespace) -> int:
    packs = load_packs(Path(path) for path in args.packs)
    engine = RuntimeEngine(packs=packs, seed=args.seed)
    data = {
        "packs": [pack.manifest.id for pack in packs],
        "passages": sorted(engine.list_passages()),
    }
    print(json.dumps(data, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="narraforge")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate one or more content packs")
    validate.add_argument("packs", nargs="+", help="Paths to pack folders")
    validate.set_defaults(func=cmd_validate)

    inspect = sub.add_parser("inspect", help="List loaded passage identifiers")
    inspect.add_argument("packs", nargs="+", help="Paths to pack folders")
    inspect.add_argument("--seed", type=int, default=42)
    inspect.set_defaults(func=cmd_inspect)

    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

