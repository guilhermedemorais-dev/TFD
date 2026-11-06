# Evidence-based technical decisions

Use for a material choice or diagnosed failure in any technology domain:
architecture, stack, API/protocol, data, dependencies, UI, security, QA or operations.
Do not repeat research for a typo or an unchanged, already-verified decision.

## Decision sequence

1. Read the approved PRD/spec/ADR and the affected implementation, configuration,
   lockfiles and tests. Identify the actual requirement, current version, relevant
   constraints, affected consumers and failure evidence. Existing broken behavior
   is evidence, not authority to override an approved requirement.
2. Reuse project reference records if their version, scope and claims remain
   applicable. Otherwise use the technical-knowledge-router topic and existing
   API/backend/UI source indexes. Read original version-matched vendor docs or
   protocol specifications for the unresolved claim. A catalog/search snippet
   does not prove consultation, correctness or runtime availability.
3. Compare the smallest compatible solution with meaningful alternatives. Ask
   whether existing code/configuration already provides it. Check compatibility,
   resource/cost implications, security, lifecycle and rollback. Do not introduce
   a service, framework, module layout or dependency merely because a guide uses it.
4. Record one short rationale in existing Task/ADR/research/receipt fields:
   requirement and affected paths; decision and rejected alternative; original
   source/version/section; why applicable; positive/negative validation; limitations.
   Classify source facts, LOCAL DECISION and ASSUMPTION separately. Link that record
   at handoff instead of copying documentation into every prompt.
5. Execute reversible technical details within the approved scope autonomously.
   A material scope/security/architecture change still needs its existing gate.
   If approval is required, present diagnosis, options, consequences and a concrete
   recommendation before the question. Do not ask the owner to resolve a technical
   fact that available documentation, code or a safe experiment can determine.
6. Validate the actual result against the requirement, source claim and affected
   consumers. A reference, generated plan, scanner PASS or cached answer is not
   implementation evidence. Record failures and rework, not merely successful runs.

If a required source is unavailable, mark NOT VERIFIED. Continue independent work;
block only the affected decision when its correctness depends on that source.
Approved specs may identify an implementation bug without a new business decision.
Escalate unresolved normative contradictions; never silently change the PRD.

## Completion and recovery

Use the existing requirement → microtask → acceptance → execution-evidence map.
For each applicable criterion require a current result and its actual owner;
report unmet, blocked and unvalidated criteria explicitly. Compare changed paths,
interfaces, dependencies and operational resources against the approved scope.
This applies beyond Compose. Investigate unexpected changes before proceeding;
never increase resources, weaken validation or alter architecture to hide drift.

On failure capture the failing observation, form a testable hypothesis and choose
a bounded check before editing again. Respect the Harness retry limit; a repeated
unchanged permission failure or an exhausted budget is a blocker, not another
attempt. No self-certified independent review or automatic merge/deploy.

This is a local agent procedure using existing schemas and evidence. It is not
a runtime permission firewall or a guarantee that a model will follow instructions.
