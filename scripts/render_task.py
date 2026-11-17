# Contexto TFD · 1288 palavras · 2772 tokens (o200k_base)

"""Render a human-readable task body from its canonical JSON."""

import argparse
import json
import sys
from pathlib import Path

from context_budget import WORDS, load_encoding
from validate_task import COVERAGE_AREAS, validate_task


AREA_LABELS = dict(zip(COVERAGE_AREAS, ("Negócio", "UI/UX", "Frontend", "Backend", "Dados",
                                      "Segurança", "Qualidade", "Operações")))


def coverage_rows(task):
    """Shared compact content for Markdown and the escaped human review."""
    for area in COVERAGE_AREAS:
        cell = task.get("technical_coverage", {}).get(area)
        if cell is None:
            continue
        if cell["status"] == "N/A":
            yield AREA_LABELS[area], "N/A", cell["reason"], ""
        else:
            links = " · ".join(", ".join(cell.get(field, [])) for field in
                               ("reference_ids", "microtask_ids", "acceptance_ids", "rule_ids") if cell.get(field))
            yield AREA_LABELS[area], "COVERED", cell["summary"], links


def sector_context(task, sector, microtask_id=None):
    if task.get("sectors", {}).get(sector, {}).get("applicability") != "REQUIRED":
        raise ValueError(f"setor sem execução: {sector}")
    microtasks = [micro for micro in task["microtasks"] if micro["sector"] == sector
                  and (microtask_id is None or micro["id"] == microtask_id)]
    if not microtasks:
        raise ValueError(f"microtarefa fora da rota: {microtask_id}")
    ids = {micro["id"] for micro in microtasks}
    phase_ids = {micro["phase"] for micro in microtasks}
    criteria = [entry for entry in task["acceptance_criteria"] if ids.intersection(entry["microtask_ids"])]
    reqs = {req for entry in criteria for req in entry["requirement_ids"]}
    tests = {entry["validation"] for entry in criteria}
    refs = {ref for micro in microtasks for ref in micro["reference_ids"]}
    context = {key: task[key] for key in ("task_id", "contract_revision", "status", "goal", "scope",
                                         "out_of_scope", "protected_paths", "business_rules", "gates", "stop_conditions")}
    projection = {**context, "sector": sector, "phases": [phase for phase in task["phases"] if phase["id"] in phase_ids],
            "microtasks": microtasks, "acceptance_criteria": criteria,
            "requirements": [entry for entry in task["requirements"] if entry["id"] in reqs],
            "required_tests": [entry for entry in task["required_tests"] if entry["id"] in tests],
            "references": [entry for entry in task["references"] if entry["id"] in refs]}
    if "technical_coverage" in task:
        # This execution slice is not a new canonical task. Keep global constraints
        # and every mandatory reference of the selected MTs and applicable cells.
        ac_ids = {ac["id"] for ac in criteria}
        rule_ids = {rule for ac in criteria for rule in ac.get("rule_ids", [])}
        projection["technical_coverage"] = {}
        for area, cell in task["technical_coverage"].items():
            if cell["status"] != "COVERED" or not ids.intersection(cell["microtask_ids"]):
                continue
            projection["technical_coverage"][area] = {
                **cell, "microtask_ids": [item for item in cell["microtask_ids"] if item in ids],
                "acceptance_ids": [item for item in cell["acceptance_ids"] if item in ac_ids],
            }
            refs.update(cell["reference_ids"])
            if area == "business":
                projection["technical_coverage"][area]["rule_ids"] = [
                    rule for rule in cell["rule_ids"] if rule in rule_ids]
        projection["references"] = [ref for ref in task["references"] if ref["id"] in refs]
        projection["business_rules"] = [rule for rule in task["business_rules"] if rule["id"] in rule_ids]
        projection["acceptance_criteria"] = [
            {**ac, "microtask_ids": [micro for micro in ac["microtask_ids"] if micro in ids]} for ac in criteria]
        projection["spec"] = task["spec"]
        if "coverage_version" in task:
            projection["coverage_version"] = task["coverage_version"]
    return projection


