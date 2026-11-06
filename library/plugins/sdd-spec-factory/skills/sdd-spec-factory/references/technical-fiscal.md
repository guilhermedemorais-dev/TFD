# Fiscal and regulated integrations

## When to consult
Use only for regulated documents, tax calculations, certificates or official
business reporting. SDD owns clarification; the accountant/domain owner owns
tax rules; Security, QA and DevOps retain their existing responsibilities.
This is a discovery/verification checklist, not tax or legal guidance.

## Nota fiscal scope clarified by the user
Focus on invoice issuance/integration, not a generic tax subsystem. For a
product e-commerce, NF-e is an ASSUMPTION until the owner confirms the actual
document model and operation. Evaluate NF-e, NFC-e or NFS-e only against the
competent authority and accountant's requirements; do not treat them as
interchangeable APIs or implement all models without an approved need.

For the selected model, discover applicable issuer/customer/item data,
number/series, access key, XML/schema, authorization protocol and printable
representation. Determine applicability of NCM, CFOP, CST/CSOSN, taxes and
other fields from official versioned rules and expert input, never fill them
from guessed defaults. Reuse existing fiscal provider/SDK before proposing
direct integration. A PDF/DANFE alone cannot serve as evidence that the selected
document was officially authorized; verify the applicable protocol/state.

## Required inputs and stop conditions
- Identify jurisdiction, competent authority, entity regime, document/model,
  operation, product classification and effective date with the accountable owner.
- Retrieve current official manuals, schemas, technical notes and environment
  endpoints. Record exact release/revision/effective dates and approved parameters.
  Do not derive rates, classifications or obligations from tutorials or AI recall.
- Inspect the project's provider, document lifecycle, numbering/key handling,
  certificate storage, immutable evidence and reconciliation routines.
- Unknown tax rules, conflicting official/owner instructions, absent required
  schemas or unexplained production/homologation differences are BLOCKED for
  that boundary. Continue independent safe work, without claiming fiscal approval.

## Decision questions
- Which transitions are allowed by this document/model and effective rules?
  Distinguish local draft, sent, uncertain transport outcome, official acceptance,
  rejection, cancellation and approved contingency. Names here are examples,
  not a replacement for the official protocol.
- Can an uncertain result be queried before resend? Specify protocol/key-based
  reconciliation; an HTTP timeout is not evidence that the document was rejected.
- Who approves tax parameters and rule changes, and where is that evidence?
- Which signing/certificate rules apply, how are secrets isolated/rotated, and
  how are audit/retention requirements established from current authority sources?
- What provider/schema compatibility and rollout gates prevent production use
  of a mock, obsolete schema or homologation credential?

## Verification example: fiscal document
Use synthetic fixtures approved for the applicable official homologation flow.
Validate a permitted document, schema rejection, an approved rejection case,
transport timeout after submission, duplicate attempt, status reconciliation,
certificate expiry and authorized cancellation/contingency when applicable.
Assert official protocol/status and absence of unintended duplicate issuance.
Mocks cover application error handling only; do not label them homologation.
Never issue/cancel a real production document during ordinary QA. Record expert
approval separately from technical tests; neither substitutes for the other.

## Source discovery
For Brazilian NF-e, start at the [official NF-e portal](https://www.nfe.fazenda.gov.br/portal/principal.aspx)
and follow the current manuals/schemas/technical notes for the actual model and
authority. Direct portal retrieval failed during this upgrade on 2026-10-11;
search verified its official landing-page metadata, not its manuals or schemas.
Its current documents and fiscal rules are NOT VERIFIED. For NFS-e, use the
[official current documentation](https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/documentacao-atual)
only when that model is approved. Search verified this index, not the contents
of its listed schemas/manuals. These pointers are discovery leads, not validated
fiscal rules. Resolve official sources in the client project before specifying
rules. Other jurisdictions need their own authority.
All scenario choices above are LOCAL TEST DESIGN awaiting domain-specific input.
