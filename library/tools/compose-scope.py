#!/usr/bin/env python3
"""Compare rendered Compose JSON against explicit change scope. Never invokes Docker."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


RESOURCES = ("services", "volumes", "networks", "secrets", "configs")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def read_config(path):
    raw = Path(path).read_bytes()
    config = json.loads(raw, object_pairs_hook=unique_object)
    # Reject nonstandard NaN/Infinity and float overflow, including unchanged data.
    json.dumps(config, allow_nan=False)
    if not isinstance(config, dict):
        raise ValueError("Compose config must be an object")
    for kind in RESOURCES:
        items = config.get(kind, {})
        if not isinstance(items, dict):
            raise ValueError("Compose resource group must be an object")
        if any(not isinstance(value, dict) and value is not None
               for value in items.values()):
            raise ValueError("Compose resource definition must be an object or null")
        if kind == "services" and any(value is None for value in items.values()):
            raise ValueError("Compose service definition must be an object")
    return config, hashlib.sha256(raw).hexdigest()


def compare(before, after, allowed):
    changes = []
    missing = object()

    def same(left, right):
        if left is missing or right is missing:
            return left is right
        # Python equality conflates true/1 and false/0 recursively. Compare JSON
        # values with their types intact instead; object key ordering is immaterial.
        return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(
            right, sort_keys=True, allow_nan=False)

    for kind in sorted(before.keys() | after.keys()):
        if kind in RESOURCES:
            old, new = before.get(kind, {}), after.get(kind, {})
            if (kind in before) != (kind in after) and not old and not new:
                changes.append({"kind": "fields", "name": kind,
                                "allowed": kind in allowed.get("fields", ())})
            for name in sorted(old.keys() | new.keys()):
                if not same(old.get(name, missing), new.get(name, missing)):
                    changes.append({"kind": kind, "name": name,
                                    "allowed": name in allowed.get(kind, ())})
        elif not same(before.get(kind, missing), after.get(kind, missing)):
            changes.append({"kind": "fields", "name": kind,
                            "allowed": kind in allowed.get("fields", ())})
    return changes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True, help="Reviewed baseline rendered JSON")
    parser.add_argument("--after", required=True, help="Proposed rendered JSON")
    for kind in (*RESOURCES, "fields"):
        parser.add_argument("--allow-" + kind, action="append", default=[],
                            help="Exact resource/field name authorized to change; repeatable")
    args = parser.parse_args(argv)
    try:
        before, before_hash = read_config(args.before)
        after, after_hash = read_config(args.after)
        allowed = {kind: set(getattr(args, "allow_" + kind))
                   for kind in (*RESOURCES, "fields")}
        changes = compare(before, after, allowed)
    except (OSError, ValueError, TypeError):
        # Never echo interpolated config, filesystem paths, credentials or parser excerpts.
        print(json.dumps({"status": "INVALID_INPUT", "operationally_verified": False}))
        return 2
    permitted = all(change["allowed"] for change in changes)
    print(json.dumps({"status": "WITHIN_SCOPE" if permitted else "OUT_OF_SCOPE",
                      "before_sha256": before_hash, "after_sha256": after_hash,
                      "changes": changes, "operationally_verified": False}, sort_keys=True))
    return 0 if permitted else 1


if __name__ == "__main__":
    sys.exit(main())
