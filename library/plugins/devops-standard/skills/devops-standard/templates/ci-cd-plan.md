# CI/CD pipeline plan

Adapted from Vasiliy Uvarov's MIT CI/CD Pipeline Template. See
[ORIGIN](../references/ORIGIN.md) and the bundle's THIRD_PARTY_NOTICES.md.
Planning template only, not executable deployment authorization.

## Overview

- Service/application:
- Pipeline: build-only / build+deploy / approved environment promotion / GitOps
- Existing target: VM/server / existing containers / Kubernetes / other
- Build artifact: image / binary / package / plan / chart
- Source revision / immutable artifact identity / owner:

## Stage design

Record the actual native command and evidence for each applicable stage:

| Stage | Command/config | Expected result | Evidence/status |
| --- | --- | --- | --- |
| Source trigger and static analysis | | | |
| Build | | | |
| Unit/integration tests | | | |
| Security checks, security-standard owner | | | |
| Artifact packaging | | | |
| Authorized staging deployment | | | |
| Smoke tests | | | |
| Explicit human production approval | | | |
| Production deployment, only when separately approved | | | |
| Verification and monitoring | | | |

No unconditional publication, deploy or GitOps push examples. Pipeline syntax
validation does not dispatch a production workflow.

## Build and test checklist

- [ ] Build inputs/dependencies are reproducible and reviewed.
- [ ] Artifact identifies its source commit; promotion uses immutable identity.
- [ ] Unit/integration tests passed with isolated data and cleanup ownership.
- [ ] Security owner reviewed relevant credentials, permissions and scanners.
- [ ] YAML/config and provider-specific validation passed; actionlint for Actions.
- [ ] Optional act execution, if used, was scoped and isolated, not production.

## Promotion and approval

- Strategy already selected by project: rolling / blue-green / canary / other:
- Environment, service, approval evidence and permitted operation:
- Baseline health, service-path test, thresholds and observation window:
- Error budget/capacity constraints and release notes:
- Previous artifact retained and schema/data compatibility checked:

## Rollback plan

Rollback Trigger:
Rollback Method:
Rollback Steps:
Validation After Rollback:
Rollback limitations or irreversible effects:
Expected recovery target and measured evidence, no guaranteed fixed duration:

## Final review

- [ ] Promotion and rollback scope are explicit; production gate has not been bypassed.
- [ ] Runtime behavior/monitoring checked separately from configuration validity.
- [ ] Initial failures, fixes and revalidation are recorded.
- [ ] Unexecuted stages marked NOT VALIDATED, not checked as successful.
