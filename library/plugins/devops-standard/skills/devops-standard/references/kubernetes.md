# Kubernetes

Identify current context, cluster and namespace explicitly, including whether
the API points to production. Inspect manifests/chart dependencies and values
before rendering. Preserve the existing Helm/Kustomize/native choice.

Validation: `helm lint` and `helm template` for a chart, or `kustomize build`
for an overlay; validate rendered resources using `kubeconform` with compatible
schemas/CRDs; then review a context-appropriate dry-run. A missing CRD schema is
a recorded coverage gap, not permission to silently skip schema validation.

`kubectl apply --dry-run=client -f RENDERED` and
`kubectl apply --dry-run=server -f RENDERED` are conditional examples, not
automatic commands. Client mode is not proof of admission/runtime compatibility
and can still need discovery. Server dry-run calls the selected API/admission
stack: require authorized target, context and credentials before invoking it.
Do not describe either mode as an isolated/offline security sandbox.

Production apply/deploy and cluster deletion require explicit human approval;
plain apply is never the syntax-validation default. Review image identity,
probes, requests/limits, persistent storage and rollout/rollback compatibility.
IAM/RBAC, secrets, public ingress/ports and security contexts require security
review. Validate rollout health and a representative service path only when
runtime operations are authorized; schema/dry-run cannot establish that result.

Source: [kubectl apply](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/).
