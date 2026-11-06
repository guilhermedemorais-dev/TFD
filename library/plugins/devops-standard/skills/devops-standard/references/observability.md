# Observability

Start from service behavior/SLOs and existing metrics/logs/traces. Identify
critical user path, baseline, actionable thresholds, owner and observation
window. Avoid generic dashboards with no response procedure. Sanitize labels,
logs and traces; never emit credentials or customer payloads for diagnostics.

For Prometheus use `promtool check config CONFIG` and
`promtool check rules RULES`; use `promtool test rules TEST_FILE` when rule-test
fixtures exist. Validate alert expression semantics, routing and runbook link,
not merely YAML syntax. Configuration paths/fixtures must already be reviewed.
Grafana/OTel use the actual project's supported native configuration/build
checks for the installed version. Do not invent a validator or report PASS
because no command was available; mark NOT VALIDATED and identify the gap.

Test synthetic success/failure signals in an approved isolated environment.
Notification delivery and production alert changes are external effects requiring
scope. Do not disable production alerting for a drill by default. Config passes
do not prove telemetry ingestion, alert delivery or user-facing health.

Source: [promtool](https://prometheus.io/docs/prometheus/latest/command-line/promtool/).
