from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from db import status_routes
from db.base import init_db # Importa la función
import time
import os
from prometheus_fastapi_instrumentator import Instrumentator

# --- OpenTelemetry SDK ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
try:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    _OTLP_AVAILABLE = True
except ImportError:
    _OTLP_AVAILABLE = False

# Configurar el proveedor de trazas
_resource = Resource.create({"service.name": "taller-diego-api", "service.version": "1.0.0"})
_provider = TracerProvider(resource=_resource)

# Exportar trazas al OTel Collector si está disponible
_otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
if _OTLP_AVAILABLE and _otel_endpoint:
    _exporter = OTLPSpanExporter(endpoint=_otel_endpoint, insecure=True)
    _provider.add_span_processor(BatchSpanProcessor(_exporter))

trace.set_tracer_provider(_provider)
tracer = trace.get_tracer(__name__)

from src.auth.infrastructure import auth_routes
from src.empleados.infrastructure import empleado_routes
from src.ordenes.infrastructure import orden_routes
from src.autopartes.infrastructure import autoparte_routes
from src.servicios.infrastructure import servicio_routes
from src.ventas.infrastructure import venta_routes
from src.producto.infrastructure import producto_routes

app = FastAPI(
    title="Taller Diego API",
    description="Sistema de gestión para taller mecánico",
    version="1.0.0",
    docs_url=None,
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Middleware de compresión gzip (reduce tamaño de respuestas)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para agregar headers de caché, performance y Trace ID
@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Propagar el Trace ID de OTel en el header de respuesta
    current_span = trace.get_current_span()
    if current_span:
        trace_id = format(current_span.get_span_context().trace_id, "032x")
        response.headers["X-Trace-Id"] = trace_id

    # Agregar header de tiempo de procesamiento
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2)) + "ms"

    # Agregar headers de caché para endpoints de API
    if request.url.path.startswith("/api/v1/"):
        response.headers["Cache-Control"] = "public, max-age=300"

    return response

@app.on_event("startup")
async def startup_event():
    # Inicializa la extensión de la BD solo al arrancar el contenedor
    init_db()

# Iniciar instrumentador de Prometheus y OpenTelemetry
Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)

app.include_router(status_routes.router,
                   prefix="/api/v1/status", tags=["Status"])
app.include_router(auth_routes.router,
                   prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(producto_routes.router,
                   prefix="/api/v1/productos", tags=["Productos"])
app.include_router(autoparte_routes.router,
                   prefix="/api/v1/autopartes", tags=["Autopartes"])
app.include_router(venta_routes.router,
                   prefix="/api/v1/ventas", tags=["Ventas"])
app.include_router(orden_routes.router,
                   prefix="/api/v1/ordenes", tags=["Ordenes"])
app.include_router(servicio_routes.router,
                   prefix="/api/v1/servicios", tags=["Servicios"])
app.include_router(empleado_routes.router,
                   prefix="/api/v1/empleados", tags=["Empleados"])

# Documentación personalizada con colores oscuros
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentación",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai",
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True,
        },
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health/live", tags=["Health"])
def liveness_probe():
    return {"status": "alive"}

@app.get("/health/ready", tags=["Health"])
def readiness_probe():
    # En un escenario real, aquí podrías verificar la conexión a DB
    return {"status": "ready"}


