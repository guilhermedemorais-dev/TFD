# Multistack Security Profiles

Detect the real stack before applying framework-specific rules. Inspect source,
manifests, lockfiles, runtime files, containers, CI/CD, infrastructure, and
deployment configuration. Record exact versions when they affect security
behavior. Do not infer the complete stack from one file extension.

## Profile Selection

Load only applicable profiles and trace shared trust boundaries across them:

| Evidence | Profile focus |
| --- | --- |
| `package.json` and JS/TS lockfile | Node.js, Express, NestJS, React, Next.js, Vue, build and supply chain |
| `composer.json` and `composer.lock` | PHP, Laravel, Symfony, WordPress packages and supply chain |
| `wp-config.php`, plugins or themes | WordPress/WooCommerce capabilities, nonces, REST/AJAX, hooks, uploads and escaping |
| Laravel application files | guards, policies, middleware, mass assignment, validation, queues, signed URLs and Blade escaping |
| Python manifests | framework auth, serializers, templates, task queues and Python supply chain |
| Java or JVM build files | filters, annotations, deserialization, expression languages and JVM supply chain |
| Go modules | handlers, middleware, templates, filesystem/network sinks and Go modules |
| Docker, Compose or Kubernetes | image provenance, users, capabilities, secrets, ports, volumes and network boundaries |
| Nginx, proxy, CDN or ingress config | routing, headers, TLS, request limits, trust forwarding and edge enforcement |
| SQL migrations and database config | roles, ownership, row isolation, constraints, raw queries, backups and exposed ports |
| CI/CD and IaC | token permissions, untrusted build input, artifact provenance, cloud/IAM and environment separation |

This list routes analysis; it is not a vulnerability checklist by itself.

## Version-Aware Rules

For every framework-specific claim:

1. Resolve the installed version from the authoritative lockfile or build output.
2. Prefer repository configuration and official documentation for that version.
3. Verify whether the behavior is runtime, build-time, edge, proxy, database, or
   application controlled.
4. Check central controls and imported wrappers before declaring a missing guard.
5. Tie dependency findings to an applicable advisory and deployed dependency path.
6. Mark unavailable version or deployment evidence as a blind spot, not proof of
   vulnerability.

## Cross-Stack Flow

Follow the complete path when multiple profiles interact:

```text
browser/client -> CDN/proxy -> application route -> middleware/policy ->
service/job -> database/cache/storage/external service
```

A control may live in another layer. Confirm its effectiveness and failure mode
instead of reporting its absence from the file currently under review.
