"""Valida fontes e evidências do Discovery. Exit 2 indica lacuna essencial."""

import argparse
import json
import re
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


def validate(sources, evidence, coverage=None):
    if coverage is not None:
        return validate_coverage(coverage, sources, evidence)
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


AREAS = ("business", "ui_ux", "frontend", "backend", "data", "security", "quality", "operations")


def validate_coverage(coverage, sources, evidence):
    """Valida vínculos de cobertura; o conteúdo das afirmações exige QA independente."""
    errors, blocked = validate(sources, evidence)
    if not isinstance(coverage, dict):
        return errors + ["coverage: esperado um objeto"], blocked
    if type(coverage.get("version")) is not int or coverage["version"] != 1:
        errors.append("coverage.version: esperado 1")

    def text_required(record, field, label):
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}.{field}: esperado texto não vazio")

    def ids(value, label, prefix=None, known=None):
        if not isinstance(value, list):
            errors.append(f"{label}: esperado uma lista")
            return []
        result = []
        for item in value:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"{label}: ID inválido")
                continue
            if prefix and not re.fullmatch(prefix + r"-[A-Za-z0-9][A-Za-z0-9_-]*", item):
                errors.append(f"{label}: ID inválido: {item}")
            if item in result:
                errors.append(f"{label}: ID duplicado: {item}")
            else:
                result.append(item)
            if known is not None and item not in known:
                errors.append(f"{label}: ID inexistente: {item}")
        return result

    requirements = ids(coverage.get("requirement_ids"), "coverage.requirement_ids", "REQ")
    rules = ids(coverage.get("business_rule_ids"), "coverage.business_rule_ids", "RULE")
    sources_by_id = {row["id"]: row for row in sources if isinstance(row, dict) and isinstance(row.get("id"), str)} if isinstance(sources, list) else {}
    evidence_by_id = {row["id"]: row for row in evidence if isinstance(row, dict) and isinstance(row.get("id"), str)} if isinstance(evidence, list) else {}

    def actual_evidence(evidence_id):
        item = evidence_by_id.get(evidence_id, {})
        source_id = item.get("source_id")
        source = sources_by_id.get(source_id, {}) if isinstance(source_id, str) else {}
        return (item.get("class") in ("OBSERVED", "INFERRED")
                and source.get("status") == "verified"
                and all(isinstance(item.get(field), str) and item[field].strip()
                        for field in ("claim", "limits", "locator"))
                and all(isinstance(source.get(field), str) and source[field].strip()
                        for field in ("location", "revision")))

    for evidence_id, item in evidence_by_id.items():
        if item.get("class") == "UNKNOWN" and item.get("essential") is False:
            for field in ("rationale", "affected_decision"):
                text_required(item, field, evidence_id)

    areas = coverage.get("areas")
    if not isinstance(areas, dict):
        errors.append("coverage.areas: esperado um objeto")
        areas = {}
    for extra in areas.keys() - set(AREAS):
        errors.append(f"coverage.areas: área inválida: {extra}")
    for area in AREAS:
        label = f"coverage.areas.{area}"
        record = areas.get(area)
        if not isinstance(record, dict):
            errors.append(f"{label}: esperado um objeto")
            continue
        text_required(record, "summary", label)
        evidence_ids = ids(record.get("evidence_ids"), f"{label}.evidence_ids", known=evidence_by_id)
        status = record.get("status")
        if status not in ("COVERED", "N/A", "UNKNOWN"):
            errors.append(f"{label}: status inválido")
        elif status == "COVERED":
            if not evidence_ids or not all(actual_evidence(item) for item in evidence_ids):
                errors.append(f"{label}: COVERED requer evidência de fonte verificada, não UNKNOWN")
        else:
            text_required(record, "reason", label)
            if status == "N/A" and evidence_ids:
                errors.append(f"{label}: N/A não pode declarar evidência")
            if status == "UNKNOWN":
                blocked.append(label)
        if area == "business" and rules and status != "COVERED":
            errors.append(f"{label}: regras de negócio exigem COVERED")

    flows = coverage.get("flows")
    if not isinstance(flows, list):
        errors.append("coverage.flows: esperado uma lista")
        flows = []
    flow_ids = []
    covered_requirements, covered_rules = set(), set()
    for row, flow in enumerate(flows, 1):
        label = f"coverage.flows[{row}]"
        if not isinstance(flow, dict):
            errors.append(f"{label}: esperado um objeto")
            continue
        current_ids = ids([flow.get("id")], f"{label}.id", "FLOW")
        if current_ids:
            if current_ids[0] in flow_ids:
                errors.append(f"{label}: ID duplicado: {current_ids[0]}")
            flow_ids.extend(current_ids)
        text_required(flow, "summary", label)
        requirement_ids = ids(flow.get("requirement_ids"), f"{label}.requirement_ids", "REQ", requirements)
        rule_ids = ids(flow.get("business_rule_ids"), f"{label}.business_rule_ids", "RULE", rules)
        evidence_ids = ids(flow.get("evidence_ids"), f"{label}.evidence_ids", known=evidence_by_id)
        if not evidence_ids or not all(actual_evidence(item) for item in evidence_ids):
            errors.append(f"{label}: fluxo requer evidência de fonte verificada, não UNKNOWN")
        else:
            covered_requirements.update(requirement_ids)
            covered_rules.update(rule_ids)
    for missing in sorted(set(requirements) - covered_requirements):
        errors.append(f"coverage: requisito sem fluxo com evidência: {missing}")
    for missing in sorted(set(rules) - covered_rules):
        errors.append(f"coverage: regra sem fluxo com evidência: {missing}")
    return errors, blocked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--require-coverage", action="store_true")
    args = parser.parse_args()
    if args.require_coverage and args.coverage is None:
        print("ERRO: --require-coverage exige --coverage")
        return 1
    try:
        sources = json.loads(args.sources.read_text(encoding="utf-8"))
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
        coverage = json.loads(args.coverage.read_text(encoding="utf-8")) if args.coverage else None
    except (OSError, ValueError) as exc:
        print(f"ERRO: {exc}")
        return 1
    errors, blocked = (validate_coverage(coverage, sources, evidence) if args.coverage
                       else validate(sources, evidence))
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
