from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# https://opentelemetry.io/docs/languages/python/exporters/#otlp-dependencies

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "new-service-name"
})

traceProvider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
processor = BatchSpanProcessor(otlp_exporter)
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

def calling_autoinstrumented_libA():
        with tracer.start_as_current_span("auto-instrumented-span-to-suppress") as span:
          span.set_attribute("app_name", "libA")
          span.set_attribute("api_key", "TFN 123456789")
          span.add_event("Event 1: Calling API")
          span.add_event("Event 2: Returned TFN 123456789")
          span.add_event("Event 3: Returned TFN 12345678 something and CC 123 456789 012-3456")
          span.add_event("1234567890123456")
          span.add_event("Event 5: Returned CC 123 456789 012-3456")
    
def calling_autoinstrumented_libB():
        with tracer.start_as_current_span("another-span-to-suppress") as span:
          span.set_attribute("app_name", "libB")
          span.set_attribute("api_key", "123456789")
          span.add_event("Event 1: Calling API")
          span.add_event("Event 2: Returned 123456")
    
def calling_autoinstrumented_libC():
        with tracer.start_as_current_span("yet-another-span-to-suppress") as span:
          span.set_attribute("app_name", "libC")
          span.set_attribute("api_key", "123456789")
          span.add_event("Event 1: Calling API")
          span.add_event("Event 2: Returned 123456")
          with tracer.start_span("subspan-of-yet-another-span-to-suppress") as subspan:
            subspan.set_attribute("app_name", "libC")
            subspan.set_attribute("api_key", "123456789")
            subspan.add_event("Event 1: Calling API")
            subspan.add_event("Event 2: Returned 123456")

def calling_autoinstrumented():
    calling_autoinstrumented_libA()
    calling_autoinstrumented_libB()
    # calling_autoinstrumented_libC()

def do_work():
    with tracer.start_as_current_span("oblivious-to-sensitivity") as span:
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
        span.add_event("Event 4: Explicit PII event", {"foo": "bar", "is_sensitive": "true"})
        print("simulating a mixed function which has a sensitive attributes...")
        log_ppi_data()

def log_ppi_data():
    with tracer.start_as_current_span("known-sensitive-span", attributes={"is_sensitive": "true"}) as span:
        span.add_event("Event 5: Implicit PII event", {"foo": "bar"})
        print("doing some work with PII...")

if __name__ == "__main__":
    # do_work()
    calling_autoinstrumented()