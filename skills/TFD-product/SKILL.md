---
name: TFD-product
description: "Run the product briefing and write a sourced PRD. Use for product scope, briefing, or PRD requests. Route code fixes, technical design, data work, and deployment to their owners."
metadata:
  version: "1.4.0"
  owner: "product"
---

# Product briefing and PRD

Read the request, existing project docs, and available transcripts. Run the briefing even with fixed scope. Reuse answered questions and cite each decision's source.

Ask only unresolved material business questions; do not repeat answered blocks. Keep acceptance measurable and estimates qualified. Route technical uncertainties to Discovery using the [decision procedure](../../library/architecture/technical-decision-procedure.md); research cannot invent a business answer or approve G1.

## Briefing

Write `docs/prd/briefing.md`. Ask one block per round and resolve it before moving on.

1. **Problem and value.** Who has the problem, how do they handle it now, what proves it, and what happens if it persists?
2. **Users and flow.** Identify roles, the main journey from start to finish, and users who need extra guidance.
3. **Scope and constraints.** Define the minimum valuable release, exclusions, and deadlines, budget, or legal constraints that affect scope.
4. **Requirements and rules.** Capture invariants, inputs, calculations, outputs, errors to prevent, and what users see on failure.
5. **References.** Ask for supporting materials as needed. If the user names reference software, record its name, known version, access, and purpose for Discovery. Reference use does not authorize copying. Otherwise, optionally note "no reference software provided" and continue.
6. **Success and risks.** Define measurable outcomes, risks, impact, and mitigation.

Record answers with sources, cited materials, and open questions with owner, due date, and whether they block G1.

## PRD and G1

Write `docs/prd/prd.md` using [the PRD template](references/prd-template.md). Keep this order: problem, objectives, users, scope, out of scope, requirements, business rules, risks, success metrics, references, open questions.

- Give each verifiable requirement a `REQ-NN` ID, source, and MUST/SHOULD/MAY priority. Give each business rule a `RULE-NN` ID and source.
- Keep unanswered questions open. Never infer requirements, users, rules, or metrics. Give only a rough time range with assumptions.
- Check sourced answers and requirements, explicit exclusions, and stated or justified risks and metrics. Missing reference software does not block G1.
- Send the briefing and PRD to `TFD-qa_spec` for ambiguity, contradictions, gaps, testability, and traceability. Fix findings and resubmit. Reopen the briefing and increment the PRD version if the client changes scope.

Limit edits to `docs/prd/`. Leave architecture, stack, data models, APIs, detailed screens, implementation, and hour estimates to later stages. Never approve your own PRD.
