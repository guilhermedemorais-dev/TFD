"""Valida fontes e evidências do Discovery. Exit 2 indica lacuna essencial."""

import argparse
import json
from pathlib import Path


def index_records(records, label, required_text, errors):
    indexed = {}
    if not isinstance(records, list):
        errors.append(f"{label}: esperado uma lista")
        return indexed
    for row, record in enumerate(records, 1):
        if not isinstance(record, dict):
            errors.append(f"{label}[{row}]: esperado um objeto")
            continue
        for field in required_text:
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}[{row}].{field}: esperado texto não vazio")
        record_id = record.get("id")
        if isinstance(record_id, str) and record_id.strip():
            if record_id in indexed:
                errors.append(f"{label}: ID duplicado: {record_id}")
            else:
                indexed[record_id] = record
    return indexed


def validate(sources, evidence):
    errors = []
    blocked = []
    if evidence == []:
        errors.append("evidence: registre pelo menos um achado ou uma lacuna")
    sources_by_id = index_records(sources, "sources", ("id", "location", "revision"), errors)
    evidence_by_id = index_records(evidence, "evidence", ("id", "claim", "limits"), errors)

    for source_id, source in sources_by_id.items():
        if source.get("status") not in ("verified", "stale", "missing"):
            errors.append(f"{source_id}: status de fonte inválido")

    for evidence_id, item in evidence_by_id.items():
        kind = item.get("class")
        if kind not in ("OBSERVED", "INFERRED", "UNKNOWN"):
            errors.append(f"{evidence_id}: classe inválida")
            continue
        source_id = item.get("source_id")
        source = sources_by_id.get(source_id) if isinstance(source_id, str) else None
        if kind == "UNKNOWN":
            if "source_id" in item and source is None:
                errors.append(f"{evidence_id}: source_id inexistente")
            if not isinstance(item.get("essential"), bool):
                errors.append(f"{evidence_id}: essential deve ser booleano")
            elif item["essential"]:
                blocked.append(evidence_id)
            continue
        if source is None or source.get("status") != "verified":
            errors.append(f"{evidence_id}: requer source_id de fonte verificada")
        locator = item.get("locator")
        if not isinstance(locator, str) or not locator.strip():
            errors.append(f"{evidence_id}: locator obrigatório")

    return errors, blocked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        sources = json.loads(args.sources.read_text(encoding="utf-8"))
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERRO: {exc}")
        return 1
    errors, blocked = validate(sources, evidence)
    if errors:
        for error in errors:
            print(f"ERRO: {error}")
        return 1
    if blocked:
        print("BLOCKED: " + ", ".join(blocked))
        return 2
    print("OK: fontes e evidências válidas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
