"""Render a human-readable task body from its canonical JSON."""

import argparse
import json
import sys
from pathlib import Path

from context_budget import WORDS, load_encoding
from validate_task import validate_task


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
    return {**context, "sector": sector, "phases": [phase for phase in task["phases"] if phase["id"] in phase_ids],
            "microtasks": microtasks, "acceptance_criteria": criteria,
            "requirements": [entry for entry in task["requirements"] if entry["id"] in reqs],
            "required_tests": [entry for entry in task["required_tests"] if entry["id"] in tests],
            "references": [entry for entry in task["references"] if entry["id"] in refs]}


def sector_lines(task, json_link, receipts):
    sectors = task["sectors"]
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
            lines.extend(f"  - {item}" for item in micro["checklist"])
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
    if "sectors" in task:
        lines.extend(["", f"Agentes: abra o [JSON canônico]({json_link}) e execute somente sua rota e seus checklists."])
    if task.get("problem"):
        lines.extend(["", "## Problema", "", task["problem"]])
    lines.extend(["", "## Solução", "", task["goal"]])
    if "sectors" in task:
        lines.extend(sector_lines(task, json_link, receipts or {}))
    else:
        lines.extend(["", "## O que será feito", ""])
        for micro in task["microtasks"]:
            lines.append(f"- {micro['title']} → {'; '.join(micro['deliverables'])}")
    lines.extend(["", "Escopo, aceite e testes no contrato JSON desta task."])
    if not task.get("estimate"):
        lines.append("Estimativa pendente. G6 bloqueado para submissão.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("output", type=Path, nargs="?", help="defaults to the Markdown sibling of the JSON")
    parser.add_argument("--draft", action="store_true", help="allow a draft with a pending estimate")
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
        errors = validate_task(task, allow_unestimated_draft=args.draft)
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
