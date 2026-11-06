"""Valida a estimativa de fase do TFD."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

from schema_lite import validate

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "estimate.json"


def estimate_order_errors(estimate: dict) -> list[str]:
    if estimate["optimistic_h"] <= estimate["likely_h"] <= estimate["pessimistic_h"]:
        return []
    return ["estimate: exige optimistic_h <= likely_h <= pessimistic_h"]


def validate_estimate(estimate: object) -> list[str]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = validate(estimate, schema)
    if errors:
        return errors

    errors = estimate_order_errors(estimate)
    updated_at = estimate["updated_at"]
    try:
        valid_date = date.fromisoformat(updated_at).isoformat() == updated_at
    except ValueError:
        valid_date = False
    if not valid_date:
        errors.append("updated_at: esperada data válida no formato AAAA-MM-DD")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: python scripts/validate_estimate.py <estimate.json>", file=sys.stderr)
        return 2
    try:
        estimate = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    errors = validate_estimate(estimate)
    if errors:
        for error in errors:
            print(f"ERRO {error}")
        return 1
    print("OK: estimativa válida")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
