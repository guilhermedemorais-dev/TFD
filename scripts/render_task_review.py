"""Render a human review from the canonical TFD task and optional workflow."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

from pipeline import evaluate, require_file
from render_task import read_sector_receipts
from resume_task import load_checkpoint
from validate_task import validate_task


APPROVAL_CHECKS = (
    "Conferi a revisão da Task, da spec e do Discovery.",
    "Conferi o QA independente e as evidências aplicáveis a esta revisão.",
    "Revisei as microtarefas, os responsáveis, as dependências e os entregáveis.",
    "Conferi os critérios de aceite, as regras de negócio e os testes previstos.",
    "Conferi os caminhos permitidos, as restrições e as condições de parada.",
    "Identifiquei as pendências que afetam meu aceite.",
)
FLOW = """```mermaid
flowchart LR
    A[Entrega] --> B[QA independente]
    B -->|PASS| C[Revisão humana]
    B -->|REWORK| D[Correção]
    C -->|Ajustes| D
    D --> B
    C -->|Aceite| E[Registrar na Issue]
```"""


def escape(value):
    return html.escape(str(value))


def paragraph(label, value):
    return f"<p><strong>{escape(label)}</strong> · {escape(value)}</p>"


def list_field(label, items):
    entries = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<p><strong>{escape(label)}</strong></p><ul>{entries}</ul>" if entries else paragraph(label, "Nenhum registrado.")


def details(title, body, *, expanded=False):
    state = " open" if expanded else ""
    return f"<details{state}>\n<summary>{escape(title)}</summary>\n\n{body}\n\n</details>"


def checklist(items, markdown, *, verdict=False):
    if markdown:
        # Keep source text literal, including Markdown syntax and mentions.
        def item_text(item):
            text = escape(" ".join(item.splitlines()))
            return "".join(f"&#{ord(ch)};" if ch in "\\`*_[]~@!" else ch for ch in text)

        return "\n" + "\n".join(f"- [ ] {item_text(item)}" for item in items) + "\n"
    group = " data-verdicts" if verdict else ""
    return f"<ul class=checklist{group}>" + "".join(
        f'<li><label><input type="checkbox"> <span>{escape(item)}</span></label></li>' for item in items
    ) + "</ul>"


def verified_evidence(root, path):
    content = require_file(path, root).read_bytes()
    if not content.strip():
        raise ValueError(f"evidência vazia: {path}")
    return content


def workflow_observations(task, task_file, task_hash, workflow, root, log):
    """Bind observed results to the current submitted bytes and valid ledger."""
    if not workflow.is_relative_to(root):
        raise ValueError("o workflow deve estar dentro da pasta do projeto")
    status = evaluate(log, root)
    if not isinstance(log.get("sector_receipts", {}), dict):
        raise ValueError("recibos por setor devem formar um objeto")
    events = log["events"]
    submissions = [e for e in events if (e["gate"], e["action"]) == ("G6", "submit")]
    identity = (task["task_id"], task["contract_revision"], task_hash)
    if not submissions:
        if log.get("sector_receipts"):
            raise ValueError("recibos requerem uma submissão G6 da Task")
        return {}, {}, []

    def matches_task(submission):
        return identity == (submission["task_id"], submission["contract_revision"], submission["sha256"]["task"])

    latest = submissions[-1]
    if not matches_task(latest) or require_file(latest["artifacts"]["task"], root) != task_file:
        raise ValueError("o workflow não corresponde ao arquivo e à revisão da Task submetida")

    phase_submissions = {e["phase"]: e for e in submissions}
    phases = {phase: e for phase, e in phase_submissions.items() if matches_task(e)}
    gate_reviews = []
    checkpoints = {}
    invalidated = {}
    phase_attempts = {}
    for phase, submitted in phases.items():
        implementation = [e for e in events if e["gate"] == "G7" and e.get("phase") == phase]
        gate_reviews.extend(e for e in events if e["gate"] == "G6" and e.get("phase") == phase
                            and e["revision"] == submitted["revision"] and e["action"] == "review")
        attempts = [e for e in implementation if e["action"] == "submit"]
        if attempts:
            gate_reviews.extend(e for e in implementation if e["action"] == "review"
                                and e["revision"] == attempts[-1]["revision"])
        attempt = len(attempts)
        if status.get("gate") == "G7" and status.get("phase") == phase and status["status"] in {
            "AWAITING_SUBMISSION", "REWORK"
        }:
            attempt += 1
        phase_attempts[phase] = attempt
        micros = {m["id"]: m for m in task["microtasks"] if m.get("phase") == phase}
        if not attempt or not micros:
            continue
        binding = {"task_id": task["task_id"], "contract_revision": task["contract_revision"],
                   "phase": phase, "attempt": attempt, "task_sha256": task_hash}
        key = hashlib.sha256(json.dumps(binding, sort_keys=True).encode()).hexdigest()[:24]
        path = workflow.with_name(workflow.stem + "-execution") / (key + ".json")
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError("checkpoint fora da pasta do projeto")
        checkpoint = load_checkpoint(path, binding, micros, root)
        checkpoints.update(checkpoint["items"])
        invalidated.update(checkpoint["invalidated"])

    reviews = {}
    if log.get("sector_receipts"):
        receipts = read_sector_receipts(task, log)
        micro_phases = {m["id"]: m["phase"] for m in task["microtasks"]}
        for receipt in receipts.values():
            for micro, review in receipt.get("reviews", {}).items():
                phase = micro_phases[micro]
                if phase not in phases:
                    raise ValueError(f"{micro}: recibo sem submissão G6 desta revisão")
                number = review.get("attempt", 1)
                if type(number) is not int or not 1 <= number <= phase_attempts[phase]:
                    raise ValueError(f"{micro}: tentativa inválida no recibo de QA")
                evidence = verified_evidence(root, review["evidence"])
                fingerprint = hashlib.sha256(json.dumps(review, sort_keys=True).encode() + evidence).hexdigest()
                if invalidated.get(micro) != fingerprint:
                    reviews[micro] = review
    for review in gate_reviews:
        verified_evidence(root, review["evidence"])
    return reviews, checkpoints, gate_reviews


def contract(task):
    parts = [paragraph("Objetivo", task["goal"]), paragraph("Complexidade", task["complexity"])]
    for field, label in (("problem", "Problema"), ("spec", "Especificação")):
        if task.get(field):
            parts.append(paragraph(label, task[field]))
    for field, label in (("scope", "Escopo"), ("out_of_scope", "Fora do escopo"),
                         ("allowed_paths", "Caminhos permitidos na Task"), ("protected_paths", "Caminhos protegidos"),
                         ("stop_conditions", "Condições de parada")):
        parts.append(list_field(label, task[field]))
    parts.append(list_field("Gates", [f"{key} · {value}" for key, value in task["gates"].items()]))
    if "estimate" in task:
        estimate = task["estimate"]
        parts.append(paragraph("Estimativa", f"{estimate['optimistic_h']} / {estimate['likely_h']} / "
                               f"{estimate['pessimistic_h']} h (otimista / provável / pessimista) · "
                               f"{estimate['confidence']} · {estimate['basis']}"))
    else:
        parts.append(paragraph("Estimativa", "Pendente no rascunho."))
    for sector in task.get("sectors", {}).values():
        reason = f" · {sector['reason']}" if sector.get("reason") else ""
        parts.append(paragraph("Setor", f"{sector['label']} · {sector['owner']} · {sector['applicability']}{reason}"))
    return details("Escopo, restrições e fases", "\n".join(parts))


def technical_contract(task):
    parts = [list_field("Requisitos", [f"{r['id']} · {r['description']} · {r['priority']} · {r['source']}"
                                     for r in task["requirements"]]),
             list_field("Regras de negócio", [f"{r['id']} · {r['description']} · {r['source']}"
                                              for r in task["business_rules"]]),
             list_field("Critérios de aceite", [f"{ac['id']} · {ac['description']} · "
                                               f"{', '.join(ac['requirement_ids'])} · {ac['validation']} · "
                                               f"{', '.join(ac['microtask_ids'])}" for ac in task["acceptance_criteria"]])]
    for test in task["required_tests"]:
        parts.extend((paragraph(test["id"], test["type"]), paragraph("Comando ou procedimento", test["command"]),
                      paragraph("Resultado esperado", test["expected"])))
    if task["references"]:
        parts.append("<h3>Referências técnicas</h3><ul>" + "".join(
            f"<li>{escape(ref['id'])} · {reference_location(ref['path'])} · {escape(ref['purpose'])}</li>"
            for ref in task["references"]
        ) + "</ul>")
    else:
        parts.append(paragraph("Referências técnicas", "Nenhuma registrada."))
    return details("Regras, critérios, testes e referências técnicas", "\n".join(parts))


def reference_location(location):
    try:
        url = urlsplit(location)
    except ValueError:
        return escape(location)
    if url.scheme in {"https", "http"} and url.hostname and url.username is None and not any(
        char.isspace() or ord(char) < 32 for char in location
    ):
        return f'<a href="{escape(location)}">{escape(location)}</a>'
    return escape(location)


def microtask_view(micro, task, markdown, review, checkpoint):
    micro_id = micro["id"]
    parts = [paragraph("Decisão humana · marque uma opção", ""),
             checklist(("Aprovado", "Reprovado"), markdown, verdict=True),
             paragraph("Responsável e validador independente", f"@{micro['owner']} · @{micro['validator']}"),
             paragraph("Depende de", ", ".join(micro.get("depends_on", [])) or "livre"),
             list_field("Caminhos permitidos", micro["allowed_paths"]),
             paragraph("Não pode", "Editar fora da lista da microtarefa ou em caminhos protegidos, ampliar o escopo ou contornar gates. Consulte Escopo, restrições e fases."),
             paragraph("Checklist de execução", ""), checklist(micro["checklist"], markdown),
             list_field("Entregáveis", micro["deliverables"]), paragraph("Concluído quando", micro["completion_condition"])]
    criteria = [ac for ac in task["acceptance_criteria"] if micro_id in ac["microtask_ids"]]
    parts.append(list_field("Critérios, testes e requisitos vinculados", [f"{ac['id']} · {ac['validation']} · "
                                                                        f"{', '.join(ac['requirement_ids'])}"
                                                                        for ac in criteria]))
    parts.append(paragraph("Referências da microtarefa", ", ".join(micro.get("reference_ids", []))
                           or "Consulte as referências da Task."))
    if checkpoint:
        parts.append(list_field("Checkpoint de execução", [
            f"Item {index} · verificado · {item['evidence']}" if item["status"] == "verified" else f"Item {index} · iniciado"
            for index, item in enumerate(checkpoint, 1)
        ]))
    else:
        parts.append(paragraph("Checkpoint de execução", "Sem registro nesta visão."))
    if review:
        parts.append(paragraph("QA independente", f"{review['verdict']} · {review['role']} · "
                               f"tentativa {review.get('attempt', 1)} · {review['observation']}"))
        parts.append(paragraph("Evidência do QA", review["evidence"]))
    else:
        parts.append(paragraph("QA independente", "Sem parecer de execução nesta visão."))
    sector = task.get("sectors", {}).get(micro.get("sector"), {}).get("label")
    label = f"{micro_id} · {micro['title']}" + (f" · {sector}" if sector else "")
    return details(label, "\n".join(parts))


def render_review_body(task, task_hash, observations, *, markdown, task_name="task.json"):
    reviews, checkpoints, gate_reviews = observations
    if markdown:
        flow = FLOW
    else:
        flow = """<figure class="flow"><figcaption>Fluxo da revisão</figcaption>
