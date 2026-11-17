"""Validação do contrato de task do TFD: schema + regras semânticas."""

from __future__ import annotations

import json
import re
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from schema_lite import validate
from validate_estimate import estimate_order_errors

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "task.json"
TFD_SECTORS = set("database backend frontend ui_ux qa security devops observability documentation harness".split())
COVERAGE_AREAS = ("business", "ui_ux", "frontend", "backend", "data", "security", "quality", "operations")
SECTOR_COVERAGE = {"database": "data", "qa": "quality", "qa_backend": "quality", "qa_ui": "quality",
                   "qa_spec": "quality", "devops": "operations", "observability": "operations",
                   "backend": "backend", "frontend": "frontend", "ui_ux": "ui_ux", "security": "security",
                   "business": "business", "product": "business"}


def load_schema() -> dict:
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def glob_to_regex(pattern: str) -> re.Pattern:
    escaped = re.escape(pattern)
    escaped = escaped.replace(r"\*\*/", r"(?:.*/)?").replace(r"\*\*", r".*")
    escaped = escaped.replace(r"\*", r"[^/]*")
    return re.compile("^" + escaped + "$")


def _duplicates(ids: list[str]) -> list[str]:
    seen, dup = set(), []
    for item in ids:
        if item in seen:
            dup.append(item)
        seen.add(item)
    return dup


def routing_errors(task: dict) -> list[str]:
    if "phases" not in task and "sectors" not in task:
        return []
    if "phases" not in task or "sectors" not in task:
        return ["routing requires phases and sectors together"]
    phases = [phase["id"] for phase in task["phases"]]
    order = {phase: index for index, phase in enumerate(phases)}
    sectors = task["sectors"]
    micros = {micro["id"]: micro for micro in task["microtasks"]}
    refs = {ref["id"] for ref in task["references"]}
    errors = [f"duplicate phase: {phase}" for phase in _duplicates(phases)]
    errors.extend(f"missing sector: {sector}" for sector in sorted(TFD_SECTORS - sectors.keys()))
    for sector, row in sectors.items():
        if not re.fullmatch(r"[a-z][a-z0-9_]*", sector):
            errors.append(f"invalid sector ID: {sector}")
        assigned = any(micro.get("sector") == sector for micro in micros.values())
        if row["applicability"] == "REQUIRED" and not assigned:
            errors.append(f"{sector}: REQUIRED without microtask")
        if row["applicability"] == "N/A" and (assigned or not row.get("reason", "").strip()):
            errors.append(f"{sector}: N/A requires a reason and no microtasks")
        if sector not in TFD_SECTORS and not row.get("reason", "").strip():
            errors.append(f"{sector}: extension requires a reason")
    for phase in phases:
        if not any(micro.get("phase") == phase for micro in micros.values()):
            errors.append(f"{phase}: phase without microtasks")
    for micro in micros.values():
        micro_id = micro["id"]
        phase = micro.get("phase")
        sector = sectors.get(micro.get("sector"))
        if phase not in order:
            errors.append(f"{micro_id}: unknown phase")
        if sector is None or sector["owner"] != micro["owner"]:
            errors.append(f"{micro_id}: sector and owner must match the matrix")
        if not micro.get("reference_ids") or set(micro["reference_ids"]) - refs:
            errors.append(f"{micro_id}: route existing reference IDs")
        for dep in micro.get("depends_on", []):
            dep_phase = micros.get(dep, {}).get("phase")
            if phase in order and dep_phase in order and order[dep_phase] > order[phase]:
                errors.append(f"{micro_id}: dependency {dep} is in a later phase")
    return errors


def coverage_errors(task: dict, *, require_coverage: bool = False) -> list[str]:
    active = "coverage_version" in task or "technical_coverage" in task
    if not active and not require_coverage:
        return []
    errors = []
    if require_coverage and task.get("coverage_version") != 1:
        errors.append("coverage_version=1 obrigatório para nova autoria")
    if require_coverage and ("phases" not in task or "sectors" not in task):
        errors.append("nova autoria exige phases e sectors")
    if not task.get("spec", "").strip():
        errors.append("technical_coverage exige spec")
    if "technical_coverage" not in task:
        return errors + ["technical_coverage obrigatório para cobertura v1"]
    refs = {ref["id"] for ref in task["references"]}
    errors.extend(f"id duplicado: {ref}" for ref in _duplicates([item["id"] for item in task["references"]]))
    micros = {micro["id"] for micro in task["microtasks"]}
    requirements = {req["id"] for req in task["requirements"]}
    rules = {rule["id"] for rule in task["business_rules"]}
    criteria = {ac["id"]: ac for ac in task["acceptance_criteria"]}
    covered_micros, covered_reqs, covered_rules = set(), set(), set()
    for area, cell in task["technical_coverage"].items():
        label = f"technical_coverage.{area}"
        links = {"reference_ids": refs, "microtask_ids": micros, "acceptance_ids": criteria.keys()}
        if area == "business":
            links["rule_ids"] = rules
        for field, known in links.items():
            for linked_id in cell[field]:
                if linked_id not in known:
                    errors.append(f"{label}: {field} contém ID inexistente: {linked_id}")
            for duplicate in _duplicates(cell[field]):
                errors.append(f"{label}: {field} contém ID duplicado: {duplicate}")
        if cell["status"] == "N/A":
            reason = cell.get("reason", "").strip()
            if not reason or reason.casefold().rstrip(".! ") in {
                "n/a", "na", "não se aplica", "nao se aplica", "fora do escopo", "não aplicável", "nao aplicavel",
            }:
                errors.append(f"{label}: N/A exige justificativa específica")
            if any(cell[field] for field in links):
                errors.append(f"{label}: N/A não permite links")
            continue
        if not cell["summary"].strip():
            errors.append(f"{label}: COVERED exige summary não vazio")
        for field in ("reference_ids", "microtask_ids", "acceptance_ids"):
            if not cell[field]:
                errors.append(f"{label}: COVERED exige {field}")
        cell_rules = set()
        for ac_id in cell["acceptance_ids"]:
            ac = criteria.get(ac_id)
            if ac is None:
                continue
            if not set(ac["microtask_ids"]).intersection(cell["microtask_ids"]):
                errors.append(f"{label}: {ac_id} sem vínculo com microtask_ids da área")
                continue
            covered_micros.update(set(ac["microtask_ids"]).intersection(cell["microtask_ids"]) & micros)
            covered_reqs.update(ac["requirement_ids"])
            cell_rules.update(ac.get("rule_ids", []))
        covered_rules.update(cell_rules)
        if area == "business":
            for rule_id in sorted(rules - set(cell["rule_ids"])):
                errors.append(f"{label}: regra sem cobertura: {rule_id}")
            for rule_id in sorted(set(cell["rule_ids"]) - cell_rules):
                errors.append(f"{label}: {rule_id} sem critério de aceite vinculado")
    for field, missing in (("microtask", micros - covered_micros),
                           ("requirement", requirements - covered_reqs), ("rule", rules - covered_rules)):
        for linked_id in sorted(missing):
            errors.append(f"technical_coverage: {field} sem cobertura: {linked_id}")
    if rules and task["technical_coverage"]["business"]["status"] != "COVERED":
        errors.append("technical_coverage.business: regras de negócio exigem COVERED")
    for sector, row in task.get("sectors", {}).items():
        area = SECTOR_COVERAGE.get(sector)
        if area and row["applicability"] == "REQUIRED" and task["technical_coverage"][area]["status"] != "COVERED":
            errors.append(f"technical_coverage.{area}: setor {sector} REQUIRED exige COVERED")
    return errors