def microtask_lines(micro, task=None):
    paths = ", ".join(f"`{path}`" for path in micro["allowed_paths"])
    outputs = "; ".join(micro["deliverables"])
    lines = [
        f"  - Responsável: `@{micro['owner']}` · Validador independente: `@{micro['validator']}`",
        f"  - Caminhos permitidos: {paths}",
        "  - Pode: executar o checklist abaixo nos caminhos permitidos, respeitando os limites globais e o gate atual.",
        *(f"    - {item}" for item in micro["checklist"]),
        "  - Não pode: editar fora desses caminhos ou em caminhos protegidos, ampliar escopo ou contornar gates; respeite os [limites globais](#limites-globais).",
        f"  - Resultado esperado: {outputs}",
        f"  - Concluído quando: {micro['completion_condition']}",
    ]
    if task and "technical_coverage" in task:
        lines.append("  - Referências obrigatórias: " + (", ".join(micro.get("reference_ids", []))
                                                       or ", ".join(ref["id"] for ref in task["references"])))
        for ac in task["acceptance_criteria"]:
            if micro["id"] in ac["microtask_ids"]:
                links = ", ".join([*ac["requirement_ids"], *ac.get("rule_ids", []), ac["validation"]])
                lines.append(f"  - Aceite {ac['id']}: {ac['description']} · {links}")
    return lines


def sector_lines(task, json_link, receipts):
    sectors = dict(sorted(task["sectors"].items(), key=lambda item: item[0] != "harness"))
    phase_order = {phase["id"]: index for index, phase in enumerate(task["phases"])}
    microtasks = sorted(task["microtasks"], key=lambda micro: phase_order[micro["phase"]])
    lines = ["", "## Fases", ""]
    for phase in task["phases"]:
        labels = dict.fromkeys(sectors[micro["sector"]]["label"] for micro in task["microtasks"]
                               if micro["phase"] == phase["id"])
        note = f". {phase['note']}" if "note" in phase else ""
        lines.append(f"- **{phase['id']} · {phase['title']}** · {', '.join(labels)}{note}")
    lines.extend(["", "## Matriz por setor", "", "| Setor | Dono | Aplicabilidade |", "|---|---|---|"])
    for sector, row in sectors.items():
        route = f"[{row['label']}](#{sector})" if row["applicability"] == "REQUIRED" else row["label"]
        applicability = row["applicability"]
        if applicability == "N/A":
            applicability += f" · {row['reason']}"
        lines.append(f"| {route} | `{row['owner']}` | {applicability} |")
    for sector, row in sectors.items():
        if row["applicability"] != "REQUIRED":
            continue
        receipt = receipts.get(sector, {})
        lines.extend(["", f'<a id="{sector}"></a>', f"### {row['label']}", ""])
        for micro in (entry for entry in microtasks if entry["sector"] == sector):
            result = receipt.get("reviews", {}).get(micro["id"], {})
            verdict = result.get("verdict")
            observation = result.get("observation", "Aguardando QA")
            if verdict == "BLOCKED":
                observation = f"Bloqueado · {observation}"
            dependencies = ", ".join(micro.get("depends_on", [])) or "livre"
            lines.append(f"- **{micro['id']} · {micro['phase']}** {micro['title']} · depende de {dependencies}")
            lines.append(f"  - {'☑' if verdict == 'PASS' else '☐'} Aprovado · "
                         f"{'☑' if verdict == 'REWORK' else '☐'} Reprovado · {observation}")
            lines.extend(microtask_lines(micro, task))
        lines.extend(["", f"[JSON]({json_link}) · `--sector {sector}`",
                      f"Feito: {receipt.get('summary', 'pendente')} · "
                      f"Bloqueios: {receipt.get('blockers', 'a verificar')} · "
                      f"Tokens reais: {receipt['total_tokens'] if receipt.get('total_tokens') is not None else 'indisponíveis'}"])
    return lines


def read_sector_receipts(task, workflow):
    if not isinstance(workflow, dict):
        raise ValueError("o workflow deve ser um objeto JSON")
    if (workflow.get("task_id"), workflow.get("contract_revision")) != (task["task_id"], task["contract_revision"]):
        raise ValueError("os recibos precisam corresponder à task e revisão atuais")
    receipts = workflow.get("sector_receipts", {})
    if not isinstance(receipts, dict):
        raise ValueError("sector_receipts deve ser um objeto")
    micros = {entry["id"]: entry for entry in task["microtasks"]}
    for sector, receipt in receipts.items():
        if task.get("sectors", {}).get(sector, {}).get("applicability") != "REQUIRED":
            raise ValueError(f"recibo sem setor aplicável: {sector}")
        if not isinstance(receipt, dict) or not isinstance(receipt.get("reviews", {}), dict):
            raise ValueError(f"{sector}: recibo ou pareceres inválidos")
        total = receipt.get("total_tokens")
        if total is not None and (type(total) is not int or total < 0 or not receipt.get("token_receipt")):
            raise ValueError(f"{sector}: tokens exigem recibo de uso")
        for micro_id, review in receipt.get("reviews", {}).items():
            micro = micros.get(micro_id, {})
            if (not isinstance(review, dict) or micro.get("sector") != sector or micro.get("validator") != review.get("role")
                    or review.get("verdict") not in {"PASS", "REWORK", "BLOCKED"}
                    or any(not isinstance(review.get(key), str) or not review[key].strip()
                           for key in ("reviewer", "executor", "evidence", "observation"))
                    or review["reviewer"].strip().casefold() == review["executor"].strip().casefold()):
                raise ValueError(f"{micro_id}: parecer exige validador independente e evidência")
    return receipts