<ol class="flow-steps"><li>Entrega</li><li>QA independente</li><li>Revisão humana</li><li>Registro na Issue</li></ol>
<div class="flow-loop"><span>QA pede correção ou o revisor solicita ajustes</span><span aria-hidden="true">→</span>
<span>Corrigir</span><span aria-hidden="true">→</span><span>Retomar QA</span></div></figure>"""
    gate_evidence = [f"{e['gate']} · {e['phase']} · {e['revision']} · {e['reviewer']} · {e['verdict']} · {e['evidence']}"
                     for e in gate_reviews]
    sections = [f"<h1>{escape(task['task_id'])} · {escape(task['title'])}</h1>",
                paragraph("Revisão", f"r{task['contract_revision']} · {task['status']}"),
                paragraph("JSON canônico", task_name),
                paragraph("SHA-256 do JSON", task_hash),
                details("Checklist para aprovar a Task", "\n".join((
                    "<p>Registre o aceite ou os ajustes na Issue vinculada e identifique a revisão.</p>",
                    checklist(APPROVAL_CHECKS, markdown), flow,
                )), expanded=True),
                details("Pareceres e evidências da revisão", list_field("QA registrado no workflow", gate_evidence)),
                contract(task), technical_contract(task)]
    micros = task["microtasks"]
    phases = task.get("phases") or [{"id": None, "title": "Microtarefas"}]
    for phase in phases:
        body = [f"<p>{escape(phase['note'])}</p>"] if phase.get("note") else []
        body.extend(microtask_view(m, task, markdown, reviews.get(m["id"]), checkpoints.get(m["id"]))
                    for m in micros if not phase["id"] or m["phase"] == phase["id"])
        title = f"{phase['id']} · {phase['title']}" if phase["id"] else phase["title"]
        sections.append(details(title, "\n\n".join(body), expanded=True))
    return ("\n\n".join(sections) + "\n").replace("\r\n", "\n").replace("\r", "\n")


def render_review_html(task, task_hash, observations, *, task_name="task.json"):
    markdown = render_review_body(task, task_hash, observations, markdown=True, task_name=task_name)
    body = render_review_body(task, task_hash, observations, markdown=False, task_name=task_name)
    return ("<!doctype html>\n<html lang=pt-BR>\n<head><meta charset=utf-8>\n"
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f"<title>{escape(task['task_id'])} · Revisão humana</title>\n"
            "<style>\n"
            ":root{color-scheme:light dark;font-family:system-ui,sans-serif;line-height:1.55}\n"
            "body{max-width:72rem;margin:1rem auto;padding:0 1rem;overflow-wrap:anywhere}\n"
            "details{margin:.6rem 0;padding:.55rem .75rem;border:1px solid color-mix(in srgb,currentColor 24%,transparent);border-radius:.4rem}\n"
            "summary{font-weight:600;cursor:pointer} .checklist{padding-inline-start:.5rem;list-style:none}\n"
            "label{display:inline-flex;align-items:baseline;gap:.35rem}\n"
            ".flow{margin:1rem 0}.flow figcaption{font-weight:600}\n"
            ".flow-steps,.flow-loop{display:flex;align-items:center;flex-wrap:wrap;gap:.5rem;padding:0}\n"
            ".flow-steps{list-style:none}.flow-steps li{padding:.2rem .55rem;border:1px solid color-mix(in srgb,currentColor 30%,transparent);border-radius:.35rem}\n"
            ".flow-steps li+li::before{content:'→';margin-inline-end:.35rem}\n"
            "#markdown{box-sizing:border-box;width:100%;min-height:8rem} #copy-status{margin-inline-start:.6rem}\n"
            "</style></head>\n<body><main>\n"
            '<button id="copy-markdown" type="button">Copiar Markdown</button>'
            '<span id="copy-status" role="status"></span>\n'
            f'<textarea id="markdown" aria-label="Markdown da revisão" readonly hidden>{escape(markdown)}</textarea>\n'
            f"{body}</main>\n"
            """<script>
