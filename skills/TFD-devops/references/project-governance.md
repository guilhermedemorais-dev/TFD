# Project governance contract

Use one contract in each project's records for work involving GitHub. DevOps drafts it during authorized setup. A request to verify, discuss or report permits only the requested review and report. Clarify an ambiguous target before inspecting it. Keep project drafting and settings changes within separately authorized scope.

## Record for G0.5

- **Revision and approval** — freeze the contract with its revision. Include the initial snapshot in the G0.5 submission as `artifacts.governance` with matching `sha256.governance`. Cite its path and the stable location of the active revision record in the environment report. Store the human decision separately as G0.5 approval evidence. After approval, link it and the frozen snapshot from the active record.
- **Actors** — verified host and active login or App installation for each actor. Record the CI identity where applicable. Keep credential values in the secret store.
- **Work and integration** — exact host, owner and name or URL for the working repository and integration destination. Record the source repository and branch and the destination repository and base branch. Verify each value independently, including for forks or multiple remotes.
- **Issue and Project** — exact Issues repository, linked Issue URL or number when known, and Project owner type, owner, number and verified node ID. Record the approved deployment provider, account and environment when applicable. Use `N/A` with a reason for resources outside scope.

Use explicitly identified targets. A similar name, default branch, remote name or Project title alone cannot establish a relationship. If identity or target differs from the contract, ask the human about the affected operation before probing another destination or suggesting access changes.

## Operation matrix

Create one row per operation. Fill in **exact target**, **responsible actor**, **explicit authorization evidence and limits**, and **observed permission with date and evidence**. Use `PENDING`, `DENIED` or `N/A` with a reason when applicable. For recurring authorization, record the permitted scope and conditions. Split actions when their permissions or authorizations differ.

| Operation | Target to bind |
| --- | --- |
| Edit Kanban or Project configuration | Exact Project and permitted fields or actions |
| Create Issues | Exact Issues repository and authorized scope |
| Manage or apply labels | Issues repository and Issue when applicable |
| Comment or record QA evidence | Same linked Issue |
| Create commit | Working repository and branch |
| Push commits | Destination remote and branch |
| Open PR | Source repository/branch and destination repository/base |
| Review PR or code | Exact PR or code revision and reviewer role |
| Merge PR | Exact PR, reviewed revision and destination branch |
| Deploy | Provider, account, environment and approved artifact or revision |

Example for a human-owned release. Agents prepare and verify the delivery. The human reviews code locally, opens the PR and merges after approval and branch checks. Assign a separate authorized PR reviewer where required. The coordinator updates the board within the recorded authorization. Confirm assignments per project.

## Use and maintain

Before an operation, verify that the actor and target match, the permission is evidenced for that resource and action, the authorization is explicit, and applicable gates are satisfied. Repository roles and Project access require separate evidence. A successful read proves only that read. The contract records decisions and does not grant authority. For a denied or uncertain operation, record what failed and a bounded next action. Continue unrelated authorized work. Keep QA in its work phase until all applicable independent reviewers pass the current revision. Where the board requires linked Issue evidence, keep QA evidence local if Issue writes are denied and hold only the remote sync and dependent move to Human Review.

Keep an active revision record in the project governance ledger or `docs/governance/active.md`. Follow the path recorded at G0.5. Verify its snapshot path, revision, SHA-256 and matching human acceptance. A draft stays pending. For a change, propose the diff and save a new snapshot. Update the active revision record after human acceptance and keep prior snapshots, hashes and approvals intact. Existing projects may link the active record in their local handoff or ledger before their next governed operation. Preserve their historical G0.5 evidence.

[Repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) · [Project access](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-access-to-your-projects) · [Issue labels](https://docs.github.com/en/rest/issues/labels)
