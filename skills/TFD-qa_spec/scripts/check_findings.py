"""Valida o findings.json do setor qa_spec do TFD.

Uso: python skills/TFD-qa_spec/scripts/check_findings.py <findings.json>

Exit 0: válido. Exit 1: inválido. Exit 2: uso errado.
Só verifica forma e coerência; o julgamento dos achados é do revisor.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERDICTS = {"PASS", "REWORK"}
SEVERITIES = {"blocker", "major", "minor"}
BLOCKING = {"blocker", "major"}
TOP_KEYS = ("artifact", "revision", "verdict", "findings")
FINDING_KEYS = ("id", "severity", "dimension", "evidence", "recommendation")
ID_PATTERN = re.compile(r"^F-[0-9]{2,}$")


def _text(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def validate_findings(data: object) -> list[str]:
    """Retorna a lista de erros; lista vazia significa findings.json válido."""
    if not isinstance(data, dict):
        return ["raiz: esperado objeto JSON"]

    errors: list[str] = []
    for key in TOP_KEYS:
        if key not in data:
            errors.append(f"campo obrigatório ausente: {key}")
    for key in data:
        if key not in TOP_KEYS:
            errors.append(f"campo não permitido: {key}")

    for key in ("artifact", "revision"):
        if key in data and not _text(data[key]):
            errors.append(f"{key}: esperado texto não vazio")

    verdict = data.get("verdict")
    valid_verdict = isinstance(verdict, str) and verdict in VERDICTS
    if "verdict" in data and not valid_verdict:
        errors.append(f"verdict: esperado PASS ou REWORK, recebido {verdict!r}")

    findings = data.get("findings")
    findings_ok = isinstance(findings, list)
    if "findings" in data and not findings_ok:
        errors.append("findings: esperado lista")
    if not findings_ok:
        findings = []

    seen_ids: set[str] = set()
    severities: list[str] = []

    for index, item in enumerate(findings):
        label = f"findings[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: esperado objeto")
            continue

        for key in FINDING_KEYS:
            if key not in item:
                errors.append(f"{label}: campo obrigatório ausente: {key}")
        for key in item:
            if key not in FINDING_KEYS:
                errors.append(f"{label}: campo não permitido: {key}")

        finding_id = item.get("id")
        if not _text(finding_id):
            errors.append(f"{label}.id: esperado texto não vazio")
        elif not ID_PATTERN.match(finding_id):
            errors.append(f"{label}.id: esperado F-NN, recebido {finding_id!r}")
        elif finding_id in seen_ids:
            errors.append(f"{label}.id: duplicado: {finding_id}")
        else:
            seen_ids.add(finding_id)

        severity = item.get("severity")
        if not isinstance(severity, str) or severity not in SEVERITIES:
            errors.append(
                f"{label}.severity: esperado blocker, major ou minor, recebido {severity!r}"
            )
        else:
            severities.append(severity)

        dimension = item.get("dimension")
        if not _text(dimension):
            errors.append(f"{label}.dimension: esperado texto não vazio")

        evidence = item.get("evidence")
        if not _text(evidence):
            errors.append(f"{label}.evidence: esperado trecho citado não vazio")
        elif len(evidence.strip()) < 3:
            errors.append(f"{label}.evidence: trecho curto demais para citar")

        if not _text(item.get("recommendation")):
            errors.append(f"{label}.recommendation: esperado texto não vazio")

    if findings_ok and valid_verdict:
        blocking = [s for s in severities if s in BLOCKING]
        if verdict == "PASS" and blocking:
            errors.append(
                "verdict PASS incompatível com severidade blocker/major: "
                + ", ".join(blocking)
            )
        if verdict == "REWORK" and not blocking:
            errors.append("verdict REWORK exige ao menos um achado blocker ou major")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print(
            "uso: python skills/TFD-qa_spec/scripts/check_findings.py <findings.json>",
            file=sys.stderr,
        )
        return 2

    path = Path(argv[0])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERRO: não foi possível ler {path}: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERRO: JSON inválido em {path}: {exc}", file=sys.stderr)
        return 1

    errors = validate_findings(data)
    if errors:
        for error in errors:
            print(f"ERRO {error}")
        return 1
    print("OK: findings válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