def render_task(task, json_link="task.json", receipts=None):
    lines = [
        f"# {task['task_id']} · {task['title']}",
        "",
        f"Revisão {task['contract_revision']} · {task['status']}",
    ]
    lines.extend(["",
                  "Coordenação: o agente principal usa a skill `TFD-harness` para coordenar e delegar as MTs conforme dependências, escopo e gates.",
                  "No Codex, o subagente `tfd_harness` é apenas de consulta/status; a delegação cabe ao agente principal.", "",
                  "Loop de implementação: execução e autotestes → QA independente → correções e nova revisão → PASS → aprovação humana."])
    if "sectors" in task:
        lines.extend(["", f"Agentes: abra o [JSON canônico]({json_link}) e execute somente sua rota e seus checklists."])
    if task.get("problem"):
        lines.extend(["", "## Problema", "", task["problem"]])
    lines.extend(["", "## Solução", "", task["goal"]])
    if "technical_coverage" in task:
        lines.extend(["", "## Cobertura técnica", "", "| Área | Estado | Resumo / justificativa | Evidências e aceite |",
                      "|---|---|---|---|"])
        for row in coverage_rows(task):
            lines.append("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ").replace("\r", " ")
                                         for value in row) + " |")
    lines.extend(["", '<a id="limites-globais"></a>', "## Limites globais", "",
                  "Fora do escopo: " + "; ".join(task["out_of_scope"]),
                  "Caminhos protegidos: " + (", ".join(f"`{path}`" for path in task["protected_paths"]) or "nenhum declarado")])
    if "sectors" in task:
        lines.extend(sector_lines(task, json_link, receipts or {}))
    else:
        lines.extend(["", "## O que será feito", ""])
        for micro in task["microtasks"]:
            lines.append(f"- **{micro['id']}** {micro['title']}")
            lines.extend(microtask_lines(micro, task))
    lines.extend(["", "Escopo, aceite e testes no contrato JSON desta task."])
    if not task.get("estimate"):
        lines.append("Estimativa pendente. G6 bloqueado para submissão.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("output", type=Path, nargs="?", help="defaults to the Markdown sibling of the JSON")
    parser.add_argument("--draft", action="store_true", help="allow a draft with a pending estimate")
    parser.add_argument("--require-coverage", action="store_true", help="require coverage v1 for new authoring")
    route = parser.add_mutually_exclusive_group()
    route.add_argument("--sector", help="print only the sector's execution context")
    route.add_argument("--workflow", type=Path, help="print the view with observed sector receipts")
    parser.add_argument("--microtask", help="limit --sector to one microtask ID")
    parser.add_argument("--measure", action="store_true", help="print route words and o200k_base tokens only")
    args = parser.parse_args()
    if (args.microtask or args.measure) and not args.sector:
        parser.error("--microtask and --measure require --sector")
    sibling = args.task.with_suffix(".md")
    if args.output is not None and args.output.absolute() != sibling.absolute():
        parser.error("update the existing Markdown sibling; alternate output paths create duplicates")
    args.output = sibling
    try:
        if args.output.resolve() == args.task.resolve() or (
            args.output.exists() and args.output.samefile(args.task)
        ):
            raise ValueError("the human view must use a different file from the canonical JSON")
        task = json.loads(args.task.read_text(encoding="utf-8"))
        errors = validate_task(task, allow_unestimated_draft=args.draft, require_coverage=args.require_coverage)
        if errors:
            raise ValueError("; ".join(errors))
        if args.sector:
            text = json.dumps(sector_context(task, args.sector, args.microtask), ensure_ascii=False,
                              separators=(",", ":")) + "\n"
            if args.measure:
                try:
                    encoding = load_encoding("o200k_base")
                    tokens = len(encoding.encode_ordinary(text))
                except (ImportError, AttributeError, OSError, ValueError) as exc:
                    print(f"Tokenizer unavailable: {exc}", file=sys.stderr)
                    tokens = None
                print(json.dumps({"words": len(WORDS.findall(text)), "tokens": tokens,
                                  "encoding": "o200k_base" if tokens is not None else None}))
                return 0 if tokens is not None else 3
            print(text, end="")
        elif args.workflow:
            workflow = json.loads(args.workflow.read_text(encoding="utf-8"))
            print(render_task(task, args.task.name, read_sector_receipts(task, workflow)), end="")
        else:
            args.output.write_text(render_task(task, args.task.name), encoding="utf-8", newline="\n")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
