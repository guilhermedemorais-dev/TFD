#!/usr/bin/env python3
"""CLI do TFD: plan, check e report sobre o contrato de task.

    python scripts/tfd.py plan   tasks/DEMO-001.json
    python scripts/tfd.py check  tasks/DEMO-001.json
    python scripts/tfd.py report tasks/DEMO-001.json

Sem LLM: valida contrato, confere escopo no diff, roda os testes e grava receipt.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from validate_task import validate_task

ROOT = Path.cwd()
DELIVERY = ROOT / "delivery"

IGNORED_DIRS = {"__pycache__", "node_modules", ".pytest_cache", ".git", "delivery"}
IGNORED_PREFIXES = ("tasks/", "delivery/", "specs/", ".tfd/")


class GitError(Exception):
    pass


def git(*args: str) -> str:
    command = " ".join(("git", *args))
    try:
        proc = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                              text=True, timeout=15)
    except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
        raise GitError(f"{command}: {exc}") from exc
    if proc.returncode != 0:
        raise GitError(f"{command} (exit {proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout.rstrip("\n")


def glob_to_regex(pattern: str) -> re.Pattern:
    escaped = re.escape(pattern)
    escaped = escaped.replace(r"\*\*/", r"(?:.*/)?").replace(r"\*\*", r".*")
    escaped = escaped.replace(r"\*", r"[^/]*")
    return re.compile("^" + escaped + "$")


def changed_paths() -> list[str]:
    out = git("status", "--porcelain")
    paths = []
    for line in out.splitlines():
        if not line.strip():
            continue
        raw = line[3:].strip()
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        path = raw.strip('"').replace("\\", "/")
        if path.endswith("/") or path.endswith(".pyc"):
            continue
        if path.startswith(IGNORED_PREFIXES):
            continue
        if any(part in IGNORED_DIRS for part in path.split("/")):
            continue
        paths.append(path)
    return sorted(set(paths))


def scope_violations(task: dict, paths: list[str]) -> list[dict]:
    allowed = task["allowed_paths"]
    protected = task.get("protected_paths", [])
    violations = []
    for path in paths:
        if any(glob_to_regex(p).match(path) for p in protected):
            violations.append({"path": path, "reason": "protected"})
        elif not any(glob_to_regex(p).match(path) for p in allowed):
            violations.append({"path": path, "reason": "outside_allowed_paths"})
    return violations


def load_task(path: str) -> dict:
    task = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = validate_task(task)
    if errors:
        for error in errors:
            print(f"ERRO {error}", file=sys.stderr)
        raise SystemExit(2)
    return task


def cmd_plan(args: argparse.Namespace) -> int:
    task = load_task(args.task)
    estimate = task["estimate"]
    print(f"TASK {task['task_id']} · {task['complexity']} · {task['status']}")
    print(f"Objetivo: {task['goal']}")
    print("Escopo: " + "; ".join(task["scope"]))
    if task["out_of_scope"]:
        print("Fora: " + "; ".join(task["out_of_scope"]))
    print("Caminhos: " + ", ".join(task["allowed_paths"]))
    if task["protected_paths"]:
        print("Protegidos: " + ", ".join(task["protected_paths"]))
    print("Requisitos:")
    for req in task["requirements"]:
        print(f"- {req['id']} [{req['priority']}] {req['description']} ({req['source']})")
    print("Aceite:")
    for ac in task["acceptance_criteria"]:
        print(f"- {ac['id']} -> {ac['validation']}: {ac['description']}")
    print("Testes:")
    for test in task["required_tests"]:
        print(f"- {test['id']} ({test['type']}): {test['command']} | esperado: {test['expected']}")
    print("Microtasks:")
    for micro in task["microtasks"]:
        deps = f" após {', '.join(micro.get('depends_on', []))}" if micro.get("depends_on") else ""
        print(f"- {micro['id']} {micro['title']} · owner {micro['owner']} · valida {micro['validator']}{deps}")
    print(f"Estimativa: {estimate['optimistic_h']}/{estimate['likely_h']}/"
          f"{estimate['pessimistic_h']}h · confiança {estimate['confidence']}")
    print("Parar se: " + "; ".join(task["stop_conditions"]))
    return 0


def _run(command: str, timeout: int) -> dict:
    started = time.perf_counter()
    try:
        proc = subprocess.run(command, shell=True, cwd=ROOT, capture_output=True,
                              text=True, timeout=timeout)
        code, output = proc.returncode, proc.stdout + proc.stderr
    except subprocess.TimeoutExpired:
        code, output = 124, f"timeout após {timeout}s"
    return {"command": command, "exit": code,
            "seconds": round(time.perf_counter() - started, 2),
            "tail": "\n".join(output.strip().splitlines()[-20:])}


def cmd_check(args: argparse.Namespace) -> int:
    task = load_task(args.task)
    scope_error = None
    try:
        paths = args.path or changed_paths()
    except GitError as exc:
        paths = []
        scope_error = str(exc)
        print(f"[ESCOPO] NÃO VERIFICADO: {scope_error}", file=sys.stderr)
    violations = scope_violations(task, paths)

    results = []
    for test in task["required_tests"]:
        result = _run(test["command"], args.timeout)
        result["id"] = test["id"]
        results.append(result)
        print(f"[{'PASS' if result['exit'] == 0 else 'FAIL'}] {test['id']}: {test['command']}")

    passed = scope_error is None and not violations and all(r["exit"] == 0 for r in results)
    commit = None
    if scope_error is None:
        try:
            commit = git("rev-parse", "--short", "HEAD") or None
        except GitError:
            pass  # O commit é metadado opcional, inclusive antes do primeiro commit.
    scope = {"changed": paths, "violations": violations}
    if scope_error is not None:
        scope["error"] = scope_error
    receipt = {
        "task_id": task["task_id"],
        "contract_revision": task["contract_revision"],
        "when": datetime.now().isoformat(timespec="seconds"),
        "commit": commit,
        "complexity": task["complexity"],
        "result": "PASSED" if passed else "FAILED",
        "scope": scope,
        "tests": results,
        "limits": "Execução local; não prova deploy, integração externa nem aceite humano.",
    }
    DELIVERY.mkdir(exist_ok=True)
    (DELIVERY / "receipts").mkdir(exist_ok=True)
    out = DELIVERY / "receipts" / f"{task['task_id']}.json"
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")

    for violation in violations:
        print(f"[ESCOPO] {violation['reason']}: {violation['path']}")
    print(f"receipt: {out} · {receipt['result']}")
    return 0 if passed else 1


def cmd_report(args: argparse.Namespace) -> int:
    task = load_task(args.task)
    receipt_path = DELIVERY / "receipts" / f"{task['task_id']}.json"
    deferred = DELIVERY / "deferred.md"

    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        rows = "\n".join(
            f"| {t['id']} | `{t['command']}` | {t['exit']} |" for t in receipt["tests"])
        verification = (f"Executado em {receipt['when']}, commit `{receipt['commit'] or 'n/a'}`. "
                        f"Resultado: **{receipt['result']}**.\n\n"
                        f"| Teste | Comando | Exit |\n|---|---|---|\n{rows}")
        scope_error = receipt["scope"].get("error")
        if scope_error:
            scope = f"- **Escopo não verificado.** {scope_error}"
        else:
            scope = "\n".join(f"- {v['reason']}: `{v['path']}`" for v in receipt["scope"]["violations"])
    else:
        verification = "**NÃO VERIFICADO.** Rode `check` antes de entregar."
        scope = "- sem receipt"

    deferred_text = deferred.read_text(encoding="utf-8", errors="ignore") \
        if deferred.exists() else "_Nada registrado._"

    text = f"""# Entrega — {task['task_id']}

## Objetivo

{task['goal']}

## Verificação

{verification}

## Violações de escopo

{scope or '- nenhuma'}

## Escopo adiado

{deferred_text}

## Como rodar

{chr(10).join(f'- `{t["command"]}`' for t in task['required_tests'])}

## Rollback

- `git revert <commit>` ou checkout da tag anterior.
- Dados: restaurar o backup anterior à migração.
"""
    DELIVERY.mkdir(exist_ok=True)
    out = DELIVERY / f"ENTREGA-{task['task_id']}.md"
    out.write_text(text, encoding="utf-8")
    print(f"entrega: {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tfd", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="imprime o brief do contrato")
    plan.add_argument("task")
    plan.set_defaults(func=cmd_plan)

    check = sub.add_parser("check", help="escopo + testes + receipt")
    check.add_argument("task")
    check.add_argument("--path", action="append", default=None)
    check.add_argument("--timeout", type=int, default=900)
    check.set_defaults(func=cmd_check)

    report = sub.add_parser("report", help="gera o handover")
    report.add_argument("task")
    report.set_defaults(func=cmd_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
