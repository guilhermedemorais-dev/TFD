"""Validador de JSON Schema (subconjunto usado pelo TFD), sem dependências.

Suporta: $ref local, $defs, type (string ou lista), required, properties,
additionalProperties (bool ou schema), items, enum, pattern, minLength,
minItems, minimum, maximum. Ignora title/description/$schema.
"""

from __future__ import annotations

import re
from typing import Any


def _resolve(ref: str, root: dict) -> dict:
    if not ref.startswith("#/"):
        raise ValueError(f"$ref não local não suportado: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        node = node[part]
    return node


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate(instance: Any, schema: dict, root: dict | None = None,
             path: str = "$") -> list[str]:
    root = root if root is not None else schema
    errors: list[str] = []

    if "$ref" in schema:
        return validate(instance, _resolve(schema["$ref"], root), root, path)

    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if not any(_type_ok(instance, t) for t in types):
            return [f"{path}: esperado {expected}, recebido {type(instance).__name__}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: valor {instance!r} fora de {schema['enum']}")

    if isinstance(instance, str):
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: {instance!r} não casa com {schema['pattern']}")
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: menor que minLength {schema['minLength']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{path}: {instance} > maximum {schema['maximum']}")

    if isinstance(instance, dict):
        for field in schema.get("required", []):
            if field not in instance:
                errors.append(f"{path}: campo obrigatório ausente: {field}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors += validate(value, properties[key], root, f"{path}.{key}")
            else:
                extra = schema.get("additionalProperties", True)
                if extra is False:
                    errors.append(f"{path}: campo não permitido: {key}")
                elif isinstance(extra, dict):
                    errors += validate(value, extra, root, f"{path}.{key}")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: menos de {schema['minItems']} item(ns)")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                errors += validate(item, item_schema, root, f"{path}[{index}]")

    return errors
