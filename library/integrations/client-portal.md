# Portal do Cliente, inspected integration

Source: https://github.com/guilhermedemorais-dev/portal-clientes
Pinned source commit: `82226fbb2385639d7812b2de929b435e6480fbbc`.
Inspected 2026-10-21: README, package manifests, source, OpenAPI, domain and
sync-template code. Source available; native deployment/OAuth/API integration
with a customer project NOT_VALIDATED. The frozen V1 `client-portal.md` reference
predates this inspection: its "source pending" statement is superseded here.
The source is a React/TypeScript/Vite frontend plus reference Fastify/PostgreSQL
backend, not a single standalone HTML dashboard. Do not copy it into the Harness.

## Reuse

Respect the original preparation/security rules in
`plugins/dev-workflow-standard/skills/dev-workflow-standard/references/client-portal.md`
with the updated source facts here. Prepare in the **client project's**
`docs/portal/`, only when selected for that project. Use pinned checkout and the
existing `scripts/sync-template.mjs --project=CLIENT_ROOT` dry run, inspect diff,
then its scoped `--apply` when authorized. Preserve customizations and conflicts.
The script's allowlist currently omits root workflow files, backend/openapi.yaml
and backend/docker-compose.yml; review the actual output instead of assuming a
complete install. Do not copy a database or provision infrastructure by default.

Known frontend checks: `npm run typecheck`, `npm test`, `npm run test:template`,
`npm run build`. They are source-defined commands, not tests executed in this
Harness integration. Backend/auth/storage and Pages configuration remain separate.

## Existing API, preparation only

- GET `/v1/projects/{projectId}/dashboard`: task counts/stages and
  `done / eligible * 100`; eligible excludes backlog. This is not weighted full
  baseline coverage and cannot stand for total delivery effort.
- POST `/v1/projects/{projectId}/tasks`: owner-only upsert with `issueNumber`,
  `issueUrl`, `title`, `description`, `stage`, `status` and `progress` integer 0..100.
  Allowed status: backlog/in_progress/blocked/done. Issue must belong to configured
  GitHub repository. Map validated full Task closure to done only after actual
  canonical completion, never merely local closure-ready.
- Source comments can be synchronized through existing owner API with explicit
  client approval marker. It is not authorization to expose raw execution logs.

`delivery_report.py --format portal` prepares task payloads and metric caveats
without contacting the backend. Its local closure-ready does not set done; use
in_progress until canonical Done has been independently confirmed. Review the
payload, obtain existing publication authorization, then use a project-approved
API tool and verify response/read-back. No automatic export of private docs.
There is no running synchronization worker in this bundle.

## Remaining gap

The current dashboard excludes backlog from its total. A portal change to render
whole-approved-baseline coverage would need its own scoped Task in portal-clientes,
API/version review and tests. This integration deliberately reports the gap and
prepares compatible existing payloads, without changing that external project.

## Client docs destination, owner clarification

The installed template belongs to `CLIENT_ROOT/docs/portal/`, inside that client's
docs tree. Link the portal from the project's existing docs home/navigation using
its actual renderer/routes, preserving technical docs and manuals alongside it.
Do not assume the filesystem directory creates a served `/docs/portal/` URL;
verify the chosen renderer/build/base path. Reports and tutorials are maintained
in the same client's versioned docs tree, with access appropriate to their audience.
The Harness catalogs the source/procedure only. Never put a client's portal,
customer payloads or generated reports in the shared Harness or another project.

Procedure for owner-approved fetching and preparation: `docs/operations/client-portal.md`.
The responsible sector performs the existing sync, not a newly invented installer.
