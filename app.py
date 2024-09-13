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
        span.set_attribute("app_name", "test")
        span.set_attribute("user_input", "My tax file number is 123456789")
        span.add_event("Event 1: TFN in attributes", {"tfn": "123456789"})
        span.add_event("Event 2: TFN in name - 123456789")
        print("doing some work...")
        mixed_function()

def mixed_function():
    with tracer.start_as_current_span("known-span-with-sensitive-attributes") as span:
        span.set_attribute("user", "someone")
        span.add_event("Event 3: No sensitive data", {"foo": "bar"})
        span.add_event("Event 4: Explicit PII event", {"foo": "bar", "has_pii": "true"})
        print("simulating a mixed function which has a sensitive attributes...")
        log_ppi_data()

def log_ppi_data():
    with tracer.start_as_current_span("known-sensitive-span", attributes={"has_pii": "true"}) as span:
        span.add_event("Event 5: Implicit PII event", {"foo": "bar"})
        print("doing some work with PII...")

if __name__ == "__main__":
    do_work()