def semantic_errors(task: dict, *, require_coverage: bool = False) -> list[str]:
    errors = routing_errors(task)
    errors.extend(coverage_errors(task, require_coverage=require_coverage))
    tests = {t["id"] for t in task["required_tests"]}
    requirements = {r["id"] for r in task["requirements"]}
    microtasks = {m["id"] for m in task["microtasks"]}
    rules = {r["id"] for r in task["business_rules"]}
    dependency_graph = TopologicalSorter()
    covered_requirements: set[str] = set()
    covered_microtasks: set[str] = set()

    for ac in task["acceptance_criteria"]:
        for rule_id in ac.get("rule_ids", []):
            if rule_id not in rules:
                errors.append(f"{ac['id']}: rule_ids contém ID inexistente: {rule_id}")
        if ac["validation"] not in tests:
            errors.append(f"{ac['id']}: validation {ac['validation']} não existe em required_tests")
        for field, known_ids, covered_ids in (
            ("requirement_ids", requirements, covered_requirements),
            ("microtask_ids", microtasks, covered_microtasks),
        ):
            for linked_id in ac[field]:
                if linked_id not in known_ids:
                    errors.append(f"{ac['id']}: {field} contém ID inexistente: {linked_id}")
                else:
                    covered_ids.add(linked_id)

    for missing_id in sorted((requirements - covered_requirements) | (microtasks - covered_microtasks)):
        errors.append(f"{missing_id}: sem critério de aceite")

    for micro in task["microtasks"]:
        dependency_graph.add(micro["id"])
        if micro["owner"] == micro["validator"]:
            errors.append(f"{micro['id']}: validator deve ser diferente de owner")
        for dep in micro.get("depends_on", []):
            if dep not in microtasks:
                errors.append(f"{micro['id']}: depends_on {dep} não existe")
            else:
                dependency_graph.add(micro["id"], dep)
        for path in micro["allowed_paths"]:
            if not any(glob_to_regex(p).match(path) for p in task["allowed_paths"]):
                errors.append(f"{micro['id']}: path {path} fora de allowed_paths da task")

    try:
        dependency_graph.prepare()
    except CycleError as exc:
        cycle = " -> ".join(reversed(exc.args[1]))
        errors.append(f"depends_on: ciclo de dependências: {cycle}")

    all_ids = ([r["id"] for r in task["requirements"]]
               + [b["id"] for b in task["business_rules"]]
               + [m["id"] for m in task["microtasks"]]
               + [a["id"] for a in task["acceptance_criteria"]]
               + [t["id"] for t in task["required_tests"]])
    for dup in _duplicates(all_ids):
        errors.append(f"id duplicado: {dup}")

    if task["complexity"] == "complex" and not task.get("spec"):
        errors.append("complexity=complex exige 'spec'")

    if "estimate" in task:
        errors.extend(estimate_order_errors(task["estimate"]))

    return errors


def validate_task(task: dict, schema: dict | None = None, *, allow_unestimated_draft: bool = False,
                  require_coverage: bool = False) -> list[str]:
    schema = schema or load_schema()
    if allow_unestimated_draft and isinstance(task, dict) and task.get("status") == "draft":
        schema = {**schema, "required": [key for key in schema["required"] if key != "estimate"]}
    schema_errors = validate(task, schema)
    if schema_errors:
        # sem forma válida não há como avaliar as regras semânticas
        return schema_errors
    return semantic_errors(task, require_coverage=require_coverage)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("--require-coverage", action="store_true", help="require coverage v1 for new authoring")
    args = parser.parse_args()
    task = json.loads(args.task.read_text(encoding="utf-8"))
    errors = validate_task(task, require_coverage=args.require_coverage)
    if errors:
        for error in errors:
            print(f"ERRO {error}")
        return 1
    print("OK: contrato válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
