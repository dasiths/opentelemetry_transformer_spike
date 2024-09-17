# OpenTelemetry Collector: Handling PII data example

## All-in-one with Azure Monitor trace sink
Utilising grafana/otel-lgtm, and an Application Insights with connection string defined in environment variable `${env:APPLICATIONINSIGHTS_CONNECTION_STRING}`

## Design

![Design](design.png)

## Filtered backend

![Filtered backend](filtered-backend.png)

- `known-span-with-sensitive-attributes` span's `user` attribute value is redacted.
- Names and attributes of spans or span events with `"has_pii": "true"` attribute is redacted.
- `known-sensitive-span` span attributes and events are redacted.
- Tax File Numbers are redacted from spans and span events.

## Unfiltered backend

![Unfiltered backend](unfiltered-backend.png)

- Tax File Numbers are redacted from spans and span events.
- All other spans and associated events (logs) are shown.