const source = document.getElementById('markdown');
const status = document.getElementById('copy-status');
document.getElementById('copy-markdown').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(source.value);
    source.hidden = true;
    status.textContent = 'Markdown copiado.';
  } catch {
    source.hidden = false;
    source.focus();
    source.select();
    status.textContent = 'Markdown selecionado. Pressione Ctrl+C ou ⌘C para copiar.';
  }
});
for (const group of document.querySelectorAll('[data-verdicts]')) {
  group.addEventListener('change', event => {
    if (!event.target.checked) return;
    for (const box of group.querySelectorAll('input')) {
      if (box !== event.target) box.checked = false;
    }
  });
}
</script>
</body></html>
""")


def reject_source_output(output, paths):
    for path in paths:
        if output == path or (output.exists() and path.exists() and output.samefile(path)):
            raise ValueError("use um arquivo separado da Task canônica, da vista de G6, do workflow e das evidências")


def ledger_files(log, observations, root):
    _, checkpoints, _ = observations
    if "preparation" in log:
        yield require_file(log["preparation"]["authorization"], root)
    for event in log["events"]:
        if event["action"] == "submit":
            yield from ((root / path).resolve() for path in event["artifacts"].values())
        else:
            yield require_file(event["evidence"], root)
    for receipt in log.get("sector_receipts", {}).values():
        for review in receipt.get("reviews", {}).values():
            yield require_file(review["evidence"], root)
        if receipt.get("total_tokens") is not None:
            yield require_file(receipt["token_receipt"], root)
    for items in checkpoints.values():
        yield from (require_file(item["evidence"], root) for item in items if item["status"] == "verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path)
    parser.add_argument("output", type=Path, help="review Markdown (.md) or standalone HTML (.html)")
    parser.add_argument("--workflow", type=Path)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        task_file = args.task.resolve(strict=True)
        output = args.output.resolve()
        workflow = args.workflow.resolve(strict=True) if args.workflow else None
        protected = [task_file, args.task.with_suffix(".md").resolve(), task_file.with_suffix(".md").resolve()]
        if workflow:
            protected.append(workflow)
        reject_source_output(output, protected)
        if output.suffix.lower() not in {".md", ".html"}:
            raise ValueError("a saída deve ter extensão .md ou .html")
        contents = task_file.read_bytes()
        task = json.loads(contents)
        errors = validate_task(task, allow_unestimated_draft=True)
        if errors:
            raise ValueError("; ".join(errors))
        digest = hashlib.sha256(contents).hexdigest()
        observations = {}, {}, []
        if workflow:
            root = args.project_root.resolve(strict=True)
            log = json.loads(workflow.read_bytes())
            observations = workflow_observations(task, task_file, digest, workflow, root, log)
            reject_source_output(output, ledger_files(log, observations, root))
        text = (render_review_html(task, digest, observations, task_name=task_file.name) if output.suffix.lower() == ".html"
                else render_review_body(task, digest, observations, markdown=True, task_name=task_file.name))
        output.write_text(text, encoding="utf-8", newline="\n")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
