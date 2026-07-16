from prometheus_client import Counter, Gauge

# Métricas de Negocio
taller_diego_domain_validation_failures_total = Counter(
    'taller_diego_domain_validation_failures_total',
    'Rechazos por Invariantes de Dominio',
    ['aggregate', 'invariant_rule']
)

taller_diego_sales_registered_total = Counter(
    'taller_diego_sales_registered_total',
    'Ventas Procesadas (Volumen de Negocio)'
)

# Métricas de Infraestructura
taller_diego_database_connections_active = Gauge(
    'taller_diego_database_connections_active',
    'Medidor de Conexiones a la Base de Datos'
)

taller_diego_cache_requests_total = Counter(
    'taller_diego_cache_requests_total',
    'Contador de Fallos y Aciertos de Caché',
    ['result', 'entity']
)
