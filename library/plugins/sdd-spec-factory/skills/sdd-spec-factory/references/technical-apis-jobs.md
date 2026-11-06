# APIs, webhooks and asynchronous jobs

## When to consult
Use for endpoints, external integrations, webhooks, queues or distributed state.
Reuse existing clients/workers/API research and specialist tool ownership.

## Inspect and decide
- Locate current schemas, version policy, auth, consumers, signatures, queue
  configuration, delivery guarantees, retry/dedup stores and error contracts.
- Specify input/output and error schema, pagination, validation limits, backwards
  compatibility and partial failure. Derive HTTP semantics from the operation,
  not an invented convention. Transport idempotency and business idempotency
  need separate verification.
- Define timeout/deadline, retryable failures, maximum attempts, jitter and quota
  handling. Do not retry unsafe operations without a verified deduplication plan.
- Verify webhook signatures against the provider-required raw payload and
  freshness policy before processing. Define duplicate and out-of-order behavior,
  durable acceptance, processing state and reconciliation with provider truth.
- Distinguish publish confirmation from consumer acknowledgment and committed
  business effects. Record exactly what the broker guarantees for this config.
- For DB write plus event publication, compare existing transactional outbox or
  reconciliation with direct publication. Specify crash windows; outbox still
  needs duplicate-safe consumers. Never promise global exactly-once behavior.
- Define ordering scope, poison-message quarantine, retry exhaustion, redrive
  authority and compensation after irreversible side effects. Compensation is
  an approved business action, not a magical cross-service rollback.

## Verification
Test accepted/rejected input, authorization, pagination boundaries, timeout
after remote success, same key with changed payload, webhook duplicate and
reordering, invalid signature and replay. Crash a synthetic worker before and
after commit/ack; check redelivery does not repeat business effects. Test poison
messages and authorized redrive. Mocks prove handling of specified responses;
only an authorized provider/broker sandbox run proves that integration boundary.
Use correlation IDs and attempt/result metrics without logging secret payloads.

## Primary sources
- [HTTP semantics, RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RabbitMQ acknowledgements and confirms](https://www.rabbitmq.com/docs/confirms)
- [Stripe webhooks](https://docs.stripe.com/webhooks)

Checked 2026-10-11. RabbitMQ treats publisher confirms and consumer acknowledgments
as separate mechanisms. Stripe documents duplicate deliveries, signature checks
and lack of guaranteed event order. Both are provider examples, not assumed
dependencies. Pin actual broker/provider/API versions and recheck their behavior.
Retry/outbox/test choices are LOCAL DECISIONS within existing task fields.
