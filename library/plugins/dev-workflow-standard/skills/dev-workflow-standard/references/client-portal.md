# Client portal preparation

## Scope and ownership

Read when the Harness organizes a client project's directory structure or the
user requests portal preparation. This is an agent workflow, not an executable
installer. The portal application/template lives in a separate source repository,
not in the plugin bundle. Its repository does not need to exist to adopt this
rule. This plugin revision does not ship the portal application.

The user-designated template source is
`https://github.com/guilhermedemorais-dev/portal-clientes.git`.
This is the intended separate repository, not evidence that it already exists
or contains a usable template. Its creation and content are pending from the
user. Keep the revision unset until inspected; do not invent a branch, tag,
commit, template subdirectory or build command. A different source requires
an explicit project decision.

Use `docs/portal/` under the client project root. Do not install the portal
into the Harness repository, host plugin cache, or another client's project.
Confirm applicability during onboarding; reuse an existing decision instead of
asking on every Task. Do not add a portal to unrelated maintenance work.

Harness owns target, scope and handoff. DevOps owns approved template preparation
and CI/CD configuration; implementation owns application/backend adaptations.
Security reviews auth, secrets and customer-data boundaries; UI/UX and QA verify
the actual portal when available. Do not require a future Studio PRD skill to
exist before using this rule.

## Before the template exists

Within authorized project-structure preparation, create `docs/portal/` with a
short `README.md` only if absent. Record:

- purpose and destination;
- template repository: the designated URL above (availability not yet verified);
- template revision: not yet supplied;
- next action: await the user's template publication, then inspect its revision;
- portal not installed, built, configured or published.

Keep any existing README/content unchanged unless an explicit merge is approved.
Record operational pending evidence in the existing task/checkpoint, not in a
public artifact. Missing source is a pending dependency of the portal only,
not a reason to stop unrelated development or demand creation of the template.
If a delivery explicitly requires a working portal, its gate remains pending.

Never guess the source URL, use the personal portfolio as a substitute, create
the source repository, generate a replacement portal, or create a fake Pages
workflow while the template is unavailable. Do not request the source again
until the user provides it or resumes portal setup.

## Once the source is supplied

1. Confirm the client root and source repository; resolve the chosen revision
   to a commit. Inspect source instructions, manifest, build/output paths,
   dependency/lockfiles, license and required services before executing scripts.
2. Fetch into a separate temporary checkout using existing authorized Git
   access. No credentials in URLs or chat. Record repository, commit and selected
   template subdirectory; do not blindly track a moving branch.
3. Inspect `docs/portal/` before copying. Preview a file list/diff, preserve
   project customizations and stop on conflicts or symlinks escaping the target.
   Copy only the reviewed template contents, not its `.git`, secrets, local
   databases, uploads, dependency directories or unrelated repository files.
4. Configure project-specific public metadata and approved board/Issue links.
   Keep source provenance and installed revision in project documentation.
   Re-running the same preparation must not overwrite or duplicate an existing
   installation. Template upgrades require a reviewed diff, not a forced copy.
5. Use the template's verified build/test commands. Report missing prerequisites
   through Environment's existing selective preparation, not another installer.
   A successful copy is not proof of build, login, integration or deployment.

## GitHub Pages and client database

The requested `github.io` address serves the portal's static frontend. DevOps
must check current host capabilities/policies and the template's static-export
support before proposing Pages configuration. Next.js server routes or any
other server-only features do not run on Pages.

Use the client's existing database through an authorized backend/API, with
restricted access and approved schema/table changes. Database reuse does not
establish backend availability. No new database by default; no database files,
dumps, connection strings, OAuth secrets or private customer payloads in
`docs/portal/` or in a Pages artifact. GitHub login identifies users; backend
authorization must still enforce access to the correct client/project.

Do not protect private data merely by hiding static HTML behind a login button.
Only reviewed public shell/assets may be published; fetch private content from
an authenticated, authorized API. Client database/backend/OAuth configuration
can remain pending while the static frontend is prepared, but the full portal
cannot be called ready.

During the existing CI/CD workflow, propose a dedicated Pages build/artifact
from the verified portal output directory. Never publish the entire `docs/`
tree, PRD, internal planning, contracts, raw Issue comments or source credentials.
Check the repository Pages base path, assets/routes and existing deployment
configuration; do not replace another site. Reuse native commands and reviewed
actions with minimum permissions. Do not invent a working workflow until
template paths and commands are known.

Preparing local files is distinct from pushing, enabling Pages, configuring
OAuth, changing DNS or deploying. Apply remote changes only with the existing
target-specific approval gates. No custom domain is required merely to prepare
a `github.io` deployment. Report the actual URL only after verified publication.

## Evidence and acceptance

Use existing receipts/checkpoints, not a new global state machine. Distinguish
source pending, files prepared, build verified, backend/auth pending and actual
publication with evidence. Report changed paths, source commit, commands,
results and next action. Do not claim this rule updates already installed host
bundles automatically.

Review these scenarios before handoff:

| Situation | Expected behavior |
| --- | --- |
| Template not created yet | Prepare only the authorized destination note; record pending source and continue unrelated Tasks |
| User supplies repository later | Inspect and pin source, review copy, then prepare `docs/portal/` |
| Destination contains customized files | Preserve them; propose diff instead of overwrite |
| Template includes server-only features | No Pages-ready claim; route static/backend separation for approval |
| Database exists but no usable API | Reuse database decision; backend prerequisite remains pending |
| Local build succeeds | Report build evidence, not deployment or successful OAuth |
| Publication requested | Review artifact boundaries, permissions and existing site, then apply only authorized changes |
