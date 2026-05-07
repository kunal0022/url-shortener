from flask import Flask, request, jsonify
import redis, hashlib, os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource

resource = Resource.create({"service.name": "url-shortener-api"})
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://jaeger.observability.svc:4317"
    ),
    insecure=True
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RedisInstrumentor().instrument()

r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=6379, decode_responses=True
)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'version': 'v2', 'author': 'kunal'})

@app.route('/shorten', methods=['POST'])
def shorten():
    with tracer.start_as_current_span("shorten-url"):
        url = request.json['url']
        code = hashlib.md5(url.encode()).hexdigest()[:6]
        r.set(code, url)
        return jsonify({'short_code': code, 'url': f'/r/{code}'})

@app.route('/r/<code>')
def resolve(code):
    with tracer.start_as_current_span("resolve-url"):
        url = r.get(code)
        if url:
            return jsonify({'original_url': url})
        return jsonify({'error': 'not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
