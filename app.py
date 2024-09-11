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
    with tracer.start_as_current_span("test-span-1") as span:
        span.set_attribute("name", "test")
        print("doing some work...")

def function_with_pii():
    with tracer.start_as_current_span("test-span-2") as span:
        span.set_attribute("has_pii", "true")
        span.set_attribute("user", "someone")
        print("doing some work with PII...")

if __name__ == "__main__":
    do_work()
    function_with_pii()