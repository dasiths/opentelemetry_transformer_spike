# OpenTelemetry Collector: Handling PII data example

## Design

![Design](design.png)

## Filtered backend

![Filtered backend](filtered-backend.png)

- `known-span-with-sensitive-attributes` span's `user` attribute value is redacted.
- `Explicit PII event` with `"has_pii": "true"` is filtered out.
- `sensitive-span` with `"has_pii": "true"` span is filtered out.

## Unfiltered backend

![Unfiltered backend](unfiltered-backend.png)

- All spans and associated events (logs) are shown.
