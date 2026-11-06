# Preventive security research

Use during Discovery/SDD when dependencies are selected/changed or security
boundaries require planning. Security owns applicability and control design;
SDD incorporates approved requirements into the existing module Task and
equivalent JSON. Do not create another audit pipeline, MCP registry or Task.

## Sources and routing

| Question | Primary source | Coverage limit |
| --- | --- | --- |
| Is a specific open-source package/version affected? | [OSV.dev](https://osv.dev) and the original advisory | Known indexed dependency vulnerabilities, not every software flaw |
| What control must our application enforce? | [OWASP ASVS](https://owasp.org/projects/asvs), applicable framework docs and project threat model | Select relevant controls; a generic checklist is not project evidence |

Follow the active Harness research routing and inspect actual host capability
availability. Prefer a suitable available advisory capability, otherwise the
official OSV website/API through an authorized HTTP tool. OSV is an advisory
source/API, not an asserted installed MCP. Do not install a wrapper or scanner
just to consult a record. Reuse suitable existing dependency audit results,
checking their source, target revision, coverage and freshness.

## Dependency advisory lookup

1. Resolve package name, ecosystem and exact version from the authoritative
   lockfile/build artifact, including relevant transitive dependencies and
   build/install paths. For a proposed dependency, label the proposed version;
   do not claim it is installed. A broad manifest range is not an exact version.
2. Consult OSV for selected or changed dependency identities. Reuse a project
   dependency inventory for unchanged modules; requery after version changes or
   stale evidence under project policy. No zero-cost/freshness guarantee.
3. Use [POST /v1/query](https://google.github.io/osv.dev/post-v1-query/)
   for package/version or commit. Use
   [POST /v1/querybatch](https://google.github.io/osv.dev/post-v1-querybatch/)
   when multiple relevant identities can be queried together. Respect the
   documented identity combinations, pagination and actual tool schema.
   Batch responses provide IDs/modified timestamps; retrieve selected full
   records through the documented vulnerability endpoint before judging impact.
4. Record query time, package identity, target revision, advisory ID/aliases,
   affected ranges, withdrawn status where present, original advisory and
   documented fix/mitigation. Do not invent a fixed version or rely on severity
   alone. Verify candidate replacement versions against compatibility and their
   own applicable advisories.
5. Assess runtime AND build/install reachability, actual configuration, existing
   mitigations and patch provenance. Development-only does not automatically
   mean harmless. Matching an affected range is an advisory match, not proof
   that this application is exploitable.

Send only authorized public dependency identities in remote queries, never
private source, secrets, customer data, private packages or unapproved private
commit hashes. Use an approved local/offline route or record a coverage limit
when remote metadata disclosure is not authorized.

Empty results mean no matching known advisory was returned for that query,
not that the dependency/application is safe. Unknown versions, unsupported
ecosystems, failed requests and incomplete pagination remain explicit limits.

## Turn prevention into an executable contract

For each applicable risk/control, record in existing spec/security fields:
source and version, affected component/flow, preconditions, invariant,
enforcement point, allowed/rejected behavior, mitigation or version decision,
linked microtask and negative/regression test with observable outcome.
Record the ASVS version and applicable control ID instead of copying its
entire checklist. Reuse approved decisions; ask only for material unresolved
scope or business-policy changes. Do not silently replace dependencies.

Example: an actor from tenant A requests an order belonging to tenant B.
Require server-side authorization against the authenticated tenant on every
applicable entry point; the negative test must deny access without exposing the
order, while the legitimate owner's operation still succeeds. UI hiding is not
the enforcement point. This example is a planning control, not a discovered CVE.

Route the mapped requirement/microtask/acceptance/planned validation through
the existing SDD consistency check. A missing material control blocks the
affected readiness claim, not unrelated modules. Reconcile card/JSON revisions.
Final Security/QA execute the checks on the implemented revision; preserve
finding validation, false-positive and external publication gates.
Planning checks do not establish CONFIRMED findings or SECURITY_STATUS PASS,
and documenting prevention does not guarantee an error-free implementation.
