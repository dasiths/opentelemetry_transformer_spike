from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# https://opentelemetry.io/docs/languages/python/exporters/#otlp-dependencies

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "your-service-name"
})

traceProvider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
processor = BatchSpanProcessor(otlp_exporter)
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def do_work():
    with tracer.start_as_current_span("parent-span") as span:
        span.set_attribute("name", "test")
        print("doing some work...")
        mixed_function()

def mixed_function():
    with tracer.start_as_current_span("known-span-with-sensitive-attributes") as span:
        span.set_attribute("user", "someone")
        span.add_event("Some event", {"event1": "value"})
        span.add_event("Explicit PII event", {"event2": "value", "has_pii": "true"})
        print("simulating a mixed function which has a sensitive attributes...")
        log_ppi_data()

def log_ppi_data():
    with tracer.start_as_current_span("sensitive-span") as span:
        span.set_attribute("has_pii", "true")
        span.add_event("Implicit PII event", {"event3": "value"})
        span.add_event("Explicit PII event", {"event4": "value", "has_pii": "true"})
        print("doing some work with PII...")

if __name__ == "__main__":
    do_work()